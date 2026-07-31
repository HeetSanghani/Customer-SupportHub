"""Tickets router — CRUD with ownership enforcement."""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, and_, or_

from app.database import get_session
from app.dependencies import get_current_user, require_role
from app.models import (
    AuditLog, Ticket, TicketChannel, TicketPriority, TicketStatus, User, UserRole
)

router = APIRouter(prefix="/tickets", tags=["tickets"])

# SLA hours per priority
SLA_HOURS = {
    TicketPriority.urgent: 1,
    TicketPriority.high: 4,
    TicketPriority.medium: 8,
    TicketPriority.low: 24,
}


# ─── Schemas ──────────────────────────────────────────────────────────────────

class TicketCreate(BaseModel):
    subject: str
    category: str
    channel: TicketChannel
    priority: TicketPriority = TicketPriority.medium
    body: Optional[str] = None  # first message body


class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    agent_id: Optional[uuid.UUID] = None
    category: Optional[str] = None


class TicketOut(BaseModel):
    id: str
    ref: str
    subject: str
    category: str
    channel: str
    status: str
    priority: str
    sla_due_at: Optional[datetime]
    sla_breached: bool
    ai_resolved: bool
    sentiment: Optional[str]
    ai_confidence: Optional[float]
    customer_id: str
    agent_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, t: Ticket) -> "TicketOut":
        return cls(
            id=str(t.id),
            ref=t.ref,
            subject=t.subject,
            category=t.category,
            channel=t.channel.value,
            status=t.status.value,
            priority=t.priority.value,
            sla_due_at=t.sla_due_at,
            sla_breached=t.sla_breached,
            ai_resolved=t.ai_resolved,
            sentiment=t.sentiment,
            ai_confidence=t.ai_confidence,
            customer_id=str(t.customer_id),
            agent_id=str(t.agent_id) if t.agent_id else None,
            created_at=t.created_at,
            updated_at=t.updated_at,
        )


def _generate_ref(session_sync=None) -> str:
    """Generate a TCK-XXXXX ref (simplified; real impl uses a DB sequence)."""
    import random
    return f"TCK-{random.randint(10000, 99999)}"


def _compute_sla(priority: TicketPriority) -> datetime:
    hours = SLA_HOURS.get(priority, 8)
    return datetime.utcnow() + timedelta(hours=hours)


# ─── Routes ───────────────────────────────────────────────────────────────────

@router.post("/", response_model=TicketOut, status_code=201)
async def create_ticket(
    body: TicketCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    ticket = Ticket(
        ref=_generate_ref(),
        customer_id=current_user.id,
        subject=body.subject,
        category=body.category,
        channel=body.channel,
        priority=body.priority,
        sla_due_at=_compute_sla(body.priority),
    )
    session.add(ticket)
    
    # Need to flush to get the ticket ID
    await session.commit()
    await session.refresh(ticket)
    
    from app.models import Message, SenderType
    if body.body:
        initial_message = Message(
            ticket_id=ticket.id,
            sender_id=current_user.id,
            sender_type=SenderType.customer,
            body=body.body
        )
        session.add(initial_message)
        
    # Always add a greeting from the AI
    greeting_message = Message(
        ticket_id=ticket.id,
        sender_id=None,
        sender_type=SenderType.ai,
        body="Hello! I am your AI Assistant. How can I help you today?"
    )
    session.add(greeting_message)
    await session.commit()
    
    return TicketOut.from_orm(ticket)


@router.get("/", response_model=List[TicketOut])
async def list_tickets(
    status_filter: Optional[TicketStatus] = Query(None, alias="status"),
    channel: Optional[TicketChannel] = None,
    priority: Optional[TicketPriority] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Ticket).where(Ticket.deleted_at.is_(None))

    # Ownership: customers only see their own tickets
    if current_user.role == UserRole.customer:
        stmt = stmt.where(Ticket.customer_id == current_user.id)

    if status_filter:
        stmt = stmt.where(Ticket.status == status_filter)
    if channel:
        stmt = stmt.where(Ticket.channel == channel)
    if priority:
        stmt = stmt.where(Ticket.priority == priority)

    stmt = stmt.order_by(Ticket.created_at.desc()).offset(skip).limit(limit)
    result = await session.exec(stmt)
    tickets = result.all()
    return [TicketOut.from_orm(t) for t in tickets]


@router.get("/{ticket_id}", response_model=TicketOut)
async def get_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")
    # Customers can only see their own tickets
    if current_user.role == UserRole.customer and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return TicketOut.from_orm(ticket)


@router.patch("/{ticket_id}", response_model=TicketOut)
async def update_ticket(
    ticket_id: uuid.UUID,
    body: TicketUpdate,
    current_user: User = Depends(require_role(UserRole.agent)),
    session: AsyncSession = Depends(get_session),
):
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")

    old_status = ticket.status

    if body.status is not None:
        ticket.status = body.status
    if body.priority is not None:
        ticket.priority = body.priority
        ticket.sla_due_at = _compute_sla(body.priority)
    if body.agent_id is not None:
        ticket.agent_id = body.agent_id
    if body.category is not None:
        ticket.category = body.category

    ticket.updated_at = datetime.utcnow()
    session.add(ticket)

    # Audit log
    session.add(AuditLog(
        actor_id=current_user.id,
        action="ticket.updated",
        entity_type="ticket",
        entity_id=str(ticket.id),
        ticket_id=ticket.id,
        diff_json=f'{{"old_status": "{old_status}", "new_status": "{ticket.status}"}}',
    ))
    await session.commit()
    await session.refresh(ticket)
    return TicketOut.from_orm(ticket)


class MessageOut(BaseModel):
    id: str
    ticket_id: str
    sender_id: Optional[str]
    sender_name: Optional[str]
    sender_role: Optional[str]
    sender_type: str
    body: str
    created_at: datetime


@router.get("/{ticket_id}/messages", response_model=List[MessageOut])
async def get_ticket_messages(
    ticket_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    if current_user.role == UserRole.customer and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    from app.models import Message
    from sqlmodel import select
    from sqlalchemy.orm import selectinload

    stmt = select(Message).where(Message.ticket_id == ticket_id).order_by(Message.created_at.asc()).options(selectinload(Message.sender))
    result = await session.exec(stmt)
    messages = result.all()

    return [
        MessageOut(
            id=str(m.id),
            ticket_id=str(m.ticket_id),
            sender_id=str(m.sender_id) if m.sender_id else None,
            sender_name=m.sender.name if m.sender else ("System" if m.sender_type == "system" else "AI Agent"),
            sender_role=m.sender.role.value if m.sender else None,
            sender_type=m.sender_type.value,
            body=m.body,
            created_at=m.created_at
        ) for m in messages
    ]


@router.delete("/{ticket_id}", status_code=204)
async def soft_delete_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(require_role(UserRole.admin)),
    session: AsyncSession = Depends(get_session),
):
    ticket = await session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.deleted_at = datetime.utcnow()
    session.add(ticket)
    await session.commit()


# ─── CSAT Endpoints ────────────────────────────────────────────────────────────

class CsatCreate(BaseModel):
    rating: int
    comment: Optional[str] = None


@router.get("/csat/my-reviews")
async def get_my_csat_reviews(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    from app.models import CsatRating
    from sqlalchemy.orm import selectinload
    stmt = (
        select(CsatRating)
        .where(CsatRating.customer_id == current_user.id)
        .options(selectinload(CsatRating.ticket))
        .order_by(CsatRating.created_at.desc())
    )
    result = await session.exec(stmt)
    csats = result.all()
    return [
        {
            "id": str(c.id),
            "ticket_id": str(c.ticket_id),
            "rating": c.rating,
            "comment": c.comment,
            "created_at": c.created_at,
            "ticket_ref": c.ticket.ref if c.ticket else "N/A",
            "ticket_subject": c.ticket.subject if c.ticket else "N/A"
        }
        for c in csats
    ]


@router.get("/csat/all")
async def get_all_csat_reviews(
    current_user: User = Depends(require_role(UserRole.agent)),
    session: AsyncSession = Depends(get_session),
):
    from app.models import CsatRating
    from sqlalchemy.orm import selectinload
    stmt = (
        select(CsatRating)
        .options(selectinload(CsatRating.ticket), selectinload(CsatRating.customer))
        .order_by(CsatRating.created_at.desc())
    )
    result = await session.exec(stmt)
    csats = result.all()
    return [
        {
            "id": str(c.id),
            "ticket_id": str(c.ticket_id),
            "rating": c.rating,
            "comment": c.comment,
            "created_at": c.created_at,
            "customer_name": c.customer.name if c.customer else "Customer User",
            "customer_email": c.customer.email if c.customer else "",
            "ticket_ref": c.ticket.ref if c.ticket else "N/A",
            "ticket_subject": c.ticket.subject if c.ticket else "N/A",
            "channel": c.ticket.channel.value if (c.ticket and c.ticket.channel) else "email"
        }
        for c in csats
    ]



@router.post("/{ticket_id}/csat", status_code=201)
async def create_csat_rating(
    ticket_id: uuid.UUID,
    payload: CsatCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    from app.models import CsatRating
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if current_user.role == UserRole.customer and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Check if rating already exists
    existing = await session.exec(select(CsatRating).where(CsatRating.ticket_id == ticket_id))
    if existing.first():
        raise HTTPException(status_code=400, detail="CSAT rating already submitted for this ticket")

    csat = CsatRating(
        ticket_id=ticket_id,
        customer_id=current_user.id,
        rating=payload.rating,
        comment=payload.comment
    )
    session.add(csat)
    await session.commit()
    await session.refresh(csat)
    return {"id": str(csat.id), "rating": csat.rating, "comment": csat.comment}


@router.get("/{ticket_id}/csat")
async def get_csat_rating(
    ticket_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    from app.models import CsatRating
    existing = await session.exec(select(CsatRating).where(CsatRating.ticket_id == ticket_id))
    rating = existing.first()
    if not rating:
        return None
    return {"id": str(rating.id), "rating": rating.rating, "comment": rating.comment}



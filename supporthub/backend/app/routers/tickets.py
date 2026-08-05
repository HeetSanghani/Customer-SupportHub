"""Tickets router — CRUD with ownership enforcement."""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile
from fastapi.responses import HTMLResponse
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
    return datetime.now() + timedelta(hours=hours)


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
        
    # Contextual professional response from AI / System
    customer_name = current_user.name or 'there'
    if ticket.channel == TicketChannel.email:
        ai_reply_body = f"Hello {customer_name}! Thank you for reaching out to SupportHub Email Support regarding '{ticket.subject}'. We have received your inquiry (Ref: {ticket.ref}). Our support team will review your request and get back to you shortly."
    elif body.body:
        ai_reply_body = f"Hello {customer_name}! I have received your request regarding '{ticket.subject}'. Our support team and AI system are reviewing your inquiry."
    else:
        ai_reply_body = f"Hello {customer_name}! How can I assist you with your support request today?"

    greeting_message = Message(
        ticket_id=ticket.id,
        sender_id=None,
        sender_type=SenderType.ai,
        body=ai_reply_body
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

    old_status_str = str(ticket.status.value if hasattr(ticket.status, 'value') else ticket.status)

    if body.status is not None:
        ticket.status = body.status
    if body.priority is not None:
        ticket.priority = body.priority
        ticket.sla_due_at = _compute_sla(body.priority)
    if body.agent_id is not None:
        ticket.agent_id = body.agent_id
    if body.category is not None:
        ticket.category = body.category

    # Auto-generate Resolution Email & 1-Click CSAT Survey if resolved
    new_status_str = str(ticket.status.value if hasattr(ticket.status, 'value') else ticket.status)
    if old_status_str not in ("resolved", "closed") and new_status_str in ("resolved", "closed"):
        from app.models import Message, SenderType
        csat_survey_html = f"""
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
             <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>
             <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [{ticket.ref}]</strong>
          </div>
          <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your email support inquiry <strong>"{ticket.subject}"</strong> has been resolved. How would you rate your support experience today?</p>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
             <a href="http://localhost:8001/api/v1/tickets/{ticket.id}/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>
             <a href="http://localhost:8001/api/v1/tickets/{ticket.id}/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>
             <a href="http://localhost:8001/api/v1/tickets/{ticket.id}/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>
             <a href="http://localhost:8001/api/v1/tickets/{ticket.id}/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>
          </div>
          <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this email thread to automatically reopen your ticket.</p>
        </div>
        """
        session.add(Message(
            ticket_id=ticket.id,
            sender_id=None,
            sender_type=SenderType.ai,
            body=f"Your email inquiry [{ticket.ref}] has been marked as resolved. If your issue is not fully resolved, simply reply to this email to automatically reopen your ticket.",
            body_html=csat_survey_html
        ))

    ticket.updated_at = datetime.now()
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
    body_html: Optional[str] = None
    attachments: Optional[str] = None
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
            body_html=m.body_html,
            attachments=m.attachments,
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
    ticket.deleted_at = datetime.now()
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


@router.get("/{ticket_id}/rate-email", response_class=HTMLResponse)
async def rate_email_ticket(
    ticket_id: uuid.UUID,
    rating: int = Query(5, ge=1, le=5),
    comment: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
):
    from app.models import CsatRating
    ticket = await session.get(Ticket, ticket_id)
    if not ticket:
        return HTMLResponse("<h2>Ticket not found</h2>", status_code=404)
        
    existing = await session.exec(select(CsatRating).where(CsatRating.ticket_id == ticket_id))
    csat = existing.first()
    if not csat:
        csat = CsatRating(
            ticket_id=ticket_id,
            customer_id=ticket.customer_id,
            rating=rating,
            comment=comment or f"Submitted via 1-Click Email Survey ({rating}/5 stars)"
        )
        session.add(csat)
        await session.commit()
    else:
        csat.rating = rating
        if comment:
            csat.comment = comment
        session.add(csat)
        await session.commit()

    stars_rendered = "★" * rating + "☆" * (5 - rating)
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Thank You for Your Feedback - SupportHub</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F6F7FC; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }}
            .card {{ background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); text-align: center; max-width: 440px; width: 100%; border: 1px solid #E5E7F3; }}
            .icon-badge {{ width: 64px; height: 64px; background: #ECFDF5; color: #10B981; border-radius: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 32px; font-weight: bold; }}
            .stars {{ color: #FBBF24; font-size: 36px; margin: 20px 0; letter-spacing: 4px; }}
            .btn {{ display: inline-block; background: #6366F1; color: white; font-weight: 700; text-decoration: none; padding: 14px 28px; border-radius: 14px; margin-top: 24px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; transition: background 0.2s ease; }}
            .btn:hover {{ background: #4F46E5; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="icon-badge">✓</div>
            <h2 style="color: #1C1B2E; margin: 0 0 10px 0; font-size: 22px;">Thank You for Your Feedback!</h2>
            <p style="color: #6C7089; font-size: 14px; line-height: 1.6; margin: 0;">Your rating of <strong>{rating} out of 5 stars</strong> has been successfully recorded for ticket <strong style="font-family: monospace; color: #4F46E5;">{ticket.ref}</strong>.</p>
            <div class="stars">{stars_rendered}</div>
            <p style="color: #9598B0; font-size: 12px; margin: 0;">Your feedback helps our team continuously improve our support experience.</p>
            <a href="http://localhost:5173/customer" class="btn">Return to SupportHub</a>
        </div>
    </body>
    </html>
    """)


import os

@router.post("/{ticket_id}/upload")
async def upload_ticket_attachment(
    ticket_id: uuid.UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")

    upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))
    os.makedirs(upload_dir, exist_ok=True)

    file_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(upload_dir, file_filename)

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    file_url = f"http://localhost:8001/static/uploads/{file_filename}"
    return {
        "filename": file.filename,
        "url": file_url,
        "size": len(contents),
        "content_type": file.content_type
    }



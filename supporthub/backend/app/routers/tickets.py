"""Tickets router — CRUD with ownership enforcement."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, and_, or_
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from app.config import get_settings
from app.database import get_session
from app.dependencies import get_current_user, require_role
from app.models import (
    AuditLog, Message, SenderType, Ticket, TicketChannel, TicketEmbedding, TicketPriority, TicketStatus, User, UserRole
)

from app.services.ai.orchestrator import AIOrchestrator

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
    subject: Optional[str] = "Support Conversation"
    category: Optional[str] = "general"
    channel: TicketChannel = TicketChannel.website_chat
    priority: TicketPriority = TicketPriority.medium
    body: Optional[str] = None  # first message body

    @field_validator('channel', mode='before')
    @classmethod
    def normalize_channel(cls, v):
        if isinstance(v, str) and v.lower() in ('web', 'chat', 'website', 'web_chat'):
            return TicketChannel.website_chat
        return v

    @field_validator('subject', mode='before')
    @classmethod
    def normalize_subject(cls, v):
        if v is None or not str(v).strip():
            return "Support Conversation"
        return str(v).strip()

    @field_validator('category', mode='before')
    @classmethod
    def normalize_category(cls, v):
        if v is None or not str(v).strip():
            return "general"
        return str(v).strip()


class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    agent_id: Optional[uuid.UUID] = None
    category: Optional[str] = None


class CustomerOut(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    channel_customer_id: Optional[str] = None
    avatar_url: Optional[str] = None


class AgentOut(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None


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
    customer: Optional[CustomerOut] = None
    agent: Optional[AgentOut] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, t: Ticket, customer_obj: Optional[User] = None, agent_obj: Optional[User] = None) -> "TicketOut":
        cust_out = None
        cust = customer_obj
        if not cust and 'customer' in getattr(t, '__dict__', {}):
            cust = t.__dict__['customer']
        if cust:
            cust_out = CustomerOut(
                id=str(cust.id),
                name=cust.name,
                email=cust.email,
                phone=cust.phone,
                channel_customer_id=cust.channel_customer_id,
                avatar_url=cust.avatar_url,
            )
        ag_out = None
        ag = agent_obj
        if not ag and 'agent' in getattr(t, '__dict__', {}):
            ag = t.__dict__['agent']
        if ag:
            ag_out = AgentOut(
                id=str(ag.id),
                name=ag.name,
                email=ag.email,
                avatar_url=ag.avatar_url,
            )
        return cls(
            id=str(t.id),
            ref=t.ref,
            subject=t.subject,
            category=t.category,
            channel=t.channel.value if hasattr(t.channel, 'value') else str(t.channel),
            status=t.status.value if hasattr(t.status, 'value') else str(t.status),
            priority=t.priority.value if hasattr(t.priority, 'value') else str(t.priority),
            sla_due_at=t.sla_due_at,
            sla_breached=t.sla_breached,
            ai_resolved=t.ai_resolved,
            sentiment=t.sentiment,
            ai_confidence=t.ai_confidence,
            customer_id=str(t.customer_id),
            agent_id=str(t.agent_id) if t.agent_id else None,
            customer=cust_out,
            agent=ag_out,
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

async def _ai_classify_ticket(ticket_id: uuid.UUID, subject: str, body_text: str, current_category: str):
    """Background task: use Gemini to auto-classify category, priority and sentiment."""
    try:
        import asyncio
        import google.generativeai as genai
        from app.database import engine

        prompt = f"""Classify this customer support ticket and respond with ONLY valid JSON.

Ticket Subject: {subject}
Message: {body_text[:500]}
Current Category: {current_category}

Respond with exactly this JSON format (no markdown, no explanation):
{{
  "category": "<one of: Billing, Technical, Account, General, Security, Shipping, Orders>",
  "priority": "<one of: low, medium, high, urgent>",
  "sentiment": "<one of: positive, neutral, negative, frustrated>"
}}

Rules:
- "urgent"/"high" priority only if customer mentions downtime, data loss, legal threats, or explicit emergency
- "frustrated" sentiment if customer uses angry or impatient language
- Pick the single best-matching category"""

        model = genai.GenerativeModel("gemini-flash-lite-latest")
        response = await asyncio.to_thread(model.generate_content, prompt)
        raw = response.text.strip().strip("```json").strip("```").strip()

        import json
        data = json.loads(raw)

        async with AsyncSession(engine) as task_session:
            ticket = await task_session.get(Ticket, ticket_id)
            if ticket:
                if data.get("category") and data["category"].lower() != "general" or current_category == "General Support":
                    ticket.category = data["category"]
                if data.get("priority") and data["priority"] in ["low", "medium", "high", "urgent"]:
                    ticket.priority = TicketPriority(data["priority"])
                    ticket.sla_due_at = _compute_sla(ticket.priority)
                if data.get("sentiment"):
                    ticket.sentiment = data["sentiment"]
                task_session.add(ticket)
                await task_session.commit()
    except Exception:
        pass  # Silently fail — auto-classify is best-effort



@router.post("/", response_model=TicketOut, status_code=201)
async def create_ticket(
    body: TicketCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    ticket_subj = body.subject or "Support Conversation"
    ticket_cat = body.category or "general"
    ticket = Ticket(
        ref=_generate_ref(),
        customer_id=current_user.id,
        subject=ticket_subj,
        category=ticket_cat,
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
        await session.commit()

        # Dynamic AI subject extraction from initial customer message
        try:
            from app.ai.subject import is_generic_subject, format_subject_from_query
            if is_generic_subject(ticket.subject):
                ai_subj = format_subject_from_query(body.body)
                if ai_subj and ai_subj.lower() != ticket.subject.lower():
                    ticket.subject = ai_subj
                    session.add(ticket)
                    await session.commit()
                    await session.refresh(ticket)
        except Exception:
            pass
        
    # Contextual response from AI / System
    customer_name = current_user.name or 'there'
    if ticket.channel == TicketChannel.email:
        ai_reply_body = f"Hello {customer_name}! Thank you for reaching out to SupportHub Email Support regarding '{ticket.subject}'. We have received your inquiry (Ref: {ticket.ref}). Our support team will review your request and get back to you shortly."
        greeting_message = Message(
            ticket_id=ticket.id,
            sender_id=None,
            sender_type=SenderType.ai,
            body=ai_reply_body
        )
        session.add(greeting_message)
        await session.commit()
    elif body.body:
        # Process the common question / inquiry via AI Orchestrator to generate an instant answer & update agent inbox
        try:
            from app.services.ai.live_chat_adapter import live_chat_ai_adapter
            await live_chat_ai_adapter.process_live_chat_message(
                ticket_id=str(ticket.id),
                message_body=body.body,
            )
        except Exception as exc:
            logger.error("[create_ticket] AI live chat processing error: %s", exc)
            fallback_greeting = Message(
                ticket_id=ticket.id,
                sender_id=None,
                sender_type=SenderType.ai,
                body=f"Hello {customer_name}! I have received your request regarding '{ticket.subject}'. Our support team and AI system are reviewing your inquiry."
            )
            session.add(fallback_greeting)
            await session.commit()
    else:
        greeting_message = Message(
            ticket_id=ticket.id,
            sender_id=None,
            sender_type=SenderType.ai,
            body=f"Hello {customer_name}! How can I assist you with your support request today?"
        )
        session.add(greeting_message)
        await session.commit()

    # Phase 6: Background AI auto-classification (category, priority, sentiment)
    import asyncio
    asyncio.create_task(_ai_classify_ticket(ticket.id, body.subject, body.body or "", body.category))

    # Evaluate Workflow Automations
    from app.services.automations.engine import evaluate_ticket_automations
    await evaluate_ticket_automations(
        session=session,
        ticket=ticket,
        event_type="ticket_created",
        message_body=body.body,
    )

    return TicketOut.from_orm(ticket)


@router.get("/", response_model=List[TicketOut])
async def list_tickets(
    status_filter: Optional[TicketStatus] = Query(None, alias="status"),
    channel: Optional[TicketChannel] = None,
    priority: Optional[TicketPriority] = None,
    human_only: Optional[bool] = Query(None),
    all_tickets: Optional[bool] = Query(False),
    skip: int = 0,
    limit: int = Query(50, le=200),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Ticket).where(Ticket.deleted_at.is_(None)).options(selectinload(Ticket.customer), selectinload(Ticket.agent))

    # Ownership: customers only see their own tickets
    if current_user.role == UserRole.customer:
        stmt = stmt.where(Ticket.customer_id == current_user.id)

    # Human intervention filtering for Agent role or when human_only=True requested
    should_filter_human = human_only is True or (
        current_user.role == UserRole.agent and not all_tickets and human_only is not False
    )

    if should_filter_human:
        stmt = stmt.where(
            (Ticket.status == TicketStatus.escalated) |
            (Ticket.agent_id.isnot(None)) |
            (Ticket.priority == TicketPriority.urgent) |
            (Ticket.category.ilike("%escalat%"))
        )

    if status_filter:
        stmt = stmt.where(Ticket.status == status_filter)
    if channel:
        stmt = stmt.where(Ticket.channel == channel)
    if priority:
        stmt = stmt.where(Ticket.priority == priority)

    stmt = stmt.order_by(func.coalesce(Ticket.updated_at, Ticket.created_at).desc(), Ticket.created_at.desc()).offset(skip).limit(limit)
    result = await session.exec(stmt)
    tickets = result.all()
    return [TicketOut.from_orm(t) for t in tickets]


@router.get("/{ticket_id}", response_model=TicketOut)
async def get_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Ticket).where(Ticket.id == ticket_id).options(selectinload(Ticket.customer), selectinload(Ticket.agent))
    result = await session.exec(stmt)
    ticket = result.first()
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
        from app.services.csat_delivery import deliver_csat_survey
        from app.models import User
        customer = await session.get(User, ticket.customer_id)
        if customer:
            await deliver_csat_survey(session, ticket, customer)

    ticket.updated_at = datetime.now()
    session.add(ticket)

    # Audit log
    session.add(AuditLog(
        actor_id=current_user.id,
        action="ticket.updated",
        entity_type="ticket",
        entity_id=str(ticket.id),
        ticket_id=ticket.id,
        diff_json=f'{{"old_status": "{old_status_str}", "new_status": "{ticket.status}"}}',
    ))
    await session.commit()
    await session.refresh(ticket)
    return TicketOut.from_orm(ticket)


@router.post("/{ticket_id}/escalate", response_model=TicketOut)
async def escalate_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Explicitly escalate ticket to human agent (customer or staff)."""
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    old_status = str(ticket.status.value if hasattr(ticket.status, 'value') else ticket.status)
    ticket.status = TicketStatus.escalated
    if ticket.priority == TicketPriority.medium:
        ticket.priority = TicketPriority.high
    ticket.updated_at = datetime.now()
    session.add(ticket)

    session.add(AuditLog(
        actor_id=current_user.id,
        action="ticket.escalated",
        entity_type="ticket",
        entity_id=str(ticket.id),
        ticket_id=ticket.id,
        diff_json=f'{{"old_status": "{old_status}", "new_status": "escalated"}}',
    ))
    await session.commit()
    await session.refresh(ticket)

    # Broadcast WS update
    from app.ws.manager import manager
    await manager.broadcast(str(ticket.id), {
        "type": "ticket_update",
        "status": "escalated",
        "subject": ticket.subject or "",
    })
    await manager.broadcast_to_agents({
        "type": "inbox_update",
        "ticket_id": str(ticket.id),
        "preview": f"Customer requested human escalation for ticket {ticket.ref}",
        "sender_name": current_user.name,
        "subject": ticket.subject or "",
        "status": "escalated",
    })

    return TicketOut.from_orm(ticket)


@router.post("/{ticket_id}/accept", response_model=TicketOut)
async def accept_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(require_role(UserRole.agent)),
    session: AsyncSession = Depends(get_session),
):
    """Agent accepts an escalated or unassigned ticket."""
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")

    old_status = str(ticket.status.value if hasattr(ticket.status, 'value') else ticket.status)
    ticket.agent_id = current_user.id
    ticket.status = TicketStatus.open
    ticket.updated_at = datetime.now()
    session.add(ticket)

    session.add(AuditLog(
        actor_id=current_user.id,
        action="ticket.accepted",
        entity_type="ticket",
        entity_id=str(ticket.id),
        ticket_id=ticket.id,
        diff_json=f'{{"old_status": "{old_status}", "new_status": "open", "agent_id": "{current_user.id}"}}',
    ))

    # Persist System Message in conversation thread
    system_msg = Message(
        ticket_id=ticket.id,
        sender_id=None,
        sender_type=SenderType.system,
        body=f"Agent {current_user.name} accepted this ticket.",
    )
    session.add(system_msg)

    await session.commit()
    await session.refresh(ticket)

    # Broadcast agent_joined and ticket_update WS events
    from app.ws.manager import manager
    await manager.broadcast(str(ticket.id), {
        "type": "agent_joined",
        "agent_id": str(current_user.id),
        "agent_name": current_user.name,
        "joined_at": datetime.now(timezone.utc).isoformat(),
    })
    await manager.broadcast(str(ticket.id), {
        "type": "ticket_update",
        "status": "open",
        "agent_id": str(current_user.id),
        "agent_name": current_user.name,
        "subject": ticket.subject or "",
    })
    await manager.broadcast_to_agents({
        "type": "inbox_update",
        "ticket_id": str(ticket.id),
        "preview": f"Agent {current_user.name} accepted ticket {ticket.ref}",
        "sender_name": current_user.name,
        "subject": ticket.subject or "",
        "status": "open",
    })

    return TicketOut.from_orm(ticket)


@router.post("/{ticket_id}/resolve", response_model=TicketOut)
async def resolve_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Resolve ticket and trigger CSAT survey."""
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    old_status = str(ticket.status.value if hasattr(ticket.status, 'value') else ticket.status)
    ticket.status = TicketStatus.resolved
    ticket.updated_at = datetime.now()
    session.add(ticket)

    session.add(AuditLog(
        actor_id=current_user.id,
        action="ticket.resolved",
        entity_type="ticket",
        entity_id=str(ticket.id),
        ticket_id=ticket.id,
        diff_json=f'{{"old_status": "{old_status}", "new_status": "resolved"}}',
    ))
    await session.commit()

    # Deliver CSAT survey if not already done
    from app.services.csat_delivery import deliver_csat_survey
    customer = await session.get(User, ticket.customer_id)
    if customer:
        try:
            await deliver_csat_survey(session, ticket, customer)
        except Exception:
            pass

    await session.refresh(ticket)

    from app.ws.manager import manager
    await manager.broadcast(str(ticket.id), {
        "type": "ticket_update",
        "status": "resolved",
        "subject": ticket.subject or "",
    })
    await manager.broadcast_to_agents({
        "type": "inbox_update",
        "ticket_id": str(ticket.id),
        "preview": f"Ticket {ticket.ref} resolved",
        "sender_name": current_user.name,
        "subject": ticket.subject or "",
        "status": "resolved",
    })

    return TicketOut.from_orm(ticket)


@router.post("/{ticket_id}/close", response_model=TicketOut)
async def close_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Close a ticket (staff or ticket owner customer)."""
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    old_status = str(ticket.status.value if hasattr(ticket.status, 'value') else ticket.status)
    ticket.status = TicketStatus.closed
    ticket.updated_at = datetime.now()
    session.add(ticket)

    session.add(AuditLog(
        actor_id=current_user.id,
        action="ticket.closed",
        entity_type="ticket",
        entity_id=str(ticket.id),
        ticket_id=ticket.id,
        diff_json=f'{{"old_status": "{old_status}", "new_status": "closed"}}',
    ))
    await session.commit()
    await session.refresh(ticket)

    from app.ws.manager import manager
    await manager.broadcast(str(ticket.id), {
        "type": "ticket_update",
        "status": "closed",
        "subject": ticket.subject or "",
    })
    await manager.broadcast_to_agents({
        "type": "inbox_update",
        "ticket_id": str(ticket.id),
        "preview": f"Ticket {ticket.ref} closed by {current_user.name}",
        "sender_name": current_user.name,
        "subject": ticket.subject or "",
        "status": "closed",
    })

    return TicketOut.from_orm(ticket)


@router.post("/{ticket_id}/reopen", response_model=TicketOut)
async def reopen_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Reopen a resolved or closed ticket."""
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    old_status = str(ticket.status.value if hasattr(ticket.status, 'value') else ticket.status)
    ticket.status = TicketStatus.open
    ticket.updated_at = datetime.now()
    session.add(ticket)

    session.add(AuditLog(
        actor_id=current_user.id,
        action="ticket.reopened",
        entity_type="ticket",
        entity_id=str(ticket.id),
        ticket_id=ticket.id,
        diff_json=f'{{"old_status": "{old_status}", "new_status": "open"}}',
    ))
    await session.commit()
    await session.refresh(ticket)

    from app.ws.manager import manager
    await manager.broadcast(str(ticket.id), {
        "type": "ticket_update",
        "status": "open",
        "subject": ticket.subject or "",
    })
    await manager.broadcast_to_agents({
        "type": "inbox_update",
        "ticket_id": str(ticket.id),
        "preview": f"Ticket {ticket.ref} reopened by {current_user.name}",
        "sender_name": current_user.name,
        "subject": ticket.subject or "",
        "status": "open",
    })

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


class MessageCreate(BaseModel):
    body: str


@router.post("/{ticket_id}/messages", response_model=MessageOut, status_code=201)
async def create_ticket_message(
    ticket_id: uuid.UUID,
    body: MessageCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val == "customer" and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    sender_type = SenderType.agent if role_val in ("agent", "admin", "manager") else SenderType.customer

    # Auto-assign ticket if an agent sends a message on an unassigned ticket
    if role_val in ("agent", "admin", "manager") and ticket.agent_id is None:
        ticket.agent_id = current_user.id
        if ticket.status in (TicketStatus.new, TicketStatus.escalated, TicketStatus.waiting):
            ticket.status = TicketStatus.open
        session.add(AuditLog(
            actor_id=current_user.id,
            action="ticket.auto_assigned",
            entity_type="ticket",
            entity_id=str(ticket.id),
            ticket_id=ticket.id,
            diff_json=f'{{"agent_id": "{current_user.id}", "status": "{ticket.status}"}}',
        ))

    msg = Message(
        ticket_id=ticket.id,
        sender_id=current_user.id,
        sender_type=sender_type,
        body=body.body,
    )

    session.add(msg)
    ticket.updated_at = datetime.now()
    session.add(ticket)
    await session.commit()
    await session.refresh(msg)

    # Generate/update dynamic subject title from customer's inquiry if currently generic
    if sender_type == SenderType.customer:
        try:
            from app.ai.subject import generate_ai_ticket_subject
            ai_subj = await generate_ai_ticket_subject(session, ticket.id)
            if ai_subj and ticket.subject != ai_subj:
                ticket.subject = ai_subj
                session.add(ticket)
                await session.commit()
                await session.refresh(ticket)
                from app.ws.manager import manager
                await manager.broadcast(str(ticket.id), {
                    "type": "ticket_update",
                    "status": str(ticket.status.value if hasattr(ticket.status, 'value') else ticket.status),
                    "subject": ticket.subject,
                    "ai_resolved": getattr(ticket, "ai_resolved", False),
                })
        except Exception:
            pass

    # Broadcast via WebSocket to room & agent inbox
    from app.ws.manager import manager
    await manager.broadcast(str(ticket.id), {
        "type": "message",
        "id": str(msg.id),
        "ticket_id": str(ticket.id),
        "sender_id": str(current_user.id),
        "sender_name": current_user.name,
        "sender_role": role_val,
        "body": msg.body,
        "created_at": msg.created_at.isoformat(),
    })
    await manager.broadcast_to_agents({
        "type": "inbox_update",
        "ticket_id": str(ticket.id),
        "preview": msg.body[:80],
        "sender_name": current_user.name,
        "subject": ticket.subject or "",
        "status": str(ticket.status.value if hasattr(ticket.status, 'value') else ticket.status),
    })

    # BUG-006 Fix: Trigger AI response for follow-up customer inquiries on unassigned tickets
    if sender_type == SenderType.customer and ticket.agent_id is None and ticket.status not in (TicketStatus.resolved, TicketStatus.closed):
        try:
            from app.services.ai.live_chat_adapter import live_chat_ai_adapter
            await live_chat_ai_adapter.process_live_chat_message(
                ticket_id=str(ticket.id),
                message_body=msg.body,
            )
        except Exception as exc:
            logger.error("[create_ticket_message] AI follow-up processing error: %s", exc)

    return MessageOut(
        id=str(msg.id),
        ticket_id=str(msg.ticket_id),
        sender_id=str(msg.sender_id),
        sender_name=current_user.name,
        sender_role=role_val,
        sender_type=msg.sender_type.value if hasattr(msg.sender_type, 'value') else str(msg.sender_type),
        body=msg.body,
        body_html=msg.body_html,
        attachments=msg.attachments,
        created_at=msg.created_at,
    )




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

    backend_url = get_settings().backend_url
    file_url = f"{backend_url}/static/uploads/{file_filename}"
    return {
        "filename": file.filename,
        "url": file_url,
        "size": len(contents),
        "content_type": file.content_type
    }


# ─── Phase 6: AI Agent Tools ──────────────────────────────────────────────────

class SuggestReplyOut(BaseModel):
    suggestion: str
    suggested_reply: Optional[str] = None
    success: bool = True
    is_fallback: bool = False
    confidence: float = 1.0
    latency_ms: int = 0
    is_grounded: bool = True
    grounding_score: float = 1.0
    grounding_violations: List[str] = []

class SummarizeOut(BaseModel):
    summary: str

class SimilarTicketOut(BaseModel):
    id: str
    ref: str
    subject: str
    category: str
    status: str
    similarity: float
    is_fallback: bool = False


@router.post("/{ticket_id}/suggest-reply", response_model=SuggestReplyOut)
async def suggest_reply(
    ticket_id: uuid.UUID,
    tone: Optional[str] = Query(None),
    current_user: User = Depends(require_role(UserRole.agent)),
    session: AsyncSession = Depends(get_session),
):
    """AI drafts a suggested reply based on ticket context, verified against GroundingValidator."""
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")

    from app.models import Message
    from sqlmodel import select as sql_select
    from app.services.ai.knowledge_rag import get_relevant_kb_context
    from app.ai.grounding import GroundingValidator

    msgs_result = await session.exec(
        sql_select(Message)
        .where(Message.ticket_id == ticket_id)
        .order_by(Message.created_at.asc())
        .limit(30)
    )
    messages = list(msgs_result.all())

    customer = None
    if ticket.customer_id:
        customer = await session.get(User, ticket.customer_id)

    search_query = f"{ticket.subject} {ticket.category or ''}"
    if messages:
        for m in reversed(messages):
            if m.body and m.body.strip():
                search_query += f" {m.body.strip()[:100]}"
                break

    kb_context = await get_relevant_kb_context(session, search_query)

    orchestrator = AIOrchestrator(session=session)
    ai_response = await orchestrator.generate_for_ticket(
        ticket=ticket,
        messages=messages,
        customer=customer,
        kb_context=kb_context,
        tone=tone or "standard",
    )

    # Validate grounding against retrieved KB context if context is present
    is_grounded = True
    grounding_score = 1.0
    grounding_violations = []

    if kb_context and ai_response.response_text:
        try:
            validator = GroundingValidator()
            g_result = validator.validate(
                response_text=ai_response.response_text,
                rag_citations=[{"content": kb_context}],
                query=search_query
            )
            is_grounded = g_result.is_grounded
            grounding_score = g_result.confidence
            grounding_violations = g_result.violations
        except Exception as g_exc:
            logger.warning("[AgentAssist WARNING] Grounding validation error: %s", g_exc)

    return SuggestReplyOut(
        suggestion=ai_response.response_text,
        suggested_reply=ai_response.response_text,
        success=True,
        is_fallback=ai_response.is_fallback,
        confidence=ai_response.confidence,
        latency_ms=ai_response.latency_ms,
        is_grounded=is_grounded,
        grounding_score=grounding_score,
        grounding_violations=grounding_violations,
    )


@router.post("/{ticket_id}/summarize", response_model=SummarizeOut)
async def summarize_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(require_role(UserRole.agent)),
    session: AsyncSession = Depends(get_session),
):
    """AI generates a 2-3 sentence summary of the ticket conversation using model adapter."""
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Use cached summary if already generated
    if ticket.ai_summary:
        return SummarizeOut(summary=ticket.ai_summary)

    from app.models import Message
    from sqlmodel import select as sql_select
    msgs_result = await session.exec(
        sql_select(Message)
        .where(Message.ticket_id == ticket_id)
        .order_by(Message.created_at.asc())
        .limit(30)
    )
    messages = list(msgs_result.all())

    if len(messages) < 3:
        summary = f"New ticket: '{ticket.subject}' — conversation just started."
        return SummarizeOut(summary=summary)

    thread_text = "\n".join([
        f"[{m.sender_type.value.upper()}]: {m.body}"
        for m in messages if m.body
    ])

    from app.ai.prompts.response import TICKET_SUMMARIZATION_PROMPT
    from app.services.ai.model_adapter import get_model_adapter
    from app.services.ai.models import Prompt

    system_prompt = TICKET_SUMMARIZATION_PROMPT.format(
        ticket_subject=ticket.subject,
        ticket_category=ticket.category or "General",
        ticket_status=ticket.status.value,
        thread_text=thread_text
    )

    try:
        adapter = get_model_adapter()
        prompt_obj = Prompt(
            system=system_prompt,
            messages=[],
            version="v1.0-summary",
            temperature=0.2,
            max_tokens=250
        )
        raw_res = await adapter.generate(prompt_obj)
        summary = raw_res.get("text", "").strip()
        if not summary:
            raise ValueError("Model adapter returned empty summary text.")
    except Exception as exc:
        logger.exception("[AgentAssist ERROR] Failed to generate ticket summary for ticket_id=%s: %s", ticket_id, str(exc))
        summary = f"Ticket '{ticket.subject}' is currently {ticket.status.value} with {len(messages)} messages exchanged."

    # Cache the summary
    ticket.ai_summary = summary
    session.add(ticket)
    await session.commit()

    return SummarizeOut(summary=summary)


@router.get("/{ticket_id}/similar", response_model=List[SimilarTicketOut])
async def find_similar_tickets(
    ticket_id: uuid.UUID,
    limit: int = Query(3, le=5),
    current_user: User = Depends(require_role(UserRole.agent)),
    session: AsyncSession = Depends(get_session),
):
    """Find similar resolved tickets using pgvector cosine similarity on ticket embeddings."""
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")

    from app.services.ai.ticket_embeddings import (
        ensure_ticket_embedding,
        generate_query_embedding,
        get_ticket_text_for_embedding,
    )
    from sqlmodel import col, type_coerce, Float, select as sql_select
    from sqlalchemy import text

    # Ensure current ticket has a real embedding stored
    await ensure_ticket_embedding(session, ticket)

    query_text = get_ticket_text_for_embedding(ticket)
    query_vec = generate_query_embedding(query_text)

    # 1. Run real pgvector cosine similarity query (<=> operator) against TicketEmbedding
    stmt = (
        sql_select(
            Ticket,
            type_coerce(col(TicketEmbedding.embedding).op("<=>")(query_vec), Float).label("distance")
        )
        .join(TicketEmbedding, Ticket.id == TicketEmbedding.ticket_id)
        .where(
            Ticket.id != ticket_id,
            Ticket.deleted_at.is_(None),
            Ticket.status.in_([TicketStatus.resolved, TicketStatus.closed])
        )
        .order_by(text("distance ASC"))
        .limit(limit)
    )

    results = (await session.exec(stmt)).all()

    output: List[SimilarTicketOut] = []
    seen_ids = set()

    for row_ticket, distance in results:
        # Distance D in pgvector cosine operator <=>: similarity S = 1.0 - D
        sim_score = max(0.0, round(1.0 - float(distance), 4))
        seen_ids.add(row_ticket.id)
        output.append(
            SimilarTicketOut(
                id=str(row_ticket.id),
                ref=row_ticket.ref,
                subject=row_ticket.subject,
                category=row_ticket.category,
                status=row_ticket.status.value,
                similarity=sim_score,
                is_fallback=False
            )
        )

    # 2. Fallback: category/time search for tickets missing embeddings
    if len(output) < limit:
        needed = limit - len(output)
        fallback_stmt = (
            sql_select(Ticket)
            .where(
                Ticket.id != ticket_id,
                Ticket.id.notin_(seen_ids) if seen_ids else True,
                Ticket.deleted_at.is_(None),
                Ticket.status.in_([TicketStatus.resolved, TicketStatus.closed]),
                Ticket.category == ticket.category
            )
            .order_by(Ticket.created_at.desc())
            .limit(needed)
        )
        fallback_tickets = (await session.exec(fallback_stmt)).all()

        for t in fallback_tickets:
            seen_ids.add(t.id)
            output.append(
                SimilarTicketOut(
                    id=str(t.id),
                    ref=t.ref,
                    subject=t.subject,
                    category=t.category,
                    status=t.status.value,
                    similarity=0.5,
                    is_fallback=True
                )
            )

    return output[:limit]


# ─── Phase B.5 — AI Copilot: Next-Best-Action ─────────────────────────────────

class ActionItem(BaseModel):
    id: str
    label: str
    rationale: str
    priority: int  # 1 = highest
    action_type: str  # "status_change" | "reply" | "escalate" | "sla" | "info"


class NextActionOut(BaseModel):
    actions: List[ActionItem]
    ticket_summary: Optional[str] = None


@router.post("/{ticket_id}/next-action", response_model=NextActionOut)
async def get_next_best_action(
    ticket_id: uuid.UUID,
    current_user: User = Depends(require_role(UserRole.agent)),
    session: AsyncSession = Depends(get_session),
):
    """
    Deterministic Next-Best-Action engine for the AI Copilot.

    Analyses ticket status, priority, SLA, sentiment, and message count
    to return 1-3 prioritised recommended agent actions.

    HITL guarantee: This endpoint ONLY returns recommendations — it never
    mutates ticket state, sends messages, or triggers any side effects.
    The agent must explicitly act on each suggestion.
    """
    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Fetch messages for context
    from sqlmodel import select as sql_select
    msgs_result = await session.exec(
        sql_select(Message)
        .where(Message.ticket_id == ticket_id)
        .order_by(Message.created_at.asc())
        .limit(50)
    )
    messages = list(msgs_result.all())

    status_val = ticket.status.value if hasattr(ticket.status, "value") else str(ticket.status)
    priority_val = ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority)
    sentiment = (ticket.sentiment or "").lower()
    msg_count = len(messages)
    now = datetime.now()
    sla_breached = ticket.sla_breached or (
        ticket.sla_due_at is not None and ticket.sla_due_at < now
    )
    sla_mins_remaining = None
    if ticket.sla_due_at and ticket.sla_due_at >= now:
        sla_mins_remaining = int((ticket.sla_due_at - now).total_seconds() / 60)

    # Determine last sender type
    last_sender_type = None
    if messages:
        last_msg = messages[-1]
        last_sender_type = last_msg.sender_type.value if hasattr(last_msg.sender_type, "value") else str(last_msg.sender_type)

    actions: List[ActionItem] = []
    priority_counter = 1

    # Rule 1 — Escalated ticket: accept it
    if status_val == "escalated":
        actions.append(ActionItem(
            id="accept_ticket",
            label="Accept & Claim Ticket",
            rationale="Ticket is escalated. Accepting it stops further SLA countdown and notifies the customer a human agent is on the case.",
            priority=priority_counter,
            action_type="status_change",
        ))
        priority_counter += 1

    # Rule 2 — SLA breached: urgent response required
    if sla_breached and status_val not in ("resolved", "closed"):
        actions.append(ActionItem(
            id="sla_breach_response",
            label="Respond Immediately — SLA Breached",
            rationale="This ticket has breached its SLA target. A prompt, empathetic reply is required to acknowledge the delay and communicate next steps.",
            priority=priority_counter,
            action_type="sla",
        ))
        priority_counter += 1

    # Rule 3 — SLA < 30 mins remaining: warn
    if sla_mins_remaining is not None and sla_mins_remaining < 30 and status_val not in ("resolved", "closed"):
        actions.append(ActionItem(
            id="sla_warning_response",
            label=f"Reply Within {sla_mins_remaining} Minutes — SLA at Risk",
            rationale=f"Only {sla_mins_remaining} minutes remain before SLA breach. Draft and send a reply immediately.",
            priority=priority_counter,
            action_type="sla",
        ))
        priority_counter += 1

    # Rule 4 — Frustrated/negative sentiment with customer waiting
    if sentiment in ("frustrated", "negative") and last_sender_type == "customer" and status_val not in ("resolved", "closed"):
        actions.append(ActionItem(
            id="empathetic_reply",
            label="Send Empathetic Reply",
            rationale=f"Customer sentiment is '{sentiment}'. An empathetic acknowledgement reduces churn risk before addressing the core issue.",
            priority=priority_counter,
            action_type="reply",
        ))
        priority_counter += 1

    # Rule 5 — Customer sent last message in an active conversation
    if last_sender_type == "customer" and msg_count >= 3 and status_val in ("open", "waiting"):
        actions.append(ActionItem(
            id="follow_up_reply",
            label="Send Follow-Up Reply",
            rationale=f"The customer sent the last message ({msg_count} total). A follow-up keeps them informed and prevents re-escalation.",
            priority=priority_counter,
            action_type="reply",
        ))
        priority_counter += 1

    # Rule 6 — Resolved ticket: offer to close
    if status_val == "resolved":
        actions.append(ActionItem(
            id="close_ticket",
            label="Close Ticket",
            rationale="Ticket is resolved. Closing it frees capacity and delivers the final CSAT survey to the customer.",
            priority=priority_counter,
            action_type="status_change",
        ))
        priority_counter += 1

    # Rule 7 — High/urgent priority with no recent agent reply
    if priority_val in ("urgent", "high") and status_val in ("open", "new", "waiting"):
        has_recent_agent = any(
            (m.sender_type.value if hasattr(m.sender_type, "value") else str(m.sender_type)) == "agent"
            for m in messages[-3:]
        )
        if not has_recent_agent:
            actions.append(ActionItem(
                id="urgent_draft_reply",
                label="Draft & Send Urgent Reply",
                rationale=f"This is a {priority_val} priority ticket with no recent agent reply. Use AI Suggest to draft a rapid response.",
                priority=priority_counter,
                action_type="reply",
            ))
            priority_counter += 1

    # Rule 8 — New ticket with no agent reply yet
    if status_val in ("new", "open") and msg_count <= 2 and last_sender_type == "customer":
        actions.append(ActionItem(
            id="initial_response",
            label="Send Initial Response",
            rationale="This ticket has no agent reply yet. An acknowledgement sets a positive experience baseline.",
            priority=priority_counter,
            action_type="reply",
        ))
        priority_counter += 1

    # Fallback: no rules triggered
    if not actions:
        actions.append(ActionItem(
            id="use_ai_suggest",
            label="Use AI Suggest to Draft a Reply",
            rationale="No urgent actions detected. Use the AI Suggest tab to generate a context-aware reply.",
            priority=1,
            action_type="info",
        ))

    # Cap at top 3 actions, re-number cleanly
    actions = sorted(actions, key=lambda a: a.priority)[:3]
    for i, action in enumerate(actions):
        action.priority = i + 1

    return NextActionOut(
        actions=actions,
        ticket_summary=ticket.ai_summary,
    )


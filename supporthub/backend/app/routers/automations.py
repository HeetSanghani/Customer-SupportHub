"""
app/routers/automations.py

REST API endpoints for Workflow Automation management.
Allows managers and admins to manage rules, test simulations, and toggle automation states.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.dependencies import get_current_user, require_role
from app.models import Automation, Ticket, TicketChannel, TicketPriority, TicketStatus, User, UserRole
from app.services.automations.engine import (
    evaluate_ticket_automations,
    get_default_automation_templates,
)

router = APIRouter(prefix="/automations", tags=["automations"])


# ─── Schemas ──────────────────────────────────────────────────────────────────

class AutomationCreate(BaseModel):
    name: str = Field(..., max_length=200)
    trigger_json: Dict[str, Any]
    action_json: Dict[str, Any]
    is_active: bool = True
    priority: int = 10


class AutomationUpdate(BaseModel):
    name: Optional[str] = None
    trigger_json: Optional[Dict[str, Any]] = None
    action_json: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None


class AutomationResponse(BaseModel):
    id: uuid.UUID
    name: str
    trigger_json: Dict[str, Any]
    action_json: Dict[str, Any]
    is_active: bool
    priority: int
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime


class DryRunRequest(BaseModel):
    subject: str = "Test Subject"
    message_body: str = ""
    channel: str = "email"
    sentiment: Optional[str] = None
    category: Optional[str] = None
    priority: str = "medium"


class DryRunResponse(BaseModel):
    simulated_ticket: Dict[str, Any]
    results: List[Dict[str, Any]]
    final_ticket_state: Dict[str, Any]


def _format_automation(auto: Automation) -> AutomationResponse:
    trigger_dict = json.loads(auto.trigger_json) if isinstance(auto.trigger_json, str) else auto.trigger_json
    action_dict = json.loads(auto.action_json) if isinstance(auto.action_json, str) else auto.action_json
    return AutomationResponse(
        id=auto.id,
        name=auto.name,
        trigger_json=trigger_dict,
        action_json=action_dict,
        is_active=auto.is_active,
        priority=auto.priority,
        created_by=auto.created_by,
        created_at=auto.created_at,
        updated_at=auto.updated_at,
    )


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get("", response_model=List[AutomationResponse])
async def list_automations(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.manager)),
):
    """List all automation rules sorted by priority (lower priority number = runs first)."""
    stmt = select(Automation).order_by(Automation.priority.asc(), Automation.created_at.asc())
    rules = (await session.exec(stmt)).all()

    # If database has no automations, auto-seed defaults for seamless experience
    if not rules:
        defaults = await get_default_automation_templates(created_by_id=current_user.id)
        for r in defaults:
            session.add(r)
        await session.commit()
        rules = (await session.exec(stmt)).all()

    return [_format_automation(r) for r in rules]


@router.post("", response_model=AutomationResponse, status_code=status.HTTP_201_CREATED)
async def create_automation(
    payload: AutomationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.manager)),
):
    """Create a new automation rule."""
    now = datetime.now()
    new_rule = Automation(
        name=payload.name,
        trigger_json=json.dumps(payload.trigger_json),
        action_json=json.dumps(payload.action_json),
        is_active=payload.is_active,
        priority=payload.priority,
        created_by=current_user.id,
        created_at=now,
        updated_at=now,
    )
    session.add(new_rule)
    await session.commit()
    await session.refresh(new_rule)
    return _format_automation(new_rule)


@router.get("/{rule_id}", response_model=AutomationResponse)
async def get_automation(
    rule_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.manager)),
):
    """Get a specific automation rule by ID."""
    rule = await session.get(Automation, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Automation rule not found")
    return _format_automation(rule)


@router.put("/{rule_id}", response_model=AutomationResponse)
async def update_automation(
    rule_id: uuid.UUID,
    payload: AutomationUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.manager)),
):
    """Update an existing automation rule."""
    rule = await session.get(Automation, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Automation rule not found")

    if payload.name is not None:
        rule.name = payload.name
    if payload.trigger_json is not None:
        rule.trigger_json = json.dumps(payload.trigger_json)
    if payload.action_json is not None:
        rule.action_json = json.dumps(payload.action_json)
    if payload.is_active is not None:
        rule.is_active = payload.is_active
    if payload.priority is not None:
        rule.priority = payload.priority

    rule.updated_at = datetime.now()
    session.add(rule)
    await session.commit()
    await session.refresh(rule)
    return _format_automation(rule)


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_automation(
    rule_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.manager)),
):
    """Delete an automation rule."""
    rule = await session.get(Automation, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Automation rule not found")
    await session.delete(rule)
    await session.commit()
    return None


@router.patch("/{rule_id}/toggle", response_model=AutomationResponse)
async def toggle_automation(
    rule_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.manager)),
):
    """Toggle the active state of an automation rule."""
    rule = await session.get(Automation, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Automation rule not found")
    rule.is_active = not rule.is_active
    rule.updated_at = datetime.now()
    session.add(rule)
    await session.commit()
    await session.refresh(rule)
    return _format_automation(rule)


@router.post("/seed-defaults", response_model=List[AutomationResponse])
async def seed_defaults(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.manager)),
):
    """Force re-seeds the default best-practice automation rules."""
    defaults = await get_default_automation_templates(created_by_id=current_user.id)
    for r in defaults:
        session.add(r)
    await session.commit()

    stmt = select(Automation).order_by(Automation.priority.asc())
    rules = (await session.exec(stmt)).all()
    return [_format_automation(r) for r in rules]


@router.post("/test-dry-run", response_model=DryRunResponse)
async def test_dry_run(
    payload: DryRunRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.manager)),
):
    """Simulate automation rule evaluations against a sample ticket without persisting changes."""
    # Build simulated transient ticket
    dummy_channel = TicketChannel.email
    try:
        dummy_channel = TicketChannel(payload.channel.lower())
    except Exception:
        pass

    dummy_priority = TicketPriority.medium
    try:
        dummy_priority = TicketPriority(payload.priority.lower())
    except Exception:
        pass

    sim_ticket = Ticket(
        id=uuid.uuid4(),
        ref=f"SIM-{uuid.uuid4().hex[:6].upper()}",
        customer_id=current_user.id,
        subject=payload.subject,
        channel=dummy_channel,
        status=TicketStatus.open,
        priority=dummy_priority,
        sentiment=payload.sentiment,
        category=payload.category,
    )

    initial_state = {
        "ref": sim_ticket.ref,
        "subject": sim_ticket.subject,
        "channel": sim_ticket.channel.value,
        "status": sim_ticket.status.value,
        "priority": sim_ticket.priority.value,
        "category": sim_ticket.category,
        "sentiment": sim_ticket.sentiment,
    }

    eval_results = await evaluate_ticket_automations(
        session=session,
        ticket=sim_ticket,
        event_type="ticket_created",
        message_body=payload.message_body,
        dry_run=True,
    )

    final_state = {
        "ref": sim_ticket.ref,
        "subject": sim_ticket.subject,
        "channel": sim_ticket.channel.value,
        "status": sim_ticket.status.value,
        "priority": sim_ticket.priority.value,
        "category": sim_ticket.category,
        "sentiment": sim_ticket.sentiment,
        "ai_resolved": sim_ticket.ai_resolved,
    }

    return DryRunResponse(
        simulated_ticket=initial_state,
        results=eval_results,
        final_ticket_state=final_state,
    )

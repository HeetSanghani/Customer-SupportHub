"""
tests/test_copilot_hitl.py

Phase B.5 — Human Agent AI Copilot: Human-In-The-Loop (HITL) Test Suite.

Tests:
1.  Role guard: customer JWT → 403 for suggest-reply (via HTTP client).
2.  Role guard: customer JWT → 403 for next-action (via HTTP client).
3.  NBA rule: escalated ticket → "Accept & Claim Ticket" is top action.
4.  NBA rule: SLA-breached ticket → "Respond Immediately" action present.
5.  NBA rule: resolved ticket → "Close Ticket" action present.
6.  NBA rule: high-priority open ticket with no agent reply → urgent draft.
7.  HITL read-only guarantee: next-action does NOT modify ticket state.
8.  HITL read-only guarantee: suggest-reply does NOT create a Message row.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Optional

import pytest
from httpx import AsyncClient, ASGITransport
from sqlmodel import select

from app.database import AsyncSessionLocal
from app.models import (
    Message,
    SenderType,
    Ticket,
    TicketChannel,
    TicketPriority,
    TicketStatus,
    User,
    UserRole,
)
from app.routers.tickets import get_next_best_action, suggest_reply


# ─── Helpers ──────────────────────────────────────────────────────────────────

async def _get_or_create_customer(session) -> User:
    res = await session.exec(select(User).where(User.role == UserRole.customer))
    user = res.first()
    if not user:
        user = User(
            name="HITL Test Customer",
            email="hitl_cust@example.com",
            role=UserRole.customer,
            password_hash="x",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


def _make_agent() -> User:
    return User(
        id=uuid.uuid4(),
        name="HITL Test Agent",
        email=f"hitl_agent_{uuid.uuid4().hex[:6]}@example.com",
        role=UserRole.agent,
        password_hash="x",
    )


async def _create_ticket(
    session,
    customer: User,
    status: TicketStatus = TicketStatus.open,
    priority: TicketPriority = TicketPriority.medium,
    sentiment: Optional[str] = None,
    sla_due_at: Optional[datetime] = None,
    sla_breached: bool = False,
) -> Ticket:
    ticket = Ticket(
        ref=f"TCK-HITL-{uuid.uuid4().hex[:6]}",
        customer_id=customer.id,
        subject="HITL test ticket",
        category="returns",
        channel=TicketChannel.email,
        status=status,
        priority=priority,
        sentiment=sentiment,
        sla_due_at=sla_due_at or (datetime.now() + timedelta(hours=8)),
        sla_breached=sla_breached,
    )
    session.add(ticket)
    await session.commit()
    await session.refresh(ticket)
    return ticket


async def _add_messages(session, ticket: Ticket, customer: User, count: int = 3) -> list:
    msgs = []
    for i in range(count):
        sender_type = SenderType.customer if i % 2 == 0 else SenderType.agent
        msg = Message(
            ticket_id=ticket.id,
            sender_id=customer.id,
            sender_type=sender_type,
            body=f"HITL test message {i+1}",
        )
        session.add(msg)
        msgs.append(msg)
    await session.commit()
    return msgs


# ─── Tests ────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_suggest_reply_requires_agent_role():
    """Customer JWT must receive a 403 from suggest-reply (agent-only endpoint)."""
    from app.main import app
    from app.routers.auth import create_access_token

    async with AsyncSessionLocal() as session:
        customer = await _get_or_create_customer(session)
        ticket = await _create_ticket(session, customer)

    customer_token = create_access_token(str(customer.id), customer.role.value)
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
            headers={"Authorization": f"Bearer {customer_token}"},
        ) as ac:
            resp = await ac.post(f"/api/v1/tickets/{ticket.id}/suggest-reply")
        assert resp.status_code == 403, f"Expected 403 for customer role, got {resp.status_code}: {resp.text}"
    finally:
        async with AsyncSessionLocal() as cleanup:
            t = await cleanup.get(Ticket, ticket.id)
            if t:
                await cleanup.delete(t)
                await cleanup.commit()


@pytest.mark.asyncio
async def test_next_action_requires_agent_role():
    """Customer JWT must receive a 403 from next-action (agent-only endpoint)."""
    from app.main import app
    from app.routers.auth import create_access_token

    async with AsyncSessionLocal() as session:
        customer = await _get_or_create_customer(session)
        ticket = await _create_ticket(session, customer)

    customer_token = create_access_token(str(customer.id), customer.role.value)
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
            headers={"Authorization": f"Bearer {customer_token}"},
        ) as ac:
            resp = await ac.post(f"/api/v1/tickets/{ticket.id}/next-action")
        assert resp.status_code == 403, f"Expected 403 for customer role, got {resp.status_code}: {resp.text}"
    finally:
        async with AsyncSessionLocal() as cleanup:
            t = await cleanup.get(Ticket, ticket.id)
            if t:
                await cleanup.delete(t)
                await cleanup.commit()


@pytest.mark.asyncio
async def test_next_action_escalated_recommends_accept():
    """Escalated ticket → NBA top action is 'Accept & Claim Ticket'."""
    async with AsyncSessionLocal() as session:
        customer = await _get_or_create_customer(session)
        agent = _make_agent()
        ticket = await _create_ticket(session, customer, status=TicketStatus.escalated)
        try:
            result = await get_next_best_action(
                ticket_id=ticket.id,
                current_user=agent,
                session=session,
            )
            assert len(result.actions) >= 1
            top = result.actions[0]
            assert top.id == "accept_ticket"
            assert top.priority == 1
            assert top.action_type == "status_change"
        finally:
            await session.delete(ticket)
            await session.commit()


@pytest.mark.asyncio
async def test_next_action_sla_breached_recommends_urgent_response():
    """SLA-breached open ticket → NBA includes the SLA breach response action."""
    async with AsyncSessionLocal() as session:
        customer = await _get_or_create_customer(session)
        agent = _make_agent()
        ticket = await _create_ticket(
            session,
            customer,
            status=TicketStatus.open,
            priority=TicketPriority.high,
            sla_due_at=datetime.now() - timedelta(hours=2),  # already past
            sla_breached=True,
        )
        try:
            result = await get_next_best_action(
                ticket_id=ticket.id,
                current_user=agent,
                session=session,
            )
            action_ids = [a.id for a in result.actions]
            assert "sla_breach_response" in action_ids, f"Expected sla_breach_response in {action_ids}"
        finally:
            await session.delete(ticket)
            await session.commit()


@pytest.mark.asyncio
async def test_next_action_resolved_ticket_recommends_close():
    """Resolved ticket → NBA includes the 'Close Ticket' action."""
    async with AsyncSessionLocal() as session:
        customer = await _get_or_create_customer(session)
        agent = _make_agent()
        ticket = await _create_ticket(session, customer, status=TicketStatus.resolved)
        try:
            result = await get_next_best_action(
                ticket_id=ticket.id,
                current_user=agent,
                session=session,
            )
            action_ids = [a.id for a in result.actions]
            assert "close_ticket" in action_ids, f"Expected close_ticket in {action_ids}"
        finally:
            await session.delete(ticket)
            await session.commit()


@pytest.mark.asyncio
async def test_next_action_high_priority_no_agent_reply():
    """High-priority open ticket with no agent reply → NBA recommends urgent draft."""
    async with AsyncSessionLocal() as session:
        customer = await _get_or_create_customer(session)
        agent = _make_agent()
        ticket = await _create_ticket(
            session,
            customer,
            status=TicketStatus.open,
            priority=TicketPriority.high,
        )
        # Add only customer messages (no agent reply)
        msg = Message(
            ticket_id=ticket.id,
            sender_id=customer.id,
            sender_type=SenderType.customer,
            body="I need urgent help!",
        )
        session.add(msg)
        await session.commit()
        try:
            result = await get_next_best_action(
                ticket_id=ticket.id,
                current_user=agent,
                session=session,
            )
            action_ids = [a.id for a in result.actions]
            assert "urgent_draft_reply" in action_ids or "initial_response" in action_ids, \
                f"Expected urgent_draft_reply or initial_response in {action_ids}"
        finally:
            await session.delete(msg)
            await session.delete(ticket)
            await session.commit()


@pytest.mark.asyncio
async def test_next_action_is_read_only_does_not_mutate_ticket():
    """
    HITL guarantee: calling next-action multiple times must NOT change ticket state.
    Confirms the endpoint is strictly read-only (no side effects).
    """
    async with AsyncSessionLocal() as session:
        customer = await _get_or_create_customer(session)
        agent = _make_agent()
        ticket = await _create_ticket(session, customer, status=TicketStatus.escalated)
        original_status = ticket.status
        original_updated_at = ticket.updated_at
        try:
            # Call twice
            await get_next_best_action(ticket_id=ticket.id, current_user=agent, session=session)
            await get_next_best_action(ticket_id=ticket.id, current_user=agent, session=session)

            # Reload from DB and verify nothing changed
            await session.refresh(ticket)
            assert ticket.status == original_status, "next-action must not change ticket status"
            assert ticket.updated_at == original_updated_at, "next-action must not update ticket.updated_at"
        finally:
            await session.delete(ticket)
            await session.commit()


@pytest.mark.asyncio
async def test_suggest_reply_does_not_auto_send_message():
    """
    HITL guarantee: suggest-reply must NOT insert a Message row.
    The suggestion is returned as text only — the agent must explicitly send.
    """
    async with AsyncSessionLocal() as session:
        customer = await _get_or_create_customer(session)
        agent = _make_agent()
        ticket = await _create_ticket(session, customer)
        msg = Message(
            ticket_id=ticket.id,
            sender_id=customer.id,
            sender_type=SenderType.customer,
            body="Please help with my order return.",
        )
        session.add(msg)
        await session.commit()

        # Count messages before
        from sqlmodel import func as sql_func
        count_before_res = await session.exec(
            select(Message).where(Message.ticket_id == ticket.id)
        )
        count_before = len(list(count_before_res.all()))

        try:
            result = await suggest_reply(
                ticket_id=ticket.id,
                tone="formal",
                current_user=agent,
                session=session,
            )

            # Assertion 1: suggestion text returned
            assert result.suggestion is not None and len(result.suggestion) > 5

            # Assertion 2: NO new Message was inserted
            count_after_res = await session.exec(
                select(Message).where(Message.ticket_id == ticket.id)
            )
            count_after = len(list(count_after_res.all()))
            assert count_after == count_before, (
                f"suggest-reply must not insert messages. "
                f"Before: {count_before}, After: {count_after}"
            )

        finally:
            await session.delete(msg)
            await session.delete(ticket)
            await session.commit()

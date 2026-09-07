"""
tests/test_human_agent_workspace_e2e.py

End-to-End Verification Suite for Phase B.4:
- Tenant & Role Anti-IDOR Authorization
- Ticket Acceptance & System Message Creation
- AI Suppression upon Agent Assignment
- REST & WebSocket Broadcast Synchronization
- Customer Auto-Resolution Intent & Audit Logging
- Complete Ticket Lifecycle (Open -> Escalated -> Accepted -> Resolved -> Reopened -> Closed)
"""

import pytest
import uuid
from datetime import datetime
from httpx import AsyncClient, ASGITransport
from sqlmodel import select

from app.main import app
from app.database import AsyncSessionLocal
from app.models import User, Ticket, Message, AuditLog, UserRole, UserStatus, TicketChannel, TicketStatus, TicketPriority, SenderType
from app.routers.auth import create_access_token
from app.services.ai.live_chat_adapter import LiveChatAIAdapter


@pytest.fixture
async def e2e_users_and_tickets():
    """Create test users (Customer A, Customer B, Agent X, Manager M) and tickets."""
    async with AsyncSessionLocal() as session:
        # Customer A
        cust_a = User(
            email=f"cust_a_{uuid.uuid4().hex[:6]}@example.com",
            name="Customer A",
            password_hash="hash",
            role=UserRole.customer,
            status=UserStatus.active,
            customer_id="CUST-001",
        )
        # Customer B
        cust_b = User(
            email=f"cust_b_{uuid.uuid4().hex[:6]}@example.com",
            name="Customer B",
            password_hash="hash",
            role=UserRole.customer,
            status=UserStatus.active,
            customer_id="CUST-002",
        )
        # Agent X
        agent_x = User(
            email=f"agent_x_{uuid.uuid4().hex[:6]}@example.com",
            name="Agent X",
            password_hash="hash",
            role=UserRole.agent,
            status=UserStatus.active,
        )
        # Manager M
        mgr_m = User(
            email=f"mgr_m_{uuid.uuid4().hex[:6]}@example.com",
            name="Manager M",
            password_hash="hash",
            role=UserRole.manager,
            status=UserStatus.active,
        )
        session.add_all([cust_a, cust_b, agent_x, mgr_m])
        await session.commit()
        await session.refresh(cust_a)
        await session.refresh(cust_b)
        await session.refresh(agent_x)
        await session.refresh(mgr_m)

        # Ticket for Customer A
        t_a = Ticket(
            ref=f"TCK-{uuid.uuid4().hex[:5].upper()}",
            customer_id=cust_a.id,
            subject="Customer A Order Query",
            category="orders",
            channel=TicketChannel.website_chat,
            status=TicketStatus.escalated,
            priority=TicketPriority.medium,
        )
        # Ticket for Customer B
        t_b = Ticket(
            ref=f"TCK-{uuid.uuid4().hex[:5].upper()}",
            customer_id=cust_b.id,
            subject="Customer B Refund Issue",
            category="billing",
            channel=TicketChannel.website_chat,
            status=TicketStatus.new,
            priority=TicketPriority.high,
        )
        session.add_all([t_a, t_b])
        await session.commit()
        await session.refresh(t_a)
        await session.refresh(t_b)

        return {
            "cust_a": cust_a,
            "cust_b": cust_b,
            "agent_x": agent_x,
            "mgr_m": mgr_m,
            "token_a": create_access_token(str(cust_a.id), "customer"),
            "token_b": create_access_token(str(cust_b.id), "customer"),
            "token_agent": create_access_token(str(agent_x.id), "agent"),
            "token_mgr": create_access_token(str(mgr_m.id), "manager"),
            "ticket_a": t_a,
            "ticket_b": t_b,
        }


@pytest.mark.asyncio
async def test_anti_idor_tenant_isolation(e2e_users_and_tickets):
    """Goal 1: Verify strict customer tenant isolation and staff access."""
    data = e2e_users_and_tickets
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Customer B attempts to view Customer A's ticket -> HTTP 403 Access Denied
        res = await ac.get(
            f"/api/v1/tickets/{data['ticket_a'].id}",
            headers={"Authorization": f"Bearer {data['token_b']}"}
        )
        assert res.status_code == 403

        # Customer A views their own ticket -> HTTP 200 OK
        res_a = await ac.get(
            f"/api/v1/tickets/{data['ticket_a'].id}",
            headers={"Authorization": f"Bearer {data['token_a']}"}
        )
        assert res_a.status_code == 200
        assert res_a.json()["id"] == str(data["ticket_a"].id)

        # Agent X views Customer A's ticket -> HTTP 200 OK
        res_agent = await ac.get(
            f"/api/v1/tickets/{data['ticket_a'].id}",
            headers={"Authorization": f"Bearer {data['token_agent']}"}
        )
        assert res_agent.status_code == 200


@pytest.mark.asyncio
async def test_ticket_acceptance_and_system_message(e2e_users_and_tickets):
    """Goal 2: Verify ticket acceptance updates agent_id, status, audit log, and creates system message."""
    data = e2e_users_and_tickets
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post(
            f"/api/v1/tickets/{data['ticket_a'].id}/accept",
            headers={"Authorization": f"Bearer {data['token_agent']}"}
        )
        assert res.status_code == 200
        body = res.json()
        assert body["agent_id"] == str(data["agent_x"].id)
        assert body["status"] == "open"

        # Verify system message in history
        res_msgs = await ac.get(
            f"/api/v1/tickets/{data['ticket_a'].id}/messages",
            headers={"Authorization": f"Bearer {data['token_agent']}"}
        )
        assert res_msgs.status_code == 200
        msgs = res_msgs.json()
        system_msgs = [m for m in msgs if m["sender_type"] == "system"]
        assert len(system_msgs) >= 1
        assert "Agent X accepted this ticket" in system_msgs[0]["body"]

        # Verify AuditLog
        async with AsyncSessionLocal() as session:
            log = (await session.exec(
                select(AuditLog).where(
                    AuditLog.ticket_id == data["ticket_a"].id,
                    AuditLog.action == "ticket.accepted"
                )
            )).first()
            assert log is not None
            assert log.actor_id == data["agent_x"].id


@pytest.mark.asyncio
async def test_ai_suppression_when_agent_assigned(e2e_users_and_tickets):
    """Goal 3: Verify AI adapter suppresses response generation when ticket has an assigned agent."""
    data = e2e_users_and_tickets

    # Assign agent to ticket A
    async with AsyncSessionLocal() as session:
        t = await session.get(Ticket, data["ticket_a"].id)
        t.agent_id = data["agent_x"].id
        session.add(t)
        await session.commit()

    # Process message via LiveChatAIAdapter
    adapter = LiveChatAIAdapter()
    res = await adapter.process_live_chat_message(
        ticket_id=str(data["ticket_a"].id),
        message_body="Can you help me with my order?",
    )
    # AI generation should be suppressed completely when agent_id is set
    assert res is None


@pytest.mark.asyncio
async def test_rest_message_post_and_ws_broadcast(e2e_users_and_tickets):
    """Goal 3/5: Verify posting a message via REST auto-assigns agent and broadcasts to WS manager."""
    data = e2e_users_and_tickets
    from app.ws.manager import manager

    broadcast_events = []
    agent_inbox_events = []
    orig_broadcast = manager.broadcast
    orig_agents = manager.broadcast_to_agents

    async def mock_b(tid, payload):
        broadcast_events.append((tid, payload))

    async def mock_a(payload):
        agent_inbox_events.append(payload)

    manager.broadcast = mock_b
    manager.broadcast_to_agents = mock_a

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            res = await ac.post(
                f"/api/v1/tickets/{data['ticket_b'].id}/messages",
                headers={"Authorization": f"Bearer {data['token_agent']}"},
                json={"body": "Hello Customer B, I am reviewing your refund."}
            )
            assert res.status_code == 201

            # Check that agent was auto-assigned and status changed to open
            t_res = await ac.get(
                f"/api/v1/tickets/{data['ticket_b'].id}",
                headers={"Authorization": f"Bearer {data['token_agent']}"}
            )
            assert t_res.json()["agent_id"] == str(data["agent_x"].id)
            assert t_res.json()["status"] == "open"

            # Check WebSocket events
            assert len(broadcast_events) >= 1
            assert broadcast_events[0][0] == str(data["ticket_b"].id)
            assert broadcast_events[0][1]["type"] == "message"
            assert "Hello Customer B" in broadcast_events[0][1]["body"]

            assert len(agent_inbox_events) >= 1
            assert agent_inbox_events[0]["type"] == "inbox_update"
    finally:
        manager.broadcast = orig_broadcast
        manager.broadcast_to_agents = orig_agents


@pytest.mark.asyncio
async def test_customer_auto_resolution_intent_and_audit(e2e_users_and_tickets):
    """Goal 4: Verify customer resolution intent marks ticket resolved, sends reply, and creates AuditLog."""
    data = e2e_users_and_tickets
    adapter = LiveChatAIAdapter()

    res_msg = await adapter.process_live_chat_message(
        ticket_id=str(data["ticket_b"].id),
        message_body="My issue is resolved now, thank you so much!",
    )
    assert res_msg is not None
    assert "marked this ticket as resolved" in res_msg.body

    async with AsyncSessionLocal() as session:
        t = await session.get(Ticket, data["ticket_b"].id)
        assert t.status == TicketStatus.resolved
        assert t.ai_resolved is True

        log = (await session.exec(
            select(AuditLog).where(
                AuditLog.ticket_id == data["ticket_b"].id,
                AuditLog.action == "ticket.auto_resolved"
            )
        )).first()
        assert log is not None
        assert log.actor_id == data["cust_b"].id


@pytest.mark.asyncio
async def test_full_ticket_lifecycle_transitions(e2e_users_and_tickets):
    """Goal 4: Verify complete agent lifecycle: Open -> Resolve -> Reopen -> Close with AuditLogs."""
    data = e2e_users_and_tickets
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Resolve
        res_res = await ac.post(
            f"/api/v1/tickets/{data['ticket_a'].id}/resolve",
            headers={"Authorization": f"Bearer {data['token_agent']}"}
        )
        assert res_res.status_code == 200
        assert res_res.json()["status"] == "resolved"

        # 2. Reopen
        res_reopen = await ac.post(
            f"/api/v1/tickets/{data['ticket_a'].id}/reopen",
            headers={"Authorization": f"Bearer {data['token_agent']}"}
        )
        assert res_reopen.status_code == 200
        assert res_reopen.json()["status"] == "open"

        # 3. Close
        res_close = await ac.post(
            f"/api/v1/tickets/{data['ticket_a'].id}/close",
            headers={"Authorization": f"Bearer {data['token_agent']}"}
        )
        assert res_close.status_code == 200
        assert res_close.json()["status"] == "closed"

        # Check all AuditLogs
        async with AsyncSessionLocal() as session:
            logs = (await session.exec(
                select(AuditLog).where(AuditLog.ticket_id == data["ticket_a"].id)
            )).all()
            actions = [l.action for l in logs]
            assert "ticket.resolved" in actions
            assert "ticket.reopened" in actions
            assert "ticket.closed" in actions

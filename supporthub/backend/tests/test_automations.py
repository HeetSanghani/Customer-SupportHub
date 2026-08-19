"""
tests/test_automations.py

Tests for the Workflow Automation Engine & REST Endpoints.
"""

import json
import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import select, delete

from app.database import AsyncSessionLocal
from app.models import Automation, Ticket, TicketChannel, TicketPriority, TicketStatus, User, UserRole
from app.routers.auth import create_access_token, hash_password
from app.services.automations.engine import evaluate_ticket_automations


@pytest_asyncio.fixture
async def manager_auth_token():
    async with AsyncSessionLocal() as session:
        from app.models import UserStatus
        user = (await session.exec(select(User).where(User.email == "test_manager_auto@supporthub.com"))).first()
        if not user:
            user = User(
                email="test_manager_auto@supporthub.com",
                name="Test Manager",
                password_hash=hash_password("Password123!"),
                role=UserRole.manager,
                status=UserStatus.active,
            )
            session.add(user)
        else:
            user.status = UserStatus.active
            session.add(user)
        await session.commit()
        await session.refresh(user)

        token = create_access_token(str(user.id), user.role.value)
        return token, user


@pytest.mark.asyncio
async def test_list_automations_auto_seeds(async_client: AsyncClient, manager_auth_token):
    token, user = manager_auth_token
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get("/api/v1/automations", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    # Check that at least one seeded default has priority and trigger
    assert any("outage" in json.dumps(r["trigger_json"]).lower() or "billing" in json.dumps(r["trigger_json"]).lower() for r in data)


@pytest.mark.asyncio
async def test_create_and_delete_automation(async_client: AsyncClient, manager_auth_token):
    token, user = manager_auth_token
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "name": "Custom Test Automation",
        "trigger_json": {
            "event_type": "ticket_created",
            "conditions": {
                "keywords": ["urgent-test-keyword"],
                "channel": "email"
            }
        },
        "action_json": {
            "set_priority": "urgent",
            "set_category": "Test Category"
        },
        "is_active": True,
        "priority": 5,
    }

    create_res = await async_client.post("/api/v1/automations", json=payload, headers=headers)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["name"] == "Custom Test Automation"
    assert created_data["priority"] == 5
    rule_id = created_data["id"]

    # Toggle
    toggle_res = await async_client.patch(f"/api/v1/automations/{rule_id}/toggle", headers=headers)
    assert toggle_res.status_code == 200
    assert toggle_res.json()["is_active"] is False

    # Delete
    del_res = await async_client.delete(f"/api/v1/automations/{rule_id}", headers=headers)
    assert del_res.status_code == 204


@pytest.mark.asyncio
async def test_dry_run_simulation(async_client: AsyncClient, manager_auth_token):
    token, user = manager_auth_token
    headers = {"Authorization": f"Bearer {token}"}

    sim_payload = {
        "subject": "CRITICAL: Server crash and system outage detected",
        "message_body": "Everything is broken and downtime is ongoing.",
        "channel": "email",
        "priority": "medium",
    }

    res = await async_client.post("/api/v1/automations/test-dry-run", json=sim_payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "simulated_ticket" in data
    assert "results" in data
    assert "final_ticket_state" in data

    # At least one outage rule should have matched
    matched_rules = [r for r in data["results"] if r["matched"]]
    assert len(matched_rules) >= 1
    assert data["final_ticket_state"]["priority"] == "urgent"


@pytest.mark.asyncio
async def test_engine_evaluation_logic():
    async with AsyncSessionLocal() as session:
        from app.models import UserStatus
        # Create a test customer
        test_user = User(
            email=f"auto_cust_{uuid.uuid4().hex[:6]}@test.local",
            name="Automation Customer",
            password_hash=hash_password("Password123!"),
            role=UserRole.customer,
            status=UserStatus.active,
        )
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)

        # Create a ticket
        ticket = Ticket(
            ref=f"TCK-{uuid.uuid4().hex[:6].upper()}",
            customer_id=test_user.id,
            subject="I need a refund for my invoice subscription cancel",
            category="General",
            channel=TicketChannel.email,
            priority=TicketPriority.medium,
            status=TicketStatus.open,
        )
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)

        # Ensure automations exist
        from app.services.automations.engine import get_default_automation_templates
        existing_rules = (await session.exec(select(Automation))).all()
        if not existing_rules:
            for r in await get_default_automation_templates(test_user.id):
                session.add(r)
            await session.commit()

        # Run evaluation
        results = await evaluate_ticket_automations(
            session=session,
            ticket=ticket,
            event_type="ticket_created",
            message_body="Please cancel my subscription and issue a refund.",
        )

        assert any(r["matched"] for r in results)
        assert ticket.category == "Billing & Refunds"

        # Teardown
        from app.models import AuditLog, Message
        await session.exec(delete(AuditLog).where(AuditLog.ticket_id == ticket.id))
        await session.exec(delete(Message).where(Message.ticket_id == ticket.id))
        await session.exec(delete(Ticket).where(Ticket.id == ticket.id))
        await session.exec(delete(User).where(User.id == test_user.id))
        await session.commit()

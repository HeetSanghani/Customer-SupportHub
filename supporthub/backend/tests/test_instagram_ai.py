"""
tests/test_instagram_ai.py

Comprehensive test suite for Instagram AI Suggested Replies feature.
Tests:
1. ContextBuilder.build_from_ticket for Instagram tickets (multi-turn history, customer naming, tone, KB)
2. PromptBuilder formatting for Instagram DMs (conciseness, plain text formatting, KB grounding, tone modifiers)
3. AIOrchestrator.generate_for_ticket with MockAdapter and fallback handling
4. POST /api/v1/instagram/tickets/{ticket_id}/ai-reply endpoint security (401, 403, 404, 400, 200)
5. POST /api/v1/tickets/{ticket_id}/suggest-reply endpoint multi-turn upgrade
"""

import uuid
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from httpx import ASGITransport
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import AsyncSessionLocal
from app.main import app
from app.models import (
    KbArticle,
    Message,
    SenderType,
    Ticket,
    TicketChannel,
    TicketPriority,
    TicketStatus,
    User,
    UserRole,
    UserStatus,
)
from app.routers.auth import create_access_token
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.model_adapter import MockAdapter
from app.services.ai.models import LLMContext
from app.services.ai.orchestrator import AIOrchestrator
from app.services.ai.prompt_builder import PromptBuilder


# ─── 1. Unit Tests: ContextBuilder & PromptBuilder ────────────────────────────

def test_context_builder_build_from_ticket():
    """Verify ContextBuilder correctly formats DB entities into LLMContext for Instagram."""
    builder = ContextBuilder()

    dummy_ticket = Ticket(
        id=uuid.uuid4(),
        ref="TCK-99001",
        subject="Order delayed issue",
        category="Orders",
        channel=TicketChannel.instagram,
        status=TicketStatus.open,
        priority=TicketPriority.high,
        customer_id=uuid.uuid4(),
    )
    dummy_customer = User(
        id=dummy_ticket.customer_id,
        name="Alex Rivera",
        email="alex@instagram.local",
        channel_customer_id="alex_style",
        role=UserRole.customer,
    )
    dummy_messages = [
        Message(
            ticket_id=dummy_ticket.id,
            sender_id=dummy_customer.id,
            sender_type=SenderType.customer,
            body="Hey, where is my package #8472?",
        ),
        Message(
            ticket_id=dummy_ticket.id,
            sender_type=SenderType.agent,
            body="Hello Alex! Let me check that for you right now.",
        ),
        Message(
            ticket_id=dummy_ticket.id,
            sender_id=dummy_customer.id,
            sender_type=SenderType.customer,
            body="Thanks! It was supposed to arrive yesterday.",
        ),
    ]

    llm_ctx = builder.build_from_ticket(
        ticket=dummy_ticket,
        messages=dummy_messages,
        customer=dummy_customer,
        kb_context="Shipping policy: Standard shipping takes 3-5 business days.",
        tone="friendly",
    )

    assert llm_ctx.channel == "instagram"
    assert llm_ctx.customer_name == "Alex Rivera"
    assert llm_ctx.customer_channel_id == "alex_style"
    assert llm_ctx.conversation_ref == "TCK-99001"
    assert llm_ctx.current_message == "Thanks! It was supposed to arrive yesterday."
    assert len(llm_ctx.history) == 2
    assert llm_ctx.history[0]["role"] == "user"
    assert llm_ctx.history[1]["role"] == "assistant"
    assert "Shipping policy" in (llm_ctx.kb_context or "")
    assert llm_ctx.tone == "friendly"


def test_prompt_builder_instagram_dm_rules_and_guardrails():
    """Verify PromptBuilder enforces Instagram formatting, tone rules, and safety guardrails."""
    builder = PromptBuilder()

    llm_ctx = LLMContext(
        customer_name="Jordan Lee",
        customer_channel_id="jordan_lee",
        channel="instagram",
        conversation_ref="TCK-12345",
        is_new_customer=False,
        is_new_conversation=False,
        ticket_status="open",
        ticket_priority="urgent",
        history=[{"role": "user", "content": "How do I return my item?"}],
        current_message="Is return shipping free?",
        current_message_type="text",
        kb_context="Returns policy: Free returns within 30 days of purchase.",
        ticket_subject="Return shipping query",
        ticket_category="Returns",
        tone="friendly",
    )

    prompt = builder.build(llm_context=llm_ctx, model_name="mock-model")

    # Guardrails checks
    assert "NEVER invent company policies, prices, discounts" in prompt.system
    assert "NEVER claim an action was performed" in prompt.system
    assert "VERIFIED KNOWLEDGE BASE & POLICIES" in prompt.system
    assert "Free returns within 30 days" in prompt.system

    # Instagram formatting & tone checks
    assert "tailored for Instagram Direct Messages" in prompt.system
    assert "plain text" in prompt.system
    assert "Do NOT use markdown headings" in prompt.system
    assert "warm, enthusiastic, and highly approachable" in prompt.system

    # Messages check
    assert len(prompt.messages) == 2
    assert prompt.messages[-1]["content"] == "Is return shipping free?"


# ─── 2. Async Unit Tests: AIOrchestrator ──────────────────────────────────────

@pytest.mark.asyncio
async def test_ai_orchestrator_generate_for_ticket():
    """Verify AIOrchestrator generates response for ticket using mock adapter without throwing."""
    dummy_ticket = Ticket(
        id=uuid.uuid4(),
        ref="TCK-55001",
        subject="Refund request",
        category="Billing",
        channel=TicketChannel.instagram,
        status=TicketStatus.open,
        priority=TicketPriority.medium,
    )
    dummy_customer = User(
        id=uuid.uuid4(),
        name="Sam Taylor",
        role=UserRole.customer,
    )
    dummy_messages = [
        Message(
            ticket_id=dummy_ticket.id,
            sender_id=dummy_customer.id,
            sender_type=SenderType.customer,
            body="Can I get a refund for my order?",
        )
    ]

    mock_adapter = MockAdapter(response_text="Hi Sam! We'll be happy to assist with your refund.")

    async with AsyncSessionLocal() as session:
        orchestrator = AIOrchestrator(session=session, adapter=mock_adapter)
        response = await orchestrator.generate_for_ticket(
            ticket=dummy_ticket,
            messages=dummy_messages,
            customer=dummy_customer,
            tone="professional",
        )

        assert response.response_text == "Hi Sam! We'll be happy to assist with your refund."
        assert not response.is_fallback
        assert response.model.provider == "mock"


# ─── 3. Endpoint Integration Tests ───────────────────────────────────────────

@pytest.fixture
def test_data_ids():
    """Deterministic UUIDs for endpoint tests."""
    return {
        "agent_id": str(uuid.uuid4()),
        "customer_id": str(uuid.uuid4()),
        "ig_ticket_id": str(uuid.uuid4()),
        "email_ticket_id": str(uuid.uuid4()),
    }


@pytest.mark.asyncio
async def test_instagram_ai_reply_endpoint_auth(test_data_ids):
    """Test authentication and authorization for Instagram AI reply endpoint."""
    ig_ticket_id = test_data_ids["ig_ticket_id"]
    customer_id = test_data_ids["customer_id"]

    # Create active customer user in DB so token validation passes
    async with AsyncSessionLocal() as db:
        customer = User(
            id=uuid.UUID(customer_id),
            email=f"cust_{uuid.uuid4().hex[:6]}@test.com",
            name="Customer User",
            password_hash="fake",
            role=UserRole.customer,
            status=UserStatus.active,
        )
        db.add(customer)
        await db.commit()

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. No token -> 401 Unauthorized
        resp = await ac.post(f"/api/v1/instagram/tickets/{ig_ticket_id}/ai-reply")
        assert resp.status_code == 401

        # 2. Customer token -> 403 Forbidden (Only agents/admins allowed)
        customer_token = create_access_token(customer_id, UserRole.customer.value)
        resp = await ac.post(
            f"/api/v1/instagram/tickets/{ig_ticket_id}/ai-reply",
            headers={"Authorization": f"Bearer {customer_token}"},
        )
        assert resp.status_code == 403

    # Cleanup
    async with AsyncSessionLocal() as db:
        await db.exec(delete(User).where(User.id == uuid.UUID(customer_id)))
        await db.commit()


@pytest.mark.asyncio
async def test_instagram_ai_reply_endpoint_not_found(test_data_ids):
    """Test 404 response for non-existent ticket ID."""
    agent_id = test_data_ids["agent_id"]
    random_id = str(uuid.uuid4())

    async with AsyncSessionLocal() as db:
        agent = User(
            id=uuid.UUID(agent_id),
            email=f"agent_{uuid.uuid4().hex[:6]}@test.com",
            name="Agent Active",
            password_hash="fake",
            role=UserRole.agent,
            status=UserStatus.active,
        )
        db.add(agent)
        await db.commit()

    agent_token = create_access_token(agent_id, UserRole.agent.value)

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            f"/api/v1/instagram/tickets/{random_id}/ai-reply",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 404

    # Cleanup
    async with AsyncSessionLocal() as db:
        await db.exec(delete(User).where(User.id == uuid.UUID(agent_id)))
        await db.commit()


@pytest.mark.asyncio
async def test_instagram_ai_reply_endpoint_wrong_channel(test_data_ids):
    """Test 400 response when calling Instagram AI reply on a non-Instagram ticket."""
    email_ticket_id = test_data_ids["email_ticket_id"]
    agent_id = test_data_ids["agent_id"]
    customer_id = test_data_ids["customer_id"]

    async with AsyncSessionLocal() as db:
        agent = User(
            id=uuid.UUID(agent_id),
            email=f"agent_{uuid.uuid4().hex[:6]}@test.com",
            name="Agent Smith",
            password_hash="fake",
            role=UserRole.agent,
            status=UserStatus.active,
        )
        customer = User(
            id=uuid.UUID(customer_id),
            email=f"cust_{uuid.uuid4().hex[:6]}@test.com",
            name="Customer One",
            password_hash="fake",
            role=UserRole.customer,
            status=UserStatus.active,
        )
        email_ticket = Ticket(
            id=uuid.UUID(email_ticket_id),
            ref=f"TCK-{uuid.uuid4().hex[:5].upper()}",
            subject="Email inquiry",
            category="General",
            channel=TicketChannel.email,
            status=TicketStatus.open,
            priority=TicketPriority.low,
            customer_id=customer.id,
        )
        db.add(agent)
        db.add(customer)
        db.add(email_ticket)
        await db.commit()

    agent_token = create_access_token(agent_id, UserRole.agent.value)

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            f"/api/v1/instagram/tickets/{email_ticket_id}/ai-reply",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert resp.status_code == 400
        assert "belongs to channel 'email', not 'instagram'" in resp.json()["detail"]

    # Cleanup
    async with AsyncSessionLocal() as db:
        await db.exec(delete(Ticket).where(Ticket.id == uuid.UUID(email_ticket_id)))
        await db.exec(delete(User).where(User.id.in_([uuid.UUID(agent_id), uuid.UUID(customer_id)])))
        await db.commit()


@pytest.mark.asyncio
async def test_instagram_ai_reply_endpoint_success(test_data_ids):
    """Test successful Instagram AI suggested reply generation with mock adapter."""
    ig_ticket_id = test_data_ids["ig_ticket_id"]
    agent_id = test_data_ids["agent_id"]
    customer_id = test_data_ids["customer_id"]

    async with AsyncSessionLocal() as db:
        agent = User(
            id=uuid.UUID(agent_id),
            email=f"agent_{uuid.uuid4().hex[:6]}@test.com",
            name="Agent Sarah",
            password_hash="fake",
            role=UserRole.agent,
            status=UserStatus.active,
        )
        customer = User(
            id=uuid.UUID(customer_id),
            email=f"cust_{uuid.uuid4().hex[:6]}@instagram.local",
            name="Maria Garcia",
            channel_customer_id="maria_g",
            password_hash="fake",
            role=UserRole.customer,
            status=UserStatus.active,
        )
        ig_ticket = Ticket(
            id=uuid.UUID(ig_ticket_id),
            ref=f"TCK-{uuid.uuid4().hex[:5].upper()}",
            subject="Question about size chart",
            category="Product",
            channel=TicketChannel.instagram,
            status=TicketStatus.open,
            priority=TicketPriority.medium,
            customer_id=customer.id,
            agent_id=agent.id,
        )
        msg1 = Message(
            ticket_id=ig_ticket.id,
            sender_id=customer.id,
            sender_type=SenderType.customer,
            body="Hi! Does the jacket run small?",
        )
        db.add(agent)
        db.add(customer)
        db.add(ig_ticket)
        db.add(msg1)
        await db.commit()

    agent_token = create_access_token(agent_id, UserRole.agent.value)

    with patch("app.routers.instagram.AIOrchestrator") as mock_cls:
        mock_instance = AsyncMock()
        mock_response = AsyncMock()
        mock_response.response_text = "Hey Maria! Our jackets have a regular fit, so if you're between sizes, we recommend sizing up!"
        mock_response.is_fallback = False
        mock_response.confidence = 0.98
        mock_response.latency_ms = 195
        mock_response.usage = AsyncMock(input_tokens=150, output_tokens=35)
        mock_instance.generate_for_ticket.return_value = mock_response
        mock_cls.return_value = mock_instance

        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
            resp = await ac.post(
                f"/api/v1/instagram/tickets/{ig_ticket_id}/ai-reply",
                headers={"Authorization": f"Bearer {agent_token}"},
                json={"tone": "friendly"},
            )

            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert data["ticket_id"] == ig_ticket_id
            assert "jackets have a regular fit" in data["suggested_reply"]
            assert data["suggestion"] == data["suggested_reply"]
            assert data["confidence"] == 0.98

    # Cleanup
    async with AsyncSessionLocal() as db:
        await db.exec(delete(Message).where(Message.ticket_id == uuid.UUID(ig_ticket_id)))
        await db.exec(delete(Ticket).where(Ticket.id == uuid.UUID(ig_ticket_id)))
        await db.exec(delete(User).where(User.id.in_([uuid.UUID(agent_id), uuid.UUID(customer_id)])))
        await db.commit()


@pytest.mark.asyncio
async def test_tickets_suggest_reply_endpoint_multiturn(test_data_ids):
    """Test updated tickets suggest-reply endpoint uses multi-turn orchestrator (not raw Gemini)."""
    ig_ticket_id = test_data_ids["ig_ticket_id"]
    agent_id = test_data_ids["agent_id"]
    customer_id = test_data_ids["customer_id"]

    async with AsyncSessionLocal() as db:
        agent = User(
            id=uuid.UUID(agent_id),
            email=f"agent_{uuid.uuid4().hex[:6]}@test.com",
            name="Agent Mike",
            password_hash="fake",
            role=UserRole.agent,
            status=UserStatus.active,
        )
        customer = User(
            id=uuid.UUID(customer_id),
            email=f"cust_{uuid.uuid4().hex[:6]}@instagram.local",
            name="Leo Ross",
            channel_customer_id="leo_r",
            password_hash="fake",
            role=UserRole.customer,
            status=UserStatus.active,
        )
        ig_ticket = Ticket(
            id=uuid.UUID(ig_ticket_id),
            ref=f"TCK-{uuid.uuid4().hex[:5].upper()}",
            subject="Fit question",
            category="Product",
            channel=TicketChannel.instagram,
            status=TicketStatus.open,
            priority=TicketPriority.low,
            customer_id=customer.id,
        )
        db.add(agent)
        db.add(customer)
        db.add(ig_ticket)
        await db.commit()

    agent_token = create_access_token(agent_id, UserRole.agent.value)

    # Patch generate_for_ticket on the class level to intercept all instances
    with patch(
        "app.services.ai.orchestrator.AIOrchestrator.generate_for_ticket",
        new_callable=AsyncMock,
    ) as mock_gen:
        mock_response = AsyncMock()
        mock_response.response_text = "Thank you for asking! The sizing is true to size."
        mock_response.confidence = 0.95
        mock_response.latency_ms = 210
        mock_gen.return_value = mock_response

        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
            resp = await ac.post(
                f"/api/v1/tickets/{ig_ticket_id}/suggest-reply",
                headers={"Authorization": f"Bearer {agent_token}"},
                json={"tone": "standard"},
            )

            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert data["suggestion"] == "Thank you for asking! The sizing is true to size."
            assert data["suggested_reply"] == data["suggestion"]

    # Cleanup
    async with AsyncSessionLocal() as db:
        await db.exec(delete(Ticket).where(Ticket.id == uuid.UUID(ig_ticket_id)))
        await db.exec(delete(User).where(User.id.in_([uuid.UUID(agent_id), uuid.UUID(customer_id)])))
        await db.commit()


@pytest.mark.asyncio
async def test_instagram_webhook_triggers_auto_ai_reply():
    """Verify that incoming Instagram customer webhook event triggers AI auto-reply pipeline end-to-end."""
    import uuid
    import asyncio
    from app.services.instagram.webhook import process_instagram_webhook_background
    from app.models import Message, Ticket, User, WebhookEvent, SenderType

    test_igsid = f"auto_ai_{uuid.uuid4().hex[:6]}"
    test_mid = f"m_auto_{uuid.uuid4().hex[:8]}"

    payload = {
        "object": "instagram",
        "entry": [
            {
                "id": "17841435478991883",
                "time": 1786363356841,
                "messaging": [
                    {
                        "sender": {"id": test_igsid},
                        "recipient": {"id": "17841435478991883"},
                        "timestamp": 1786363356298,
                        "message": {
                            "mid": test_mid,
                            "text": "Do you ship internationally?"
                        }
                    }
                ]
            }
        ]
    }

    with patch("app.services.instagram.client.MetaInstagramClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get_user_profile.return_value = {"name": "Auto User", "profile_pic": None}
        mock_delivery = AsyncMock()
        mock_delivery.success = True
        mock_delivery.provider_message_id = f"m_ig_out_{uuid.uuid4().hex[:8]}"
        mock_client.send_text_message.return_value = mock_delivery
        mock_client.access_token = "mock_token"
        mock_client_cls.return_value = mock_client

        with patch("app.services.ai.orchestrator.AIOrchestrator") as mock_orch_cls:
            mock_orch = AsyncMock()
            mock_orch.generate_for_ticket.return_value = {
                "suggested_reply": "Yes! We ship worldwide to over 100 countries.",
                "confidence": 0.99,
                "latency_ms": 150,
            }
            mock_orch_cls.return_value = mock_orch

            from app.services.ai.debouncer import ai_debouncer
            original_delay = ai_debouncer.delay_seconds
            ai_debouncer.delay_seconds = 0.01
            
            await process_instagram_webhook_background(payload)
            await asyncio.sleep(0.15)
            if ai_debouncer._tasks:
                await asyncio.gather(*list(ai_debouncer._tasks.values()), return_exceptions=True)
                
            ai_debouncer.delay_seconds = original_delay

            # Verify Meta client was called with recipient IGSID and AI response
            mock_client.send_text_message.assert_called_once_with(
                recipient_igsid=test_igsid,
                text="Yes! We ship worldwide to over 100 countries.",
            )

    async with AsyncSessionLocal() as db:
        user = (await db.exec(select(User).where(User.channel_customer_id == test_igsid))).first()
        assert user is not None

        ticket = (await db.exec(select(Ticket).where(Ticket.customer_id == user.id))).first()
        assert ticket is not None

        messages = (await db.exec(select(Message).where(Message.ticket_id == ticket.id).order_by(Message.created_at))).all()
        assert len(messages) == 2

        # Message 1: Customer
        assert messages[0].sender_type == SenderType.customer
        assert messages[0].body == "Do you ship internationally?"
        assert messages[0].external_message_id == test_mid

        # Message 2: Auto AI
        assert messages[1].sender_type == SenderType.ai
        assert messages[1].body == "Yes! We ship worldwide to over 100 countries."
        assert messages[1].external_message_id == mock_delivery.provider_message_id

        # Teardown
        await db.exec(delete(Message).where(Message.ticket_id == ticket.id))
        await db.exec(delete(Ticket).where(Ticket.id == ticket.id))
        await db.exec(delete(User).where(User.id == user.id))
        await db.exec(delete(WebhookEvent).where(WebhookEvent.event_id == test_mid))
        await db.commit()

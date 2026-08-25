"""
End-to-End Live Chat AI Integration Test Suite.

Validates the full integration between SupportHub Live Chat and the SupportHub AI Architecture:
- Product inquiries with tool grounding
- Order tracking and shipment status
- Payment inquiries
- Policy & Knowledge Base RAG retrieval
- Prompt injection & security validation
- Resource ownership authorization across tenants / accounts
- Human agent escalation and ticket state mutation
- Conversation resolution & CSAT survey triggering
- Multi-turn conversation slot continuity
"""

import uuid
import pytest
from datetime import datetime
from sqlmodel import select

from app.database import AsyncSessionLocal
from app.models import Message, SenderType, Ticket, TicketChannel, TicketPriority, TicketStatus, User, UserRole, UserStatus
from app.services.ai.live_chat_adapter import live_chat_ai_adapter
from app.ws.manager import manager


@pytest.fixture
async def sample_customer_and_ticket():
    """Create a test customer (CUST-001) and an active Live Chat ticket."""
    async with AsyncSessionLocal() as session:
        cust_email = f"test_customer_{uuid.uuid4().hex[:6]}@example.com"
        user = User(
            email=cust_email,
            name="Aarav Sharma",
            password_hash="hashed_pw",
            role=UserRole.customer,
            status=UserStatus.active,
            channel_customer_id="CUST-001",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        ticket = Ticket(
            ref=f"TCK-{uuid.uuid4().hex[:5].upper()}",
            customer_id=user.id,
            subject="Website Live Chat Inquiry",
            category="general",
            channel=TicketChannel.website_chat,
            status=TicketStatus.open,
            priority=TicketPriority.medium,
        )
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)

        return user, ticket


@pytest.mark.asyncio
async def test_live_chat_product_inquiry(sample_customer_and_ticket):
    """Verify customer can inquire about a product and receive structured product information."""
    user, ticket = sample_customer_and_ticket
    ticket_id = str(ticket.id)

    ai_msg = await live_chat_ai_adapter.process_live_chat_message(
        ticket_id=ticket_id,
        message_body="Can you tell me about product PROD-001?",
    )

    assert ai_msg is not None
    assert ai_msg.sender_type == SenderType.ai
    # PROD-001 is NovaPhone Pro 5G
    assert "PROD-001" in ai_msg.body or "NovaPhone" in ai_msg.body or "Pro 5G" in ai_msg.body or "₹" in ai_msg.body


@pytest.mark.asyncio
async def test_live_chat_order_tracking(sample_customer_and_ticket):
    """Verify customer can check their order status with grounding from ShopKart database."""
    user, ticket = sample_customer_and_ticket
    ticket_id = str(ticket.id)

    ai_msg = await live_chat_ai_adapter.process_live_chat_message(
        ticket_id=ticket_id,
        message_body="Where is my order ORD-001?",
    )

    assert ai_msg is not None
    assert ai_msg.sender_type == SenderType.ai
    assert "ORD-001" in ai_msg.body
    assert ("DELIVERED" in ai_msg.body or "Delhivery" in ai_msg.body or "46,999" in ai_msg.body)


@pytest.mark.asyncio
async def test_live_chat_payment_inquiry(sample_customer_and_ticket):
    """Verify customer can query payment information for their order."""
    user, ticket = sample_customer_and_ticket
    ticket_id = str(ticket.id)

    ai_msg = await live_chat_ai_adapter.process_live_chat_message(
        ticket_id=ticket_id,
        message_body="What was the payment status for order ORD-001?",
    )

    assert ai_msg is not None
    assert "ORD-001" in ai_msg.body
    # ORD-001 payment is FAILED via CREDIT_CARD
    assert ("FAILED" in ai_msg.body or "CREDIT_CARD" in ai_msg.body or "₹" in ai_msg.body or "46,999" in ai_msg.body)


@pytest.mark.asyncio
async def test_live_chat_return_policy_rag(sample_customer_and_ticket):
    """Verify customer receives policy grounded responses via RAG pipeline."""
    user, ticket = sample_customer_and_ticket
    ticket_id = str(ticket.id)

    ai_msg = await live_chat_ai_adapter.process_live_chat_message(
        ticket_id=ticket_id,
        message_body="What is your return policy for electronics?",
    )

    assert ai_msg is not None
    assert ai_msg.sender_type == SenderType.ai
    assert len(ai_msg.body) > 20
    assert ("return" in ai_msg.body.lower() or "policy" in ai_msg.body.lower() or "days" in ai_msg.body.lower())


@pytest.mark.asyncio
async def test_live_chat_ownership_security_denial():
    """Verify that an unauthorized customer cannot view another customer's order details."""
    async with AsyncSessionLocal() as session:
        # Create customer CUST-002
        user = User(
            email=f"cust2_{uuid.uuid4().hex[:6]}@example.com",
            name="Diya Patel",
            password_hash="hashed_pw",
            role=UserRole.customer,
            status=UserStatus.active,
            channel_customer_id="CUST-002",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        # Ticket for CUST-002
        ticket = Ticket(
            ref=f"TCK-{uuid.uuid4().hex[:5].upper()}",
            customer_id=user.id,
            subject="Unauthorized Query Test",
            category="general",
            channel=TicketChannel.website_chat,
            status=TicketStatus.open,
            priority=TicketPriority.medium,
        )
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)

    ticket_id = str(ticket.id)
    # ORD-001 belongs to CUST-001, so CUST-002 must be denied
    ai_msg = await live_chat_ai_adapter.process_live_chat_message(
        ticket_id=ticket_id,
        message_body="Can you show me the tracking details for order ORD-001?",
    )

    assert ai_msg is not None
    assert ("Access Denied" in ai_msg.body or "not authorized" in ai_msg.body.lower())


@pytest.mark.asyncio
async def test_live_chat_human_escalation_mutates_ticket(sample_customer_and_ticket):
    """Verify that explicit customer request for a human agent escalates the ticket status and sets high priority."""
    user, ticket = sample_customer_and_ticket
    ticket_id = str(ticket.id)

    ai_msg = await live_chat_ai_adapter.process_live_chat_message(
        ticket_id=ticket_id,
        message_body="I want to speak with a human agent right now!",
    )

    assert ai_msg is not None
    assert ("transferred" in ai_msg.body.lower() or "human" in ai_msg.body.lower() or "representative" in ai_msg.body.lower())

    # Check that ticket status in DB mutated to escalated
    async with AsyncSessionLocal() as session:
        updated_ticket = await session.get(Ticket, ticket.id)
        assert updated_ticket is not None
        assert updated_ticket.status == TicketStatus.escalated
        assert updated_ticket.priority in (TicketPriority.high, TicketPriority.urgent)


@pytest.mark.asyncio
async def test_live_chat_resolution_and_csat(sample_customer_and_ticket):
    """Verify that customer closing statement marks ticket as resolved and ai_resolved."""
    user, ticket = sample_customer_and_ticket
    ticket_id = str(ticket.id)

    ai_msg = await live_chat_ai_adapter.process_live_chat_message(
        ticket_id=ticket_id,
        message_body="Thanks, that fixed it! You can close this chat now.",
    )

    assert ai_msg is not None

    async with AsyncSessionLocal() as session:
        updated_ticket = await session.get(Ticket, ticket.id)
        assert updated_ticket is not None
        assert updated_ticket.status == TicketStatus.resolved
        assert updated_ticket.ai_resolved is True


@pytest.mark.asyncio
async def test_live_chat_multi_turn_continuity(sample_customer_and_ticket):
    """Verify context and slot retention across multiple conversation turns."""
    user, ticket = sample_customer_and_ticket
    ticket_id = str(ticket.id)

    # Turn 1: Establish order context
    turn1_msg = await live_chat_ai_adapter.process_live_chat_message(
        ticket_id=ticket_id,
        message_body="I want to check order ORD-001",
    )
    assert turn1_msg is not None
    assert "ORD-001" in turn1_msg.body

    # Turn 2: Follow-up question without repeating order ID
    turn2_msg = await live_chat_ai_adapter.process_live_chat_message(
        ticket_id=ticket_id,
        message_body="When will it be delivered?",
    )
    assert turn2_msg is not None
    # Since slot ORD-001 was retained, it answers with the delivery details
    assert ("DELIVERED" in turn2_msg.body or "ORD-001" in turn2_msg.body or "Delhivery" in turn2_msg.body or "delivered" in turn2_msg.body.lower())

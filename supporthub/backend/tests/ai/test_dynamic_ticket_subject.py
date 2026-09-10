import pytest
import uuid
from sqlmodel import select
from app.models import Ticket, Message, SenderType, User, UserRole
from app.ai.subject import (
    is_generic_subject,
    is_greeting,
    format_subject_from_query,
    generate_ai_ticket_subject,
)


def test_is_generic_subject():
    # Generic category starting subjects should return True
    assert is_generic_subject("Billing & Orders Query") is True
    assert is_generic_subject("General Support Query") is True
    assert is_generic_subject("Technical Issue Query") is True
    assert is_generic_subject("New conversation") is True
    assert is_generic_subject("chat support") is True
    assert is_generic_subject(None) is True
    assert is_generic_subject("") is True
    assert is_generic_subject("Help") is True  # short

    # Specific question subjects should return False
    assert is_generic_subject("Where is my order?") is False
    assert is_generic_subject("Where is my order ORD-001?") is False
    assert is_generic_subject("Why was my payment declined?") is False
    assert is_generic_subject("Show me all products") is False


def test_is_greeting():
    assert is_greeting("Hello") is True
    assert is_greeting("hi!") is True
    assert is_greeting("good morning") is True
    assert is_greeting("hey there") is True
    assert is_greeting("namaste") is True

    # Substantive questions should NOT be greetings
    assert is_greeting("where is my order") is False
    assert is_greeting("hello where is my order") is False
    assert is_greeting("show me all products") is False
    assert is_greeting("my payment failed") is False


def test_format_subject_from_query():
    # Extracts core intent and avoids copying conversational clutter
    assert format_subject_from_query("hi, i want Show all products") == "Product Catalog Overview"
    assert format_subject_from_query("where is my order") == "Order Status & Tracking"
    assert format_subject_from_query("where is my order?") == "Order Status & Tracking"

    # Entities and domain intent
    assert format_subject_from_query("can you please tell me where is my order ord-001") == "Order Status (ORD-001)"
    assert format_subject_from_query("i want to know why my payment was declined") == "Payment & Billing Inquiry"
    assert format_subject_from_query("tell me how to return product prod-005") == "Return Request (PROD-005)"
    assert format_subject_from_query("give me all info of all my orders") == "Order History & All Orders"
    assert format_subject_from_query("please help me reset my password") == "Password Reset Assistance"

    # General questions cleanly formatted in Title Case
    assert format_subject_from_query("do you have discounts for gaming laptops") == "Discounts for Gaming Laptops"

    # Truncation if excessively long
    long_q = "Can you explain the detailed fragile packaging requirements and container specifications for bulk transportation?"
    formatted_long = format_subject_from_query(long_q)
    assert len(formatted_long) <= 48
    assert formatted_long.endswith("...")


from app.database import AsyncSessionLocal


@pytest.mark.asyncio
async def test_generate_ai_ticket_subject_flow():
    async with AsyncSessionLocal() as db_session:
        # 1. Create a customer
        cust_id = uuid.uuid4()
        cust = User(
            id=cust_id,
            email=f"cust_{cust_id.hex[:8]}@example.com",
            name="Test Customer",
            role=UserRole.customer,
            password_hash="hashed_pw",
        )
        db_session.add(cust)
        await db_session.commit()

        # 2. Create ticket with generic category title
        ticket = Ticket(
            ref=f"TCK-{uuid.uuid4().hex[:8].upper()}",
            customer_id=cust.id,
            subject="Billing & Orders Query",
            category="billing",
            channel="website_chat",
        )
        db_session.add(ticket)
        await db_session.commit()
        await db_session.refresh(ticket)

        # 3. Before any message: should be None (keep category title)
        subj = await generate_ai_ticket_subject(db_session, ticket.id)
        assert subj is None

        # 4. Message 1 is a greeting: "Hello" -> should skip greeting, remain None
        m1 = Message(
            ticket_id=ticket.id,
            sender_id=cust.id,
            sender_type=SenderType.customer,
            body="Hello!",
        )
        db_session.add(m1)
        await db_session.commit()

        subj = await generate_ai_ticket_subject(db_session, ticket.id)
        assert subj is None

        # 5. Message 2 is a question: "Where is my order?" -> should generate dynamic title
        m2 = Message(
            ticket_id=ticket.id,
            sender_id=cust.id,
            sender_type=SenderType.customer,
            body="Where is my order?",
        )
        db_session.add(m2)
        await db_session.commit()

        subj = await generate_ai_ticket_subject(db_session, ticket.id)
        assert subj == "Order Status & Tracking"

        # 6. Simulate updating ticket subject to "Order Status & Tracking"
        ticket.subject = subj
        db_session.add(ticket)
        await db_session.commit()
        await db_session.refresh(ticket)

        # 7. Customer sends Message 3 on a completely different topic: "Show me all products"
        m3 = Message(
            ticket_id=ticket.id,
            sender_id=cust.id,
            sender_type=SenderType.customer,
            body="Show me all products",
        )
        db_session.add(m3)
        await db_session.commit()

        # Title is LOCKED! Must return None and preserve "Order Status & Tracking"
        locked_subj = await generate_ai_ticket_subject(db_session, ticket.id)
        assert locked_subj is None
        assert ticket.subject == "Order Status & Tracking"


@pytest.mark.asyncio
async def test_generate_ai_ticket_subject_scan_up_to_3_messages():
    async with AsyncSessionLocal() as db_session:
        cust_id = uuid.uuid4()
        cust = User(
            id=cust_id,
            email=f"cust_{cust_id.hex[:8]}@example.com",
            name="Multi Msg Customer",
            role=UserRole.customer,
            password_hash="hashed_pw",
        )
        db_session.add(cust)
        await db_session.commit()

        ticket = Ticket(
            ref=f"TCK-{uuid.uuid4().hex[:8].upper()}",
            customer_id=cust.id,
            subject="General Support Query",
            category="general",
            channel="website_chat",
        )
        db_session.add(ticket)
        await db_session.commit()

        # Msg 1: "Hi"
        db_session.add(Message(ticket_id=ticket.id, sender_id=cust.id, sender_type=SenderType.customer, body="Hi"))
        await db_session.commit()
        assert await generate_ai_ticket_subject(db_session, ticket.id) is None

        # Msg 2: "Good morning"
        db_session.add(Message(ticket_id=ticket.id, sender_id=cust.id, sender_type=SenderType.customer, body="Good morning!"))
        await db_session.commit()
        assert await generate_ai_ticket_subject(db_session, ticket.id) is None

        # Msg 3: Question with order id: "Can you tell me where is my order ord-003?"
        db_session.add(Message(ticket_id=ticket.id, sender_id=cust.id, sender_type=SenderType.customer, body="Can you tell me where is my order ord-003?"))
        await db_session.commit()

        # Should scan through msg 1, 2, and pick up question from msg 3!
        subj = await generate_ai_ticket_subject(db_session, ticket.id)
        assert subj == "Order Status (ORD-003)"


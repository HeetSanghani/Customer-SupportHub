"""Unit tests for ConversationService, Customer Management, and Deduplication."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
import pytest
from sqlmodel import select

from app.database import AsyncSessionLocal
from app.services.conversations.service import ConversationService
from app.services.conversations.exceptions import DuplicateMessageError, ValidationError
from app.services.channels.models import Channel, IncomingMessage, MessageType, MediaAttachment
from app.models import User, Ticket, Message, WebhookEvent, TicketStatus


def make_incoming(
    msg_id: str = None,
    from_phone: str = "919876543210",
    name: str = "Heet Patel",
    text: str = "Hello I need help",
    msg_type: str = "text",
    channel: str = "whatsapp",
    attachments=None,
):
    type_map = {
        "text": MessageType.text,
        "image": MessageType.image,
        "audio": MessageType.audio,
        "document": MessageType.document,
    }
    return IncomingMessage(
        channel=Channel(channel),
        channel_message_id=msg_id or f"wamid.TEST_{uuid.uuid4().hex[:8]}",
        customer_channel_id=from_phone,
        customer_name=name,
        message_type=type_map.get(msg_type, MessageType.text),
        text=text if msg_type == "text" else None,
        attachments=attachments or [],
        timestamp=datetime.now(timezone.utc),
        phone_number_id="123456789",
    )


@pytest.mark.asyncio
async def test_conversation_creates_new_customer():
    async with AsyncSessionLocal() as session:
        phone = f"9100{uuid.uuid4().int % 10**6:06d}"
        incoming = make_incoming(from_phone=phone, name="Pytest User A")
        svc = ConversationService(session)
        ctx = await svc.process_incoming(incoming)

        async with AsyncSessionLocal() as s2:
            user = (await s2.exec(select(User).where(User.channel_customer_id == phone))).first()

        assert user is not None
        assert user.name == "Pytest User A"
        assert user.phone == phone
        assert ctx.is_new_customer is True


@pytest.mark.asyncio
async def test_conversation_reuses_existing_customer():
    async with AsyncSessionLocal() as session:
        phone = f"9101{uuid.uuid4().int % 10**6:06d}"
        incoming1 = make_incoming(from_phone=phone, name="Pytest User B")
        await ConversationService(session).process_incoming(incoming1)

        incoming2 = make_incoming(from_phone=phone, name="Pytest User B")
        ctx2 = await ConversationService(session).process_incoming(incoming2)

        async with AsyncSessionLocal() as s2:
            users = (await s2.exec(select(User).where(User.channel_customer_id == phone))).all()

        assert len(users) == 1
        assert ctx2.is_new_customer is False


@pytest.mark.asyncio
async def test_conversation_customer_name_update():
    async with AsyncSessionLocal() as session:
        phone = f"9102{uuid.uuid4().int % 10**6:06d}"
        incoming1 = make_incoming(from_phone=phone, name="Old Name")
        await ConversationService(session).process_incoming(incoming1)

        incoming2 = make_incoming(from_phone=phone, name="New Name")
        await ConversationService(session).process_incoming(incoming2)

        async with AsyncSessionLocal() as s2:
            user = (await s2.exec(select(User).where(User.channel_customer_id == phone))).first()

        assert user is not None
        assert user.name == "New Name"


@pytest.mark.asyncio
async def test_conversation_creates_new_ticket():
    async with AsyncSessionLocal() as session:
        phone = f"9103{uuid.uuid4().int % 10**6:06d}"
        incoming = make_incoming(from_phone=phone, text="My order is broken")
        ctx = await ConversationService(session).process_incoming(incoming)

        assert ctx.is_new_conversation is True
        assert ctx.ticket.ref.startswith("TCK-")
        assert ctx.ticket.status.value == "new"


@pytest.mark.asyncio
async def test_conversation_reuses_open_ticket():
    async with AsyncSessionLocal() as session:
        phone = f"9104{uuid.uuid4().int % 10**6:06d}"
        incoming1 = make_incoming(from_phone=phone, text="First message")
        ctx1 = await ConversationService(session).process_incoming(incoming1)

        incoming2 = make_incoming(from_phone=phone, text="Follow-up message")
        ctx2 = await ConversationService(session).process_incoming(incoming2)

        assert ctx1.ticket.id == ctx2.ticket.id
        assert ctx2.is_new_conversation is False


@pytest.mark.asyncio
async def test_conversation_deduplication_rejects_duplicate_msg():
    async with AsyncSessionLocal() as session:
        phone = f"9106{uuid.uuid4().int % 10**6:06d}"
        msg_id = f"wamid.DEDUP_{uuid.uuid4().hex[:8]}"
        incoming = make_incoming(msg_id=msg_id, from_phone=phone)
        await ConversationService(session).process_incoming(incoming)

        with pytest.raises(DuplicateMessageError):
            async with AsyncSessionLocal() as session2:
                incoming2 = make_incoming(msg_id=msg_id, from_phone=phone)
                await ConversationService(session2).process_incoming(incoming2)


@pytest.mark.asyncio
async def test_conversation_validation_error_on_empty_fields():
    async with AsyncSessionLocal() as session:
        bad = IncomingMessage(
            channel=Channel.whatsapp,
            channel_message_id="",
            customer_channel_id="919876543210",
            customer_name="Test",
            message_type=MessageType.text,
            text="test",
        )
        with pytest.raises(ValidationError):
            await ConversationService(session).process_incoming(bad)

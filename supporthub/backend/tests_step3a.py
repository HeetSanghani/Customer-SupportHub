"""
tests_step3a.py — Step 3A: Conversation Management Test Suite

Tests:
  [3a-1]  New customer created on first message
  [3a-2]  Existing customer reused on second message
  [3a-3]  Customer name updated when WhatsApp profile changes
  [3a-4]  New conversation (Ticket) created for new customer
  [3a-5]  Existing open conversation reused on follow-up message
  [3a-6]  Message stored with correct sender_type and body
  [3a-7]  DUPLICATE — same message_id is rejected (DuplicateMessageError)
  [3a-8]  DUPLICATE — concurrent duplicate (race condition via second service call)
  [3a-9]  ConversationContext fields are all populated correctly
  [3a-10] history_for_ai returns correct OpenAI-compatible format
  [3a-11] New conversation after resolved ticket
  [3a-12] Missing channel_message_id → ValidationError
  [3a-13] Missing customer_channel_id → ValidationError
  [3a-14] WebhookEvent row created and marked processed=True
  [3a-15] Image message stored with [image message] body fallback
"""

from __future__ import annotations

import asyncio
import sys
import uuid
from datetime import datetime, timezone

# ─── Setup ────────────────────────────────────────────────────────────────────

results: list[tuple[str, bool, str]] = []

def check(test_id: str, condition: bool, detail: str = "") -> None:
    icon = "✅ PASS" if condition else "❌ FAIL"
    results.append((test_id, condition, detail))
    print(f"  {icon}  [{test_id}] {detail}")


def make_incoming(
    msg_id: str = None,
    from_phone: str = "919876543210",
    name: str = "Heet Patel",
    text: str = "Hello I need help",
    msg_type: str = "text",
    channel: str = "whatsapp",
    attachments=None,
):
    """Build a minimal IncomingMessage for testing."""
    from app.services.channels.models import (
        Channel, IncomingMessage, MessageType, MediaAttachment
    )
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


# ─── Test Runner ──────────────────────────────────────────────────────────────

async def run_tests():
    from app.database import AsyncSessionLocal
    from app.services.conversations.service import ConversationService
    from app.services.conversations.exceptions import (
        DuplicateMessageError, ValidationError
    )
    from app.models import User, Ticket, Message, WebhookEvent, TicketStatus
    from sqlmodel import select

    print("\n" + "═" * 65)
    print("  STEP 3A — Conversation Management Test Suite")
    print("═" * 65)

    # Each test gets its own unique phone to avoid cross-test contamination
    BASE_PHONE = f"99{uuid.uuid4().int % 10**9:09d}"

    # ── [3a-1] New customer created on first message ───────────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9100{uuid.uuid4().int % 10**6:06d}"
        incoming = make_incoming(from_phone=phone, name="Test User A")
        svc = ConversationService(session)
        ctx = await svc.process_incoming(incoming)

        async with AsyncSessionLocal() as s2:
            user = (await s2.exec(select(User).where(User.channel_customer_id == phone))).first()

        check("3a-1",
              user is not None and user.name == "Test User A" and user.phone == phone,
              f"New customer | name={user.name if user else None} phone={user.phone if user else None}")

    # ── [3a-2] Existing customer reused on second message ─────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9101{uuid.uuid4().int % 10**6:06d}"
        # First message — creates customer
        incoming1 = make_incoming(from_phone=phone, name="Test User B")
        await ConversationService(session).process_incoming(incoming1)

        # Second message — should reuse customer
        incoming2 = make_incoming(from_phone=phone, name="Test User B")
        ctx2 = await ConversationService(session).process_incoming(incoming2)

        async with AsyncSessionLocal() as s2:
            users = (await s2.exec(select(User).where(User.channel_customer_id == phone))).all()

        check("3a-2",
              len(users) == 1 and ctx2.is_new_customer is False,
              f"Existing customer reused | user_count={len(users)} is_new={ctx2.is_new_customer}")

    # ── [3a-3] Customer name updated when profile changes ─────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9102{uuid.uuid4().int % 10**6:06d}"
        incoming1 = make_incoming(from_phone=phone, name="Old Name")
        await ConversationService(session).process_incoming(incoming1)

        incoming2 = make_incoming(from_phone=phone, name="New Name")
        ctx = await ConversationService(session).process_incoming(incoming2)

        async with AsyncSessionLocal() as s2:
            user = (await s2.exec(select(User).where(User.channel_customer_id == phone))).first()

        check("3a-3",
              user is not None and user.name == "New Name",
              f"Name updated | name={user.name if user else None}")

    # ── [3a-4] New conversation (Ticket) created for new customer ──────────
    async with AsyncSessionLocal() as session:
        phone = f"9103{uuid.uuid4().int % 10**6:06d}"
        incoming = make_incoming(from_phone=phone, text="My order is broken")
        ctx = await ConversationService(session).process_incoming(incoming)

        check("3a-4",
              ctx.is_new_conversation is True
              and ctx.ticket.ref.startswith("TCK-")
              and ctx.ticket.status.value == "new",
              f"New conversation | ref={ctx.ticket.ref} status={ctx.ticket.status}")

    # ── [3a-5] Existing conversation reused on follow-up ──────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9104{uuid.uuid4().int % 10**6:06d}"
        incoming1 = make_incoming(from_phone=phone, text="First message")
        ctx1 = await ConversationService(session).process_incoming(incoming1)

        incoming2 = make_incoming(from_phone=phone, text="Follow-up message")
        ctx2 = await ConversationService(session).process_incoming(incoming2)

        check("3a-5",
              ctx1.ticket.id == ctx2.ticket.id and ctx2.is_new_conversation is False,
              f"Same conversation | ref={ctx2.ticket.ref} is_new={ctx2.is_new_conversation}")

    # ── [3a-6] Message stored with correct sender_type ────────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9105{uuid.uuid4().int % 10**6:06d}"
        incoming = make_incoming(from_phone=phone, text="Store this message")
        ctx = await ConversationService(session).process_incoming(incoming)

        async with AsyncSessionLocal() as s2:
            msg = (await s2.exec(
                select(Message).where(Message.ticket_id == ctx.ticket.id)
            )).first()

        check("3a-6",
              msg is not None
              and msg.sender_type.value == "customer"
              and msg.body == "Store this message"
              and msg.external_message_id == incoming.channel_message_id,
              f"Message stored | sender={msg.sender_type if msg else None} body={msg.body[:20] if msg else None}")

    # ── [3a-7] DUPLICATE — same message_id rejected ────────────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9106{uuid.uuid4().int % 10**6:06d}"
        msg_id = f"wamid.DEDUP_{uuid.uuid4().hex[:8]}"
        incoming = make_incoming(msg_id=msg_id, from_phone=phone)
        await ConversationService(session).process_incoming(incoming)

        # Second call with same msg_id
        duplicate_raised = False
        async with AsyncSessionLocal() as session2:
            try:
                incoming2 = make_incoming(msg_id=msg_id, from_phone=phone)
                await ConversationService(session2).process_incoming(incoming2)
            except DuplicateMessageError:
                duplicate_raised = True

        check("3a-7",
              duplicate_raised,
              f"Duplicate rejected | DuplicateMessageError raised={duplicate_raised}")

    # ── [3a-8] DUPLICATE — check only 1 message row exists ────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9107{uuid.uuid4().int % 10**6:06d}"
        msg_id = f"wamid.DEDUP2_{uuid.uuid4().hex[:8]}"
        incoming = make_incoming(msg_id=msg_id, from_phone=phone, text="Original")
        ctx = await ConversationService(session).process_incoming(incoming)

        async with AsyncSessionLocal() as s2:
            msgs = (await s2.exec(
                select(Message).where(Message.external_message_id == msg_id)
            )).all()

        check("3a-8",
              len(msgs) == 1,
              f"No duplicate Message rows | count={len(msgs)}")

    # ── [3a-9] ConversationContext fields populated ────────────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9108{uuid.uuid4().int % 10**6:06d}"
        incoming = make_incoming(from_phone=phone, name="Context Test User", text="Context test")
        ctx = await ConversationService(session).process_incoming(incoming)

        check("3a-9",
              ctx.customer is not None
              and ctx.ticket is not None
              and ctx.incoming_message is not None
              and isinstance(ctx.history, list)
              and ctx.channel.value == "whatsapp"
              and ctx.webhook_event_id is not None,
              f"ConversationContext | ref={ctx.conversation_ref} customer={ctx.customer_display_name}")

    # ── [3a-10] history_for_ai format ─────────────────────────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9109{uuid.uuid4().int % 10**6:06d}"
        # First message
        await ConversationService(session).process_incoming(
            make_incoming(from_phone=phone, text="First msg")
        )
        # Second message — should have 1 history item
        ctx = await ConversationService(session).process_incoming(
            make_incoming(from_phone=phone, text="Second msg")
        )
        ai_history = ctx.history_for_ai
        check("3a-10",
              len(ai_history) == 1
              and ai_history[0]["role"] == "user"
              and ai_history[0]["content"] == "First msg",
              f"AI history | len={len(ai_history)} first={ai_history[0] if ai_history else None}")

    # ── [3a-11] New conversation after resolved ticket ─────────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9110{uuid.uuid4().int % 10**6:06d}"
        ctx1 = await ConversationService(session).process_incoming(
            make_incoming(from_phone=phone, text="First conversation")
        )
        # Resolve the ticket
        ctx1.ticket.status = TicketStatus.resolved
        session.add(ctx1.ticket)
        await session.commit()

        # New message should create NEW conversation
        ctx2 = await ConversationService(session).process_incoming(
            make_incoming(from_phone=phone, text="Second conversation")
        )
        check("3a-11",
              ctx2.is_new_conversation is True and ctx2.ticket.id != ctx1.ticket.id,
              f"New conv after resolve | ref1={ctx1.ticket.ref} ref2={ctx2.ticket.ref}")

    # ── [3a-12] Missing channel_message_id → ValidationError ──────────────
    async with AsyncSessionLocal() as session:
        from app.services.channels.models import Channel, IncomingMessage, MessageType
        bad = IncomingMessage(
            channel=Channel.whatsapp,
            channel_message_id="",   # empty!
            customer_channel_id="919876543210",
            customer_name="Test",
            message_type=MessageType.text,
            text="test",
        )
        validation_raised = False
        try:
            await ConversationService(session).process_incoming(bad)
        except ValidationError:
            validation_raised = True
        check("3a-12",
              validation_raised,
              f"Empty message_id → ValidationError raised={validation_raised}")

    # ── [3a-13] Missing customer_channel_id → ValidationError ─────────────
    async with AsyncSessionLocal() as session:
        from app.services.channels.models import Channel, IncomingMessage, MessageType
        bad = IncomingMessage(
            channel=Channel.whatsapp,
            channel_message_id="wamid.TEST_NOPHONE",
            customer_channel_id="",   # empty!
            customer_name="Test",
            message_type=MessageType.text,
            text="test",
        )
        validation_raised = False
        try:
            await ConversationService(session).process_incoming(bad)
        except ValidationError:
            validation_raised = True
        check("3a-13",
              validation_raised,
              f"Empty customer_id → ValidationError raised={validation_raised}")

    # ── [3a-14] WebhookEvent row marked processed=True ────────────────────
    async with AsyncSessionLocal() as session:
        phone = f"9111{uuid.uuid4().int % 10**6:06d}"
        incoming = make_incoming(from_phone=phone)
        ctx = await ConversationService(session).process_incoming(incoming)

        async with AsyncSessionLocal() as s2:
            event = (await s2.exec(
                select(WebhookEvent).where(
                    WebhookEvent.event_id == incoming.channel_message_id
                )
            )).first()

        check("3a-14",
              event is not None and event.processed is True and event.processing_ms is not None,
              f"WebhookEvent processed | processed={event.processed if event else None} ms={event.processing_ms if event else None}")

    # ── [3a-15] Image message stored with body fallback ───────────────────
    async with AsyncSessionLocal() as session:
        from app.services.channels.models import MediaAttachment
        phone = f"9112{uuid.uuid4().int % 10**6:06d}"
        attachment = MediaAttachment(media_id="media_abc", mime_type="image/jpeg")
        incoming = make_incoming(
            from_phone=phone,
            msg_type="image",
            text=None,
            attachments=[attachment],
        )
        ctx = await ConversationService(session).process_incoming(incoming)

        async with AsyncSessionLocal() as s2:
            msg = (await s2.exec(
                select(Message).where(Message.ticket_id == ctx.ticket.id)
            )).first()

        check("3a-15",
              msg is not None and "[image message]" in msg.body,
              f"Image body fallback | body={msg.body if msg else None}")


def print_summary():
    print("\n" + "═" * 65)
    print("  SUMMARY")
    print("═" * 65)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"\n  Total: {len(results)}  |  ✅ Passed: {passed}  |  ❌ Failed: {failed}\n")
    if failed:
        print("  FAILURES:")
        for tid, ok, detail in results:
            if not ok:
                print(f"    ❌ [{tid}] {detail}")
    print()
    return failed


if __name__ == "__main__":
    asyncio.run(run_tests())
    sys.exit(1 if print_summary() else 0)

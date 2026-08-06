"""
app/services/conversations/repository.py

Data Access layer for the Conversation Management domain.

RESPONSIBILITY:
  This is the ONLY file in the entire application that speaks raw SQL
  (via SQLAlchemy/SQLModel). It contains zero business logic.

  It knows HOW to query the database.
  It does NOT know WHEN to query, or WHAT to do with the results.
  That is the Service layer's job.

SEPARATION OF CONCERNS:
  Repository  ← knows SQL
  Service     ← knows business rules
  Router      ← knows HTTP

  This means:
    - Switching from PostgreSQL to MySQL = only touch repository.py
    - Unit testing service logic = mock the repository, no DB needed
    - Adding a caching layer = wrap repository methods with Redis cache

TRANSACTION PATTERN:
  Repository methods accept an AsyncSession and do NOT commit.
  The Service layer controls transaction boundaries (commit/rollback).
  This gives the service the power to wrap multiple repository calls
  in a single atomic transaction.

  Example:
    async with session.begin():          # Service opens transaction
        customer = await repo.create_customer(...)   # Repository inserts
        ticket   = await repo.create_ticket(...)     # Repository inserts
        message  = await repo.create_message(...)    # Repository inserts
    # session.begin() auto-commits here if no exception, else rolls back
"""

from __future__ import annotations

import json
import logging
import random
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import (
    ChannelType,
    Message,
    SenderType,
    Ticket,
    TicketChannel,
    TicketPriority,
    TicketStatus,
    User,
    UserRole,
    UserStatus,
    WebhookEvent,
)
from app.services.channels.models import Channel, IncomingMessage, MessageType
from app.services.conversations.exceptions import DatabaseError, DuplicateMessageError
from app.services.conversations.models import MessageRecord

logger = logging.getLogger(__name__)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _channel_to_ticket_channel(channel: Channel) -> TicketChannel:
    """Map the normalized Channel enum to the existing TicketChannel enum."""
    mapping = {
        Channel.whatsapp: TicketChannel.whatsapp,
        Channel.email: TicketChannel.email,
        Channel.instagram: TicketChannel.instagram,
        Channel.facebook: TicketChannel.facebook,
        Channel.website_chat: TicketChannel.website_chat,
    }
    return mapping[channel]


def _channel_to_channel_type(channel: Channel) -> ChannelType:
    """Map the normalized Channel enum to the existing ChannelType enum."""
    mapping = {
        Channel.whatsapp: ChannelType.whatsapp,
        Channel.email: ChannelType.email,
        Channel.instagram: ChannelType.instagram,
        Channel.facebook: ChannelType.facebook,
        Channel.website_chat: ChannelType.website_chat,
    }
    return mapping[channel]


def _generate_ticket_ref() -> str:
    """
    Generate a unique ticket reference number (e.g. TCK-47291).

    In production, use a dedicated sequence or atomic counter in the DB
    to guarantee uniqueness without retries. For now, the large random
    range (10000–99999) makes collisions extremely rare.
    """
    return f"TCK-{random.randint(10000, 99999)}"


def _message_record_from_orm(msg: Message) -> MessageRecord:
    """Convert a SQLModel Message ORM object to a serialization-safe MessageRecord."""
    attachments = []
    if msg.attachments:
        try:
            attachments = json.loads(msg.attachments)
        except (json.JSONDecodeError, TypeError):
            pass

    return MessageRecord(
        id=msg.id,
        sender_type=msg.sender_type.value if hasattr(msg.sender_type, "value") else str(msg.sender_type),
        body=msg.body or "",
        message_type="text",  # existing Message model has no message_type field; default text
        channel_message_id=msg.external_message_id,
        attachments=attachments,
        created_at=msg.created_at,
    )


# ─── WebhookEvent Repository ──────────────────────────────────────────────────

class WebhookEventRepository:
    """
    Manages the idempotency log (webhook_events table).

    This is the FIRST thing called when a webhook arrives.
    If the event_id already exists → DuplicateMessageError.
    If not → create a new record and return it.
    """

    @staticmethod
    async def find_by_event_id(
        session: AsyncSession,
        event_id: str,
    ) -> Optional[WebhookEvent]:
        """Look up a webhook event by its channel-specific message ID."""
        stmt = select(WebhookEvent).where(WebhookEvent.event_id == event_id)
        return (await session.exec(stmt)).first()

    @staticmethod
    async def create(
        session: AsyncSession,
        event_id: str,
        channel: Channel,
        raw_payload: Optional[dict] = None,
    ) -> WebhookEvent:
        """
        Create a new WebhookEvent record (processed=False).

        Raises DuplicateMessageError if event_id already exists
        (handles the race condition where two requests arrive simultaneously).
        """
        event = WebhookEvent(
            event_id=event_id,
            channel=_channel_to_channel_type(channel),
            processed=False,
            raw_payload=json.dumps(raw_payload) if raw_payload else None,
            received_at=datetime.utcnow(),  # naive UTC — matches TIMESTAMP WITHOUT TIME ZONE
        )
        session.add(event)
        try:
            await session.flush()  # flush to DB but don't commit — let service control commit
        except IntegrityError:
            await session.rollback()
            raise DuplicateMessageError(
                channel_message_id=event_id,
                channel=channel.value,
            )
        return event

    @staticmethod
    async def mark_processed(
        session: AsyncSession,
        event: WebhookEvent,
        processing_ms: Optional[int] = None,
        error: Optional[str] = None,
    ) -> None:
        """Mark a webhook event as processed (success or failure)."""
        event.processed = error is None
        event.error = error
        event.processing_ms = processing_ms
        event.processed_at = datetime.utcnow()  # naive UTC
        session.add(event)


# ─── Customer (User) Repository ───────────────────────────────────────────────

class CustomerRepository:
    """
    Manages customer lookup and creation.

    'Customer' in this context = a User with role=customer.
    We use the existing User table — channel_customer_id + channel fields
    added in Step 3A models extension identify omnichannel customers.
    """

    @staticmethod
    async def find_by_channel_id(
        session: AsyncSession,
        channel: Channel,
        channel_customer_id: str,
    ) -> Optional[User]:
        """
        Find a customer by their channel-specific ID.

        For WhatsApp: channel_customer_id is the phone number "919876543210"
        For Instagram: it's the PSID/IGSID
        For Email: use find_by_email instead
        """
        channel_type = _channel_to_channel_type(channel)
        stmt = select(User).where(
            User.channel == channel_type,
            User.channel_customer_id == channel_customer_id,
            User.role == UserRole.customer,
        )
        return (await session.exec(stmt)).first()

    @staticmethod
    async def find_by_email(
        session: AsyncSession,
        email: str,
    ) -> Optional[User]:
        """Find a customer by email address (used for email channel)."""
        stmt = select(User).where(User.email == email, User.role == UserRole.customer)
        return (await session.exec(stmt)).first()

    @staticmethod
    async def create(
        session: AsyncSession,
        incoming: IncomingMessage,
    ) -> User:
        """
        Create a new customer User record from an IncomingMessage.

        WHY WE SYNTHESIZE AN EMAIL:
          The User model requires a unique email. WhatsApp customers don't have
          emails. We generate a synthetic, platform-specific email address that:
            1. Is unique (phone number is unique per WhatsApp account)
            2. Is clearly identifiable as a synthetic record
            3. Will never conflict with a real email account

          Pattern: whatsapp_<phone>@channel.supporthub.internal
          The .internal TLD ensures it can never be confused with a real domain.
        """
        channel_type = _channel_to_channel_type(incoming.channel)

        synthetic_email = (
            f"{incoming.channel.value}_{incoming.customer_channel_id}"
            "@channel.supporthub.internal"
        )

        display_name = (
            incoming.customer_name
            or f"{incoming.channel.value.title()} User ({incoming.customer_channel_id})"
        )

        user = User(
            email=synthetic_email,
            name=display_name,
            password_hash="__channel_customer__",  # not a real password; login not possible
            role=UserRole.customer,
            status=UserStatus.active,
            channel=channel_type,
            channel_customer_id=incoming.customer_channel_id,
            phone=incoming.customer_channel_id if incoming.channel == Channel.whatsapp else None,
        )
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    async def update_name_if_changed(
        session: AsyncSession,
        customer: User,
        new_name: Optional[str],
    ) -> None:
        """
        Update the customer's display name if WhatsApp provides a new one.

        WHY: WhatsApp users can change their display name. If they do,
        subsequent messages will carry the new name. We keep the DB in sync.
        """
        if new_name and new_name != customer.name:
            customer.name = new_name
            customer.updated_at = datetime.utcnow()
            session.add(customer)


# ─── Conversation (Ticket) Repository ────────────────────────────────────────

class ConversationRepository:
    """
    Manages conversation (Ticket) lookup and creation.

    'Conversation' = a Ticket in our existing schema.
    An open conversation = a Ticket with status in [new, open, waiting].
    A closed conversation = status in [resolved, closed].

    WHY ONE OPEN CONVERSATION PER CUSTOMER PER CHANNEL:
      If a customer sends 5 messages, they're all part of ONE conversation
      thread — not 5 separate tickets. This matches how WhatsApp works
      (one continuous chat thread) and how Intercom/Zendesk handle it.

      When the conversation is resolved, the next message opens a new one.
    """

    OPEN_STATUSES = [TicketStatus.new, TicketStatus.open, TicketStatus.waiting]

    @staticmethod
    async def find_open(
        session: AsyncSession,
        customer_id: uuid.UUID,
        channel: Channel,
    ) -> Optional[Ticket]:
        """Find the most recent open conversation for a customer on a channel."""
        ticket_channel = _channel_to_ticket_channel(channel)
        stmt = (
            select(Ticket)
            .where(
                Ticket.customer_id == customer_id,
                Ticket.channel == ticket_channel,
                Ticket.status.in_(ConversationRepository.OPEN_STATUSES),
                Ticket.deleted_at.is_(None),
            )
            .order_by(Ticket.created_at.desc())
        )
        return (await session.exec(stmt)).first()

    @staticmethod
    async def create(
        session: AsyncSession,
        customer: User,
        incoming: IncomingMessage,
    ) -> Ticket:
        """
        Create a new conversation (Ticket) for a customer.

        Subject is auto-generated from the first message snippet.
        Category defaults to the channel name — agents can reclassify later.
        """
        ticket_channel = _channel_to_ticket_channel(incoming.channel)

        # Build smart subject from first message text
        import re
        raw_text = incoming.text or ""
        if incoming.attachments:
            attachment_hint = f"[{incoming.message_type.value}]"
            raw_text = f"{attachment_hint} {raw_text}".strip()

        cleaned = re.sub(r"^(hello|hi|hey|good morning|good afternoon|dear support)[\s,!.]*", "", raw_text, flags=re.IGNORECASE).strip()
        if cleaned and len(cleaned) >= 4:
            subject = cleaned.split(".")[0].split("\n")[0].strip()
            if len(subject) > 60:
                subject = subject[:60].rsplit(" ", 1)[0]
            subject = subject.capitalize()
        else:
            subject = f"{incoming.channel.value.title()} Support Inquiry"

        # Retry on ref collision (extremely rare with 90000 possible values)
        for _ in range(5):
            ref = _generate_ticket_ref()
            try:
                ticket = Ticket(
                    ref=ref,
                    customer_id=customer.id,
                    subject=subject,
                    category=incoming.channel.value,
                    channel=ticket_channel,
                    status=TicketStatus.new,
                    priority=TicketPriority.medium,
                )
                session.add(ticket)
                await session.flush()
                return ticket
            except IntegrityError:
                await session.rollback()
                logger.warning("Ticket ref collision on %s — retrying.", ref)
                continue

        raise DatabaseError("create_ticket", Exception("Failed to generate unique ticket ref after 5 attempts"))

    @staticmethod
    async def update_last_message_at(
        session: AsyncSession,
        ticket: Ticket,
    ) -> None:
        """Touch updated_at on the ticket so the inbox sorts correctly."""
        ticket.updated_at = datetime.utcnow()
        session.add(ticket)


# ─── Message Repository ───────────────────────────────────────────────────────

class MessageRepository:
    """
    Manages message storage and history retrieval.
    """

    @staticmethod
    async def create_incoming(
        session: AsyncSession,
        ticket: Ticket,
        customer: User,
        incoming: IncomingMessage,
    ) -> Message:
        """
        Store an incoming customer message.

        external_message_id = channel_message_id (the idempotency key).
        This field is indexed and we rely on it being set for future dedup checks.

        Attachments are serialized to JSON since the existing Message model
        stores them as a Text column (JSON string).
        """
        attachments_json = None
        if incoming.attachments:
            attachments_list = [
                {
                    "media_id": a.media_id,
                    "url": a.url,
                    "mime_type": a.mime_type,
                    "filename": a.filename,
                    "caption": a.caption,
                }
                for a in incoming.attachments
            ]
            attachments_json = json.dumps(attachments_list)

        message = Message(
            ticket_id=ticket.id,
            sender_id=customer.id,
            sender_type=SenderType.customer,
            body=incoming.text or f"[{incoming.message_type.value} message]",
            attachments=attachments_json,
            external_message_id=incoming.channel_message_id,
        )
        session.add(message)
        await session.flush()
        return message

    @staticmethod
    async def get_history(
        session: AsyncSession,
        ticket_id: uuid.UUID,
        limit: int = 50,
    ) -> list[MessageRecord]:
        """
        Fetch conversation history as MessageRecord objects (serialization-safe).

        Orders oldest-first so the AI receives chronological context.
        Limits to last `limit` messages to keep AI prompts within token budgets.
        """
        stmt = (
            select(Message)
            .where(Message.ticket_id == ticket_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        messages = (await session.exec(stmt)).all()
        return [_message_record_from_orm(m) for m in messages]

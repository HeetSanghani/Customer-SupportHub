"""All SQLModel table definitions for SupportHub."""

import enum
import uuid
from datetime import datetime, timezone
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel


# ─── Enums ────────────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    customer = "customer"
    agent = "agent"
    manager = "manager"
    admin = "admin"


class UserStatus(str, enum.Enum):
    active = "active"
    invited = "invited"
    suspended = "suspended"


class TicketStatus(str, enum.Enum):
    new = "new"
    open = "open"
    waiting = "waiting"
    escalated = "escalated"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, enum.Enum):
    urgent = "urgent"
    high = "high"
    medium = "medium"
    low = "low"


class TicketChannel(str, enum.Enum):
    email = "email"
    website_chat = "website_chat"
    whatsapp = "whatsapp"
    instagram = "instagram"
    facebook = "facebook"


class SenderType(str, enum.Enum):
    customer = "customer"
    agent = "agent"
    ai = "ai"
    system = "system"


class ChannelType(str, enum.Enum):
    email = "email"
    website_chat = "website_chat"
    whatsapp = "whatsapp"
    instagram = "instagram"
    facebook = "facebook"


class ChannelStatus(str, enum.Enum):
    connected = "connected"
    needs_attention = "needs_attention"
    disconnected = "disconnected"


# ─── User ─────────────────────────────────────────────────────────────────────

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    role: UserRole = Field(default=UserRole.customer)
    status: UserStatus = Field(default=UserStatus.invited)
    avatar_url: Optional[str] = Field(default=None, sa_column=Column(Text))
    totp_secret: Optional[str] = Field(default=None)
    totp_enabled: bool = Field(default=False)
    email_signature: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # ── Channel Identity (for omnichannel customers) ──────────────────────────
    # WHY: A WhatsApp customer has no email. Rather than creating a separate
    # Customer table, we store the channel-specific ID here. This keeps all
    # customer records in one table and preserves all existing FK relationships
    # (tickets, messages, audit logs, CSAT) without schema duplication.
    #
    # channel_customer_id examples:
    #   WhatsApp  → "919876543210"  (phone number, no + prefix)
    #   Instagram → "17841234567"   (Instagram-scoped user ID / IGSID)
    #   Facebook  → "1234567890"    (Page-scoped User ID / PSID)
    #   Email     → stored in email field directly
    channel: Optional[ChannelType] = Field(default=None, index=True)
    channel_customer_id: Optional[str] = Field(
        default=None,
        max_length=255,
        index=True,
        # Unique per channel enforced at the service layer via compound lookup
    )
    phone: Optional[str] = Field(default=None, max_length=30, index=True)

    # Relationships
    submitted_tickets: list["Ticket"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.customer_id]"},
    )
    assigned_tickets: list["Ticket"] = Relationship(
        back_populates="agent",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.agent_id]"},
    )
    messages: list["Message"] = Relationship(back_populates="sender")
    csat_ratings: list["CsatRating"] = Relationship(back_populates="customer")
    audit_logs: list["AuditLog"] = Relationship(back_populates="actor")


# ─── Ticket ───────────────────────────────────────────────────────────────────

class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    ref: str = Field(unique=True, index=True)  # e.g. TCK-10001
    customer_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    agent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True)
    subject: str = Field(max_length=500)
    category: str = Field(max_length=100, index=True)
    channel: TicketChannel = Field(index=True)
    status: TicketStatus = Field(default=TicketStatus.new, index=True)
    priority: TicketPriority = Field(default=TicketPriority.medium, index=True)
    sla_due_at: Optional[datetime] = Field(default=None, index=True)
    sla_breached: bool = Field(default=False)
    sentiment: Optional[str] = Field(default=None, max_length=50)
    ai_confidence: Optional[float] = Field(default=None)
    ai_resolved: bool = Field(default=False)
    ai_summary: Optional[str] = Field(default=None, sa_column=Column(Text))
    deleted_at: Optional[datetime] = Field(default=None)  # soft-delete
    created_at: datetime = Field(default_factory=datetime.now, index=True)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    customer: Optional[User] = Relationship(
        back_populates="submitted_tickets",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.customer_id]"},
    )
    agent: Optional[User] = Relationship(
        back_populates="assigned_tickets",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.agent_id]"},
    )
    messages: list["Message"] = Relationship(back_populates="ticket")
    csat_rating: Optional["CsatRating"] = Relationship(back_populates="ticket")
    audit_logs: list["AuditLog"] = Relationship(back_populates="ticket")


# ─── Message ──────────────────────────────────────────────────────────────────

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    ticket_id: uuid.UUID = Field(foreign_key="tickets.id", index=True)
    sender_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    sender_type: SenderType
    body: str = Field(sa_column=Column(Text))
    body_html: Optional[str] = Field(default=None, sa_column=Column(Text))
    attachments: Optional[str] = Field(default=None, sa_column=Column(Text))  # JSON list
    external_message_id: Optional[str] = Field(default=None, max_length=255, index=True)
    created_at: datetime = Field(default_factory=datetime.now, index=True)

    ticket: Optional[Ticket] = Relationship(back_populates="messages")
    sender: Optional[User] = Relationship(back_populates="messages")


# ─── KB Article ───────────────────────────────────────────────────────────────

class KbArticle(SQLModel, table=True):
    __tablename__ = "kb_articles"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=300, index=True)
    category: str = Field(max_length=100, index=True)
    body: str = Field(sa_column=Column(Text))
    embedding: Optional[list[float]] = Field(
        default=None, sa_column=Column(Vector(1536))
    )
    views: int = Field(default=0)
    helpful_count: int = Field(default=0)
    published: bool = Field(default=True)
    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ─── Channel Integration ──────────────────────────────────────────────────────

class ChannelIntegration(SQLModel, table=True):
    __tablename__ = "channel_integrations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    channel_type: ChannelType = Field(unique=True)
    status: ChannelStatus = Field(default=ChannelStatus.disconnected)
    credentials_encrypted: Optional[str] = Field(default=None, sa_column=Column(Text))
    display_name: Optional[str] = Field(default=None, max_length=200)
    config_json: Optional[str] = Field(default=None, sa_column=Column(Text))
    weekly_volume: int = Field(default=0)
    last_checked_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ─── Macro (Quick Reply) ──────────────────────────────────────────────────────

class Macro(SQLModel, table=True):
    __tablename__ = "macros"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=200)
    body: str = Field(sa_column=Column(Text))
    category: Optional[str] = Field(default=None, max_length=100)
    created_by: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ─── CSAT Rating ──────────────────────────────────────────────────────────────

class CsatRating(SQLModel, table=True):
    __tablename__ = "csat_ratings"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    ticket_id: uuid.UUID = Field(foreign_key="tickets.id", unique=True, index=True)
    customer_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.now)

    ticket: Optional[Ticket] = Relationship(back_populates="csat_rating")
    customer: Optional[User] = Relationship(back_populates="csat_ratings")


# ─── Automation ───────────────────────────────────────────────────────────────

class Automation(SQLModel, table=True):
    __tablename__ = "automations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=200)
    trigger_json: str = Field(sa_column=Column(Text))  # JSON-encoded trigger config
    action_json: str = Field(sa_column=Column(Text))   # JSON-encoded action config
    is_active: bool = Field(default=True)
    priority: int = Field(default=0)  # lower = evaluated first
    created_by: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ─── AI Settings (singleton row) ──────────────────────────────────────────────

class AiSettings(SQLModel, table=True):
    __tablename__ = "ai_settings"

    id: int = Field(default=1, primary_key=True)  # always 1 — singleton
    enabled: bool = Field(default=True)
    auto_resolve: bool = Field(default=True)
    suggest_replies: bool = Field(default=True)
    auto_summary: bool = Field(default=True)
    sentiment_detection: bool = Field(default=True)
    confidence_threshold: float = Field(default=0.75)
    model_name: str = Field(default="claude-sonnet-4-5", max_length=100)
    updated_at: datetime = Field(default_factory=datetime.now)


# ─── Audit Log (append-only) ─────────────────────────────────────────────────

class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_log"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    actor_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True)
    action: str = Field(max_length=100, index=True)  # e.g. "ticket.status_changed"
    entity_type: str = Field(max_length=100, index=True)
    entity_id: Optional[str] = Field(default=None, max_length=100, index=True)
    ticket_id: Optional[uuid.UUID] = Field(default=None, foreign_key="tickets.id", index=True)
    diff_json: Optional[str] = Field(default=None, sa_column=Column(Text))
    ip_address: Optional[str] = Field(default=None, max_length=45)
    created_at: datetime = Field(default_factory=datetime.now, index=True)

    actor: Optional[User] = Relationship(back_populates="audit_logs")
    ticket: Optional[Ticket] = Relationship(back_populates="audit_logs")


# ─── Email Delivery Log ───────────────────────────────────────────────────────

class EmailLog(SQLModel, table=True):
    __tablename__ = "email_logs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    ticket_id: Optional[uuid.UUID] = Field(default=None, foreign_key="tickets.id", index=True)
    recipient_email: str = Field(max_length=255, index=True)
    subject: str = Field(max_length=500)
    status: str = Field(default="sent", max_length=50, index=True)  # sent, delivered, failed, bounced
    error_detail: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.now, index=True)


# ─── Email Template ──────────────────────────────────────────────────────────

class EmailTemplate(SQLModel, table=True):
    __tablename__ = "email_templates"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)  # e.g. ticket_created, ticket_resolved
    subject_pattern: str = Field(max_length=300)
    body_html: str = Field(sa_column=Column(Text))
    updated_at: datetime = Field(default_factory=datetime.now)


# ─── Webhook Event (Idempotency Log) ─────────────────────────────────────────
#
# WHY THIS TABLE EXISTS:
#   Meta retries webhook delivery when your server doesn't respond within 20s,
#   or if it gets a non-2xx response. This means the exact same message can
#   arrive 2, 3, or even 5+ times.
#
#   Without an idempotency log:
#     - Same customer message → 3 AI replies sent to the customer
#     - 3 duplicate Message rows in the database
#     - 3 separate Ticket rows if the ticket finder has a race condition
#
#   With WebhookEvent:
#     - First arrival: create record (processed=False), process, mark processed=True
#     - Second arrival: find existing record → skip immediately
#     - Result: exactly-once processing, regardless of how many times Meta sends it
#
#   This is the same pattern used by Stripe (idempotency keys), Twilio
#   (X-Twilio-Signature), and all production webhook-driven platforms.
#
# FIELDS:
#   event_id   — the channel's unique message ID (wamid.XXX for WhatsApp)
#                This is the PRIMARY idempotency key.
#   channel    — which channel sent this event
#   processed  — False on arrival, True after full pipeline completion
#   error      — if processing failed, stores the error message for retry logic

class WebhookEvent(SQLModel, table=True):
    __tablename__ = "webhook_events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # The channel-specific unique message ID — idempotency key
    # For WhatsApp: "wamid.HBgM..." from messages[0].id
    # UNIQUE constraint: one DB row per channel_message_id across all channels
    event_id: str = Field(
        max_length=500,
        index=True,
        sa_column_kwargs={"unique": True},
    )

    channel: ChannelType = Field(index=True)

    # Processing state
    processed: bool = Field(default=False, index=True)
    error: Optional[str] = Field(default=None, sa_column=Column(Text))
    processing_ms: Optional[int] = Field(default=None)  # processing time in milliseconds

    # The full raw payload stored for audit, debugging, and potential replay
    raw_payload: Optional[str] = Field(default=None, sa_column=Column(Text))  # JSON string

    received_at: datetime = Field(
        default_factory=datetime.utcnow,  # naive UTC — PostgreSQL TIMESTAMP WITHOUT TIME ZONE
        index=True,
    )
    processed_at: Optional[datetime] = Field(default=None)


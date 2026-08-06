"""
app/services/conversations/models.py

Domain models for the Conversation Management layer.

NOTE: These are NOT SQLModel/database table models.
These are in-memory Python objects used to pass rich context
between layers without coupling to the database schema.

WHY ConversationContext EXISTS:
  In a layered architecture, each layer should receive exactly what it needs.
  Without ConversationContext:
    - AI layer gets a Ticket ID
    - AI layer must query DB for customer name (1 query)
    - AI layer must query DB for conversation history (1 query)
    - AI layer must query DB for channel info (1 query)
    = 3 extra DB round-trips inside what should be pure AI logic

  With ConversationContext:
    - Conversation layer assembles everything in ONE place
    - AI layer receives the context, does zero extra DB queries
    - Sender layer receives the context, knows exactly which channel to reply on
    - This is the "Unit of Work" pattern used by Intercom and Zendesk internally

  Think of ConversationContext like the "briefing packet" handed to every
  subsequent step in the pipeline. One assembly point, many consumers.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    # Avoid circular imports at runtime — only used for type checking
    from app.models import Ticket, User, Message
    from app.services.channels.models import Channel, IncomingMessage


@dataclass
class MessageRecord:
    """
    A lightweight, serializable representation of a stored message.
    Used in conversation history — decoupled from the SQLModel ORM object.

    WHY NOT USE THE ORM Message DIRECTLY:
      ORM objects have lazy-loaded relationships that can trigger N+1 queries
      when iterated. A plain dataclass is safe to pass between async contexts
      and serialize to JSON for the AI prompt.
    """
    id: uuid.UUID
    sender_type: str          # "customer" | "agent" | "ai" | "system"
    body: str
    message_type: str         # "text" | "image" | "audio" etc.
    channel_message_id: Optional[str]
    attachments: list[dict]
    created_at: datetime


@dataclass
class ConversationContext:
    """
    Rich context object assembled by the Conversation Service.

    This is the OUTPUT of Step 3A and the INPUT of Step 3B (AI orchestration).

    Fields:
      customer:
        The User ORM object for this customer. Contains name, phone,
        channel_customer_id (phone number for WhatsApp), and channel.

      ticket:
        The Ticket ORM object representing the conversation thread.
        Contains status, priority, channel, SLA fields, and ref (e.g. TCK-10023).

      incoming_message:
        The normalized IncomingMessage that triggered this context assembly.
        Contains the current message text, attachments, message_type, etc.

      history:
        Ordered list of MessageRecord objects (oldest first) representing
        the full conversation history. Used to build the AI prompt context.
        Excludes the current incoming_message (which hasn't been stored yet).

      channel:
        The Channel enum value (Channel.whatsapp, Channel.email, etc.)
        Used by the Sender layer to know which API to call for replies.

      is_new_customer:
        True if the customer was just created (first-ever message).
        Useful for AI to give a welcome message vs. a returning-customer response.

      is_new_conversation:
        True if this is the first message in a new conversation thread.
        Useful for AI to introduce itself, or for SLA timer to start.

      webhook_event_id:
        The UUID of the WebhookEvent row in the idempotency log.
        Used by the pipeline to mark the event as processed=True after completion.
    """
    customer: "User"
    ticket: "Ticket"
    incoming_message: "IncomingMessage"
    history: list[MessageRecord]
    channel: "Channel"
    is_new_customer: bool = False
    is_new_conversation: bool = False
    webhook_event_id: Optional[uuid.UUID] = None

    @property
    def customer_display_name(self) -> str:
        """Human-readable customer name for logging and AI prompts."""
        return self.customer.name or self.customer.channel_customer_id or "Unknown Customer"

    @property
    def conversation_ref(self) -> str:
        """Ticket reference for logging (e.g. 'TCK-10023')."""
        return self.ticket.ref

    @property
    def history_for_ai(self) -> list[dict]:
        """
        Formats conversation history as OpenAI/Claude-compatible message dicts.

        Returns list of {"role": "user"|"assistant", "content": "..."} dicts.
        System messages and AI messages are mapped to "assistant".
        This is the exact format consumed by the AI layer in Step 3B.
        """
        result = []
        for msg in self.history:
            if msg.sender_type == "customer":
                role = "user"
            else:
                role = "assistant"

            # Skip empty bodies (e.g. image-only messages with no caption)
            if msg.body and msg.body.strip():
                result.append({"role": role, "content": msg.body})

        return result

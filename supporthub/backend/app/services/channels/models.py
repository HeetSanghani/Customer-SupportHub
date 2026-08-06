"""
app/services/channels/models.py

Normalized internal message model — the Channel Adapter contract.

WHY THIS EXISTS:
  Every messaging channel sends data in a completely different format.
  WhatsApp uses phone numbers, Instagram uses PSIDs, Email uses email addresses.
  Message content is in different fields, attachments are structured differently,
  timestamps are in different formats.

  Rather than letting this channel-specific complexity bleed into your core
  business logic (ticket creation, AI pipeline, conversation management),
  we define a single internal contract: IncomingMessage.

  Every channel adapter (parser) must convert its raw payload into this model.
  Everything downstream (ConversationManager, AI Agent, Sender) works ONLY
  with IncomingMessage — it doesn't know or care about the source channel.

  This is the Channel Adapter pattern, used in production by:
    - Intercom (Unified Inbox)
    - Zendesk (Omnichannel)
    - Freshdesk (Freshchat)
    - Salesforce Service Cloud (Einstein Messaging)

DESIGN PRINCIPLES:
  - Immutable after construction (frozen=True)
  - All fields are optional where the channel may not provide them
  - channel_message_id is used for IDEMPOTENCY — prevents duplicate processing
  - attachments is a list of MediaAttachment, not raw URLs
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


# ─── Channel Enum ─────────────────────────────────────────────────────────────

class Channel(str, Enum):
    """
    Identifies which messaging channel this message came from.
    Matches the TicketChannel enum in app/models/__init__.py.
    """
    whatsapp = "whatsapp"
    email = "email"
    instagram = "instagram"
    facebook = "facebook"
    website_chat = "website_chat"


# ─── Message Type Enum ────────────────────────────────────────────────────────

class MessageType(str, Enum):
    """
    The type of content in this message.

    WHY THIS MATTERS:
      Your AI agent, ticket subject generation, and routing logic may behave
      differently based on message type. You can't reply to an audio message
      with a template — you need to send a text response acknowledging it.
    """
    text = "text"
    image = "image"
    audio = "audio"
    video = "video"
    document = "document"
    location = "location"
    sticker = "sticker"
    reaction = "reaction"
    interactive = "interactive"   # button replies, list replies
    unknown = "unknown"


# ─── Media Attachment ─────────────────────────────────────────────────────────

@dataclass(frozen=True)
class MediaAttachment:
    """
    A normalized media attachment from any channel.

    media_id: The channel-specific ID to fetch the actual file.
              For WhatsApp: use Meta's Media API with this ID.
              For Email: this is the attachment filename or CID.

    url: If the channel provides a direct URL (e.g., Mailgun attachments).
         For WhatsApp, this is None until you call the Media API.

    mime_type: e.g., "image/jpeg", "application/pdf", "audio/ogg"
    filename: Original filename if provided by the sender.
    caption: Optional text the user typed alongside the media.
    """
    media_id: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None
    filename: Optional[str] = None
    caption: Optional[str] = None
    size_bytes: Optional[int] = None


# ─── Location Data ────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class LocationData:
    """
    Normalized location shared by the customer.
    Used when message_type == MessageType.location.
    """
    latitude: float
    longitude: float
    name: Optional[str] = None       # e.g., "Ahmedabad International Airport"
    address: Optional[str] = None    # Full street address if provided


# ─── Core: IncomingMessage ────────────────────────────────────────────────────

@dataclass(frozen=True)
class IncomingMessage:
    """
    The normalized internal representation of any incoming customer message.

    This is the ONLY model that the ConversationManager, AI pipeline,
    and ticket creation logic should ever work with. They must never
    depend on raw WhatsApp, Email, or Instagram payload structures.

    Fields:
      channel:
        Which platform sent this message (whatsapp, email, instagram, etc.)

      channel_message_id:
        The unique message ID from the originating platform.
        For WhatsApp: the "wamid.XXXX" string from the payload.
        CRITICAL: Use this for idempotency checks. Meta retries webhook
        delivery on failure — without this, you'll process the same message
        multiple times and send duplicate AI replies.

      customer_channel_id:
        How this customer is identified ON THIS CHANNEL.
        For WhatsApp: their phone number (e.g., "919876543210")
        For Email: their email address
        For Instagram/Facebook: their Page-scoped User ID (PSID)
        This is used to look up or create the Customer record in your DB.

      customer_name:
        Display name from the channel profile. May be None if not provided.
        For WhatsApp: the name from their WhatsApp profile
        For Email: the From header name
        For Instagram: the user's IG display name

      message_type:
        The type of content (text, image, audio, etc.)

      text:
        The text body of the message. None for non-text messages
        (though image/document messages may have a caption here).

      attachments:
        List of media files attached to the message.
        Empty list for text-only messages.

      location:
        Populated only when message_type == location.

      timestamp:
        When the customer sent the message (from the channel's metadata).
        Always UTC. For WhatsApp this comes as Unix epoch seconds.

      raw_payload:
        The original raw dict from the channel, stored for debugging/audit.
        Never use this in business logic — always use the normalized fields.

      phone_number_id:
        WhatsApp-specific: your business phone number ID.
        Needed to send replies back via the correct phone number.
        None for non-WhatsApp channels.
    """
    channel: Channel
    channel_message_id: str
    customer_channel_id: str
    customer_name: Optional[str]
    message_type: MessageType
    text: Optional[str]
    attachments: list[MediaAttachment] = field(default_factory=list)
    location: Optional[LocationData] = None
    timestamp: Optional[datetime] = None
    phone_number_id: Optional[str] = None    # WhatsApp only
    raw_payload: Optional[dict] = None       # For debugging/audit only


# ─── Parse Result ─────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ParseResult:
    """
    Container returned by a channel parser.

    A single webhook POST from Meta can contain MULTIPLE messages
    (batching is rare but possible). The parser always returns a list.

    messages: Successfully parsed IncomingMessage objects.
    errors: Any parsing errors (malformed messages, unknown types, etc.)
            Errors are logged but do not prevent other messages from processing.
    """
    messages: list[IncomingMessage] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

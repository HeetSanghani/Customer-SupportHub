"""
app/services/whatsapp/parser.py

WhatsApp Channel Adapter — converts raw Meta Cloud API payloads
into normalized IncomingMessage objects.

RESPONSIBILITY:
  This module has exactly ONE job: take the raw dict that Meta sends
  to your webhook and convert it into a list of IncomingMessage objects.

  It handles:
    ✅ Text messages
    ✅ Image messages (with caption)
    ✅ Audio messages
    ✅ Video messages
    ✅ Document messages
    ✅ Location messages
    ✅ Sticker messages
    ✅ Status updates (delivery receipts — filtered OUT, not processed as messages)
    ✅ Malformed / unknown message types (graceful degradation)

  It does NOT handle:
    ✗ Database operations
    ✗ AI calls
    ✗ Sending replies
    ✗ Business logic

META PAYLOAD STRUCTURE (high-level):
  payload
    .object                   → "whatsapp_business_account"
    .entry[]
      .id                     → WABA ID
      .changes[]
        .field                → "messages"
        .value
          .metadata
            .phone_number_id  → Your business phone number ID
          .contacts[]
            .wa_id            → Customer phone number
            .profile.name     → Customer display name
          .messages[]
            .id               → Unique message ID (use for idempotency)
            .from             → Customer phone number
            .timestamp        → Unix epoch (seconds)
            .type             → "text" | "image" | "audio" | ...
            .text.body        → Message content (when type == "text")
            .image.id         → Media ID to fetch (when type == "image")
          .statuses[]         → Delivery receipts — SKIP THESE
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from app.services.channels.models import (
    Channel,
    IncomingMessage,
    LocationData,
    MediaAttachment,
    MessageType,
    ParseResult,
)

logger = logging.getLogger(__name__)


# ─── Message Type Mapping ─────────────────────────────────────────────────────

_WA_TYPE_MAP: dict[str, MessageType] = {
    "text": MessageType.text,
    "image": MessageType.image,
    "audio": MessageType.audio,
    "video": MessageType.video,
    "document": MessageType.document,
    "location": MessageType.location,
    "sticker": MessageType.sticker,
    "reaction": MessageType.reaction,
    "interactive": MessageType.interactive,
}


# ─── Internal Helpers ─────────────────────────────────────────────────────────

def _parse_timestamp(ts_str: Optional[str]) -> Optional[datetime]:
    """
    Convert WhatsApp Unix epoch string to UTC datetime.

    WhatsApp sends timestamps as epoch SECONDS (not milliseconds).
    Example: "1722918000" → datetime(2026, 8, 6, 5, 0, 0, tzinfo=UTC)
    """
    if not ts_str:
        return None
    try:
        return datetime.fromtimestamp(int(ts_str), tz=timezone.utc)
    except (ValueError, OSError) as exc:
        logger.warning("Failed to parse WhatsApp timestamp '%s': %s", ts_str, exc)
        return None


def _extract_contact_name(contacts: list[dict], wa_id: str) -> Optional[str]:
    """
    Find the customer's display name from the contacts array.

    The contacts array contains profile info for each sender in the payload.
    We match by wa_id to find the right contact.
    """
    for contact in contacts:
        if contact.get("wa_id") == wa_id:
            return contact.get("profile", {}).get("name")
    # Fallback: return name from first contact if only one exists
    if contacts:
        return contacts[0].get("profile", {}).get("name")
    return None


def _parse_media_attachment(
    msg: dict,
    media_type: str,
) -> Optional[MediaAttachment]:
    """
    Extract a MediaAttachment from a media message dict.

    For image, audio, video, document, sticker messages.
    The media_id is the handle you use with Meta's Media API
    (GET /media/{media_id}) to download the actual file bytes.

    Note: Meta does NOT send the file directly in the webhook.
    You get an ID, and must make a separate authenticated API call to download.
    """
    media_data = msg.get(media_type, {})
    if not media_data:
        return None

    return MediaAttachment(
        media_id=media_data.get("id"),
        url=None,                              # Requires separate Media API call
        mime_type=media_data.get("mime_type"),
        filename=media_data.get("filename"),   # Only present for documents
        caption=media_data.get("caption"),     # Optional user-typed caption
    )


def _parse_single_message(
    msg: dict,
    contacts: list[dict],
    phone_number_id: str,
    raw_value: dict,
) -> Optional[IncomingMessage]:
    """
    Parse a single message dict from the Meta payload into an IncomingMessage.

    Returns None if the message should be skipped (e.g., unknown type, missing data).

    Args:
        msg: The individual message dict from payload.entry[].changes[].value.messages[]
        contacts: The contacts array from the same value object
        phone_number_id: Your business phone number ID from metadata
        raw_value: The full value object (stored in raw_payload for debugging)
    """
    msg_id: Optional[str] = msg.get("id")
    from_phone: Optional[str] = msg.get("from")
    msg_type_str: str = msg.get("type", "unknown")
    timestamp_str: Optional[str] = msg.get("timestamp")

    # Guard: message ID and sender phone are mandatory
    if not msg_id:
        logger.warning("WhatsApp message missing 'id' — skipping: %s", msg)
        return None

    if not from_phone:
        logger.warning("WhatsApp message %s missing 'from' — skipping.", msg_id)
        return None

    # Resolve message type
    message_type = _WA_TYPE_MAP.get(msg_type_str, MessageType.unknown)
    if message_type == MessageType.unknown:
        logger.info(
            "WhatsApp message %s has unknown type '%s' — creating record with unknown type.",
            msg_id,
            msg_type_str,
        )

    # Extract customer name
    customer_name = _extract_contact_name(contacts, from_phone)

    # Extract text content
    text: Optional[str] = None
    attachments: list[MediaAttachment] = []
    location: Optional[LocationData] = None

    if message_type == MessageType.text:
        text = msg.get("text", {}).get("body", "").strip() or None

    elif message_type in (MessageType.image, MessageType.video, MessageType.sticker):
        attachment = _parse_media_attachment(msg, message_type.value)
        if attachment:
            attachments.append(attachment)
            text = attachment.caption  # e.g., user captioned the image

    elif message_type == MessageType.audio:
        attachment = _parse_media_attachment(msg, "audio")
        if attachment:
            attachments.append(attachment)

    elif message_type == MessageType.document:
        attachment = _parse_media_attachment(msg, "document")
        if attachment:
            attachments.append(attachment)
            text = attachment.caption

    elif message_type == MessageType.location:
        loc_data = msg.get("location", {})
        try:
            location = LocationData(
                latitude=float(loc_data["latitude"]),
                longitude=float(loc_data["longitude"]),
                name=loc_data.get("name"),
                address=loc_data.get("address"),
            )
            # Create a text representation for the AI/agent
            text = f"[Location shared] {location.name or ''} ({location.latitude}, {location.longitude})"
        except (KeyError, ValueError, TypeError) as exc:
            logger.warning("Failed to parse location data for message %s: %s", msg_id, exc)

    elif message_type == MessageType.reaction:
        # Reactions are emoji responses to a specific message — log but don't process as support ticket
        emoji = msg.get("reaction", {}).get("emoji", "")
        logger.info("WhatsApp reaction '%s' on message %s — skipping.", emoji, msg_id)
        return None

    elif message_type == MessageType.interactive:
        # Button reply or list reply
        interactive_data = msg.get("interactive", {})
        if interactive_data.get("type") == "button_reply":
            text = interactive_data.get("button_reply", {}).get("title", "")
        elif interactive_data.get("type") == "list_reply":
            text = interactive_data.get("list_reply", {}).get("title", "")

    return IncomingMessage(
        channel=Channel.whatsapp,
        channel_message_id=msg_id,
        customer_channel_id=from_phone,
        customer_name=customer_name,
        message_type=message_type,
        text=text,
        attachments=attachments,
        location=location,
        timestamp=_parse_timestamp(timestamp_str),
        phone_number_id=phone_number_id,
        raw_payload=raw_value,
    )


# ─── Public API ───────────────────────────────────────────────────────────────

def parse_whatsapp_payload(payload: dict) -> ParseResult:
    """
    Parse a complete Meta WhatsApp Cloud API webhook payload.

    This is the public entry point for the WhatsApp parser.
    Takes the raw dict from the POST body and returns a ParseResult
    containing a list of IncomingMessage objects.

    IMPORTANT — What gets SKIPPED:
      - Status updates (delivery receipts, read receipts) — not customer messages
      - Reaction messages — not actionable support content
      - Messages with missing required fields (msg_id, from)
      - Non-"messages" field changes (e.g., template status updates)

    Args:
        payload: The raw JSON dict from Meta's webhook POST body.

    Returns:
        ParseResult with .messages (list of IncomingMessage) and .errors (list of str).
    """
    messages: list[IncomingMessage] = []
    errors: list[str] = []

    # Guard: verify this is a WhatsApp payload (not FB/IG)
    if payload.get("object") != "whatsapp_business_account":
        logger.warning(
            "Unexpected webhook object type: '%s' — expected 'whatsapp_business_account'",
            payload.get("object"),
        )
        return ParseResult(messages=[], errors=["unexpected_object_type"])

    entries: list[dict] = payload.get("entry", [])

    for entry_idx, entry in enumerate(entries):
        changes: list[dict] = entry.get("changes", [])

        for change_idx, change in enumerate(changes):
            # We only care about the "messages" field
            # Other fields: "message_template_status_update", "phone_number_quality_update"
            if change.get("field") != "messages":
                logger.debug(
                    "Skipping change with field='%s' (entry=%d, change=%d)",
                    change.get("field"),
                    entry_idx,
                    change_idx,
                )
                continue

            value: dict = change.get("value", {})

            # Skip if this change contains ONLY status updates (no messages)
            if "statuses" in value and "messages" not in value:
                logger.debug(
                    "Skipping status-only change (entry=%d, change=%d) — "
                    "contains delivery/read receipts, not customer messages.",
                    entry_idx,
                    change_idx,
                )
                continue

            # Extract metadata
            metadata: dict = value.get("metadata", {})
            phone_number_id: str = metadata.get("phone_number_id", "")
            contacts: list[dict] = value.get("contacts", [])
            raw_messages: list[dict] = value.get("messages", [])

            if not phone_number_id:
                logger.warning(
                    "WhatsApp webhook value missing metadata.phone_number_id "
                    "(entry=%d, change=%d) — messages may still be processed.",
                    entry_idx,
                    change_idx,
                )

            # Parse each individual message
            for msg_idx, msg in enumerate(raw_messages):
                try:
                    parsed = _parse_single_message(
                        msg=msg,
                        contacts=contacts,
                        phone_number_id=phone_number_id,
                        raw_value=value,
                    )
                    if parsed is not None:
                        messages.append(parsed)
                        logger.info(
                            "Parsed WhatsApp message | id=%s | from=%s | type=%s",
                            parsed.channel_message_id,
                            parsed.customer_channel_id,
                            parsed.message_type.value,
                        )
                except Exception as exc:
                    error_msg = (
                        f"Failed to parse message at entry={entry_idx} "
                        f"change={change_idx} msg={msg_idx}: {exc}"
                    )
                    logger.error(error_msg, exc_info=True)
                    errors.append(error_msg)

    logger.info(
        "WhatsApp payload parsed: %d message(s), %d error(s)",
        len(messages),
        len(errors),
    )
    return ParseResult(messages=messages, errors=errors)

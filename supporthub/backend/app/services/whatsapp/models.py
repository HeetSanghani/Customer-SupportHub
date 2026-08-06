"""
app/services/whatsapp/models.py

Domain models and value objects for the WhatsApp Outbound Delivery Layer.

WHY THIS FILE EXISTS:
  These pure Python dataclasses and enums represent the contracts between:
    - AI Response / Webhook Handler → WhatsApp Sender
    - WhatsApp Sender → Outbound Formatter
    - Meta HTTP Client → Delivery Tracker / Repository

  Using explicit value objects ensures immutability, zero database coupling,
  and type safety across the delivery pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


# ─── Delivery Status Enum ─────────────────────────────────────────────────────

class DeliveryStatus(str, Enum):
    """
    Lifecycle states of an outbound WhatsApp message.

    Transition flow:
      queued → sending → sent → delivered → read
                    └──────────→ failed
                    └──────────→ retrying → sending
    """
    queued = "queued"
    sending = "sending"
    sent = "sent"            # Accepted by Meta API (HTTP 200 with wamid)
    delivered = "delivered"  # Meta webhook status: delivered to customer device
    read = "read"            # Meta webhook status: read by customer
    failed = "failed"        # Hard failure or max retries exhausted
    retrying = "retrying"    # Transient failure, scheduled for backoff retry


# ─── Outgoing Message Dataclass ───────────────────────────────────────────────

@dataclass(frozen=True)
class OutgoingMessage:
    """
    Normalized outbound message request before Meta JSON formatting.

    Fields:
      recipient_phone: E.164 phone number (e.g. "+919876543210" or "919876543210").
      message_type: "text" | "image" | "document" | "audio" | "interactive" | "template"
      text_body: Plain text content for text messages.
      media_url: Direct download URL for image/document/audio attachments.
      caption: Optional caption for media messages.
      template_name: Meta-approved template name (if message_type == "template").
      template_language: ISO language code (e.g. "en_US").
      interactive_components: Dict defining quick replies or button components.
      idempotency_key: Unique client-generated UUID for duplicate send protection.
    """
    recipient_phone: str
    message_type: str = "text"
    text_body: Optional[str] = None
    media_url: Optional[str] = None
    caption: Optional[str] = None
    template_name: Optional[str] = None
    template_language: str = "en_US"
    interactive_components: Optional[dict[str, Any]] = None
    idempotency_key: Optional[str] = None


# ─── Provider Response Dataclass ──────────────────────────────────────────────

@dataclass(frozen=True)
class ProviderResponse:
    """
    Normalized HTTP response returned directly by Meta API Client (`client.py`).

    Fields:
      success: True if HTTP 200/201 and Meta returned a message ID.
      provider_message_id: Meta's official message identifier (e.g. "wamid.HBgL...").
      status_code: HTTP status code returned by Meta servers.
      raw_response: Complete raw JSON dictionary returned by Meta.
      error_message: Extracted error message if success is False.
      error_code: Meta error code integer if available.
    """
    success: bool
    provider_message_id: Optional[str] = None
    status_code: int = 200
    raw_response: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None
    error_code: Optional[int] = None


# ─── Delivery Result Dataclass ────────────────────────────────────────────────

@dataclass
class DeliveryResult:
    """
    Final summary object returned by `WhatsAppSender.send()` to callers.

    Fields:
      conversation_id: Ticket/Conversation reference (e.g. "TCK-10023").
      outbound_message_id: Local Message DB primary key or UUID.
      provider_message_id: Meta's `wamid` if successfully dispatched.
      recipient_phone: Target phone number.
      status: DeliveryStatus enum value.
      retry_count: Number of retries executed before final state.
      latency_ms: Total duration of Meta HTTP dispatch in milliseconds.
      error_message: Explanatory error text if status is failed.
      sent_at: UTC timestamp when message was accepted by Meta.
    """
    conversation_id: str
    recipient_phone: str
    outbound_message_id: Optional[str] = None
    provider_message_id: Optional[str] = None
    status: DeliveryStatus = DeliveryStatus.queued
    retry_count: int = 0
    latency_ms: int = 0
    error_message: Optional[str] = None
    sent_at: Optional[datetime] = None


# ─── Retry Policy Config Object ───────────────────────────────────────────────

@dataclass(frozen=True)
class RetryPolicy:
    """
    Configuration parameters for outbound retry logic (`retry.py`).

    Fields:
      max_retries: Total retry attempts allowed for transient failures.
      base_delay_seconds: Initial backoff delay (seconds).
      max_delay_seconds: Maximum backoff delay cap (seconds).
      exponential_factor: Multiplier for backoff curve.
      retryable_status_codes: HTTP status codes eligible for retry.
    """
    max_retries: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 10.0
    exponential_factor: float = 2.0
    retryable_status_codes: set[int] = field(
        default_factory=lambda: {429, 500, 502, 503, 504}
    )

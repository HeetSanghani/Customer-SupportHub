"""
app/services/whatsapp/delivery.py

Outbound Delivery State Machine and Status Tracker.

WHY THIS FILE EXISTS:
  An outbound message passes through several distinct lifecycle states:
    `queued` → `sending` → `sent` → `delivered` → `read`
                   └──────────→ `retrying` → `sending`
                   └──────────→ `failed`

  Without a central state machine:
    - Out-of-order webhooks (e.g., `read` arriving before `delivered`) corrupt status state.
    - Status transitions become chaotic and unvalidated.
    - Timestamp logging (`sent_at`, `delivered_at`, `read_at`) gets lost.

  This file acts as a Delivery State Tracker and transition guard that:
    1. Enforces valid state transitions.
    2. Provides hooks for processing incoming Meta Delivery Status Webhook events.
    3. Maintains accurate timing metrics across the lifecycle.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from app.services.whatsapp.models import DeliveryStatus

logger = logging.getLogger(__name__)


# ─── Allowed State Transitions ────────────────────────────────────────────────

ALLOWED_TRANSITIONS: dict[DeliveryStatus, set[DeliveryStatus]] = {
    DeliveryStatus.queued: {DeliveryStatus.sending, DeliveryStatus.failed},
    DeliveryStatus.sending: {DeliveryStatus.sent, DeliveryStatus.retrying, DeliveryStatus.failed},
    DeliveryStatus.retrying: {DeliveryStatus.sending, DeliveryStatus.failed},
    DeliveryStatus.sent: {DeliveryStatus.delivered, DeliveryStatus.read, DeliveryStatus.failed},
    DeliveryStatus.delivered: {DeliveryStatus.read, DeliveryStatus.failed},
    DeliveryStatus.read: set(),   # Terminal state
    DeliveryStatus.failed: set(), # Terminal state
}


@dataclass
class DeliveryState:
    """
    In-memory representation of an outbound message's delivery status & timeline.
    """
    outbound_id: str
    recipient: str
    provider_message_id: Optional[str] = None
    status: DeliveryStatus = DeliveryStatus.queued
    retry_count: int = 0
    queued_at: datetime = datetime.now(timezone.utc)
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class DeliveryTracker:
    """
    Delivery state manager enforcing lifecycle state transitions.

    Usage:
        tracker = DeliveryTracker(outbound_id="out_123", recipient="919876543210")
        tracker.transition_to(DeliveryStatus.sending)
        tracker.mark_sent(wamid="wamid.HBgL...")
    """

    def __init__(self, outbound_id: str, recipient: str) -> None:
        self.state = DeliveryState(outbound_id=outbound_id, recipient=recipient)

    @property
    def current_status(self) -> DeliveryStatus:
        return self.state.status

    def can_transition_to(self, new_status: DeliveryStatus) -> bool:
        """Check if transitioning from current_status to new_status is valid."""
        allowed = ALLOWED_TRANSITIONS.get(self.state.status, set())
        return new_status in allowed

    def transition_to(
        self,
        new_status: DeliveryStatus,
        error_message: Optional[str] = None,
    ) -> bool:
        """
        Transition state to new_status if allowed. Returns True if transition occurred.
        Logs warning on invalid transition (e.g. out-of-order webhooks).
        """
        if not self.can_transition_to(new_status):
            logger.warning(
                "⚠️ Invalid delivery state transition ignored: %s → %s | outbound_id=%s",
                self.state.status.value,
                new_status.value,
                self.state.outbound_id,
            )
            return False

        old_status = self.state.status
        self.state.status = new_status
        now = datetime.now(timezone.utc)

        if new_status == DeliveryStatus.sending:
            pass
        elif new_status == DeliveryStatus.sent:
            self.state.sent_at = now
        elif new_status == DeliveryStatus.delivered:
            self.state.delivered_at = now
        elif new_status == DeliveryStatus.read:
            self.state.read_at = now
        elif new_status == DeliveryStatus.failed:
            self.state.failed_at = now
            self.state.error_message = error_message
        elif new_status == DeliveryStatus.retrying:
            self.state.retry_count += 1

        logger.info(
            "🔄 Delivery state transition | outbound_id=%s | %s → %s",
            self.state.outbound_id,
            old_status.value,
            new_status.value,
        )

        return True

    # ─── Convenience Helpers ──────────────────────────────────────────────────

    def mark_sent(self, provider_message_id: str) -> None:
        """Mark message as successfully accepted by Meta API."""
        self.state.provider_message_id = provider_message_id
        self.transition_to(DeliveryStatus.sent)

    def mark_failed(self, error_message: str) -> None:
        """Mark message delivery as failed."""
        self.transition_to(DeliveryStatus.failed, error_message=error_message)

    def mark_retrying(self) -> None:
        """Mark message as queued for retry attempt."""
        self.transition_to(DeliveryStatus.retrying)

    # ─── Webhook Status Interfaces (Prepared for Future Webhooks) ─────────────

    def handle_status_webhook(self, status_str: str, timestamp_str: Optional[str] = None) -> None:
        """
        Prepared interface for future Meta Status Webhook notifications (sent, delivered, read, failed).
        """
        status_map = {
            "sent": DeliveryStatus.sent,
            "delivered": DeliveryStatus.delivered,
            "read": DeliveryStatus.read,
            "failed": DeliveryStatus.failed,
        }
        target_status = status_map.get(status_str.lower())
        if target_status:
            self.transition_to(target_status)

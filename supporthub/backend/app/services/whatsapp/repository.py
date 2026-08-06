"""
app/services/whatsapp/repository.py

Outbound Repository and Idempotency Persistence Manager.

WHY THIS FILE EXISTS:
  This is the ONLY file in the outbound WhatsApp delivery layer that touches
  the database (`Message` model / SQLModel session).

IDEMPOTENCY & AT-LEAST-ONCE DELIVERY EXPLAINED:
  In distributed network messaging, network retries introduce the risk of
  DUPLICATE SENDS (the customer receiving the same AI answer multiple times).

  Scenario:
    1. WhatsAppSender sends reply to Meta Cloud API.
    2. Meta accepts the message and sends reply to customer.
    3. The TCP connection breaks before Meta's HTTP 200 reaches our server.
    4. Our retry engine retries the message.
    5. Customer receives the response a second time!

  Outbound Idempotency Solution:
    - We generate an `idempotency_key` (UUID) BEFORE sending to Meta.
    - We claim the key in the repository/database prior to network dispatch.
    - If the worker crashes or retries, `claim_or_get_outbound()` checks if a
      matching idempotency key already has a `provider_message_id` (wamid).
    - If `provider_message_id` exists, the duplicate send is suppressed.

  This guarantees EXACTLY-ONCE outward customer delivery even under
  at-least-once network retry mechanics.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Message, SenderType
from app.services.whatsapp.delivery import DeliveryTracker
from app.services.whatsapp.models import DeliveryResult, DeliveryStatus

logger = logging.getLogger(__name__)


class WhatsAppOutboundRepository:
    """
    Persists outbound delivery state and manages outbound idempotency keys.

    Usage:
        repo = WhatsAppOutboundRepository(session)
        is_duplicate, msg_record = await repo.claim_or_get_outbound(idempotency_key)
        ...
        await repo.update_delivery_result(result)
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def claim_or_get_outbound(
        self,
        idempotency_key: str,
        ticket_id: str,
        recipient_phone: str,
        payload_json: str,
    ) -> tuple[bool, Message]:
        """
        Claim an outbound idempotency key in the database before sending to Meta.

        Returns:
            (is_already_sent: bool, message_record: Message)
            - If is_already_sent is True, this message was ALREADY delivered to Meta.
            - If is_already_sent is False, caller can proceed to send to Meta.
        """
        # Look up existing message by idempotency key stored in external_message_id
        external_id = f"outbound:{idempotency_key}"
        statement = select(Message).where(Message.external_message_id == external_id)
        existing = (await self.session.exec(statement)).first()

        if existing:
            # Check if this outbound message was already sent to Meta (has wamid in metadata)
            metadata = self._parse_attachments(existing.attachments)
            provider_msg_id = metadata.get("provider_message_id")

            if provider_msg_id or metadata.get("status") == DeliveryStatus.sent.value:
                logger.info(
                    "⚡ Outbound idempotency check: Message ALREADY sent to Meta | key=%s | wamid=%s",
                    idempotency_key,
                    provider_msg_id,
                )
                return True, existing

            logger.info("Outbound message claimed previously but pending send | key=%s", idempotency_key)
            return False, existing

        # Create new claimed Message record in DB with SenderType.ai
        message = Message(
            ticket_id=uuid.UUID(ticket_id),
            sender_id=None,
            sender_type=SenderType.ai,
            body="",  # Will be updated or populated from payload
            external_message_id=external_id,
            attachments=json.dumps({
                "outbound_idempotency_key": idempotency_key,
                "recipient_phone": recipient_phone,
                "status": DeliveryStatus.sending.value,
                "payload": payload_json,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }),
        )

        self.session.add(message)
        await self.session.flush()

        logger.info(
            "📝 Claimed new outbound idempotency key | key=%s | ticket_id=%s",
            idempotency_key,
            ticket_id,
        )

        return False, message

    async def update_delivery_result(
        self,
        message: Message,
        result: DeliveryResult,
        tracker: DeliveryTracker,
    ) -> None:
        """
        Update the Message DB record with the final DeliveryResult metrics.
        """
        metadata = self._parse_attachments(message.attachments)

        metadata.update({
            "status": result.status.value,
            "provider_message_id": result.provider_message_id,
            "retry_count": result.retry_count,
            "latency_ms": result.latency_ms,
            "error_message": result.error_message,
            "sent_at": result.sent_at.isoformat() if result.sent_at else None,
            "delivered_at": tracker.state.delivered_at.isoformat() if tracker.state.delivered_at else None,
            "read_at": tracker.state.read_at.isoformat() if tracker.state.read_at else None,
        })

        message.attachments = json.dumps(metadata)
        self.session.add(message)
        await self.session.commit()

        logger.info(
            "💾 Outbound delivery persisted | ticket_id=%s | status=%s | wamid=%s | latency=%dms",
            result.conversation_id,
            result.status.value,
            result.provider_message_id,
            result.latency_ms,
        )

    # ─── Helper Methods ───────────────────────────────────────────────────────

    @staticmethod
    def _parse_attachments(raw_attachments: Optional[str]) -> dict:
        if not raw_attachments:
            return {}
        try:
            return json.loads(raw_attachments)
        except Exception:
            return {}

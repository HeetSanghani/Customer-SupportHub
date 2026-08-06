"""
app/services/whatsapp/sender.py

High-Level Outbound Delivery Orchestrator for WhatsApp.

THE CONDUCTOR OF OUTBOUND DELIVERY:
  This file coordinates the complete outbound delivery flow.
  It does NOT:
    - Format payloads (that's `formatter.py`)
    - Execute HTTP requests directly (that's `client.py`)
    - Manage backoff retries directly (that's `retry.py`)
    - Track state machine transitions directly (that's `delivery.py`)
    - Touch raw DB tables directly (that's `repository.py`)

  It ONLY orchestrates:

    ConversationContext + AIResponse (Input)
                    │
                    ▼
     WhatsAppPayloadFormatter.format()
                    │
                    ▼
   WhatsAppOutboundRepository.claim()  (Idempotency Check)
                    │
                    ▼
        DeliveryTracker.transition()
                    │
                    ▼
  RetryExecutor(MetaWhatsAppClient.send())  (HTTP + Retries)
                    │
                    ▼
   WhatsAppOutboundRepository.update()
                    │
                    ▼
          DeliveryResult (Output)
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.ai.models import AIResponse
from app.services.conversations.models import ConversationContext
from app.services.whatsapp.client import MetaWhatsAppClient
from app.services.whatsapp.delivery import DeliveryTracker
from app.services.whatsapp.exceptions import WhatsAppDeliveryError
from app.services.whatsapp.formatter import WhatsAppPayloadFormatter
from app.services.whatsapp.models import (
    DeliveryResult,
    DeliveryStatus,
    OutgoingMessage,
    RetryPolicy,
)
from app.services.whatsapp.repository import WhatsAppOutboundRepository
from app.services.whatsapp.retry import RetryExecutor

logger = logging.getLogger(__name__)


class WhatsAppSender:
    """
    High-level orchestrator for delivering AI or domain messages to WhatsApp customers.

    Usage (in webhook.py):
        sender = WhatsAppSender(session)
        result = await sender.send_ai_reply(context, ai_response)
    """

    def __init__(
        self,
        session: AsyncSession,
        client: Optional[MetaWhatsAppClient] = None,
        formatter: Optional[WhatsAppPayloadFormatter] = None,
        retry_executor: Optional[RetryExecutor] = None,
        repository: Optional[WhatsAppOutboundRepository] = None,
    ) -> None:
        self.session = session
        self.client = client or MetaWhatsAppClient()
        self.formatter = formatter or WhatsAppPayloadFormatter()
        self.retry_executor = retry_executor or RetryExecutor(policy=RetryPolicy())
        self.repository = repository or WhatsAppOutboundRepository(session)

    async def send_ai_reply(
        self,
        context: ConversationContext,
        ai_response: AIResponse,
        idempotency_key: Optional[str] = None,
    ) -> DeliveryResult:
        """
        Deliver an AIResponse to a customer on WhatsApp based on ConversationContext.

        Args:
            context: ConversationContext from Step 3A.
            ai_response: AIResponse from Step 3B.
            idempotency_key: Optional unique key (generated automatically if None).

        Returns:
            DeliveryResult containing delivery status, wamid, and latency.
        """
        # Determine recipient phone number from customer context
        recipient_phone = (
            getattr(context.customer, "channel_customer_id", "")
            or context.incoming_message.customer_channel_id
        )

        # 1. Format payload using Formatter
        payload = self.formatter.format_ai_response(
            ai_response=ai_response,
            recipient_phone=recipient_phone,
        )

        key = idempotency_key or f"ai_reply_{context.incoming_message.channel_message_id}"

        return await self._orchestrate_send(
            ticket_id=str(context.ticket.id),
            conversation_ref=context.conversation_ref,
            recipient_phone=recipient_phone,
            payload=payload,
            idempotency_key=key,
        )

    async def send_outgoing(
        self,
        ticket_id: str,
        conversation_ref: str,
        message: OutgoingMessage,
    ) -> DeliveryResult:
        """
        Deliver a generic OutgoingMessage (template, media, interactive) to WhatsApp.
        """
        payload = self.formatter.format_outgoing(message)
        key = message.idempotency_key or f"out_{uuid.uuid4().hex[:12]}"

        return await self._orchestrate_send(
            ticket_id=ticket_id,
            conversation_ref=conversation_ref,
            recipient_phone=message.recipient_phone,
            payload=payload,
            idempotency_key=key,
        )

    # ─── Orchestration Pipeline ───────────────────────────────────────────────

    async def _orchestrate_send(
        self,
        ticket_id: str,
        conversation_ref: str,
        recipient_phone: str,
        payload: dict,
        idempotency_key: str,
    ) -> DeliveryResult:
        """
        Execute the 5-step outbound delivery pipeline.
        """
        start_time = time.monotonic()
        clean_phone = WhatsAppPayloadFormatter.normalize_phone(recipient_phone)
        payload_str = json.dumps(payload)

        # ── Step 1: Idempotency Claim ─────────────────────────────────────────
        is_sent, msg_record = await self.repository.claim_or_get_outbound(
            idempotency_key=idempotency_key,
            ticket_id=ticket_id,
            recipient_phone=clean_phone,
            payload_json=payload_str,
        )

        if is_sent:
            # Message was ALREADY sent in a previous execution — suppress duplicate send
            metadata = WhatsAppOutboundRepository._parse_attachments(msg_record.attachments)
            provider_wamid = metadata.get("provider_message_id") or msg_record.external_message_id

            return DeliveryResult(
                conversation_id=conversation_ref,
                recipient_phone=clean_phone,
                outbound_message_id=str(msg_record.id),
                provider_message_id=provider_wamid,
                status=DeliveryStatus.sent,
                latency_ms=0,
            )

        # ── Step 2: Initialize State Tracker ─────────────────────────────────
        tracker = DeliveryTracker(
            outbound_id=str(msg_record.id),
            recipient=clean_phone,
        )
        tracker.transition_to(DeliveryStatus.sending)

        # ── Step 3: Execute Dispatch via Client + Retry Executor ─────────────
        try:
            provider_res = await self.retry_executor.execute(
                self.client.send_payload,
                payload=payload,
            )

            latency_ms = int((time.monotonic() - start_time) * 1000)
            wamid = provider_res.provider_message_id or f"wamid.GEN_{uuid.uuid4().hex[:10]}"

            tracker.mark_sent(provider_message_id=wamid)

            result = DeliveryResult(
                conversation_id=conversation_ref,
                outbound_message_id=str(msg_record.id),
                provider_message_id=wamid,
                recipient_phone=clean_phone,
                status=DeliveryStatus.sent,
                retry_count=tracker.state.retry_count,
                latency_ms=latency_ms,
                sent_at=datetime.now(timezone.utc),
            )

        except Exception as exc:
            latency_ms = int((time.monotonic() - start_time) * 1000)
            error_msg = str(exc)

            tracker.mark_failed(error_message=error_msg)

            result = DeliveryResult(
                conversation_id=conversation_ref,
                outbound_message_id=str(msg_record.id),
                provider_message_id=None,
                recipient_phone=clean_phone,
                status=DeliveryStatus.failed,
                retry_count=tracker.state.retry_count,
                latency_ms=latency_ms,
                error_message=error_msg,
            )

        # ── Step 4: Persist Metrics to Database ──────────────────────────────
        await self.repository.update_delivery_result(
            message=msg_record,
            result=result,
            tracker=tracker,
        )

        logger.info(
            "🚀 WhatsApp outbound delivery finished | ref=%s | status=%s | wamid=%s | latency=%dms",
            conversation_ref,
            result.status.value,
            result.provider_message_id,
            result.latency_ms,
        )

        return result

"""
app/services/ai/repository.py

Data persistence for AI-generated responses.

RESPONSIBILITY:
  This is the ONLY file in the AI layer that talks to the database.
  It stores AI messages using the existing Message model (same table
  that stores customer messages). The SenderType.ai discriminates them.

WHY USE THE SAME MESSAGE TABLE:
  Using one messages table means:
    - The agent dashboard shows customer + AI messages in one query
    - Conversation history is a simple ORDER BY created_at
    - CSAT ratings can evaluate the full thread including AI responses
    - No JOIN between separate tables needed

  The existing Message model has everything we need:
    - ticket_id: the conversation thread
    - sender_type: SenderType.ai
    - body: the AI's reply text
    - external_message_id: we'll use this to store prompt_version+model
    - attachments: we'll repurpose to store AI metadata as JSON

OBSERVABILITY FIELDS STORED:
  Every AI message record stores:
    - model_name (via external_message_id prefix)
    - prompt_version
    - input/output tokens
    - latency_ms
    - confidence
    - estimated cost
    - finish_reason
    - error (if fallback was used)

  This is stored in the attachments JSON field since the existing Message
  model doesn't have dedicated columns for these. In a greenfield design,
  you'd add a separate ai_message_logs table. Here we adapt cleanly.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Message, SenderType
from app.services.ai.models import AIMessageRecord, AIResponse

logger = logging.getLogger(__name__)


class AIRepository:
    """
    Persists AI-generated messages to the database.

    Usage:
        repo = AIRepository()
        record = repo.build_record(ai_response, ticket_id=str(ticket.id))
        message = await repo.store(session, record)
    """

    def build_record(
        self,
        ai_response: AIResponse,
        ticket_id: str,
    ) -> AIMessageRecord:
        """
        Build an AIMessageRecord from an AIResponse.

        The ticket_id is the Ticket.id (UUID as string).
        This is a pure mapping operation — no DB calls.
        """
        return AIMessageRecord(
            ticket_id=ticket_id,
            response_text=ai_response.response_text,
            model_name=ai_response.model.model_name,
            provider=ai_response.model.provider,
            prompt_version=ai_response.model.prompt_version,
            system_hash=ai_response.model.system_hash,
            input_tokens=ai_response.usage.input_tokens,
            output_tokens=ai_response.usage.output_tokens,
            latency_ms=ai_response.latency_ms,
            finish_reason=ai_response.finish_reason,
            confidence=ai_response.confidence,
            estimated_cost_usd=ai_response.usage.estimated_cost_usd,
            error=ai_response.error,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )

    async def store(
        self,
        session: AsyncSession,
        record: AIMessageRecord,
    ) -> Message:
        """
        Persist an AIMessageRecord as a Message row in the database.

        Returns the created Message ORM object.

        AI metadata (tokens, latency, cost, etc.) is stored in the
        attachments JSON field as a structured metadata dict.
        """
        # Pack all AI observability data into the attachments JSON field
        ai_metadata = {
            "ai_metadata": {
                "provider": record.provider,
                "model_name": record.model_name,
                "prompt_version": record.prompt_version,
                "system_hash": record.system_hash,
                "input_tokens": record.input_tokens,
                "output_tokens": record.output_tokens,
                "latency_ms": record.latency_ms,
                "finish_reason": record.finish_reason,
                "confidence": record.confidence,
                "estimated_cost_usd": record.estimated_cost_usd,
                "error": record.error,
            }
        }

        message = Message(
            ticket_id=uuid.UUID(record.ticket_id),
            sender_id=None,                  # AI has no user account
            sender_type=SenderType.ai,
            body=record.response_text,
            external_message_id=f"ai:{record.prompt_version}:{record.model_name}",
            attachments=json.dumps(ai_metadata),
        )

        session.add(message)
        await session.flush()

        logger.info(
            "AI message stored | ticket_id=%s | model=%s | tokens=%d+%d | "
            "latency=%dms | confidence=%.2f | cost=$%.6f",
            record.ticket_id,
            record.model_name,
            record.input_tokens,
            record.output_tokens,
            record.latency_ms,
            record.confidence,
            record.estimated_cost_usd,
        )

        return message

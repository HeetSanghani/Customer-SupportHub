"""
app/routers/instagram.py

Instagram channel router — handles Instagram-specific AI suggestions and channel tools.
"""

from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlmodel import select as sql_select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.dependencies import require_role
from app.models import Message, Ticket, TicketChannel, User, UserRole
from app.services.ai.knowledge_rag import get_relevant_kb_context
from app.services.ai.orchestrator import AIOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/instagram", tags=["instagram"])


class InstagramAiReplyIn(BaseModel):
    tone: Optional[str] = "standard"  # "standard" | "shorter" | "professional" | "friendly"


class InstagramAiReplyOut(BaseModel):
    success: bool = True
    ticket_id: str
    suggested_reply: str
    suggestion: str  # compatibility field
    is_fallback: bool = False
    confidence: float = 1.0
    latency_ms: int = 0


@router.post(
    "/tickets/{ticket_id}/ai-reply",
    response_model=InstagramAiReplyOut,
    status_code=status.HTTP_200_OK,
    summary="Generate AI Suggested Reply for Instagram DM Ticket",
)
async def generate_instagram_ai_reply(
    ticket_id: uuid.UUID,
    payload: Optional[InstagramAiReplyIn] = None,
    tone: Optional[str] = Query(None),
    current_user: User = Depends(require_role(UserRole.agent)),
    session: AsyncSession = Depends(get_session),
):
    """
    Generate an AI-powered suggested reply for an Instagram DM conversation.

    Workflow:
    1. Authenticates agent / manager / admin role.
    2. Verifies ticket exists and belongs to the Instagram channel.
    3. Loads multi-turn conversation history and customer metadata.
    4. Retrieves relevant Knowledge Base articles for policy grounding.
    5. Formats the prompt using Instagram DM-specific tone rules (friendly, concise, no markdown headers).
    6. Returns suggested reply to be inserted into the agent's message composer.
    """
    logger.info(
        "[IG AI] Suggested reply requested | ticket_id=%s | user=%s | role=%s",
        ticket_id,
        current_user.email,
        current_user.role,
    )

    ticket = await session.get(Ticket, ticket_id)
    if not ticket or ticket.deleted_at:
        logger.warning("[IG AI] Ticket not found or deleted | ticket_id=%s", ticket_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )

    # Validate channel
    if ticket.channel != TicketChannel.instagram:
        channel_name = ticket.channel.value if hasattr(ticket.channel, 'value') else str(ticket.channel)
        logger.warning(
            "[IG AI] Invalid channel for Instagram endpoint | ticket_id=%s | channel=%s",
            ticket_id,
            channel_name,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ticket {ticket_id} belongs to channel '{channel_name}', not 'instagram'",
        )

    # Load conversation history
    msgs_stmt = (
        sql_select(Message)
        .where(Message.ticket_id == ticket_id)
        .order_by(Message.created_at.asc())
        .limit(30)
    )
    msgs_result = await session.exec(msgs_stmt)
    messages = list(msgs_result.all())

    logger.info(
        "[IG AI] Loaded conversation | ticket_id=%s | ref=%s | messages_count=%d",
        ticket_id,
        ticket.ref,
        len(messages),
    )

    # Load customer profile
    customer = None
    if ticket.customer_id:
        customer = await session.get(User, ticket.customer_id)

    # Determine requested tone
    resolved_tone = (payload.tone if payload and payload.tone else None) or tone or "standard"

    # Retrieve Knowledge Base articles for factual grounding
    search_query = f"{ticket.subject} {ticket.category or ''}"
    if messages:
        for m in reversed(messages):
            if m.body and m.body.strip():
                search_query += f" {m.body.strip()[:100]}"
                break

    kb_context = await get_relevant_kb_context(session, search_query)

    # Orchestrate AI response generation
    orchestrator = AIOrchestrator(session=session)
    ai_response = await orchestrator.generate_for_ticket(
        ticket=ticket,
        messages=messages,
        customer=customer,
        kb_context=kb_context,
        tone=resolved_tone,
    )

    logger.info(
        "[IG AI] Suggested reply generated | ticket_id=%s | is_fallback=%s | latency_ms=%d | tokens=%d+%d",
        ticket_id,
        ai_response.is_fallback,
        ai_response.latency_ms,
        ai_response.usage.input_tokens,
        ai_response.usage.output_tokens,
    )

    return InstagramAiReplyOut(
        success=True,
        ticket_id=str(ticket.id),
        suggested_reply=ai_response.response_text,
        suggestion=ai_response.response_text,
        is_fallback=ai_response.is_fallback,
        confidence=ai_response.confidence,
        latency_ms=ai_response.latency_ms,
    )

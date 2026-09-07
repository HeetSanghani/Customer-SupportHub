"""
app/services/ai/ticket_embeddings.py

Service for generating, storing, and searching pgvector ticket embeddings.
"""

from __future__ import annotations

import logging
from typing import List, Tuple, Optional
from datetime import datetime, timezone
import uuid

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, func

from app.models import Ticket, TicketEmbedding, TicketStatus
from app.rag.embeddings import GoogleEmbeddingProvider

logger = logging.getLogger(__name__)

# Module-level embedding provider instance
_embedding_provider = GoogleEmbeddingProvider()


def get_ticket_text_for_embedding(ticket: Ticket) -> str:
    """Build standardized input text for ticket vector embedding."""
    subject = ticket.subject or ""
    category = ticket.category or ""
    return f"{subject} {category}".strip()


async def ensure_ticket_embedding(
    session: AsyncSession,
    ticket: Ticket,
    force_update: bool = False
) -> Optional[TicketEmbedding]:
    """
    Ensure the ticket has a vector embedding stored in ticket_embeddings table.
    Uses GoogleEmbeddingProvider (768-dim real embeddings).
    """
    if not ticket or not ticket.id:
        return None

    # Check if embedding already exists
    existing = await session.exec(
        select(TicketEmbedding).where(TicketEmbedding.ticket_id == ticket.id)
    )
    ticket_emb = existing.first()

    if ticket_emb and not force_update:
        return ticket_emb

    text_to_embed = get_ticket_text_for_embedding(ticket)
    if not text_to_embed:
        return None

    # Generate 768-dim vector using retrieval_document task type
    vector = _embedding_provider.embed_text(text_to_embed, task_type="retrieval_document")

    if not ticket_emb:
        ticket_emb = TicketEmbedding(
            ticket_id=ticket.id,
            embedding=vector,
            created_at=datetime.now(),
        )
        session.add(ticket_emb)
    else:
        ticket_emb.embedding = vector
        ticket_emb.created_at = datetime.now()
        session.add(ticket_emb)

    await session.commit()
    await session.refresh(ticket_emb)
    return ticket_emb


def generate_query_embedding(query_text: str) -> List[float]:
    """Generate 768-dim vector for a search query using retrieval_query task type."""
    return _embedding_provider.embed_text(query_text, task_type="retrieval_query")

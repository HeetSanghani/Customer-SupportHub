"""
app/services/ai/knowledge_rag.py

Knowledge Base RAG (Retrieval-Augmented Generation) service.

Retrieves the most relevant KB articles for a given query using:
1. pgvector cosine similarity search (primary)
2. Keyword-based ILIKE fallback (when no embeddings exist or pgvector unavailable)

The context returned is injected into AI prompts to ground replies
in verified company policies and documentation.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

from sqlmodel import select, or_, col
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import KbArticle

logger = logging.getLogger(__name__)

# Maximum number of KB articles to retrieve
_MAX_RESULTS = 3
# Maximum characters to include from each article body
_MAX_BODY_CHARS = 500


async def get_relevant_kb_context(
    session: Optional[AsyncSession] = None,
    query: str = "",
    max_results: int = _MAX_RESULTS,
) -> Optional[str]:
    """
    Retrieve relevant KB context using canonical app/rag/ RAGPipeline.
    Canonicalized to use PGVectorRetriever on kb_chunk_embeddings.
    """
    if not query or not query.strip():
        return None

    try:
        from app.rag.pipeline import rag_pipeline
        rag_res = rag_pipeline.query(query.strip(), top_k=max_results)
        if rag_res and rag_res.get("has_knowledge"):
            context_text = rag_res.get("context_text")
            logger.info(
                "[KB RAG RETRIEVAL PATH: CANONICAL RAG PIPELINE] Retrieved %d chunks (%d chars) for query: %s",
                rag_res.get("results_count", 0), len(context_text or ""), query[:60]
            )
            return context_text
    except Exception as e:
        logger.error(
            "[KB RAG RETRIEVAL PATH: FAILED] Canonical RAG pipeline exception | type=%s | error=%s",
            type(e).__name__, e, exc_info=True
        )

    return None


async def _embed_query(query: str) -> Optional[list[float]]:
    """
    Generate an embedding vector for the query string using GoogleEmbeddingProvider.
    Returns None if embedding generation fails.
    """
    try:
        from app.rag.embeddings import GoogleEmbeddingProvider
        provider = GoogleEmbeddingProvider()
        loop = asyncio.get_event_loop()
        vec = await loop.run_in_executor(
            None,
            lambda: provider.embed_text(query, task_type="retrieval_query")
        )
        return vec
    except Exception as e:
        logger.error("[KB RAG] Embedding generation failed | type=%s | error=%s", type(e).__name__, e, exc_info=True)
        return None


def _extract_keywords(query: str) -> list[str]:
    """
    Extract meaningful keywords from a query string for ILIKE fallback search.
    Removes common stop words and short tokens.
    """
    stop_words = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "on",
        "at", "by", "for", "with", "from", "about", "as", "into", "through",
        "and", "or", "but", "not", "my", "your", "our", "their", "its",
        "i", "me", "we", "you", "he", "she", "they", "it", "this", "that",
        "what", "how", "when", "where", "why", "who", "which",
    }
    words = query.lower().split()
    keywords = [
        w.strip(".,?!;:'\"()[]")
        for w in words
        if w.strip(".,?!;:'\"()[]") and
        w.strip(".,?!;:'\"()[]") not in stop_words and
        len(w.strip(".,?!;:'\"()[]")) > 2
    ]
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique.append(kw)
    return unique[:6]

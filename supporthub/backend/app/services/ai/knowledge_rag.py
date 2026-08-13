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
    session: AsyncSession,
    query: str,
    max_results: int = _MAX_RESULTS,
) -> Optional[str]:
    """
    Retrieve relevant KB articles for a query string.

    Tries vector similarity search first (requires pgvector + embeddings),
    then falls back to keyword ILIKE search.

    Returns formatted context string for injection into AI prompts,
    or None if no relevant articles found.
    """
    if not query or not query.strip():
        return None

    query = query.strip()
    articles: list[KbArticle] = []

    # ── 1. Try pgvector similarity search ─────────────────────────────────────
    try:
        embedding = await _embed_query(query)
        if embedding:
            stmt = (
                select(KbArticle)
                .where(KbArticle.published == True)
                .where(KbArticle.embedding != None)
                .order_by(col(KbArticle.embedding).op("<=>")(embedding))
                .limit(max_results)
            )
            result = await session.exec(stmt)
            articles = list(result.all())
            if articles:
                logger.debug(
                    "[KB RAG] Vector search found %d articles for query: %s",
                    len(articles), query[:60]
                )
    except Exception as e:
        logger.warning("[KB RAG] Vector search failed, using keyword fallback: %s", e)
        articles = []

    # ── 2. Keyword fallback ────────────────────────────────────────────────────
    if not articles:
        try:
            keywords = _extract_keywords(query)
            if keywords:
                conditions = [
                    or_(
                        col(KbArticle.title).ilike(f"%{kw}%"),
                        col(KbArticle.body).ilike(f"%{kw}%"),
                        col(KbArticle.category).ilike(f"%{kw}%"),
                    )
                    for kw in keywords[:3]  # Limit to top 3 keywords
                ]
                stmt = (
                    select(KbArticle)
                    .where(KbArticle.published == True)
                    .where(or_(*conditions))
                    .order_by(KbArticle.helpful_count.desc(), KbArticle.views.desc())
                    .limit(max_results)
                )
                result = await session.exec(stmt)
                articles = list(result.all())
                if articles:
                    logger.debug(
                        "[KB RAG] Keyword fallback found %d articles for keywords: %s",
                        len(articles), keywords
                    )
        except Exception as e:
            logger.warning("[KB RAG] Keyword search also failed: %s", e)
            articles = []

    if not articles:
        logger.debug("[KB RAG] No relevant KB articles found for query: %s", query[:60])
        return None

    # ── 3. Format context for prompt injection ─────────────────────────────────
    lines = []
    for i, article in enumerate(articles, start=1):
        body_snippet = (article.body or "")[:_MAX_BODY_CHARS].strip()
        if len(article.body or "") > _MAX_BODY_CHARS:
            body_snippet += "..."
        lines.append(
            f"[Article {i}: {article.title}]\n"
            f"Category: {article.category}\n"
            f"{body_snippet}"
        )

    context = "\n\n".join(lines)
    logger.info(
        "[KB RAG] Injecting %d KB articles (%d chars) for query: %s",
        len(articles), len(context), query[:60]
    )
    return context


async def _embed_query(query: str) -> Optional[list[float]]:
    """
    Generate an embedding vector for the query string using Google's text embedding API.
    Returns None if embedding generation fails or is unavailable.
    """
    try:
        import google.generativeai as genai

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: genai.embed_content(
                model="models/text-embedding-004",
                content=query,
                task_type="retrieval_query",
            )
        )
        return result.get("embedding")
    except Exception as e:
        logger.debug("[KB RAG] Embedding generation skipped: %s", e)
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

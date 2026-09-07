"""Retriever for searching indexed RAG chunks with pgvector and Google Embeddings."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import text, type_coerce, Float

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, col, delete
from app.rag.chunker import Chunk
from app.rag.embeddings import BaseEmbeddingProvider, GoogleEmbeddingProvider, get_embedding_provider
from app.models import KbChunkEmbedding
from app.config import get_settings
from app.ai.config import settings as ai_settings

settings = get_settings()


@dataclass
class RetrievedChunk:
    """A search result chunk with relevance score and provenance."""
    chunk: Chunk
    score: float

    @property
    def source_id(self) -> str:
        return self.chunk.source_id

    @property
    def title(self) -> str:
        return self.chunk.title

    @property
    def text(self) -> str:
        return self.chunk.text


import threading

_db_loop = asyncio.new_event_loop()


def _start_db_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


_db_thread = threading.Thread(target=_start_db_event_loop, args=(_db_loop,), daemon=True)
_db_thread.start()

_rag_engine = create_async_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
)
_rag_session_maker = async_sessionmaker(_rag_engine, class_=AsyncSession, expire_on_commit=False)


def _execute_db_op(async_fn):
    """Executes an async DB function safely across any sync/async context using a single module-level engine."""
    async def _wrapper():
        async with _rag_session_maker() as session:
            return await async_fn(session)

    future = asyncio.run_coroutine_threadsafe(_wrapper(), _db_loop)
    return future.result()


class PGVectorRetriever:
    """Production pgvector-backed retriever with 768-dim Google embeddings."""

    def __init__(
        self,
        embedding_provider: Optional[BaseEmbeddingProvider] = None,
        similarity_threshold: Optional[float] = None
    ):
        self.embedding_provider = embedding_provider or get_embedding_provider()
        self.similarity_threshold = (
            similarity_threshold if similarity_threshold is not None else ai_settings.RAG_SIMILARITY_THRESHOLD
        )
        self._is_indexed_cache: Optional[bool] = None
        self._indexed_hash: Optional[str] = None

    @property
    def _is_indexed(self) -> bool:
        """Check if PostgreSQL database already contains indexed chunk embeddings."""
        if self._is_indexed_cache is True:
            return True

        async def _async_check(session: AsyncSession):
            from sqlalchemy import func
            stmt = select(func.count(KbChunkEmbedding.id))
            res = await session.exec(stmt)
            return (res.one() or 0) > 0

        try:
            is_populated = _execute_db_op(_async_check)
            if is_populated:
                self._is_indexed_cache = True
            return is_populated
        except Exception:
            return False

    def index_chunks(self, chunks: List[Chunk], force: bool = False) -> None:
        """Embed and upsert document chunks into PostgreSQL pgvector storage with Content-MD5 skip."""
        if not chunks:
            return

        import hashlib
        hasher = hashlib.md5()
        hasher.update(self.embedding_provider.__class__.__name__.encode("utf-8"))
        provider_model = getattr(self.embedding_provider, "model", "")
        if provider_model:
            hasher.update(str(provider_model).encode("utf-8"))
        for c in sorted(chunks, key=lambda x: x.chunk_id):
            hasher.update(c.chunk_id.encode("utf-8"))
            hasher.update(c.text.encode("utf-8"))
        current_hash = hasher.hexdigest()

        if not force and self._is_indexed and self._indexed_hash == current_hash and not getattr(self.embedding_provider, "quota_exceeded", False):
            import logging
            logging.getLogger(__name__).info("[Retriever] Chunks content MD5 unchanged (%s), skipping re-indexing.", current_hash[:8])
            return

        texts = [c.text for c in chunks]
        titles = [c.title for c in chunks]

        # Embed batch using retrieval_document task_type
        embeddings = self.embedding_provider.embed_batch(
            texts=texts,
            titles=titles,
            task_type="retrieval_document"
        )

        async def _async_index(session: AsyncSession):
            chunk_ids = [c.chunk_id for c in chunks]
            
            # Clean existing rows to avoid duplicate chunk_ids on re-indexing
            if chunk_ids:
                stmt = delete(KbChunkEmbedding).where(KbChunkEmbedding.chunk_id.in_(chunk_ids))
                await session.exec(stmt)
                await session.commit()

            # Insert new embeddings
            for chunk, emb in zip(chunks, embeddings):
                record = KbChunkEmbedding(
                    chunk_id=chunk.chunk_id,
                    source_id=chunk.source_id,
                    source_type=chunk.source_type,
                    title=chunk.title,
                    category=chunk.category,
                    content=chunk.text,
                    embedding=emb
                )
                session.add(record)

            await session.commit()

        _execute_db_op(_async_index)
        self._is_indexed_cache = True
        self._indexed_hash = current_hash

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        category_filter: Optional[str] = None
    ) -> List[RetrievedChunk]:
        """Retrieve top-K relevant chunks using Hybrid Search (Dense pgvector + Sparse FTS) fused with Reciprocal Rank Fusion (RRF) and Reranking."""
        if not query or not query.strip():
            return []

        k = top_k or ai_settings.RAG_TOP_K
        clean_query = query.strip()

        # Embed query using retrieval_query task_type
        query_vector = self.embedding_provider.embed_text(clean_query, task_type="retrieval_query")

        async def _async_retrieve_hybrid(session: AsyncSession):
            # 1. Dense Vector Search (<=> cosine operator)
            dense_stmt = (
                select(
                    KbChunkEmbedding.chunk_id,
                    KbChunkEmbedding.source_id,
                    KbChunkEmbedding.source_type,
                    KbChunkEmbedding.title,
                    KbChunkEmbedding.category,
                    KbChunkEmbedding.content,
                    type_coerce(col(KbChunkEmbedding.embedding).op("<=>")(query_vector), Float).label("distance")
                )
            )
            if category_filter and category_filter.strip():
                dense_stmt = dense_stmt.where(col(KbChunkEmbedding.category).ilike(category_filter.strip()))
            dense_stmt = dense_stmt.order_by(text("distance ASC")).limit(k * 3)

            dense_rows = (await session.exec(dense_stmt)).all()

            # 2. Sparse Full-Text Search (tsvector + plainto_tsquery)
            sparse_rows = []
            try:
                fts_query = text("""
                    SELECT chunk_id, source_id, source_type, title, category, content,
                           ts_rank_cd(to_tsvector('english', title || ' ' || content), plainto_tsquery('english', :q)) AS fts_score
                    FROM kb_chunk_embeddings
                    WHERE to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('english', :q)
                    ORDER BY fts_score DESC
                    LIMIT :limit
                """)
                fts_stmt = fts_query.params(q=clean_query, limit=k * 3)
                fts_res = await session.exec(fts_stmt)
                sparse_rows = fts_res.all()
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning("[Retriever] FTS query fallback skipped: %s", e)

            return dense_rows, sparse_rows

        dense_rows, sparse_rows = _execute_db_op(_async_retrieve_hybrid)

        # 3. Reciprocal Rank Fusion (RRF) with k_rrf = 60
        rrf_scores: dict[str, float] = {}
        chunk_map: dict[str, Chunk] = {}
        dense_similarity_map: dict[str, float] = {}

        # Dense ranking scores
        for rank, row in enumerate(dense_rows, start=1):
            chunk_id, source_id, source_type, title, category, content, distance = row
            sim = max(0.0, float(1.0 - distance)) if distance is not None else 0.0
            dense_similarity_map[chunk_id] = sim

            if chunk_id not in chunk_map:
                chunk_map[chunk_id] = Chunk(
                    chunk_id=chunk_id,
                    doc_id=source_id,
                    source_id=source_id,
                    source_type=source_type,
                    title=title,
                    category=category,
                    text=content
                )
            rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (60.0 + rank))

        # Sparse FTS ranking scores
        for rank, row in enumerate(sparse_rows, start=1):
            chunk_id, source_id, source_type, title, category, content, fts_score = row
            if chunk_id not in chunk_map:
                chunk_map[chunk_id] = Chunk(
                    chunk_id=chunk_id,
                    doc_id=source_id,
                    source_id=source_id,
                    source_type=source_type,
                    title=title,
                    category=category,
                    text=content
                )
            rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (60.0 + rank))

        # 4. Cross-Reranking and Relevance Score Normalization
        keywords = [w.lower().strip(".,?!;") for w in clean_query.split() if len(w) > 2]

        scored_results: List[RetrievedChunk] = []
        for chunk_id, chunk in chunk_map.items():
            base_rrf = rrf_scores.get(chunk_id, 0.0)
            dense_sim = dense_similarity_map.get(chunk_id, 0.0)

            title_text = chunk.title.lower()
            body_text = chunk.text.lower()
            keyword_hits = sum(1 for kw in keywords if kw in title_text or kw in body_text)
            title_hits = sum(1 for kw in keywords if kw in title_text)
            
            boost = 1.0 + (0.1 * keyword_hits) + (0.2 * title_hits)
            combined_score = max(dense_sim, base_rrf * 30.0) * boost

            if dense_sim >= self.similarity_threshold or base_rrf > 0.015:
                scored_results.append(RetrievedChunk(chunk=chunk, score=round(combined_score, 4)))

        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:k]


# Primary Retriever export
Retriever = PGVectorRetriever

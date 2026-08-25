"""Retriever for searching indexed RAG chunks."""
from dataclasses import dataclass
from typing import List, Optional
from app.rag.chunker import Chunk
from app.rag.embeddings import BaseEmbeddingProvider, LocalVectorEmbeddingProvider, cosine_similarity
from app.ai.config import settings


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


class Retriever:
    """Indexes and retrieves document chunks based on semantic similarity and lexical relevance."""

    def __init__(
        self,
        embedding_provider: Optional[BaseEmbeddingProvider] = None,
        similarity_threshold: Optional[float] = None
    ):
        self.embedding_provider = embedding_provider or LocalVectorEmbeddingProvider()
        self.similarity_threshold = (
            similarity_threshold if similarity_threshold is not None else settings.RAG_SIMILARITY_THRESHOLD
        )
        self.chunks: List[Chunk] = []
        self.chunk_vectors: List[List[float]] = []
        self._is_indexed: bool = False

    def index_chunks(self, chunks: List[Chunk]) -> None:
        """Build vector index over chunks."""
        self.chunks = chunks
        corpus = [f"{c.title} {c.category} {c.text}" for c in chunks]

        if isinstance(self.embedding_provider, LocalVectorEmbeddingProvider):
            self.embedding_provider.fit(corpus)

        self.chunk_vectors = self.embedding_provider.embed_batch(corpus)
        self._is_indexed = True

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        category_filter: Optional[str] = None
    ) -> List[RetrievedChunk]:
        """Retrieve top-K most relevant chunks for a user query."""
        if not self._is_indexed or not self.chunks:
            return []

        k = top_k or settings.RAG_TOP_K
        query_vector = self.embedding_provider.embed_text(query)

        scored_results: List[RetrievedChunk] = []
        for i, (chunk, vec) in enumerate(zip(self.chunks, self.chunk_vectors)):
            # Optional category filter
            if category_filter and chunk.category.lower() != category_filter.lower():
                continue

            score = cosine_similarity(query_vector, vec)
            if score >= self.similarity_threshold:
                scored_results.append(RetrievedChunk(chunk=chunk, score=score))

        # Sort descending by similarity score
        scored_results.sort(key=lambda r: r.score, reverse=True)
        return scored_results[:k]

"""End-to-end RAG Knowledge Pipeline."""
from typing import List, Dict, Any, Optional
from app.rag.document_processor import DocumentProcessor, Document
from app.rag.chunker import DocumentChunker, Chunk
from app.rag.retriever import Retriever, RetrievedChunk
from app.rag.embeddings import get_embedding_provider


class RAGPipeline:
    """Coordinates document ingestion, chunking, indexing, and retrieval."""

    def __init__(
        self,
        processor: Optional[DocumentProcessor] = None,
        chunker: Optional[DocumentChunker] = None,
        retriever: Optional[Retriever] = None
    ):
        self.processor = processor or DocumentProcessor()
        self.chunker = chunker or DocumentChunker()
        self.retriever = retriever or Retriever(embedding_provider=get_embedding_provider())
        self._initialized: bool = False
        self.documents: List[Document] = []
        self.chunks: List[Chunk] = []

    def initialize(self, force: bool = False) -> None:
        """Load, chunk, and index all policies and knowledge articles."""
        if self._initialized and not force:
            return

        self.documents = self.processor.process_all_documents()
        self.chunks = self.chunker.chunk_all(self.documents)
        if not getattr(self.retriever, "_is_indexed", False) or force:
            self.retriever.index_chunks(self.chunks, force=force)
        self._initialized = True

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        category_filter: Optional[str] = None
    ) -> List[RetrievedChunk]:
        """Search relevant chunks for a user query."""
        self.initialize()
        return self.retriever.retrieve(query=query, top_k=top_k, category_filter=category_filter)

    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """Execute query and assemble structured knowledge context with citations."""
        results = self.retrieve(query=question, top_k=top_k)
        
        citations = []
        formatted_context_blocks = []

        for r in results:
            citations.append({
                "source_id": r.chunk.source_id,
                "source_type": r.chunk.source_type,
                "title": r.chunk.title,
                "category": r.chunk.category,
                "score": round(r.score, 4)
            })
            formatted_context_blocks.append(
                f"[{r.chunk.source_id}: {r.chunk.title}]\n{r.chunk.text}"
            )

        method = getattr(self.retriever.embedding_provider, "embedding_method", "unknown")

        return {
            "query": question,
            "has_knowledge": len(results) > 0,
            "results_count": len(results),
            "embedding_method": method,
            "citations": citations,
            "context_text": "\n\n".join(formatted_context_blocks),
            "retrieved_chunks": results
        }


# Singleton RAG pipeline instance
rag_pipeline = RAGPipeline()

"""SupportHub RAG Pipeline Package."""
from app.rag.loader import RAGLoader
from app.rag.document_processor import DocumentProcessor, Document
from app.rag.chunker import DocumentChunker, Chunk
from app.rag.embeddings import (
    BaseEmbeddingProvider,
    LocalVectorEmbeddingProvider,
    cosine_similarity,
    get_embedding_provider
)
from app.rag.retriever import Retriever, RetrievedChunk
from app.rag.pipeline import RAGPipeline, rag_pipeline

__all__ = [
    "RAGLoader",
    "DocumentProcessor",
    "Document",
    "DocumentChunker",
    "Chunk",
    "BaseEmbeddingProvider",
    "LocalVectorEmbeddingProvider",
    "cosine_similarity",
    "get_embedding_provider",
    "Retriever",
    "RetrievedChunk",
    "RAGPipeline",
    "rag_pipeline",
]

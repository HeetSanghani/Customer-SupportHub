"""RAG knowledge retrieval contracts with mandatory tenant scoping."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class RAGQueryRequest:
    """Request payload for RAG semantic search."""
    query: str
    tenant_id: str
    category_filter: Optional[str] = None  # e.g., 'policy', 'knowledge_article'
    top_k: int = 3
    min_score: float = 0.15
    metadata_filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGCitation:
    """Document citation provenance metadata."""
    source_id: str
    tenant_id: str
    title: str
    category: str
    chunk_index: int
    score: float
    snippet: str
    effective_date: Optional[str] = None


@dataclass
class RAGSearchResult:
    """Aggregated semantic search response."""
    query: str
    tenant_id: str
    citations: List[RAGCitation] = field(default_factory=list)
    has_relevant_results: bool = False

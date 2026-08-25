"""Document processing and metadata normalization for RAG."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from app.rag.loader import RAGLoader


@dataclass
class Document:
    """Normalized document representation for knowledge ingestion."""
    doc_id: str
    source_type: str             # "policy" | "knowledge_article"
    source_id: str               # "POL-001", "KB-001"
    title: str
    category: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class DocumentProcessor:
    """Normalizes raw policy and article JSON items into standardized Documents."""

    def __init__(self, loader: Optional[RAGLoader] = None):
        self.loader = loader or RAGLoader()

    def process_all_documents(self) -> List[Document]:
        """Process both policies and knowledge articles into Document instances."""
        documents: List[Document] = []
        
        # 1. Process Policies
        raw_policies = self.loader.load_raw_policies()
        for p in raw_policies:
            policy_id = p.get("policy_id", "")
            title = p.get("title", "")
            category = p.get("category", "")
            content = p.get("content", "")
            doc = Document(
                doc_id=f"doc_{policy_id}",
                source_type="policy",
                source_id=policy_id,
                title=title,
                category=category,
                content=content,
                metadata={
                    "version": p.get("version", "1.0"),
                    "status": p.get("status", "ACTIVE"),
                    "effective_date": p.get("effective_date", ""),
                    "company_id": p.get("company_id", "SHOPKART-001")
                }
            )
            documents.append(doc)

        # 2. Process Knowledge Articles
        raw_articles = self.loader.load_raw_knowledge_articles()
        for a in raw_articles:
            article_id = a.get("article_id", "")
            title = a.get("title", "")
            category = a.get("category", "")
            content = a.get("content", "")
            doc = Document(
                doc_id=f"doc_{article_id}",
                source_type="knowledge_article",
                source_id=article_id,
                title=title,
                category=category,
                content=content,
                metadata={
                    "keywords": a.get("keywords", []),
                    "status": a.get("status", "PUBLISHED"),
                    "created_at": a.get("created_at", ""),
                    "updated_at": a.get("updated_at", ""),
                    "company_id": a.get("company_id", "SHOPKART-001")
                }
            )
            documents.append(doc)

        return documents

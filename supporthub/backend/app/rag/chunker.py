"""Document Chunker for RAG pipeline."""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from app.rag.document_processor import Document
from app.ai.config import settings


@dataclass
class Chunk:
    """A granular, contextual piece of a Document for vector indexing."""
    chunk_id: str
    doc_id: str
    source_type: str
    source_id: str
    title: str
    category: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class DocumentChunker:
    """Splits documents into contextual chunks with metadata preservation."""

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.RAG_CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.RAG_CHUNK_OVERLAP

    def chunk_document(self, doc: Document) -> List[Chunk]:
        """Split a single Document into one or more Chunks."""
        chunks: List[Chunk] = []
        content = doc.content.strip()

        if len(content) <= self.chunk_size:
            chunk = Chunk(
                chunk_id=f"{doc.source_id}_chunk_0",
                doc_id=doc.doc_id,
                source_type=doc.source_type,
                source_id=doc.source_id,
                title=doc.title,
                category=doc.category,
                text=content,
                metadata={**doc.metadata, "chunk_index": 0}
            )
            return [chunk]

        # Paragraph / Window splitting
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        current_text = ""
        chunk_idx = 0

        for para in paragraphs:
            if current_text and (len(current_text) + len(para) + 2) > self.chunk_size:
                chunks.append(Chunk(
                    chunk_id=f"{doc.source_id}_chunk_{chunk_idx}",
                    doc_id=doc.doc_id,
                    source_type=doc.source_type,
                    source_id=doc.source_id,
                    title=doc.title,
                    category=doc.category,
                    text=current_text.strip(),
                    metadata={**doc.metadata, "chunk_index": chunk_idx}
                ))
                chunk_idx += 1
                # Preserve overlap by carrying trailing characters/words
                overlap_text = current_text[-self.chunk_overlap:] if len(current_text) > self.chunk_overlap else ""
                current_text = overlap_text + "\n\n" + para if overlap_text else para
            else:
                if current_text:
                    current_text += "\n\n" + para
                else:
                    current_text = para

        if current_text.strip():
            chunks.append(Chunk(
                chunk_id=f"{doc.source_id}_chunk_{chunk_idx}",
                doc_id=doc.doc_id,
                source_type=doc.source_type,
                source_id=doc.source_id,
                title=doc.title,
                category=doc.category,
                text=current_text.strip(),
                metadata={**doc.metadata, "chunk_index": chunk_idx}
            ))

        return chunks

    def chunk_all(self, documents: List[Document]) -> List[Chunk]:
        """Chunk a list of Documents."""
        all_chunks: List[Chunk] = []
        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks

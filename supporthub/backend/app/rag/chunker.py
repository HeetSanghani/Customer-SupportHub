"""Document Chunker for RAG pipeline."""
import re
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

    def _split_into_heading_sections(self, content: str) -> List[Dict[str, str]]:
        """Splits markdown content into sections based on heading boundaries (#, ##, ###)."""
        lines = content.splitlines(keepends=True)
        sections = []
        current_heading = ""
        current_lines = []

        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith("#") and re.match(r'^#{1,6}\s+', stripped):
                if current_lines:
                    sec_text = "".join(current_lines).strip()
                    if sec_text:
                        sections.append({"heading": current_heading, "text": sec_text})
                current_heading = line.strip()
                current_lines = [line]
            else:
                current_lines.append(line)

        if current_lines:
            sec_text = "".join(current_lines).strip()
            if sec_text:
                sections.append({"heading": current_heading, "text": sec_text})

        # Merge title-only top H1 sections into subsequent section if total length <= chunk_size
        merged = []
        i = 0
        while i < len(sections):
            sec = sections[i]
            lines = [l.strip() for l in sec["text"].splitlines() if l.strip()]
            if len(lines) == 1 and lines[0].startswith("#") and i + 1 < len(sections):
                next_sec = sections[i + 1]
                combined_text = sec["text"] + "\n\n" + next_sec["text"]
                if len(combined_text) <= self.chunk_size:
                    merged.append({"heading": next_sec["heading"], "text": combined_text})
                    i += 2
                    continue
            merged.append(sec)
            i += 1

        return merged

    def _sub_split_section_text(self, text: str, heading: str = "") -> List[str]:
        """Sub-splits long section text exceeding chunk_size using paragraph windowing."""
        if len(text) <= self.chunk_size:
            return [text]

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks = []
        current_text = ""

        for para in paragraphs:
            test_len = len(current_text) + len(para) + 2 if current_text else len(para)
            if current_text and test_len > self.chunk_size:
                chunks.append(current_text.strip())
                if heading and not para.startswith("#"):
                    current_text = f"{heading}\n\n{para}"
                else:
                    current_text = para
            else:
                if current_text:
                    current_text += "\n\n" + para
                else:
                    current_text = para

        if current_text.strip():
            chunks.append(current_text.strip())

        return chunks

    def chunk_document(self, doc: Document) -> List[Chunk]:
        """Split a single Document into one or more Chunks."""
        content = doc.content.strip()

        if len(content) <= self.chunk_size:
            return [
                Chunk(
                    chunk_id=f"{doc.source_id}_chunk_0",
                    doc_id=doc.doc_id,
                    source_type=doc.source_type,
                    source_id=doc.source_id,
                    title=doc.title,
                    category=doc.category,
                    text=content,
                    metadata={**doc.metadata, "chunk_index": 0}
                )
            ]

        sections = self._split_into_heading_sections(content)
        # If no markdown headings found in document, fall back to paragraph sub-splitting
        if len(sections) <= 1 and (not sections or not sections[0]["heading"]):
            raw_texts = self._sub_split_section_text(content)
        else:
            raw_texts = []
            for sec in sections:
                sec_text = sec["text"]
                if len(sec_text) <= self.chunk_size:
                    raw_texts.append(sec_text)
                else:
                    raw_texts.extend(self._sub_split_section_text(sec_text, heading=sec["heading"]))

        chunks = []
        for idx, t in enumerate(raw_texts):
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.source_id}_chunk_{idx}",
                    doc_id=doc.doc_id,
                    source_type=doc.source_type,
                    source_id=doc.source_id,
                    title=doc.title,
                    category=doc.category,
                    text=t,
                    metadata={**doc.metadata, "chunk_index": idx}
                )
            )

        return chunks

    def chunk_all(self, documents: List[Document]) -> List[Chunk]:
        """Chunk a list of Documents."""
        all_chunks: List[Chunk] = []
        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))
        return all_chunks

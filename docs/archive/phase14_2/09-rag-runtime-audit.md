# 09 — RAG Runtime Audit

## Engine Architecture
- Primary RAG: `app/rag/pipeline.py` & `app/rag/retriever.py` (Local TF-IDF/Cosine Similarity & Document Chunker).
- Secondary Async RAG: `app/services/ai/knowledge_rag.py` (Queries PostgreSQL `KbArticle` table with pgvector/ILIKE for dynamic admin KB articles).

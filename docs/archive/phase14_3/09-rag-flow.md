# 09 — RAG Flow

- **Canonical Documents**: `knowledge_base/policies/policies.json` (10 Policies), `knowledge_base/articles/knowledge_articles.json` (13 Articles).
- **Pipeline**: `app/rag/pipeline.py` & `app/rag/retriever.py` (Local Cosine Similarity).
- **Dynamic Articles**: `app/services/ai/knowledge_rag.py` (Pgvector on PostgreSQL `KbArticle`).

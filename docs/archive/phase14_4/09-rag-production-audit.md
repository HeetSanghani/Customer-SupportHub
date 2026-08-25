# 09 — RAG Production Audit

- **Canonical Documents**: `knowledge_base/policies/policies.json` (10 Policies) and `knowledge_base/articles/knowledge_articles.json` (13 Articles).
- **Loader**: `app/rag/loader.py` resolves from local `knowledge_base/` with `DataLoader` fallback.
- **Vector Store**: Local memory index for static policies + `pgvector` for dynamic `KbArticle` records in PostgreSQL.

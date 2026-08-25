# Phase 17 — 18. Knowledge Base & RAG Indexing Audit

## Vector Search Configuration
- **Vector DB**: `pgvector` extension in PostgreSQL.
- **Embedding Model**: Text embedding model creating 768-dimensional vectors.
- **Query Performance**: Indexing via HNSW cosine distance provides sub-15ms similarity lookup.

# 12 — Pgvector Audit

- Database: PostgreSQL (`supporthub`)
- Model: `KbArticle` with `embedding` column (`Vector(1536)` or `Vector(768)`).
- Status: Fully active for admin-created KB articles via `app/services/ai/knowledge_rag.py`.

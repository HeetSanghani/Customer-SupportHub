# 12 — Duplication Audit

## Duplicated Components & Recommendations

1. **AI Helper (`Customer-SupportHub/backend/app/ai.py` vs `supporthub-ai-architecture/ai/*`)**:
   - **Audit**: `app/ai.py` contains legacy Phase 6 RAG logic. `supporthub-ai-architecture/ai/` contains the active Phase 13+ production AI engine.
   - **Active**: `supporthub-ai-architecture/ai/*`.
   - **Recommendation**: Archive `app/ai.py` during consolidation.

2. **Policy Documents (`supporthub-ai-architecture/rag/documents/policies/` vs dataset `policies.json`)**:
   - **Audit**: Markdown files in `supporthub-ai-architecture` are used for RAG chunking. `policies.json` in data generator was the source for Markdown extraction.
   - **Canonical**: Markdown policy files in `supporthub-ai-architecture/rag/documents/policies/`.

3. **Data Access Models**:
   - **Audit**: SQLModel classes in `Customer-SupportHub/app/models` manage PostgreSQL application data. PyMySQL data access classes in `supporthub-ai-architecture/data_access` manage MySQL business data.
   - **Conclusion**: NOT a duplication; both serve distinct databases.

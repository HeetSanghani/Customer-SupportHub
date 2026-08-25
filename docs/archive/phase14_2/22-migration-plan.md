# 22 — Migration Plan

1. Create `knowledge_base/policies/` and `knowledge_base/articles/` in `Customer-SupportHub`.
2. Copy policy JSON files and knowledge articles into `knowledge_base/`.
3. Update `app/rag/loader.py` to default to `knowledge_base/` path.
4. Verify 373/373 test suite pass rate.

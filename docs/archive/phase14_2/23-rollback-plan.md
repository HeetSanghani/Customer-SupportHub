# 23 — Rollback Plan

If any test fails after Stage B copy:
1. Revert `app/rag/loader.py` path default.
2. Remove created `knowledge_base/` directory.
3. Re-run `pytest tests` to restore baseline.

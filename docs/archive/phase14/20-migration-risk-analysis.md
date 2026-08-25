# 20 — Migration Risk Analysis

## Risk Assessment Matrix

| Proposed Move | Risk Level | Potential Regression | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Consolidate AI Engine to Backend** | **MEDIUM** | Broken import paths (`sys.path`) | Update imports to `app.ai.*` and run 373-test suite. |
| **Consolidate RAG & Documents** | **LOW** | Vector store path mismatch | Maintain relative path to policy documents in `app/rag/documents`. |
| **Consolidate Test Suite** | **LOW** | Test path resolution issues | Move tests to `backend/tests/ai/` and update PYTHONPATH. |
| **Keep Data Generator Separate**| **NONE** | No runtime impact | Retain `supporthub-data-generator` as external seed utility. |

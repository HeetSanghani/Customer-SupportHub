# 19 — Keep / Move / Reference Matrix

| Component | Target Action | Target Location | Rationale |
| :--- | :--- | :--- | :--- |
| `Customer-SupportHub/frontend` | **KEEP** | `Customer-SupportHub` | Production UI SPA |
| `Customer-SupportHub/backend` | **KEEP** | `Customer-SupportHub` | Production API server |
| `supporthub-ai-architecture/ai` | **MOVE LATER (14.1)** | `Customer-SupportHub/.../app/ai` | Consolidate runtime AI |
| `supporthub-ai-architecture/data_access`| **MOVE LATER (14.1)**| `Customer-SupportHub/.../app/data_access` | Consolidate MySQL repo |
| `supporthub-ai-architecture/rag` | **MOVE LATER (14.2)** | `Customer-SupportHub/.../app/rag` | Consolidate RAG engine |
| `supporthub-data-generator` | **KEEP SEPARATE** | Standalone Repo | Offline seed ETL tool only |
| Legacy `app/ai.py` | **ARCHIVE** | `Customer-SupportHub/.../app/legacy` | Replaced by AIOrchestrator |

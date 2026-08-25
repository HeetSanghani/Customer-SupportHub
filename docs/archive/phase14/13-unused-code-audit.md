# 13 — Unused & Dead Code Audit

## Code Classification Table

| File / Component | Classification | Evidence | Action for Consolidation |
| :--- | :--- | :--- | :--- |
| `Customer-SupportHub/supporthub/backend/app/ai.py` | **LEGACY / UNUSED** | Replaced by `LiveChatAIAdapter` & `AIOrchestrator`. | Archive / Remove |
| `Customer-SupportHub/scripts/tests_step3*.py` | **LEGACY TEST** | Replaced by `tests/phase13/` test suite. | Retain in scripts/ |
| `supporthub-ai-architecture/main.py` | **DEMO / ENTRY** | CLI test script for standalone testing. | Retain for standalone CLI test |
| `supporthub-data-generator/output/*.json` | **SEED DATA** | Imported into MySQL during migration. | Retain in data generator |

# 19 — Cleanup Execution Plan (Post-Audit Action Plan)

## Executive Summary
This document outlines the step-by-step phased execution plan for performing the repository cleanup, consolidation, and refactoring upon explicit user instruction.

> [!IMPORTANT]
> **Execution Status**: This execution plan will be carried out ONLY when the user explicitly issues the command to begin cleanup execution.

---

## Phased Execution Roadmap

### Phase 1: Unused File & Artifact Removal
1. Delete zero-byte backend files (`AIOrchestrator`, `AIRouter`, `Client`, `Execution`, `LiveChatAIAdapter`, `Ownership`, `support_hub.db`, `supporthub.db` in `supporthub/backend/`).
2. Delete root legacy frontend/script files (`app.js`, `index.html`, `vercel.json`, `fix_redirect.py`, `test.md`).
3. Delete shadowed `supporthub/backend/app/ai.py`.
4. Delete obsolete MySQL migration script `supporthub/backend/app/scripts/migrate_json_to_mysql.py`.
5. Run test suite (`uv run pytest`) to confirm zero breakage.

### Phase 2: AI & RAG Pipeline Consolidation
1. Update social webhook handlers (`app/services/instagram/webhook.py`, `facebook/webhook.py`, `whatsapp/webhook.py`, `webhooks/email.py`) to instantiate `app.ai.orchestrator.AIOrchestrator`.
2. Verify that `app/ai/orchestrator.py` handles all background webhook response synthesis requirements.
3. Flag `app/services/ai/` (`orchestrator.py`, `context_builder.py`, `prompt_builder.py`, `model_adapter.py`, `response_parser.py`, `knowledge_rag.py`) for archival/removal.
4. Run test suite to verify all 559 pytest items.

### Phase 3: Repository & Service Naming Refactoring
1. Rename `app/data_access/mysql_repository.py` -> `app/data_access/postgres_business_repository.py`.
2. Update imports across `customer_service.py`, `order_service.py`, `refund_service.py`, `shipment_service.py`, `return_service.py`, `seller_service.py`, `product_service.py`, `payment_service.py`.
3. Rename `mysql_db` -> `postgres_business_db` in `app/data_access/db.py`.
4. Run full test suite to verify 100% pass rate.

### Phase 4: Git Hygiene & Documentation Archival
1. Move historical phase docs to `docs/archive/`.
2. Clean up untracked temporary files and update `.gitignore`.
3. Final verification run of pytest suite.
4. Commit pristine repository state to Git.

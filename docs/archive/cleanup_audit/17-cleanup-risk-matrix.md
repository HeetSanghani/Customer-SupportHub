# 17 — Cleanup Risk Assessment Matrix

## Executive Summary
This document provides a risk assessment for every proposed cleanup operation, establishing safety protocols and regression testing requirements prior to execution.

---

## 1. Risk Evaluation Matrix

| Proposed Cleanup Action | Risk Level | Potential System Impact | Mitigation Strategy | Verification Step |
| :--- | :--- | :--- | :--- | :--- |
| **Delete Root Legacy Files** (`app.js`, `index.html`, `vercel.json`) | **LOW** | None. No runtime components reference root HTML/JS files. | Verify frontend build (`npm run build`) before deletion. | Run frontend dev server & E2E smoke test. |
| **Delete Zero-Byte Backend Artifacts** | **ZERO** | None. Files contain 0 bytes. | Verify file byte size is 0. | Run backend pytest suite post-deletion. |
| **Delete Shadowed `app/ai.py`** | **LOW** | Potential breakage if hidden import specifically targeted `app.ai`. | Verified via grep that package `app/ai/` handles all imports (`generate_embedding`). | Run full backend test suite (`uv run pytest`). |
| **Consolidate Webhook AI Orchestrators** | **MEDIUM** | Background webhooks (Instagram/WhatsApp) might experience interface mismatches. | Ensure `app.ai.orchestrator.AIOrchestrator` satisfies all webhook response attributes (`AIResponse`). | Run webhook unit & integration test suites (`test_instagram_webhook.py`). |
| **Deprecate `app/services/ai/knowledge_rag.py`** | **LOW** | Webhook AI callers relying on old RAG fallback. | Ensure `app/rag/pipeline.py` is invoked across all RAG queries. | Run RAG unit tests (`test_rag.py`). |
| **Refactor `mysql_repository.py` Filename** | **MEDIUM** | Breaking import references across routers/services. | Perform atomic multi-file rename using AST/Grep replacement. | Execute regression suite (559 pytest cases). |

---

## 2. Safety Guidelines for Execution Phase

1. **Pre-Execution Git Snapshot**: Create a clean git commit or branch before initiating any file removals.
2. **Atomic Steps**: Execute cleanup actions in isolated, verifiable steps (e.g., zero-byte deletion -> test -> root file cleanup -> test -> AI consolidation -> test).
3. **Automated Regression Verification**: Re-run the full 559-item test suite after each cleanup step to verify zero regressions.

# 14 — Test Ownership Audit

## Test Suite Inventory

| Test Suite Path | Repository | Count | Scope & Ownership | Status |
| :--- | :--- | :--- | :--- | :--- |
| `supporthub-ai-architecture/tests/` | `supporthub-ai-architecture` | 143 | AI Router, Intent, Context, ToolRegistry, Security, RAG, MySQL Adapter | **143 / 143 PASS** |
| `Customer-SupportHub/supporthub/backend/tests/` | `Customer-SupportHub` | 230 | Auth, Tickets, WebSocket, Quick Replies, Phase 13 MySQL & Security | **230 / 230 PASS** |
| **Combined Baseline** | **Both** | **373** | **Full System E2E Coverage** | **373 / 373 PASS** |

## Recommendation
Consolidate `supporthub-ai-architecture/tests/` into `Customer-SupportHub/supporthub/backend/tests/ai/` during Phase 14 consolidation so `pytest` runs the full 373-test suite natively from a single root.

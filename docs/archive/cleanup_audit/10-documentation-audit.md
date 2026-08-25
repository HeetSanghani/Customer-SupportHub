# 10 — Documentation Audit & Contradiction Matrix

## Executive Summary
This document provides an audit of all documentation across `docs/`, `supporthub/docs/`, `output/`, and root Markdown files, identifying outdated phase reports, contradictions, and archival candidates.

---

## 1. Documentation Inventory

```
docs/
├── phase11/                 [HISTORICAL DOCUMENTATION — 6 Files]
│   └── Early Live Chat & AI integration specs
├── phase13/                 [HISTORICAL DOCUMENTATION — 80+ Files]
│   └── MySQL migration, business data access, and context remediation reports
├── phase14/                 [HISTORICAL DOCUMENTATION — 23 Files]
│   └── PostgreSQL consolidation & target architecture docs
├── phase14_4_3/             [HISTORICAL DOCUMENTATION — 20 Files]
│   └── Load testing, Redis performance, capacity benchmarking reports
supporthub/docs/             [HISTORICAL DOCUMENTATION — Phase reports]
output/                      [HISTORICAL REPORTS — 40+ JSON/MD Inspection Files]
README.md                    [CURRENT DOCUMENTATION — Root Guide]
SETUP_NEW_MACHINE.md        [CURRENT DOCUMENTATION — Onboarding Guide]
```

---

## 2. Contradiction Evaluation Matrix

| Topic | Document Reference A | Document Reference B | Resolution / Single Source of Truth |
| :--- | :--- | :--- | :--- |
| **Business DB Engine** | `docs/phase13/05-mysql-schema-design.md` states "ShopKart business data resides in MySQL". | `docs/phase14/10-database-architecture.md` states "Unified PostgreSQL database". | **PostgreSQL** is the canonical database. `phase13` docs reflect historical phase status. |
| **RAG Retrieval** | `output/phase11_5_report.md` describes file keyword search. | `docs/phase14/09-rag-document-audit.md` describes 1536-dim pgvector cosine similarity. | **pgvector** in PostgreSQL is canonical. |
| **AI Orchestrator** | `docs/phase11/03-ai-integration-boundary.md` references `app/services/ai/orchestrator.py`. | `docs/phase14/03-ai-architecture-audit.md` references `app/ai/orchestrator.py` with LangGraph. | **`app/ai/orchestrator.py`** is canonical. |

---

## 3. Documentation Audit Verdict

* **Active Docs**: Root `README.md` and `SETUP_NEW_MACHINE.md` accurately depict current environment requirements.
* **Phase Archives**: Historical documentation in `docs/phase11`, `docs/phase13`, `docs/phase14`, and `docs/phase14_4_3` represents valuable architectural audit history and should be retained under `docs/archive/` or kept read-only as phase snapshots.

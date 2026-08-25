# 01 — Repository Inventory & Directory Classification

## Executive Summary
This document provides a complete, itemized inventory of all top-level and nested directories within the `Customer-SupportHub` workspace. Each directory is classified according to the cleanup classification system based on actual runtime, test, and development requirements.

---

## Workspace Root Layout

The active workspace root is `/home/python/Projects/Customer-SupportHub`.

```
Customer-SupportHub/
├── README.md                                 [KEEP — DOCUMENTATION]
├── SETUP_NEW_MACHINE.md                      [KEEP — DOCUMENTATION]
├── SupportHub_Build_Plan_Python_FastAPI.docx [HISTORICAL DOCUMENTATION]
├── app.js                                    [REMOVE CANDIDATE]
├── data/                                     [HISTORICAL DATASET]
├── db_explorer.py                            [KEEP — DEVELOPMENT]
├── docs/                                     [KEEP — DOCUMENTATION]
│   ├── phase11/                              [HISTORICAL DOCUMENTATION]
│   ├── phase13/                              [HISTORICAL DOCUMENTATION]
│   ├── phase14/                              [HISTORICAL DOCUMENTATION]
│   └── phase14_4_3/                          [HISTORICAL DOCUMENTATION]
├── fix_redirect.py                           [REMOVE CANDIDATE]
├── index.html                                [REMOVE CANDIDATE]
├── inspect_db.py                             [KEEP — DEVELOPMENT]
├── knowledge_base/                           [KEEP — RUNTIME]
│   ├── articles/                             [KEEP — RUNTIME]
│   └── policies/                             [KEEP — RUNTIME]
├── output/                                   [KEEP — DOCUMENTATION]
├── scripts/                                  [KEEP — DEVELOPMENT]
├── supporthub/                               [KEEP — CRITICAL RUNTIME]
│   ├── backend/                              [KEEP — CRITICAL RUNTIME]
│   ├── frontend/                             [KEEP — CRITICAL RUNTIME]
│   ├── docs/                                 [KEEP — DOCUMENTATION]
│   ├── docker-compose.yml                    [KEEP — CRITICAL RUNTIME]
│   ├── nginx.conf                            [KEEP — CRITICAL RUNTIME]
│   └── output/                               [KEEP — DOCUMENTATION]
├── supporthub_dump.sql                       [ARCHIVE]
├── test.md                                   [REMOVE CANDIDATE]
├── updates.md                                [HISTORICAL DOCUMENTATION]
└── vercel.json                               [REMOVE CANDIDATE]
```

---

## Detailed Component Classification

### 1. Root Directory Artifacts

| Path | Classification | Runtime / Build Role | Evidence & Notes |
| :--- | :--- | :--- | :--- |
| `README.md` | `KEEP — DOCUMENTATION` | Root Project Guide | Main project documentation. |
| `SETUP_NEW_MACHINE.md` | `KEEP — DEVELOPMENT` | Dev Onboarding | Setup instructions for new dev environments. |
| `SupportHub_Build_Plan_Python_FastAPI.docx` | `ARCHIVE` | Historical Spec | Early planning document in binary docx format. |
| `app.js` | `REMOVE CANDIDATE` | Legacy Frontend Prototype | Single JS file referenced only by root `index.html`. Not used by Vite frontend. |
| `index.html` | `REMOVE CANDIDATE` | Legacy Frontend Prototype | Standalone HTML page. Not used by Vite frontend in `supporthub/frontend/index.html`. |
| `data/` | `ARCHIVE` | Legacy JSON Fixtures | Early mock data directory. Active business data now in PostgreSQL. |
| `db_explorer.py` | `KEEP — DEVELOPMENT` | Database Inspection UI | Standalone FastAPI browser UI for inspecting PostgreSQL tables (running on port 8090). |
| `inspect_db.py` | `KEEP — DEVELOPMENT` | CLI DB Inspector | Read-only Python script for quick DB table queries. |
| `fix_redirect.py` | `REMOVE CANDIDATE` | One-off Script | Regex string replacement script used during Phase 13 frontend patch. |
| `knowledge_base/` | `KEEP — RUNTIME` | RAG Knowledge Source | Contains canonical `policies/policies.json` and `articles/knowledge_articles.json`. |
| `scripts/` | `KEEP — DEVELOPMENT` | Dev Automation | Utility scripts for local dev operations. |
| `supporthub_dump.sql` | `ARCHIVE` | Raw SQL Snapshot | Historical SQL dump file. |
| `test.md` | `REMOVE CANDIDATE` | Temporary Scratch Pad | Scratch notes file. |
| `updates.md` | `HISTORICAL DOCUMENTATION` | Dev Changelog | Log of early feature updates. |
| `vercel.json` | `REMOVE CANDIDATE` | Obsolete Deployment | Early Vercel config. Production deployment uses Docker/Nginx. |

---

### 2. Primary Application (`supporthub/`)

#### Backend (`supporthub/backend/`)
* **`app/`**: Active FastAPI backend (`KEEP — CRITICAL`).
  * `app/ai/`: Active modular AI package (`KEEP — CRITICAL`).
  * `app/ai/graph/`: LangGraph node execution engine (`KEEP — CRITICAL`).
  * `app/rag/`: Vector retriever & embedding pipeline (`KEEP — CRITICAL`).
  * `app/models/`: SQLModel data models for PostgreSQL (`KEEP — CRITICAL`).
  * `app/routers/`: REST endpoints & WebSocket handlers (`KEEP — CRITICAL`).
  * `app/services/ai/`: Legacy AI & adapter layer (`DUPLICATE / LEGACY CANDIDATE`).
  * `app/ai.py`: Shadowed legacy script (`OBSOLETE / REMOVE CANDIDATE`).
* **`tests/`**: Active pytest suite containing 559 test items (`KEEP — TEST`).
* **Zero-byte files**: `AIOrchestrator`, `AIRouter`, `Client`, `Execution`, `LiveChatAIAdapter`, `Ownership`, `support_hub.db`, `supporthub.db` (`REMOVE CANDIDATE`).

#### Frontend (`supporthub/frontend/`)
* **`src/`**: Active React 18 / Vite application (`KEEP — CRITICAL`).
* **`index.html`**: Canonical Vite entrypoint (`KEEP — CRITICAL`).
* **`package.json` / `vite.config.js`**: Frontend build configuration (`KEEP — CRITICAL`).

---

## Audit Verification Verdict

The repository inventory confirms that the active core application is concentrated inside `supporthub/`. Root level legacy scripts (`app.js`, `index.html`, `fix_redirect.py`, `vercel.json`) and zero-byte backend files represent clean candidates for removal/archival.

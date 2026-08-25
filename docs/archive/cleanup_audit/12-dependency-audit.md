# 12 — Dependency Audit & Package Inventory

## Executive Summary
This report analyzes Python dependencies (`pyproject.toml`, `uv.lock`) and Node.js dependencies (`package.json`, `package-lock.json`), evaluating active usage, framework versions, and unused or redundant packages.

---

## 1. Python Backend Dependencies (`supporthub/backend/pyproject.toml`)

### Core Web & ORM Frameworks
* `fastapi>=0.110.0`: FastAPI web framework (`KEEP — CRITICAL`).
* `uvicorn[standard]>=0.28.0`: ASGI server (`KEEP — CRITICAL`).
* `sqlmodel>=0.0.16`: SQLModel ORM combining Pydantic & SQLAlchemy (`KEEP — CRITICAL`).
* `asyncpg>=0.29.0`: High-performance PostgreSQL async driver (`KEEP — CRITICAL`).
* `psycopg2-binary>=2.9.9`: Synchronous PostgreSQL driver used by Celery tasks (`KEEP — CRITICAL`).
* `pgvector>=0.2.5`: Vector extension integration for SQLModel (`KEEP — CRITICAL`).
* `redis>=5.0.0` & `celery>=5.3.6`: Background task queue and caching (`KEEP — CRITICAL`).

### AI & RAG Ecosystem
* `langchain>=0.3.0`: LangChain framework (`KEEP — CRITICAL`).
* `langchain-core>=0.3.0`: LangChain abstractions (`KEEP — CRITICAL`).
* `langgraph>=0.2.0`: Graph orchestration framework (`KEEP — CRITICAL`).
* `google-generativeai>=0.5.0`: Legacy Gemini SDK (`KEEP — DEPRECATED WARNING`).
* `openai>=1.14.0`: OpenAI API client (`KEEP — RUNTIME`).
* `pydantic>=2.6.0`: Data validation & settings management (`KEEP — CRITICAL`).

### Unused / Legacy Dependencies Discovered
* `pymysql`: MySQL driver (`REMOVE CANDIDATE`). Runtime connects exclusively to PostgreSQL via `asyncpg`.

---

## 2. Frontend Node.js Dependencies (`supporthub/frontend/package.json`)

* `react` & `react-dom` (`^18.2.0`): React 18 web UI (`KEEP — CRITICAL`).
* `vite` (`^5.2.0`): Vite build tool (`KEEP — CRITICAL`).
* `@tanstack/react-query` (`^5.28.0`): Server state management & cache (`KEEP — CRITICAL`).
* `lucide-react` (`^0.359.0`): UI icon library (`KEEP — CRITICAL`).
* `axios` (`^1.6.8`): HTTP client (`KEEP — CRITICAL`).
* `socket.io-client` (`^4.7.5`): Real-time WebSocket connection (`KEEP — CRITICAL`).
* `tailwindcss` (`^3.4.1`): Utility CSS framework (`KEEP — CRITICAL`).

---

## 3. Dependency Audit Verdict
* **Backend**: Clean dependency definition managed via `uv`. `pymysql` is the only obsolete package.
* **Frontend**: Highly efficient dependency set without bloated unneeded libraries.

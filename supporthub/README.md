# SupportHub — AI Omnichannel Customer Support Platform

> Full-stack production application: FastAPI backend + React frontend + PostgreSQL + Redis + Celery

## Quick Start (Local Dev)

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.12+ with `uv`

> **Ports used by SupportHub** (chosen to avoid conflicts with system services):
> - Postgres → `5433` (system may use 5432)
> - Redis → `6380` (system Redis uses 6379)
> - FastAPI backend → `8001` (avoids other projects on 8000)
> - React frontend → `5173`

---

### Terminal 1 — Start Database & Redis
```bash
cd "/home/heet/Documents/Kumar Sir demo [Customer Support]/demo/ai powered customer /supporthub"
docker compose up -d
```

### Terminal 2 — Start Backend (FastAPI)
```bash
cd "/home/heet/Documents/Kumar Sir demo [Customer Support]/demo/ai powered customer /supporthub/backend"
cp .env.example .env          # First time only — fill in your API keys
uv run uvicorn app.main:app --reload --port 8001
```

> API docs: http://localhost:8001/api/docs

### Terminal 3 — Start Frontend (React)
```bash
cd "/home/heet/Documents/Kumar Sir demo [Customer Support]/demo/ai powered customer /supporthub/frontend"
npm run dev
```

> App: http://localhost:5173

### Terminal 4 — Celery Worker (background jobs, optional for now)
```bash
cd "/home/heet/Documents/Kumar Sir demo [Customer Support]/demo/ai powered customer /supporthub/backend"
uv run celery -A app.tasks.celery_app worker --loglevel=info
```

---

## Project Structure

```
supporthub/
├── backend/         FastAPI + SQLModel + Celery
├── frontend/        React + Vite + TypeScript + Tailwind
├── docker-compose.yml  PostgreSQL 16 (pgvector) + Redis 7
└── .github/workflows/  CI pipelines
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + TypeScript + Tailwind CSS |
| State | Zustand + TanStack Query |
| Backend | FastAPI (Python 3.12) |
| ORM | SQLModel + Alembic |
| Database | PostgreSQL 16 + pgvector |
| Cache/Queue | Redis 7 + Celery 5 |
| AI | Claude API (Anthropic) |
| Auth | JWT (python-jose) + bcrypt |
| Real-time | FastAPI native WebSockets |
| Storage | Supabase Storage |
| Email | Postmark |
| Monitoring | Sentry |

## Phase Progress

- [x] Phase 0 — Project setup & foundations ✅
- [x] Phase 1 — Auth, DB schema & RBAC ✅
- [x] Phase 2 — Tickets CRUD + Unified Inbox ✅
- [x] Phase 3 — Real-time WebSocket chat ✅
- [x] Phase 4 — Knowledge Base ✅
- [x] Phase 5 — AI Chatbot + RAG ✅
- [ ] Phase 6 — AI Agent Tools
- [ ] Phase 7 — Quick Replies + CSAT
- [ ] Phase 8 — User Management
- [ ] Phase 9 — SLA Engine + Notifications
- [ ] Phase 10 — Analytics Dashboards
- [ ] Phase 11 — Reports & Export
- [ ] Phase 12 — Workflow Automation
- [ ] Phase 13 — WhatsApp / Instagram / Facebook
- [ ] Phase 14 — AI Settings UI
- [ ] Phase 15 — System Settings & Security
- [ ] Phase 16 — Hardening & Launch

## API Docs
Available at `/api/docs` (Swagger UI) and `/api/redoc` when the backend is running.

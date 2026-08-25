# Phase 16 — Developer Onboarding & Architecture Learning Guide

## 1. Welcome to Customer-SupportHub

Customer-SupportHub is built with modern, maintainable design patterns. This guide helps new developers understand the project structure and local workflows.

---

## 2. Key Directories

- `backend/app/main.py`: FastAPI entrypoint and router registration.
- `backend/app/models/__init__.py`: Unified SQLModel database schemas.
- `backend/app/routers/`: Endpoint definitions for Auth, Orders, Tickets, Admin, CSAT, Automations.
- `backend/app/services/ai/`: AI router, orchestrator, live chat adapter, RAG knowledge base.
- `frontend/src/App.jsx`: React Router page routing & RoleRouter access control.
- `frontend/src/store/authStore.js`: Zustand authentication state persistence.

---

## 3. Running Local Environment

1. **Start Backend**:
   ```bash
   cd backend
   .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev -- --host 0.0.0.0 --port 5173
   ```

3. **Run Test Suite**:
   ```bash
   cd backend
   .venv/bin/pytest tests/ -v
   ```

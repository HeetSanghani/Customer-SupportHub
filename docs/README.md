# Customer-SupportHub Documentation Hub

Welcome to the canonical documentation hub for **Customer-SupportHub**, an enterprise-grade AI customer support platform powered by FastAPI, PostgreSQL 16, LangGraph, pgvector RAG, and React/Vite.

---

## Authoritative Architecture Overview

| Subsystem | Canonical Source Path | Engine / Framework | Key References |
| :--- | :--- | :--- | :--- |
| **Database Source of Truth** | `supporthub/backend/app/data_access/` | **PostgreSQL 16** (`supporthub` DB) | `postgres_business_repository.py`, `db.py` |
| **AI Orchestration Engine** | `supporthub/backend/app/ai/` | **LangGraph StateGraph** & `AIOrchestrator` | `orchestrator.py`, `router.py`, `graph/` |
| **LangGraph Graph Pipeline** | `supporthub/backend/app/ai/graph/` | **LangGraph 0.2+** | `support_graph.py`, `state.py`, `nodes.py` |
| **RAG Pipeline Engine** | `supporthub/backend/app/rag/` | **pgvector** Cosine Similarity & Fallback | `pipeline.py`, `retriever.py`, `vector_store.py` |
| **Knowledge Base Articles** | `knowledge_base/` | Markdown documents | Policy articles, shipping rules, return policy |
| **Authentication & AuthZ** | `supporthub/backend/app/routers/auth.py` | JWT + bcrypt + PostgreSQL `users` | `auth.py`, `models/user.py` |
| **Customer Security & Anti-IDOR**| `supporthub/backend/app/core/security.py` | Server-Side Authenticated Identity | `TenantSecurityGuard`, `postgres_business_repository.py` |
| **Human Escalation Workflow** | `supporthub/backend/app/routers/tickets.py` | WebSocket + Agent Queue + CSAT | `chat.py`, `tickets.py` |
| **Frontend Application** | `supporthub/frontend/` | React 18 / Vite / TailwindCSS | `CustomerDashboard.jsx`, `CustomerLiveChat.jsx` |

---

## Active Documentation Categories

- 📐 **[Architecture Overview](architecture/system-architecture.md)** — Core design principles, data flow, component boundaries.
- 🤖 **[AI & Orchestration](ai/ai-overview.md)** — AI routing, LangGraph graph state, multi-intent decomposition, tool execution.
- 🔍 **[RAG Pipeline](rag/rag-overview.md)** — Knowledge base ingestion, pgvector embeddings, retrieval, grounding.
- 🗄️ **[Database Architecture](database/schema-overview.md)** — Relational schemas, users, customers, orders, tickets.
- 🔌 **[API Documentation](api/authentication.md)** — REST endpoints, authentication, WebSockets, payloads.
- 🛡️ **[Security Architecture](security/authentication-security.md)** — Anti-IDOR guards, tenant isolation, prompt injection defense.
- 💻 **[Development Guide](development/setup.md)** — Quickstart, environment setup, testing, debugging.
- 🚀 **[Deployment Guide](deployment/docker.md)** — Docker Compose, Nginx, production environment secrets.
- 📊 **[Documentation Audit & Metrics](documentation_audit/01-documentation-inventory.md)** — Phase A.3 audit report suite.
- 📦 **[Historical Archive](archive/)** — Phase 11 through Phase A.2 historical phase reports and audit evidence.

---

## Important Notice: Single Source of Truth
Historical phase documentation located in `docs/archive/` reflects earlier development stages (e.g., prototype MySQL implementations, initial AI scripts). **For all active development, maintenance, and deployment, consult the canonical files under `docs/` listed above.**

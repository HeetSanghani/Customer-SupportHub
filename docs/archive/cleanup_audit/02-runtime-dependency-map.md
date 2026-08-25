# 02 — Runtime Dependency Map & Execution Traces

## Executive Summary
This report documents the exact end-to-end execution flow and component call graphs for the active SupportHub application across Live Chat WebSocket interactions, REST API endpoints, background webhooks, and AI response generation.

---

## 1. Primary Execution Flow: Live Chat (WebSocket)

The primary customer interactive channel is Live Chat over WebSocket. The runtime call chain was traced directly from source code:

```
Browser / React Frontend (CustomerLiveChat.jsx)
  ↓ [WebSocket Connection via Socket.io / Native WS]
FastAPI Router (supporthub/backend/app/routers/ws/chat.py)
  ↓ [JWT Authentication & Session Context Lookup]
LiveChatAIAdapter (supporthub/backend/app/services/ai/live_chat_adapter.py)
  ↓ [Human Agent Check — Suppress AI if agent assigned]
AIOrchestrator (supporthub/backend/app/ai/orchestrator.py)
  ↓ [Context Resolution via ContextManager (app/ai/context.py)]
LangGraph Execution Graph (app/ai/graph/build.py -> compiled_graph)
  ↓
  ├─► Router Node (AIRouter in app/ai/router.py)
  ├─► Intent Classifier (IntentClassifier in app/ai/intent.py)
  ├─► Tool Execution (ToolRegistry & CustomerService in app/ai/tools.py)
  ├─► RAG Retrieval (RAGPipeline in app/rag/pipeline.py -> pgvector)
  └─► Security & Escalation Gating (SecurityValidator & EscalationEvaluator)
  ↓
Response Synthesizer (app/ai/response.py -> ResponseSynthesizer)
  ↓ [Persist Message into PostgreSQL 'messages' table]
PostgreSQL 16 (pgvector / asyncpg)
  ↓
WebSocket Broadcast (chat.py) -> Frontend UI Update
```

---

## 2. Background Channel Flow: Social Webhooks (Instagram / WhatsApp / Email)

Background webhook processing follows a distinct parallel path:

```
Meta Webhook Server / Email Inbound
  ↓ [HTTP POST Webhook Endpoint]
Webhook Router (app/routers/webhooks/ or app/routers/instagram.py)
  ↓ [HMAC / Signature Verification & Event Deduplication]
Webhook Handler Service (app/services/instagram/webhook.py)
  ↓ [Database Session Setup]
Legacy AIOrchestrator (app/services/ai/orchestrator.py)
  ↓ [ContextBuilder -> PromptBuilder -> ModelAdapter]
LLM Provider API Call (Google Gemini / OpenAI / Mock)
  ↓ [Store Message & Update Ticket]
PostgreSQL 16 Database
```

> [!WARNING]
> **Architecture Divergence**: Background webhooks currently invoke `app/services/ai/orchestrator.py`, whereas Live Chat invokes `app/ai/orchestrator.py` (which uses LangGraph). Standardizing all channels onto `app/ai/orchestrator.py` is a key recommendation before the next phase.

---

## 3. REST API Execution Flow (Customer / Agent / Admin Portals)

```
React Frontend (src/api/auth.js, tickets.js, orders.js)
  ↓ [HTTP Axios with Bearer JWT Token]
FastAPI Router (app/routers/auth.py, tickets.py, orders.py)
  ↓ [OAuth2PasswordBearer / get_current_user Dependency]
Service Layer (CustomerService, OrderService, TicketService)
  ↓ [Database Query via SQLModel / asyncpg]
PostgreSQL 16 Database (supporthub)
  ↓ [JSON Serialization]
HTTP 200 OK Response -> Frontend State Update
```

---

## 4. Component Interdependency Matrix

| Layer | Canonical Module | Depends On | Used By |
| :--- | :--- | :--- | :--- |
| **FastAPI Core** | `app.main:app` | `app.routers.*`, `app.database` | Uvicorn / Nginx |
| **Authentication** | `app.routers.auth` | `app.models.User`, `jose` JWT | All REST & WS routers |
| **Live Chat AI** | `app.services.ai.live_chat_adapter` | `app.ai.orchestrator` | `app.routers.ws.chat` |
| **Modular AI** | `app.ai.orchestrator` | `app.ai.graph.build`, `app.rag` | `LiveChatAIAdapter` |
| **LangGraph Nodes**| `app.ai.graph.nodes` | `app.ai.router`, `app.rag` | `app.ai.graph.build` |
| **RAG Retrieval** | `app.rag.pipeline` | `app.rag.embeddings`, `pgvector` | `app.ai.orchestrator`, `nodes.py` |
| **Business Data** | `app.data_access.mysql_repository` | `app.data_access.db`, `asyncpg` | `CustomerService`, `OrderService` |
| **Database Model** | `app.models` | `SQLModel`, `sqlalchemy` | All services & routers |

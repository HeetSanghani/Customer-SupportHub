# System Architecture Overview

## Overview
**Customer-SupportHub** is a modern, enterprise-grade AI customer support platform designed for omnichannel communication (Web Live Chat, Email, WhatsApp, Instagram, Facebook). The architecture integrates deterministic business data access with LLM-powered conversational routing, pgvector RAG, and real-time human agent escalation.

```
                   ┌─────────────────────────────────────────┐
                   │             React/Vite UI               │
                   │        (Customer / Agent / Admin)       │
                   └────────────────────┬────────────────────┘
                                        │ REST / WebSockets
                                        ▼
                   ┌─────────────────────────────────────────┐
                   │            FastAPI Backend              │
                   │        (App Engine & Routers)           │
                   └───────┬─────────────────┬───────────────┘
                           │                 │
             ┌─────────────▼──────┐   ┌──────▼────────────────┐
             │  app/ai/ Engine   │   │ PostgreSQL 16 Database│
             │ (LangGraph Graph) │   │ (supporthub DB)       │
             └─────────────┬──────┘   └──────▲────────────────┘
                           │                 │
             ┌─────────────▼──────┐          │
             │ app/rag/ Pipeline  ├──────────┘ (pgvector)
             │ (Knowledge Base)   │
             └────────────────────┘
```

## System Components

### 1. Data Layer (PostgreSQL 16)
- **Single Source of Truth**: All business data (Users, Customers, Products, Orders, Payments, Shipments, Returns, Refunds) and support data (Tickets, Messages, CSAT, Vector Embeddings) are stored in PostgreSQL 16 (`supporthub` database).
- **Data Access Layer**: `app/data_access/postgres_business_repository.py` handles parameterized query execution with anti-IDOR checks.

### 2. AI Layer (`app/ai/`)
- **Orchestration**: `AIOrchestrator` & `AIRouter` analyze user queries, perform multi-question decomposition, enforce tenant context, and execute graph nodes.
- **LangGraph StateGraph**: `app/ai/graph/` implements a graph state execution pipeline (`support_graph.py`).

### 3. RAG Layer (`app/rag/`)
- **Ingestion & Indexing**: Loads markdown policy articles from `knowledge_base/`, chunks text, generates embeddings (1536 dimensions), and stores them in PostgreSQL `pgvector`.
- **Retrieval & Grounding**: Executes cosine similarity search with keyword fallback and grounds model responses.

### 4. Live Chat & Escalation Layer
- **WebSocket Gateway**: `app/routers/ws/chat.py` manages real-time messaging, ticket session state, agent assignment, and AI suppression when an agent joins (`agent_joined = True`).

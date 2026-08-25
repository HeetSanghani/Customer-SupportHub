# 21 — Target Architecture Proposal

## Proposed Consolidated Repository Structure

```
Customer-SupportHub/
├── supporthub/
│   ├── frontend/                   (React + Vite SPA)
│   └── backend/
│       ├── app/
│       │   ├── main.py             (FastAPI Entry)
│       │   ├── models/             (PostgreSQL SQLModels)
│       │   ├── routers/            (REST Routers)
│       │   ├── ws/                 (WebSocket Handler)
│       │   ├── services/           (LiveChatAIAdapter)
│       │   │
│       │   ├── ai/                 (Consolidated AI Engine from supporthub-ai-architecture)
│       │   │   ├── router.py
│       │   │   ├── intent.py
│       │   │   ├── orchestrator.py
│       │   │   ├── context.py
│       │   │   ├── tools.py
│       │   │   ├── security.py
│       │   │   └── response.py
│       │   │
│       │   ├── data_access/        (MySQL 8.0 PyMySQL Repository & Services)
│       │   │   ├── db.py
│       │   │   ├── mysql_repository.py
│       │   │   └── *_service.py
│       │   │
│       │   └── rag/                (RAG Ingestion & Vector Retriever)
│       │       ├── pipeline.py
│       │       ├── retriever.py
│       │       └── documents/policies/
│       │
│       └── tests/
│           ├── test_auth.py
│           ├── test_tickets.py
│           └── ai/                  (Consolidated AI Architecture Tests)
```

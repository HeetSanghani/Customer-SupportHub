# 18 — Proposed Target Repository Structure

## Executive Summary
This document defines the target consolidated project structure for `Customer-SupportHub` following cleanup and refactoring, establishing a pristine foundation for the LangGraph/LangChain phase.

---

## 1. Consolidated Target Tree

```
Customer-SupportHub/
├── README.md                                [Root Guide]
├── SETUP_NEW_MACHINE.md                     [Dev Onboarding]
├── db_explorer.py                           [DB Inspection Web UI]
├── inspect_db.py                            [DB Inspection CLI Tool]
├── knowledge_base/                          [RAG Knowledge Base Source]
│   ├── articles/                            [knowledge_articles.json]
│   └── policies/                            [policies.json]
├── docs/                                    [Project Documentation & Phase Reports]
│   ├── archive/                             [Historical Phase Reports 11-14]
│   └── cleanup_audit/                       [Phase A.1 Audit Reports]
├── output/                                  [Audit Summary Reports]
├── scripts/                                 [Dev Operations & Maintenance Scripts]
└── supporthub/                              [Primary Application Folder]
    ├── docker-compose.yml                   [Docker Composition]
    ├── nginx.conf                           [Nginx Reverse Proxy Config]
    ├── frontend/                            [React 18 / Vite Frontend]
    │   ├── src/
    │   ├── package.json
    │   └── vite.config.js
    └── backend/                             [FastAPI / SQLModel Backend]
        ├── pyproject.toml
        ├── uv.lock
        ├── clean_and_seed.py
        ├── restore_real_data.py
        ├── app/
        │   ├── main.py                      [FastAPI Entrypoint]
        │   ├── config.py                    [Pydantic Settings]
        │   ├── database.py                  [SQLModel Async Engine]
        │   ├── dependencies.py              [JWT Auth & Dep Injection]
        │   ├── ai/                          [CANONICAL MODULAR AI ENGINE]
        │   │   ├── orchestrator.py          [Central AI Orchestrator]
        │   │   ├── router.py                [Intent Classifier & Router]
        │   │   ├── intent.py                [Intent Rules & Regex]
        │   │   ├── context.py               [Multi-turn Conversation Context]
        │   │   ├── security.py              [Security & Prompt Injection Validator]
        │   │   ├── escalation.py            [Human Escalation Evaluator]
        │   │   ├── tools.py                 [Tool Registry & Customer Service]
        │   │   ├── response.py              [Response Synthesizer]
        │   │   ├── graph/                   [LANGGRAPH ENGINE]
        │   │   │   ├── build.py             [Compiled State Graph]
        │   │   │   ├── nodes.py             [Graph State Nodes]
        │   │   │   └── state.py             [Graph State Type Definitions]
        │   │   ├── llm/                     [LLM Provider Adapters]
        │   │   └── prompts/                 [Prompt Templates]
        │   ├── rag/                         [CANONICAL RAG ENGINE]
        │   │   ├── pipeline.py              [RAG Pipeline]
        │   │   ├── retriever.py             [pgvector 1536-dim Retriever]
        │   │   ├── embeddings.py            [Embedding Provider]
        │   │   ├── chunker.py               [Document Chunker]
        │   │   ├── document_processor.py    [Document Standardization]
        │   │   └── loader.py                [JSON Document Loader]
        │   ├── data_access/                 [UNIFIED BUSINESS DATA REPOSITORY]
        │   │   ├── postgres_business_repository.py  [PostgreSQL Business Data Repo]
        │   │   ├── customer_service.py      [Customer Operations]
        │   │   ├── order_service.py         [Order Operations]
        │   │   └── refund_service.py        [Refund Operations]
        │   ├── models/                      [SQLMODEL POSTGRESQL SCHEMAS]
        │   ├── routers/                     [REST & WEBSOCKET ENDPOINTS]
        │   └── services/                    [BUSINESS & OMNICHANNEL SERVICES]
        │       ├── instagram/               [Instagram Webhook Handler]
        │       ├── whatsapp/                [WhatsApp Webhook Handler]
        │       ├── facebook/                [Facebook Webhook Handler]
        │       └── conversations/           [Conversation Thread Repository]
        └── tests/                           [REGRESSION & UNIT TEST SUITE]
```

---

## 2. Structural Improvements Highlighted

1. **Elimination of Obsolete Root Files**: Removal of root `app.js`, `index.html`, `vercel.json`, and zero-byte backend files.
2. **Unified AI Engine**: AI capabilities consolidated into `app/ai/` and `app/ai/graph/`. `app/services/ai/` deprecated.
3. **Unified RAG Engine**: RAG capabilities consolidated into `app/rag/`. `knowledge_rag.py` deprecated.
4. **Renamed Business Repository**: `mysql_repository.py` renamed to `postgres_business_repository.py` to accurately reflect PostgreSQL database storage.

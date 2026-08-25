# 15 — Duplicate Code & Component Audit

## Executive Summary
This document catalogs all duplicate, redundant, or parallel implementations discovered within `Customer-SupportHub`, identifying canonical vs. duplicate implementations for each component.

---

## 1. Itemized Duplication Matrix

| Component Area | Canonical Implementation | Duplicate / Redundant Implementation | Evidence & Risk of Removal | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **AI Orchestrator** | `app/ai/orchestrator.py` | `app/services/ai/orchestrator.py` | `app/ai/` integrates LangGraph and multi-turn context. `app/services/ai/` uses legacy sequential prompts. | **Consolidate**: Update webhooks to use `app/ai/orchestrator.py`. |
| **RAG Pipeline** | `app/rag/pipeline.py` | `app/services/ai/knowledge_rag.py` | `app/rag/` uses pgvector 1536-dim embeddings. `knowledge_rag.py` uses legacy regex string search. | **Deprecate**: Point all queries to `app/rag/pipeline.py`. |
| **AI File vs. Pkg** | `app/ai/` (Package Dir) | `app/ai.py` (Single File) | `app/ai.py` is shadowed by Python package resolution rules and cannot be imported directly. | **Remove**: Delete `app/ai.py`. |
| **DB Explorer Script**| `db_explorer.py` (Root) | `inspect_db.py` (Root) | Both perform read-only DB inspection. `db_explorer` provides a web UI on port 8090; `inspect_db` is CLI. | **Keep Both as Dev Tools** or consolidate into `scripts/`. |
| **Root Frontend** | `supporthub/frontend/` | Root `index.html` & `app.js` | `supporthub/frontend/` is the active React/Vite app. Root files are legacy prototype code. | **Remove**: Flag root `index.html` and `app.js` for removal. |
| **Zero-Byte Artifacts**| N/A | `AIOrchestrator`, `AIRouter`, `Client`, `Execution`, `LiveChatAIAdapter`, `Ownership` in `backend/` | Zero-byte files created accidentally in `backend/` directory root. | **Remove**: Delete zero-byte artifact files. |

---

## 2. Consolidation Strategy

The primary cleanup goal prior to the LangGraph phase is establishing **`app/ai/`** as the single canonical AI package and **`app/rag/`** as the single canonical RAG package:

```
BEFORE CLEANUP:
supporthub/backend/app/
├── ai/                      <-- Canonical Modular AI (LangGraph)
├── rag/                     <-- Canonical pgvector RAG
├── services/
│   └── ai/                  <-- Duplicate Legacy AI & RAG
└── ai.py                    <-- Obsolete Shadowed Script

AFTER CLEANUP:
supporthub/backend/app/
├── ai/                      <-- SINGLE CANONICAL AI ENGINE
│   └── graph/               <-- LangGraph Nodes & State
├── rag/                     <-- SINGLE CANONICAL RAG ENGINE
└── services/                <-- Business & Omnichannel Services Only
```

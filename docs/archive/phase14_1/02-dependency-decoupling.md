# Phase 14.1 — Dependency Decoupling & Import Refactoring

## Sys.path Removal
The legacy `sys.path.insert(0, _AI_ARCH_PATH)` injection in `LiveChatAIAdapter` (`app/services/ai/live_chat_adapter.py`) was completely removed.

## Native Package Import Hierarchy
All modules now import natively from `app.*`:
- `from app.ai.orchestrator import AIOrchestrator, ai_orchestrator`
- `from app.ai.context import ContextManager, context_manager`
- `from app.ai.router import AIRouter, ai_router`
- `from app.data_access.loader import data_loader`
- `from app.rag.retriever import RAGRetriever`
- `from app.ai.config import settings`

No external PYTHONPATH or sys.path hacks are needed or used.

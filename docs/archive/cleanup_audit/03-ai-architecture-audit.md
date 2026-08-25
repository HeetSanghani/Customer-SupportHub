# 03 — AI Architecture & LangGraph Preparedness Audit

## Executive Summary
This audit evaluates all AI-related source code across `Customer-SupportHub`, specifically assessing `app/ai/`, `app/services/ai/`, `app/ai/graph/`, and external repositories (`supporthub-ai-architecture`). The objective is to determine which implementation is canonical and evaluate readiness for the upcoming LangGraph/LangChain migration phase.

---

## 1. AI Codebase Inventory & Duplication Analysis

The audit uncovered two distinct AI implementations inside the backend:

### Implementation A: `app/ai/` (Canonical Modular Engine)
* **Location**: `supporthub/backend/app/ai/`
* **Components**:
  * `orchestrator.py`: Modular AI orchestrator integrating LangGraph execution.
  * `router.py`: Dual-mode intent router (deterministic regex + LLM classifier).
  * `intent.py`: Intent classification hierarchy with entity extraction.
  * `context.py`: Multi-turn context manager with turn sliding-window logic.
  * `security.py`: Security validator enforcing cross-tenant ownership and prompt injection guards.
  * `escalation.py`: Rules-based & sentiment-based human handoff evaluator.
  * `tools.py`: Tool registry integrating `CustomerService` and order/return tools.
  * `response.py`: Response synthesizer with grounding validation and fallback handling.
  * `graph/`: LangGraph execution graph implementation (`build.py`, `nodes.py`, `state.py`).
  * `llm/`: LLM provider adapters (`client.py`, `provider.py`, `models.py`).

### Implementation B: `app/services/ai/` (Legacy Webhook Pipeline)
* **Location**: `supporthub/backend/app/services/ai/`
* **Components**:
  * `orchestrator.py`: Legacy sequential orchestrator.
  * `context_builder.py`: Context formatter for legacy prompt construction.
  * `prompt_builder.py`: Prompt builder generating monolithic system prompts.
  * `model_adapter.py`: Direct model adapter for Gemini/OpenAI.
  * `response_parser.py`: Regex response parser for structured LLM outputs.
  * `knowledge_rag.py`: File-based keyword/GenAI RAG search.

### Shadowed File: `app/ai.py`
* **Location**: `supporthub/backend/app/ai.py`
* **Status**: OBSOLETE. Fully shadowed by the `app/ai/` package directory. Contains legacy 768-to-1536 zero-padded Gemini embedding function.

---

## 2. LangGraph & LangChain Integration Assessment

> [!IMPORTANT]
> **Key Finding**: LangGraph is **already partially implemented and actively executed** within `app/ai/graph/`!

### Existing LangGraph Implementation Details:
1. **Dependencies**: `langgraph>=0.2.0`, `langchain-core` installed and configured in `pyproject.toml` and `uv.lock`.
2. **Graph Structure** (`app/ai/graph/build.py`):
   * Graph state defined in `app/ai/graph/state.py` (`GraphState`).
   * State nodes defined in `app/ai/graph/nodes.py`:
     * `context_resolution_node`
     * `intent_routing_node`
     * `tool_execution_node`
     * `rag_retrieval_node`
     * `security_validation_node`
     * `response_synthesis_node`
3. **Execution Integration**: `app/ai/orchestrator.py` invokes `compiled_graph.invoke(initial_state)` inside `process_message()`.

---

## 3. Detailed Comparison & Primary AI Questions Answered

### Q1: Which AI code is actually used?
* **Live Chat WebSocket**: Uses `app/services/ai/live_chat_adapter.py` -> `app/ai/orchestrator.py` -> `app/ai/graph/build.py` (LangGraph).
* **Background Webhooks**: Uses `app/services/ai/orchestrator.py` (Legacy).

### Q2: Which AI code is legacy / duplicate?
* `app/services/ai/orchestrator.py`, `context_builder.py`, `prompt_builder.py`, `response_parser.py`, `knowledge_rag.py`, and `app/ai.py` are duplicate/legacy artifacts.

### Q3: Which AI code should become the foundation for LangGraph?
* `app/ai/` (specifically `app/ai/graph/`) is the clean foundation for all future LangGraph development.

### Q4: Would introducing LangGraph create duplicate architecture?
* If introduced as a new package alongside `app/services/ai/`, yes. But because `app/ai/graph/` is already in place, migrating remaining webhook callers to `app/ai/orchestrator.py` will eliminate all duplication cleanly.

---

## 4. Recommendations Before LangGraph Phase

1. **Consolidate Webhook Handlers**: Update Instagram, WhatsApp, and Email webhooks to instantiate `app.ai.orchestrator.AIOrchestrator` instead of `app.services.ai.orchestrator.AIOrchestrator`.
2. **Deprecate `app/services/ai/`**: Once webhooks are updated, flag `app/services/ai/` for archival.
3. **Delete Shadowed `app/ai.py`**: Remove the unimported `app/ai.py` file to clean up the module namespace.

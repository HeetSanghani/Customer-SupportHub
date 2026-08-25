# LangGraph StateGraph Architecture

## Implementation Status
- **Location**: `supporthub/backend/app/ai/graph/`
- **Framework**: `langgraph` (v0.2+)
- **Status**: **Partially Implemented & Integrated**

## Graph Structure

```
                     ┌──────────────────────┐
                     │   check_escalation   │
                     └──────────┬───────────┘
                                │ Conditional Edge
            ┌───────────────────┴───────────────────┐
            │ escalate                              │ decompose
            ▼                                       ▼
 ┌──────────────────────┐                ┌──────────────────────┐
 │handle_human_escalation               │   decompose_query    │
 └──────────┬───────────┘                └──────────┬───────────┘
            │                                       │
            │                                       ▼
            │                            ┌──────────────────────┐
            │                            │  handle_subquestions │
            │                            └──────────┬───────────┘
            │                                       │
            │                                       ▼
            │                            ┌──────────────────────┐
            │                            │ aggregate_responses  │
            │                            └──────────┬───────────┘
            │                                       │
            └───────────────────┬───────────────────┘
                                ▼
                       ┌──────────────────┐
                       │       END        │
                       └──────────────────┘
```

## Graph State Definition (`state.py`)
The graph state is encapsulated in `GraphState` (TypedDict):
- `messages`: List of message objects.
- `customer_id`: Linked business customer ID.
- `tenant_id`: Multi-tenant organization.
- `subquestions`: Extracted sub-queries.
- `subquestion_results`: Individual tool/RAG execution outputs.
- `escalated`: Boolean escalation flag.
- `final_response`: Formatted response string.

## Active Implementation Matrix

| Component | Status | Implementation File | Description |
| :--- | :--- | :--- | :--- |
| **State Schema** | ✅ Implemented | `app/ai/graph/state.py` | `GraphState` definition |
| **Graph Nodes** | ✅ Implemented | `app/ai/graph/nodes.py` | `check_escalation`, `decompose_query`, `handle_subquestions`, `aggregate_responses`, `handle_human_escalation` |
| **StateGraph Builder**| ✅ Implemented | `app/ai/graph/build.py` | `build_graph()` & `compiled_graph` |
| **Checkpoint Persist** | 📋 Planned (Phase B) | `app/ai/graph/checkpointer.py` | PostgreSQL state persistence across turns |

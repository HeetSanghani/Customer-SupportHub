# AI Engine Overview

## Architecture Location
- **Canonical Package**: `supporthub/backend/app/ai/`
- **Primary Entrypoint**: `app.ai.orchestrator.AIOrchestrator`
- **Router Module**: `app.ai.router.AIRouter`
- **LangGraph Graph**: `app.ai.graph.support_graph.SupportGraph`

## Core Concepts

### 1. Intent Classification & Routing
Incoming queries are classified into five primary execution routes:
- **`STRUCTURED`**: Queries regarding specific orders, shipments, returns, refunds, or payment status. Resolved via deterministic data queries in `PostgresBusinessRepository`.
- **`RAG`**: General policy, warranty, shipping terms, or FAQ inquiries. Resolved via `app.rag.pipeline.RAGPipeline`.
- **`HYBRID`**: Complex multi-intent queries requiring both structured order data and policy synthesis.
- **`HUMAN`**: Explicit user requests for a human agent or repeated dissatisfaction signals. Triggers ticket escalation.
- **`SECURITY`**: Unauthenticated or unauthorized cross-tenant data requests (Anti-IDOR). Instantly blocked with access denied message.

### 2. Context & Identity Propagation
Every request processed by `AIOrchestrator` includes:
- `user_id`: Authenticated user account identifier.
- `customer_id`: Linked business customer profile ID.
- `tenant_id`: Multi-tenant organization identifier (e.g., `shopkart`).
- `channel`: Originating communication channel (`live_chat`, `whatsapp`, `instagram`, `facebook`, `email`).

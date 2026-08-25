# 04 — Architecture Contradiction Matrix

## Audit of Historical Claims vs. Current Source of Truth

| Subsystem / Topic | Historical Claim (Archive) | Current Reality (Active Code & Docs) | Affected Historical Documents | Resolution / Action |
| :--- | :--- | :--- | :--- | :--- |
| **Business DB Engine** | ShopKart business data resides in MySQL (`mysql_repository.py`) | Business data resides in **PostgreSQL 16** (`postgres_business_repository.py`) | `phase13/*`, `phase14/*` | **Archived** to `docs/archive/`. Current docs explicitly specify PostgreSQL 16. |
| **AI Orchestration** | Legacy standalone scripts or external `supporthub-ai-architecture` project | Integrated **`supporthub/backend/app/ai/`** package with `AIOrchestrator` | `phase11/*`, `phase14/*` | **Archived** to `docs/archive/`. Active entrypoint is `app/ai/`. |
| **LangGraph Status** | Planned future migration | **Partially Implemented** in `app/ai/graph/` (`support_graph.py`, `nodes.py`) | `phase14/*` | **Updated** in current `docs/ai/langgraph-architecture.md`. |
| **RAG Retrieval Engine** | Standalone file keyword search or isolated scripts | Integrated **`app/rag/`** with PostgreSQL `pgvector` (1536-dim embeddings) | `phase11/*`, `phase12/*` | **Archived** to `docs/archive/`. Active entrypoint is `app/rag/`. |
| **User ↔ Customer Identity** | Separate unlinked User and Customer entities | Unified **User linkage** via `user.customer_id` and JWT tokens | `phase11/*` | **Archived** to `docs/archive/`. Active security model documented in `docs/security/`. |

## Certification
Zero active documentation files in `docs/` contain contradictory architecture claims. All historical claims are preserved strictly in `docs/archive/`.

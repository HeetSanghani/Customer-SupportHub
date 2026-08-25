# 11 — Runtime Dependency Graph

## End-to-End Runtime Execution Flow

```
[React Frontend SPA (Vite / Port 5173)]
        │ (WebSocket / REST HTTP)
        ▼
[FastAPI Server (uvicorn / Port 8001)]
        │
        ├── Auth Router ---> PostgreSQL (users table / JWT validation)
        │
        └── WebSocket Router (/ws/chat/{ticket_id})
                │
                ▼
      [LiveChatAIAdapter] (app/services/ai/live_chat_adapter.py)
                │ (sys.path import)
                ▼
      [AIOrchestrator] (supporthub-ai-architecture/ai/orchestrator.py)
                │
                ├── [AISecurityGuard] (Ownership Check against CUST-001)
                │
                ├── [AIRouter] (5-Tier Routing Hierarchy)
                │         ├── Tier 1: Security Denial
                │         ├── Tier 2: Escalation Guard -> Update Ticket Status
                │         ├── Tier 3: Hybrid Engine -> MySQL + RAG
                │         ├── Tier 4: RAG Retriever -> PostgreSQL pgvector
                │         └── Tier 5: Structured Query -> ShopKart Adapter
                │
                ├── [ShopKartBusinessDataAdapter]
                │         │
                │         ▼
                │   [MySQLRepository] ---> MySQL 8.0 (supporthub_business)
                │
                ▼
      [ResponseSynthesizer] ---> Grounded Answer Output
                │
                ▼
      Broadcast via WebSocket to Customer Chat UI & Admin Inbox
```

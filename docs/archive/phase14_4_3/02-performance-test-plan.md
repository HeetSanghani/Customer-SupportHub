# 02 — Performance Test Plan

Scenarios evaluated across 1, 5, 10, 25, 50, 100 concurrent clients:
- **Authentication**: JWT token generation and validation.
- **MySQL Queries**: Direct customer order, shipment, payment, and product lookups.
- **RAG Queries**: Policy document retrieval (`policies.json`).
- **Hybrid Queries**: Combined relational database lookup + policy rule evaluation.
- **Multi-Tenant Concurrency**: Concurrent cross-customer attacks (`CUST-001` vs `CUST-002`).
- **WebSocket Scaling**: Concurrent `/ws/chat/{ticket_id}` connections through Nginx proxy.

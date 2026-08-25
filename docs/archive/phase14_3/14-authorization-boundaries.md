# 14 — Authorization Boundaries

- Layer 1: FastAPI Endpoint Auth (`get_current_user`).
- Layer 2: WebSocket Ticket Ownership (`/ws/chat/{ticket_id}`).
- Layer 3: Tool-level Ownership Check (`_check_ownership()` in `AIOrchestrator`).

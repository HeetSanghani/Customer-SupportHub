# 12 - WebSocket Authentication & Anti-IDOR Audit

## Endpoint
- **URL**: `ws://<host>/api/v1/ws/chat/{ticket_id}?token=<jwt_token>`
- **File**: `app/routers/ws/chat.py`

## Authentication & Authorization Sequence

```
Client (Browser / Mobile)
    │
    │ 1. Connect WS with query param ?token=JWT
    ▼
FastAPI endpoint: websocket_chat(ticket_id, websocket)
    │
    ├── Step 1: `await websocket.accept()`
    │
    ├── Step 2: Authenticate via `get_ws_user(websocket, session)`
    │      ├── Extract token from `websocket.query_params.get("token")`
    │      ├── Decode JWT signature and extract `sub` claim (User UUID)
    │      ├── Fetch User from PostgreSQL (`session.get(User, UUID(user_id))`)
    │      └── If invalid/expired/suspended: `await websocket.close(code=4001/4003)` and RETURN
    │
    ├── Step 3: Validate Ticket UUID format
    │      └── If invalid UUID: `await websocket.close(code=4004)` and RETURN
    │
    ├── Step 4: Verify Ticket existence in PostgreSQL
    │      └── If ticket not found: `await websocket.close(code=4004)` and RETURN
    │
    ├── Step 5: Anti-IDOR Ownership Guard (Phase 12 / 13)
    │      if user.role.value == "customer":
    │          if ticket.customer_id and ticket.customer_id != user.id:
    │              logger.warning("[WS SERVER] Anti-IDOR guard triggered...")
    │              await websocket.close(code=4003)  # Forbidden
    │              return
    │
    └── Step 6: Connection Approved
           Add connection to `manager.connect(ticket_id, websocket)`
           Broadcast presence and enter message receive loop
```

## Security Assessment
1. **Token Authentication**: All WebSocket connections require a valid JWT passed in query string `?token=...`.
2. **Ticket Ownership Enforcement (Anti-IDOR)**: Customers are restricted to connecting strictly to ticket rooms where `ticket.customer_id == user.id`. If a customer attempts to connect to another customer's ticket room, the server rejects the connection with close code `4003` (Forbidden).
3. **Staff Privileges**: Agents, Managers, and Admins (`role != 'customer'`) bypass the ticket ownership check to allow support representatives to enter and respond in any customer ticket room.

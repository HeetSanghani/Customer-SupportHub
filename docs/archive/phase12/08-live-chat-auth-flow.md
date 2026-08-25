# 08 — Authenticated Live Chat Message Lifecycle

## Executive Summary
This document traces the complete end-to-end lifecycle of an authenticated live chat message from the browser to the backend WebSocket router, `LiveChatAIAdapter`, `AIOrchestrator`, and real-time response delivery.

---

## Complete End-to-End Sequence Diagram

```
CUSTOMER (BROWSER)           FASTAPI WS ROUTER          LIVE CHAT AI ADAPTER          AI ORCHESTRATOR           SHOPKART DB / RAG
       │                            │                            │                            │                         │
       │ 1. CONNECT /ws/chat/{id}   │                            │                            │                         │
       │    ?token=<jwt_token>      │                            │                            │                         │
       ├───────────────────────────>│                            │                            │                         │
       │                            │ 2. Authenticate User       │                            │                         │
       │                            │    Verify Room Ownership   │                            │                         │
       │                            ├──────────────────────────┐ │                            │                         │
       │                            │ user = get_ws_user()     │ │                            │                         │
       │                            │ ticket.customer_id==user │ │                            │                         │
       │                            │<─────────────────────────┘ │                            │                         │
       │                            │                            │                            │                         │
       │ 3. SEND message:           │                            │                            │                         │
       │    "Where is my order?"    │                            │                            │                         │
       ├───────────────────────────>│                            │                            │                         │
       │                            │ 4. Persist User Message    │                            │                         │
       │                            │    to Postgres DB          │                            │                         │
       │                            │                            │                            │                         │
       │                            │ 5. Trigger Async Task      │                            │                         │
       │                            ├───────────────────────────>│                            │                         │
       │                            │                            │ 6. Resolve customer_id     │                         │
       │                            │                            │    (e.g., CUST-001)        │                         │
       │                            │                            │ 7. Invoke Orchestrator     │                         │
       │                            │                            ├───────────────────────────>│                         │
       │                            │                            │                            │ 8. Intent & Tool Select │
       │                            │                            │                            │    Execute Tool         │
       │                            │                            │                            ├────────────────────────>│
       │                            │                            │                            │<────────────────────────┤
       │                            │                            │                            │ 9. Ownership Verification│
       │                            │                            │                            │    Synthesize Response  │
       │                            │                            │<───────────────────────────┤                         │
       │                            │<───────────────────────────┤                            │                         │
       │ 10. BROADCAST AI Response  │ 9. Persist AI Message      │                            │                         │
       │<───────────────────────────┤    to Postgres DB          │                            │                         │
       │                            │                            │                            │                         │
```

---

## Lifecycle Steps Detail

1. **Connection Initialization**:
   - Customer UI opens WebSocket connection to `ws://localhost:8000/api/v1/ws/chat/{ticket_id}?token={jwt_access_token}`.
   - Server runs `get_ws_user()`, decoding `sub` to fetch the `User` object.
2. **Room Access Verification**:
   - Server checks `ticket.customer_id == user.id`. If unowned and user is not agent/admin, socket closes with code `4003`.
3. **Inbound Message Submission**:
   - Customer sends JSON payload: `{"type": "message", "body": "Where is my order?"}`.
   - Message saved to `messages` table with `sender_id = user.id`, `sender_type = "customer"`.
4. **AI Processing Invocation**:
   - WebSocket handler schedules non-blocking task `handle_ai_response()`.
   - `live_chat_ai_adapter.process_live_chat_message()` executes in an isolated DB session.
5. **AI Orchestration & Data Retrieval**:
   - `_orchestrator.process_message()` resolves context, classifies intent (`ORDERS`), extracts entities, and calls `get_customer_orders(customer_id="CUST-001")`.
   - `_check_ownership()` confirms returned orders belong to `"CUST-001"`.
   - ResponseSynthesizer formats response text: *"Your order ORD-013 is currently IN_TRANSIT..."*
6. **Persistence & Broadcasting**:
   - AI response saved to `messages` table (`sender_type = "ai"`).
   - WebSocket manager broadcasts response to room subscribers.

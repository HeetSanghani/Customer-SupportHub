# SupportHub Phase 11 — Live Chat Current Flow Deep Analysis

**Document Version:** 1.0.0  
**Status:** Completed  
**Author:** AI Integration Pair Programmer  
**Target:** Live Chat Channel (Website) Only  

---

## 1. Executive Summary

This document details the exact end-to-end technical flow of SupportHub's **Website Live Chat** channel in its current state. It traces the lifecycle of a message from the React frontend, through the WebSocket transport layer and authentication mechanism, to PostgreSQL database persistence, and back via real-time broadcasting.

The objective is to establish an authoritative baseline before introducing the **Live Chat AI Architecture Adapter** in Phase 11.

---

## 2. End-to-End Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (React)                              │
│                                                                         │
│   CustomerLiveChat.jsx ──▶ ChatPane Component                           │
│   ├── ticketsApi.create()                                               │
│   ├── ticketsApi.getMessages()                                          │
│   └── WebSocket Client (`ws://host/ws/chat/{ticket_id}?token={token}`)   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                     WebSocket JSON Frames (Bidirectional)
                                     │
┌────────────────────────────────────▼────────────────────────────────────┐
│                    BACKEND (FastAPI + SQLModel)                         │
│                                                                         │
│   app/routers/ws/chat.py (`websocket_chat` route handler)               │
│   ├── 1. WebSocket accept & JWT Auth via `get_ws_user()`                │
│   ├── 2. ConnectionManager (`app/ws/manager.py`) Room Registration     │
│   ├── 3. JSON Frame Processing (`type: "message"`)                      │
│   ├── 4. PostgreSQL Persistence (`Message`, `Ticket` timestamp)         │
│   ├── 5. WebSocket Broadcast to Room Subscribers                        │
│   ├── 6. WebSocket Broadcast to Agent Inbox (`__agent_inbox__`)        │
│   └── 7. Asynchronous AI Processing Hook (`process_ai_reply`)          │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                      Database & AI Subsystems
                                     │
┌────────────────────────────────────▼────────────────────────────────────┐
│                       DATA & SERVICE LAYERS                             │
│                                                                         │
│   PostgreSQL: `tickets`, `messages`, `users` tables                     │
│   AI Layer: Legacy inline orchestrator in `app/services/ai/`           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Message Trace

### Step 1: Conversation Initialization & Navigation
1. **Frontend Initiation**:
   - Location: `supporthub/frontend/src/pages/customer/CustomerLiveChat.jsx` (Lines 444–460)
   - The user opens the Category Picker modal and selects a category (e.g., Billing, Technical, General).
   - A POST request is made via `ticketsApi.create()` to `/tickets/` with:
     ```json
     {
       "subject": "BILLING Support Query",
       "category": "billing",
       "priority": "medium",
       "channel": "website_chat",
       "metadata": {}
     }
     ```
2. **Backend Ticket Creation**:
   - Location: `supporthub/backend/app/routers/tickets.py` (Lines 173–236)
   - `create_ticket()` generates a unique `ref` (e.g. `TCK-10492`), calculates SLA based on priority, commits the `Ticket` record, and injects an initial greeting `Message` (`sender_type="ai"`).
   - The React client navigates to `/customer/chat/{ticket.id}`.

---

### Step 2: WebSocket Handshake & Authentication
1. **Frontend Connection Establishment**:
   - Location: `supporthub/frontend/src/pages/customer/CustomerLiveChat.jsx` (Lines 162–203)
   - The `ChatPane` component instantiates `new WebSocket(wsUrl)`:
     ```javascript
     const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
     const host = window.location.host;
     const wsUrl = `${protocol}//${host}/ws/chat/${ticketId}?token=${token}`;
     ```
2. **Backend Route & Authentication**:
   - Location: `supporthub/backend/app/routers/ws/chat.py` (Lines 134–178)
   - Handler: `@router.websocket("/ws/chat/{ticket_id}")`
   - `await websocket.accept()` accepts the socket.
   - `user = await get_ws_user(websocket, session)` in `app/dependencies.py` extracts the JWT from query parameter `token`, decodes it, and fetches the `User` from PostgreSQL.
   - Validates `ticket_id` UUID exists in the `tickets` table; if not found, closes with code `4004`.
   - Calls `await manager.connect(ticket_id, websocket)` to register the socket connection in memory.
   - Broadcasts presence event:
     ```json
     {
       "type": "presence",
       "user_id": "<uuid>",
       "name": "Customer Name",
       "role": "customer",
       "joined_at": "2026-08-19T13:24:59Z"
     }
     ```

---

### Step 3: Inbound Customer Message Transmission
1. **Frontend Dispatch**:
   - Location: `supporthub/frontend/src/pages/customer/CustomerLiveChat.jsx` (Lines 208–216)
   - User types query and submits:
     ```javascript
     ws.send(JSON.stringify({ type: 'message', body: inputText }));
     setInputText('');
     setIsTyping(true);
     ```
2. **Backend Receipt**:
   - Location: `supporthub/backend/app/routers/ws/chat.py` (Lines 180–185)
   - `data = await websocket.receive_json()`
   - Validates `data.get("type") == "message"` and strips whitespace.

---

### Step 4: Message Persistence & State Management
1. **Database Write**:
   - Location: `supporthub/backend/app/routers/ws/chat.py` (Lines 186–200)
   - Updates `ticket.updated_at = datetime.now()`.
   - Creates and commits `Message` instance:
     ```python
     msg = Message(
         ticket_id=ticket_uuid,
         sender_id=user.id,
         sender_type=SenderType.customer,
         body=body,
     )
     session.add(msg)
     await session.commit()
     await session.refresh(msg)
     ```

---

### Step 5: Real-Time Broadcasting
1. **Room Broadcast**:
   - Location: `supporthub/backend/app/routers/ws/chat.py` (Lines 212–221)
   - Transmits to all connected participants in the ticket room:
     ```json
     {
       "type": "message",
       "id": "<message_uuid>",
       "ticket_id": "<ticket_uuid>",
       "sender_id": "<user_uuid>",
       "sender_name": "Customer Name",
       "sender_role": "customer",
       "body": "Where is my order ORD-2026-1001?",
       "created_at": "2026-08-19T13:25:00Z"
     }
     ```
2. **Agent Inbox Broadcast**:
   - Location: `supporthub/backend/app/routers/ws/chat.py` (Lines 224–229)
   - Pushes preview update to agent dashboard room `__agent_inbox__`.

---

### Step 6: Current AI Assistant Hook (Legacy Baseline)
1. **Invocation**:
   - Location: `supporthub/backend/app/routers/ws/chat.py` (Lines 232–355)
   - If `user.role.value == "customer"`, invokes `asyncio.create_task(process_ai_reply(body, ticket_id))`.
2. **Shortcomings of Current Legacy AI Hook**:
   - Uses generic LLM prompt or simple similarity retrieval without business entity awareness.
   - Lacks tenant isolation guards.
   - Has no structured tool execution for Order, Shipment, Product, Payment, Return, or Refund data from the ShopKart repository.
   - Has no multi-stage security validation (prompt injection, PII leak prevention, resource ownership authorization).
   - Lacks formal deterministic escalation decision contracts and department handoff payloads.

---

## 4. Summary of Data Structures & Contract Comparison

| Attribute | Current Live Chat | SupportHub AI Architecture (`supporthub-ai-architecture`) |
| :--- | :--- | :--- |
| **Inbound Message Contract** | Raw WS JSON dict `{"type": "message", "body": "..."}` | `NormalizedInboundMessage` dataclass with tenant, channel, customer metadata |
| **Data Grounding** | Unstructured KB text embeddings (`get_relevant_kb_context`) | 8 ShopKart domain tools (`Order`, `Product`, `Shipment`, `Payment`, etc.) + Multi-tenant RAG |
| **Security Validation** | Route-level JWT auth only | Multi-layer: Prompt injection detection + Caller ownership enforcement + Tenant security guards |
| **Result Payload** | Plain string `ai_text` | `NormalizedAIResult` with intent, route type, citations, confidence, escalation details |
| **Escalation Mechanism** | Simple string keyword matching (`"close chat"`, `"end ticket"`) | Dynamic `EscalationDecision` with priority, department, reason, and structured handoff payloads |

---

## 5. Conclusion & Transition to Stage 3

The existing Live Chat transport, WebSocket connection management, authentication, and database schemas are rock-solid and performant. 

In **Stage 3**, we design the integration adapter boundary to bridge the WebSocket layer (`app/routers/ws/chat.py`) to the production AI Architecture (`supporthub-ai-architecture`) without modifying transport or non-Live Chat channels.

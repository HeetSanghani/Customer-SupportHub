# SupportHub Phase 11 — AI Integration Boundary Specification

**Document Version:** 1.0.0  
**Status:** Completed  
**Author:** AI Integration Pair Programmer  
**Target:** Live Chat AI Adapter Architecture  

---

## 1. Architectural Boundary Overview

The integration between **SupportHub Live Chat** and the **SupportHub AI Architecture** is designed on the principle of a **Strict Additive Adapter Pattern**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SUPPORTHUB CORE                               │
│                                                                         │
│  [WebSocket Chat Router] ──▶ [Message Service & Database]                │
│             │                                                           │
│             ▼                                                           │
│  [LiveChatAIAdapter] ◄─── (Thin Boundary Adapter)                       │
└─────────────┬───────────────────────────────────────────────────────────┘
              │ 1. Normalize (Ticket, User, Message) ──▶ NormalizedInboundMessage
              │ 2. Process via AI Orchestrator (Intent, Tools, RAG, Security)
              │ 3. Receive NormalizedAIResult (Text, Citations, Escalation)
              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      SUPPORTHUB AI ARCHITECTURE                         │
│                    (supporthub-ai-architecture)                         │
│                                                                         │
│  ├── AIOrchestrator (Router, Tools, RAG, Security, Synthesizer)        │
│  ├── ShopKart Data Access & Grounding Tools                             │
│  ├── Policy RAG Engine with pgvector / Chroma Vector Store              │
│  └── Multi-Tenant Boundary & Ownership Security Guard                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Interface Contracts & Data Mapping

### A. Inbound Mapping: SupportHub ➔ NormalizedInboundMessage

The adapter converts SupportHub entities into the canonical `NormalizedInboundMessage`:

```python
normalized_msg = NormalizedInboundMessage(
    message_id=str(msg.id),
    conversation_id=str(ticket.id),
    customer_id=str(user.id) if user.id else "GUEST",
    tenant_id="shopkart",
    channel=ChannelType.WEBSITE,
    text=msg.body,
    timestamp=msg.created_at.isoformat() if msg.created_at else datetime.now(timezone.utc).isoformat(),
    sender_type=SenderType.CUSTOMER,
    metadata={
        "ticket_ref": ticket.ref,
        "ticket_subject": ticket.subject,
        "ticket_category": ticket.category,
        "customer_email": user.email,
        "customer_name": user.name,
        "customer_channel_id": user.channel_customer_id,
    }
)
```

### B. Outbound Mapping: NormalizedAIResult ➔ SupportHub Entities

When `AIOrchestrator` returns `NormalizedAIResult`:

```python
# 1. Create and Persist AI Message
ai_message = Message(
    ticket_id=ticket.id,
    sender_id=None,
    sender_type=SenderType.ai,
    body=ai_result.response_text,
    metadata=json.dumps({
        "intent": ai_result.intent,
        "route": ai_result.route,
        "confidence": ai_result.confidence,
        "is_grounded": ai_result.is_grounded,
        "citations": [c.source_id for c in ai_result.citations] if ai_result.citations else [],
    })
)

# 2. Process Escalation
if ai_result.escalation and ai_result.escalation.required:
    ticket.status = TicketStatus.escalated
    if ai_result.escalation.priority:
        ticket.priority = TicketPriority(ai_result.escalation.priority.lower())
    ticket.category = ai_result.escalation.department or "escalation"

# 3. Broadcast Real-Time Events
await manager.broadcast(str(ticket.id), {
    "type": "message",
    "id": str(ai_message.id),
    "ticket_id": str(ticket.id),
    "sender_id": "AI",
    "sender_name": "Support AI",
    "sender_role": "ai",
    "body": ai_result.response_text,
    "created_at": ai_message.created_at.isoformat(),
})
```

---

## 3. Separation of Responsibilities

| Domain Responsibility | Handled By | Implementation Location |
| :--- | :--- | :--- |
| **WebSocket Connection Management** | SupportHub Backend | `app/ws/manager.py` |
| **User Authentication & RBAC** | SupportHub Backend | `app/dependencies.py` |
| **Database Transaction & ACID Writes** | SupportHub Backend | `app/database.py`, `app/models/` |
| **Intent Classification & Routing** | AI Architecture | `ai/router.py` |
| **ShopKart Business Entity Queries** | AI Architecture | `ai/tools.py`, `data_access/` |
| **Policy Retrieval-Augmented Generation** | AI Architecture | `rag/pipeline.py` |
| **Prompt Injection & Resource Security** | AI Architecture | `ai/security.py` |
| **Escalation Reason & Department Routing**| AI Architecture | `ai/orchestrator.py` |
| **Real-time Presence & Room Broadcasting**| SupportHub Backend | `app/routers/ws/chat.py` |

---

## 4. Error Handling, Fallback, and Async Isolation

1. **Non-blocking Execution**: AI response generation executes in an isolated `asyncio.create_task()` background context so that WebSocket ping/pong and message delivery remain ultra-responsive (<5ms latency).
2. **Graceful Fallbacks**: If the AI model or API encounters rate limits (429) or transient provider outages, the adapter falls back cleanly:
   ```
   "I'm sorry, our AI assistant is temporarily unavailable due to high demand. A human agent will assist you shortly."
   ```
3. **Database Session Isolation**: The background AI task instantiates its own `AsyncSessionLocal()` scope to prevent session conflict with the active WebSocket loop.

---

## 5. Non-Live Chat Channel Guarantee

To ensure zero regression:
- **WhatsApp** (`app/routers/webhooks/whatsapp.py`) remains **100% UNTOUCHED**.
- **Instagram** (`app/routers/webhooks/instagram.py`) remains **100% UNTOUCHED**.
- **Facebook / Messenger** remains **100% UNTOUCHED**.
- **Email** remains **100% UNTOUCHED**.

All modifications are strictly confined to the Live Chat adapter and the Live Chat WebSocket router.

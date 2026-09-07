# Phase B.5.2 — Ticket State & Conversation Lifecycle Mapping

**Module**: SupportHub Customer-Facing Experience  
**Phase**: B.5.2 — Customer Role Audit & Conversational UI/UX Redesign  
**Date**: September 1, 2026  

---

## 1. Ticket Lifecycle States

SupportHub enforces a deterministic ticket state machine across both AI and Human Agent interactions:

```
[ New Ticket ]
      |
      v
+------------------+
|   ✨ AI Active   | <--- Customer chats with RAG AI assistant
+------------------+
      |
      | (Customer clicks "Talk to Human" or AI detects escalation intent)
      v
+------------------+
|  Human Escalated | <--- AI responses paused; assigned to Human Agent queue
+------------------+
      |
      | (Agent accepts & responds)
      v
+------------------+
| In Progress      | <--- Active Human-Customer interaction
+------------------+
      |
      | (Resolution confirmed by Agent or Customer)
      v
+------------------+
|    Resolved      | <--- Triggers CSAT Rating / Review Prompt
+------------------+
      |
      | (Customer submits feedback or auto-close timer)
      v
+------------------+
|     Closed       | <--- Terminal state (Can be reopened via new message)
+------------------+
```

---

## 2. Real-time WebSocket Protocol & UI States

The conversational frontend connects to `/ws/chat/{ticket_id}` using a resilient event-driven handler.

### Event Types & UI Handling

| Event Type | Payload | UI Behavior |
| :--- | :--- | :--- |
| `message` | `{ id, sender_type, content, created_at }` | Appends new message bubble; auto-scrolls to bottom. |
| `typing` | `{ sender_type: 'bot' \| 'agent' }` | Displays streaming typing indicator (`SupportHub AI is typing...`). |
| `ticket_status_updated` | `{ status: 'in_progress' \| 'resolved' }` | Updates live status badge in header & renders banner notice. |
| `human_escalated` | `{ ticket_id, agent_name }` | Renders amber notification banner: *"Escalated to Human Agent. AI responses paused."* |
| `csat_requested` | `{ ticket_id }` | Displays inline 5-star CSAT feedback modal/card. |

---

## 3. Empty, Loading, and Error UI States

1. **Empty Workspace State**:
   - Displays SupportHub AI mascot icon & greeting.
   - Renders 6 pre-formatted common question chips.

2. **Loading State**:
   - Pulsing skeleton loaders for sidebar conversation items.
   - Animated typing dots in message area during AI streaming generation.

3. **WebSocket Disconnect State**:
   - Banner: *"Connecting to real-time sync service..."* with automatic exponential backoff retry (1s, 2s, 5s).
   - REST fallback API polls for messages if WebSocket loses connectivity.

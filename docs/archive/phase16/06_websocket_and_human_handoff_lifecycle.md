# Phase 16 — WebSocket Architecture & Human Handoff Lifecycle

## 1. Real-Time Infrastructure

The real-time communication layer is powered by FastAPI's WebSocket endpoint (`/ws/chat/{ticket_id}`) managed by `ConnectionManager`.

---

## 2. Event Lifecycle Sequence

1. **Handshake & Auth**: WebSocket connection validates token in query params and verifies ticket room authorization.
2. **AI Assistance**: Incoming customer messages trigger `LiveChatAIAdapter`. Bot replies are broadcast to room.
3. **Escalation Trigger**: Customer clicks "Talk to Human" -> Ticket status set to `escalated`.
4. **Agent Acceptance**: Agent accepts ticket -> Server broadcasts `agent_joined` event.
5. **AI Suppression**: `LiveChatAIAdapter` suppresses bot replies while agent is assigned (`agent_id IS NOT NULL`).
6. **Resolution & CSAT**: Agent resolves ticket -> Server sends CSAT survey prompt. Customer submits 1-5 star rating.

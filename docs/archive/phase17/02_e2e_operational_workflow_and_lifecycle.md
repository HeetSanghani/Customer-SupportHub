# Phase 17 — 02. End-to-End Operational Workflow & Lifecycle

## Lifecycle Sequence
1. **User Authentication**: Customer authenticates via `POST /api/v1/auth/token` receiving JWT access token.
2. **Session Initialization**: SPA initializes WebSocket connection to `/ws/chat/{ticket_id}?token={jwt}` or loads dashboard.
3. **Ticket Creation**: Customer submits ticket via UI or Chat (`POST /api/v1/tickets/`).
4. **AI Auto-Classification & Auto-Reply**:
   - `_ai_classify_ticket` background task creates dedicated DB session and queries Gemini API for category, priority, and sentiment.
   - `LiveChatAIAdapter` evaluates RAG context from vector store to supply automated response if confidence threshold >= 0.70.
5. **Agent Handoff**: If customer requests agent or AI confidence is low, ticket transitions to `open` status with unassigned agent.
6. **Agent Resolution**: Support agent claims ticket via `POST /api/v1/tickets/{id}/accept`, posts resolution message, and closes ticket via `POST /api/v1/tickets/{id}/resolve`.
7. **CSAT Feedback**: Customer submits rating and feedback via `POST /api/v1/csat/`.

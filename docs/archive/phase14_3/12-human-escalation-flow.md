# 12 — Human Escalation Flow

- **Trigger**: Low confidence, sentiment escalation, or explicit user request for a agent.
- **Action**: Ticket `status` set to `ESCALATED`, AI response paused, real-time WebSocket notification to Admin Inbox.

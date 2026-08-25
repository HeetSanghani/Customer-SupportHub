# 15 - Human Escalation Audit

## Human Escalation Triggers
The AI system escalates a conversation from AI automated handling to human agent intervention under five specific conditions:

1. **Explicit Customer Request**: Phrases like `"I want to talk to a human"`, `"agent please"`, `"representative"`.
2. **High Frustration Score**: Frustration detector exceeds threshold (`frustration_score >= 3`).
3. **Low Confidence Score**: AI confidence prediction drops below threshold (`ai_confidence < 0.75`).
4. **Sensitive Query Policy**: Financial disputes, account takeover reports, fraud allegations.
5. **Complex Multi-Turn Loop**: Unresolved intent loops after 3 attempts.

## Escalation Lifecycle Sequence

```
Customer Message
       │
       ▼
AIOrchestrator / Router
       │  Detects Escalation Trigger
       ▼
Route: HUMAN ESCALATION
       │
       ├── 1. Set Ticket Status: `ticket.status = TicketStatus.escalated`
       ├── 2. Set Context Escalated Flag: `ctx.escalated = True`
       ├── 3. Persist System / AI Hold Message to `messages` table
       ├── 4. Broadcast `inbox_update` event via `manager.broadcast_to_agents()`
       │      (Appears immediately in Agent Dashboard Inbox)
       └── 5. Future messages in ticket room bypass AI handling until resolved by Agent.
```

## Customer Identity Attachment
When a ticket escalates to a human agent, the customer's authenticated identity (`User.id`, `User.email`, `User.name`, `User.phone`, `User.customer_id`) remains linked to `ticket.customer_id`. The receiving human agent views the complete verified customer profile in their dashboard panel.

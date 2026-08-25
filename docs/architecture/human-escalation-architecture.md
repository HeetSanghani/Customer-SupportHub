# Human Support & Escalation Architecture

## Lifecycle Overview

```
 Customer Inquiry
        │
        ▼
 ┌──────────────┐      Issue Unresolved / Escalation Requested
 │  AI Chatbot  ├─────────────────────────────────────────────────┐
 └──────┬───────┘                                                 │
        │ Resolved                                                ▼
        ▼                                               ┌───────────────────┐
 ┌──────────────┐                                       │  Create Ticket    │
 │ Close Session│                                       │ (status: open)    │
 └──────────────┘                                       └─────────┬─────────┘
                                                                  │
                                                                  ▼
 ┌──────────────┐       Agent Accepts Ticket            ┌───────────────────┐
 │ CSAT Survey  │ ◄─────────────────────────────────────┤ Agent Joined      │
 └──────────────┘           (Issue Resolved)            │ (AI Suppressed)   │
                                                        └───────────────────┘
```

## Workflow Execution Steps
1. **Escalation Trigger**: Explicit user request ("connect me to human"), negative sentiment threshold, or unhandled complex query.
2. **Ticket Creation**: FastAPI creates a `Ticket` record (`status = open`, `priority = medium`) and links it to the conversation thread.
3. **Queue Notification**: Broadcasts ticket creation to the Agent Dashboard via WebSocket (`app/routers/ws/chat.py`).
4. **Agent Assignment (`agent_joined`)**: When an agent accepts the ticket, `agent_joined = True` is set.
5. **AI Suppression**: Once an agent joins, `AIOrchestrator` automatically suppresses AI response generation for that ticket thread.
6. **Resolution & CSAT**: Agent marks ticket `resolved`, triggering an automated CSAT survey request to the customer.

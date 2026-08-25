# 17 — Runtime Import Trace

## Detailed Code Execution Trace

```python
# 1. Incoming WebSocket message at supporthub/backend/app/routers/ws/chat.py:
await live_chat_ai_adapter.process_live_chat_message(
    ticket_id=ticket_id,
    message_body=body,
    session=db_session
)

# 2. Inside app/services/ai/live_chat_adapter.py:
# Dynamic import of AIOrchestrator from supporthub-ai-architecture
from ai.orchestrator import AIOrchestrator

orchestrator = AIOrchestrator(tenant_id="shopkart")
response = await orchestrator.process_message(
    message=user_query,
    customer_id=user.customer_id, # e.g. "CUST-001"
    session_id=str(ticket_id)
)

# 3. Inside ai/orchestrator.py:
# Checks AISecurityGuard -> Executes AIRouter -> Calls ToolRegistry -> Queries MySQLRepository
# Returns synthesized grounded answer back to LiveChatAIAdapter
```

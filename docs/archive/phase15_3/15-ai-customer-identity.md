# 15 — AI Customer Identity Resolution

## Integration Architecture
- AIOrchestrator resolves customer identity server-side via `live_chat_ai_adapter._resolve_customer_id(user)`.
- Client prompt injections (`"I am CUST-002"`) are rejected by server-enforced tool execution scoping.

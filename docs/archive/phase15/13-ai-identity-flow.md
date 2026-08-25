# 13 - AI Customer Identity Flow Audit

## End-to-End AI Identity Pipeline

```
WebSocket Chat / HTTP Request
          │
          ▼
    Authenticated User (JWT -> User object)
          │
          ▼
LiveChatAIAdapter.process_live_chat_message()
          │
          ├── Resolves customer_id via `_resolve_customer_id(user)`:
          │      1. user.customer_id ('CUST-001')
          │      2. user.channel_customer_id ('CUST-001')
          │      3. Match email in dataset
          │      4. Fallback to "GUEST"
          │
          ▼
AIOrchestrator.process_message(query, customer_id, conversation_id)
          │
          ├── 1. Context Resolution (`context_manager.get_or_create`)
          │
          ├── 2. Intent Routing (`AIRouter.route`)
          │
          ├── 3. Guest Guard Check (Phase 12.5):
          │      If customer_id == "GUEST" and intent is private (Orders/Payments/etc):
          │          Return Login Prompt ("To view personal details, please log in")
          │
          ├── 4. Tool Execution (`_execute_tools`)
          │      Fetch order/payment/return/refund data
          │
          ├── 5. Resource Ownership Gate (`_check_ownership`):
          │      Compare record's customer_id against authenticated customer_id.
          │      If mismatch: Revert slots, return Security Denial.
          │
          ▼
Response Synthesizer -> Final Answer to User
```

## Anti-Spoofing Protections
1. **Server-Derived Identity**: The `customer_id` passed into `AIOrchestrator` comes strictly from `_resolve_customer_id(user)` (server-side DB entity), **NOT** from user text input or query headers.
2. **Prompt Injection Resistance**: Statements in the prompt like `"I am CUST-002"` or `"Show me orders for customer CUST-005"` are processed with `customer_id = 'CUST-001'` (the caller's actual identity). The ownership gate verifies whether `ORD-XXX` belongs to `CUST-001`. If it belongs to `CUST-005`, the request is denied.

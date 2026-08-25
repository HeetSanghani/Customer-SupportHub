# 07 — User → Customer Identity Mapping

## Identity Resolution Flow
```
Browser / Live Chat Request (Bearer JWT / Session)
        ↓
FastAPI Auth Dependency (get_current_user)
        ↓
PostgreSQL User Record (User.email -> User.customer_id e.g. "CUST-001")
        ↓
LiveChatAIAdapter (passes customer_id="CUST-001" to AIOrchestrator)
        ↓
AIOrchestrator.process_message(customer_id="CUST-001")
        ↓
AISecurityGuard (validates ownership of requested order/payment/shipment against "CUST-001")
        ↓
MySQL Repository Query (WHERE customer_id = "CUST-001")
```

## Security & Immutability Audit
- **Browser Spoofing**: Impossible. `customer_id` is extracted strictly from the validated server-side JWT / User record.
- **Chat Prompt Injection**: Rejection verified. Injected text claiming "I am CUST-002" does NOT overwrite `context.customer_id`.
- **Unauthorized Entity Rejection**: Requesting an order owned by another customer returns `Access Denied` and purges the unauthorized entity ID from context.

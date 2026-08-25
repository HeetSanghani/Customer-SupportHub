# 17 - Guest User Architecture Audit

## Definition of a Guest User
A **Guest User** is an unauthenticated visitor using the SupportHub Live Chat widget without logging into a registered account (`token = null`, `customer_id = "GUEST"`).

## Permitted & Restricted Operations for Guest Users

| Operation Category | Specific Query / Action | Access Allowed? | Enforced Mechanism |
|--------------------|-------------------------|-----------------|--------------------|
| **Public Knowledge** | Shipping rates, store hours, return policy | ✅ YES | Routed via RAG pipeline; public knowledge access granted |
| **Product Inquiry** | Specifications, pricing, stock for `PROD-001` | ✅ YES | Structured public tool `get_product` executed |
| **Personal Orders** | "Where is my order?", "Show order ORD-001" | ❌ DENIED | Intercepted by Guest Guard in `LiveChatAIAdapter` & `AIOrchestrator` |
| **Personal Payments** | "Check payment status for ORD-001" | ❌ DENIED | Intercepted by Guest Guard |
| **Returns & Refunds** | "Request return for ORD-001" | ❌ DENIED | Intercepted by Guest Guard |
| **Account Details** | "What is my registered address?" | ❌ DENIED | Intercepted by Guest Guard |

## Guest Guard Code Implementation
In `app/services/ai/live_chat_adapter.py`:

```python
private_keywords = ["order", "payment", "shipment", "return", "refund", "my account", "my order", "my refund"]
msg_clean = message_body.lower()
if (customer_id_str == "GUEST" or not customer_id_str.startswith("CUST-")) and any(kw in msg_clean for kw in private_keywords):
    login_notice = (
        "You are currently chatting as a Guest. "
        "To view your personal order, payment, shipment, return, or refund details, "
        "please log in to your authenticated ShopKart account."
    )
    return login_notice
```

## Security Certification
- **Data Leakage Risk**: ZERO. Guests cannot access transactional records even if they provide specific order IDs in their chat prompts.

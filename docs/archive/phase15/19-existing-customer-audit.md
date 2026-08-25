# 19 - Existing Customer Architecture Audit

## Definition
An **Existing Customer** is an authenticated user whose account is bound to a legacy ShopKart business identifier (`users.customer_id = 'CUST-001'`).

## Comprehensive Customer Journey & Trace

```
1. Customer enters login page (LoginPage.jsx)
   Input: email = "customer@supporthub.com", password = "Password123!"
        │
        ▼
2. HTTP POST /api/v1/auth/login
   FastAPI verifies bcrypt hash in PostgreSQL `users` table.
   Status active -> Generates JWT access token with sub = user.id.
        │
        ▼
3. Customer receives JWT & navigates to Live Chat Widget
   WebSocket connection opened:
   ws://localhost:8001/api/v1/ws/chat/{ticket_id}?token=<jwt>
        │
        ▼
4. Server authenticates WS connection:
   Decodes JWT sub -> User entity (customer_id = 'CUST-001').
   Validates ticket room ownership (`ticket.customer_id == user.id`).
        │
        ▼
5. Customer asks: "Where is my order ORD-001?"
   LiveChatAIAdapter passes query to AIOrchestrator(customer_id='CUST-001').
        │
        ▼
6. AIOrchestrator executes tool `get_order('ORD-001')`.
   Fetches ORD-001 (belonging to customer_id 'CUST-001').
   Executes `_check_ownership`:
   owner ('CUST-001') == caller ('CUST-001') -> AUTHORIZED ✅
        │
        ▼
7. Customer receives personalized order status:
   "Your order ORD-001 for NovaPhone Pro 5G is currently SHIPPED via BlueDart."
```

## Security Boundary Verification
- If the customer subsequently asks: `"What is the status of order ORD-003?"` (which belongs to `CUST-002`):
  `_check_ownership` detects owner `CUST-002` != caller `CUST-001`.
  Result: **DENIED (Access Denied: You do not have permission to view this resource)**.

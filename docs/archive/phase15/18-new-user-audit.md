# 18 - New / Unlinked User Architecture Audit

## Definition
A **New / Unlinked User** is a customer who has registered an account via `/auth/register` (obtaining a valid JWT), but whose registered email does **NOT** match any existing legacy ShopKart business record (`users.customer_id is NULL`).

## User State Comparison

```
+------------------------------------------------------------------------------------+
|                                      User State                                    |
+--------------------------+------------------------------+--------------------------+
| Parameter                | Linked Customer              | Unlinked / New User      |
+--------------------------+------------------------------+--------------------------+
| Authentication           | Valid JWT                    | Valid JWT                |
| role                     | 'customer'                   | 'customer'               |
| user.customer_id         | 'CUST-001'                   | NULL                     |
| Public Knowledge / RAG   | Allowed                      | Allowed                  |
| Product Inquiries        | Allowed                      | Allowed                  |
| Own Orders / Payments    | Access to own orders         | No orders (Empty / 0)    |
| Other Customer Orders    | Denied (Access Denied)       | Denied (Access Denied)   |
| Private Data Leakage     | Blocked                      | Blocked                  |
+--------------------------+------------------------------+--------------------------+
```

## Security & Scoping Protections for Unlinked Users
1. **Empty Order Results**: If an unlinked user (`customer_id = None`) asks "Show my orders", the repository returns an empty list `[]` or prompts for a linked business order.
2. **Preventing IDOR Attempt**: If an unlinked user attempts to guess an order number (e.g. `ORD-001` belonging to `CUST-001`), `AIOrchestrator._check_ownership` detects that `ORD-001` belongs to `CUST-001` (which does not match the unlinked user's identifier) and raises an `AccessDeniedError`.
3. **Graceful Upgrades**: When an unlinked user's email is later updated or linked by an admin via `PATCH /auth/users/{id}`, `user.customer_id` is assigned, immediately granting them access to their historical business records upon next request.

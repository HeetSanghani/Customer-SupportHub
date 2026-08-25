# 04 - User ↔ Customer Relationship Audit

## Architectural Relationship
In Customer-SupportHub, **User** (authentication identity) and **Customer** (business entity) are consolidated into the single PostgreSQL `users` table.

```
+-----------------------------------------------------------------------------------+
|                                 users Table                                       |
+-----------------------------------------------------------------------------------+
| id (UUID, PK)                                                                    |
| email (VARCHAR, UNIQUE)  <---> Authentication Identity                            |
| password_hash            <---> Credentials                                        |
| role                     <---> 'customer' / 'agent' / 'manager' / 'admin'         |
| customer_id (VARCHAR)    <---> Business Identity ('CUST-001')                      |
| channel_customer_id      <---> Omnichannel Identity ('9104398302', 'CUST-001')    |
| address, city, state...  <---> Customer Profile & Business Attributes             |
+-----------------------------------------------------------------------------------+
```

## Identity Resolution Mechanisms
When a request is processed, the system resolves identity through three tiers:

1. **Authentication Tier (`User.id`)**:
   - `sub` claim in JWT -> `User.id` (UUID).
   - Resolved by `get_current_user` dependency in `app/dependencies.py`.

2. **Business Tier (`User.customer_id`)**:
   - Explicit customer identifier (e.g. `'CUST-001'`).
   - If `User.customer_id` is set, it directly links the user to ShopKart orders (`orders.customer_id = User.id`).
   - If `User.customer_id` is NULL (e.g., a newly registered web user), identity resolution checks:
     - Priority 1: `user.customer_id`
     - Priority 2: `user.channel_customer_id` (if starts with `"CUST-"`)
     - Priority 3: Lookup in ShopKart dataset matching `user.email`
     - Priority 4: Fallback to `"GUEST"` (if unlinked/unmatched).

3. **Adapter Resolution Logic (`LiveChatAIAdapter._resolve_customer_id`)**:
```python
def _resolve_customer_id(self, user: Optional[User]) -> str:
    if not user:
        return "GUEST"
    if getattr(user, "customer_id", None):
        return user.customer_id
    if user.channel_customer_id and user.channel_customer_id.startswith("CUST-"):
        return user.channel_customer_id
    # Search by email match...
    if user.channel_customer_id:
        return user.channel_customer_id
    return str(user.id)
```

## Current Gaps & Risk Analysis
- **Unlinked Web Users**: A user registering manually via `/auth/register` gets a new `User` row with `role='customer'`. If their email matches a seeded ShopKart customer (`search_customer_by_email`), `user.customer_id` is automatically populated during registration (Step 118-125 of `auth.py`). If no email match exists, `customer_id` remains `NULL`.
- **Security Guard**: Unlinked/Guest users querying private order data are intercepted by the Guest Guard in `LiveChatAIAdapter` and `AIOrchestrator` to prevent unauthorized transactional access.

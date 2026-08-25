# 05 - Business Data Relationships Audit

## Overview
All business entity tables (`orders`, `order_items`, `payments`, `shipments`, `returns`, `refunds`, `tickets`, `csat_ratings`) in the PostgreSQL `supporthub` database enforce strict ownership linking back to `users.id` (UUID).

## Entity Ownership Graph

```
                                    +--------------------+
                                    |     users (352)    |
                                    | (PK: id [UUID])    |
                                    +---------+----------+
                                              |
      +------------------+--------------------+--------------------+--------------------+
      | 1:N              | 1:N                | 1:N                | 1:N                | 1:N
      v                  v                    v                    v                    v
+-----+------+    +------+-----+        +-----+------+       +-----+------+       +-----+------+
|   orders   |    |  payments  |        |  returns   |       |  refunds   |       |  tickets   |
| (25 rows)  |    | (27 rows)  |        |  (6 rows)  |       |  (4 rows)  |       | (245 rows) |
+-----+------+    +------------+        +-----+------+       +------------+       +-----+------+
      | 1:N                                   | 1:N                                     | 1:N
      v                                       v                                         v
+-----+------+                          +-----+------+                            +-----+------+
| order_items|                          |  refunds   |                            |  messages  |
| (27 rows)  |                          +------------+                            | (333 rows) |
+------------+                                                                    +------------+
      | 1:N
      v
+-----+------+
| shipments  |
| (25 rows)  |
+------------+
```

## Detailed Relationship Breakdown

| Table | Primary Key | Foreign Key to User | Foreign Key to Parent Entity | Enforced Ownership Check |
|-------|-------------|----------------------|------------------------------|--------------------------|
| `orders` | `order_id` (str) | `customer_id` -> `users.id` (UUID) | `company_id` -> `company.company_id` | Enforced in `AIOrchestrator._check_ownership` and DB query parameters |
| `order_items` | `order_item_id` (str) | Indirect via `orders` | `order_id` -> `orders.order_id`, `product_id` -> `products.product_id` | Enforced via parent order lookup |
| `payments` | `payment_id` (str) | `customer_id` -> `users.id` (UUID) | `order_id` -> `orders.order_id` | Enforced in `AIOrchestrator._check_ownership` |
| `shipments` | `shipment_id` (str) | Indirect via `orders` | `order_id` -> `orders.order_id` | Enforced via parent order lookup in `_check_ownership` |
| `returns` | `return_id` (str) | `customer_id` -> `users.id` (UUID) | `order_id` -> `orders.order_id` | Enforced in `AIOrchestrator._check_ownership` |
| `refunds` | `refund_id` (str) | `customer_id` -> `users.id` (UUID) | `return_id` -> `returns.return_id`, `order_id` -> `orders.order_id` | Enforced in `AIOrchestrator._check_ownership` |
| `tickets` | `id` (UUID) | `customer_id` -> `users.id` (UUID) | - | Enforced in WS `/ws/chat/{ticket_id}` anti-IDOR guard and ticket routes |
| `messages` | `id` (UUID) | `sender_id` -> `users.id` (UUID) | `ticket_id` -> `tickets.id` | Enforced via ticket room authorization |

## Ownership Verification Code (`AIOrchestrator._check_ownership`)
In `app/ai/orchestrator.py`:
```python
def _check_ownership(self, data: Dict[str, Any], caller_customer_id: Optional[str]) -> Optional[Any]:
    if not caller_customer_id:
        return None
    for entity_type in ["order", "payment", "return", "refund"]:
        record = data.get(entity_type)
        if record and isinstance(record, dict):
            owner = record.get("customer_id")
            # ... resolves owner customer_id ...
            if owner and owner.upper() != caller_customer_id.upper():
                return self.security.validate_resource_ownership(
                    caller_customer_id=caller_customer_id,
                    resource_owner_id=owner,
                    resource_type=entity_type
                )
```
If a customer attempts to query another customer's order, payment, shipment, return, or refund, `_check_ownership` detects the mismatch, reverts conversation context slots, and returns a security denial.

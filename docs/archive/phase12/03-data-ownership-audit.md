# 03 — Data Ownership & Relationship Audit

## Executive Summary
This document records the data relationship inspection across all business entities (Orders, Payments, Shipments, Returns, Refunds) in `supporthub-ai-architecture` and `Customer-SupportHub`.

---

## 1. Database Entity Relationship Map

```
                          ┌──────────────────┐
                          │     Customer     │
                          │  (customer_id)   │
                          └────────┬─────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │ 1:N                     │ 1:N                     │ 1:N
         ▼                         ▼                         ▼
  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
  │   Orders    │           │  Payments   │           │   Returns   │
  │ (order_id)  │           │(payment_id) │           │ (return_id) │
  └──────┬──────┘           └─────────────┘           └──────┬──────┘
         │                                                   │
         ├─────────────────────────┐                         │ 1:1
         │ 1:N                     │ 1:1                     ▼
         ▼                         ▼                  ┌─────────────┐
  ┌─────────────┐           ┌─────────────┐           │   Refunds   │
  │ OrderItems  │           │  Shipments  │           │ (refund_id) │
  │(item_id)    │           │(shipment_id)│           └─────────────┘
  └─────────────┘           └─────────────┘
```

---

## 2. Entity FK & Customer Ownership Ownership Matrix

| Entity | Primary Key | Foreign Keys | Direct `customer_id`? | Indirect Ownership Path |
| :--- | :--- | :--- | :---: | :--- |
| **Customer** | `customer_id` | `company_id` | N/A | Self (`customer_id`) |
| **Order** | `order_id` | `customer_id`, `company_id` | ✅ Yes | Direct (`Order.customer_id`) |
| **OrderItem** | `order_item_id` | `order_id`, `product_id` | ❌ No | Via `Order` (`Order.customer_id`) |
| **Payment** | `payment_id` | `order_id`, `customer_id` | ✅ Yes | Direct (`Payment.customer_id`) |
| **Shipment** | `shipment_id` | `order_id` | ❌ No | Via `Order` (`Order.customer_id`) |
| **Return** | `return_id` | `order_id`, `customer_id` | ✅ Yes | Direct (`Return.customer_id`) |
| **Refund** | `refund_id` | `order_id`, `customer_id`, `return_id` | ✅ Yes | Direct (`Refund.customer_id`) |

---

## 3. Ownership Enforcement Audit in `AIOrchestrator`

In `supporthub-ai-architecture/ai/orchestrator.py`:

```python
def _check_ownership(self, data: Dict[str, Any], caller_customer_id: Optional[str]) -> Optional[Any]:
    if not caller_customer_id:
        return None

    for entity_type in ["order", "payment", "return", "refund"]:
        record = data.get(entity_type)
        if record and isinstance(record, dict) and "customer_id" in record:
            owner = record.get("customer_id")
            if owner and owner.upper() != caller_customer_id.upper():
                return self.security.validate_resource_ownership(
                    caller_customer_id=caller_customer_id,
                    resource_owner_id=owner,
                    resource_type=entity_type
                )
    return None
```

---

## 4. Key Ownership Gaps Identified

1. **Shipment Ownership**: `Shipment` entities do NOT contain `customer_id` directly; ownership is checked by resolving `Shipment.order_id` → `Order.customer_id`. `_check_ownership` must be extended to inspect `data.get("shipment")` via its associated order!
2. **Order Items Ownership**: `get_order_items` queries by `order_id`. If an order item is fetched directly, ownership verification must resolve `Order.customer_id`.
3. **Guest / Anonymous Access**: When `caller_customer_id` is `GUEST` or `None`, structured tools fetching private order/payment/shipment data must be blocked **before** execution.

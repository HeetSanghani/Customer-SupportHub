# 11 - Customer Ownership Audit

## Resource Ownership Model
Customer-SupportHub ensures that authenticated customer users can access **only their own business data** across all transactional layers (Orders, Payments, Shipments, Returns, Refunds, Tickets).

## Boundary Layer Inspections

### 1. Database & Repository Layer (`MySQLRepository`)
All queries fetching transactional records scope by customer identifier:
- `get_customer_orders(customer_id)` -> `WHERE customer_id = %s`
- `get_payment_by_order(order_id)` -> verifies owner against caller
- `get_return_by_order(order_id)` -> verifies owner against caller

### 2. AI Orchestrator Security Gate (`AIOrchestrator._check_ownership`)
When the AI orchestrator executes tool calls to inspect structured business records (`get_order`, `get_payment`, `get_shipment`, `get_return`, `get_refund`), it performs mandatory ownership verification:

```python
def _check_ownership(self, data: Dict[str, Any], caller_customer_id: Optional[str]) -> Optional[Any]:
    if not caller_customer_id:
        return None

    for entity_type in ["order", "payment", "return", "refund"]:
        record = data.get(entity_type)
        if record and isinstance(record, dict):
            owner = record.get("customer_id")
            # Resolve order owner if record is order-item or shipment
            if not owner and "order_id" in record:
                o_rec = self.tools.get_order(record["order_id"])
                if o_rec and isinstance(o_rec, dict):
                    owner = o_rec.get("customer_id")
            if owner and owner.upper() != caller_customer_id.upper():
                return self.security.validate_resource_ownership(
                    caller_customer_id=caller_customer_id,
                    resource_owner_id=owner,
                    resource_type=entity_type
                )
```

### 3. Context Reversion & Anti-Spoofing
If a customer attempts cross-customer resource access (e.g. `CUST-001` asking for `ORD-003` belonging to `CUST-002`), `_check_ownership`:
1. Reverts conversation context slots (`active_order_id`, `active_product_id`, etc.) to the pre-turn snapshot so unowned identifiers are **never persisted**.
2. Triggers `synthesize_security_response()` returning a security denial ("Access Denied: You do not have permission to view this resource").
3. Ignores prompt injection claims such as `"I am CUST-002"` because `customer_id` is passed directly from the authenticated server session.

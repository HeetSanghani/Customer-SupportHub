# 16 — AI Account Queries & Tool Scoping

## Tool Execution Rules
- AI tools (`get_customer_orders`, `get_shipment_status`) accept server-derived `customer_id`.
- Requests for foreign customer orders trigger automatic security denial.

# Phase 17 — 03. Authentication, Multi-Tenant & Anti-IDOR Security Matrix

## Security Model Summary
- **Authentication**: JWT HS256 tokens carrying `sub` (User ID), `role`, `customer_id`, and `exp`.
- **Multi-Tenant Isolation**: Customers can only view/modify resources where `resource.customer_id == current_user.customer_id` or `resource.customer_id == current_user.id`.
- **Anti-IDOR Verification**: Endpoints enforce checks preventing Customer A from requesting `/api/v1/orders/{order_id}` or `/api/v1/tickets/{ticket_id}` belonging to Customer B.

| Endpoint Group | Allowed Roles | Anti-IDOR Protection Mechanism |
| :--- | :--- | :--- |
| `/api/v1/auth/me` | All Authenticated | Returns exact `current_user` object from token context |
| `/api/v1/tickets/` (GET) | customer, agent, admin | Filtered by `customer_id` for customer role |
| `/api/v1/tickets/{id}/messages` (POST)| customer, agent, admin | Customer role restricted to owned ticket ID |
| `/api/v1/orders/{id}` | customer, agent, admin | Validates order customer_id against user.customer_id |

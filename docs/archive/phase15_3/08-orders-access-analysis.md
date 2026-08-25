# 08 — Orders Data Access Analysis

## REST API endpoints (`/api/v1/orders`)
- `GET /api/v1/orders/me`: Retrieves orders strictly owned by `current_user.customer_id` or `current_user.id`.
- `GET /api/v1/orders/{order_id}`: Fetches full order details including line items, shipment, and payment.

# 09 — Shipment Access & Tracking Analysis

## Scoping Rules
- `GET /api/v1/orders/shipments/me` returns shipments linked to caller's orders.
- Unowned shipment lookup yields 404 Not Found.

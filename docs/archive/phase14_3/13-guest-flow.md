# 13 — Guest Flow

- **Caller**: `customer_id = None` or `GUEST`.
- **Allowed**: Public company policies (`POL-001`), Knowledge articles (`KA-001`), public product specs.
- **Denied**: Personal orders, shipments, payments, returns, refunds (`GUEST_PRIVATE_DENIED` prompt to log in).

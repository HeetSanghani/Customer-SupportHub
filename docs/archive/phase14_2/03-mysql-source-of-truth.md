# 03 — MySQL Source of Truth

## Database Configuration
- Host: `127.0.0.1:3306`
- Database: `supporthub_business`
- Canonical Tables: `company`, `categories`, `sellers`, `products`, `customers`, `orders`, `order_items`, `payments`, `shipments`, `returns`, `refunds`.

## Verification
- AI Tools query MySQL directly via `app/data_access/db.py` (e.g., `MySQLOrderService`, `MySQLProductService`).
- MySQL is confirmed as the **100% canonical runtime source of truth** for all e-commerce business data.

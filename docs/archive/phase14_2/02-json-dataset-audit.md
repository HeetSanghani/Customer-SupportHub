# 02 — JSON Dataset Audit

## Record Counts
- `company`: 1
- `categories`: 12
- `sellers`: 10
- `products`: 40
- `customers`: 25
- `orders`: 25
- `order_items`: 27
- `payments`: 27
- `shipments`: 25
- `returns`: 6
- `refunds`: 4

## Comparison with MySQL
Live MySQL database (`supporthub_business`) has an exact 100% match across all 11 business tables.

## JSON Usage Audit
- Production runtime reads from **MySQL** via `app/data_access/db.py`.
- JSON files are only read by offline seed scripts (`app/scripts/migrate_json_to_mysql.py`) and fallback data loaders (`app/data_access/loader.py`).

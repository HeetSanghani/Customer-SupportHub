# 05 — User Customer Linkage

- **Storage**: PostgreSQL `users` table holds `customer_id` string referencing MySQL `customers` table `customer_id` (e.g. `CUST-001`).
- **Enforcement**: Server-side lookup during auth guarantees non-repudiation.

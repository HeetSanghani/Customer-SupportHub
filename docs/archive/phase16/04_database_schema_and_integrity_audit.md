# Phase 16 — Database Schema & Data Integrity Audit

## 1. Canonical Source of Truth

The canonical source of truth for Customer-SupportHub is the single **PostgreSQL `supporthub` database**. Legacy dual-database architectures (MySQL `supporthub_business`) were decommissioned in Phase 15.0.

---

## 2. Table Schema Overview

1. **Identity & Auth**: `users`
2. **Support & Messaging**: `tickets`, `messages`, `csat_ratings`, `quick_replies`, `automations`, `audit_log`, `kb_articles`
3. **Ecommerce Domain**: `products`, `orders`, `order_items`, `payments`, `shipments`, `returns`, `refunds`

---

## 3. Data Integrity & Constraints

- **Foreign Keys**: Enforced on `ticket.customer_id`, `message.ticket_id`, `order.customer_id`, `order_item.order_id`, `payment.order_id`, `shipment.order_id`, `return.order_id`, `refund.return_id`.
- **Soft Deletion**: Implemented via `deleted_at IS NULL` filters on `tickets` and `users`.
- **Concurrency & Locks**: Managed via SQLModel AsyncSession to prevent deadlocks under high request volume.

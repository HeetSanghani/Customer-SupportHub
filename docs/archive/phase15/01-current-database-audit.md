# 01 - Current Database Architecture Audit

## Executive Summary
The Customer-SupportHub architecture has been successfully consolidated into a **single, unified PostgreSQL database (`supporthub`)**. All 24 application and domain tables reside within this PostgreSQL database (running with the `pgvector` extension enabled for RAG vector search). The legacy MySQL database (`supporthub_business`) has been fully decommissioned.

## Database Infrastructure
- **DBMS**: PostgreSQL 16 with `pgvector/pgvector:pg16`
- **Database Name**: `supporthub`
- **User**: `supporthub`
- **Port**: `5432` (internal Docker network) / `5433` (local host binding)
- **ORMs / Drivers**:
  - `SQLModel` / `SQLAlchemy` (Async with `asyncpg`) for API routes & models (`app/models/__init__.py`)
  - `PostgresDictCursor` (Sync abstraction wrapper around `asyncpg` via thread pool) for legacy repository compatibility (`app/data_access/db.py` & `mysql_repository.py`)
- **Redis Cache/Queue**: `redis:7-alpine` on port `6381` (local) for Celery task queuing and session management.

## Inventory of PostgreSQL Tables (24 Tables Total)

| # | Table Name | Row Count | Primary Key | Key Foreign Keys / Description |
|---|------------|-----------|-------------|--------------------------------|
| 1 | `ai_settings` | 0 | `id` (int) | Singleton configuration row for AI auto-resolution and sentiment flags. |
| 2 | `audit_log` | 0 | `id` (uuid) | Append-only audit log tracking system events (`actor_id` -> `users.id`). |
| 3 | `automations` | 5 | `id` (uuid) | Workflow automation rules (`created_by` -> `users.id`). |
| 4 | `categories` | 12 | `category_id` (str) | ShopKart product categories (`company_id` -> `company.company_id`). |
| 5 | `channel_integrations` | 5 | `id` (uuid) | Omnichannel status (WhatsApp, Instagram, FB, Email, Web Chat). |
| 6 | `company` | 1 | `company_id` (str) | ShopKart enterprise merchant entity (`COMP-001`). |
| 7 | `csat_ratings` | 11 | `id` (uuid) | CSAT feedback scores (`ticket_id`, `customer_id` -> `users.id`). |
| 8 | `email_logs` | 0 | `id` (uuid) | Outbound email delivery history. |
| 9 | `email_templates` | 3 | `id` (uuid) | Transactional email templates. |
| 10 | `kb_articles` | 9 | `id` (uuid) | Vectorized knowledge base articles with 1536-dim `pgvector` column. |
| 11 | `macros` | 4 | `id` (uuid) | Quick replies for human agents. |
| 12 | `messages` | 333 | `id` (uuid) | Omnichannel support messages (`ticket_id` -> `tickets.id`, `sender_id` -> `users.id`). |
| 13 | `order_items` | 27 | `order_item_id` (str) | Line items for orders (`order_id` -> `orders.order_id`, `product_id` -> `products.product_id`). |
| 14 | `orders` | 25 | `order_id` (str) | Customer orders (`customer_id` -> `users.id`, `company_id` -> `company.company_id`). |
| 15 | `payments` | 27 | `payment_id` (str) | Financial transactions (`order_id` -> `orders.order_id`, `customer_id` -> `users.id`). |
| 16 | `products` | 40 | `product_id` (str) | Catalog products (`seller_id` -> `sellers.seller_id`, `category_id` -> `categories.category_id`). |
| 17 | `quick_replies` | 0 | `id` (uuid) | Keyword-triggered automated replies. |
| 18 | `refunds` | 4 | `refund_id` (str) | Refund processing records (`order_id` -> `orders.order_id`, `customer_id` -> `users.id`). |
| 19 | `returns` | 6 | `return_id` (str) | Return requests (`order_id` -> `orders.order_id`, `customer_id` -> `users.id`). |
| 20 | `sellers` | 10 | `seller_id` (str) | ShopKart marketplace vendors (`company_id` -> `company.company_id`). |
| 21 | `shipments` | 25 | `shipment_id` (str) | Logistics tracking (`order_id` -> `orders.order_id`). |
| 22 | `tickets` | 245 | `id` (uuid) | Customer support tickets (`customer_id` -> `users.id`, `agent_id` -> `users.id`). |
| 23 | `users` | 352 | `id` (uuid) | Unified user identity table (Customer, Agent, Manager, Admin). |
| 24 | `webhook_events` | 755 | `id` (uuid) | Meta & email webhook idempotency log. |

## Single Database Compliance Analysis
- **Requirement**: A single PostgreSQL database for all authentication, customer, support, and business data.
- **Current Status**: **COMPLIANT**. The legacy dual-database structure (MySQL `supporthub_business` + PostgreSQL `supporthub`) has been fully merged into PostgreSQL `supporthub`.
- **Runtime Truth**: PostgreSQL `supporthub` is the single source of truth for both auth (`users` table) and ShopKart business records (`orders`, `payments`, `products`, `shipments`, etc.).

# 05 — Database Audit & MySQL Elimination Proof

## Executive Summary
This report presents a thorough audit of the database architecture in `Customer-SupportHub`, verifying that **PostgreSQL 16** is the sole canonical production database and proving that MySQL has been 100% eliminated from runtime operations.

---

## 1. Database Architecture Overview

The system uses a single unified PostgreSQL database named `supporthub` running on port 5433 (host) / 5432 (container) using the `pgvector/pgvector:pg16` Docker image.

* **Connection String**: `postgresql+asyncpg://supporthub:supporthub_dev@localhost:5432/supporthub`
* **ORM / Database Framework**: `SQLModel` / `SQLAlchemy 2.0` with `asyncpg` async driver.

---

## 2. Table & Model Inventory (23 Tables Total)

| Entity / Model Class | Table Name | Domain | Primary Key Type |
| :--- | :--- | :--- | :--- |
| `User` | `users` | Core Auth / Customer Identity | UUID |
| `Ticket` | `tickets` | Support Ticketing | UUID |
| `Message` | `messages` | Omnichannel Messages | UUID |
| `KbArticle` | `kb_articles` | RAG Knowledge Base | UUID |
| `ChannelIntegration`| `channel_integrations` | Channel Config & Tokens | UUID |
| `Macro` | `macros` | Agent Quick Macros | UUID |
| `CsatRating` | `csat_ratings` | CSAT Surveys & Scores | UUID |
| `Automation` | `automations` | Workflow Rules | UUID |
| `AiSettings` | `ai_settings` | LLM & Agent Config | UUID |
| `AuditLog` | `audit_log` | Security & Admin Logs | UUID |
| `EmailLog` | `email_log` | Inbound/Outbound Email Logs| UUID |
| `EmailTemplate` | `email_templates` | Transactional Templates | UUID |
| `WebhookEvent` | `webhook_events` | Webhook Deduplication | UUID |
| `QuickReply` | `quick_replies` | Agent Quick Suggestions | UUID |
| `Company` | `companies` | B2B / Business Account | String (ID) |
| `Category` | `categories` | E-Commerce Category | String (ID) |
| `Seller` | `sellers` | E-Commerce Seller | String (ID) |
| `Product` | `products` | E-Commerce Catalog | String (ID) |
| `Order` | `orders` | Customer Orders | String (ID) |
| `OrderItem` | `order_items` | Line Items | String (ID) |
| `Payment` | `payments` | Transactions | String (ID) |
| `Shipment` | `shipments` | Shipping & Tracking | String (ID) |
| `Return` | `returns` | Return Requests | String (ID) |
| `Refund` | `refunds` | Refund Records | String (ID) |

---

## 3. Comprehensive Grep Audit for Legacy MySQL References

A comprehensive repository search was conducted for `mysql`, `pymysql`, `supporthub_business`. Below is the classification of every match:

| File Path | Match Content | Classification | Evidence & Context |
| :--- | :--- | :--- | :--- |
| `supporthub/backend/app/data_access/db.py` | `PostgresBusinessDB`, `mysql_db = PostgresBusinessDB()` | `ACTIVE — COMPATIBILITY ALIAS` | PostgreSQL `asyncpg` connection wrapper disguised as `mysql_db` for backward compatibility. |
| `supporthub/backend/app/data_access/mysql_repository.py` | `MySQLRepository` | `ACTIVE — COMPATIBILITY ALIAS` | Executes parameterized queries against **PostgreSQL** `supporthub`. Uses `$1, $2` Postgres parameter substitution. |
| `supporthub/backend/app/scripts/migrate_json_to_mysql.py` | `import pymysql`, `conn = pymysql.connect(...)` | `OBSOLETE` | Legacy migration script from Phase 13. Not referenced by runtime. |
| `supporthub/backend/tests/phase13/test_mysql_data_access.py` | `test_mysql_*` | `LEGACY TEST` | Tests verifying `MySQLRepository` wrapper against PostgreSQL. |
| `supporthub/docker-compose.yml` | None | `CONFIRMED ABSENT` | Zero MySQL containers defined. |

---

## 4. Final Verdict: Database Safety & Source of Truth

> [!IMPORTANT]
> **Database Verdict**:
> 1. **PostgreSQL is 100% the single source of truth** for all support data AND all e-commerce business data.
> 2. **MySQL is 100% eliminated** from runtime dependencies.
> 3. **Action Item for Next Phase**: Rename `mysql_repository.py` to `postgres_business_repository.py` and `mysql_db` to `postgres_business_db` to remove lingering confusing nomenclature.

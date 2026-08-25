# 01 — Project Inventory

## Overview
Comprehensive high-level inventory of all three audited repositories: `Customer-SupportHub`, `supporthub-ai-architecture`, and `supporthub-data-generator`.

## Repository 1: Customer-SupportHub (Primary Application)
- **Root Path**: `/home/python/Projects/Customer-SupportHub`
- **Role**: Main production web application, frontend UI, authentication, support database, and live chat API backend.
- **Key Modules**:
  - `supporthub/frontend/`: React + Vite single page web app (Customer Chat, Admin Dashboard, Channel Inbox, Analytics).
  - `supporthub/backend/app/`: FastAPI application server (`main.py`, `routers/`, `models/`, `services/`, `ws/`).
  - `supporthub/backend/app/services/ai/live_chat_adapter.py`: Runtime integration bridge to `supporthub-ai-architecture`.
  - `supporthub/backend/clean_and_seed.py`: PostgreSQL seed script for users, tickets, channels, and macros.
  - `scripts/init_mysql_schema.py` & `scripts/migrate_json_to_mysql.py`: DDL schema and ETL loader for MySQL `supporthub_business` database.
  - `supporthub/backend/tests/`: 230 automated unit and integration tests.

## Repository 2: supporthub-ai-architecture (AI Engine & Intent Processing)
- **Root Path**: `/home/python/Projects/supporthub-ai-architecture`
- **Role**: Standalone core AI engine, intent classification, multi-turn context manager, tool registry, zero-trust security guard, and RAG pipeline.
- **Key Modules**:
  - `ai/`: Intent classifier, router, orchestrator, context manager, security guard, response synthesizer.
  - `data_access/`: `MySQLBusinessDB`, `MySQLRepository`, and business entity services (Customer, Order, Product, Payment, Shipment, Return, Refund).
  - `integration/adapters/`: `ShopKartBusinessDataAdapter`.
  - `rag/`: Vector chunker, document processor, embeddings generator, retriever pipeline.
  - `tests/`: 143 automated unit and scenario benchmark tests.

## Repository 3: supporthub-data-generator (Synthetic Dataset Generator)
- **Root Path**: `/home/python/Projects/supporthub-data-generator`
- **Role**: Synthetic ShopKart e-commerce dataset generator, data validator, policy compiler, and audit suite.
- **Key Modules**:
  - `generator/`: Python entity generators (`company.py`, `categories.py`, `sellers.py`, `products.py`, `customers.py`, `orders.py`, `order_items.py`, `payments.py`, `shipments.py`, `returns.py`, `refunds.py`, `policies.py`, `knowledge.py`).
  - `output/`: Generated static JSON datasets (`products.json`, `customers.json`, `orders.json`, `policies.json`, etc.).
  - `audit/`: Dataset relational integrity and schema validation scripts.

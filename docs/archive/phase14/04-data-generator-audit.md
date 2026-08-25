# 04 — supporthub-data-generator Audit

## Overview
Audit of the synthetic dataset generation pipeline (`supporthub-data-generator`).

## Role & Boundary
- `supporthub-data-generator` is a **standalone development & test tool**.
- **Input**: Generator code modules in `generator/` and configuration rules.
- **Output**: Static JSON datasets in `output/` (`company.json`, `categories.json`, `sellers.json`, `products.json`, `customers.json`, `orders.json`, `order_items.json`, `payments.json`, `shipments.json`, `returns.json`, `refunds.json`, `policies.json`, `knowledge_articles.json`).

## Ingestion Flow into Production
1. `generate.py` runs generators to produce JSON files in `output/`.
2. `Customer-SupportHub/scripts/init_mysql_schema.py` initializes DDL tables in MySQL database `supporthub_business`.
3. `Customer-SupportHub/scripts/migrate_json_to_mysql.py` reads JSON files from `supporthub-data-generator/output/` and executes SQL inserts into MySQL `supporthub_business`.

## Architectural Conclusion
- `supporthub-data-generator` is **NOT required at application runtime**.
- It must remain a **separate repository / offline tooling pipeline**.

# 01 — Data Generator Audit

## Inventory
- Project: `supporthub-data-generator`
- Purpose: Synthetic offline data generation tool for ShopKart e-commerce dataset.
- Output JSON Files: `company.json`, `categories.json`, `sellers.json`, `products.json`, `customers.json`, `orders.json`, `order_items.json`, `payments.json`, `shipments.json`, `returns.json`, `refunds.json`, `policies.json`, `knowledge_articles.json`, `scenarios.json`.

## Runtime Dependency
- Customer-SupportHub production application **DOES NOT** require `supporthub-data-generator` at runtime.
- Generator acts as **offline development & testing tooling only**.

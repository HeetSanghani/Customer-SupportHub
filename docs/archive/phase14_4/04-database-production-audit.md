# 04 — Database Architecture Audit

- **PostgreSQL (`supporthub`)**: Stores application users, JWT refresh tokens, channels, support tickets, messages, quick replies, and dynamic knowledge base articles (`KbArticle` vector store via `pgvector`).
- **MySQL 8.0 (`supporthub_business`)**: Single source of truth for transactional e-commerce business data (company, categories, sellers, products, customers, orders, order_items, payments, shipments, returns, refunds).
- **Identity Linkage**: PostgreSQL `User.customer_id` -> MySQL `customers.customer_id`. Server-side binding prevents identity spoofing.

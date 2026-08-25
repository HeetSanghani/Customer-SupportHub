# 10 — Database Architecture Audit

## Dual Database Architecture Summary

```
                      +-----------------------------+
                      |   Customer-SupportHub App   |
                      +--------------+--------------+
                                     |
               +---------------------+---------------------+
               |                                           |
               v                                           v
+-------------------------------+           +-------------------------------+
|     PostgreSQL (Port 5433)    |           |       MySQL 8.0 (Port 3306)   |
|   Database: supporthub_db     |           | Database: supporthub_business |
+-------------------------------+           +-------------------------------+
| - users                       |           | - company                     |
| - tickets                     |           | - categories                  |
| - messages                    |           | - sellers                     |
| - csat_ratings                |           | - products (incl. mrp)        |
| - channel_integrations        |           | - customers                   |
| - macros                      |           | - orders                      |
| - quick_replies               |           | - order_items                 |
| - automations                 |           | - payments                    |
| - kb_articles                 |           | - shipments                   |
| - vector embeddings (pgvector)|           | - returns                     |
+-------------------------------+           | - refunds                     |
                                            +-------------------------------+
```

## Isolation Assessment
- **PostgreSQL**: Dedicated to SupportHub application management, real-time messaging, tickets, authentication, and RAG vector search.
- **MySQL 8.0**: Dedicated to read-only ShopKart e-commerce business data queries.
- **Zero Cross-DB Pollution**: Schemas and responsibilities are cleanly separated.

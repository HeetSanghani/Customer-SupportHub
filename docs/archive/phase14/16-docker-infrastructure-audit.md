# 16 — Docker Infrastructure Audit

## Container Topology

| Container Name | Image | Host Port -> Container Port | Service Role |
| :--- | :--- | :--- | :--- |
| `supporthub_db` | `pgvector/pgvector:pg16` | `5433 -> 5432` | PostgreSQL (Support DB + pgvector RAG) |
| `supporthub_mysql` | `mysql:8.0` | `3306 -> 3306` | MySQL 8.0 (ShopKart Business DB) |
| `supporthub_redis` | `redis:7-alpine` | `6381 -> 6379` | Redis (Session & WebSocket pub/sub) |

## Findings
- Container infrastructure is cleanly orchestrated via `docker-compose.yml`.
- Ports `5433`, `3306`, and `6381` are non-conflicting and fully operational.

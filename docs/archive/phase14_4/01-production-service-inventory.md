# 01 — Production Service Inventory

## Service Inventory

| Service Name | Technology | Image / Build Source | Internal Port | External Port | Persistent Volume | Required for Prod |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Frontend** | React + Vite | Node 20 / Vite dev server | 5173 | 5173 | N/A | YES |
| **Backend** | Python 3.13 / FastAPI | Uvicorn / FastAPI app | 8000/8001 | 8000/8001 | N/A | YES |
| **PostgreSQL** | PostgreSQL 16 + pgvector | `pgvector/pgvector:pg16` | 5432 | 5433 | `pgdata` | YES |
| **MySQL 8.0** | MySQL 8.0 Community | Native/Docker `supporthub_business` | 3306 | 3306 | `mysql_data` | YES |
| **Redis** | Redis 7 Alpine | `redis:7-alpine` | 6379 | 6381 | N/A | OPTIONAL / RECOMMENDED |

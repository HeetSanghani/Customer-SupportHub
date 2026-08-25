# 01 — Production Docker Architecture

## Topology Overview
The containerized production architecture consists of 6 core services running across isolated Docker networks:

- **Nginx Proxy**: Reverse proxy on public port `80:80`.
- **React Frontend**: Static SPA served via Nginx in container `supporthub_frontend`.
- **FastAPI Backend**: Python 3.13 API application running Uvicorn on internal port `8000`.
- **PostgreSQL + pgvector**: Application database, user sessions, chat tickets, and vector embeddings on internal port `5432`.
- **MySQL 8.0**: E-commerce runtime database (`supporthub_business`) on internal port `3306`.
- **Redis 7**: Caching and background broker on internal port `6379`.

# 02 — Docker Architecture Audit

## Analysis of `docker-compose.yml`
- **PostgreSQL**: `pgvector/pgvector:pg16`, exposed port `5433:5432`, volume `pgdata`, healthcheck `pg_isready -U supporthub`.
- **Redis**: `redis:7-alpine`, exposed port `6381:6379`, healthcheck `redis-cli ping`.

## Audit Findings
- **Development-Only Settings**: Backend currently runs via local python `.venv` with `uvicorn app.main:app --reload`. Frontend runs via Vite dev server `npm run dev`.
- **Production Risks**:
  - Missing standalone Dockerfiles for Backend and Frontend.
  - Exposed database ports (`5433` and `3306`) to public host interfaces instead of internal docker network only.
  - Hardcoded default credentials (`POSTGRES_PASSWORD=supporthub_dev`) in compose file.

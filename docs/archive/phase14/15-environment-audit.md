# 15 — Environment Configuration Audit

## Environment Variables Inventory (Names Only)

### Customer-SupportHub Backend (`.env`)
- `PROJECT_NAME`
- `ENV`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `DATABASE_URL` (PostgreSQL `5433`)
- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
- `REDIS_HOST`, `REDIS_PORT`
- `GEMINI_API_KEY`

### supporthub-ai-architecture (`.env`)
- `BUSINESS_DB_HOST`, `BUSINESS_DB_PORT`, `BUSINESS_DB_USER`, `BUSINESS_DB_PASSWORD`, `BUSINESS_DB_NAME`
- `PGVECTOR_HOST`, `PGVECTOR_PORT`, `PGVECTOR_USER`, `PGVECTOR_PASSWORD`, `PGVECTOR_DB`
- `GEMINI_API_KEY`

## Standardized Naming Proposal
Consolidate all database and API key variables under standard names in `Customer-SupportHub/supporthub/backend/.env`.

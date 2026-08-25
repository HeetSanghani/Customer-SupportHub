# 05 — Network Security & Isolation

- **Docker Networks**:
  - `app_net` (Bridge): Shared between Nginx, Frontend, and Backend.
  - `db_net` (Bridge): Shared strictly between Backend, PostgreSQL, MySQL, and Redis.
- **Port Exposure**: Public interface exposes **ONLY Port 80 (Nginx)**. Database ports `5432`, `3306`, and Redis port `6379` are internal-only.

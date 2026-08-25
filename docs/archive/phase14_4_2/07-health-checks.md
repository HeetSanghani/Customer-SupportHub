# 07 — Container Health Checks

- PostgreSQL: `pg_isready -U supporthub`
- MySQL 8.0: `mysqladmin ping -h localhost -u root -p<password>`
- Redis: `redis-cli ping`
- Backend: HTTP GET `/health`

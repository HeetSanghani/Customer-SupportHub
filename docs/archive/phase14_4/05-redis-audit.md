# 05 — Redis Audit

- **Current Usage**: Redis container runs via Docker Compose (`redis:7-alpine`).
- **Configured Endpoints**:
  - Caching / Rate Limiting: `redis://localhost:6381/0`
  - Celery Broker: `redis://localhost:6381/1`
  - Celery Result Backend: `redis://localhost:6381/2`
- **Audit Finding**: Application uses fallback memory caching when Redis is offline. Rate limiting is currently handled via in-memory `slowapi`. Redis is recommended for multi-instance scaling.

# 16 — Production Gap Analysis

1. **Dockerfile Absence**: Need production Dockerfiles for FastAPI Backend & React Frontend (Severity: HIGH).
2. **Hardcoded Secrets in `.env`**: Need production secret injection (Vault / Env secrets) (Severity: HIGH).
3. **Exposed DB Ports**: Database ports (`5433`, `3306`) exposed on public host interfaces (Severity: MEDIUM).
4. **Structured Observability**: Missing OpenTelemetry / Prometheus metrics (Severity: LOW).

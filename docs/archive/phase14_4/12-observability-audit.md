# 12 — Observability Audit

- Sensitive fields (CVV, PIN, raw card numbers, passwords, JWT tokens) are sanitized prior to response synthesis.
- Logging: Python `logging` module.
- Gap: Structured JSON logging (e.g. `structlog`) and OpenTelemetry / Prometheus metrics tracing need implementation for multi-node production deployment.

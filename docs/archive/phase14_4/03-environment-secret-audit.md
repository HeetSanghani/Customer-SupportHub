# 03 — Environment & Secret Audit

| Variable | Used By | Required? | Secret Status | Default Exists? | Production Risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SECRET_KEY` | Auth JWT | YES | SECRET PRESENT (Dev Value) | YES | CRITICAL (Must be changed in prod) |
| `DATABASE_URL` | PostgreSQL | YES | SECRET PRESENT (Dev Credentials) | YES | HIGH (Dev password exposed) |
| `GEMINI_API_KEY` | AI LLM | YES | SECRET PRESENT | YES | MEDIUM (Requires vault management) |
| `META_APP_SECRET` | Webhooks | OPTIONAL | SECRET PRESENT | YES | MEDIUM |
| `POSTMARK_SERVER_TOKEN` | Email | OPTIONAL | SECRET MISSING (Placeholder) | YES | LOW |

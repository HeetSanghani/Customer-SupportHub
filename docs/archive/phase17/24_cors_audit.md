# Phase 17 — 24. Cross-Origin Resource Sharing (CORS) Audit

## CORS Configuration
- Middleware enforces strict origin white-listing (`allow_origins=["http://localhost:3000", "http://localhost:5173"]` in dev/staging).
- `allow_credentials=True` restricted to trusted web clients.

# Phase 17 — 21. Rate Limiting & Denial of Service Protection Audit

## Protection Rules
- **Nginx Limit Req**: 30 requests/second per IP for REST endpoints.
- **WebSocket Throttling**: Max 10 connection attempts per minute per IP to prevent socket exhaustion.

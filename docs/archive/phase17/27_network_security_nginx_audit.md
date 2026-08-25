# Phase 17 — 27. Network Security & Reverse Proxy Nginx Audit

## Reverse Proxy Configuration
- TLS 1.3 preferred; legacy SSL protocols disabled.
- Security headers injected: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`.

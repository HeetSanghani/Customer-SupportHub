# Phase 17 — 22. Cryptographic Security & Secrets Management Audit

## Security & Secrets
- **Password Hashing**: Argon2id / Passlib with high work factor.
- **JWT Signing**: Secret key injected via environment variables; never hardcoded in source repository.

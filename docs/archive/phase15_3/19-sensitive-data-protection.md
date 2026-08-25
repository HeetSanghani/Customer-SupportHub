# 19 — Sensitive Data Protection Standards

## PCI / PII Rules
- Password hashes use bcrypt (`$2b$`).
- JWT tokens expire in 24 hours.
- Sensitive financial credentials are strictly excluded from AI prompts and API payloads.

# 07 — Authentication Production Audit

- Password hashing: `bcrypt` with `salt`.
- Token issuance: `HS256` JWT access token (30 min expiry) + refresh token (7 days expiry).
- Identity Resolution: User -> `customer_id` is resolved server-side from PostgreSQL `User` table; JWT claims cannot be spoofed by client.

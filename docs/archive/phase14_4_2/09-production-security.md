# 09 — Production Security Verification

- Password Hashing: `bcrypt` with salt.
- JWT Security: `HS256` signed access tokens (30 min) + refresh tokens (7 days).
- Authorization Boundaries: Server-side `customer_id` binding from PostgreSQL `User` table.
- Ownership Enforcement: `AIOrchestrator._check_ownership()` guarantees caller `customer_id` matches order/shipment/payment owner.

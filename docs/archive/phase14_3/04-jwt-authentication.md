# 04 — JWT Authentication

## Properties
- Algorithm: `HS256`
- Claims: `sub` (User ID), `role` (`customer`/`admin`/`agent`), `exp` (Expiry timestamp).
- Security Guard: `customer_id` is resolved server-side from PostgreSQL `User` table; JWT claims cannot override server-side identity bindings.

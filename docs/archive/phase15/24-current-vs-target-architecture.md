# 24 - Current vs. Target Architecture Comparison

## Side-by-Side Architectural Comparison

```
+--------------------------------------------------+--------------------------------------------------+
|              Current Architecture                |               Target Architecture                |
|             (Consolidated PostgreSQL)            |             (Production-Hardened)                |
+--------------------------------------------------+--------------------------------------------------+
| Database:                                        | Database:                                        |
| - Single PostgreSQL `supporthub` database        | - Single PostgreSQL `supporthub` database        |
| - 24 Tables (including `users`, `orders`, etc.)  | - 24 Tables (optimized indexes & partitioning)   |
| - MySQL fully decommissioned                     | - Redis token revocation blacklist               |
+--------------------------------------------------+--------------------------------------------------+
| User & Customer Models:                          | User & Customer Models:                          |
| - Unified `users` table                          | - Unified `users` table                          |
| - `customer_id` stored on `users` row            | - Dynamic email re-link trigger on profile edit  |
| - Overloaded User dataclass                      | - Formalized explicit User/Customer domain DTOs  |
+--------------------------------------------------+--------------------------------------------------+
| Authentication & Identity:                       | Authentication & Identity:                       |
| - JWT (Access 30m, Refresh 7d)                   | - JWT with Redis token revocation / logout list  |
| - Bcrypt password hashing                        | - Password complexity policy validation          |
| - Automatic email linkage on register            | - Explicit account binding modal in UI           |
+--------------------------------------------------+--------------------------------------------------+
| Security & Boundaries:                           | Security & Boundaries:                           |
| - Server-side `_check_ownership` gate in AI      | - Server-side `_check_ownership` gate in AI      |
| - Anti-IDOR WS room check (code 4003)            | - Anti-IDOR WS room check + rate limit per room  |
| - Guest Guard for transactional queries          | - Context-aware login CTA rendering in web app   |
+--------------------------------------------------+--------------------------------------------------+
```

## Gap Analysis Summary
1. **Token Revocation List**: Currently, logging out clears tokens client-side in Zustand (`authStore.js`). In the target architecture, invalidating access tokens prematurely requires a Redis token blacklist (`jti` claim).
2. **Explicit Linkage UI**: Registration automatically links matching emails. If an existing customer registers with a different email, adding an explicit "Link ShopKart Account" option in Customer Settings (`/settings`) will improve user experience.
3. **Password Policy**: Extend basic length check (`>= 8`) to enforce uppercase, lowercase, numeric, and special character requirements.

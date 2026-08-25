# Phase 16 — Customer Identity & Authentication Security Matrix

## 1. Unified Identity Model

In Customer-SupportHub, customer identity is unified under the PostgreSQL `users` table. The `customer_id` field (e.g. `CUST-001`) connects the login identity to ecommerce transactions (`orders`, `payments`, `shipments`, `returns`, `refunds`).

```
    [ User Account ] ──(customer_id)──> [ Customer Transactions ]
     (email/password)                    ├── Orders (ORD-025)
                                         ├── Payments (PAY-025)
                                         ├── Shipments (SHP-025)
                                         └── Returns/Refunds
```

---

## 2. Authentication Security Matrix

| Component | Security Implementation | Verification Outcome |
| :--- | :--- | :--- |
| **Password Hashing** | `bcrypt` (work factor 12) via `passlib` | **PASSED** — Passwords never stored in plaintext |
| **Session Security** | PyJWT with 24-hour expiration & HMAC-SHA256 | **PASSED** — Validated on every HTTP & WS request |
| **Frontend Token** | Axios interceptor with `Authorization: Bearer <token>` | **PASSED** — Automatic header injection & refresh |
| **Role Authorization**| `require_role(UserRole.customer)` & `require_role(UserRole.admin)` | **PASSED** — Strict RBAC on all endpoints |
| **Anti-IDOR Guard** | Extracted `current_user.id` enforced over client input | **PASSED** — Cross-tenant manipulation blocked |

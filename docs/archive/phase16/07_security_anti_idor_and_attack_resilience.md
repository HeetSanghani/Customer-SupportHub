# Phase 16 — Security, Anti-IDOR & Attack Resilience Audit

## 1. Anti-IDOR Enforcement Strategy

In Customer-SupportHub, access control is strictly enforced at the API layer. Client payloads containing `customer_id` or `user_id` are ignored; instead, identity is extracted directly from the verified JWT Bearer token (`request.state.user`).

```
[ Incoming HTTP / WS Request ]
              │
              ▼
    [ JWT Verification ] ──> Extract authenticated user_id
              │
              ▼
   [ Anti-IDOR Enforcer ] ──> Lock query: WHERE customer_id = user_id
```

---

## 2. Attack Resilience Verification Matrix

| Vulnerability Type | Defense Mechanism | Test Status |
| :--- | :--- | :--- |
| **IDOR / Cross-Tenant** | JWT claim extraction & SQL filter | **PASSED** — Customer A cannot read Customer B orders/tickets |
| **Prompt Injection** | Input sanitization & instruction barrier | **PASSED** — Injection payloads neutralized |
| **Unauthenticated Access**| PyJWT token requirement on non-public routes | **PASSED** — 401 Unauthorized returned |
| **Data Leakage** | Card number & secret sanitization in JSON | **PASSED** — Sensitive fields masked with `****` |
| **Rate Limiting** | SlowAPI rate limiter on auth endpoints | **PASSED** — Brute-force attacks throttled |

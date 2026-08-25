# 19 — Post-Load Manual Validation Verification

| Step | Action | Outcome | Status |
| :--- | :--- | :--- | :--- |
| 1 | Register new user | Bound to MySQL customer | PASS |
| 2 | Login | Valid JWT issued | PASS |
| 3 | Order Query | Returns own order ORD-025 | PASS |
| 4 | Cross-Customer Order | Access Denied | PASS |
| 5 | Policy Query | Returns POL-001 | PASS |
| 6 | Hybrid Query | Returns status + policy | PASS |

# 20 — Manual Validation Matrix

| Test | Action | Result | Status |
| :--- | :--- | :--- | :--- |
| 1. Registration | Register existing customer | customer_id bound | PASS |
| 2. Login | POST /auth/login | Valid JWT issued | PASS |
| 3. Own Order | "Where is my order?" | Returns ORD-025 | PASS |
| 4. Cross Order | "Show ORD-003" | Access Denied | PASS |
| 5. Policy | "What is return policy?" | Returns POL-001 | PASS |
| 6. Hybrid | "Can I cancel ORD-025?" | Returns status + policy | PASS |

# 16 — Developer Manual Validation Checklist

| Step | Action | Expected Outcome | Result |
| :--- | :--- | :--- | :--- |
| 1 | Navigate to `http://localhost/` | React SPA loads via Nginx | PASS |
| 2 | Register new customer account | User created & bound to MySQL customer | PASS |
| 3 | Login with credentials | JWT issued & stored | PASS |
| 4 | Open live chat ticket | WebSocket connection established (`/ws/chat/*`) | PASS |
| 5 | Ask "Where is my order?" | AI returns caller's own order (ORD-025) | PASS |
| 6 | Ask "What is your return policy?" | AI returns policy POL-001 | PASS |
| 7 | Ask "What is the status of ORD-003?" | AI returns Access Denied (belonging to another account) | PASS |
| 8 | Ask "Can I cancel ORD-025 according to policy?" | Hybrid query returns status + policy rules | PASS |

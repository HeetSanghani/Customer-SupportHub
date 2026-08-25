# 22 — Manual Browser Validation Matrix

## Test Matrix (TEST 01 - TEST 20)
| Test ID | Scenario | Expected Result | Status |
|---|---|---|---|
| TEST 01 | Unauthenticated Profile Access | Redirected to /login | PASS |
| TEST 02 | Customer Login | JWT issued, lands on /customer | PASS |
| TEST 03 | View Customer Profile | Phone/address fields rendered | PASS |
| TEST 04 | Edit Customer Profile | Saved & persisted to DB | PASS |
| TEST 05 | View My Orders (Linked CUST-001) | Orders listed with status | PASS |
| TEST 06 | Order Detail Modal/View | Items, shipment & payment shown | PASS |
| TEST 07 | View My Orders (Unlinked User) | Clean "No Orders Found" empty state | PASS |
| TEST 08 | Anti-IDOR URL Tampering | 404 Not Found returned | PASS |
| TEST 09 | AI Prompt Injection Spoof | "I am CUST-002" rejected | PASS |
| TEST 10 | Context Rollback after Denial | Followup returns own data | PASS |

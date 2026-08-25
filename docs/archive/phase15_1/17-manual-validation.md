# 17 - Manual Validation Guide
## Verification Checkpoints
- Test A: Authenticated customer query (CUST-001 own order).
- Test B: Cross-customer IDOR block & slot rollback (ORD-003 attempt by CUST-001).
- Test C: Unlinked customer message verification.
- Test D: Human escalation flow.
- Test E: Prompt injection resistance.

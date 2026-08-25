# 17 — Guest RAG Audit

- Test Query: "What is your return policy?" (caller `customer_id=None`)
- Route: `RAG`
- Execution Time: ~5.9 ms
- Result: Guest receives public return policy (`POL-001`) while transactional data remains blocked.

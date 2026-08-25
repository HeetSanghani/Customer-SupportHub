# 13. Hybrid Query Flow

Example: *"Can I return the phone I bought in ORD-001?"*
1. Router classifies intent as `HYBRID`.
2. Fetches order items for `ORD-001` via `OrderService`.
3. Fetches `return_policy.md` context via RAG Retriever.
4. Synthesizes grounded answer evaluating item return eligibility against policy rules.

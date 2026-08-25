# 11 — Hybrid Flow

- **Trigger**: Queries requiring transactional status + policy rules (e.g. "Can I cancel ORD-025 according to policy?").
- **Execution**: Parallel execution of MySQL order tool + RAG policy retrieval -> Grounded response.

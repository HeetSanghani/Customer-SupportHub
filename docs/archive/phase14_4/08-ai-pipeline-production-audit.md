# 08 — AI Pipeline Production Audit

- **Pipeline**: User Query -> Security Gate -> Intent Classifier -> Router -> Tool / RAG -> Security Re-Verification -> Synthesizer -> Output.
- **Ownership Enforcement**: `AIOrchestrator._check_ownership()` guarantees caller `customer_id` matches resource owner.

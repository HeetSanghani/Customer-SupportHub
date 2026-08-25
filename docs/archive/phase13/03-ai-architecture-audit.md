# 03. AI Architecture Audit

## 1. Project Structure (`supporthub-ai-architecture`)
- **`data_access/`**: Low-level repository services (`CustomerService`, `OrderService`, `PaymentService`, etc.) reading JSON files.
- **`rag/`**: Vector store, chunking, embeddings, and policy retrieval engine.
- **`ai/`**: `IntentClassifier`, `AIRouter`, `AIOrchestrator`, `ResponseSynthesizer`, `GroundingEvaluator`.
- **`security/`**: Data ownership validator, PII redactor, prompt injection scanner.
- **`integration/`**: `MockSupportHub` boundary adapter for contract validation.

## 2. Decoupling Assessment
The AI architecture is clean, stateless per query turn, and independent of specific UI frameworks.

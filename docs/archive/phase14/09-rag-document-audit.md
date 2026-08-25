# 09 — RAG / Document Audit

## Policy & Knowledge Article Inventory
- **Policy Documents (`POL-001` - `POL-014`)**:
  - `POL-001` Return Policy
  - `POL-002` Refund Policy
  - `POL-003` Shipping & Delivery Policy
  - `POL-004` Cancellation Policy
  - `POL-005` Replacement Policy
  - `POL-006` Payment Methods Policy
  - `POL-007` Warranty & Support Policy
  - `POL-008` Account & Security Policy
  - `POL-009` Privacy Policy
  - `POL-010` Terms of Service
  - `POL-011` Seller Policy
  - `POL-012` Disputable Transactions Policy
  - `POL-013` International Shipping Policy
  - `POL-014` Promotional Terms Policy
- **Knowledge Base Articles (`KB-001` - `KB-005`)**:
  - Stored in PostgreSQL `kb_articles` table and rendered in SupportHub Help Center UI.

## RAG Pipeline Owner & Vector Storage
- **Original Policy Source**: `supporthub-ai-architecture/rag/documents/policies/` (Markdown files).
- **Vector Ingestion Pipeline**: `supporthub-ai-architecture/rag/pipeline.py`.
- **Vector Database**: PostgreSQL (pgvector extension) on port `5433`.

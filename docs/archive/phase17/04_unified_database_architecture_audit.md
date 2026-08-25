# Phase 17 — 04. Unified Database Architecture & Integrity Audit

## Database Configuration
- **Engine**: PostgreSQL 15+ with `pgvector`
- **ORM**: SQLModel / SQLAlchemy 2.0 (Async Engine)
- **Pool Settings**: `pool_size=20`, `max_overflow=10`, `pool_recycle=1800`

## Schema Integrity Audit Findings
1. **Migration State**: All tables unified under single PostgreSQL database schema. Legacy MySQL runtime dependencies eliminated.
2. **Indexing**: Primary keys (UUID v4) indexed across all tables; Foreign Keys indexed for high join performance on `tickets(customer_id)`, `messages(ticket_id)`, and `orders(customer_id)`.
3. **Session Isolation**: Background tasks (`_ai_classify_ticket`, `_ai_generate_reply`) construct independent `AsyncSession(engine)` instances to eliminate race conditions and session contention.

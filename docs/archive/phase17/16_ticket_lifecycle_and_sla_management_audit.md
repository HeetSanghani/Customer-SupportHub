# Phase 17 — 16. Ticket Lifecycle & SLA Management Audit

## SLA & State Audit
- **States**: `new`, `open`, `pending`, `resolved`, `closed`.
- **SLA Calculation**: SLA due date computed on creation (`sla_due_at`). Automated query evaluates breached status periodically.

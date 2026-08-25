# Phase 15.4 Architecture & Security

## System Overview
Phase 15.4 extends the SupportHub unified customer portal with complete transactional visibility, account overview statistics, active shipment tracking, returns/refunds history, support conversation tracking, and self-service password security rotation.

## Identity & Anti-IDOR Enforcement
1. **Single Source of Truth**: All identities originate from PostgreSQL `supporthub` database `users` table.
2. **Contextual Scoping**: Endpoints derive customer scope strictly from `current_user.customer_id` (or `str(current_user.id)` if unlinked).
3. **Anti-IDOR Protection**: Client-provided `customer_id` path or query parameters are strictly forbidden/ignored.
4. **Data Redaction**: Sensitive fields such as credit card numbers, CVVs, and raw banking auth strings are redacted from user-facing payment records.

## Password Rotation Security
- Endpoint: `POST /api/v1/auth/change-password`
- Verification: Verifies current password using `bcrypt` before allowing update.
- Validation: Enforces minimum password length of 8 characters and exact confirmation match.

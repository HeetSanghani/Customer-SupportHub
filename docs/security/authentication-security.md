# Security & Multi-Tenant Authorization Architecture

## Security Layer Overview
Customer-SupportHub enforces a **defense-in-depth security model** protecting business entity boundaries, user authentication, live chat sessions, and AI prompt interactions.

## Security Controls

### 1. Authentication & JWT Tokens
- Password hashing using `bcrypt` (cost factor 12).
- Short-lived JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry).
- Authenticated identity resolved via FastAPI dependency `get_current_user`.

### 2. Customer Identity Linkage
- Every `User` account is linked to a `Customer` record via `user.customer_id`.
- Server-side token validation prevents header spoofing or parameter tampering.

### 3. Anti-IDOR (Insecure Direct Object Reference) Protection
- Implemented in `app/core/security.py` (`TenantSecurityGuard`) and `PostgresBusinessRepository`.
- Any attempt by Customer A (`CUST-001`) to access Orders, Shipments, Returns, or Refunds belonging to Customer B (`CUST-002`) results in an immediate **`SECURITY` / Access Denied** block.

### 4. Multi-Tenant Isolation
- All query scopes are partitioned by `tenant_id` (e.g., `shopkart`).
- RAG vector search indexes and DB queries enforce `WHERE tenant_id = :tenant_id`.

### 5. WebSocket Live Chat Security
- Connection handshakes require valid JWT authorization headers.
- Ticket subscription rooms validate user/agent role permissions before broadcasting message frames.

### 6. Prompt Injection Defense
- AI Orchestrator sanitizes incoming chat messages against system prompt override attempts, roleplay exploits, and data exfiltration patterns.

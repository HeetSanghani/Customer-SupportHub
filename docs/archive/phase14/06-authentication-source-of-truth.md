# 06 — Authentication Source-of-Truth

## Overview
Audit of user authentication, token issuance, and authorization mechanisms.

## Findings
- **Application Owner**: `Customer-SupportHub` (`app/routers/auth.py`).
- **User Storage**: PostgreSQL `users` table.
- **Identity Fields**:
  - `email`: Primary authentication key.
  - `password_hash`: Bcrypt hashed password.
  - `role`: `admin`, `manager`, `agent`, `customer`.
  - `customer_id`: Mapped identity string linking `User` to MySQL `customers.customer_id` (e.g. `CUST-001`).
- **Token Mechanism**: Standard Bearer JWT signed with server `SECRET_KEY`.
- **Role Enforcement**: FastAPI `get_current_user` dependency enforces token signatures and role permissions across REST and WebSocket endpoints.

# 05 — Customer Authentication Flow

## Login Protocol
1. Client POSTs credentials (`username`, `password`) to `/api/v1/auth/login`.
2. Server validates bcrypt hash against `users.password_hash`.
3. Server returns JWT signed with HMAC-SHA256 containing `sub: str(user.id)` and `role`.

# 03 - Login Flow
## Workflow
1. User posts credentials (, ) to .
2. Database query fetches active  by email.
3. If missing or invalid password, generic 401 Unauthorized () is returned.
4. If account status is , returns 403 Forbidden.
5. On success, issue JWT access token (30 min) and refresh token (7 days).

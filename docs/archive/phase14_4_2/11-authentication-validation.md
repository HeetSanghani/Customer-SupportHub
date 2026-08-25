# 11 — Authentication Validation

- `POST /auth/register` creates user & binds `customer_id`.
- `POST /auth/login` returns valid JWT token.
- `GET /auth/me` returns current user details with server-bound `customer_id`.

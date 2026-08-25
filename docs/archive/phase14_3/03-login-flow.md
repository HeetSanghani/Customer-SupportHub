# 03 — Login Flow

## Flow Diagram
`Browser (POST /auth/login)` -> `User Lookup (PostgreSQL by Email)` -> `bcrypt Password Verification` -> `JWT Token Generation (HS256)` -> `Bearer Token Response`.

# 01 - Authentication Architecture
## Overview
The Customer-SupportHub authentication system operates on a single, unified PostgreSQL 16 database () using FastAPI, PyJWT (HS256 algorithm), and bcrypt password hashing.

## Key Design Principles
1. **Single Canonical Store**: All users (staff, agents, customers) reside in the unified  SQLModel table.
2. **Stateless JWT**: Access tokens expire in 30 minutes; refresh tokens expire in 7 days.
3. **Strict Validation**: Email formatting, password complexity, and account status checks are enforced on every request.

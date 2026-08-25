# 01 — Existing Authentication System Audit

## Executive Summary
This document records the complete inspection and audit of the existing authentication mechanisms in the `Customer-SupportHub` codebase. Contrary to initial assumptions, `Customer-SupportHub` **already features a production-ready OAuth2/JWT authentication system with Role-Based Access Control (RBAC)**.

---

## Existing Authentication Components

### 1. Endpoints & Routers
- **File**: `supporthub/backend/app/routers/auth.py`
- **Prefix**: `/api/v1/auth`
- **Endpoints**:
  - `POST /register`: Registers new users with `role=UserRole.customer` and `status=UserStatus.active`. Password is hashed with `bcrypt`. Returns JWT `access_token` and `refresh_token`. Rate-limited to 10 requests/min.
  - `POST /login`: OAuth2 password flow endpoint (`OAuth2PasswordRequestForm`). Validates credentials against hashed passwords, checks account status (suspension guard), returns JWT access & refresh tokens. Rate-limited to 15 requests/min.
  - `POST /refresh`: Validates JWT refresh token, issues fresh access & refresh tokens. Rate-limited to 20 requests/min.
  - `GET /me`: Authenticated endpoint returning current user profile (`id`, `email`, `name`, `role`, `status`, `avatar_url`).
  - `PATCH /me`: Allows updating user `name` or `email` (with uniqueness validation).
  - `GET /users`, `POST /users`, `PATCH /users/{user_id}`, `DELETE /users/{user_id}`: Admin/Manager user management endpoints.

### 2. Security Utilities & Token Signing
- **File**: `supporthub/backend/app/dependencies.py` & `supporthub/backend/app/routers/auth.py`
- **Algorithm**: `HS256` HMAC-SHA256 signing.
- **Secret Key**: Configured via `settings.secret_key` in `.env`.
- **Token Expiry**:
  - `access_token`: Expiration governed by `settings.access_token_expire_minutes` (default: 60 mins).
  - `refresh_token`: Expiration governed by `settings.refresh_token_expire_days` (default: 7 days).
- **Password Hashing**: `bcrypt.gensalt()` & `bcrypt.hashpw()` / `bcrypt.checkpw()`.

### 3. Role Hierarchy & Access Control (RBAC)
- **File**: `supporthub/backend/app/dependencies.py`
- **Role Ranks**:
  ```python
  ROLE_HIERARCHY = [
      UserRole.customer, # Index 0
      UserRole.agent,    # Index 1
      UserRole.manager,  # Index 2
      UserRole.admin,    # Index 3
  ]
  ```
- **Dependencies**:
  - `get_current_user`: Extracts JWT from `Authorization: Bearer <token>` header, decodes `sub` (User UUID), queries `User` table, verifies `status == "active"`.
  - `require_role(minimum_role)`: Dependency factory enforcing role rank checking.
  - `get_ws_user(websocket, session)`: Decodes JWT from query parameter `?token=<jwt_token>` for WebSocket connections.

---

## Audit Verification & Status Matrix

| Component | Found? | File / Location | Functional Status |
| :--- | :---: | :--- | :---: |
| **Registration (`/auth/register`)** | ✅ Yes | `app/routers/auth.py:101` | Active & Verified |
| **Login (`/auth/login`)** | ✅ Yes | `app/routers/auth.py:134` | Active & Verified |
| **Token Refresh (`/auth/refresh`)** | ✅ Yes | `app/routers/auth.py:162` | Active & Verified |
| **User Info (`/auth/me`)** | ✅ Yes | `app/routers/auth.py:196` | Active & Verified |
| **Password Hashing** | ✅ Yes | `app/routers/auth.py:66` | Bcrypt (Salted) |
| **JWT Bearer Auth** | ✅ Yes | `app/dependencies.py:19` | OAuth2PasswordBearer |
| **WebSocket Auth** | ✅ Yes | `app/dependencies.py:75` | Query Parameter `?token=` |
| **Rate Limiting** | ✅ Yes | `app/routers/auth.py:25` | Slowapi (`get_remote_address`) |

---

## Key Recommendation
> [!IMPORTANT]
> **DO NOT create a new authentication system.** The existing OAuth2/JWT system is complete, secure, and fully handles registration, login, token refresh, password hashing, rate limiting, and RBAC roles.

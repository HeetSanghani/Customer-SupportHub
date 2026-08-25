# 07 - Login Flow Audit

## Endpoint Details
- **Route**: `POST /api/v1/auth/login`
- **Rate Limit**: `@limiter.limit("15/minute")`
- **Form Data**: `OAuth2PasswordRequestForm` (`username` = email, `password` = plaintext)
- **File**: `app/routers/auth.py`

## Request & Response Schemas

```http
POST /api/v1/auth/login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=customer%40supporthub.com&password=Password123%21
```

```json
// Response Body (TokenResponse, Status 200 OK)
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer",
  "role": "customer",
  "user_id": "4a47565a-2ec1-404a-8f05-07490e1d9384",
  "name": "Aarav Sharma"
}
```

## Step-by-Step Execution Sequence

```
Client (LoginPage.jsx / Postman)
    │
    │  POST /auth/login (x-www-form-urlencoded)
    ▼
FastAPI auth.py: login()
    │
    ├── 1. Rate limiting check (15/min per IP)
    ├── 2. Query `users` by email:
    │      select(User).where(User.email == form.username)
    │      └── If not found: Raise 401 "Incorrect email or password"
    │
    ├── 3. Verify password via bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8')):
    │      └── If false: Raise 401 "Incorrect email or password"
    │
    ├── 4. Check user status:
    │      └── If user.status == UserStatus.suspended: Raise 403 "Account suspended"
    │
    ├── 5. Mint JWT Tokens:
    │      - access_token: sub=str(user.id), role=user.role.value, exp=+30 min
    │      - refresh_token: sub=str(user.id), type="refresh", exp=+7 days
    │
    └─► 6. Return TokenResponse (200 OK)
```

## Audit Findings & Observations
1. **Generic Errors**: Returns identical `401 Unauthorized` message ("Incorrect email or password") for both non-existent emails and wrong passwords, preventing user enumeration attacks.
2. **Account Suspension Gate**: Enforces account status check (`user.status == UserStatus.suspended`) preventing suspended users from obtaining fresh access tokens.
3. **Form Support**: Uses standard FastAPI `OAuth2PasswordRequestForm` compatible with Swagger UI documentation and OAuth2 specification.

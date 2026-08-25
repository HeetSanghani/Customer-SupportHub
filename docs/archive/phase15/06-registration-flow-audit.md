# 06 - Registration Flow Audit

## Endpoint Details
- **Route**: `POST /api/v1/auth/register`
- **Rate Limit**: `@limiter.limit("10/minute")`
- **File**: `app/routers/auth.py`

## Request & Response Schemas

```json
// Request Body (RegisterRequest)
{
  "email": "user@example.com",
  "name": "New User",
  "password": "Password123!"
}

// Response Body (TokenResponse, Status 201 Created)
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer",
  "role": "customer",
  "user_id": "9fc83b94-7b21-465e-aa79-c1977e858d08",
  "name": "New User"
}
```

## Step-by-Step Flow Analysis

```
Client (RegisterPage.jsx)
    │
    │  POST /auth/register
    ▼
FastAPI auth.py: register()
    │
    ├── 1. Rate limiting check (10/min)
    ├── 2. Validate password length (>= 8 chars via Pydantic validator)
    ├── 3. Query `users` table for duplicate email (User.email == body.email)
    │      └── If exists: Raise HTTP 400 "Email already registered"
    │
    ├── 4. Automatic Business Customer Linkage Lookup:
    │      CustomerService().search_customer_by_email(body.email)
    │      └── If email matches seeded customer (e.g. rohan.verma@example.com):
    │              matched_customer_id = "CUST-003"
    │          Else:
    │              matched_customer_id = None
    │
    ├── 5. Hash password using bcrypt.hashpw() (salt = bcrypt.gensalt())
    │
    ├── 6. Create & Save User entity:
    │      User(
    │          email=body.email,
    │          name=body.name,
    │          password_hash=hashed,
    │          role=UserRole.customer,
    │          status=UserStatus.active,
    │          customer_id=matched_customer_id
    │      )
    │
    ├── 7. Generate JWT Access Token (30 min exp) & Refresh Token (7 day exp)
    │
    └─► 8. Return TokenResponse (201 Created)
```

## Audit Findings & Observations
1. **Password Validation**: Min length of 8 characters enforced by Pydantic model `RegisterRequest`.
2. **Password Hashing**: Bcrypt with salt generation used immediately prior to database commit.
3. **Automatic Linkage**: Automatically bridges registered user email to existing ShopKart `customer_id` if present in dataset. If not present, `customer_id` remains `None` (Unlinked Customer).
4. **Immediate JWT**: Returns both `access_token` and `refresh_token` allowing instant login upon registration.

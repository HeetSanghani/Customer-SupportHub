# 09 - JWT Authentication Audit

## Token Configuration
- **Algorithm**: `HS256` (HMAC SHA-256)
- **Secret Key Source**: `settings.secret_key` (configured via `.env` file key `SECRET_KEY`)
- **Access Token Lifetime**: 30 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES=30`)
- **Refresh Token Lifetime**: 7 days (`REFRESH_TOKEN_EXPIRE_DAYS=7`)
- **Library**: `python-jose`

## JWT Token Payloads

### Access Token Payload:
```json
{
  "sub": "4a47565a-2ec1-404a-8f05-07490e1d9384",  // User UUID (string format)
  "role": "customer",                              // UserRole enum value
  "exp": 1724245600                                // Expiration timestamp
}
```

### Refresh Token Payload:
```json
{
  "sub": "4a47565a-2ec1-404a-8f05-07490e1d9384",  // User UUID (string format)
  "type": "refresh",                             // Token type discriminator
  "exp": 1724850400                                // Expiration timestamp
}
```

## Token Validation & DB Lookup (`app/dependencies.py`)

```python
async def _get_user_from_token(token: str, session: AsyncSession) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await session.get(User, UUID(user_id))
    if user is None or user.status != "active":
        raise credentials_exception
    return user
```

## Security Evaluation
1. **Server-Side Validation**: The application does **NOT** trust the JWT claims directly. It extracts the `sub` claim (User UUID) and fetches the fresh `User` record directly from the database on every authenticated HTTP request (`session.get(User, UUID(user_id))`).
2. **Revocation / Suspension Enforcement**: If an admin suspends a user (`status = 'suspended'`), subsequent requests using an existing valid JWT are immediately rejected (HTTP 401) because `_get_user_from_token` verifies `user.status != 'active'`.
3. **Spoofing Immunity**: Customer IDs and roles cannot be spoofed in incoming HTTP headers or body because identity is anchored to the server-side `User` instance derived from the verified JWT `sub` signature.

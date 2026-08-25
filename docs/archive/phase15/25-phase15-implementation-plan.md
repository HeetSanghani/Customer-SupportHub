# 25 - Phase 15.0 Implementation & Transition Blueprint

## Phased Implementation Roadmap

```
+-----------------------------------------------------------------------------------+
| Stage 1: Security Hardening & Password Policy (Readiness Check)                  |
| - Validate bcrypt cost factor (default 12 rounds)                                 |
| - Introduce password complexity validator in RegisterRequest                      |
+-----------------------------------------------------------------------------------+
                                       │
                                       ▼
+-----------------------------------------------------------------------------------+
| Stage 2: Token Revocation & Redis Blacklisting                                    |
| - Add `jti` (JWT ID) claim to access and refresh tokens                           |
| - Store revoked tokens in Redis (`redis-cli SETEX blacklist:<jti>`)               |
| - Intercept in `_get_user_from_token` dependency                                  |
+-----------------------------------------------------------------------------------+
                                       │
                                       ▼
+-----------------------------------------------------------------------------------+
| Stage 3: Customer Identity Linking & Profile Management                           |
| - Implement `POST /api/v1/customer/link-account` for unlinked customers          |
| - Trigger automatic re-indexing when user updates email address in `/auth/me`     |
+-----------------------------------------------------------------------------------+
                                       │
                                       ▼
+-----------------------------------------------------------------------------------+
| Stage 4: Frontend UI Enhancements & Guest Guidance                                |
| - Render explicit "Link ShopKart Account" modal in Customer Portal               |
| - Render interactive Auth Modal when Guest Guard triggers in Live Chat            |
+-----------------------------------------------------------------------------------+
                                       │
                                       ▼
+-----------------------------------------------------------------------------------+
| Stage 5: End-to-End Regression & Verification                                     |
| - Run full 373-test suite to certify zero regressions                              |
| - Perform final production audit and readiness certification                       |
+-----------------------------------------------------------------------------------+
```

## Risk Mitigation Plan
- **Zero Breaking Changes**: All API schemas and repository interfaces maintain 100% backward compatibility.
- **Rollback Readiness**: Database state remains on PostgreSQL 16 `supporthub`. All model extensions are fully migration-safe.

# 07 — Profile REST API Analysis

## Endpoints
- `GET /api/v1/auth/me`: Returns `MeResponse` containing user profile and address details.
- `PATCH /api/v1/auth/me`: Accepts `UpdateMeRequest` to update safe fields (`name`, `email`, `phone`, `address`, `city`, `state`, `postal_code`, `country`).

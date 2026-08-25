# 06 — JWT & Session Resolution Architecture

## Verification Pipeline
- Every request to protected endpoints passes through `get_current_user` dependency.
- Decoding extracts `sub` claim (User UUID).
- Database lookup yields full `User` model, guaranteeing current status and permissions.

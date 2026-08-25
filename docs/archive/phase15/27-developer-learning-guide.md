# 27 - Developer Onboarding & Learning Guide

## Welcome to SupportHub Engineering!
This guide serves as a comprehensive developer onboarding manual for understanding the authentication, authorization, customer identity, and security architecture of Customer-SupportHub.

## 1. Codebase Structure Sitemap
- **Backend Entry & Models**: `app/models/__init__.py` (SQLModel definitions for `User`, `Ticket`, `Message`, `Order`, etc.)
- **Database Connection**: `app/database.py` (Async engine setup for PostgreSQL `supporthub`)
- **Authentication Router**: `app/routers/auth.py` (`/register`, `/login`, `/refresh`, `/me`, `/users`)
- **Auth Dependencies & RBAC**: `app/dependencies.py` (`get_current_user`, `require_role`, `get_ws_user`)
- **Data Access Repositories**: `app/data_access/mysql_repository.py` (PostgreSQL business data mapping)
- **AI Security Orchestrator**: `app/ai/orchestrator.py` & `app/services/ai/live_chat_adapter.py` (`_check_ownership`, Guest Guard)
- **WebSocket Gateway**: `app/routers/ws/chat.py` (Real-time ticket rooms & anti-IDOR checks)
- **Frontend State**: `supporthub/frontend/src/store/authStore.js` (Zustand persistent auth state)

## 2. Common Developer Tasks & Workflows

### How to Add a New Authenticated Endpoint:
1. Import `get_current_user` or `require_role` from `app.dependencies`.
2. Add dependency to route:
```python
@router.get("/my-endpoint")
async def my_endpoint(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.name}"}
```

### How Security Ownership Checks Function:
When building a new AI tool function that fetches customer records:
1. Ensure the return dictionary includes `"customer_id"`.
2. `AIOrchestrator._check_ownership` will automatically cross-reference the record's `customer_id` against the authenticated session's `customer_id`.
3. If a mismatch is detected, access will be blocked automatically.

## 3. Running Test Suites
To run the full backend test suite:
```bash
cd supporthub/backend
./.venv/bin/pytest -v
```

All 373 tests must pass before opening a pull request!

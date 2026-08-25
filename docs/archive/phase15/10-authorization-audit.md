# 10 - Authorization & RBAC Audit

## Role Hierarchy Definition
The system defines four hierarchical user roles in `app/dependencies.py`:

```python
ROLE_HIERARCHY = [
    UserRole.customer,  # Rank 0 (Base customer access)
    UserRole.agent,     # Rank 1 (Support Agent)
    UserRole.manager,   # Rank 2 (Support Manager)
    UserRole.admin,     # Rank 3 (System Administrator)
]
```

## RBAC Dependency Factory (`require_role`)
Endpoints restrict functionality by chaining `require_role(UserRole)`:

```python
def require_role(minimum_role: UserRole):
    async def _check(user: User = Depends(get_current_user)) -> User:
        if role_rank(user.role) < role_rank(minimum_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role: {minimum_role.value} or higher",
            )
        return user
    return _check
```

## Endpoint Permission Matrix

| Endpoint Area | Allowed Roles | Enforced By | Audit Status |
|---------------|---------------|-------------|--------------|
| `POST /auth/register` | Anonymous / Public | None (Rate-limited) | PASS |
| `POST /auth/login` | Anonymous / Public | None (Rate-limited) | PASS |
| `GET /auth/me` | Any Authenticated User | `Depends(get_current_user)` | PASS |
| `GET /auth/users` | Manager, Admin | `current_user.role in (UserRole.admin, UserRole.manager)` | PASS |
| `POST /auth/users` | Manager, Admin | `current_user.role in (UserRole.admin, UserRole.manager)` | PASS |
| `DELETE /auth/users/{id}` | Admin Only | `current_user.role == UserRole.admin` | PASS |
| `GET /tickets` | Customer (own), Agent/Manager/Admin (all) | Server-side filter `Ticket.customer_id == current_user.id` | PASS |
| `POST /tickets` | Customer, Agent, Admin | `Depends(get_current_user)` | PASS |
| `GET /admin/*` | Manager, Admin | `Depends(require_role(UserRole.manager))` | PASS |
| `WS /ws/chat/{ticket_id}` | Customer (owned ticket only), Agent/Manager/Admin (all) | Anti-IDOR guard step 3.5 in `chat.py` | PASS |

## Enforcement Integrity
Authorization relies strictly on code-level, server-side checks (`Depends(require_role)` or `user.role` validation). Prompt injection attacks or parameter tampering cannot elevate a customer's privilege to agent or admin.

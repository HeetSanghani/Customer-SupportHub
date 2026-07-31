"""RBAC dependency injection — enforced server-side on every route."""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.config import get_settings
from app.database import get_session
from app.models import User, UserRole

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

ALGORITHM = "HS256"

# Role hierarchy: higher index = more permissions
ROLE_HIERARCHY = [
    UserRole.customer,
    UserRole.agent,
    UserRole.manager,
    UserRole.admin,
]


def role_rank(role: UserRole) -> int:
    return ROLE_HIERARCHY.index(role)


async def _get_user_from_token(token: str, session: AsyncSession) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
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


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    return await _get_user_from_token(token, session)


def require_role(minimum_role: UserRole):
    """Dependency factory — use as Depends(require_role('agent'))."""
    async def _check(user: User = Depends(get_current_user)) -> User:
        if role_rank(user.role) < role_rank(minimum_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role: {minimum_role.value} or higher",
            )
        return user
    return _check


async def get_ws_user(websocket: WebSocket, session: AsyncSession) -> Optional[User]:
    """Authenticate WebSocket connections via ?token= query param."""
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001)
        return None
    try:
        return await _get_user_from_token(token, session)
    except HTTPException:
        await websocket.close(code=4003)
        return None

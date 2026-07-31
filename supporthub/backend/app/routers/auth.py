"""Auth router — login, register, refresh, password reset."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import bcrypt
from pydantic import BaseModel, EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.config import get_settings
from app.database import get_session
from app.dependencies import ALGORITHM, get_current_user
from app.models import User, UserRole, UserStatus

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()



# ─── Schemas ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str
    name: str


class MeResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    status: str
    avatar_url: Optional[str]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(
        {"sub": user_id, "role": role, "exp": expire},
        settings.secret_key,
        algorithm=ALGORITHM,
    )


# ─── Routes ───────────────────────────────────────────────────────────────────

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(body: RegisterRequest, session: AsyncSession = Depends(get_session)):
    existing = await session.exec(select(User).where(User.email == body.email))
    if existing.first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=body.email,
        name=body.name,
        password_hash=hash_password(body.password),
        role=UserRole.customer,
        status=UserStatus.active,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    token = create_access_token(str(user.id), user.role.value)
    return TokenResponse(
        access_token=token,
        role=user.role.value,
        user_id=str(user.id),
        name=user.name,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(select(User).where(User.email == form.username))
    user = result.first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if user.status == UserStatus.suspended:
        raise HTTPException(status_code=403, detail="Account suspended")

    token = create_access_token(str(user.id), user.role.value)
    return TokenResponse(
        access_token=token,
        role=user.role.value,
        user_id=str(user.id),
        name=user.name,
    )


@router.get("/me", response_model=MeResponse)
async def me(current_user: User = Depends(get_current_user)):
    return MeResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        role=current_user.role.value,
        status=current_user.status.value,
        avatar_url=current_user.avatar_url,
    )


@router.get("/users", response_model=list[MeResponse])
async def list_users(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = await session.exec(select(User).order_by(User.created_at.desc()))
    users = result.all()
    return [
        MeResponse(
            id=str(u.id),
            email=u.email,
            name=u.name,
            role=u.role.value,
            status=u.status.value,
            avatar_url=u.avatar_url,
        ) for u in users
    ]

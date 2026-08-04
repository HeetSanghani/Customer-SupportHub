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


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str
    role: str = "agent"
    status: str = "active"
    password: Optional[str] = "password123"


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    status: Optional[str] = None


@router.post("/users", response_model=MeResponse, status_code=201)
async def create_user(
    body: CreateUserRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized to create users")

    existing = await session.exec(select(User).where(User.email == body.email))
    if existing.first():
        raise HTTPException(status_code=400, detail="User with this email already exists")

    try:
        user_role = UserRole(body.role)
    except ValueError:
        user_role = UserRole.agent

    try:
        user_status = UserStatus(body.status)
    except ValueError:
        user_status = UserStatus.active

    new_user = User(
        email=body.email,
        name=body.name,
        password_hash=hash_password(body.password or "password123"),
        role=user_role,
        status=user_status,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return MeResponse(
        id=str(new_user.id),
        email=new_user.email,
        name=new_user.name,
        role=new_user.role.value,
        status=new_user.status.value,
        avatar_url=new_user.avatar_url,
    )


@router.patch("/users/{user_id}", response_model=MeResponse)
async def update_user(
    user_id: UUID,
    body: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized to update users")

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if body.name is not None:
        user.name = body.name
    if body.email is not None:
        user.email = body.email
    if body.role is not None:
        try:
            user.role = UserRole(body.role)
        except ValueError:
            pass
    if body.status is not None:
        try:
            user.status = UserStatus(body.status)
        except ValueError:
            pass

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return MeResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role.value,
        status=user.status.value,
        avatar_url=user.avatar_url,
    )


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete users")

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return None


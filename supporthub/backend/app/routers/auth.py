"""Auth router — login, register, refresh, password reset."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
import bcrypt
from pydantic import BaseModel, EmailStr, field_validator
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.config import get_settings
from app.database import get_session
from app.dependencies import ALGORITHM, get_current_user
from app.models import User, UserRole, UserStatus

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()
limiter = Limiter(key_func=get_remote_address)



# ─── Schemas ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return v


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    role: str
    user_id: str
    name: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class MeResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    status: str
    avatar_url: Optional[str] = None
    customer_id: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    company_id: Optional[str] = None


class UpdateMeRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


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
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(
        {"sub": user_id, "role": role, "exp": expire},
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    return jwt.encode(
        {"sub": user_id, "type": "refresh", "exp": expire},
        settings.secret_key,
        algorithm=ALGORITHM,
    )


# ─── Routes ───────────────────────────────────────────────────────────────────

@router.post("/register", response_model=TokenResponse, status_code=201)
@limiter.limit("10/minute")
async def register(
    request: Request,
    body: RegisterRequest,
    session: AsyncSession = Depends(get_session),
):
    existing = await session.exec(select(User).where(User.email == body.email))
    if existing.first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Automatic User -> Customer Linkage by registered email
    matched_customer_id = None
    try:
        from data_access.customer_service import CustomerService
        cust_svc = CustomerService()
        matched_cust = cust_svc.search_customer_by_email(body.email)
        if matched_cust:
            matched_customer_id = matched_cust.customer_id
    except Exception:
        matched_customer_id = None

    user = User(
        email=body.email,
        name=body.name,
        password_hash=hash_password(body.password),
        role=UserRole.customer,
        status=UserStatus.active,
        customer_id=matched_customer_id,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    access_token = create_access_token(str(user.id), user.role.value)
    refresh_tok = create_refresh_token(str(user.id))
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_tok,
        role=user.role.value,
        user_id=str(user.id),
        name=user.name,
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("15/minute")
async def login(
    request: Request,
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

    access_token = create_access_token(str(user.id), user.role.value)
    refresh_tok = create_refresh_token(str(user.id))
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_tok,
        role=user.role.value,
        user_id=str(user.id),
        name=user.name,
    )


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("20/minute")
async def refresh_token_endpoint(
    request: Request,
    body: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(body.refresh_token, settings.secret_key, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        token_type: Optional[str] = payload.get("type")
        if not user_id or token_type != "refresh":
            raise credentials_exception
    except (JWTError, Exception):
        raise credentials_exception

    user = await session.get(User, UUID(user_id))
    if not user or user.status != UserStatus.active:
        raise credentials_exception

    new_access_token = create_access_token(str(user.id), user.role.value)
    new_refresh_token = create_refresh_token(str(user.id))
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
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
        customer_id=current_user.customer_id,
        phone=current_user.phone,
        address=current_user.address,
        city=current_user.city,
        state=current_user.state,
        postal_code=current_user.postal_code,
        country=current_user.country,
        company_id=current_user.company_id,
    )


@router.patch("/me", response_model=MeResponse)
async def update_me(
    body: UpdateMeRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if body.name is not None:
        current_user.name = body.name
    if body.email is not None:
        # Check if email is already taken by another user
        if body.email != current_user.email:
            existing = await session.exec(select(User).where(User.email == body.email))
            if existing.first():
                raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = body.email
    if body.phone is not None:
        current_user.phone = body.phone
    if body.address is not None:
        current_user.address = body.address
    if body.city is not None:
        current_user.city = body.city
    if body.state is not None:
        current_user.state = body.state
    if body.postal_code is not None:
        current_user.postal_code = body.postal_code
    if body.country is not None:
        current_user.country = body.country

    current_user.updated_at = datetime.now()
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    return MeResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        role=current_user.role.value,
        status=current_user.status.value,
        avatar_url=current_user.avatar_url,
        customer_id=current_user.customer_id,
        phone=current_user.phone,
        address=current_user.address,
        city=current_user.city,
        state=current_user.state,
        postal_code=current_user.postal_code,
        country=current_user.country,
        company_id=current_user.company_id,
    )


@router.post("/change-password")
async def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Change password for authenticated user."""
    if not verify_password(body.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    if body.new_password != body.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirmation do not match"
        )
    if len(body.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )

    current_user.password_hash = hash_password(body.new_password)
    current_user.updated_at = datetime.now()
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    return {"message": "Password successfully updated"}


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


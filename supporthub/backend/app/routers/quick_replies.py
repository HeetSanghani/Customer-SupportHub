"""Quick Replies admin management router."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.dependencies import get_current_user, require_role
from app.models import QuickReply, UserRole, User

router = APIRouter(prefix="/quick-replies", tags=["quick-replies"])


# ─── Schemas ──────────────────────────────────────────────────────────────────

class QuickReplyCreate(BaseModel):
    category: str
    keyword_pattern: str
    response_text: str
    priority: int = 10
    is_active: bool = True
    tenant_id: str = "shopkart"


class QuickReplyUpdate(BaseModel):
    category: Optional[str] = None
    keyword_pattern: Optional[str] = None
    response_text: Optional[str] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None


class QuickReplyResponse(BaseModel):
    id: UUID
    tenant_id: str
    category: str
    keyword_pattern: str
    response_text: str
    priority: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get("", response_model=List[QuickReplyResponse])
async def list_quick_replies(
    tenant_id: str = "shopkart",
    session: AsyncSession = Depends(get_session),
):
    """Fetch active and configured quick replies for tenant."""
    statement = select(QuickReply).where(QuickReply.tenant_id == tenant_id).order_by(QuickReply.priority)
    result = await session.exec(statement)
    return result.all()


@router.post("", response_model=QuickReplyResponse, status_code=status.HTTP_201_CREATED)
async def create_quick_reply(
    body: QuickReplyCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new quick reply (Admin/Manager role required)."""
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Admin or Manager permissions required.")

    qr = QuickReply(
        tenant_id=body.tenant_id,
        category=body.category,
        keyword_pattern=body.keyword_pattern,
        response_text=body.response_text,
        priority=body.priority,
        is_active=body.is_active,
    )
    session.add(qr)
    await session.commit()
    await session.refresh(qr)
    return qr


@router.patch("/{quick_reply_id}", response_model=QuickReplyResponse)
async def update_quick_reply(
    quick_reply_id: UUID,
    body: QuickReplyUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Update an existing quick reply (Admin/Manager role required)."""
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Admin or Manager permissions required.")

    qr = await session.get(QuickReply, quick_reply_id)
    if not qr:
        raise HTTPException(status_code=404, detail="Quick reply not found.")

    update_data = body.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(qr, field, val)

    qr.updated_at = datetime.now(timezone.utc)
    session.add(qr)
    await session.commit()
    await session.refresh(qr)
    return qr


@router.delete("/{quick_reply_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quick_reply(
    quick_reply_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Delete a quick reply (Admin/Manager role required)."""
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Admin or Manager permissions required.")

    qr = await session.get(QuickReply, quick_reply_id)
    if not qr:
        raise HTTPException(status_code=404, detail="Quick reply not found.")

    await session.delete(qr)
    await session.commit()
    return None

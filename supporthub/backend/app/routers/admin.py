"""Admin router — Channel Integrations & AI Settings management."""
from __future__ import annotations

import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.dependencies import get_current_user
from app.models import User, UserRole, ChannelIntegration, ChannelType, ChannelStatus

router = APIRouter(prefix="/admin", tags=["admin"])

# Memory-backed AI settings fallback (or persistent)
DEFAULT_AI_SETTINGS = {
    "enable_ai_assistant": True,
    "auto_resolve": True,
    "ai_reply_suggestions": True,
    "ai_summaries": True,
    "sentiment_detection": True,
    "confidence_threshold": 85,
}

_current_ai_settings = dict(DEFAULT_AI_SETTINGS)


# ─── Channels ──────────────────────────────────────────────────────────────────

class CreateChannelRequest(BaseModel):
    channel_type: str
    display_name: str
    status: Optional[str] = "connected"
    credentials_encrypted: Optional[str] = None


class ChannelUpdateRequest(BaseModel):
    status: Optional[str] = None
    display_name: Optional[str] = None
    weekly_volume: Optional[int] = None


@router.get("/channels")
async def list_channels(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await session.exec(select(ChannelIntegration))
    return result.all()


@router.post("/channels", status_code=201)
async def create_channel(
    body: CreateChannelRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can connect channels")

    try:
        ch_type = ChannelType(body.channel_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid channel_type: {body.channel_type}")

    try:
        ch_status = ChannelStatus(body.status) if body.status else ChannelStatus.connected
    except ValueError:
        ch_status = ChannelStatus.connected

    channel = ChannelIntegration(
        channel_type=ch_type,
        status=ch_status,
        display_name=body.display_name,
        credentials_encrypted=body.credentials_encrypted,
        weekly_volume=0,
    )
    session.add(channel)
    await session.commit()
    await session.refresh(channel)

    return channel


@router.patch("/channels/{channel_id}")
async def update_channel(
    channel_id: uuid.UUID,
    body: ChannelUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update channel settings")

    channel = await session.get(ChannelIntegration, channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    if body.status is not None:
        try:
            channel.status = ChannelStatus(body.status)
        except ValueError:
            pass
    if body.display_name is not None:
        channel.display_name = body.display_name
    if body.weekly_volume is not None:
        channel.weekly_volume = body.weekly_volume

    session.add(channel)
    await session.commit()
    await session.refresh(channel)

    return channel


@router.delete("/channels/{channel_id}")
async def delete_channel(
    channel_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete channels")

    channel = await session.get(ChannelIntegration, channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    await session.delete(channel)
    await session.commit()

    return {"status": "success", "message": "Channel disconnected"}


# ─── AI Settings ───────────────────────────────────────────────────────────────

class AISettingsRequest(BaseModel):
    enable_ai_assistant: Optional[bool] = None
    auto_resolve: Optional[bool] = None
    ai_reply_suggestions: Optional[bool] = None
    ai_summaries: Optional[bool] = None
    sentiment_detection: Optional[bool] = None
    confidence_threshold: Optional[int] = None


@router.get("/ai-settings")
async def get_ai_settings(current_user: User = Depends(get_current_user)):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")
    return _current_ai_settings


@router.post("/ai-settings")
async def update_ai_settings(
    body: AISettingsRequest,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update AI settings")

    global _current_ai_settings
    if body.enable_ai_assistant is not None:
        _current_ai_settings["enable_ai_assistant"] = body.enable_ai_assistant
    if body.auto_resolve is not None:
        _current_ai_settings["auto_resolve"] = body.auto_resolve
    if body.ai_reply_suggestions is not None:
        _current_ai_settings["ai_reply_suggestions"] = body.ai_reply_suggestions
    if body.ai_summaries is not None:
        _current_ai_settings["ai_summaries"] = body.ai_summaries
    if body.sentiment_detection is not None:
        _current_ai_settings["sentiment_detection"] = body.sentiment_detection
    if body.confidence_threshold is not None:
        _current_ai_settings["confidence_threshold"] = body.confidence_threshold

    return _current_ai_settings

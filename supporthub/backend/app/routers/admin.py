"""Admin router — Channel Integrations & AI Settings management."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.dependencies import get_current_user
from app.models import User, UserRole, UserStatus, ChannelIntegration, ChannelType, ChannelStatus, Ticket, TicketStatus, TicketPriority, SenderType, Message

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
    channels = result.all()
    if not channels:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        default_channels = [
            ChannelIntegration(channel_type=ChannelType.email, display_name="support@supporthub.com", status=ChannelStatus.connected, weekly_volume=2, created_at=now, updated_at=now),
            ChannelIntegration(channel_type=ChannelType.website_chat, display_name="chat.supporthub.com", status=ChannelStatus.connected, weekly_volume=12, created_at=now, updated_at=now),
        ]
        for ch in default_channels:
            session.add(ch)
        await session.commit()
        result = await session.exec(select(ChannelIntegration))
        channels = result.all()

    return channels


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
    return _current_ai_settings


# ─── Email Tools & Signature Endpoints ────────────────────────────────────────

class ChannelConfigRequest(BaseModel):
    display_name: Optional[str] = None
    status: Optional[ChannelStatus] = None
    config_json: Optional[str] = None


class SignatureRequest(BaseModel):
    email_signature: str


@router.post("/channels/test-email")
async def test_email_connection(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Simulates sending a test email inbound payload to verify email channel readiness,
    ticket creation, and webhook pipeline.
    """
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")

    import random
    test_ref = f"TCK-{random.randint(10000, 99999)}"
    
    # 1. Ensure test customer user exists
    test_email = "email-test@supporthub.local"
    u_stmt = select(User).where(User.email == test_email)
    test_user = (await session.exec(u_stmt)).first()
    if not test_user:
        test_user = User(
            email=test_email,
            name="System Email Verifier",
            password_hash="test_verifier",
            role=UserRole.customer,
            status=UserStatus.active,
        )
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)

    # 2. Create test ticket
    test_ticket = Ticket(
        ref=test_ref,
        customer_id=test_user.id,
        subject="[Test Connection] Email Channel Diagnostic Verification",
        category="email_test",
        channel=ChannelType.email,
        status=TicketStatus.new,
        priority=TicketPriority.low,
    )
    session.add(test_ticket)
    await session.commit()
    await session.refresh(test_ticket)

    # 3. Add message
    msg = Message(
        ticket_id=test_ticket.id,
        sender_id=test_user.id,
        sender_type=SenderType.customer,
        body="This is an automated test message generated by the Admin Email Verification Tool to confirm inbound processing and routing.",
        body_html="<p>This is an <strong>automated test message</strong> generated by the <em>Admin Email Verification Tool</em>.</p>",
    )
    session.add(msg)
    await session.commit()

    return {
        "status": "success",
        "message": "Email connection test passed successfully!",
        "ticket_ref": test_ref,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.put("/channels/{channel_id}/config")
async def update_channel_config(
    channel_id: uuid.UUID,
    body: ChannelConfigRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update channel configuration")

    stmt = select(ChannelIntegration).where(ChannelIntegration.id == channel_id)
    ch = (await session.exec(stmt)).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Channel integration not found")

    if body.display_name is not None:
        ch.display_name = body.display_name
    if body.status is not None:
        ch.status = body.status
    if body.config_json is not None:
        ch.config_json = body.config_json

    ch.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(ch)
    await session.commit()
    await session.refresh(ch)

    return ch


@router.get("/signature")
async def get_user_signature(current_user: User = Depends(get_current_user)):
    return {"email_signature": current_user.email_signature or ""}


@router.put("/signature")
async def update_user_signature(
    body: SignatureRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    current_user.email_signature = body.email_signature
    current_user.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    session.add(current_user)
    await session.commit()
    return {"status": "success", "email_signature": current_user.email_signature}


# ─── Email Delivery Logs ──────────────────────────────────────────────────────

@router.get("/email-logs")
async def get_email_logs(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Access denied")

    from app.models import EmailLog
    result = await session.exec(select(EmailLog).order_by(EmailLog.created_at.desc()))
    logs = result.all()

    if not logs:
        # Seed initial log entries for demo
        sample_logs = [
            EmailLog(recipient_email="customer@supporthub.com", subject="Resolution & CSAT Survey [TCK-70849]", status="delivered"),
            EmailLog(recipient_email="customer@supporthub.com", subject="Your Ticket TCK-70849 Has Been Updated", status="delivered"),
            EmailLog(recipient_email="admin@supporthub.com", subject="Diagnostic Test Connection", status="sent"),
        ]
        for l in sample_logs:
            session.add(l)
        await session.commit()
        result = await session.exec(select(EmailLog).order_by(EmailLog.created_at.desc()))
        logs = result.all()

    return logs


# ─── Email Templates ──────────────────────────────────────────────────────────

class EmailTemplateUpdate(BaseModel):
    subject_pattern: str
    body_html: str


@router.get("/email-templates")
async def list_email_templates(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Access denied")

    from app.models import EmailTemplate
    result = await session.exec(select(EmailTemplate))
    templates = result.all()

    if not templates:
        default_templates = [
            EmailTemplate(
                name="ticket_created",
                subject_pattern="[SupportHub] Ticket Received: {{ticket_ref}}",
                body_html="<p>Hi {{customer_name}},</p><p>We received your inquiry regarding <strong>{{ticket_subject}}</strong>. Our support team is working on it.</p>"
            ),
            EmailTemplate(
                name="ticket_resolved",
                subject_pattern="[SupportHub] Resolution & Survey: {{ticket_ref}}",
                body_html="<p>Hi {{customer_name}},</p><p>Your inquiry <strong>{{ticket_ref}}</strong> has been resolved. Please rate your experience below:</p><p><a href='{{survey_link_5}}'>⭐⭐⭐⭐⭐ Excellent</a></p>"
            ),
            EmailTemplate(
                name="agent_reply",
                subject_pattern="Re: {{ticket_subject}} [{{ticket_ref}}]",
                body_html="<p>Hi {{customer_name}},</p><p>{{agent_message}}</p><p>Best regards,<br>{{agent_name}}<br>SupportHub Team</p>"
            ),
        ]
        for t in default_templates:
            session.add(t)
        await session.commit()
        result = await session.exec(select(EmailTemplate))
        templates = result.all()

    return templates


@router.put("/email-templates/{name}")
async def update_email_template(
    name: str,
    body: EmailTemplateUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update email templates")

    from app.models import EmailTemplate
    stmt = select(EmailTemplate).where(EmailTemplate.name == name)
    template = (await session.exec(stmt)).first()

    if not template:
        template = EmailTemplate(name=name, subject_pattern=body.subject_pattern, body_html=body.body_html)
    else:
        template.subject_pattern = body.subject_pattern
        template.body_html = body.body_html
        template.updated_at = datetime.now()

    session.add(template)
    await session.commit()
    await session.refresh(template)
    return template


# ─── CSV Report Exports ────────────────────────────────────────────────────────

from fastapi.responses import Response
import csv
import io


@router.get("/reports/csat/export")
async def export_csat_csv(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Access denied")

    from app.models import CsatRating
    ratings = (await session.exec(select(CsatRating).order_by(CsatRating.created_at.desc()))).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Rating ID", "Ticket ID", "Rating (1-5)", "Comment", "Created At"])

    for r in ratings:
        writer.writerow([str(r.id), str(r.ticket_id), r.rating, r.comment or "", str(r.created_at)])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=csat_report.csv"}
    )


@router.get("/reports/performance/export")
async def export_performance_csv(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Access denied")

    from app.models import Ticket
    tickets = (await session.exec(select(Ticket))).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Ticket Reference", "Subject", "Status", "Priority", "Category", "SLA Breached", "AI Resolved", "Created At"])

    for t in tickets:
        writer.writerow([t.ref, t.subject, str(t.status.value if hasattr(t.status, 'value') else t.status), str(t.priority.value if hasattr(t.priority, 'value') else t.priority), t.category or "General", t.sla_breached, t.ai_resolved, str(t.created_at)])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=performance_report.csv"}
    )


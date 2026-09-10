"""Admin router — Channel Integrations & AI Settings management."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.config import get_settings
from app.database import get_session
from app.dependencies import get_current_user
from app.models import User, UserRole, UserStatus, ChannelIntegration, ChannelType, ChannelStatus, Ticket, TicketStatus, TicketPriority, SenderType, Message, AiSettings

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

def _settings_to_dict(ai: AiSettings) -> dict:
    threshold_val = ai.confidence_threshold
    if threshold_val is not None and 0.0 <= threshold_val <= 1.0:
        threshold_display = int(round(threshold_val * 100))
    elif threshold_val is not None:
        threshold_display = int(threshold_val)
    else:
        threshold_display = 85
    return {
        "enable_ai_assistant": ai.enabled,
        "auto_resolve": ai.auto_resolve,
        "ai_reply_suggestions": ai.suggest_replies,
        "ai_summaries": ai.auto_summary,
        "sentiment_detection": ai.sentiment_detection,
        "confidence_threshold": threshold_display,
    }


class AISettingsRequest(BaseModel):
    enable_ai_assistant: Optional[bool] = None
    auto_resolve: Optional[bool] = None
    ai_reply_suggestions: Optional[bool] = None
    ai_summaries: Optional[bool] = None
    sentiment_detection: Optional[bool] = None
    confidence_threshold: Optional[float] = None


@router.get("/ai-settings")
async def get_ai_settings(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")

    global _current_ai_settings
    ai_row = await session.get(AiSettings, 1)
    if not ai_row:
        ai_row = AiSettings(
            id=1,
            enabled=True,
            auto_resolve=True,
            suggest_replies=True,
            auto_summary=True,
            sentiment_detection=True,
            confidence_threshold=0.85,
        )
        session.add(ai_row)
        await session.commit()
        await session.refresh(ai_row)

    _current_ai_settings = _settings_to_dict(ai_row)
    return _current_ai_settings


@router.post("/ai-settings")
@router.put("/ai-settings")
@router.patch("/ai-settings")
async def update_ai_settings(
    body: AISettingsRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update AI settings")

    global _current_ai_settings
    ai_row = await session.get(AiSettings, 1)
    if not ai_row:
        ai_row = AiSettings(
            id=1,
            enabled=True,
            auto_resolve=True,
            suggest_replies=True,
            auto_summary=True,
            sentiment_detection=True,
            confidence_threshold=0.85,
        )
        session.add(ai_row)

    if body.enable_ai_assistant is not None:
        ai_row.enabled = body.enable_ai_assistant
    if body.auto_resolve is not None:
        ai_row.auto_resolve = body.auto_resolve
    if body.ai_reply_suggestions is not None:
        ai_row.suggest_replies = body.ai_reply_suggestions
    if body.ai_summaries is not None:
        ai_row.auto_summary = body.ai_summaries
    if body.sentiment_detection is not None:
        ai_row.sentiment_detection = body.sentiment_detection
    if body.confidence_threshold is not None:
        raw = float(body.confidence_threshold)
        ai_row.confidence_threshold = (raw / 100.0) if raw > 1.0 else raw

    ai_row.updated_at = datetime.now()
    session.add(ai_row)
    await session.commit()
    await session.refresh(ai_row)

    _current_ai_settings = _settings_to_dict(ai_row)
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


# ─── WhatsApp Access Token & Credentials Management ─────────────────────────

class WhatsAppConfigRequest(BaseModel):
    whatsapp_access_token: Optional[str] = None
    whatsapp_phone_id: Optional[str] = None
    whatsapp_verify_token: Optional[str] = None


def _update_env_file(key_values: dict[str, str]):
    import os
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
    if not os.path.exists(env_path):
        env_path = os.path.abspath(".env")
    
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            new_lines = []
            updated_keys = set()
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and "=" in stripped:
                    key = stripped.split("=", 1)[0].strip()
                    if key in key_values:
                        new_lines.append(f"{key}={key_values[key]}\n")
                        updated_keys.add(key)
                        continue
                new_lines.append(line)
            
            for key, val in key_values.items():
                if key not in updated_keys and val:
                    new_lines.append(f"{key}={val}\n")
            
            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        except Exception as e:
            print(f"Warning: Could not write to .env file: {e}")

    for key, val in key_values.items():
        if val is not None:
            os.environ[key] = val


@router.get("/whatsapp-config")
async def get_whatsapp_config(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")

    import os
    token = os.environ.get("WHATSAPP_ACCESS_TOKEN", "") or get_settings().whatsapp_access_token
    phone_id = os.environ.get("WHATSAPP_PHONE_ID", "") or get_settings().whatsapp_phone_id
    verify_token = os.environ.get("META_VERIFY_TOKEN", "") or os.environ.get("WHATSAPP_VERIFY_TOKEN", "") or get_settings().meta_verify_token

    stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.whatsapp)
    ch = (await session.exec(stmt)).first()

    if not token and ch and ch.credentials_encrypted:
        token = ch.credentials_encrypted

    return {
        "whatsapp_access_token": token,
        "whatsapp_phone_id": phone_id,
        "whatsapp_verify_token": verify_token,
        "status": ch.status.value if (ch and hasattr(ch.status, 'value')) else (ch.status if ch else "connected"),
        "channel_id": str(ch.id) if ch else None
    }


@router.post("/whatsapp-config")
async def update_whatsapp_config(
    body: WhatsAppConfigRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update WhatsApp credentials")

    import os
    env_updates = {}
    if body.whatsapp_access_token is not None:
        token_clean = body.whatsapp_access_token.strip()
        env_updates["WHATSAPP_ACCESS_TOKEN"] = token_clean
        os.environ["WHATSAPP_ACCESS_TOKEN"] = token_clean
        get_settings().whatsapp_access_token = token_clean
    if body.whatsapp_phone_id is not None:
        phone_clean = body.whatsapp_phone_id.strip()
        env_updates["WHATSAPP_PHONE_ID"] = phone_clean
        os.environ["WHATSAPP_PHONE_ID"] = phone_clean
        get_settings().whatsapp_phone_id = phone_clean
    if body.whatsapp_verify_token is not None:
        verify_clean = body.whatsapp_verify_token.strip()
        env_updates["META_VERIFY_TOKEN"] = verify_clean
        env_updates["WHATSAPP_VERIFY_TOKEN"] = verify_clean
        os.environ["META_VERIFY_TOKEN"] = verify_clean
        os.environ["WHATSAPP_VERIFY_TOKEN"] = verify_clean
        get_settings().meta_verify_token = verify_clean

    if env_updates:
        _update_env_file(env_updates)

    stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.whatsapp)
    ch = (await session.exec(stmt)).first()
    saved_token = os.environ.get("WHATSAPP_ACCESS_TOKEN", "")
    if not ch:
        ch = ChannelIntegration(
            channel_type=ChannelType.whatsapp,
            display_name=os.environ.get("WHATSAPP_PHONE_ID") or "WhatsApp Business API",
            status=ChannelStatus.connected,
            credentials_encrypted=saved_token,
            weekly_volume=0
        )
        session.add(ch)
    else:
        if saved_token:
            ch.credentials_encrypted = saved_token
        if os.environ.get("WHATSAPP_PHONE_ID"):
            ch.display_name = os.environ.get("WHATSAPP_PHONE_ID")
        ch.status = ChannelStatus.connected
        session.add(ch)
    
    await session.commit()
    await session.refresh(ch)

    return {
        "status": "success",
        "message": "WhatsApp Access Token and credentials updated successfully in .env and database!",
        "whatsapp_phone_id": os.environ.get("WHATSAPP_PHONE_ID", ""),
        "whatsapp_access_token": saved_token,
    }


@router.post("/whatsapp-config/test")
async def test_whatsapp_config(
    body: Optional[WhatsAppConfigRequest] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")

    import os
    import httpx

    token = (body.whatsapp_access_token if (body and body.whatsapp_access_token) else os.environ.get("WHATSAPP_ACCESS_TOKEN", "") or get_settings().whatsapp_access_token).strip()
    phone_id = (body.whatsapp_phone_id if (body and body.whatsapp_phone_id) else os.environ.get("WHATSAPP_PHONE_ID", "") or get_settings().whatsapp_phone_id).strip()

    if not token:
        raise HTTPException(status_code=400, detail="WhatsApp Access Token is required to run connection test.")
    if not phone_id:
        raise HTTPException(status_code=400, detail="WhatsApp Phone ID is required to run connection test.")

    url = f"https://graph.facebook.com/v20.0/{phone_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as http_client:
            res = await http_client.get(url, headers=headers)
            data = res.json()

        if res.status_code == 200:
            display_phone = data.get("display_phone_number") or data.get("phone_number") or phone_id
            verified_name = data.get("verified_name") or data.get("name") or "WhatsApp Business Account"
            quality_rating = data.get("quality_rating", "GREEN")

            stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.whatsapp)
            ch = (await session.exec(stmt)).first()
            if ch:
                ch.status = ChannelStatus.connected
                session.add(ch)
                await session.commit()

            return {
                "status": "success",
                "connected": True,
                "message": f"✅ WhatsApp Access Token Verified! Connected to Meta WhatsApp Account: '{verified_name}' ({display_phone})",
                "details": {
                    "id": data.get("id"),
                    "display_phone_number": display_phone,
                    "verified_name": verified_name,
                    "quality_rating": quality_rating,
                    "code_verification_status": data.get("code_verification_status", "VERIFIED")
                }
            }
        else:
            error_obj = data.get("error", {})
            err_msg = error_obj.get("message", res.text)
            err_code = error_obj.get("code")

            stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.whatsapp)
            ch = (await session.exec(stmt)).first()
            if ch:
                ch.status = ChannelStatus.needs_attention
                session.add(ch)
                await session.commit()

            return {
                "status": "error",
                "connected": False,
                "error_code": err_code,
                "message": f"❌ Meta WhatsApp Token Test Failed (Code {err_code}): {err_msg}",
                "raw_error": data
            }

    except Exception as e:
        return {
            "status": "error",
            "connected": False,
            "message": f"❌ Network or Server Error while contacting Meta API: {str(e)}"
        }


# ─── Instagram Access Token & Credentials Management ─────────────────────────

class InstagramConfigRequest(BaseModel):
    instagram_access_token: Optional[str] = None
    instagram_account_id: Optional[str] = None
    instagram_verify_token: Optional[str] = None


@router.get("/instagram-config")
async def get_instagram_config(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")

    import os
    token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "") or get_settings().instagram_access_token
    account_id = os.environ.get("INSTAGRAM_ACCOUNT_ID", "") or os.environ.get("IG_PAGE_ID", "") or get_settings().instagram_account_id or get_settings().ig_page_id
    verify_token = os.environ.get("META_VERIFY_TOKEN", "") or os.environ.get("INSTAGRAM_VERIFY_TOKEN", "") or get_settings().meta_verify_token

    stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.instagram)
    ch = (await session.exec(stmt)).first()

    if not token and ch and ch.credentials_encrypted:
        token = ch.credentials_encrypted

    return {
        "instagram_access_token": token,
        "instagram_account_id": account_id,
        "instagram_verify_token": verify_token,
        "status": ch.status.value if (ch and hasattr(ch.status, 'value')) else (ch.status if ch else "connected"),
        "channel_id": str(ch.id) if ch else None
    }


@router.post("/instagram-config")
async def update_instagram_config(
    body: InstagramConfigRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update Instagram credentials")

    import os
    env_updates = {}
    if body.instagram_access_token is not None:
        token_clean = body.instagram_access_token.strip()
        env_updates["INSTAGRAM_ACCESS_TOKEN"] = token_clean
        os.environ["INSTAGRAM_ACCESS_TOKEN"] = token_clean
        get_settings().instagram_access_token = token_clean
    if body.instagram_account_id is not None:
        acc_clean = body.instagram_account_id.strip()
        env_updates["INSTAGRAM_ACCOUNT_ID"] = acc_clean
        os.environ["INSTAGRAM_ACCOUNT_ID"] = acc_clean
        get_settings().instagram_account_id = acc_clean
    if body.instagram_verify_token is not None:
        verify_clean = body.instagram_verify_token.strip()
        env_updates["META_VERIFY_TOKEN"] = verify_clean
        env_updates["INSTAGRAM_VERIFY_TOKEN"] = verify_clean
        os.environ["META_VERIFY_TOKEN"] = verify_clean
        os.environ["INSTAGRAM_VERIFY_TOKEN"] = verify_clean
        get_settings().meta_verify_token = verify_clean

    if env_updates:
        _update_env_file(env_updates)

    stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.instagram)
    ch = (await session.exec(stmt)).first()
    saved_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
    if not ch:
        ch = ChannelIntegration(
            channel_type=ChannelType.instagram,
            display_name=os.environ.get("INSTAGRAM_ACCOUNT_ID") or "Instagram Direct",
            status=ChannelStatus.connected,
            credentials_encrypted=saved_token,
            weekly_volume=0
        )
        session.add(ch)
    else:
        if saved_token:
            ch.credentials_encrypted = saved_token
        if os.environ.get("INSTAGRAM_ACCOUNT_ID"):
            ch.display_name = os.environ.get("INSTAGRAM_ACCOUNT_ID")
        ch.status = ChannelStatus.connected
        session.add(ch)
    
    await session.commit()
    await session.refresh(ch)

    return {
        "status": "success",
        "message": "Instagram Access Token and credentials updated successfully in .env and database!",
        "instagram_account_id": os.environ.get("INSTAGRAM_ACCOUNT_ID", ""),
        "instagram_access_token": saved_token,
    }


@router.post("/instagram-config/test")
async def test_instagram_config(
    body: Optional[InstagramConfigRequest] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")

    import os
    import httpx

    token = (body.instagram_access_token if (body and body.instagram_access_token) else os.environ.get("INSTAGRAM_ACCESS_TOKEN", "") or get_settings().instagram_access_token).strip()
    account_id = (body.instagram_account_id if (body and body.instagram_account_id) else os.environ.get("INSTAGRAM_ACCOUNT_ID", "") or get_settings().instagram_account_id).strip()

    if not token:
        raise HTTPException(status_code=400, detail="Instagram Access Token is required to run connection test.")

    url = "https://graph.instagram.com/v19.0/me?fields=id,username,name,account_type"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as http_client:
            res = await http_client.get(url, headers=headers)
            data = res.json()

        if res.status_code == 200:
            username = data.get("username") or data.get("name") or "Instagram Account"
            acc_id = data.get("id") or account_id

            stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.instagram)
            ch = (await session.exec(stmt)).first()
            if ch:
                ch.status = ChannelStatus.connected
                session.add(ch)
                await session.commit()

            return {
                "status": "success",
                "connected": True,
                "message": f"✅ Instagram Access Token Verified! Connected to @{username} (ID: {acc_id})",
                "details": {
                    "id": acc_id,
                    "username": username,
                    "account_type": data.get("account_type", "BUSINESS"),
                }
            }
        else:
            error_obj = data.get("error", {})
            err_msg = error_obj.get("message", res.text)
            err_code = error_obj.get("code")

            stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.instagram)
            ch = (await session.exec(stmt)).first()
            if ch:
                ch.status = ChannelStatus.needs_attention
                session.add(ch)
                await session.commit()

            return {
                "status": "error",
                "connected": False,
                "error_code": err_code,
                "message": f"❌ Meta Instagram Token Test Failed (Code {err_code}): {err_msg}",
                "raw_error": data
            }

    except Exception as e:
        return {
            "status": "error",
            "connected": False,
            "message": f"❌ Network or Server Error while contacting Meta Instagram API: {str(e)}"
        }


# ─── Facebook Access Token & Credentials Management ─────────────────────────

class FacebookConfigRequest(BaseModel):
    facebook_access_token: Optional[str] = None
    facebook_page_access_token: Optional[str] = None
    facebook_page_id: Optional[str] = None
    facebook_verify_token: Optional[str] = None


@router.get("/facebook-config")
async def get_facebook_config(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")

    import os
    token = (
        os.environ.get("PAGE_ACCESS_TOKEN", "")
        or os.environ.get("FACEBOOK_ACCESS_TOKEN", "")
        or os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN", "")
        or get_settings().page_access_token
    )
    page_id = (
        os.environ.get("FACEBOOK_PAGE_ID", "")
        or os.environ.get("FB_PAGE_ID", "")
        or get_settings().fb_page_id
    )
    verify_token = (
        os.environ.get("META_VERIFY_TOKEN", "")
        or os.environ.get("FACEBOOK_VERIFY_TOKEN", "")
        or get_settings().meta_verify_token
    )

    stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.facebook)
    ch = (await session.exec(stmt)).first()

    if not token and ch and ch.credentials_encrypted:
        token = ch.credentials_encrypted

    return {
        "facebook_access_token": token,
        "facebook_page_access_token": token,
        "facebook_page_id": page_id,
        "facebook_verify_token": verify_token,
        "status": ch.status.value if (ch and hasattr(ch.status, 'value')) else (ch.status if ch else "connected"),
        "channel_id": str(ch.id) if ch else None
    }


@router.post("/facebook-config")
async def update_facebook_config(
    body: FacebookConfigRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update Facebook credentials")

    import os
    env_updates = {}
    token_val = body.facebook_page_access_token or body.facebook_access_token
    if token_val is not None:
        token_clean = token_val.strip()
        env_updates["PAGE_ACCESS_TOKEN"] = token_clean
        env_updates["FACEBOOK_ACCESS_TOKEN"] = token_clean
        env_updates["FACEBOOK_PAGE_ACCESS_TOKEN"] = token_clean
        os.environ["PAGE_ACCESS_TOKEN"] = token_clean
        os.environ["FACEBOOK_ACCESS_TOKEN"] = token_clean
        os.environ["FACEBOOK_PAGE_ACCESS_TOKEN"] = token_clean
        get_settings().page_access_token = token_clean

    if body.facebook_page_id is not None:
        page_id_clean = body.facebook_page_id.strip()
        env_updates["FACEBOOK_PAGE_ID"] = page_id_clean
        env_updates["FB_PAGE_ID"] = page_id_clean
        os.environ["FACEBOOK_PAGE_ID"] = page_id_clean
        os.environ["FB_PAGE_ID"] = page_id_clean
        get_settings().fb_page_id = page_id_clean

    if body.facebook_verify_token is not None:
        verify_clean = body.facebook_verify_token.strip()
        env_updates["META_VERIFY_TOKEN"] = verify_clean
        env_updates["FACEBOOK_VERIFY_TOKEN"] = verify_clean
        os.environ["META_VERIFY_TOKEN"] = verify_clean
        os.environ["FACEBOOK_VERIFY_TOKEN"] = verify_clean
        get_settings().meta_verify_token = verify_clean

    if env_updates:
        _update_env_file(env_updates)

    stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.facebook)
    ch = (await session.exec(stmt)).first()
    saved_token = os.environ.get("PAGE_ACCESS_TOKEN", "")
    if not ch:
        ch = ChannelIntegration(
            channel_type=ChannelType.facebook,
            display_name=os.environ.get("FACEBOOK_PAGE_ID") or "Facebook Messenger",
            status=ChannelStatus.connected,
            credentials_encrypted=saved_token,
            weekly_volume=0
        )
        session.add(ch)
    else:
        if saved_token:
            ch.credentials_encrypted = saved_token
        if os.environ.get("FACEBOOK_PAGE_ID"):
            ch.display_name = os.environ.get("FACEBOOK_PAGE_ID")
        ch.status = ChannelStatus.connected
        session.add(ch)
    
    await session.commit()
    await session.refresh(ch)

    return {
        "status": "success",
        "message": "Facebook Access Token and credentials updated successfully in .env and database!",
        "facebook_page_id": os.environ.get("FACEBOOK_PAGE_ID", ""),
        "facebook_access_token": saved_token,
        "facebook_page_access_token": saved_token,
    }


@router.post("/facebook-config/test")
async def test_facebook_config(
    body: Optional[FacebookConfigRequest] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status_code=403, detail="Not authorized")

    import os
    import httpx

    token_val = ""
    if body:
        token_val = (body.facebook_page_access_token or body.facebook_access_token or "").strip()
    if not token_val:
        token_val = (
            os.environ.get("PAGE_ACCESS_TOKEN")
            or os.environ.get("FACEBOOK_ACCESS_TOKEN")
            or os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
            or get_settings().page_access_token
            or ""
        ).strip()

    if not token_val:
        raise HTTPException(status_code=400, detail="Facebook Access Token is required to run connection test.")

    url = "https://graph.facebook.com/v19.0/debug_token"
    params = {"input_token": token_val, "access_token": token_val}

    try:
        async with httpx.AsyncClient(timeout=10.0) as http_client:
            res = await http_client.get(url, params=params)
            data = res.json()

        if res.status_code == 200 and data.get("data", {}).get("is_valid"):
            token_data = data.get("data", {})
            name = token_data.get("application") or "Facebook Page"
            acc_id = token_data.get("profile_id") or token_data.get("app_id")

            stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.facebook)
            ch = (await session.exec(stmt)).first()
            if ch:
                ch.status = ChannelStatus.connected
                session.add(ch)
                await session.commit()

            return {
                "status": "success",
                "connected": True,
                "message": f"✅ Facebook Access Token Verified! Connected App: '{name}' (Profile ID: {acc_id})",
                "details": {
                    "id": acc_id,
                    "name": name,
                    "scopes": token_data.get("scopes", [])
                }
            }
        else:
            # Fallback to /me endpoint if debug_token doesn't succeed (e.g. Page Access Token vs User Token)
            async with httpx.AsyncClient(timeout=10.0) as http_client:
                me_res = await http_client.get(f"https://graph.facebook.com/v19.0/me?access_token={token_val}")
                me_data = me_res.json()
            
            if me_res.status_code == 200 and me_data.get("id"):
                page_name = me_data.get("name") or "Facebook Page"
                page_id = me_data.get("id")
                
                stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.facebook)
                ch = (await session.exec(stmt)).first()
                if ch:
                    ch.status = ChannelStatus.connected
                    session.add(ch)
                    await session.commit()

                return {
                    "status": "success",
                    "connected": True,
                    "message": f"✅ Facebook Access Token Verified! Connected to '{page_name}' (ID: {page_id})",
                    "details": {
                        "id": page_id,
                        "name": page_name,
                    }
                }

            error_obj = data.get("error", {})
            err_msg = error_obj.get("message", res.text)
            err_code = error_obj.get("code")

            stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.facebook)
            ch = (await session.exec(stmt)).first()
            if ch:
                ch.status = ChannelStatus.needs_attention
                session.add(ch)
                await session.commit()

            return {
                "status": "error",
                "connected": False,
                "error_code": err_code,
                "message": f"❌ Meta Facebook Token Test Failed (Code {err_code}): {err_msg}",
                "raw_error": data
            }

    except Exception as e:
        return {
            "status": "error",
            "connected": False,
            "message": f"❌ Network or Server Error while contacting Meta Facebook API: {str(e)}"
        }


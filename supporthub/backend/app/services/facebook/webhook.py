"""
app/services/facebook/webhook.py

Background Orchestration and Database Storage for Incoming Facebook Messenger Webhooks.
Decoupled from HTTP request lifecycle and strict about avoiding AI / outbound calls in this phase.
"""

import random
import logging
import json
from datetime import datetime
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
import httpx

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models import (
    Message,
    SenderType,
    Ticket,
    TicketChannel,
    TicketPriority,
    TicketStatus,
    User,
    UserRole,
    UserStatus,
    WebhookEvent,
    ChannelType,
)
from app.services.senders import send_messenger_reply
from app.services.ai.orchestrator import AIOrchestrator
from app.services.ai.knowledge_rag import get_relevant_kb_context
from app.services.channels.media import GenericMediaDownloader

logger = logging.getLogger(__name__)
settings = get_settings()


def generate_ticket_ref() -> str:
    """Generate a random unique ticket reference code."""
    return f"TCK-{random.randint(10000, 99999)}"


async def process_facebook_webhook_background(payload: dict[str, Any]) -> None:
    """
    Background worker function for Facebook Messenger webhooks.
    """
    logger.info("[FB WEBHOOK] Background task started | object=%s", payload.get("object"))

    if not isinstance(payload, dict):
        logger.warning("[FB WEBHOOK] Non-dict payload received — skipped.")
        return

    entries = payload.get("entry", [])
    if not entries:
        logger.debug("[FB WEBHOOK] Payload ignored: no entries found.")
        return

    async with AsyncSessionLocal() as db_session:
        for entry in entries:
            entry_page_id = str(entry.get("id", "")).strip()
            logger.info("[FB WEBHOOK] Processing entry | page_id=%s", entry_page_id)

            messaging_events = entry.get("messaging", [])
            for event in messaging_events:
                await _process_single_facebook_event(
                    db_session=db_session,
                    event=event,
                    entry_page_id=entry_page_id,
                )


async def _process_single_facebook_event(
    db_session: AsyncSession,
    event: dict[str, Any],
    entry_page_id: str,
) -> None:
    """Process a single messaging event dictionary from Facebook Messenger."""
    sender_info = event.get("sender", {})
    recipient_info = event.get("recipient", {})
    message_info = event.get("message", {})

    sender_id = str(sender_info.get("id", "")).strip()
    recipient_id = str(recipient_info.get("id", "")).strip()
    message_mid = str(message_info.get("mid", "")).strip()
    text_body = message_info.get("text", "").strip() if message_info.get("text") else ""

    # Safe validation for unsupported event types, echos, or empty message IDs
    if not sender_id or message_info.get("is_echo"):
        logger.debug("[FB WEBHOOK] Skipping echo or empty event | mid=%s", message_mid)
        return

    if not message_mid:
        # Some events like deliveries don't have mid in 'message' but in 'delivery'
        logger.debug("[FB WEBHOOK] Skipping non-message event.")
        return

    # Download attachments if present
    # Facebook CDN URLs are access-token-protected, so the local download may fail.
    # We always fall back to using the raw URL so attachment-only messages are never dropped.
    attachments = message_info.get("attachments", [])
    has_any_attachment = False
    if attachments:
        for att in attachments:
            att_type = att.get("type", "file")
            att_payload = att.get("payload", {})
            att_url = att_payload.get("url")
            
            if att_url:
                has_any_attachment = True
                # Try local download first (works when URL is publicly accessible)
                local_url, filename = await GenericMediaDownloader.download_url(url=att_url)
                if local_url and filename:
                    # Successfully downloaded — use local URL
                    markdown = f"\n📎 [Attachment: {att_type}]({local_url})"
                else:
                    # Download failed (auth-protected FB CDN) — use raw CDN URL as fallback
                    logger.info("[FB WEBHOOK] Could not download attachment locally, using raw CDN URL | type=%s", att_type)
                    markdown = f"\n📎 [Attachment: {att_type}]({att_url})"
                text_body = (text_body + markdown).strip()

    logger.info(
        "[FB WEBHOOK] Event received | sender=%s | recipient=%s | page_id=%s | mid=%s | has_text=%s | has_attachment=%s",
        sender_id,
        recipient_id,
        entry_page_id,
        message_mid,
        bool(message_info.get("text", "").strip()),
        has_any_attachment,
    )

    # Skip event only if there is truly nothing to process
    if not text_body and not has_any_attachment:
        logger.info("[FB WEBHOOK] Ignoring message %s: empty text body and no attachments.", message_mid)
        return

    # ──────────────────────────────────────────────────────────────────────────
    # Step 1: Strict Idempotency Check & Claim via WebhookEvent
    # ──────────────────────────────────────────────────────────────────────────
    try:
        stmt_event = select(WebhookEvent).where(
            WebhookEvent.event_id == message_mid,
            WebhookEvent.channel == ChannelType.facebook,
        )
        existing_event = (await db_session.exec(stmt_event)).first()
        if existing_event:
            if existing_event.processed:
                logger.info("[FB WEBHOOK] ⚡ Duplicate skipped | mid=%s | processed=True", message_mid)
                return
            webhook_evt = existing_event
            logger.info("[FB WEBHOOK] Retrying previously uncompleted event | event_db_id=%s | mid=%s", webhook_evt.id, message_mid)
        else:
            webhook_evt = WebhookEvent(
                event_id=message_mid,
                channel=ChannelType.facebook,
                processed=False,
                raw_payload=json.dumps(event),
            )
            db_session.add(webhook_evt)
            await db_session.commit()
            await db_session.refresh(webhook_evt)
            logger.info("[FB WEBHOOK] WebhookEvent claimed | event_db_id=%s | mid=%s", webhook_evt.id, message_mid)

    except IntegrityError:
        await db_session.rollback()
        logger.info("[FB WEBHOOK] ⚡ Race condition — duplicate mid=%s", message_mid)
        return
    except Exception as exc:
        await db_session.rollback()
        logger.error("[FB WEBHOOK] ❌ Idempotency failure | mid=%s | error=%s", message_mid, exc, exc_info=True)
        return

    # ──────────────────────────────────────────────────────────────────────────
    # Step 2: Customer User, Ticket, and Message Resolution
    # ──────────────────────────────────────────────────────────────────────────
    try:
        # Find or Create Customer User
        synthetic_email = f"messenger_{sender_id[:100]}@supporthub.local"[:255]
        user_stmt = select(User).where(
            (User.channel_customer_id == sender_id) | (User.email == synthetic_email)
        )
        user = (await db_session.exec(user_stmt)).first()

        # Query live Meta Graph API for customer profile
        actual_name = ""
        avatar_url = ""
        token = settings.page_access_token
        
        if token and sender_id:
            async with httpx.AsyncClient(timeout=10.0) as client:
                try:
                    url = f"https://graph.facebook.com/v19.0/{sender_id}"
                    params = {"fields": "first_name,last_name,profile_pic", "access_token": token}
                    resp = await client.get(url, params=params)
                    if resp.status_code == 200:
                        profile_data = resp.json()
                        first_name = profile_data.get("first_name", "")
                        last_name = profile_data.get("last_name", "")
                        actual_name = f"{first_name} {last_name}".strip()
                        avatar_url = profile_data.get("profile_pic", "")
                except Exception as exc:
                    logger.warning("[FB WEBHOOK] Could not fetch profile for %s (Strategy A): %s", sender_id, exc)

                # Fallback to conversations endpoint if name is missing
                if not actual_name:
                    try:
                        url = "https://graph.facebook.com/v19.0/me/conversations"
                        params = {"user_id": sender_id, "fields": "senders", "access_token": token}
                        resp = await client.get(url, params=params)
                        if resp.status_code == 200:
                            data = resp.json().get("data", [])
                            if data:
                                senders = data[0].get("senders", {}).get("data", [])
                                for s in senders:
                                    if s.get("id") == sender_id:
                                        actual_name = s.get("name", "")
                                        break
                    except Exception as exc:
                        logger.warning("[FB WEBHOOK] Could not fetch profile for %s (Strategy B): %s", sender_id, exc)

        actual_name = actual_name or (user.name if user and not user.name.startswith("Messenger User") else None) or f"Messenger User ({sender_id[:8]})"
        
        if not avatar_url and not (user and user.avatar_url):
            bg_color = "1877F2"
            encoded_name = actual_name.replace(" ", "+")
            avatar_url = f"https://ui-avatars.com/api/?name={encoded_name}&background={bg_color}&color=fff&size=128&rounded=true"
        elif not avatar_url and user:
            avatar_url = user.avatar_url

        if not user:
            logger.info("[FB WEBHOOK] Creating new User for sender=%s (name=%s)", sender_id, actual_name)
            user = User(
                email=synthetic_email,
                name=actual_name[:100],
                password_hash=f"external_messenger_{sender_id}"[:255],
                role=UserRole.customer,
                status=UserStatus.active,
                channel=ChannelType.facebook,
                channel_customer_id=sender_id,
                avatar_url=avatar_url,
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
        else:
            user_dirty = False
            if not user.channel_customer_id:
                user.channel_customer_id = sender_id
                user_dirty = True
            if user.channel != ChannelType.facebook:
                user.channel = ChannelType.facebook
                user_dirty = True
            if actual_name and (user.name != actual_name or user.name.startswith("Messenger User")):
                user.name = actual_name[:100]
                user_dirty = True
            if avatar_url and user.avatar_url != avatar_url:
                user.avatar_url = avatar_url
                user_dirty = True

            if user_dirty:
                db_session.add(user)
                await db_session.commit()
                await db_session.refresh(user)

        # Enforce single-ticket policy for Facebook Messenger
        ticket_stmt = (
            select(Ticket)
            .where(
                Ticket.customer_id == user.id,
                Ticket.channel == TicketChannel.facebook,
                Ticket.deleted_at.is_(None),
            )
            .order_by(Ticket.created_at.desc())
        )
        ticket = (await db_session.exec(ticket_stmt)).first()

        if not ticket:
            ticket = Ticket(
                ref=generate_ticket_ref(),
                customer_id=user.id,
                subject=f"Messenger from {user.name}",
                category="messenger",
                channel=TicketChannel.facebook,
                status=TicketStatus.new,
                priority=TicketPriority.medium,
            )
            db_session.add(ticket)
            await db_session.commit()
            await db_session.refresh(ticket)
        else:
            if ticket.status in [TicketStatus.resolved, TicketStatus.closed]:
                ticket.status = TicketStatus.open
            if "Messenger from " in ticket.subject and (sender_id[:8] in ticket.subject or "Messenger User" in ticket.subject):
                ticket.subject = f"Messenger from {user.name}"
            ticket.updated_at = datetime.now()
            db_session.add(ticket)
            await db_session.commit()
            await db_session.refresh(ticket)

        # Save Customer Message
        cust_msg = Message(
            ticket_id=ticket.id,
            sender_id=user.id,
            sender_type=SenderType.customer,
            body=text_body,
            external_message_id=message_mid,
        )
        db_session.add(cust_msg)

        # Mark WebhookEvent as processed
        webhook_evt.processed = True
        db_session.add(webhook_evt)

        await db_session.commit()
        await db_session.refresh(cust_msg)

        # ──────────────────────────────────────────────────────────────────────────
        # Step 3: Real-Time WebSocket Broadcast
        # ──────────────────────────────────────────────────────────────────────────
        try:
            from app.ws.manager import manager
            ticket_id_str = str(ticket.id)

            await manager.broadcast(ticket_id_str, {
                "type": "message",
                "id": str(cust_msg.id),
                "ticket_id": ticket_id_str,
                "sender_id": str(user.id),
                "sender_name": user.name or f"Messenger User ({sender_id})",
                "sender_role": "customer",
                "sender_type": "customer",
                "body": text_body,
                "created_at": cust_msg.created_at.isoformat() if cust_msg.created_at else "",
                "external_message_id": message_mid,
            })

            await manager.broadcast_to_agents({
                "type": "inbox_update",
                "ticket_id": ticket_id_str,
                "preview": text_body[:80],
                "sender_name": user.name or f"Messenger User ({sender_id})",
                "subject": ticket.subject,
                "status": ticket.status.value,
                "channel": ticket.channel.value,
            })
        except Exception as ws_err:
            logger.error("[FB REALTIME] broadcast failed | error=%s", ws_err, exc_info=True)

        # ──────────────────────────────────────────────────────────────────────────
        # Step 4: AI Auto-Reply Generation with Debounce
        # ──────────────────────────────────────────────────────────────────────────
        from app.services.ai.debouncer import ai_debouncer
        
        async def trigger_ai():
            await _execute_ai_for_facebook(ticket.id, sender_id, ticket_id_str)
            
        ai_debouncer.schedule(ticket_id_str, trigger_ai)

    except Exception as exc:
        await db_session.rollback()
        logger.error("[FB WEBHOOK] ❌ Error processing mid=%s: %s", message_mid, exc, exc_info=True)
        try:
            async with AsyncSessionLocal() as err_session:
                evt_stmt = select(WebhookEvent).where(
                    WebhookEvent.event_id == message_mid,
                    WebhookEvent.channel == ChannelType.facebook,
                )
                err_evt = (await err_session.exec(evt_stmt)).first()
                if err_evt:
                    err_evt.error = str(exc)[:500]
                    err_session.add(err_evt)
                    await err_session.commit()
        except Exception:
            pass


async def _execute_ai_for_facebook(ticket_id, sender_id: str, ticket_id_str: str):
    """
    Executes the AI orchestration for Facebook Messenger after the debounce timer expires.
    """
    try:
        from app.database import AsyncSessionLocal
        from app.models import Ticket, User, Message, SenderType
        from sqlmodel import select
        from app.services.ai.orchestrator import AIOrchestrator
        from app.ws.manager import manager
        
        async with AsyncSessionLocal() as db_session:
            ticket = await db_session.get(Ticket, ticket_id)
            if not ticket:
                return
            user = await db_session.get(User, ticket.customer_id)

            # 1. Fetch ALL conversational message history (including newest messages)
            msg_stmt = select(Message).where(Message.ticket_id == ticket.id).order_by(Message.created_at)
            msg_history = (await db_session.exec(msg_stmt)).all()

            # Find the most recent customer message text for KB search context
            last_cust = next((m for m in reversed(msg_history) if m.sender_type == SenderType.customer), None)
            text_body = last_cust.body if last_cust else ""

            # 2. Retrieve Knowledge Base RAG Context
            kb_context = await get_relevant_kb_context(db_session, text_body)

            # 3. Generate grounded AI response
            orchestrator = AIOrchestrator(session=db_session)
            ai_out = await orchestrator.generate_for_ticket(
                ticket=ticket,
                messages=msg_history,
                customer=user,
                kb_context=kb_context,
                tone="friendly",
            )

            if isinstance(ai_out, dict):
                ai_text = ai_out.get("suggested_reply") or ai_out.get("response_text") or ""
            else:
                ai_text = getattr(ai_out, "suggested_reply", None) or getattr(ai_out, "response_text", "")
                
            if ai_text:
                # 4. Deliver response to Meta Facebook Messenger API
                ext_msg_id = None
                recipient_id = user.channel_customer_id or sender_id
                
                delivery_success = await send_messenger_reply(recipient_id=recipient_id, text=ai_text)
                
                if delivery_success:
                    logger.info("[FB AUTO-AI] Sent AI reply to Facebook Messenger | recip=%s", recipient_id)
                else:
                    logger.warning("[FB AUTO-AI] FB Delivery returned unsuccessful")

                # 5. Store AI message in database
                ticket.updated_at = datetime.now()
                db_session.add(ticket)
                ai_msg = Message(
                    ticket_id=ticket.id,
                    sender_id=None,
                    sender_type=SenderType.ai,
                    body=ai_text,
                    external_message_id=ext_msg_id,
                )
                db_session.add(ai_msg)
                await db_session.commit()
                await db_session.refresh(ai_msg)

                # 6. Real-time WebSocket broadcast of AI message to dashboard
                await manager.broadcast(ticket_id_str, {
                    "type": "message",
                    "id": str(ai_msg.id),
                    "ticket_id": ticket_id_str,
                    "sender_id": "AI",
                    "sender_name": "Support AI",
                    "sender_role": "ai",
                    "sender_type": "ai",
                    "body": ai_text,
                    "created_at": ai_msg.created_at.isoformat() if ai_msg.created_at else "",
                    "external_message_id": ext_msg_id or "",
                })

                await manager.broadcast_to_agents({
                    "type": "inbox_update",
                    "ticket_id": ticket_id_str,
                    "preview": ai_text[:80],
                    "sender_name": "Support AI",
                    "subject": ticket.subject,
                    "status": ticket.status.value,
                    "channel": ticket.channel.value,
                })

    except Exception as ai_err:
        logger.error("[FB AUTO-AI] Failed to process auto-AI reply for ticket %s: %s", ticket_id, ai_err, exc_info=True)

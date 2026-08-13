"""
app/services/instagram/webhook.py

Background Orchestration and Database Storage for Incoming Instagram Webhooks.
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
from app.services.instagram.client import MetaInstagramClient
from app.services.ai.orchestrator import AIOrchestrator
from app.services.ai.knowledge_rag import get_relevant_kb_context

logger = logging.getLogger(__name__)
settings = get_settings()


def generate_ticket_ref() -> str:
    """Generate a random unique ticket reference code."""
    return f"TCK-{random.randint(10000, 99999)}"


async def process_instagram_webhook_background(payload: dict[str, Any]) -> None:
    """
    Background worker function for Instagram webhooks.
    Opens an independent AsyncSession, validates recipient ID, checks WebhookEvent idempotency,
    resolves/creates User & Ticket, and saves incoming customer Message.
    """
    logger.info("[IG WEBHOOK] Background task started | object=%s", payload.get("object"))

    if not isinstance(payload, dict):
        logger.warning("[IG WEBHOOK] Non-dict payload received — skipped.")
        return

    if payload.get("object") != "instagram":
        logger.debug("[IG WEBHOOK] Payload ignored: object=%r is not 'instagram'.", payload.get("object"))
        return

    entries = payload.get("entry", [])
    if not entries:
        logger.debug("[IG WEBHOOK] Payload ignored: no entries found.")
        return

    # Build valid account ID set from env
    configured_account_id = str(settings.instagram_account_id or "").strip()
    ig_page_id = str(getattr(settings, "ig_page_id", "") or "").strip()
    valid_account_ids = {x for x in [configured_account_id, ig_page_id] if x}

    logger.info("[IG WEBHOOK] Configured valid account IDs: %s", valid_account_ids)

    async with AsyncSessionLocal() as db_session:
        for entry in entries:
            entry_account_id = str(entry.get("id", "")).strip()
            logger.info("[IG WEBHOOK] Processing entry | entry_id=%s", entry_account_id)

            # Format 1: Direct entry.messaging list
            messaging_events = entry.get("messaging", [])
            for event in messaging_events:
                await _process_single_instagram_event(
                    db_session=db_session,
                    event=event,
                    entry_account_id=entry_account_id,
                    valid_account_ids=valid_account_ids,
                )

            # Format 2: Meta changes structure (entry.changes[].value)
            changes = entry.get("changes", [])
            for change in changes:
                field = change.get("field")
                value = change.get("value")
                if field == "messages" and isinstance(value, dict):
                    await _process_single_instagram_event(
                        db_session=db_session,
                        event=value,
                        entry_account_id=entry_account_id,
                        valid_account_ids=valid_account_ids,
                    )


async def _process_single_instagram_event(
    db_session: AsyncSession,
    event: dict[str, Any],
    entry_account_id: str,
    valid_account_ids: set,
) -> None:
    """Process a single messaging event dictionary from Instagram."""
    sender_info = event.get("sender", {})
    recipient_info = event.get("recipient", {})
    message_info = event.get("message", {})

    sender_id = str(sender_info.get("id", "")).strip()
    recipient_id = str(recipient_info.get("id", "")).strip()
    message_mid = str(message_info.get("mid", "")).strip()
    text_body = message_info.get("text", "").strip() if message_info.get("text") else ""

    # Download attachments if present
    attachments = message_info.get("attachments", [])
    if attachments:
        from app.services.channels.media import GenericMediaDownloader
        for att in attachments:
            att_payload = att.get("payload", {})
            att_url = att_payload.get("url")
            
            if att_url:
                local_url, filename = await GenericMediaDownloader.download_url(url=att_url)
                if local_url and filename:
                    markdown = f" 📎 [Attachment: {filename}]({local_url})"
                    text_body = (text_body + markdown).strip()

    logger.info(
        "[IG WEBHOOK] Event received | sender=%s | recipient=%s | entry_id=%s | mid=%s | is_echo=%s | has_text=%s",
        sender_id,
        recipient_id,
        entry_account_id,
        message_mid,
        message_info.get("is_echo"),
        bool(text_body),
    )

    # Safe validation for unsupported event types, echos, or empty message IDs
    if not sender_id or not message_mid or message_info.get("is_echo"):
        logger.debug("[IG WEBHOOK] Skipping echo/empty event | mid=%s", message_mid)
        return

    # Check recipient account verification
    if valid_account_ids:
        target_account_id = recipient_id or entry_account_id
        if target_account_id and target_account_id not in valid_account_ids:
            logger.info(
                "[IG WEBHOOK] SKIPPED — recipient %r not in valid accounts %s",
                target_account_id,
                valid_account_ids,
            )
            return
        logger.info(
            "[IG WEBHOOK] Recipient validation PASSED | target=%r | valid=%s",
            target_account_id,
            valid_account_ids,
        )

    # Skip event if text_body is empty (after processing attachments)
    if not text_body:
        logger.info("[IG WEBHOOK] Ignoring message %s: empty text body and no attachments.", message_mid)
        return

    # ──────────────────────────────────────────────────────────────────────────
    # Step 1: Strict Idempotency Check & Claim via WebhookEvent
    # ──────────────────────────────────────────────────────────────────────────
    try:
        stmt_event = select(WebhookEvent).where(
            WebhookEvent.event_id == message_mid,
            WebhookEvent.channel == ChannelType.instagram,
        )
        existing_event = (await db_session.exec(stmt_event)).first()
        if existing_event:
            if existing_event.processed:
                logger.info("[IG WEBHOOK] ⚡ Duplicate skipped | mid=%s | processed=True", message_mid)
                return
            webhook_evt = existing_event
            logger.info("[IG WEBHOOK] Retrying previously uncompleted event | event_db_id=%s | mid=%s", webhook_evt.id, message_mid)
        else:
            webhook_evt = WebhookEvent(
                event_id=message_mid,
                channel=ChannelType.instagram,
                processed=False,
                raw_payload=json.dumps(event),
            )
            db_session.add(webhook_evt)
            await db_session.commit()
            await db_session.refresh(webhook_evt)
            logger.info("[IG WEBHOOK] WebhookEvent claimed | event_db_id=%s | mid=%s", webhook_evt.id, message_mid)

    except IntegrityError:
        await db_session.rollback()
        logger.info("[IG WEBHOOK] ⚡ Race condition — duplicate mid=%s", message_mid)
        return
    except Exception as exc:
        await db_session.rollback()
        logger.error("[IG WEBHOOK] ❌ Idempotency failure | mid=%s | error=%s", message_mid, exc, exc_info=True)
        return

    # ──────────────────────────────────────────────────────────────────────────
    # Step 2: Customer User, Ticket, and Message Resolution
    # ──────────────────────────────────────────────────────────────────────────
    try:
        # Find or Create Customer User (using IGSID)
        synthetic_email = f"instagram_{sender_id[:100]}@supporthub.local"[:255]
        user_stmt = select(User).where(
            (User.channel_customer_id == sender_id) | (User.email == synthetic_email)
        )
        user = (await db_session.exec(user_stmt)).first()

        # Query live Meta Graph API for customer profile (name, username, profile_pic)
        ig_client = MetaInstagramClient()
        profile_data = {}
        try:
            profile_data = await ig_client.get_user_profile(sender_id)
        except Exception as exc:
            logger.warning("[IG WEBHOOK] Could not fetch profile for %s: %s", sender_id, exc)

        actual_name = (
            profile_data.get("name")
            or profile_data.get("username")
            or (user.name if user and not user.name.startswith("Instagram User") else None)
            or f"Instagram User ({sender_id[:8]})"
        )[:100]
        avatar_url = profile_data.get("profile_pic") or (user.avatar_url if user else None)

        if not user:
            logger.info("[IG WEBHOOK] Creating new User for sender=%s (name=%s)", sender_id, actual_name)
            user = User(
                email=synthetic_email,
                name=actual_name,
                password_hash=f"external_instagram_{sender_id}"[:255],
                role=UserRole.customer,
                status=UserStatus.active,
                channel=ChannelType.instagram,
                channel_customer_id=sender_id,
                avatar_url=avatar_url,
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
            logger.info("[IG WEBHOOK] User CREATED | user_id=%s | name=%s", user.id, user.name)
        else:
            logger.info(
                "[IG WEBHOOK] User FOUND | user_id=%s | channel_customer_id=%s",
                user.id,
                user.channel_customer_id,
            )
            user_dirty = False
            if not user.channel_customer_id:
                user.channel_customer_id = sender_id
                user_dirty = True
            if user.channel != ChannelType.instagram:
                user.channel = ChannelType.instagram
                user_dirty = True
            if actual_name and (user.name != actual_name or user.name.startswith("Instagram User")):
                user.name = actual_name
                user_dirty = True
            if avatar_url and user.avatar_url != avatar_url:
                user.avatar_url = avatar_url
                user_dirty = True

            if user_dirty:
                db_session.add(user)
                await db_session.commit()
                await db_session.refresh(user)

        # Enforce strict single-ticket policy per customer on Instagram
        ticket_stmt = (
            select(Ticket)
            .where(
                Ticket.customer_id == user.id,
                Ticket.channel == TicketChannel.instagram,
                Ticket.deleted_at.is_(None),
            )
            .order_by(Ticket.created_at.desc())
        )
        ticket = (await db_session.exec(ticket_stmt)).first()

        if not ticket:
            logger.info("[IG WEBHOOK] No existing ticket found — creating single ticket | user_id=%s", user.id)
            ticket = Ticket(
                ref=generate_ticket_ref(),
                customer_id=user.id,
                subject=f"Instagram DM from {user.name}",
                category="instagram",
                channel=TicketChannel.instagram,
                status=TicketStatus.new,
                priority=TicketPriority.medium,
            )
            db_session.add(ticket)
            await db_session.commit()
            await db_session.refresh(ticket)
            logger.info("[IG WEBHOOK] Ticket CREATED | ticket_id=%s | ref=%s", ticket.id, ticket.ref)
        else:
            logger.info(
                "[IG WEBHOOK] Ticket FOUND (reusing single ticket) | ticket_id=%s | ref=%s | status=%s",
                ticket.id,
                ticket.ref,
                ticket.status.value,
            )
            # If resolved or closed, reopen the ticket for continuous customer thread
            if ticket.status in [TicketStatus.resolved, TicketStatus.closed]:
                ticket.status = TicketStatus.open
            # Update generic subjects if present
            if "Instagram DM from " in ticket.subject and (sender_id[:8] in ticket.subject or "Instagram User" in ticket.subject):
                ticket.subject = f"Instagram DM from {user.name}"
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

        logger.info(
            "[IG REALTIME] message persisted\nticket=%s\nmessage=%s",
            ticket.id,
            cust_msg.id,
        )

        await db_session.commit()
        await db_session.refresh(cust_msg)

        logger.info(
            "[IG REALTIME] DB commit successful\nticket=%s\nmessage=%s",
            ticket.id,
            cust_msg.id,
        )

        # ──────────────────────────────────────────────────────────────────────────
        # Step 3: Real-Time WebSocket Broadcast (ONLY AFTER SUCCESSFUL DB COMMIT)
        # ──────────────────────────────────────────────────────────────────────────
        try:
            from app.ws.manager import manager
            ticket_id_str = str(ticket.id)

            broadcast_payload = {
                "type": "message",
                "id": str(cust_msg.id),
                "ticket_id": ticket_id_str,
                "sender_id": str(user.id),
                "sender_name": user.name or f"Instagram User ({sender_id})",
                "sender_role": "customer",
                "sender_type": "customer",
                "body": text_body,
                "created_at": cust_msg.created_at.isoformat() if cust_msg.created_at else "",
                "external_message_id": message_mid,
            }

            logger.info(
                "[IG REALTIME] broadcasting message\nticket=%s\nmessage=%s",
                ticket_id_str,
                str(cust_msg.id),
            )

            await manager.broadcast(ticket_id_str, broadcast_payload)

            await manager.broadcast_to_agents({
                "type": "inbox_update",
                "ticket_id": ticket_id_str,
                "preview": text_body[:80],
                "sender_name": user.name or f"Instagram User ({sender_id})",
                "subject": ticket.subject,
                "status": ticket.status.value,
            })

            logger.info(
                "[IG REALTIME] broadcast complete\nticket=%s\nmessage=%s",
                ticket_id_str,
                str(cust_msg.id),
            )
        except Exception as ws_err:
            logger.error(
                "[IG REALTIME] broadcast failed\nticket=%s\nerror=%s",
                ticket_id_str,
                ws_err,
                exc_info=True,
            )

        # ──────────────────────────────────────────────────────────────────────────
        # Step 4: AI Auto-Reply Generation with Debounce
        # ──────────────────────────────────────────────────────────────────────────
        from app.services.ai.debouncer import ai_debouncer
        
        async def trigger_ai():
            await _execute_ai_for_instagram(ticket.id, sender_id, ticket_id_str)
            
        ai_debouncer.schedule(ticket_id_str, trigger_ai)

    except Exception as exc:
        await db_session.rollback()
        logger.error("[IG WEBHOOK] ❌ Error processing mid=%s: %s", message_mid, exc, exc_info=True)
        # Update WebhookEvent error if possible
        try:
            async with AsyncSessionLocal() as err_session:
                evt_stmt = select(WebhookEvent).where(
                    WebhookEvent.event_id == message_mid,
                    WebhookEvent.channel == ChannelType.instagram,
                )
                err_evt = (await err_session.exec(evt_stmt)).first()
                if err_evt:
                    err_evt.error = str(exc)[:500]
                    err_session.add(err_evt)
                    await err_session.commit()
        except Exception:
            pass

async def _execute_ai_for_instagram(ticket_id, sender_id: str, ticket_id_str: str):
    """
    Executes the AI orchestration for Instagram after the debounce timer expires.
    This fetches the latest message history so rapid-fire messages are grouped.
    """
    try:
        from app.database import AsyncSessionLocal
        from app.models import Ticket, User, Message, SenderType
        from sqlmodel import select
        from app.services.ai.orchestrator import AIOrchestrator
        from app.services.instagram.client import MetaInstagramClient
        from app.services.ai.knowledge_rag import get_relevant_kb_context
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
                # 4. Deliver response to Meta Instagram Direct API
                ext_msg_id = None
                recipient_igsid = user.channel_customer_id or sender_id
                try:
                    ig_client = MetaInstagramClient()
                    if ig_client.access_token:
                        delivery_res = await ig_client.send_text_message(
                            recipient_igsid=recipient_igsid,
                            text=ai_text,
                        )
                        if delivery_res and delivery_res.success:
                            ext_msg_id = delivery_res.provider_message_id
                            logger.info("[IG AUTO-AI] Sent AI reply to Instagram Direct | recip=%s | mid=%s", recipient_igsid, ext_msg_id)
                        else:
                            logger.warning("[IG AUTO-AI] IG Delivery returned unsuccessful: %s", delivery_res)
                    else:
                        logger.info("[IG AUTO-AI] INSTAGRAM_ACCESS_TOKEN not configured; skipping live Meta HTTP call.")
                except Exception as send_err:
                    logger.warning("[IG AUTO-AI] Outbound IG API call failed (saved locally): %s", send_err)

                # 5. Store AI message in database
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
                })

                logger.info("[IG AUTO-AI] AI response generated and broadcast for ticket=%s", ticket_id_str)

    except Exception as ai_err:
        logger.error("[IG AUTO-AI] Failed to process auto-AI reply for ticket %s: %s", ticket_id, ai_err, exc_info=True)

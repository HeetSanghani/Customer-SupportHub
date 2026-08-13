"""
app/services/whatsapp/webhook.py

WhatsApp Webhook Orchestration Service.

Full pipeline (Steps 1–3B wired):
  1. Parse raw Meta payload → list[IncomingMessage]         (parser.py)
  2. Process through ConversationService → ConversationContext  (Step 3A)
  3. Generate AI response → AIResponse                      (Step 3B)
  4. [Step 3C] Send WhatsApp reply — coming next
"""

from __future__ import annotations

import logging

from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.ai.orchestrator import AIOrchestrator
from app.services.channels.models import IncomingMessage
from app.services.conversations.exceptions import DuplicateMessageError
from app.services.conversations.service import ConversationService
from app.services.whatsapp.parser import parse_whatsapp_payload
from app.services.whatsapp.sender import WhatsAppSender

from app.database import AsyncSessionLocal
from app.ws.manager import manager
from sqlmodel import select
from app.models import Message

logger = logging.getLogger(__name__)


async def process_whatsapp_payload(
    payload: dict,
    session: AsyncSession = None,
) -> None:
    """
    Entry point for background processing of a Meta WhatsApp webhook payload.
    Uses an independent database session to prevent closed-session errors.
    """
    parse_result = parse_whatsapp_payload(payload)

    if parse_result.errors:
        logger.warning("WhatsApp parsing errors: %s", parse_result.errors)

    if not parse_result.messages:
        logger.debug("No actionable messages in payload.")
        return

    logger.info("Processing %d WhatsApp message(s).", len(parse_result.messages))

    async with AsyncSessionLocal() as db_session:
        conv_service = ConversationService(db_session)
        ai_orchestrator = AIOrchestrator(session=db_session)
        whatsapp_sender = WhatsAppSender(session=db_session)

        # Download media attachments before processing
        from app.services.whatsapp.client import MetaWhatsAppClient
        whatsapp_client = MetaWhatsAppClient()

        from dataclasses import replace

        for incoming in parse_result.messages:
            if incoming.attachments:
                new_attachments = []
                new_text = incoming.text or ""
                
                for attachment in incoming.attachments:
                    if attachment.media_id:
                        local_url, filename = await whatsapp_client.download_media(attachment.media_id, attachment.mime_type)
                        if local_url and filename:
                            new_attachment = replace(
                                attachment,
                                url=local_url,
                                filename=attachment.filename or filename
                            )
                            markdown = f" 📎 [Attachment: {filename}]({local_url})"
                            new_text += markdown
                            new_attachments.append(new_attachment)
                        else:
                            new_attachments.append(attachment)
                    else:
                        new_attachments.append(attachment)
                        
                incoming = replace(incoming, text=new_text, attachments=new_attachments)

            await _process_single_message(db_session, conv_service, ai_orchestrator, whatsapp_sender, incoming)


async def _process_single_message(
    db_session: AsyncSession,
    conv_service: ConversationService,
    ai_orchestrator: AIOrchestrator,
    whatsapp_sender: WhatsAppSender,
    incoming: IncomingMessage,
) -> None:
    """Process one IncomingMessage through conversation + AI + delivery pipeline."""
    try:
        # ── Step 3A: Conversation Management ──────────────────────────────
        context = await conv_service.process_incoming(incoming)

        logger.info(
            "✅ Conversation | ref=%s | customer=%s | new=%s",
            context.conversation_ref,
            context.customer_display_name,
            context.is_new_conversation,
        )

        ticket_id_str = str(context.ticket.id)

        # Broadcast incoming customer message over WebSocket to dashboard UI
        await manager.broadcast(ticket_id_str, {
            "type": "message",
            "id": incoming.channel_message_id,
            "ticket_id": ticket_id_str,
            "sender_id": str(context.customer.id),
            "sender_name": context.customer.name,
            "sender_role": "customer",
            "body": incoming.text or "",
            "created_at": incoming.timestamp.isoformat() if incoming.timestamp else "",
        })

        await manager.broadcast_to_agents({
            "type": "inbox_update",
            "ticket_id": ticket_id_str,
            "preview": (incoming.text or "")[:80],
            "sender_name": context.customer.name,
        })

        # Auto-update ticket subject if currently set to a generic greeting or placeholder
        import re
        curr_subj = (context.ticket.subject or "").lower().strip()
        generic_subjects = ["hello", "hi", "hey", "help", "whatsapp support inquiry", "whatsapp message", "general customer inquiry", "new support query"]
        if curr_subj in generic_subjects or len(curr_subj) < 8:
            user_text = incoming.text or ""
            cleaned = re.sub(r"^(hello|hi|hey|good morning|good afternoon|dear support)[\s,!.]*", "", user_text, flags=re.IGNORECASE).strip()
            if cleaned and len(cleaned) >= 5:
                new_subj = cleaned.split(".")[0].split("\n")[0].strip()
                if len(new_subj) > 60:
                    new_subj = new_subj[:60].rsplit(" ", 1)[0]
                context.ticket.subject = new_subj.capitalize()
                db_session.add(context.ticket)
                await db_session.commit()
                await db_session.refresh(context.ticket)

        # ── Step 3B: AI Orchestration ──────────────────────────────────────
        ai_response = await ai_orchestrator.generate(context)

        logger.info(
            "🤖 AI Response | ref=%s | provider=%s | tokens=%d | ms=%d | fallback=%s | "
            "preview=%r",
            context.conversation_ref,
            ai_response.model.provider,
            ai_response.usage.total_tokens,
            ai_response.latency_ms,
            ai_response.is_fallback,
            ai_response.response_text[:80],
        )

        # ── Step 3C: Outbound WhatsApp Delivery via Meta Cloud API ───────────
        delivery_result = await whatsapp_sender.send_ai_reply(context, ai_response)

        logger.info(
            "🚀 Reply Delivered | ref=%s | status=%s | wamid=%s | latency=%dms",
            context.conversation_ref,
            delivery_result.status.value,
            delivery_result.provider_message_id,
            delivery_result.latency_ms,
        )

        # Check if customer message or AI response requests to resolve/close the chat
        user_msg = (incoming.text or "").lower().strip()
        ai_msg = (ai_response.response_text or "").lower().strip()

        resolution_phrases = [
            "close this chat", "close chat", "end this chat", "end chat",
            "close ticket", "end ticket", "resolve ticket", "mark as resolved",
            "you can close", "you can end", "thanks, that fixed it", "thanks that fixed it",
            "that fixed it", "problem solved", "issue is resolved", "issue resolved"
        ]

        is_resolved_intent = (
            any(phrase in user_msg for phrase in resolution_phrases)
            or (("close" in user_msg or "end" in user_msg) and ("chat" in user_msg or "ticket" in user_msg))
            or ("pleasure assisting" in ai_msg and "have a great day" in ai_msg)
        )

        if is_resolved_intent:
            from app.models import TicketStatus
            context.ticket.status = TicketStatus.resolved
            context.ticket.ai_resolved = True
            db_session.add(context.ticket)
            await db_session.commit()
            await db_session.refresh(context.ticket)
            logger.info("✅ Ticket %s automatically RESOLVED via resolution intent.", context.ticket.ref)

        # Broadcast AI response over WebSocket to dashboard UI
        await manager.broadcast(ticket_id_str, {
            "type": "message",
            "id": delivery_result.outbound_message_id,
            "ticket_id": ticket_id_str,
            "sender_id": "AI",
            "sender_name": "Support AI",
            "sender_role": "ai",
            "body": ai_response.response_text,
            "created_at": delivery_result.sent_at.isoformat() if delivery_result.sent_at else "",
            "external_message_id": delivery_result.provider_message_id,
        })

        # Dynamically generate AI subject line based on full conversation topic
        from app.ai import generate_ai_ticket_subject
        ai_subj = await generate_ai_ticket_subject(db_session, context.ticket.id)
        if ai_subj:
            context.ticket.subject = ai_subj

        # Broadcast ticket update event so UI updates status & subject immediately
        await manager.broadcast(ticket_id_str, {
            "type": "ticket_update",
            "status": context.ticket.status.value,
            "subject": context.ticket.subject,
            "ai_resolved": context.ticket.ai_resolved,
        })

        await manager.broadcast_to_agents({
            "type": "inbox_update",
            "ticket_id": ticket_id_str,
            "preview": ai_response.response_text[:80],
            "sender_name": "Support AI",
            "subject": context.ticket.subject,
            "status": context.ticket.status.value,
        })

    except DuplicateMessageError as exc:
        logger.info("⚡ Duplicate skipped | id=%s", exc.channel_message_id)

    except Exception as exc:
        logger.error(
            "❌ Pipeline error | id=%s | error=%s",
            incoming.channel_message_id,
            exc,
            exc_info=True,
        )

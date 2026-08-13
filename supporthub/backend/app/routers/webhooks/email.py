import email.utils
import hashlib
import logging
import random
import re
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session, AsyncSessionLocal
from app.models import Ticket, User, Message, TicketChannel, TicketStatus, TicketPriority, SenderType, UserRole, UserStatus
from app.services.ai_reply import generate_ai_reply
from app.services.senders import send_email_reply

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/email", tags=["webhooks-email"])


def generate_ticket_ref() -> str:
    return f"TCK-{random.randint(10000, 99999)}"


def clean_email_body(body_text: str) -> str:
    """
    Strips email client signatures, Mailtrack notices, and quoted reply headers
    using regex heuristics.
    """
    if not body_text:
        return ""
    
    # Common markers indicating reply history or email footers
    reply_patterns = [
        r"(?im)^On\s+.*?\s+wrote:\s*$",
        r"(?im)^-+\s*Original Message\s*-+",
        r"(?im)^From:\s+.*$",
        r"(?im)^Sent:\s+.*$",
        r"(?im)^Sender notified with Mailtrack.*$",
        r"(?im)^--\s*$",
        r"(?im)^________________________________\s*$",
    ]

    cleaned = body_text
    for pattern in reply_patterns:
        match = re.search(pattern, cleaned)
        if match:
            cleaned = cleaned[:match.start()]

    return cleaned.strip()


async def process_ai_email_reply(ticket_id: uuid.UUID, email_address: str, email_subject: str, ticket_ref: str):
    """
    Background task to generate AI reply and dispatch outbound email via Mailgun.
    Executes asynchronously in background to ensure webhook HTTP response returns in <200ms.
    """
    try:
        async with AsyncSessionLocal() as session:
            # 1. Fetch ticket, user, and conversation history
            ticket = await session.get(Ticket, ticket_id)
            if not ticket:
                return
            user = await session.get(User, ticket.customer_id)
            
            history_stmt = select(Message).where(Message.ticket_id == ticket_id).order_by(Message.created_at.asc())
            history_msgs = (await session.exec(history_stmt)).all()

            # 2. Generate AI reply using unified orchestrator
            from app.services.ai.orchestrator import AIOrchestrator
            from app.services.ai.knowledge_rag import get_relevant_kb_context

            latest_customer_msg = next((m for m in reversed(history_msgs) if m.sender_type == SenderType.customer), None)
            search_query = latest_customer_msg.body if latest_customer_msg else email_subject
            kb_context = await get_relevant_kb_context(session, search_query)

            orchestrator = AIOrchestrator(session=session)
            ai_out = await orchestrator.generate_for_ticket(
                ticket=ticket,
                messages=history_msgs,
                customer=user,
                kb_context=kb_context,
                tone="professional",
            )
            
            if isinstance(ai_out, dict):
                ai_reply_text = ai_out.get("suggested_reply") or ai_out.get("response_text") or ""
            else:
                ai_reply_text = getattr(ai_out, "suggested_reply", None) or getattr(ai_out, "response_text", "")

            if ai_reply_text:
                # 3. Save AI reply Message record to database
                ai_msg = Message(
                    ticket_id=ticket_id,
                    sender_id=None,
                    sender_type=SenderType.ai,
                    body=ai_reply_text,
                )
                session.add(ai_msg)
                await session.commit()


            # 4. Deliver reply back to original sender via Mailgun API
            try:
                subject_header = email_subject if email_subject.lower().startswith("re:") else f"Re: {email_subject}"
                await send_email_reply(
                    to_email=email_address,
                    subject=subject_header,
                    body=ai_reply_text,
                    ticket_ref=ticket_ref,
                )
            except Exception as send_err:
                logger.error(f"[{ticket_ref}] Failed to dispatch outbound Mailgun email to {email_address}: {send_err}")

    except Exception as exc:
        logger.error(f"[{ticket_ref}] Error in background AI email processing for ticket {ticket_id}: {exc}", exc_info=True)


@router.post("")
async def receive_mailgun_email(
    request: Request,
    background_tasks: BackgroundTasks,
    sender: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    body_plain: Optional[str] = Form(None, alias="body-plain"),
    stripped_text: Optional[str] = Form(None, alias="stripped-text"),
    message_id: Optional[str] = Form(None, alias="Message-Id"),
    attachment_count: Optional[int] = Form(None, alias="attachment-count"),
    session: AsyncSession = Depends(get_session),
):
    """
    Inbound Mailgun webhook endpoint parsing multipart/form-data.
    Includes idempotency checks, signature stripping, ticket state updates, and
    fast response via BackgroundTasks.
    """
    try:
        # Fallback to request.form() if fields not bound by FastAPI Form dependency
        form_data = await request.form()
        sender_raw = sender or form_data.get("sender") or form_data.get("from") or ""
        subject_raw = subject or form_data.get("subject") or ""
        body_plain_raw = body_plain or form_data.get("body-plain") or ""
        stripped_text_raw = stripped_text or form_data.get("stripped-text") or ""
        msg_id_raw = message_id or form_data.get("Message-Id") or form_data.get("message-id") or ""
        att_count = attachment_count or form_data.get("attachment-count") or 0

        if not sender_raw:
            logger.warning("Mailgun webhook received without 'sender' field.")
            return {"status": "ok", "message": "Missing sender field"}

        # 1. Parse sender display name & email address
        parsed_name, parsed_email = email.utils.parseaddr(sender_raw)
        email_address = (parsed_email or sender_raw).strip().lower()
        display_name = parsed_name.strip() if parsed_name else email_address.split("@")[0].replace(".", " ").title()

        # 2. Extract body text & HTML
        body_html_raw = form_data.get("body-html") or form_data.get("stripped-html") or None
        raw_body = (stripped_text_raw or body_plain_raw).strip()
        cleaned_body = clean_email_body(raw_body)

        # 2.5 Extract attachments from form_data
        import os
        from starlette.datastructures import UploadFile
        
        upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads"))
        os.makedirs(upload_dir, exist_ok=True)
        
        for key, value in form_data.multi_items():
            if isinstance(value, UploadFile):
                try:
                    content = await value.read()
                    if content:
                        ext = os.path.splitext(value.filename)[1] if value.filename else ""
                        file_uuid = uuid.uuid4().hex
                        filename = f"{file_uuid}{ext}"
                        file_path = os.path.join(upload_dir, filename)
                        with open(file_path, "wb") as f:
                            f.write(content)
                        local_url = f"http://localhost:8001/static/uploads/{filename}"
                        display_name = value.filename or filename
                        markdown = f" 📎 [Attachment: {display_name}]({local_url})"
                        cleaned_body = (cleaned_body + markdown).strip()
                except Exception as e:
                    logger.error(f"Failed to save email attachment: {e}")

        if not cleaned_body and not body_html_raw:
            logger.warning(f"Mailgun webhook from {email_address} contained empty body.")
            return {"status": "ok", "message": "Empty body"}

        # Log attachment notices if present
        try:
            att_num = int(att_count)
            if att_num > 0:
                logger.info(f"Mailgun email from {email_address} included {att_num} attachment(s).")
        except ValueError:
            pass

        # 3. Idempotency Check via external_message_id
        ext_msg_id = msg_id_raw.strip("<> ").strip()
        if not ext_msg_id:
            # Fallback hash if Message-Id header is missing
            hash_input = f"{email_address}:{subject_raw}:{raw_body}"
            ext_msg_id = f"hash-{hashlib.sha256(hash_input.encode()).hexdigest()[:32]}"

        existing_msg_stmt = select(Message).where(Message.external_message_id == ext_msg_id)
        existing_msg = (await session.exec(existing_msg_stmt)).first()
        if existing_msg:
            logger.info(f"Duplicate Mailgun webhook delivery detected (external_message_id={ext_msg_id}). Skipping reprocessing.")
            return {"status": "ok", "message": "duplicate_skipped"}

        # 4. Find or Create User
        user_stmt = select(User).where(User.email == email_address)
        user = (await session.exec(user_stmt)).first()

        if not user:
            user = User(
                email=email_address,
                name=display_name,
                password_hash="external_mailgun_user",
                role=UserRole.customer,
                status=UserStatus.active,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        # 5. Email Threading Check (Subject regex e.g. TCK-10234 or In-Reply-To)
        email_subject = subject_raw.strip() or "Email Inquiry"
        ticket = None
        
        # Check for ticket reference pattern TCK-XXXXX in subject
        tck_match = re.search(r"TCK-\d{5}", email_subject, re.IGNORECASE)
        if tck_match:
            matched_ref = tck_match.group(0).upper()
            ref_stmt = select(Ticket).where(Ticket.ref == matched_ref)
            ticket = (await session.exec(ref_stmt)).first()

        # Fallback to customer's open ticket if no ref in subject
        if not ticket:
            ticket_stmt = select(Ticket).where(
                Ticket.customer_id == user.id,
                Ticket.channel == TicketChannel.email,
                Ticket.status.in_([TicketStatus.new, TicketStatus.open, TicketStatus.waiting])
            )
            ticket = (await session.exec(ticket_stmt)).first()

        if not ticket:
            ticket = Ticket(
                ref=generate_ticket_ref(),
                customer_id=user.id,
                subject=email_subject,
                category="email",
                channel=TicketChannel.email,
                status=TicketStatus.new,
                priority=TicketPriority.medium,
            )
            session.add(ticket)
            await session.commit()
            await session.refresh(ticket)
        else:
            # Reopening / updating existing open ticket
            ticket.updated_at = datetime.now()
            if ticket.ai_resolved or ticket.status in (TicketStatus.resolved, TicketStatus.closed):
                ticket.ai_resolved = False
                ticket.status = TicketStatus.open
            session.add(ticket)
            await session.commit()
            await session.refresh(ticket)

        # 6. Save incoming customer Message record (including body_html)
        cust_msg = Message(
            ticket_id=ticket.id,
            sender_id=user.id,
            sender_type=SenderType.customer,
            body=cleaned_body or "HTML Content Email",
            body_html=body_html_raw,
            external_message_id=ext_msg_id,
        )
        session.add(cust_msg)
        await session.commit()

        # 7. Schedule background task for AI reply & outbound send
        background_tasks.add_task(
            process_ai_email_reply,
            ticket_id=ticket.id,
            email_address=email_address,
            email_subject=email_subject,
            ticket_ref=ticket.ref,
        )

        # 8. Return HTTP 200 immediately to Mailgun
        return {"status": "ok", "ticket_ref": ticket.ref}

    except Exception as exc:
        logger.error(f"Error handling Mailgun email webhook: {exc}", exc_info=True)
        return {"status": "ok", "error": str(exc)}

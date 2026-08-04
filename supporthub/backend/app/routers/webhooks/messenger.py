import logging
import random
from fastapi import APIRouter, Depends, Query, Request, Response
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.models import Ticket, User, Message, TicketChannel, TicketStatus, TicketPriority, SenderType, UserRole, UserStatus
from app.services.ai_reply import generate_ai_reply
from app.services.senders import send_messenger_reply

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter(prefix="/messenger", tags=["webhooks-messenger"])


def generate_ticket_ref() -> str:
    return f"TCK-{random.randint(10000, 99999)}"


@router.get("")
async def verify_messenger_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    """Handshake verification endpoint for Meta Messenger & Instagram Direct webhooks."""
    expected_token = settings.meta_verify_token or "supporthub_verify"
    if hub_mode == "subscribe" and hub_verify_token == expected_token:
        logger.info("Messenger/Instagram webhook verified successfully.")
        return Response(content=str(hub_challenge or ""), media_type="text/plain")
    logger.warning("Messenger/Instagram webhook verification failed.")
    return Response(content="Forbidden", status_code=403)


@router.post("")
async def receive_messenger_webhook(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Receives inbound messages from Meta Messenger & Instagram Direct webhooks."""
    try:
        payload = await request.json()
        entries = payload.get("entry", [])
        if not entries:
            return {"status": "ok"}

        for entry in entries:
            page_id = str(entry.get("id", ""))
            messaging_events = entry.get("messaging", [])

            # Distinguish Instagram vs Facebook Messenger using entry.id vs settings.ig_page_id / settings.fb_page_id
            is_instagram = (
                (settings.ig_page_id and page_id == str(settings.ig_page_id))
                or entry.get("object") == "instagram"
            )
            channel_enum = TicketChannel.instagram if is_instagram else TicketChannel.facebook

            for event in messaging_events:
                sender_info = event.get("sender", {})
                sender_id = sender_info.get("id")
                message_info = event.get("message", {})
                text_body = message_info.get("text", "").strip()

                # Ignore echo/delivery notifications or empty messages
                if not sender_id or not text_body or message_info.get("is_echo"):
                    continue

                prefix_str = "instagram" if is_instagram else "messenger"
                synthetic_email = f"{prefix_str}_{sender_id}@supporthub.local"
                display_name = f"{prefix_str.title()} User ({sender_id[:8]})"

                # 1. Find or Create User
                user_stmt = select(User).where(User.email == synthetic_email)
                user = (await session.exec(user_stmt)).first()

                if not user:
                    user = User(
                        email=synthetic_email,
                        name=display_name,
                        password_hash=f"external_{prefix_str}_user",
                        role=UserRole.customer,
                        status=UserStatus.active,
                    )
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)

                # 2. Find or Create Ticket
                ticket_stmt = select(Ticket).where(
                    Ticket.customer_id == user.id,
                    Ticket.channel == channel_enum,
                    Ticket.status.in_([TicketStatus.new, TicketStatus.open, TicketStatus.waiting])
                )
                ticket = (await session.exec(ticket_stmt)).first()

                if not ticket:
                    ticket = Ticket(
                        ref=generate_ticket_ref(),
                        customer_id=user.id,
                        subject=f"{prefix_str.title()} Message from {sender_id[:8]}",
                        category=prefix_str,
                        channel=channel_enum,
                        status=TicketStatus.new,
                        priority=TicketPriority.medium,
                    )
                    session.add(ticket)
                    await session.commit()
                    await session.refresh(ticket)

                # 3. Save incoming customer Message
                cust_msg = Message(
                    ticket_id=ticket.id,
                    sender_id=user.id,
                    sender_type=SenderType.customer,
                    body=text_body,
                )
                session.add(cust_msg)
                await session.commit()

                # 4. Fetch history & generate AI reply
                history_stmt = select(Message).where(Message.ticket_id == ticket.id).order_by(Message.created_at.asc())
                history_msgs = (await session.exec(history_stmt)).all()
                conversation_history = [
                    {
                        "role": "user" if m.sender_type == SenderType.customer else "assistant",
                        "content": m.body
                    }
                    for m in history_msgs
                ]

                ai_reply_text = await generate_ai_reply(conversation_history)

                # 5. Outbound Messenger/Instagram Send
                await send_messenger_reply(recipient_id=sender_id, text=ai_reply_text)

                # 6. Save AI reply Message
                ai_msg = Message(
                    ticket_id=ticket.id,
                    sender_id=None,
                    sender_type=SenderType.ai,
                    body=ai_reply_text,
                )
                session.add(ai_msg)
                await session.commit()

        return {"status": "ok"}

    except Exception as exc:
        logger.error(f"Error handling Messenger/Instagram webhook: {exc}", exc_info=True)
        return {"status": "ok", "error": str(exc)}

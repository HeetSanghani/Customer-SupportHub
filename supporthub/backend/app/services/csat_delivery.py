"""CSAT Delivery Service for explicitly pushing survey messages when tickets are resolved."""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Ticket, User, Message, SenderType, TicketChannel
from app.services.whatsapp.client import MetaWhatsAppClient
from app.services.instagram.client import MetaInstagramClient
from app.services.senders import send_email_reply
from app.ws.manager import manager

logger = logging.getLogger(__name__)

async def deliver_csat_survey(session: AsyncSession, ticket: Ticket, customer: User) -> Optional[Message]:
    """Generate and deliver a CSAT survey message to the appropriate channel."""
    
    frontend_url = "http://localhost:8001" # Or from settings
    
    # Text fallback for social channels
    text_prompt = (
        f"Your ticket [{ticket.ref}] has been resolved.\n\n"
        f"How would you rate your support experience today?\n"
        f"Please click the link below to submit your rating (1-5):\n"
        f"{frontend_url}/api/v1/tickets/{ticket.id}/rate-email?rating=5\n"
        f"We appreciate your feedback!"
    )
    
    html_prompt = f"""
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>
            <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [{ticket.ref}]</strong>
        </div>
        <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your inquiry <strong>"{ticket.subject}"</strong> has been resolved. How would you rate your support experience today?</p>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <a href="{frontend_url}/api/v1/tickets/{ticket.id}/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>
            <a href="{frontend_url}/api/v1/tickets/{ticket.id}/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>
            <a href="{frontend_url}/api/v1/tickets/{ticket.id}/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>
            <a href="{frontend_url}/api/v1/tickets/{ticket.id}/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>
        </div>
        <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this thread to automatically reopen your ticket.</p>
    </div>
    """

    msg = Message(
        ticket_id=ticket.id,
        sender_id=None,
        sender_type=SenderType.ai,
        body=text_prompt,
        body_html=html_prompt if ticket.channel == TicketChannel.email else None
    )
    session.add(msg)
    await session.commit()
    await session.refresh(msg)
    
    # Broadcast to websocket room
    await manager.broadcast(str(ticket.id), {
        "type": "message",
        "id": str(msg.id),
        "ticket_id": str(ticket.id),
        "sender_id": "System",
        "sender_name": "SupportHub",
        "sender_role": "system",
        "body": text_prompt,
        "body_html": msg.body_html,
        "created_at": msg.created_at.isoformat(),
    })

    # Dispatch to appropriate channel
    if ticket.channel == TicketChannel.email:
        if customer and customer.email:
            asyncio.create_task(send_email_reply(
                to_email=customer.email,
                subject=ticket.subject,
                body=html_prompt,
                ticket_ref=ticket.ref
            ))
            
    elif ticket.channel == TicketChannel.whatsapp:
        if customer and (customer.phone or customer.channel_customer_id):
            asyncio.create_task(_send_whatsapp_csat(ticket, customer, msg))
            
    elif ticket.channel == TicketChannel.instagram:
        if customer and customer.channel_customer_id:
            asyncio.create_task(_send_instagram_csat(ticket, customer, msg))

    return msg

async def _send_whatsapp_csat(ticket: Ticket, customer: User, msg: Message):
    from app.database import AsyncSessionLocal
    from app.services.whatsapp.formatter import WhatsAppPayloadFormatter
    
    phone = customer.phone or customer.channel_customer_id
    clean_phone = WhatsAppPayloadFormatter.normalize_phone(phone)
    client = MetaWhatsAppClient()
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": clean_phone,
        "type": "text",
        "text": {"body": msg.body}
    }
    
    try:
        res = await client.send_payload(payload)
        async with AsyncSessionLocal() as session:
            db_msg = await session.get(Message, msg.id)
            if db_msg:
                db_msg.attachments = json.dumps({"status": "delivered", "provider_message_id": res.provider_message_id})
                db_msg.external_message_id = res.provider_message_id
                session.add(db_msg)
                await session.commit()
    except Exception as exc:
        logger.error(f"Failed to send CSAT via WhatsApp for ticket {ticket.ref}: {exc}")
        async with AsyncSessionLocal() as session:
            db_msg = await session.get(Message, msg.id)
            if db_msg:
                db_msg.attachments = json.dumps({"status": "failed", "error_message": str(exc)})
                session.add(db_msg)
                await session.commit()

async def _send_instagram_csat(ticket: Ticket, customer: User, msg: Message):
    from app.database import AsyncSessionLocal
    client = MetaInstagramClient()
    try:
        res = await client.send_text_message(recipient_igsid=customer.channel_customer_id, text=msg.body)
        async with AsyncSessionLocal() as session:
            db_msg = await session.get(Message, msg.id)
            if db_msg:
                db_msg.attachments = json.dumps({"status": "delivered", "provider_message_id": res.provider_message_id})
                db_msg.external_message_id = res.provider_message_id
                session.add(db_msg)
                await session.commit()
    except Exception as exc:
        logger.error(f"Failed to send CSAT via Instagram for ticket {ticket.ref}: {exc}")
        async with AsyncSessionLocal() as session:
            db_msg = await session.get(Message, msg.id)
            if db_msg:
                db_msg.attachments = json.dumps({"status": "failed", "error_message": str(exc)})
                session.add(db_msg)
                await session.commit()

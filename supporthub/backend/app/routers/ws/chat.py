"""WebSocket chat endpoint — real-time messages per ticket room."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.dependencies import get_ws_user
from app.models import Message, SenderType, Ticket
from app.ws.manager import manager

logger = logging.getLogger(__name__)
router = APIRouter(tags=["websocket"])


async def _send_whatsapp_outbound(ticket_id_str: str, msg_id_str: str, body_text: str):
    import json
    from uuid import UUID
    from app.database import AsyncSessionLocal
    from app.models import Ticket, User, Message, TicketChannel
    from app.services.whatsapp.client import MetaWhatsAppClient
    from app.services.whatsapp.formatter import WhatsAppPayloadFormatter

    async with AsyncSessionLocal() as session:
        t = await session.get(Ticket, UUID(ticket_id_str))
        if not t or t.channel != TicketChannel.whatsapp:
            return

        u = await session.get(User, t.customer_id)
        if not u:
            return

        phone = u.phone or u.channel_customer_id
        if not phone:
            return

        clean_phone = WhatsAppPayloadFormatter.normalize_phone(phone)
        client = MetaWhatsAppClient()
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_phone,
            "type": "text",
            "text": {"body": body_text}
        }

        msg = await session.get(Message, UUID(msg_id_str))
        try:
            res = await client.send_payload(payload)
            print(f"✅ OUTBOUND WHATSAPP SUCCESS for ticket {ticket_id_str} | WAMID: {res.provider_message_id}")
            if msg:
                msg.attachments = json.dumps({"status": "delivered", "provider_message_id": res.provider_message_id})
                msg.external_message_id = res.provider_message_id
                session.add(msg)
                await session.commit()
                # Broadcast updated status to WS subscribers
                await manager.broadcast(ticket_id_str, {
                    "type": "message_status",
                    "id": msg_id_str,
                    "status": "delivered"
                })
        except Exception as exc:
            err_msg = str(exc)
            print(f"❌ OUTBOUND WHATSAPP ERROR for ticket {ticket_id_str}: {err_msg}")
            if msg:
                msg.attachments = json.dumps({"status": "failed", "error_message": err_msg})
                session.add(msg)
                await session.commit()
                # Broadcast updated failed status to WS subscribers
                await manager.broadcast(ticket_id_str, {
                    "type": "message_status",
                    "id": msg_id_str,
                    "status": "failed",
                    "error": err_msg
                })


async def _send_instagram_outbound(ticket_id_str: str, msg_id_str: str, body_text: str):
    import json
    from uuid import UUID
    from app.database import AsyncSessionLocal
    from app.models import Ticket, User, Message, TicketChannel
    from app.services.instagram.client import MetaInstagramClient

    async with AsyncSessionLocal() as session:
        t = await session.get(Ticket, UUID(ticket_id_str))
        if not t or t.channel != TicketChannel.instagram:
            return

        u = await session.get(User, t.customer_id)
        if not u:
            return

        recipient_igsid = u.channel_customer_id
        if not recipient_igsid:
            return

        client = MetaInstagramClient()
        msg = await session.get(Message, UUID(msg_id_str))
        try:
            res = await client.send_text_message(recipient_igsid=recipient_igsid, text=body_text)
            print(f"✅ OUTBOUND INSTAGRAM SUCCESS for ticket {ticket_id_str} | MSG ID: {res.provider_message_id}")
            if msg:
                msg.attachments = json.dumps({"status": "delivered", "provider_message_id": res.provider_message_id})
                msg.external_message_id = res.provider_message_id
                session.add(msg)
                await session.commit()
                # Broadcast updated status to WS subscribers
                await manager.broadcast(ticket_id_str, {
                    "type": "message_status",
                    "id": msg_id_str,
                    "status": "delivered"
                })
        except Exception as exc:
            err_msg = str(exc)
            print(f"❌ OUTBOUND INSTAGRAM ERROR for ticket {ticket_id_str}: {err_msg}")
            if msg:
                msg.attachments = json.dumps({"status": "failed", "error_message": err_msg})
                session.add(msg)
                await session.commit()
                # Broadcast updated failed status to WS subscribers
                await manager.broadcast(ticket_id_str, {
                    "type": "message_status",
                    "id": msg_id_str,
                    "status": "failed",
                    "error": err_msg
                })


@router.websocket("/ws/chat/{ticket_id}")
async def websocket_chat(
    ticket_id: str,
    websocket: WebSocket,
    session: AsyncSession = Depends(get_session),
):
    # 1. Accept WebSocket exactly once
    await websocket.accept()

    # 2. Authenticate user via ?token= query parameter
    user = await get_ws_user(websocket, session)
    if not user:
        logger.warning("[WS SERVER] Authentication failed for ticket=%s", ticket_id)
        return

    # 3. Validate ticket UUID format and verify ticket exists
    try:
        ticket_uuid = UUID(ticket_id)
    except (ValueError, TypeError):
        logger.warning("[WS SERVER] Invalid ticket UUID format: %s", ticket_id)
        await websocket.close(code=4004)
        return

    ticket = await session.get(Ticket, ticket_uuid)
    if not ticket:
        logger.warning("[WS SERVER] Ticket not found ticket=%s", ticket_id)
        await websocket.close(code=4004)
        return

    # 3.5. Enforce ticket room ownership (Anti-IDOR) for customer role
    if user.role.value == "customer":
        if ticket.customer_id and ticket.customer_id != user.id:
            logger.warning(
                "[WS SERVER] Anti-IDOR guard triggered: customer user %s (%s) attempted to access unowned ticket %s",
                user.name,
                user.id,
                ticket_id,
            )
            await websocket.close(code=4003)
            return

    # 4. Register connected WebSocket with ConnectionManager
    connected = False
    try:
        await manager.connect(ticket_id, websocket)
        connected = True
        logger.info("[WS SERVER] Connection accepted | ticket=%s | user=%s (%s)", ticket_id, user.name, user.id)

        # Announce presence
        await manager.broadcast(ticket_id, {
            "type": "presence",
            "user_id": str(user.id),
            "name": user.name,
            "role": user.role.value,
            "joined_at": datetime.now(timezone.utc).isoformat(),
        })

        while True:
            data = await websocket.receive_json()
            if data.get("type") == "message":
                body = data.get("body", "").strip()
                if not body:
                    continue

                # Persist message and update ticket activity timestamp
                ticket.updated_at = datetime.now()
                session.add(ticket)
                msg = Message(
                    ticket_id=ticket_uuid,
                    sender_id=user.id,
                    sender_type=SenderType(user.role.value)
                        if user.role.value in ("customer", "agent")
                        else SenderType.agent,
                    body=body,
                )
                session.add(msg)
                await session.commit()
                await session.refresh(msg)

                # If ticket is WhatsApp and message is from agent, trigger Meta Cloud API send
                if ticket.channel.value == "whatsapp" and user.role.value != "customer":
                    import asyncio
                    asyncio.create_task(_send_whatsapp_outbound(ticket_id, str(msg.id), body))

                # If ticket is Instagram and message is from agent, trigger Meta Instagram Graph API send
                if ticket.channel.value == "instagram" and user.role.value != "customer":
                    import asyncio
                    asyncio.create_task(_send_instagram_outbound(ticket_id, str(msg.id), body))

                # Broadcast to room
                await manager.broadcast(ticket_id, {
                    "type": "message",
                    "id": str(msg.id),
                    "ticket_id": ticket_id,
                    "sender_id": str(user.id),
                    "sender_name": user.name,
                    "sender_role": user.role.value,
                    "sender_type": msg.sender_type.value,
                    "body": body,
                    "created_at": msg.created_at.isoformat(),
                })

                # Also push to agent inbox
                await manager.broadcast_to_agents({
                    "type": "inbox_update",
                    "ticket_id": ticket_id,
                    "preview": body[:80],
                    "sender_name": user.name,
                })

                # Phase 11: SupportHub AI Architecture Live Chat Integration
                if user.role.value == "customer":
                    try:
                        from app.ai.subject import generate_ai_ticket_subject
                        ai_subj = await generate_ai_ticket_subject(session, ticket.id)
                        if ai_subj and ticket.subject != ai_subj:
                            ticket.subject = ai_subj
                            session.add(ticket)
                            await session.commit()
                            await session.refresh(ticket)
                            await manager.broadcast(ticket_id, {
                                "type": "ticket_update",
                                "status": ticket.status.value if hasattr(ticket.status, "value") else str(ticket.status),
                                "subject": ticket.subject,
                                "ai_resolved": getattr(ticket, "ai_resolved", False),
                            })
                            await manager.broadcast_to_agents({
                                "type": "inbox_update",
                                "ticket_id": ticket_id,
                                "preview": body[:80],
                                "sender_name": user.name,
                                "subject": ticket.subject,
                                "status": ticket.status.value if hasattr(ticket.status, "value") else str(ticket.status),
                            })
                    except Exception:
                        pass

                    import asyncio
                    from app.services.ai.live_chat_adapter import live_chat_ai_adapter

                    async def handle_ai_response(msg_body: str, room_id: str):
                        try:
                            ai_msg = await live_chat_ai_adapter.process_live_chat_message(
                                ticket_id=room_id,
                                message_body=msg_body,
                            )
                            # Trigger Meta Outbound API send if originating from WhatsApp or Instagram
                            if ai_msg and ticket.channel.value == "whatsapp":
                                asyncio.create_task(_send_whatsapp_outbound(room_id, str(ai_msg.id), ai_msg.body))
                            elif ai_msg and ticket.channel.value == "instagram":
                                asyncio.create_task(_send_instagram_outbound(room_id, str(ai_msg.id), ai_msg.body))
                        except Exception as exc:
                            logger.error("[WS SERVER] Error in Live Chat AI processing for ticket %s: %s", room_id, exc, exc_info=True)

                    # Run asynchronously so we don't block the socket loop
                    asyncio.create_task(handle_ai_response(body, ticket_id))

    except WebSocketDisconnect:
        logger.info("[WS SERVER] Client disconnected normally | ticket=%s | user=%s (%s)", ticket_id, user.name, user.id)
    except RuntimeError as exc:
        logger.warning("[WS SERVER] Connection state error | ticket=%s | error=%s", ticket_id, exc)
    except Exception as exc:
        logger.error("[WS SERVER] Unexpected WebSocket error | ticket=%s | error=%s", ticket_id, exc, exc_info=True)
    finally:
        if connected:
            manager.disconnect(ticket_id, websocket)
            try:
                await manager.broadcast(ticket_id, {
                    "type": "presence_left",
                    "user_id": str(user.id),
                    "name": user.name,
                })
            except Exception:
                pass


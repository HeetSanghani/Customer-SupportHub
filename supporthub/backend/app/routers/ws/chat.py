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

                # Phase 5: AI Chatbot Auto-Reply for Customers
                if user.role.value == "customer":
                    import asyncio
                    from app.database import AsyncSessionLocal
                    
                    async def process_ai_reply(msg_body: str, room_id: str):
                        async with AsyncSessionLocal() as ai_session:
                            try:
                                from sqlalchemy import select
                                from app.models import Message, Ticket, User
                                from app.services.ai.orchestrator import AIOrchestrator
                                from app.services.ai.knowledge_rag import get_relevant_kb_context
                                
                                room_uuid = UUID(room_id)
                                fresh_ticket = await ai_session.get(Ticket, room_uuid)
                                fresh_user = await ai_session.get(User, fresh_ticket.customer_id)
                                
                                stmt = select(Message).where(Message.ticket_id == room_uuid).order_by(Message.created_at.asc())
                                history_msgs = (await ai_session.execute(stmt)).scalars().all()
                                
                                kb_context = await get_relevant_kb_context(ai_session, msg_body)
                                
                                orchestrator = AIOrchestrator(session=ai_session)
                                ai_out = await orchestrator.generate_for_ticket(
                                    ticket=fresh_ticket,
                                    messages=history_msgs,
                                    customer=fresh_user,
                                    kb_context=kb_context,
                                    tone="friendly",
                                )
                                
                                if isinstance(ai_out, dict):
                                    ai_text = ai_out.get("suggested_reply") or ai_out.get("response_text") or ""
                                else:
                                    ai_text = getattr(ai_out, "suggested_reply", None) or getattr(ai_out, "response_text", "")
                                    
                            except Exception as e:
                                import traceback
                                err_str = str(e)
                                logger.error("AI ERROR for ticket %s: %s\n%s", room_id, err_str[:500], traceback.format_exc())
                                if "429" in err_str or "quota" in err_str.lower() or "ResourceExhausted" in err_str:
                                    ai_text = "I'm sorry, our AI assistant is temporarily unavailable due to high demand. A human agent will assist you shortly."
                                else:
                                    ai_text = "I'm sorry, something went wrong on our end. Please try again in a moment."

                            if fresh_ticket:
                                fresh_ticket.updated_at = datetime.now()
                                ai_session.add(fresh_ticket)

                            ai_msg = Message(
                                ticket_id=UUID(room_id),
                                sender_id=None,
                                sender_type=SenderType.ai,
                                body=ai_text,
                            )
                            ai_session.add(ai_msg)
                            await ai_session.commit()
                            await ai_session.refresh(ai_msg)
                            
                            # Trigger Meta Outbound API send for AI reply
                            if ticket.channel.value == "whatsapp":
                                asyncio.create_task(_send_whatsapp_outbound(room_id, str(ai_msg.id), ai_text))
                            elif ticket.channel.value == "instagram":
                                asyncio.create_task(_send_instagram_outbound(room_id, str(ai_msg.id), ai_text))

                            await manager.broadcast(room_id, {
                                "type": "message",
                                "id": str(ai_msg.id),
                                "ticket_id": room_id,
                                "sender_id": "AI",
                                "sender_name": "Support AI",
                                "sender_role": "ai",
                                "body": ai_text,
                                "created_at": ai_msg.created_at.isoformat(),
                            })
                            
                            # Check resolution intent
                            fresh_ticket = await ai_session.get(Ticket, UUID(room_id))
                            if fresh_ticket:
                                user_msg = (msg_body or "").lower().strip()
                                ai_msg_str = (ai_text or "").lower().strip()
                                resolution_phrases = [
                                    "close this chat", "close chat", "end this chat", "end chat",
                                    "close ticket", "end ticket", "resolve ticket", "mark as resolved",
                                    "you can close", "you can end", "thanks, that fixed it", "thanks that fixed it",
                                    "that fixed it", "problem solved", "issue is resolved", "issue resolved"
                                ]
                                if any(phrase in user_msg for phrase in resolution_phrases) or (("close" in user_msg or "end" in user_msg) and ("chat" in user_msg or "ticket" in user_msg)) or ("pleasure assisting" in ai_msg_str and "have a great day" in ai_msg_str):
                                    from app.models import TicketStatus
                                    fresh_ticket.status = TicketStatus.resolved
                                    fresh_ticket.ai_resolved = True
                                    ai_session.add(fresh_ticket)
                                    await ai_session.commit()
                                    await ai_session.refresh(fresh_ticket)
                                    
                                    from app.services.csat_delivery import deliver_csat_survey
                                    await deliver_csat_survey(ai_session, fresh_ticket, fresh_user)

                            # Generate dynamic AI subject title from conversation topic
                            from app.ai import generate_ai_ticket_subject
                            ai_subj = await generate_ai_ticket_subject(ai_session, room_id)
                            if ai_subj and fresh_ticket:
                                fresh_ticket.subject = ai_subj

                            ticket_status = fresh_ticket.status.value if fresh_ticket else None

                            await manager.broadcast_to_agents({
                                "type": "inbox_update",
                                "ticket_id": room_id,
                                "preview": ai_text[:80],
                                "sender_name": "Support AI",
                                "subject": fresh_ticket.subject if fresh_ticket else "",
                                "status": ticket_status,
                            })
                            
                            await manager.broadcast(room_id, {
                                "type": "ticket_update",
                                "status": ticket_status,
                                "subject": fresh_ticket.subject if fresh_ticket else "",
                                "ai_resolved": fresh_ticket.ai_resolved if fresh_ticket else False,
                            })

                    # Run asynchronously so we don't block the socket
                    asyncio.create_task(process_ai_reply(body, ticket_id))

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


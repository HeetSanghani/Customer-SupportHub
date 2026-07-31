"""WebSocket chat endpoint — real-time messages per ticket room."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.dependencies import get_ws_user
from app.models import Message, SenderType, Ticket
from app.ws.manager import manager

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/chat/{ticket_id}")
async def websocket_chat(
    ticket_id: str,
    websocket: WebSocket,
    session: AsyncSession = Depends(get_session),
):
    user = await get_ws_user(websocket, session)
    if not user:
        return

    # Verify ticket exists
    ticket = await session.get(Ticket, UUID(ticket_id))
    if not ticket:
        await websocket.close(code=4004)
        return

    await manager.connect(ticket_id, websocket)

    # Announce presence
    await manager.broadcast(ticket_id, {
        "type": "presence",
        "user_id": str(user.id),
        "name": user.name,
        "role": user.role.value,
        "joined_at": datetime.utcnow().isoformat(),
    })

    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "message":
                body = data.get("body", "").strip()
                if not body:
                    continue

                # Persist message
                msg = Message(
                    ticket_id=UUID(ticket_id),
                    sender_id=user.id,
                    sender_type=SenderType(user.role.value)
                        if user.role.value in ("customer", "agent")
                        else SenderType.agent,
                    body=body,
                )
                session.add(msg)
                await session.commit()
                await session.refresh(msg)

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
                    from app.ai import generate_rag_response
                    from app.database import AsyncSessionLocal
                    
                    async def process_ai_reply(msg_body: str, room_id: str):
                        async with AsyncSessionLocal() as ai_session:
                            try:
                                ai_text = await generate_rag_response(ai_session, msg_body, room_id)
                            except Exception as e:
                                import traceback
                                err_str = str(e)
                                # Print full error to terminal so we can diagnose it
                                print(f"\n{'='*60}")
                                print(f"AI ERROR for ticket {room_id}:")
                                print(f"Type: {type(e).__name__}")
                                print(f"Message: {err_str[:500]}")
                                print(traceback.format_exc())
                                print(f"{'='*60}\n")
                                # Handle API quota exceeded gracefully
                                if "429" in err_str or "quota" in err_str.lower() or "ResourceExhausted" in err_str:
                                    ai_text = "I'm sorry, our AI assistant is temporarily unavailable due to high demand. A human agent will assist you shortly."
                                else:
                                    ai_text = "I'm sorry, something went wrong on our end. Please try again in a moment."

                            ai_msg = Message(
                                ticket_id=UUID(room_id),
                                sender_id=None,
                                sender_type=SenderType.ai,
                                body=ai_text,
                            )
                            ai_session.add(ai_msg)
                            await ai_session.commit()
                            await ai_session.refresh(ai_msg)
                            
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
                            
                            # Fetch current ticket status from DB to include in broadcast
                            # This avoids the frontend needing to make a separate API call
                            fresh_ticket = await ai_session.get(Ticket, UUID(room_id))
                            ticket_status = fresh_ticket.status.value if fresh_ticket else None

                            await manager.broadcast_to_agents({
                                "type": "inbox_update",
                                "ticket_id": room_id,
                                "preview": ai_text[:80],
                                "sender_name": "Support AI",
                            })
                            
                            # Broadcast ticket update WITH status so frontend locks instantly
                            await manager.broadcast(room_id, {
                                "type": "ticket_update",
                                "status": ticket_status,
                            })

                    # Run asynchronously so we don't block the socket
                    asyncio.create_task(process_ai_reply(body, ticket_id))

    except WebSocketDisconnect:
        manager.disconnect(ticket_id, websocket)
        await manager.broadcast(ticket_id, {
            "type": "presence_left",
            "user_id": str(user.id),
            "name": user.name,
        })

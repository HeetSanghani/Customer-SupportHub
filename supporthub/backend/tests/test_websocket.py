"""
tests/test_websocket.py

Tests for WebSocket manager, route authentication, duplicate accept prevention,
and real-time message broadcasting.
"""

import pytest
import uuid
import json
from unittest.mock import AsyncMock, MagicMock
from fastapi import WebSocket

from app.ws.manager import ConnectionManager
from app.services.instagram.webhook import process_instagram_webhook_background
from app.database import AsyncSessionLocal
from sqlmodel import select
from app.models import Message, Ticket, WebhookEvent


@pytest.mark.asyncio
async def test_connection_manager_no_duplicate_accept():
    """Verify ConnectionManager.connect stores the socket WITHOUT calling accept()."""
    mgr = ConnectionManager()
    ws_mock = MagicMock(spec=WebSocket)
    ws_mock.accept = AsyncMock()

    ticket_id = str(uuid.uuid4())
    await mgr.connect(ticket_id, ws_mock)

    # accept() should NOT have been called inside manager.connect
    ws_mock.accept.assert_not_called()
    assert ws_mock in mgr._rooms[ticket_id]


@pytest.mark.asyncio
async def test_connection_manager_prevents_duplicate_registration():
    """Verify ConnectionManager.connect prevents duplicate registration of the same socket."""
    mgr = ConnectionManager()
    ws_mock = MagicMock(spec=WebSocket)

    ticket_id = str(uuid.uuid4())
    await mgr.connect(ticket_id, ws_mock)
    await mgr.connect(ticket_id, ws_mock)

    assert len(mgr._rooms[ticket_id]) == 1
    assert mgr._rooms[ticket_id][0] == ws_mock


@pytest.mark.asyncio
async def test_connection_manager_disconnect_idempotent_and_cleans_room():
    """Verify ConnectionManager.disconnect is idempotent and prunes empty rooms."""
    mgr = ConnectionManager()
    ws_mock = MagicMock(spec=WebSocket)

    ticket_id = str(uuid.uuid4())
    await mgr.connect(ticket_id, ws_mock)
    assert ticket_id in mgr._rooms

    # Disconnect once
    mgr.disconnect(ticket_id, ws_mock)
    assert ticket_id not in mgr._rooms

    # Disconnect again (idempotent, does not throw)
    mgr.disconnect(ticket_id, ws_mock)
    assert ticket_id not in mgr._rooms


@pytest.mark.asyncio
async def test_connection_manager_broadcast_and_disconnect():
    """Verify room broadcasting and dead client cleanup."""
    mgr = ConnectionManager()
    ticket_id = str(uuid.uuid4())

    ws1 = MagicMock(spec=WebSocket)
    ws1.send_json = AsyncMock()

    ws2 = MagicMock(spec=WebSocket)
    ws2.send_json = AsyncMock(side_effect=Exception("Connection lost"))

    await mgr.connect(ticket_id, ws1)
    await mgr.connect(ticket_id, ws2)

    assert len(mgr._rooms[ticket_id]) == 2

    # Broadcast data
    test_data = {"type": "message", "body": "hello"}
    await mgr.broadcast(ticket_id, test_data)

    ws1.send_json.assert_called_once_with(test_data)
    # ws2 should have been disconnected due to exception
    assert len(mgr._rooms[ticket_id]) == 1
    assert ws1 in mgr._rooms[ticket_id]



@pytest.mark.asyncio
async def test_instagram_webhook_broadcasts_after_commit():
    """Verify Instagram background worker broadcasts WebSocket message after DB commit."""
    from app.ws.manager import manager

    test_mid = f"m_ws_broadcast_test_{uuid.uuid4().hex[:8]}"
    sender_igsid = f"23086741_{uuid.uuid4().hex[:4]}"

    payload = {
        "object": "instagram",
        "entry": [
            {
                "time": 1786363356841,
                "id": "17841435478991883",
                "messaging": [
                    {
                        "sender": {"id": sender_igsid},
                        "recipient": {"id": "17841435478991883"},
                        "timestamp": 1786363356298,
                        "message": {
                            "mid": test_mid,
                            "text": "WS BROADCAST INTEGRATION TEST"
                        }
                    }
                ]
            }
        ]
    }

    # Mock manager.broadcast to capture event
    original_broadcast = manager.broadcast
    broadcast_events = []

    async def mock_broadcast(ticket_id, data):
        broadcast_events.append((ticket_id, data))
        await original_broadcast(ticket_id, data)

    manager.broadcast = mock_broadcast

    try:
        await process_instagram_webhook_background(payload)

        # Verify message was saved to DB
        async with AsyncSessionLocal() as db:
            msg = (await db.exec(select(Message).where(Message.external_message_id == test_mid))).first()
            assert msg is not None
            assert msg.body == "WS BROADCAST INTEGRATION TEST"

            # Verify broadcast was called with matching ticket_id and message body
            assert len(broadcast_events) >= 1
            broadcast_ticket_id, broadcast_payload = broadcast_events[0]
            assert broadcast_ticket_id == str(msg.ticket_id)
            assert broadcast_payload["type"] == "message"
            assert broadcast_payload["body"] == "WS BROADCAST INTEGRATION TEST"
            assert broadcast_payload["id"] == str(msg.id)
    finally:
        manager.broadcast = original_broadcast


@pytest.mark.asyncio
async def test_instagram_webhook_broadcasts_to_exact_ticket_uuid():
    """Verify Instagram webhook broadcast routes to exact existing ticket UUID and broadcasts after commit."""
    from app.ws.manager import manager
    from app.models import User, Ticket, UserRole, UserStatus, TicketChannel, TicketStatus, TicketPriority

    target_ticket_uuid = uuid.UUID("f84f326f-8fd7-4582-97d0-ac023dc09b08")
    sender_igsid = "2308674163238603"
    test_mid = f"m_exact_test_{uuid.uuid4().hex[:8]}"

    # Ensure user and ticket exist in DB
    async with AsyncSessionLocal() as db:
        user = (await db.exec(select(User).where(User.channel_customer_id == sender_igsid))).first()
        if not user:
            user = User(
                email=f"instagram_{sender_igsid}@supporthub.local",
                name="Instagram User (23086741)",
                password_hash="test_pass",
                role=UserRole.customer,
                status=UserStatus.active,
                channel_customer_id=sender_igsid,
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

        ticket = await db.get(Ticket, target_ticket_uuid)
        if not ticket:
            ticket = Ticket(
                id=target_ticket_uuid,
                ref="TCK-40555",
                customer_id=user.id,
                subject="Instagram DM from 23086741",
                category="instagram",
                channel=TicketChannel.instagram,
                status=TicketStatus.new,
                priority=TicketPriority.medium,
            )
            db.add(ticket)
            await db.commit()
            await db.refresh(ticket)

    payload = {
        "object": "instagram",
        "entry": [
            {
                "time": 1786363356841,
                "id": "17841435478991883",
                "messaging": [
                    {
                        "sender": {"id": sender_igsid},
                        "recipient": {"id": "17841435478991883"},
                        "timestamp": 1786363356298,
                        "message": {
                            "mid": test_mid,
                            "text": "PRODUCTION REALTIME FINAL TEST 1835"
                        }
                    }
                ]
            }
        ]
    }

    original_broadcast = manager.broadcast
    broadcast_events = []

    async def mock_broadcast(ticket_id, data):
        broadcast_events.append((ticket_id, data))
        await original_broadcast(ticket_id, data)

    manager.broadcast = mock_broadcast

    try:
        await process_instagram_webhook_background(payload)

        async with AsyncSessionLocal() as db:
            msg = (await db.exec(select(Message).where(Message.external_message_id == test_mid))).first()
            assert msg is not None
            assert msg.ticket_id == target_ticket_uuid
            assert msg.body == "PRODUCTION REALTIME FINAL TEST 1835"

            assert len(broadcast_events) >= 1
            broadcast_ticket_id, broadcast_payload = broadcast_events[0]
            assert broadcast_ticket_id == "f84f326f-8fd7-4582-97d0-ac023dc09b08"
            assert broadcast_payload["type"] == "message"
            assert broadcast_payload["ticket_id"] == "f84f326f-8fd7-4582-97d0-ac023dc09b08"
            assert broadcast_payload["body"] == "PRODUCTION REALTIME FINAL TEST 1835"
            assert broadcast_payload["id"] == str(msg.id)
    finally:
        manager.broadcast = original_broadcast


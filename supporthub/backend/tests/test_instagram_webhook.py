"""
tests/test_instagram_webhook.py

Unit tests for Instagram Webhook Router and Ingestion Processing.
Tests GET handshake verification, POST HMAC signature validation with instagram_app_secret,
entry.changes payload compatibility, database user/ticket/message creation, idempotency,
and failure resilience.
"""

import hmac
import hashlib
import json
import pytest
from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.config import get_settings
from app.models import TicketChannel, TicketStatus, SenderType

settings = get_settings()
client = TestClient(app)


def compute_signature(payload_bytes: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
    return f"sha256={sig}"


def test_get_webhook_verification_success():
    """Test 1: GET webhook verification succeeds with valid token and mode."""
    expected_token = settings.meta_verify_token or "supporthub_verify"
    response = client.get(
        "/api/v1/webhooks/instagram",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "987654321",
            "hub.verify_token": expected_token,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "987654321"


def test_get_webhook_verification_invalid_token():
    """Test 2: GET webhook verification fails (403) with invalid verify token."""
    response = client.get(
        "/api/v1/webhooks/instagram",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "987654321",
            "hub.verify_token": "wrong_token_123",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_webhook_verification_wrong_mode():
    """Test 3: GET webhook verification fails (403) with invalid hub.mode."""
    expected_token = settings.meta_verify_token or "supporthub_verify"
    response = client.get(
        "/api/v1/webhooks/instagram",
        params={
            "hub.mode": "unsubscribe",
            "hub.challenge": "987654321",
            "hub.verify_token": expected_token,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_webhook_missing_signature():
    """Test 4: POST webhook fails (403) when signature header is missing in production."""
    with patch.object(settings, "instagram_app_secret", "test_ig_secret_123"):
        with patch.object(settings, "app_env", "production"):
            payload = {"object": "instagram", "entry": []}
            response = client.post(
                "/api/v1/webhooks/instagram",
                json=payload,
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_webhook_invalid_signature():
    """Test 5: POST webhook fails (403) when HMAC signature is invalid."""
    with patch.object(settings, "instagram_app_secret", "test_ig_secret_123"):
        payload = {"object": "instagram", "entry": []}
        payload_bytes = json.dumps(payload).encode("utf-8")
        invalid_sig = compute_signature(payload_bytes, "wrong_secret_123")

        response = client.post(
            "/api/v1/webhooks/instagram",
            content=payload_bytes,
            headers={"X-Hub-Signature-256": invalid_sig, "Content-Type": "application/json"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_webhook_valid_instagram_secret_signature_success():
    """Test 6: POST webhook succeeds (200) when signed specifically with instagram_app_secret."""
    secret = "my_custom_instagram_app_secret_999"
    payload = {"object": "instagram", "entry": []}
    payload_bytes = json.dumps(payload).encode("utf-8")
    sig = compute_signature(payload_bytes, secret)

    with patch.object(settings, "instagram_app_secret", secret):
        with patch("app.routers.webhooks.instagram.BackgroundTasks.add_task") as mock_add_task:
            response = client.post(
                "/api/v1/webhooks/instagram",
                content=payload_bytes,
                headers={"X-Hub-Signature-256": sig, "Content-Type": "application/json"},
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_process_instagram_webhook_meta_changes_payload():
    """Test 7: Background worker parses Meta's entry[].changes[].value structure correctly."""
    from app.services.instagram.webhook import process_instagram_webhook_background

    import uuid
    test_igsid = f"998877_{uuid.uuid4().hex[:6]}"
    test_mid = f"m_mid_changes_{uuid.uuid4().hex[:8]}"
    test_text = "Testing Meta changes field format"

    changes_payload = {
        "object": "instagram",
        "entry": [
            {
                "id": "28564753216451440",
                "time": 1786347229,
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "sender": {"id": test_igsid},
                            "recipient": {"id": "28564753216451440"},
                            "timestamp": "1527459824",
                            "message": {
                                "mid": test_mid,
                                "text": test_text
                            }
                        }
                    }
                ]
            }
        ]
    }

    # Execute background worker
    await process_instagram_webhook_background(changes_payload)

    # Verify database records
    from app.database import AsyncSessionLocal
    from sqlmodel import select
    from app.models import User, Ticket, Message, WebhookEvent

    async with AsyncSessionLocal() as db:
        # Check User
        stmt_user = select(User).where(User.channel_customer_id == test_igsid)
        user = (await db.exec(stmt_user)).first()
        assert user is not None

        # Check Message
        stmt_msg = select(Message).where(Message.external_message_id == test_mid)
        msg = (await db.exec(stmt_msg)).first()
        assert msg is not None
        assert msg.body == test_text

        # Teardown test records
        from sqlmodel import delete
        stmt_t = select(Ticket).where(Ticket.customer_id == user.id)
        ticket_obj = (await db.exec(stmt_t)).first()
        if ticket_obj:
            await db.exec(delete(Message).where(Message.ticket_id == ticket_obj.id))
            await db.exec(delete(Ticket).where(Ticket.id == ticket_obj.id))
        await db.exec(delete(User).where(User.id == user.id))
        await db.exec(delete(WebhookEvent).where(WebhookEvent.event_id == test_mid))
        await db.commit()


@pytest.mark.asyncio
async def test_idempotency_duplicate_message_skipped():
    """Test 8: Duplicate message with same mid is safely skipped."""
    import uuid
    from app.services.instagram.webhook import process_instagram_webhook_background

    test_igsid = f"17841499_{uuid.uuid4().hex[:6]}"
    test_mid = f"m_mid_duplicate_test_{uuid.uuid4().hex[:8]}"

    payload = {
        "object": "instagram",
        "entry": [
            {
                "id": "28564753216451440",
                "messaging": [
                    {
                        "sender": {"id": test_igsid},
                        "recipient": {"id": "28564753216451440"},
                        "message": {"mid": test_mid, "text": "First attempt"}
                    }
                ]
            }
        ]
    }

    # Run twice sequentially
    await process_instagram_webhook_background(payload)
    await process_instagram_webhook_background(payload)

    # Verify only one Message created
    from app.database import AsyncSessionLocal
    from sqlmodel import select, delete
    from app.models import Message, WebhookEvent, Ticket, User, SenderType

    async with AsyncSessionLocal() as db:
        stmt_msg = select(Message).where(Message.external_message_id == test_mid)
        msgs = (await db.exec(stmt_msg)).all()
        assert len(msgs) == 1

        stmt_evt = select(WebhookEvent).where(WebhookEvent.event_id == test_mid)
        evts = (await db.exec(stmt_evt)).all()
        assert len(evts) == 1

        # Teardown test records
        user = (await db.exec(select(User).where(User.channel_customer_id == test_igsid))).first()
        if user:
            stmt_t = select(Ticket).where(Ticket.customer_id == user.id)
            t_obj = (await db.exec(stmt_t)).first()
            if t_obj:
                await db.exec(delete(Message).where(Message.ticket_id == t_obj.id))
                await db.exec(delete(Ticket).where(Ticket.id == t_obj.id))
            await db.exec(delete(User).where(User.id == user.id))
        await db.exec(delete(WebhookEvent).where(WebhookEvent.event_id == test_mid))
        await db.commit()


@pytest.mark.asyncio
async def test_process_instagram_webhook_real_payload_success():
    """Test 9: Processing a real Instagram DM webhook creates User, Ticket, and Message."""
    import uuid
    from app.services.instagram.webhook import process_instagram_webhook_background
    from app.database import AsyncSessionLocal
    from sqlmodel import select, delete
    from app.models import Message, Ticket, User, WebhookEvent, TicketChannel

    test_mid = f"m_real_test_{uuid.uuid4().hex[:8]}"
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
                            "text": "INSTAGRAM E2E TEST 2026-NEW-001"
                        }
                    }
                ]
            }
        ]
    }

    await process_instagram_webhook_background(payload)

    async with AsyncSessionLocal() as db:
        # Check Message
        msg = (await db.exec(select(Message).where(Message.external_message_id == test_mid))).first()
        assert msg is not None
        assert msg.body == "INSTAGRAM E2E TEST 2026-NEW-001"

        # Check Ticket
        ticket = (await db.exec(select(Ticket).where(Ticket.id == msg.ticket_id))).first()
        assert ticket is not None
        assert ticket.channel == TicketChannel.instagram
        assert ticket.category == "instagram"

        # Check User
        user = (await db.exec(select(User).where(User.id == ticket.customer_id))).first()
        assert user is not None
        assert user.channel_customer_id == sender_igsid

        # Check WebhookEvent
        evt = (await db.exec(select(WebhookEvent).where(WebhookEvent.event_id == test_mid))).first()
        assert evt is not None
        assert evt.processed is True

        # Teardown test records
        await db.exec(delete(Message).where(Message.ticket_id == ticket.id))
        await db.exec(delete(Ticket).where(Ticket.id == ticket.id))
        await db.exec(delete(User).where(User.id == user.id))
        await db.exec(delete(WebhookEvent).where(WebhookEvent.event_id == test_mid))
        await db.commit()


@pytest.mark.asyncio
async def test_process_instagram_webhook_invalid_recipient_skipped():
    """Test 10: Instagram event with unknown recipient ID is skipped without database creation."""
    import uuid
    from app.services.instagram.webhook import process_instagram_webhook_background
    from app.database import AsyncSessionLocal
    from sqlmodel import select
    from app.models import Message, WebhookEvent

    test_mid = f"m_unmatched_test_{uuid.uuid4().hex[:8]}"

    payload = {
        "object": "instagram",
        "entry": [
            {
                "id": "99999999999999999",
                "messaging": [
                    {
                        "sender": {"id": "123456"},
                        "recipient": {"id": "99999999999999999"},
                        "message": {"mid": test_mid, "text": "Unmatched account text"}
                    }
                ]
            }
        ]
    }

    with patch.object(settings, "instagram_account_id", "28564753216451440"):
        await process_instagram_webhook_background(payload)

    async with AsyncSessionLocal() as db:
        msg = (await db.exec(select(Message).where(Message.external_message_id == test_mid))).first()
        assert msg is None

        evt = (await db.exec(select(WebhookEvent).where(WebhookEvent.event_id == test_mid))).first()
        assert evt is None


@pytest.mark.asyncio
async def test_single_ticket_reused_for_subsequent_messages():
    """Test 11: Subsequent incoming messages from the same user reuse the single existing ticket."""
    import uuid
    from app.services.instagram.webhook import process_instagram_webhook_background
    from app.database import AsyncSessionLocal
    from sqlmodel import select, delete
    from app.models import Ticket, Message, User, WebhookEvent, SenderType

    test_igsid = f"178414_{uuid.uuid4().hex[:8]}"
    mid1 = f"m_mid_reuse_1_{uuid.uuid4().hex[:6]}"
    mid2 = f"m_mid_reuse_2_{uuid.uuid4().hex[:6]}"

    payload1 = {
        "object": "instagram",
        "entry": [
            {
                "id": "28564753216451440",
                "messaging": [
                    {
                        "sender": {"id": test_igsid},
                        "recipient": {"id": "28564753216451440"},
                        "message": {"mid": mid1, "text": "First message from customer"}
                    }
                ]
            }
        ]
    }

    payload2 = {
        "object": "instagram",
        "entry": [
            {
                "id": "28564753216451440",
                "messaging": [
                    {
                        "sender": {"id": test_igsid},
                        "recipient": {"id": "28564753216451440"},
                        "message": {"mid": mid2, "text": "Second message from same customer"}
                    }
                ]
            }
        ]
    }

    # First message creates ticket
    await process_instagram_webhook_background(payload1)

    # Second message should reuse the same ticket
    await process_instagram_webhook_background(payload2)

    async with AsyncSessionLocal() as db:
        user = (await db.exec(select(User).where(User.channel_customer_id == test_igsid))).first()
        assert user is not None

        tickets = (await db.exec(select(Ticket).where(Ticket.customer_id == user.id, Ticket.channel == 'instagram'))).all()
        # Exactly ONE ticket created for this user!
        assert len(tickets) == 1

        messages = (await db.exec(select(Message).where(Message.ticket_id == tickets[0].id))).all()
        cust_messages = [m for m in messages if m.sender_type == SenderType.customer]
        # Both customer messages saved in the same ticket
        assert len(cust_messages) == 2

        # Teardown test records
        await db.exec(delete(Message).where(Message.ticket_id == tickets[0].id))
        await db.exec(delete(Ticket).where(Ticket.id == tickets[0].id))
        await db.exec(delete(User).where(User.id == user.id))
        await db.exec(delete(WebhookEvent).where(WebhookEvent.event_id.in_([mid1, mid2])))
        await db.commit()




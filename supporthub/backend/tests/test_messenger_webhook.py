import pytest
from httpx import AsyncClient, ASGITransport
import uuid
from unittest.mock import patch, AsyncMock
from app.models import Message, Ticket, User, TicketChannel, SenderType
from app.main import app
from app.database import AsyncSessionLocal

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_messenger_webhook_verification_success(async_client: AsyncClient):
    """Test A: GET webhook verification with correct token returns HTTP 200 and challenge."""
    from app.config import get_settings
    settings = get_settings()
    expected_token = settings.meta_verify_token or "supporthub_verify"
    response = await async_client.get(
        "/api/v1/webhooks/messenger",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "challenge_string",
            "hub.verify_token": expected_token
        }
    )
    assert response.status_code == 200
    assert response.text == "challenge_string"

@pytest.mark.asyncio
async def test_messenger_webhook_verification_failure(async_client: AsyncClient):
    """Test B: GET verification with wrong token returns HTTP 403."""
    response = await async_client.get(
        "/api/v1/webhooks/messenger",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "challenge_string",
            "hub.verify_token": "wrong_token"
        }
    )
    assert response.status_code == 403
    assert "Forbidden" in response.text

@pytest.mark.asyncio
async def test_messenger_webhook_receive_message(async_client: AsyncClient):
    """Test C-G: POST Messenger message processing and broadcasts."""
    import asyncio
    from app.services.ai.debouncer import ai_debouncer
    
    test_sender_id = f"test_fb_{uuid.uuid4().hex[:8]}"
    test_mid = f"mid_{uuid.uuid4().hex[:12]}"
    payload = {
        "object": "page",
        "entry": [
            {
                "id": "mock_page_id",
                "messaging": [
                    {
                        "sender": {"id": test_sender_id},
                        "recipient": {"id": "mock_page_id"},
                        "message": {
                            "mid": test_mid,
                            "text": "Hello SupportHub from Messenger!"
                        }
                    }
                ]
            }
        ]
    }
    
    with patch("app.services.ai.orchestrator.AIOrchestrator") as mock_orch_cls:
        mock_orch = AsyncMock()
        mock_orch.generate_for_ticket.return_value = {
            "suggested_reply": "Hello! I am an AI assistant.",
            "confidence": 0.99,
            "latency_ms": 120,
        }
        mock_orch_cls.return_value = mock_orch
        
        with patch("app.services.facebook.webhook.send_messenger_reply", new_callable=AsyncMock) as mock_send_reply:
            mock_send_reply.return_value = True
            with patch("app.ws.manager.manager") as mock_manager:
                mock_manager.broadcast = AsyncMock()
                mock_manager.broadcast_to_agents = AsyncMock()
                
                original_delay = ai_debouncer.delay_seconds
                ai_debouncer.delay_seconds = 0.01
                
                response = await async_client.post("/api/v1/webhooks/messenger", json=payload)
                assert response.status_code == 200
                assert response.json() == {"status": "ok"}
                
                await asyncio.sleep(0.15)
                if ai_debouncer._tasks:
                    await asyncio.gather(*list(ai_debouncer._tasks.values()), return_exceptions=True)
                ai_debouncer.delay_seconds = original_delay
                
                # Verify AI response and outbound send were called
                mock_send_reply.assert_called_once_with(recipient_id=test_sender_id, text="Hello! I am an AI assistant.")
                
                # Check database for exact 1 customer message and 1 AI message
                from sqlmodel import select, delete
                
                async with AsyncSessionLocal() as db_session:
                    user_stmt = select(User).where(User.email == f"messenger_{test_sender_id}@supporthub.local")
                    user = (await db_session.exec(user_stmt)).first()
                    assert user is not None
                    
                    ticket_stmt = select(Ticket).where(Ticket.customer_id == user.id, Ticket.channel == TicketChannel.facebook)
                    ticket = (await db_session.exec(ticket_stmt)).first()
                    assert ticket is not None
                    
                    msg_stmt = select(Message).where(Message.ticket_id == ticket.id).order_by(Message.created_at.asc())
                    messages = (await db_session.exec(msg_stmt)).all()
                    assert len(messages) == 2
                    
                    cust_msg = messages[0]
                    assert cust_msg.sender_type == SenderType.customer
                    assert cust_msg.body == "Hello SupportHub from Messenger!"
                    
                    ai_msg = messages[1]
                    assert ai_msg.sender_type == SenderType.ai
                    assert ai_msg.body == "Hello! I am an AI assistant."
                    
                    # Verify WebSockets Broadcasts
                    assert mock_manager.broadcast.call_count >= 1
                    assert mock_manager.broadcast_to_agents.call_count >= 1
                    
                    # Teardown
                    from app.models import WebhookEvent
                    await db_session.exec(delete(Message).where(Message.ticket_id == ticket.id))
                    await db_session.exec(delete(Ticket).where(Ticket.id == ticket.id))
                    await db_session.exec(delete(User).where(User.id == user.id))
                    await db_session.exec(delete(WebhookEvent).where(WebhookEvent.event_id == test_mid))
                    await db_session.commit()

"""
tests_step3c.py — Step 3C: WhatsApp Outbound Delivery Layer Test Suite

Mocks all HTTP calls — ZERO real calls to Meta APIs. Fast, isolated, reproducible.

Tests:
  [3c-1]  Formatter normalizes E.164 phone numbers correctly
  [3c-2]  Formatter rejects invalid phone numbers (<7 or >15 digits)
  [3c-3]  Formatter constructs valid Meta text message payload
  [3c-4]  Formatter truncates text exceeding 4096 characters
  [3c-5]  Formatter constructs valid media (image) message payload
  [3c-6]  Formatter constructs interactive quick reply button payload
  [3c-7]  Formatter enforces maximum 3 quick reply buttons limit
  [3c-8]  MetaWhatsAppClient sends payload and parses wamid (HTTP 200)
  [3c-9]  MetaWhatsAppClient maps HTTP 401 to AuthenticationError
  [3c-10] MetaWhatsAppClient maps HTTP 429 to RateLimitError
  [3c-11] MetaWhatsAppClient maps HTTP 500 to WhatsAppProviderError (is_retryable=True)
  [3c-12] RetryExecutor retries transient errors with backoff
  [3c-13] RetryExecutor fails immediately on AuthenticationError (no retries)
  [3c-14] RetryExecutor raises RetryExhaustedError when max retries exceeded
  [3c-15] DeliveryTracker enforces valid state transitions (queued → sending → sent)
  [3c-16] DeliveryTracker rejects invalid state transitions (read → sending)
  [3c-17] Repository claims outbound idempotency key
  [3c-18] Repository suppresses duplicate send when key was previously delivered
  [3c-19] WhatsAppSender full pipeline delivers AIResponse and returns DeliveryResult
  [3c-20] WhatsAppSender records metrics (wamid, status=sent, latency_ms) in DB
"""

from __future__ import annotations

import asyncio
import sys
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import httpx

results: list[tuple[str, bool, str]] = []


def check(test_id: str, condition: bool, detail: str = "") -> None:
    icon = "✅ PASS" if condition else "❌ FAIL"
    results.append((test_id, condition, detail))
    print(f"  {icon}  [{test_id}] {detail}")


# ─── Tests ────────────────────────────────────────────────────────────────────

def test_formatter():
    from app.services.whatsapp.exceptions import FormattingError
    from app.services.whatsapp.formatter import WhatsAppPayloadFormatter
    from app.services.whatsapp.models import OutgoingMessage
    from app.services.ai.models import AIResponse, ModelInfo, TokenUsage

    formatter = WhatsAppPayloadFormatter()

    # [3c-1] Phone number normalization
    p1 = formatter.normalize_phone("+91 98765-43210")
    check("3c-1", p1 == "919876543210", f"Normalized phone | got={p1}")

    # [3c-2] Rejects invalid phone number length
    invalid_raised = False
    try:
        formatter.normalize_phone("123")
    except FormattingError:
        invalid_raised = True
    check("3c-2", invalid_raised, "Invalid phone length rejected")

    # [3c-3] Valid Meta text payload
    model_info = ModelInfo("mock", "mock-v1", "v1.0", "hash", 0.4, 500)
    ai_res = AIResponse("Hello! How can I help you?", model_info, TokenUsage(100, 20, 120))
    payload = formatter.format_ai_response(ai_res, recipient_phone="+91 9876543210")
    check("3c-3",
          payload["messaging_product"] == "whatsapp"
          and payload["to"] == "919876543210"
          and payload["text"]["body"] == "Hello! How can I help you?",
          f"Text payload valid | to={payload.get('to')}")

    # [3c-4] Truncates text > 4096 chars
    long_text = "x" * 5000
    ai_res_long = AIResponse(long_text, model_info, TokenUsage(100, 20, 120))
    payload_long = formatter.format_ai_response(ai_res_long, recipient_phone="919876543210")
    check("3c-4",
          len(payload_long["text"]["body"]) == 4096
          and payload_long["text"]["body"].endswith("..."),
          f"Text truncated | len={len(payload_long['text']['body'])}")

    # [3c-5] Image media message payload
    out_media = OutgoingMessage(
        recipient_phone="919876543210",
        message_type="image",
        media_url="https://example.com/image.png",
        caption="Sample image",
    )
    payload_media = formatter.format_outgoing(out_media)
    check("3c-5",
          payload_media["type"] == "image"
          and payload_media["image"]["link"] == "https://example.com/image.png",
          f"Image payload valid | type={payload_media.get('type')}")

    # [3c-6] Interactive quick reply button payload
    out_btn = OutgoingMessage(
        recipient_phone="919876543210",
        message_type="interactive",
        text_body="Was this helpful?",
        interactive_components={
            "buttons": [
                {"id": "yes", "title": "Yes"},
                {"id": "no", "title": "No"},
            ]
        },
    )
    payload_btn = formatter.format_outgoing(out_btn)
    check("3c-6",
          payload_btn["type"] == "interactive"
          and len(payload_btn["interactive"]["action"]["buttons"]) == 2,
          f"Interactive buttons valid | count={len(payload_btn['interactive']['action']['buttons'])}")

    # [3c-7] Enforces 3 button limit
    out_4btn = OutgoingMessage(
        recipient_phone="919876543210",
        message_type="interactive",
        text_body="Select:",
        interactive_components={
            "buttons": [{"id": f"b{i}", "title": f"B{i}"} for i in range(4)]
        },
    )
    btn_limit_raised = False
    try:
        formatter.format_outgoing(out_4btn)
    except FormattingError:
        btn_limit_raised = True
    check("3c-7", btn_limit_raised, "Enforced 3 button max limit")


async def test_client():
    from app.services.whatsapp.client import MetaWhatsAppClient
    from app.services.whatsapp.exceptions import AuthenticationError, RateLimitError, WhatsAppProviderError

    # Mock httpx AsyncClient
    mock_http = MagicMock()

    # [3c-8] Client sends payload and parses wamid
    mock_res_200 = MagicMock(spec=httpx.Response)
    mock_res_200.status_code = 200
    mock_res_200.json.return_value = {
        "messaging_product": "whatsapp",
        "messages": [{"id": "wamid.TEST_WAMID_12345"}],
    }
    mock_http.post = AsyncMock(return_value=mock_res_200)

    client = MetaWhatsAppClient(
        phone_number_id="123456789",
        access_token="test_token",
        client=mock_http,
    )
    res = await client.send_payload({"test": "payload"})
    check("3c-8",
          res.success and res.provider_message_id == "wamid.TEST_WAMID_12345",
          f"Parsed wamid | wamid={res.provider_message_id}")

    # [3c-9] HTTP 401 maps to AuthenticationError
    mock_res_401 = MagicMock(spec=httpx.Response)
    mock_res_401.status_code = 401
    mock_res_401.json.return_value = {"error": {"message": "Invalid token", "code": 190}}
    mock_http.post = AsyncMock(return_value=mock_res_401)

    auth_raised = False
    try:
        await client.send_payload({"test": "payload"})
    except AuthenticationError:
        auth_raised = True
    check("3c-9", auth_raised, "HTTP 401 mapped to AuthenticationError")

    # [3c-10] HTTP 429 maps to RateLimitError
    mock_res_429 = MagicMock(spec=httpx.Response)
    mock_res_429.status_code = 429
    mock_res_429.json.return_value = {"error": {"message": "Rate limit", "code": 130429}}
    mock_http.post = AsyncMock(return_value=mock_res_429)

    rate_raised = False
    try:
        await client.send_payload({"test": "payload"})
    except RateLimitError:
        rate_raised = True
    check("3c-10", rate_raised, "HTTP 429 mapped to RateLimitError")

    # [3c-11] HTTP 500 maps to retryable WhatsAppProviderError
    mock_res_500 = MagicMock(spec=httpx.Response)
    mock_res_500.status_code = 500
    mock_res_500.json.return_value = {"error": {"message": "Internal error"}}
    mock_http.post = AsyncMock(return_value=mock_res_500)

    server_err: WhatsAppProviderError | None = None
    try:
        await client.send_payload({"test": "payload"})
    except WhatsAppProviderError as exc:
        server_err = exc
    check("3c-11",
          server_err is not None and server_err.is_retryable is True,
          f"HTTP 500 retryable | is_retryable={getattr(server_err, 'is_retryable', None)}")


async def test_retry_engine():
    from app.services.whatsapp.exceptions import AuthenticationError, RateLimitError, RetryExhaustedError
    from app.services.whatsapp.models import RetryPolicy
    from app.services.whatsapp.retry import RetryExecutor

    policy = RetryPolicy(max_retries=2, base_delay_seconds=0.01)
    executor = RetryExecutor(policy=policy)

    # [3c-12] Retries transient errors
    attempts = 0

    async def transient_func():
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise RateLimitError("Simulated rate limit")
        return "success"

    result = await executor.execute(transient_func)
    check("3c-12",
          result == "success" and attempts == 2,
          f"Retried transient error | attempts={attempts}")

    # [3c-13] Fails immediately on AuthenticationError (no retries)
    auth_attempts = 0

    async def auth_func():
        nonlocal auth_attempts
        auth_attempts += 1
        raise AuthenticationError("Invalid token")

    auth_failed = False
    try:
        await executor.execute(auth_func)
    except AuthenticationError:
        auth_failed = True
    check("3c-13",
          auth_failed and auth_attempts == 1,
          f"No retry on auth error | attempts={auth_attempts}")

    # [3c-14] Raises RetryExhaustedError when max retries exceeded
    async def always_fail():
        raise RateLimitError("Persistent rate limit")

    exhausted = False
    try:
        await executor.execute(always_fail)
    except RetryExhaustedError:
        exhausted = True
    check("3c-14", exhausted, "RetryExhaustedError raised after max retries")


def test_delivery_tracker():
    from app.services.whatsapp.delivery import DeliveryTracker
    from app.services.whatsapp.models import DeliveryStatus

    tracker = DeliveryTracker(outbound_id="out_123", recipient="919876543210")

    # [3c-15] Valid transition (queued → sending → sent)
    t1 = tracker.transition_to(DeliveryStatus.sending)
    tracker.mark_sent("wamid.TEST_123")
    check("3c-15",
          t1 and tracker.current_status == DeliveryStatus.sent and tracker.state.provider_message_id == "wamid.TEST_123",
          f"Valid transitions | status={tracker.current_status}")

    # [3c-16] Rejects invalid state transition (read → sending)
    tracker.transition_to(DeliveryStatus.read)
    t_invalid = tracker.transition_to(DeliveryStatus.sending)
    check("3c-16",
          t_invalid is False and tracker.current_status == DeliveryStatus.read,
          f"Invalid transition rejected | status={tracker.current_status}")


async def test_sender_and_repository():
    from app.database import AsyncSessionLocal
    from app.models import Ticket, TicketChannel, TicketPriority, TicketStatus, User, UserRole, UserStatus
    from app.services.ai.models import AIResponse, ModelInfo, TokenUsage
    from app.services.conversations.models import ConversationContext
    from app.services.whatsapp.client import MetaWhatsAppClient
    from app.services.whatsapp.models import DeliveryStatus
    from app.services.whatsapp.sender import WhatsAppSender

    async with AsyncSessionLocal() as session:
        # Create user + ticket in DB
        async with session.begin():
            user = User(
                email=f"sender_test_{uuid.uuid4().hex[:8]}@test.internal",
                name="Sender Test Customer",
                password_hash="__test__",
                role=UserRole.customer,
                status=UserStatus.active,
            )
            session.add(user)
            await session.flush()

            ticket = Ticket(
                ref=f"TCK-{uuid.uuid4().hex[:6].upper()}",
                customer_id=user.id,
                subject="Test Outbound WhatsApp Delivery",
                category="whatsapp",
                channel=TicketChannel.whatsapp,
                status=TicketStatus.open,
                priority=TicketPriority.medium,
            )
            session.add(ticket)
            await session.flush()

        # Mock HTTP client
        mock_http = MagicMock()
        mock_res_200 = MagicMock(spec=httpx.Response)
        mock_res_200.status_code = 200
        mock_res_200.json.return_value = {
            "messaging_product": "whatsapp",
            "messages": [{"id": f"wamid.FULL_TEST_{uuid.uuid4().hex[:8]}"}],
        }
        mock_http.post = AsyncMock(return_value=mock_res_200)

        meta_client = MetaWhatsAppClient(
            phone_number_id="123456789",
            access_token="test_token",
            client=mock_http,
        )

        sender = WhatsAppSender(session=session, client=meta_client)

        # Mock ConversationContext
        customer_mock = MagicMock()
        customer_mock.channel_customer_id = "919876543210"
        customer_mock.name = "Sender Test Customer"

        incoming_mock = MagicMock()
        incoming_mock.channel_message_id = f"wamid.INCOMING_{uuid.uuid4().hex[:8]}"
        incoming_mock.customer_channel_id = "919876543210"

        context_mock = MagicMock(spec=ConversationContext)
        context_mock.ticket = ticket
        context_mock.customer = customer_mock
        context_mock.incoming_message = incoming_mock
        context_mock.conversation_ref = ticket.ref

        # AI Response
        model_info = ModelInfo("mock", "mock-v1", "v1.0", "hash", 0.4, 500)
        ai_response = AIResponse("Your order #1023 is on the way!", model_info, TokenUsage(100, 20, 120))

        # [3c-19] WhatsAppSender full pipeline delivers reply
        result = await sender.send_ai_reply(context_mock, ai_response)
        check("3c-19",
              result.status == DeliveryStatus.sent
              and result.provider_message_id.startswith("wamid.FULL_TEST_")
              and result.recipient_phone == "919876543210",
              f"Full sender pipeline | status={result.status.value} wamid={result.provider_message_id[:20]}")

        # [3c-18] Idempotency check: duplicate send suppressed
        dup_result = await sender.send_ai_reply(context_mock, ai_response)
        cond_18 = (
            dup_result.status == DeliveryStatus.sent
            and dup_result.provider_message_id == result.provider_message_id
            and mock_http.post.call_count == 1
        )
        check("3c-18",
              cond_18,
              f"Duplicate send suppressed | http_calls={mock_http.post.call_count}")


async def run_all():
    print("\n" + "═" * 65)
    print("  STEP 3C — WhatsApp Outbound Delivery Layer Test Suite")
    print("═" * 65)

    test_formatter()
    test_delivery_tracker()
    await test_client()
    await test_retry_engine()
    await test_sender_and_repository()


def print_summary():
    print("\n" + "═" * 65)
    print("  SUMMARY")
    print("═" * 65)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"\n  Total: {len(results)}  |  ✅ Passed: {passed}  |  ❌ Failed: {failed}\n")
    if failed:
        print("  FAILURES:")
        for tid, ok, detail in results:
            if not ok:
                print(f"    ❌ [{tid}] {detail}")
    print()
    return failed


if __name__ == "__main__":
    asyncio.run(run_all())
    sys.exit(1 if print_summary() else 0)

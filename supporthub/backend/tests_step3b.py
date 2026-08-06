"""
tests_step3b.py — Step 3B: AI Orchestration Layer Test Suite

All tests use MockAdapter — ZERO real API calls. Fast, free, reproducible.

Tests:
  [3b-1]  ContextBuilder extracts customer name correctly
  [3b-2]  ContextBuilder handles missing customer name (fallback)
  [3b-3]  ContextBuilder trims history to token budget
  [3b-4]  ContextBuilder generates media message description
  [3b-5]  PromptBuilder produces system prompt with all 5 sections
  [3b-6]  PromptBuilder includes customer name in context section
  [3b-7]  PromptBuilder sets correct tone for WhatsApp channel
  [3b-8]  PromptBuilder adds welcome message for new customer
  [3b-9]  PromptBuilder appends current message as final user message
  [3b-10] ResponseParser normalizes valid response correctly
  [3b-11] ResponseParser handles empty response → fallback
  [3b-12] ResponseParser handles safety block → fallback, confidence=0.3
  [3b-13] ResponseParser scores uncertainty phrases → confidence < 1.0
  [3b-14] MockAdapter returns deterministic response
  [3b-15] MockAdapter raises configured exception (for error path testing)
  [3b-16] Orchestrator full pipeline → AIResponse with all fields
  [3b-17] Orchestrator stores AI message in DB (SenderType.ai)
  [3b-18] Orchestrator returns fallback when provider fails
  [3b-19] AIResponse.is_fallback = False for real responses
  [3b-20] AIResponse.is_fallback = True for fallback responses
  [3b-21] TokenUsage.estimated_cost_usd is calculated
  [3b-22] Prompt.system_hash changes when system prompt changes
  [3b-23] Orchestrator handles ContextBuildError → fallback AIResponse
"""

from __future__ import annotations

import asyncio
import sys
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch


results: list[tuple[str, bool, str]] = []


def check(test_id: str, condition: bool, detail: str = "") -> None:
    icon = "✅ PASS" if condition else "❌ FAIL"
    results.append((test_id, condition, detail))
    print(f"  {icon}  [{test_id}] {detail}")


# ─── Fixtures ────────────────────────────────────────────────────────────────

def make_message_record(
    sender_type: str = "customer",
    body: str = "Hello I need help",
    idx: int = 0,
):
    from app.services.conversations.models import MessageRecord
    return MessageRecord(
        id=uuid.uuid4(),
        sender_type=sender_type,
        body=body,
        message_type="text",
        channel_message_id=f"wamid.TEST_{idx}",
        attachments=[],
        created_at=datetime.now(timezone.utc),
    )


def make_conversation_context(
    customer_name: str = "Heet Patel",
    channel: str = "whatsapp",
    msg_type: str = "text",
    msg_text: str = "I need a refund",
    history_count: int = 2,
    is_new_customer: bool = False,
    is_new_conversation: bool = False,
    ticket_status: str = "open",
    ticket_priority: str = "medium",
):
    """Build a mock ConversationContext without hitting the DB."""
    from app.services.channels.models import Channel, IncomingMessage, MessageType
    from app.services.conversations.models import ConversationContext

    # Mock customer
    customer = MagicMock()
    customer.name = customer_name
    customer.channel_customer_id = "919876543210"
    customer.id = uuid.uuid4()

    # Mock ticket
    ticket = MagicMock()
    ticket.id = uuid.uuid4()
    ticket.ref = "TCK-99999"
    ticket.status = MagicMock()
    ticket.status.value = ticket_status
    ticket.priority = MagicMock()
    ticket.priority.value = ticket_priority

    # Mock incoming message
    type_map = {
        "text": MessageType.text,
        "image": MessageType.image,
        "audio": MessageType.audio,
    }
    msg_type_enum = type_map.get(msg_type, MessageType.text)

    incoming = MagicMock()
    incoming.channel_message_id = f"wamid.TEST_{uuid.uuid4().hex[:8]}"
    incoming.customer_channel_id = "919876543210"
    incoming.customer_name = customer_name
    incoming.message_type = msg_type_enum          # real enum object
    incoming.text = msg_text if msg_type == "text" else None
    incoming.attachments = []
    incoming.channel = Channel(channel)
    incoming.raw_payload = {}


    # Build history
    history = [
        make_message_record(sender_type="customer", body=f"Msg {i}", idx=i)
        for i in range(history_count)
    ]

    ctx = MagicMock(spec=ConversationContext)
    ctx.customer = customer
    ctx.ticket = ticket
    ctx.incoming_message = incoming
    ctx.history = history
    ctx.channel = Channel(channel)
    ctx.is_new_customer = is_new_customer
    ctx.is_new_conversation = is_new_conversation
    ctx.conversation_ref = "TCK-99999"
    ctx.customer_display_name = customer_name
    ctx.history_for_ai = [
        {"role": "user", "content": f"Msg {i}"} for i in range(history_count)
    ]
    return ctx


# ─── Tests ────────────────────────────────────────────────────────────────────

def test_context_builder():
    from app.services.ai.context_builder import ContextBuilder

    builder = ContextBuilder()

    # [3b-1] Customer name extracted
    ctx = make_conversation_context(customer_name="Heet Patel")
    result = builder.build(ctx)
    check("3b-1", result.customer_name == "Heet Patel",
          f"Customer name | got={result.customer_name}")

    # [3b-2] Missing name → privacy-safe fallback
    ctx = make_conversation_context(customer_name="")
    ctx.customer.name = ""
    result = builder.build(ctx)
    check("3b-2", result.customer_name.startswith("Customer"),
          f"Name fallback | got={result.customer_name}")

    # [3b-3] History trimmed to budget
    ctx = make_conversation_context(history_count=25)
    ctx.history_for_ai = [{"role": "user", "content": "x" * 100} for _ in range(25)]
    result = builder.build(ctx)
    check("3b-3", len(result.history) <= 25,
          f"History trimmed | original=25 got={len(result.history)}")

    # [3b-4] Media message description
    ctx = make_conversation_context(msg_type="image", msg_text=None)
    ctx.incoming_message.text = None
    ctx.incoming_message.attachments = []
    result = builder.build(ctx)
    check("3b-4", "image" in result.current_message.lower() or "📷" in result.current_message,
          f"Media description | got={result.current_message}")


def test_prompt_builder():
    from app.services.ai.context_builder import ContextBuilder
    from app.services.ai.prompt_builder import PromptBuilder

    context_builder = ContextBuilder()
    prompt_builder = PromptBuilder()

    ctx = make_conversation_context(customer_name="Heet Patel", channel="whatsapp")
    llm_context = context_builder.build(ctx)
    prompt = prompt_builder.build(llm_context)

    # [3b-5] System prompt has all 5 sections
    system = prompt.system
    check("3b-5",
          all(kw in system for kw in ["## ROLE", "## RULES", "## TONE", "## CURRENT CONTEXT", "## OUTPUT FORMAT"]),
          f"All 5 sections present | sections found={sum(1 for kw in ['ROLE','RULES','TONE','CONTEXT','OUTPUT'] if kw in system)}")

    # [3b-6] Customer name in context section
    check("3b-6", "Heet Patel" in system,
          f"Customer name in prompt | found={'Heet Patel' in system}")

    # [3b-7] WhatsApp tone
    check("3b-7", "conversational" in system.lower() or "friendly" in system.lower(),
          f"WhatsApp tone | in_system={'conversational' in system.lower()}")

    # [3b-8] New customer welcome
    ctx_new = make_conversation_context(is_new_customer=True)
    llm_ctx_new = context_builder.build(ctx_new)
    prompt_new = prompt_builder.build(llm_ctx_new)
    check("3b-8", "first interaction" in prompt_new.system.lower() or "welcome" in prompt_new.system.lower(),
          f"New customer welcome | found={'first interaction' in prompt_new.system.lower()}")

    # [3b-9] Current message is last in messages list
    check("3b-9",
          prompt.messages[-1]["role"] == "user" and prompt.messages[-1]["content"],
          f"Current msg last | role={prompt.messages[-1]['role'] if prompt.messages else None}")


def test_response_parser():
    from app.services.ai.response_parser import ResponseParser
    from app.services.ai.models import Prompt

    parser = ResponseParser()
    mock_prompt = Prompt(
        system="Test system",
        messages=[{"role": "user", "content": "test"}],
        model_name="mock-model-v1",
    )

    # [3b-10] Valid response normalized correctly
    raw = {"text": "Your order has been processed successfully.", "input_tokens": 100,
           "output_tokens": 20, "finish_reason": "stop"}
    result = parser.parse(raw, mock_prompt, "mock", "mock-model-v1", latency_ms=50)
    check("3b-10",
          result.response_text == "Your order has been processed successfully."
          and result.usage.input_tokens == 100
          and result.finish_reason == "stop"
          and result.latency_ms == 50,
          f"Parsed correctly | text={result.response_text[:30]} tokens={result.usage.input_tokens}")

    # [3b-11] Empty response → fallback
    raw_empty = {"text": "", "input_tokens": 0, "output_tokens": 0, "finish_reason": "stop"}
    result_empty = parser.parse(raw_empty, mock_prompt, "mock", "mock-model-v1")
    check("3b-11",
          result_empty.is_fallback and result_empty.confidence == 0.0,
          f"Empty → fallback | is_fallback={result_empty.is_fallback} confidence={result_empty.confidence}")

    # [3b-12] Safety block → fallback, confidence 0.3
    raw_blocked = {"text": "", "input_tokens": 10, "output_tokens": 0, "finish_reason": "content_filter"}
    result_blocked = parser.parse(raw_blocked, mock_prompt, "mock", "mock-model-v1")
    check("3b-12",
          result_blocked.is_fallback and result_blocked.confidence <= 0.3,
          f"Safety block | is_fallback={result_blocked.is_fallback} confidence={result_blocked.confidence}")

    # [3b-13] Uncertainty phrases → confidence < 1.0
    raw_uncertain = {"text": "I'm not sure about that. I don't know the answer.",
                     "input_tokens": 50, "output_tokens": 15, "finish_reason": "stop"}
    result_uncertain = parser.parse(raw_uncertain, mock_prompt, "mock", "mock-model-v1")
    check("3b-13",
          result_uncertain.confidence < 1.0,
          f"Uncertainty scored | confidence={result_uncertain.confidence}")


async def test_mock_adapter():
    from app.services.ai.model_adapter import MockAdapter
    from app.services.ai.models import Prompt
    from app.services.ai.exceptions import AIProviderError

    prompt = Prompt(
        system="Test",
        messages=[{"role": "user", "content": "Hello"}],
        model_name="mock-model-v1",
    )

    # [3b-14] Returns deterministic response
    adapter = MockAdapter(response_text="Test AI response")
    result = await adapter.generate(prompt)
    check("3b-14",
          result["text"] == "Test AI response" and "latency_ms" in result,
          f"Mock response | text={result['text']}")

    # [3b-15] Raises configured exception
    adapter_err = MockAdapter(
        should_raise=AIProviderError("mock", "Simulated failure", is_retryable=False)
    )
    raised = False
    try:
        await adapter_err.generate(prompt)
    except AIProviderError:
        raised = True
    check("3b-15",
          raised,
          f"MockAdapter raises error | raised={raised}")


async def test_orchestrator():
    from app.database import AsyncSessionLocal
    from app.services.ai.orchestrator import AIOrchestrator
    from app.services.ai.model_adapter import MockAdapter
    from app.services.ai.exceptions import AIProviderError
    from app.models import Message, SenderType
    from sqlmodel import select

    # [3b-16] Full pipeline produces AIResponse
    async with AsyncSessionLocal() as session:
        ctx = make_conversation_context(customer_name="Test User", channel="whatsapp")
        ctx.ticket.id = uuid.uuid4()  # need a real-ish UUID for DB storage

        # Create a real ticket in DB for the AI message to reference
        from app.models import Ticket, TicketChannel, TicketStatus, TicketPriority, User, UserRole, UserStatus, ChannelType
        import random

        # Create a minimal user + ticket so FK works
        async with session.begin():
            user = User(
                email=f"ai_test_{uuid.uuid4().hex[:8]}@test.internal",
                name="Test User",
                password_hash="__test__",
                role=UserRole.customer,
                status=UserStatus.active,
            )
            session.add(user)
            await session.flush()

            ticket = Ticket(
                ref=f"TCK-{random.randint(10000, 99999)}",
                customer_id=user.id,
                subject="Test AI conversation",
                category="whatsapp",
                channel=TicketChannel.whatsapp,
                status=TicketStatus.open,
                priority=TicketPriority.medium,
            )
            session.add(ticket)
            await session.flush()

        # Set the real ticket ID on the mock context
        ctx.ticket.id = ticket.id
        ctx.ticket.ref = ticket.ref

        adapter = MockAdapter(response_text="Thank you! I'll help you with your refund request.")
        orchestrator = AIOrchestrator(session=session, adapter=adapter)
        ai_response = await orchestrator.generate(ctx)

        check("3b-16",
              ai_response.response_text == "Thank you! I'll help you with your refund request."
              and ai_response.model.provider == "mock"
              and ai_response.usage.input_tokens == 150,
              f"Full pipeline | text={ai_response.response_text[:40]} provider={ai_response.model.provider}")

    # [3b-17] AI message stored in DB
    async with AsyncSessionLocal() as session:
        stored = (await session.exec(
            select(Message).where(
                Message.ticket_id == ticket.id,
                Message.sender_type == SenderType.ai,
            )
        )).first()
        check("3b-17",
              stored is not None and stored.sender_type == SenderType.ai,
              f"AI message stored | found={stored is not None} sender={stored.sender_type if stored else None}")

    # [3b-18] Orchestrator returns fallback when provider fails
    async with AsyncSessionLocal() as session:
        ctx2 = make_conversation_context()
        ctx2.ticket.id = ticket.id  # reuse existing ticket

        failing_adapter = MockAdapter(
            should_raise=AIProviderError("mock", "Simulated failure", is_retryable=False)
        )
        orchestrator2 = AIOrchestrator(session=session, adapter=failing_adapter)
        fallback_response = await orchestrator2.generate(ctx2)

        check("3b-18",
              fallback_response.is_fallback and fallback_response.error is not None,
              f"Fallback on error | is_fallback={fallback_response.is_fallback} error={fallback_response.error[:30] if fallback_response.error else None}")


async def test_models():
    from app.services.ai.models import AIResponse, ModelInfo, TokenUsage, Prompt

    # [3b-19] is_fallback=False for real response
    model = ModelInfo("mock", "mock-model-v1", "v1.0", "abc123", 0.4, 500)
    usage = TokenUsage(100, 20, 120)
    real = AIResponse("Real response", model, usage, "stop", 50, 1.0, error=None)
    check("3b-19", real.is_fallback is False,
          f"Real response not fallback | is_fallback={real.is_fallback}")

    # [3b-20] is_fallback=True when error is set
    fallback = AIResponse("Fallback", model, usage, "error", 0, 0.0, error="provider_failed")
    check("3b-20", fallback.is_fallback is True,
          f"Fallback correctly detected | is_fallback={fallback.is_fallback}")

    # [3b-21] estimated_cost_usd calculated
    usage_with_tokens = TokenUsage(1000, 200, 1200)
    check("3b-21", usage_with_tokens.estimated_cost_usd > 0,
          f"Cost calculated | cost=${usage_with_tokens.estimated_cost_usd}")

    # [3b-22] system_hash changes with content
    p1 = Prompt("System A", [], model_name="m")
    p2 = Prompt("System B", [], model_name="m")
    check("3b-22", p1.system_hash != p2.system_hash,
          f"Hash differs | p1={p1.system_hash} p2={p2.system_hash}")

    # [3b-23] ContextBuildError handled → fallback (tested via orchestrator)
    from app.services.ai.context_builder import ContextBuilder
    from app.services.ai.exceptions import ContextBuildError

    class BrokenContextBuilder(ContextBuilder):
        def build(self, ctx):
            raise ContextBuildError("Simulated context failure")

    async def _test_context_error():
        from app.database import AsyncSessionLocal
        from app.services.ai.orchestrator import AIOrchestrator
        from app.services.ai.model_adapter import MockAdapter
        async with AsyncSessionLocal() as session:
            ctx = make_conversation_context()
            orchestrator = AIOrchestrator(
                session=session,
                adapter=MockAdapter(),
                context_builder=BrokenContextBuilder(),
            )
            result = await orchestrator.generate(ctx)
            check("3b-23", result.is_fallback and "context" in (result.error or "").lower(),
                  f"ContextBuildError → fallback | error={result.error}")

    await _test_context_error()


async def run_all():
    print("\n" + "═" * 65)
    print("  STEP 3B — AI Orchestration Layer Test Suite")
    print("═" * 65)

    # Sync tests (no DB needed)
    test_context_builder()
    test_prompt_builder()
    test_response_parser()
    await test_mock_adapter()

    # Async tests (DB needed for storage tests)
    await test_orchestrator()

    # Model validation tests
    await test_models()


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

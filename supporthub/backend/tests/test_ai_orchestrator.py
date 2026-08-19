"""Unit tests for AI Context Builder, Prompt Builder, Model Adapter, and Orchestrator."""
from __future__ import annotations

import pytest
from app.services.ai.context_builder import ContextBuilder
from app.services.ai.prompt_builder import PromptBuilder
from app.services.ai.response_parser import ResponseParser
from app.services.ai.models import LLMContext, Prompt


def test_llm_prompt_builder_sections():
    prompt_builder = PromptBuilder()

    ctx = LLMContext(
        customer_name="Heet Patel",
        customer_channel_id="919876543210",
        channel="whatsapp",
        conversation_ref="TCK-10001",
        is_new_customer=False,
        is_new_conversation=False,
        ticket_status="open",
        ticket_priority="medium",
        history=[{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}],
        current_message="How can I track my order?",
        current_message_type="text",
        kb_context="Order tracking is available at supporthub.com/track",
        ticket_subject="Order Issue",
        ticket_category="Orders",
    )

    built_prompt = prompt_builder.build(ctx)
    assert built_prompt.system is not None
    assert len(built_prompt.messages) > 0
    assert built_prompt.messages[-1]["role"] == "user"
    assert "How can I track my order?" in built_prompt.messages[-1]["content"]


def test_llm_response_parser_valid_text():
    prompt_builder = PromptBuilder()
    ctx = LLMContext(
        customer_name="Heet Patel",
        customer_channel_id="919876543210",
        channel="whatsapp",
        conversation_ref="TCK-10001",
        is_new_customer=False,
        is_new_conversation=False,
        ticket_status="open",
        ticket_priority="medium",
        history=[],
        current_message="Hello",
        current_message_type="text",
    )
    prompt = prompt_builder.build(ctx)

    parser = ResponseParser()
    raw = {
        "text": "Your order is out for delivery today.",
        "input_tokens": 100,
        "output_tokens": 25,
        "finish_reason": "stop"
    }
    parsed = parser.parse(raw, prompt=prompt, provider="mock", model_name="mock-model", latency_ms=15)
    assert parsed.is_fallback is False
    assert parsed.response_text == "Your order is out for delivery today."
    assert parsed.confidence > 0.8


def test_llm_response_parser_empty_fallback():
    prompt_builder = PromptBuilder()
    ctx = LLMContext(
        customer_name="Heet Patel",
        customer_channel_id="919876543210",
        channel="whatsapp",
        conversation_ref="TCK-10001",
        is_new_customer=False,
        is_new_conversation=False,
        ticket_status="open",
        ticket_priority="medium",
        history=[],
        current_message="Hello",
        current_message_type="text",
    )
    prompt = prompt_builder.build(ctx)

    parser = ResponseParser()
    raw = {
        "text": "",
        "input_tokens": 100,
        "output_tokens": 0,
        "finish_reason": "stop"
    }
    parsed = parser.parse(raw, prompt=prompt, provider="mock", model_name="mock-model", latency_ms=15)
    assert parsed.is_fallback is True
    assert parsed.confidence == 0.0
    assert len(parsed.response_text) > 0  # Fallback text provided

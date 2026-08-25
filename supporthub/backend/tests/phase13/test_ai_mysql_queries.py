"""
Phase 13.2 — AI MySQL Response Grounding & Scenario Validation Test Suite.

Validates end-to-end AI response grounding over real MySQL business data,
multi-order ambiguity handling, guest data protection, and unlinked customer identity rules.
"""

import pytest
from app.ai.orchestrator import AIOrchestrator


def test_ai_grounded_order_query():
    """Verify AI Orchestrator queries MySQL and grounds response with real order data."""
    orchestrator = AIOrchestrator(use_llm=False)
    query = "What is the status of my order ORD-001?"

    response = orchestrator.process_message(
        query=query,
        customer_id="CUST-001",
        conversation_id="conv_order_test_101",
        channel_type="WEBSITE",
    )

    assert response.route_type in ("STRUCTURED", "HYBRID")
    assert response.is_grounded is True
    assert "ORD-001" in response.content
    assert "DELIVERED" in response.content.upper()


def test_multi_order_handling():
    """
    Verify customer with multiple orders (CUST-001 has ORD-025, ORD-001, ORD-002)
    asking 'Where is my order?' without an order ID receives order list or clarification prompt.
    """
    orchestrator = AIOrchestrator(use_llm=False)
    query = "Where is my order?"

    response = orchestrator.process_message(
        query=query,
        customer_id="CUST-001",
        conversation_id="conv_multi_order_102",
        channel_type="WEBSITE",
    )

    assert response.route_type in ("STRUCTURED", "HYBRID")
    # Response should reference active orders or ask for order ID
    content = response.content.upper()
    assert "ORD-" in content or "ORDER ID" in content or "ORDERS" in content


def test_guest_protection_guard():
    """
    Verify Guest customer (unauthenticated / identity = GUEST) querying private order data
    is blocked and prompted to log in.
    """
    orchestrator = AIOrchestrator(use_llm=False)
    query = "What is the status of my order ORD-001?"

    response = orchestrator.process_message(
        query=query,
        customer_id="GUEST",
        conversation_id="conv_guest_test_103",
        channel_type="WEBSITE",
    )

    # Must block access and prompt login
    assert response.route_type == "STRUCTURED"
    assert "log in" in response.content.lower() or "authenticated" in response.content.lower()


def test_unlinked_user_protection():
    """
    Verify user without a linked customer_id (None or empty string)
    querying private transactional data is prompted to log in or link account.
    """
    orchestrator = AIOrchestrator(use_llm=False)
    query = "Can you check my refund status for REF-001?"

    response = orchestrator.process_message(
        query=query,
        customer_id=None,
        conversation_id="conv_unlinked_test_104",
        channel_type="WEBSITE",
    )

    assert response.route_type == "STRUCTURED"
    assert "log in" in response.content.lower() or "authenticated" in response.content.lower()

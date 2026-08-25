"""Phase 13.4 — Multi-Turn Hybrid Context Isolation Test Suite."""
import pytest
from app.ai.orchestrator import AIOrchestrator
from app.ai.context import ConversationContext


@pytest.fixture
def orchestrator():
    return AIOrchestrator(use_llm=False)


def test_multi_turn_product_to_hybrid_cancellation(orchestrator):
    """Product inquiry followed by explicit order cancellation must isolate order context."""
    ctx = ConversationContext(conversation_id="mt01_sess", customer_id="CUST-001")

    # Turn 1: Product inquiry
    resp1 = orchestrator.process_message("Tell me about PROD-002", context_override=ctx, use_llm=False)
    assert resp1.route_type == "STRUCTURED"
    assert ctx.active_product_id == "PROD-002"
    assert ctx.active_order_id is None

    # Turn 2: Hybrid order cancellation query
    resp2 = orchestrator.process_message("Can I cancel ORD-025?", context_override=ctx, use_llm=False)
    assert resp2.route_type == "HYBRID"
    assert ctx.active_order_id == "ORD-025"
    assert ctx.last_product_id == "PROD-002"


def test_multi_turn_order_to_hybrid_return(orchestrator):
    """Order status followed by implicit return inquiry must maintain order context."""
    ctx = ConversationContext(conversation_id="mt02_sess", customer_id="CUST-001")

    # Turn 1: Order status query
    resp1 = orchestrator.process_message("What is the status of ORD-025?", context_override=ctx, use_llm=False)
    assert resp1.route_type == "STRUCTURED"
    assert ctx.active_order_id == "ORD-025"

    # Turn 2: Implicit return inquiry ("Can I return it?")
    resp2 = orchestrator.process_message("Can I return it?", context_override=ctx, use_llm=False)
    assert resp2.route_type == "HYBRID"
    assert ctx.active_order_id == "ORD-025"

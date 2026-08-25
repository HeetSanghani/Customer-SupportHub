"""Phase 13.4 — Hybrid Routing Test Suite (H01-H12)."""
import pytest
from app.ai.router import AIRouter, RouteType
from app.ai.orchestrator import AIOrchestrator
from app.ai.context import ConversationContext


@pytest.fixture
def router():
    return AIRouter(use_llm_intent=False)


@pytest.fixture
def orchestrator():
    return AIOrchestrator(use_llm=False)


def test_h01_can_i_cancel_order(router, orchestrator):
    """H01: Can I cancel ORD-025? -> HYBRID route."""
    query = "Can I cancel ORD-025?"
    ctx = ConversationContext(conversation_id="h01_sess", customer_id="CUST-001")
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.HYBRID
    assert "get_order" in decision.target_tools

    response = orchestrator.process_message(query, context_override=ctx, use_llm=False)
    assert response.route_type == "HYBRID"
    assert "ORD-025" in response.content or "order" in response.content.lower()


def test_h02_can_i_return_order(router, orchestrator):
    """H02: Can I return ORD-025? -> HYBRID route."""
    query = "Can I return ORD-025?"
    ctx = ConversationContext(conversation_id="h02_sess", customer_id="CUST-001")
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.HYBRID

    response = orchestrator.process_message(query, context_override=ctx, use_llm=False)
    assert response.route_type == "HYBRID"


def test_h03_refund_delayed_with_policy(router, orchestrator):
    """H03: Why is my refund delayed and what is the refund policy? -> HYBRID route."""
    query = "Why is my refund delayed and what is the refund policy for ORD-025?"
    ctx = ConversationContext(conversation_id="h03_sess", customer_id="CUST-001")
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.HYBRID

    response = orchestrator.process_message(query, context_override=ctx, use_llm=False)
    assert response.route_type == "HYBRID"


def test_h04_order_status_only(router):
    """H04: What is my order status? -> STRUCTURED route."""
    query = "What is the status of ORD-025?"
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.STRUCTURED


def test_h05_cancellation_policy_only(router):
    """H05: What is the cancellation policy? -> RAG route."""
    query = "What is the cancellation policy?"
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.RAG


def test_h06_product_price_only(router):
    """H06: What is the price of PROD-002? -> STRUCTURED route."""
    query = "What is the price of PROD-002?"
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.STRUCTURED


def test_h07_payment_methods_supported(router):
    """H07: What payment methods do you support? -> RAG route."""
    query = "What payment methods do you support?"
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.RAG


def test_h08_unauthorized_order_hybrid_query(orchestrator):
    """H08: Unauthorized order + policy query -> SECURITY DENIAL."""
    query = "Can I cancel ORD-003?"  # ORD-003 belongs to CUST-002
    ctx = ConversationContext(conversation_id="h08_sess", customer_id="CUST-001")
    response = orchestrator.process_message(query, context_override=ctx, use_llm=False)
    assert response.route_type == "SECURITY"
    assert "Access Denied" in response.content or "denied" in response.content.lower()


def test_h09_hybrid_missing_entity(orchestrator):
    """H09: Hybrid query with missing entity -> safe response asking for order details or policy info."""
    query = "Can I cancel?"  # No order ID provided
    ctx = ConversationContext(conversation_id="h09_sess", customer_id="CUST-001")
    response = orchestrator.process_message(query, context_override=ctx, use_llm=False)
    assert response.route_type in ("HYBRID", "RAG", "STRUCTURED")
    assert len(response.content) > 0


def test_h10_product_context_hybrid_followup(router, orchestrator):
    """H10: Product context follow-up for return policy -> HYBRID route."""
    ctx = ConversationContext(conversation_id="h10_sess", customer_id="CUST-001")
    # Turn 1: Product inquiry
    orchestrator.process_message("Tell me about PROD-002", context_override=ctx, use_llm=False)
    assert ctx.active_product_id == "PROD-002"

    # Turn 2: Hybrid return policy follow-up
    query2 = "What is its return policy?"
    slots = {"product_id": ctx.active_product_id, "order_id": ctx.active_order_id}
    decision2 = router.route(query2, customer_id="CUST-001", context_slots=slots)
    assert decision2.route_type == RouteType.HYBRID


def test_h11_order_context_hybrid_followup(router, orchestrator):
    """H11: Order context follow-up for cancellation -> HYBRID route."""
    ctx = ConversationContext(conversation_id="h11_sess", customer_id="CUST-001")
    orchestrator.process_message("What is the status of ORD-025?", context_override=ctx, use_llm=False)
    assert ctx.active_order_id == "ORD-025"

    query2 = "Can I cancel it?"
    slots = {"order_id": ctx.active_order_id, "product_id": ctx.active_product_id}
    decision2 = router.route(query2, customer_id="CUST-001", context_slots=slots)
    assert decision2.route_type == RouteType.HYBRID


def test_h12_multi_turn_hybrid_domain_isolation(orchestrator):
    """H12: Multi-turn hybrid domain transition from Product to Order."""
    ctx = ConversationContext(conversation_id="h12_sess", customer_id="CUST-001")
    orchestrator.process_message("Tell me about PROD-002", context_override=ctx, use_llm=False)
    assert ctx.active_product_id == "PROD-002"

    resp2 = orchestrator.process_message("Can I cancel ORD-025?", context_override=ctx, use_llm=False)
    assert resp2.route_type == "HYBRID"
    assert ctx.active_order_id == "ORD-025"

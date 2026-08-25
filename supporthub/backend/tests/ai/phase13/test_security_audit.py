"""Phase 13.4 — Security & Zero-Trust Audit Test Suite."""
import pytest
from app.ai.orchestrator import AIOrchestrator
from app.ai.context import ConversationContext


@pytest.fixture
def orchestrator():
    return AIOrchestrator(use_llm=False)


def test_cross_customer_order_cancellation_attempt(orchestrator):
    """Customer 1 attempting to query or cancel Customer 2's order must be DENIED."""
    ctx = ConversationContext(conversation_id="sec01_sess", customer_id="CUST-001")
    response = orchestrator.process_message("Can I cancel ORD-003?", context_override=ctx, use_llm=False)
    assert response.route_type == "SECURITY"
    assert "Access Denied" in response.content or "denied" in response.content.lower()


def test_guest_user_private_data_query_denied(orchestrator):
    """Unauthenticated guest trying to access order ORD-025 must be DENIED."""
    ctx = ConversationContext(conversation_id="sec02_sess", customer_id="GUEST")
    response = orchestrator.process_message("What is the status of ORD-025?", context_override=ctx, use_llm=False)
    assert response.route_type == "STRUCTURED"
    assert "log in" in response.content.lower() or "authenticated" in response.content.lower()

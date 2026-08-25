"""Unit tests for LangGraph AI Orchestrator workflow and parity validation."""
import pytest
from app.ai.orchestrator import AIOrchestrator
from app.ai.response import AIResponse


@pytest.fixture
def orchestrator():
    return AIOrchestrator(use_llm=False)


def test_single_question_order_inquiry(orchestrator):
    """Test single-question message processing through LangGraph."""
    response = orchestrator.process_message(
        query="Where is my order ORD-001?",
        customer_id="CUST-001",
        conversation_id="conv_test_single_order"
    )

    assert isinstance(response, AIResponse)
    assert response.route_type in ("STRUCTURED", "HYBRID", "RAG")
    assert "ORD-001" in response.content or "order" in response.content.lower()


def test_single_question_policy_inquiry(orchestrator):
    """Test single-question RAG policy inquiry."""
    response = orchestrator.process_message(
        query="What is your return policy?",
        customer_id="CUST-001",
        conversation_id="conv_test_single_rag"
    )

    assert isinstance(response, AIResponse)
    assert response.route_type in ("RAG", "HYBRID", "STRUCTURED")
    assert len(response.content) > 0


def test_single_question_escalation(orchestrator):
    """Test escalation path via LangGraph."""
    response = orchestrator.process_message(
        query="I am extremely angry! Connect me to a human manager right now!",
        customer_id="CUST-001",
        conversation_id="conv_test_escalate"
    )

    assert isinstance(response, AIResponse)
    assert response.route_type == "HUMAN"
    assert response.escalation_decision is not None
    assert response.escalation_decision.should_escalate is True


def test_multi_question_decomposition(orchestrator):
    """Test multi-question message splitting and response aggregation."""
    response = orchestrator.process_message(
        query="Where is my order ORD-001? Also, what is your return policy?",
        customer_id="CUST-001",
        conversation_id="conv_test_multi"
    )

    assert isinstance(response, AIResponse)
    assert len(response.content) > 0
    # Should combine order details and return policy info
    assert "ORD-001" in response.content or "order" in response.content.lower()

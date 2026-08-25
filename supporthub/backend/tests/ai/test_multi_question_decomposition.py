"""Permanent regression tests for multi-question query decomposition and response merging."""
import pytest
from app.ai.orchestrator import ai_orchestrator
from app.ai.graph.build import compiled_graph
from app.data_access.loader import data_loader


@pytest.fixture(autouse=True)
def ensure_data_loaded():
    data_loader.load()


def test_single_question_multiple_attributes_does_not_split():
    """a) Single question with multiple attributes -> sub_questions count == 1."""
    query = "Does this laptop have 16GB RAM and a 4-hour battery life?"
    state = {
        "conversation_id": "test_decomp_a",
        "customer_id": None,
        "channel_type": "WEBSITE",
        "raw_query": query,
        "use_llm": False,
    }
    result_state = compiled_graph.invoke(state)
    assert len(result_state["sub_questions"]) == 1
    assert result_state["sub_questions"][0]["text"] == query


def test_two_separate_questions_split_and_merge():
    """b) Two separate questions in one message -> sub_questions count == 2 and merged response addresses both."""
    query = "Where is my order ORD-001, and can I also return a different item from ORD-002?"
    state = {
        "conversation_id": "test_decomp_b",
        "customer_id": "CUST-001",
        "channel_type": "WEBSITE",
        "raw_query": query,
        "use_llm": False,
    }
    result_state = compiled_graph.invoke(state)
    assert len(result_state["sub_questions"]) == 2
    
    final_content = result_state["final_response"].content
    assert "ORD-001" in final_content
    assert "ORD-002" in final_content or "Return Policy" in final_content


def test_three_separate_questions_handled_and_merged():
    """c) Three separate questions in one message -> all 3 handled and merged."""
    query = "Where is my order ORD-001? What is the return policy for electronics? And can I also check my order ORD-002?"
    state = {
        "conversation_id": "test_decomp_c",
        "customer_id": "CUST-001",
        "channel_type": "WEBSITE",
        "raw_query": query,
        "use_llm": False,
    }
    result_state = compiled_graph.invoke(state)
    assert len(result_state["sub_questions"]) == 3

    final_content = result_state["final_response"].content
    assert "ORD-001" in final_content
    assert "ORD-002" in final_content
    assert "Return Policy" in final_content or "7 calendar days" in final_content


def test_mixed_question_and_escalation_trigger():
    """d) Mixed message (question + escalation trigger) -> routes to HUMAN with query context and order entity retained."""
    query = "I need help with my order ORD-001 and I want to speak to a human manager immediately"
    response = ai_orchestrator.process_message(
        query=query,
        customer_id="CUST-001",
        conversation_id="test_decomp_d"
    )
    assert response.route_type == "HUMAN"
    assert response.escalation_decision is not None
    assert response.escalation_decision.should_escalate is True
    assert "I need help with my order ORD-001" in response.escalation_decision.customer_message
    assert response.escalation_decision.customer_id == "CUST-001"
    assert response.escalation_decision.active_order_id == "ORD-001"


def test_mixed_route_types_structured_and_rag():
    """e) Mixed route types (STRUCTURED order lookup + RAG policy query) -> both answered."""
    query = "Where is my order ORD-001, and also what is the return window for electronics?"
    response = ai_orchestrator.process_message(
        query=query,
        customer_id="CUST-001",
        conversation_id="test_decomp_e"
    )
    assert "ORD-001" in response.content
    assert "DELIVERED" in response.content
    assert "Return Policy" in response.content or "7 calendar days" in response.content

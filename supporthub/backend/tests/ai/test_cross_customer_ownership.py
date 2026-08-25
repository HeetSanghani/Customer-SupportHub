"""Permanent regression tests for cross-customer resource ownership isolation."""
import pytest
from app.ai.orchestrator import ai_orchestrator
from app.data_access.loader import data_loader


@pytest.fixture(autouse=True)
def ensure_data_loaded():
    data_loader.load()


def test_cust002_query_order_owned_by_cust001_denied():
    """a) CUST-002 queries an order owned by CUST-001 -> SECURITY denial."""
    response = ai_orchestrator.process_message(
        query="What is the status of order ORD-001?",
        customer_id="CUST-002",
        conversation_id="test_own_a"
    )
    assert response.route_type == "SECURITY"
    assert response.security_decision is not None
    assert response.security_decision.is_allowed is False
    assert "Access Denied" in response.content


def test_cust002_query_return_owned_by_cust013_denied():
    """b) CUST-002 queries a return owned by CUST-013 -> SECURITY denial."""
    response = ai_orchestrator.process_message(
        query="What's the status of return RET-002",
        customer_id="CUST-002",
        conversation_id="test_own_b"
    )
    assert response.route_type == "SECURITY"
    assert response.security_decision is not None
    assert response.security_decision.is_allowed is False
    assert "Access Denied" in response.content


def test_cust002_query_refund_owned_by_cust015_denied():
    """c) CUST-002 queries a refund owned by CUST-015 -> SECURITY denial."""
    response = ai_orchestrator.process_message(
        query="Where is my refund REF-002",
        customer_id="CUST-002",
        conversation_id="test_own_c"
    )
    assert response.route_type == "SECURITY"
    assert response.security_decision is not None
    assert response.security_decision.is_allowed is False
    assert "Access Denied" in response.content


def test_legitimate_owner_queries_succeed():
    """d) Legitimate owners query their own records -> succeeds normally."""
    # CUST-001 queries ORD-001
    resp_order = ai_orchestrator.process_message(
        query="Where is my order ORD-001?",
        customer_id="CUST-001",
        conversation_id="test_own_d1"
    )
    assert resp_order.route_type in ("STRUCTURED", "HYBRID")
    assert "ORD-001" in resp_order.content
    assert "Access Denied" not in resp_order.content

    # CUST-013 queries RET-002
    resp_ret = ai_orchestrator.process_message(
        query="What's the status of return RET-002?",
        customer_id="CUST-013",
        conversation_id="test_own_d2"
    )
    assert resp_ret.route_type in ("STRUCTURED", "HYBRID")
    assert "Access Denied" not in resp_ret.content

    # CUST-015 queries REF-002
    resp_ref = ai_orchestrator.process_message(
        query="Where is my refund REF-002?",
        customer_id="CUST-015",
        conversation_id="test_own_d3"
    )
    assert resp_ref.route_type in ("STRUCTURED", "HYBRID")
    assert "Access Denied" not in resp_ref.content

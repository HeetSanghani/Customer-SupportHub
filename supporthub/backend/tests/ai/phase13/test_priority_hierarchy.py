"""Phase 13.4 — 5-Tier Routing Priority Hierarchy Test Suite."""
import pytest
from app.ai.router import AIRouter, RouteType


@pytest.fixture
def router():
    return AIRouter(use_llm_intent=False)


def test_tier1_security_precedence(router):
    """Tier 1: Security/PII interception overrides all other rules."""
    query = "My password is Password123! Can I cancel ORD-025?"
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.SECURITY


def test_tier2_escalation_precedence(router):
    """Tier 2: Human escalation overrides Hybrid/Structured/RAG."""
    query = "This is ridiculous! Transfer me to a human manager immediately! ORD-025"
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.HUMAN


def test_tier3_hybrid_precedence(router):
    """Tier 3: Hybrid (entity + policy) takes precedence over pure RAG/Structured."""
    query = "Can I cancel ORD-025?"
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.HYBRID


def test_tier4_pure_rag_precedence(router):
    """Tier 4: Pure RAG / Knowledge queries (no entity state)."""
    query = "What is the cancellation policy?"
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.RAG


def test_tier5_structured_precedence(router):
    """Tier 5: Transactional entity query (no policy aspect)."""
    query = "What is the status of ORD-025?"
    decision = router.route(query, customer_id="CUST-001")
    assert decision.route_type == RouteType.STRUCTURED

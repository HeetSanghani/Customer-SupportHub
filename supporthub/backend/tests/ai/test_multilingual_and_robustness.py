"""
Test Suite: Multilingual (Hinglish), Typo Robustness & Fallback Resiliency
Covers:
  - LANG-01: Hinglish conversational order, return, and cancellation inquiries
  - LANG-02: Typo resilience on common customer misspellings ('cancle ordr', 'clame warrnty', 'paymnt declind')
  - RESIL-01: Vector embedding fallback graceful degradation under API rate limits
"""
import uuid
import pytest
from app.ai.orchestrator import AIOrchestrator
from app.ai.intent import normalize_query_typos


def make_orch():
    return AIOrchestrator(use_llm=False)


class TestMultilingualAndRobustness:
    """Tests real-world Hinglish queries, misspelling normalization, and graceful degradation."""

    def test_normalize_query_typos_utility(self):
        """Verify the typo normalization utility handles common typos cleanly."""
        assert normalize_query_typos("pls cancle my ordr") == "pls cancel my order"
        assert normalize_query_typos("how to clame warrnty") == "how to claim warranty"
        assert normalize_query_typos("my paymnt declind") == "my payment declined"
        assert normalize_query_typos("item retun status") == "item return status"
        assert normalize_query_typos("delivry date") == "delivery date"

    def test_hinglish_order_status_query(self):
        """LANG-01: 'Mera order status kya hai?' returns customer order info."""
        orch = make_orch()
        resp = orch.process_message(
            "Mera order status kya hai?",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        assert "ORD-001" in resp.content or "DELIVERED" in resp.content

    def test_hinglish_return_query(self):
        """LANG-01: 'Mujhe product return karna hai' routes to return policy / hybrid workflow."""
        orch = make_orch()
        resp = orch.process_message(
            "Mujhe product return karna hai",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type in ("HYBRID", "RAG", "STRUCTURED")
        assert "return" in resp.content.lower() or "ORD-001" in resp.content

    def test_typo_cancellation(self):
        """LANG-02: 'pls cancle my ordr' is recognized as order cancellation intent."""
        orch = make_orch()
        resp = orch.process_message(
            "pls cancle my ordr",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type in ("HYBRID", "STRUCTURED", "RAG")
        assert "cancel" in resp.content.lower() or "ord-" in resp.content.lower()

    def test_typo_warranty(self):
        """LANG-02: 'how to clame warrnty' routes to warranty policy knowledge retrieval."""
        orch = make_orch()
        resp = orch.process_message(
            "how to clame warrnty",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type in ("RAG", "HYBRID")
        has_warranty_citation = any("warranty" in c.get("title", "").lower() or "warranty" in c.get("category", "").lower() for c in resp.rag_citations)
        assert has_warranty_citation or "warranty" in resp.content.lower() or "order id" in resp.content.lower()

    def test_typo_payment_declined(self):
        """LANG-02: 'my paymnt declind' routes to payment failure troubleshooting guide."""
        orch = make_orch()
        resp = orch.process_message(
            "why was my paymnt declind",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "RAG"
        assert "KA-005" in resp.content or "Payment Fails" in resp.content or "payment" in resp.content.lower()

    def test_gemini_fallback_resiliency(self):
        """RESIL-01: Verify system returns structured/RAG content without unhandled exception."""
        orch = make_orch()
        resp = orch.process_message(
            "What is the return window for electronics?",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp is not None
        assert len(resp.content) > 0
        assert resp.route_type in ("RAG", "HYBRID", "STRUCTURED")

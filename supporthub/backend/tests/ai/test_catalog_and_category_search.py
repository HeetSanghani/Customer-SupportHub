"""
Test Suite: Product Catalog Overview, Category Search, and Payment FAQ Routing
Covers:
  - CATALOG-01: 'Show me all products', 'What products do you have?' -> STRUCTURED with list_all_products
  - CATALOG-02: 'Give me all info of all products' -> Anti-collision guard (does not return orders)
  - SEARCH-01: 'Do you have headphones?', 'Show me laptops' -> Category/name search with normalization
  - SEARCH-02: Stock badges and category resolution
  - PAY-FAQ-01: General payment failure questions ('Why was my payment declined?') -> RAG (KA-005)
  - PAY-PERSONAL-03: Personal transactional payment queries -> STRUCTURED
"""
import uuid
import pytest
from app.ai.orchestrator import AIOrchestrator
from app.ai.tools import ToolRegistry


def make_orch():
    return AIOrchestrator(use_llm=False)


class TestCatalogAndCategorySearch:
    """Test suite for product catalog querying and search capabilities."""

    def test_catalog_overview_show_me_all_products(self):
        """CATALOG-01: 'Show me all products' routes to STRUCTURED and returns grouped catalog."""
        orch = make_orch()
        resp = orch.process_message(
            "Show me all products",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        assert "catalog" in resp.content.lower() or "available" in resp.content.lower()
        # Verify category headers are present
        assert "Mobiles & Tablets" in resp.content or "Electronics" in resp.content or "Audio" in resp.content
        assert "PROD-" in resp.content

    def test_catalog_overview_what_products_do_you_sell(self):
        """CATALOG-01: 'What products do you have in your store?' routes to catalog overview."""
        orch = make_orch()
        resp = orch.process_message(
            "What products do you have in your store?",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        assert "PROD-" in resp.content
        assert "₹" in resp.content

    def test_catalog_anti_order_collision(self):
        """CATALOG-02: 'Give me all info of all products' must NOT return customer orders."""
        orch = make_orch()
        resp = orch.process_message(
            "Give me all info of all products",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        # Must return product info, not order shipment tracking
        assert "Order ORD-001" not in resp.content
        assert "Shipment SHIP-001" not in resp.content
        assert "PROD-" in resp.content

    def test_category_search_headphones(self):
        """SEARCH-01: 'Do you have headphones?' finds headphone products."""
        orch = make_orch()
        resp = orch.process_message(
            "Do you have headphones?",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        assert "SoundWave" in resp.content or "Headphone" in resp.content or "PROD-009" in resp.content
        assert "IN_STOCK" in resp.content

    def test_category_search_laptops(self):
        """SEARCH-01: 'Show me laptops' finds laptop products."""
        orch = make_orch()
        resp = orch.process_message(
            "Show me laptops",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        assert "ZenBook" in resp.content or "Laptop" in resp.content or "PROD-005" in resp.content

    def test_search_punctuation_and_plural_normalization(self):
        """SEARCH-01: Searches with trailing punctuation and plurals work smoothly."""
        orch = make_orch()
        resp = orch.process_message(
            "What kind of tablets do you offer???",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        assert "AeroTab" in resp.content or "PROD-002" in resp.content

    def test_tool_registry_list_all_products(self):
        """Direct verification of ToolRegistry.list_all_products."""
        registry = ToolRegistry()
        products = registry.execute("list_all_products", limit=40)
        assert len(products) > 0
        p = products[0]
        assert "product_id" in p
        assert "name" in p
        assert "price" in p
        assert "category_name" in p

    def test_payment_faq_routing_declined(self):
        """PAY-FAQ-01: 'Why was my payment declined?' routes to RAG with KA-005."""
        orch = make_orch()
        resp = orch.process_message(
            "Why was my payment declined?",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "RAG"
        assert "KA-005" in resp.content or "What to Do When Payment Fails" in resp.content or "payment" in resp.content.lower()

    def test_payment_faq_routing_general_failure(self):
        """PAY-FAQ-01: 'What to do when payment fails?' routes to RAG with KA-005."""
        orch = make_orch()
        resp = orch.process_message(
            "What to do when payment fails?",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "RAG"
        assert "KA-005" in resp.content or "Payment Fails" in resp.content or "reversal" in resp.content.lower() or "bank" in resp.content.lower()

    def test_payment_financial_discrepancy_escalates_to_human(self):
        """PAY-ESC-01: 'Money deducted from bank but payment failed' escalates to HUMAN."""
        orch = make_orch()
        resp = orch.process_message(
            "Money deducted from bank but payment failed",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "HUMAN"
        assert resp.escalation_decision is not None

    def test_personal_payment_preserved_for_order(self):
        """PAY-PERSONAL-03: 'Why did my payment fail?' routes to STRUCTURED."""
        orch = make_orch()
        resp = orch.process_message(
            "Why did my payment fail?",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"

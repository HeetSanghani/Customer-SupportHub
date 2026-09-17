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

    def test_catalog_overview_no_truncation_and_out_of_stock(self):
        """CATALOG-03: 'give me info of your all products!' displays all items without truncation and shows OUT_OF_STOCK for 0-stock items."""
        orch = make_orch()
        resp = orch.process_message(
            "give me info of your all products!",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        # Zero-stock items must show OUT_OF_STOCK, not IN_STOCK (0 in stock)
        assert "IN_STOCK (0 in stock)" not in resp.content
        assert "*OUT_OF_STOCK* (0 in stock)" in resp.content
        # No artificial truncation
        assert "...and" not in resp.content
        assert "more items in" not in resp.content

    def test_category_search_every_products_for_electronics(self):
        """SEARCH-03: 'tell me every products for Electronics' returns Electronics products, not flip-flops."""
        orch = make_orch()
        resp = orch.process_message(
            "tell me every products for Electronics",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        # Must include electronics products
        assert any(k in resp.content for k in ["NovaPhone", "ZenBook", "SoundWave", "BeardMaster", "PROD-001", "PROD-005", "PROD-031"])
        # Must NOT match flip-flop slides or unrelated clothing items via naive 'every' substring match
        assert "CloudSlide" not in resp.content
        assert "PROD-030" not in resp.content
        assert "Flip-Flop" not in resp.content
        # Zero-stock items in category show OUT_OF_STOCK
        assert "IN_STOCK (0 available)" not in resp.content
        if "PROD-003" in resp.content:
            assert "*OUT_OF_STOCK* (0 available)" in resp.content

    def test_category_search_all_products_in_electronics(self):
        """SEARCH-04: 'show me all products in Electronics' routes to category search rather than full store dump."""
        orch = make_orch()
        resp = orch.process_message(
            "show me all products in Electronics",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        assert any(k in resp.content for k in ["NovaPhone", "ZenBook", "SoundWave", "PROD-001"])
        # Should not include footwear or furniture
        assert "PROD-030" not in resp.content
        assert "CloudSlide" not in resp.content

    def test_category_search_gifting_for_men(self):
        """SEARCH-05: 'tell me every products for gifting for men' returns Men's clothing and grooming products."""
        orch = make_orch()
        resp = orch.process_message(
            "tell me every products for gifting for men",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        # Must return Men's clothing and/or BeardMaster Trimmer
        assert any(k in resp.content for k in ["Oxford Shirt", "Denim Jeans", "Crewneck T-Shirt", "Boxer Briefs", "BeardMaster", "PROD-021", "PROD-031"])
        # Must not say 'unable to locate requested record'
        assert "unable to locate" not in resp.content.lower()

    def test_category_search_empty_fallback(self):
        """SEARCH-06: Unmatched product search returns a helpful store message instead of record-not-found error."""
        orch = make_orch()
        resp = orch.process_message(
            "tell me every products for completelyrandomnonexistentxyz",
            customer_id="CUST-001",
            conversation_id=uuid.uuid4().hex
        )
        assert resp.route_type == "STRUCTURED"
        assert "couldn't find any products" in resp.content.lower() or "not find" in resp.content.lower()
        assert "unable to locate the requested record" not in resp.content.lower()

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

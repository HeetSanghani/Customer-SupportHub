"""
Phase 13.2 Remediation Verification Test Suite.
Validates Shipment intent recognition, context slot isolation, MRP data preservation, and security boundary isolation.
"""

import pytest
import pymysql
from app.ai.intent import intent_classifier, IntentCategory
from app.ai.orchestrator import AIOrchestrator
from app.ai.context import context_manager
from app.data_access.product_service import ProductService
product_service = ProductService()


def test_shipment_intent_phrasing():
    """Verify natural customer shipment queries are classified as SHIPMENT_INQUIRY."""
    phrases = [
        "Where is my shipment?",
        "Where is my package?",
        "Where is my delivery?",
        "Track my shipment",
        "Track my package",
        "What's happening with my shipment?",
        "When will my shipment arrive?",
        "where is my order ord-013",
        "courier tracking number TRK-DELHIVERY-764130526"
    ]
    for q in phrases:
        res = intent_classifier.classify(q)
        assert res.category == IntentCategory.SHIPMENTS, f"Query '{q}' should be classified as SHIPMENTS, got {res.category}"
        assert res.intent_name == "SHIPMENT_INQUIRY"


def test_context_slot_isolation():
    """Verify active product context does not hijack unrelated shipment queries."""
    conv_id = "test_conv_context_iso_1"
    orchestrator = AIOrchestrator(use_llm=False)
    cust_id = "CUST-001"

    # Turn 1: Product query sets active_product_id in context
    resp1 = orchestrator.process_message("Is PROD-001 available?", customer_id=cust_id, conversation_id=conv_id)
    assert resp1.route_type == "STRUCTURED"
    assert "NovaPhone" in resp1.content

    ctx = context_manager.get_or_create(conv_id)
    assert ctx.active_product_id == "PROD-001"

    # Turn 2: Unrelated shipment query
    resp2 = orchestrator.process_message("Where is my shipment?", customer_id=cust_id, conversation_id=conv_id)
    assert resp2.route_type == "STRUCTURED"
    assert "Shipment" in resp2.content
    assert "NovaPhone" not in resp2.content


def test_legitimate_context_inheritance():
    """Verify legitimate contextual queries (e.g. 'What is its price?') inherit active product context."""
    conv_id = "test_conv_context_inh_1"
    orchestrator = AIOrchestrator(use_llm=False)
    cust_id = "CUST-001"

    # Turn 1: Product query
    orchestrator.process_message("Tell me about PROD-001.", customer_id=cust_id, conversation_id=conv_id)
    
    # Turn 2: Contextual price query
    resp2 = orchestrator.process_message("What is its price?", customer_id=cust_id, conversation_id=conv_id)
    assert resp2.route_type == "STRUCTURED"
    assert "46,999" in resp2.content
    assert "54,999" in resp2.content


def test_mysql_mrp_database_verification():
    """Verify MySQL database contains non-zero MRP values matching source JSON dataset."""
    p1 = product_service.get_product("PROD-001")
    assert p1 is not None
    assert float(p1.price) == 46999.00
    assert float(p1.mrp) == 54999.00
    assert p1.stock_quantity == 45
    assert p1.availability_status == "IN_STOCK"

    p2 = product_service.get_product("PROD-002")
    assert p2 is not None
    assert float(p2.price) == 27499.00
    assert float(p2.mrp) == 32999.00
    assert p2.stock_quantity == 4
    assert p2.availability_status == "IN_STOCK"


def test_mrp_end_to_end_response_and_discount():
    """Verify AI responses include correct MRP formatting and discount percentage."""
    orchestrator = AIOrchestrator(use_llm=False)

    resp1 = orchestrator.process_message("Is PROD-001 available?")
    assert "54,999.00" in resp1.content
    assert "14.5%" in resp1.content or "14.55%" in resp1.content

    resp2 = orchestrator.process_message("What is the price of PROD-002?")
    assert "32,999.00" in resp2.content
    assert "16.7%" in resp2.content or "16.67%" in resp2.content


def test_shipment_by_tracking_and_order():
    """Verify explicit tracking and order shipment queries return correct details."""
    orchestrator = AIOrchestrator(use_llm=False)

    # Tracking query
    resp1 = orchestrator.process_message("Where is shipment TRK-XPRESSBEES-819595113?", customer_id="CUST-001")
    assert "XpressBees" in resp1.content
    assert "SHIP-025" in resp1.content

    # Specific order query
    resp2 = orchestrator.process_message("What is the status of shipment for ORD-001?", customer_id="CUST-001")
    assert "Delhivery" in resp2.content or "SHIP-001" in resp2.content


def test_security_isolation_maintained():
    """Verify cross-customer data authorization and anti-IDOR protection remain intact."""
    orchestrator = AIOrchestrator(use_llm=False)

    # Customer A (CUST-001) attempting to access Customer B (CUST-002) order ORD-003
    resp = orchestrator.process_message("What is the status of ORD-003?", customer_id="CUST-001")
    assert "access denied" in resp.content.lower() or "not authorized" in resp.content.lower() or "unable to locate" in resp.content.lower()

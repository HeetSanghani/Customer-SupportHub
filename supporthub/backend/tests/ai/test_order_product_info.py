"""Unit tests for AI Order Product Info synthesis logic."""
import pytest
from app.ai.response import ResponseSynthesizer
from app.ai.orchestrator import ai_orchestrator


class TestOrderProductInfo:
    @pytest.fixture
    def synthesizer(self):
        return ResponseSynthesizer()

    def test_product_info_query_returns_itemized_breakdown(self, synthesizer):
        data = {
            "order": {
                "order_id": "ORD-009",
                "status": "DELIVERED",
                "total_amount": 2598.0
            },
            "shipment": {
                "shipment_id": "SHIP-009",
                "order_id": "ORD-009",
                "carrier": "Shadowfax",
                "status": "DELIVERED"
            },
            "order_items": [
                {
                    "order_item_id": "ITEM-010",
                    "product_id": "PROD-021",
                    "product_name": "Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)",
                    "quantity": 2,
                    "unit_price": 1299.0,
                    "total_price": 2598.0
                }
            ]
        }
        query = "give me the product info. of ORD-009"
        res = synthesizer.synthesize_structured_response("ORDERS", data, query)

        assert res.is_grounded is True
        assert "Classic Fit 100% Pure Cotton Oxford Shirt" in res.content
        assert "PROD-021" in res.content
        assert "Qty: 2" in res.content
        assert "₹1,299.00" in res.content
        assert "₹2,598.00" in res.content

    def test_orchestrator_end_to_end_product_info(self):
        response = ai_orchestrator.process_message(
            "give me the product info. of ORD-009",
            customer_id="CUST-008"
        )
        assert "Classic Fit 100% Pure Cotton Oxford Shirt" in response.content
        assert "PROD-021" in response.content
        assert "Qty: 2" in response.content

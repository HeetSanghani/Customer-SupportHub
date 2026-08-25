"""Tests for LLM tool invocation and structured schema generation."""
import unittest
from app.ai.tools import tool_registry
from app.ai.intent import llm_intent_classifier, IntentCategory


class TestToolsAndLLM(unittest.TestCase):
    """Test suite for tool integration and intent entity slot filling."""

    def test_tool_registry_executions(self):
        """Verify registered tools return valid structured domain dictionaries."""
        order = tool_registry.get_order("ORD-001")
        self.assertIsNotNone(order)
        self.assertEqual(order["order_id"], "ORD-001")

        shipment = tool_registry.get_shipment_by_order("ORD-001")
        self.assertIsNotNone(shipment)
        self.assertIn("tracking_number", shipment)

        product = tool_registry.get_product("PROD-001")
        self.assertIsNotNone(product)
        self.assertEqual(product["product_id"], "PROD-001")

    def test_intent_entity_extraction_regex_guard(self):
        """Verify regex entities are preserved in intent classification."""
        query = "What is the status of my order ORD-015 and return RET-003?"
        result = llm_intent_classifier.classify(query, use_llm=False)
        self.assertEqual(result.entities.get("order_id"), "ORD-015")
        self.assertEqual(result.entities.get("return_id"), "RET-003")


if __name__ == "__main__":
    unittest.main()

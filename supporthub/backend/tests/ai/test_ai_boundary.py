"""Unit tests validating AI Orchestrator boundary execution through integration contracts."""
import unittest

from app.integration.adapters.mock_supporthub import MockSupportHubSystem


class TestAIBoundary(unittest.TestCase):
    def setUp(self):
        self.hub = MockSupportHubSystem(tenant_id="shopkart")

    def test_structured_query_boundary(self):
        result = self.hub.receive_channel_message(
            channel="website",
            sender_id="CUST-001",
            text="Can you check status of order ORD-001?",
        )
        self.assertEqual(result.route, "STRUCTURED")
        self.assertTrue(result.is_grounded)
        self.assertIn("ORD-001", result.response_text)

    def test_rag_query_boundary(self):
        result = self.hub.receive_channel_message(
            channel="whatsapp",
            sender_id="CUST-002",
            text="What is your return policy window?",
        )
        self.assertIn(result.route, ["RAG", "HYBRID"])
        self.assertTrue(len(result.citations) > 0)
        self.assertIn("return", result.response_text.lower())

    def test_security_violation_boundary(self):
        # Customer 2 attempting to view Customer 1's order
        result = self.hub.receive_channel_message(
            channel="instagram",
            sender_id="CUST-002",
            text="Please give me details on ORD-001",  # Belongs to CUST-001
        )
        self.assertEqual(result.route, "SECURITY")
        self.assertIn("Access Denied", result.response_text)


if __name__ == "__main__":
    unittest.main()

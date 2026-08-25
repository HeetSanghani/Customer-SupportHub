"""Unit tests for MockSupportHubSystem simulation adapter."""
import unittest

from app.integration.adapters.mock_supporthub import MockSupportHubSystem
from app.integration.security import TenantIsolationViolationError


class TestMockSupportHubSystem(unittest.TestCase):
    def setUp(self):
        self.hub = MockSupportHubSystem(tenant_id="shopkart")

    def test_receive_inbound_message_creates_ticket_and_replies(self):
        result = self.hub.receive_channel_message(
            channel="whatsapp",
            sender_id="CUST-001",
            text="Where is my order ORD-001?",
            tenant_id="shopkart",
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.customer_id, "CUST-001")
        self.assertEqual(result.route, "STRUCTURED")
        self.assertTrue(result.is_grounded)
        self.assertIn("ORD-001", result.response_text)

        # Check that a ticket and conversation session were created
        self.assertEqual(len(self.hub.conversations), 1)
        self.assertEqual(len(self.hub.tickets), 1)
        self.assertEqual(len(self.hub.outbound_messages), 1)

    def test_multi_turn_conversation_in_same_session(self):
        conv_id = "test_conv_123"
        # Turn 1
        res1 = self.hub.receive_channel_message(
            channel="website",
            sender_id="CUST-001",
            text="Hello!",
            conversation_id=conv_id,
        )
        self.assertIsNotNone(res1)

        # Turn 2
        res2 = self.hub.receive_channel_message(
            channel="website",
            sender_id="CUST-001",
            text="Where is my order ORD-001?",
            conversation_id=conv_id,
        )
        self.assertEqual(res2.route, "STRUCTURED")
        session = self.hub.conversations[conv_id]
        # Should have 4 turns total (2 customer, 2 ai)
        self.assertEqual(len(session.history), 4)

    def test_cross_tenant_message_blocked(self):
        with self.assertRaises(TenantIsolationViolationError):
            self.hub.receive_channel_message(
                channel="instagram",
                sender_id="CUST-001",
                text="Hello",
                tenant_id="unauthorized_tenant",
            )


if __name__ == "__main__":
    unittest.main()

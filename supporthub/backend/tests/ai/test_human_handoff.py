"""Unit tests validating human escalation, ticket state transition, and AI lockout."""
import unittest

from app.integration.adapters.mock_supporthub import MockSupportHubSystem


class TestHumanHandoff(unittest.TestCase):
    def setUp(self):
        self.hub = MockSupportHubSystem(tenant_id="shopkart")

    def test_escalation_triggers_ticket_state_and_payload(self):
        conv_id = "escalation_conv_1"
        res = self.hub.receive_channel_message(
            channel="whatsapp",
            sender_id="CUST-001",
            text="I want to speak with a human agent or manager immediately!",
            conversation_id=conv_id,
        )
        self.assertEqual(res.route, "HUMAN")
        self.assertTrue(res.escalation.required)
        self.assertIsNotNone(res.escalation.reason)

        session = self.hub.conversations[conv_id]
        self.assertTrue(session.is_escalated)

        ticket = self.hub.tickets[session.ticket_ref]
        self.assertEqual(ticket.status, "escalated")
        self.assertTrue(len(self.hub.escalation_handoffs) > 0)

        # Subsequent messages in this escalated session should be held for human agent
        res_followup = self.hub.receive_channel_message(
            channel="whatsapp",
            sender_id="CUST-001",
            text="Are you still there?",
            conversation_id=conv_id,
        )
        self.assertEqual(res_followup.route, "HUMAN")
        self.assertIn("human support agent", res_followup.response_text)


if __name__ == "__main__":
    unittest.main()

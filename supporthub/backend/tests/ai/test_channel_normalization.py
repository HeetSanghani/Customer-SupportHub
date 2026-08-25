"""Unit tests validating omnichannel normalization across WhatsApp, Instagram, Facebook, Email, and Website."""
import unittest

from app.integration.adapters.mock_supporthub import MockSupportHubSystem


class TestChannelNormalization(unittest.TestCase):
    def setUp(self):
        self.hub = MockSupportHubSystem(tenant_id="shopkart")

    def test_all_channels_produce_identical_factual_responses(self):
        channels = ["website", "whatsapp", "instagram", "facebook", "email"]
        query = "Where is my order ORD-001?"
        responses = []

        for ch in channels:
            res = self.hub.receive_channel_message(
                channel=ch,
                sender_id="CUST-001",
                text=query,
            )
            self.assertEqual(res.route, "STRUCTURED")
            self.assertTrue(res.is_grounded)
            responses.append(res.response_text)

        # All 5 channels should receive the exact same core tracking information
        first_resp = responses[0]
        for resp in responses[1:]:
            self.assertEqual(resp, first_resp)


if __name__ == "__main__":
    unittest.main()

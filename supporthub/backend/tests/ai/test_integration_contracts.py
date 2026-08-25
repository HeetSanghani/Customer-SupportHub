"""Unit tests for Phase 10 integration contracts."""
import unittest
from datetime import datetime, timezone

from app.integration.contracts import (
    CustomerIdentity,
    AuthContext,
    ConversationSession,
    NormalizedInboundMessage,
    ChannelType,
    SenderType,
    TicketRecord,
    TicketHandoffPayload,
    RAGQueryRequest,
    RAGCitation,
    NormalizedAIResult,
    EscalationDetail,
)


class TestIntegrationContracts(unittest.TestCase):
    def test_customer_identity_serialization(self):
        auth = AuthContext(is_authenticated=True, auth_method="jwt", token_verified=True)
        customer = CustomerIdentity(
            customer_id="CUST-001",
            tenant_id="shopkart",
            full_name="Aarav Sharma",
            email="aarav.sharma@example.com",
            phone="+919876543210",
            auth_context=auth,
        )
        data = customer.to_dict()
        self.assertEqual(data["customer_id"], "CUST-001")
        self.assertEqual(data["tenant_id"], "shopkart")
        self.assertTrue(data["is_authenticated"])

    def test_normalized_inbound_message(self):
        msg = NormalizedInboundMessage(
            message_id="msg_001",
            conversation_id="conv_001",
            customer_id="CUST-001",
            tenant_id="shopkart",
            channel=ChannelType.WHATSAPP,
            text="Where is my order?",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        data = msg.to_dict()
        self.assertEqual(data["channel"], "whatsapp")
        self.assertEqual(data["sender_type"], "customer")
        self.assertEqual(data["text"], "Where is my order?")

    def test_conversation_session_turn_management(self):
        session = ConversationSession(
            conversation_id="conv_001",
            tenant_id="shopkart",
            customer_id="CUST-001",
            channel="website",
            ticket_ref="TCK-10001",
        )
        session.add_turn("customer", "Hello", "2026-08-19T10:00:00Z")
        session.add_turn("ai", "Hello Aarav, how can I help you today?", "2026-08-19T10:00:02Z")
        self.assertEqual(len(session.history), 2)
        self.assertEqual(session.history[0].sender_type, "customer")
        self.assertEqual(session.history[1].sender_type, "ai")

    def test_normalized_ai_result_serialization(self):
        res = NormalizedAIResult(
            conversation_id="conv_001",
            customer_id="CUST-001",
            tenant_id="shopkart",
            intent="track_order",
            route="STRUCTURED",
            response_text="Your order ORD-2024-1001 is IN_TRANSIT.",
            is_grounded=True,
            citations=[
                RAGCitation(
                    source_id="POL-SHIPPING-01",
                    tenant_id="shopkart",
                    title="Shipping Policy",
                    category="policy",
                    chunk_index=0,
                    score=0.85,
                    snippet="Orders ship within 24 hours.",
                )
            ],
            confidence=0.98,
        )
        data = res.to_dict()
        self.assertEqual(data["intent"], "track_order")
        self.assertEqual(data["route"], "STRUCTURED")
        self.assertTrue(data["is_grounded"])
        self.assertEqual(len(data["citations"]), 1)


if __name__ == "__main__":
    unittest.main()

"""
Test Suite: Multi-Turn Conversation & Session State Edge Cases
Covers:
  - CONV-01: Context switching from Order to Product without context poisoning
  - CONV-02: Pronoun resolution ('When will it arrive?') mapped to active entity
  - CONV-03: Concurrent conversation context isolation across multiple tickets
  - CONV-04: Follow-up handling after conversation state resolution
"""
import uuid
import pytest
from app.ai.orchestrator import AIOrchestrator
from app.ai.context import context_manager


def make_orch():
    return AIOrchestrator(use_llm=False)


class TestConversationSessionState:
    """Tests multi-turn context slot tracking, switching, and isolation."""

    def test_context_switching_order_to_product(self):
        """CONV-01: Asking about an order, then asking about a product clears/switches context cleanly."""
        orch = make_orch()
        cid = uuid.uuid4().hex
        cust = "CUST-001"

        # Turn 1: Ask about order
        resp1 = orch.process_message("Where is my order ORD-001?", customer_id=cust, conversation_id=cid)
        assert resp1.route_type in ("STRUCTURED", "HYBRID")
        assert "ORD-001" in resp1.content

        # Turn 2: Switch to product query
        resp2 = orch.process_message("Tell me about the ZenBook laptop", customer_id=cust, conversation_id=cid)
        assert resp2.route_type == "STRUCTURED"
        assert "ZenBook" in resp2.content or "PROD-005" in resp2.content
        # Ensure order info does not hijack product response
        assert "Order ORD-001 status" not in resp2.content

    def test_pronoun_resolution_followup(self):
        """CONV-02: Pronoun 'it' resolves to active order shipment status."""
        orch = make_orch()
        cid = uuid.uuid4().hex
        cust = "CUST-001"

        # Turn 1: Discuss order
        resp1 = orch.process_message("Tell me about ORD-001", customer_id=cust, conversation_id=cid)
        assert resp1.route_type in ("STRUCTURED", "HYBRID")

        # Turn 2: Follow up with pronoun 'it'
        resp2 = orch.process_message("When will it arrive?", customer_id=cust, conversation_id=cid)
        assert resp2.route_type in ("STRUCTURED", "HYBRID")
        assert "DELIVERED" in resp2.content or "Delhivery" in resp2.content or "2026" in resp2.content

    def test_concurrent_ticket_context_isolation(self):
        """CONV-03: Two simultaneous tickets for same customer do not leak context."""
        orch = make_orch()
        cust = "CUST-001"
        conv_order_ticket = f"conv_order_{uuid.uuid4().hex[:6]}"
        conv_account_ticket = f"conv_account_{uuid.uuid4().hex[:6]}"

        # Ticket A talks about ORD-001
        orch.process_message("Where is my order ORD-001?", customer_id=cust, conversation_id=conv_order_ticket)

        # Ticket B talks about password
        resp_b = orch.process_message("How do I reset my password?", customer_id=cust, conversation_id=conv_account_ticket)
        assert resp_b.route_type in ("RAG", "ACCOUNT", "HYBRID")
        # Ticket B must not contain order ORD-001 tracking
        assert "ORD-001" not in resp_b.content

        # Verify context manager slot isolation
        ctx_a = context_manager.get_or_create(conv_order_ticket)
        ctx_b = context_manager.get_or_create(conv_account_ticket)
        assert ctx_a.active_order_id == "ORD-001"
        assert ctx_b.active_order_id is None

    def test_context_clear_on_explicit_new_entity(self):
        """CONV-04: Explicitly mentioning a different order switches active context slot."""
        orch = make_orch()
        cid = uuid.uuid4().hex
        cust = "CUST-001"

        # Turn 1: ORD-001
        orch.process_message("Check ORD-001", customer_id=cust, conversation_id=cid)
        ctx = context_manager.get_or_create(cid)
        assert ctx.active_order_id == "ORD-001"

        # Turn 2: Mention ORD-002
        resp = orch.process_message("Now check ORD-002", customer_id=cust, conversation_id=cid)
        assert "ORD-002" in resp.content
        assert ctx.active_order_id == "ORD-002"

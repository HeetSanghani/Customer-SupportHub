"""Unit tests for AI Routing and Orchestration Engine."""
import unittest
from app.ai.router import ai_router, RouteType
from app.ai.orchestrator import ai_orchestrator
from app.ai.context import context_manager


class TestAIRouterAndOrchestrator(unittest.TestCase):
    """Test routing decisions and multi-turn message processing."""

    @classmethod
    def setUpClass(cls):
        context_manager.clear_all()

    def test_structured_order_routing(self):
        decision = ai_router.route("What is the status of my order ORD-001?")
        self.assertEqual(decision.route_type, RouteType.STRUCTURED)
        self.assertIn("get_order", decision.target_tools)

    def test_pure_rag_policy_routing(self):
        decision = ai_router.route("What is the return policy of ShopKart for electronics?")
        self.assertEqual(decision.route_type, RouteType.RAG)
        self.assertIsNotNone(decision.rag_query)

    def test_hybrid_routing(self):
        decision = ai_router.route("Does the ZenBook Ultra 14 Laptop come with warranty?")
        self.assertEqual(decision.route_type, RouteType.HYBRID)
        self.assertIn("get_product", decision.target_tools)
        self.assertIsNotNone(decision.rag_query)

    def test_security_interception_routing(self):
        decision = ai_router.route("My OTP is 482910")
        self.assertEqual(decision.route_type, RouteType.SECURITY)

    def test_human_escalation_routing(self):
        decision = ai_router.route("Transfer me to a live human representative.")
        self.assertEqual(decision.route_type, RouteType.HUMAN)

    def test_orchestrator_multi_turn(self):
        conv_id = "test_multi_turn_01"
        
        # Turn 1 (ORD-013 is owned by CUST-012)
        resp1 = ai_orchestrator.process_message(
            query="Where is my order ORD-013 right now?",
            customer_id="CUST-012",
            conversation_id=conv_id
        )
        self.assertEqual(resp1.route_type, "STRUCTURED")
        self.assertTrue(resp1.is_grounded)

        # Turn 2 (Anaphora reference to ORD-013)
        resp2 = ai_orchestrator.process_message(
            query="And what is the carrier tracking number for it?",
            customer_id="CUST-012",
            conversation_id=conv_id
        )
        self.assertEqual(resp2.route_type, "STRUCTURED")
        self.assertTrue(resp2.is_grounded)
        self.assertIn("ORD-013", resp2.content)


if __name__ == "__main__":
    unittest.main()

"""Unit tests for Human Escalation Evaluator."""
import unittest
from app.ai.escalation import escalation_evaluator


class TestEscalationEvaluator(unittest.TestCase):
    """Test explicit, sentimental, and operational escalation pathways."""

    def test_standard_query_no_escalation(self):
        dec = escalation_evaluator.evaluate("What is the status of my order ORD-001?")
        self.assertFalse(dec.should_escalate)
        self.assertEqual(dec.reason, "NONE")

    def test_explicit_human_agent_request(self):
        dec = escalation_evaluator.evaluate("I want to speak with a human support agent immediately.")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "EXPLICIT_HUMAN_REQUEST")
        self.assertEqual(dec.priority, "HIGH")

    def test_supervisor_escalation(self):
        dec = escalation_evaluator.evaluate("Connect me to your manager or supervisor right now.")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "SUPERVISOR_REQUEST")
        self.assertEqual(dec.priority, "URGENT")

    def test_angry_sentiment_and_legal_threat(self):
        dec = escalation_evaluator.evaluate("This is the worst customer service ever! I will take legal action!")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "ANGRY_SENTIMENT")

    def test_repeated_contact(self):
        dec = escalation_evaluator.evaluate("This is the 4th time I am contacting you about my delayed order!")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "REPEATED_UNRESOLVED")

    def test_deadlock_condition(self):
        dec = escalation_evaluator.evaluate("Nobody is helping me with my issue!")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "DEADLOCK")

    def test_operational_triggers(self):
        # Delivered but not received
        dec_del = escalation_evaluator.evaluate("My order ORD-009 says delivered, but I never received it!")
        self.assertTrue(dec_del.should_escalate)
        self.assertIn("DELIVERED_NOT_RECEIVED", dec_del.reason)

        # Charged twice
        dec_charge = escalation_evaluator.evaluate("I was charged twice for my order ORD-010.")
        self.assertTrue(dec_charge.should_escalate)
        self.assertEqual(dec_charge.priority, "URGENT")

        # Lost in transit
        dec_lost = escalation_evaluator.evaluate("Tracking for ORD-006 has not updated in a week. Is it lost?")
        self.assertTrue(dec_lost.should_escalate)
        self.assertIn("LOST_SHIPMENT", dec_lost.reason)

        # Compromised account
        dec_sec = escalation_evaluator.evaluate("Someone logged into my account from another city and placed an order!")
        self.assertTrue(dec_sec.should_escalate)
        self.assertEqual(dec_sec.priority, "CRITICAL")

    def test_explicit_human_agent_typo_humen(self):
        """Verify that typo 'humen' properly triggers human agent escalation."""
        dec = escalation_evaluator.evaluate("i want to talk with humen agent!")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "EXPLICIT_HUMAN_REQUEST")
        self.assertEqual(dec.priority, "HIGH")

    def test_explicit_human_customer_agent(self):
        """Verify that 'human customer agent' triggers human escalation."""
        dec = escalation_evaluator.evaluate("i want to talk with human customer agent")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "EXPLICIT_HUMAN_REQUEST")

    def test_transfer_to_human_customer_agent(self):
        """Verify phrase 'transfer your request to our human customer agent' escalates."""
        dec = escalation_evaluator.evaluate("transfer your request to our human customer agent")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "EXPLICIT_HUMAN_REQUEST")

    def test_can_i_speak_with_a_human(self):
        dec = escalation_evaluator.evaluate("Can I please speak with a human right now?")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "EXPLICIT_HUMAN_REQUEST")

    def test_talk_with_agent(self):
        dec = escalation_evaluator.evaluate("I need to talk with an agent")
        self.assertTrue(dec.should_escalate)
        self.assertEqual(dec.reason, "EXPLICIT_HUMAN_REQUEST")

    def test_router_routes_humen_to_human_pipeline(self):
        from app.ai.router import ai_router, RouteType
        route = ai_router.route("i want to talk with humen agent!")
        self.assertEqual(route.route_type, RouteType.HUMAN)
        self.assertTrue(route.escalation_decision.should_escalate)

    def test_ticket_subject_for_human_escalation(self):
        from app.ai.subject import format_subject_from_query
        subj = format_subject_from_query("i want to talk with humen agent!")
        self.assertEqual(subj, "Human Agent Support Request")
        subj2 = format_subject_from_query("i want to talk with human customer agent")
        self.assertEqual(subj2, "Human Agent Support Request")


if __name__ == "__main__":
    unittest.main()


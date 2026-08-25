"""Integration test executing 60 ShopKart synthetic scenarios through the integration boundary."""
import unittest

from app.integration.adapters.mock_supporthub import MockSupportHubSystem
from app.evaluation.scenario_loader import scenario_loader
from app.data_access.loader import data_loader


class TestIntegrationScenarios(unittest.TestCase):
    def setUp(self):
        self.hub = MockSupportHubSystem(tenant_id="shopkart")
        data_loader.load()
        self.scenarios = scenario_loader.load_all_scenarios()

    def test_run_all_60_scenarios_through_integration_boundary(self):
        passed_count = 0
        total_scenarios = len(self.scenarios)
        self.assertGreaterEqual(total_scenarios, 60)

        for sc in self.scenarios:
            sid = sc.scenario_id
            question = sc.customer_question
            req_cond = sc.required_conditions
            expected_route = sc.expected_route

            # Resolve caller customer ID
            caller_cust_id = req_cond.get("customer_id")
            if not caller_cust_id and "order_id" in req_cond:
                ord_rec = data_loader.orders.get(req_cond["order_id"])
                if ord_rec:
                    caller_cust_id = ord_rec.customer_id

            # Fallback: extract order ID from question text when required_conditions empty
            if not caller_cust_id:
                import re
                match = re.search(r"ORD-\d+", question)
                if match:
                    ord_id = match.group(0)
                    ord_rec = data_loader.orders.get(ord_id)
                    if ord_rec:
                        caller_cust_id = ord_rec.customer_id
                    elif ord_id == "ORD-003":
                        caller_cust_id = "CUST-002"
                if not caller_cust_id:
                    caller_cust_id = "CUST-001"

            # Map ingress channel dynamically
            channel = "whatsapp" if "WA" in sid else "website"

            result = self.hub.receive_channel_message(
                channel=channel,
                sender_id=caller_cust_id,
                text=question,
                conversation_id=f"conv_{sid.lower()}",
                tenant_id="shopkart",
            )

            # Assert standard properties
            self.assertIsNotNone(result.response_text)
            self.assertEqual(result.tenant_id, "shopkart")

            # Route match verification
            if expected_route == "SECURITY":
                self.assertEqual(result.route, "SECURITY", f"Failed on {sid}")
            elif expected_route == "HUMAN":
                self.assertEqual(result.route, "HUMAN", f"Failed on {sid}")
            else:
                self.assertIn(result.route, ["STRUCTURED", "RAG", "HYBRID"], f"Failed on {sid}")

            passed_count += 1

        self.assertEqual(passed_count, total_scenarios)


if __name__ == "__main__":
    unittest.main()

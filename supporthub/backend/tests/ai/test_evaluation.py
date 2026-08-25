"""Unit tests for the evaluation framework components."""
import unittest
from app.evaluation.scenario_loader import scenario_loader, BenchmarkScenario
from app.evaluation.assertions import assertions
from app.evaluation.metrics import metrics_calculator, EvaluationMetrics
from app.ai.response import AIResponse


class TestEvaluationFramework(unittest.TestCase):
    """Test suite validating evaluation framework correctness."""

    def test_scenario_loader(self):
        """Verify all 60 scenarios are loaded and categorized."""
        scenarios = scenario_loader.load_all_scenarios()
        self.assertEqual(len(scenarios), 69)

        # Check category filter
        orders_scenarios = scenario_loader.get_by_category("orders")
        self.assertEqual(len(orders_scenarios), 8)

        sec_scenarios = scenario_loader.get_by_category("security")
        self.assertEqual(len(sec_scenarios), 6)

    def test_metrics_calculator(self):
        """Verify accurate calculation of pass rates, confusion matrix, and latencies."""
        mock_results = [
            {
                "scenario_id": "P01",
                "category": "product",
                "expected_route": "STRUCTURED",
                "actual_route": "STRUCTURED",
                "expected_escalation": False,
                "actual_escalation": False,
                "passed": True,
                "latency_seconds": 0.05,
                "tokens": 100,
                "assertions": {"route": True, "escalation": True, "security": True, "grounding": True}
            },
            {
                "scenario_id": "H01",
                "category": "escalation",
                "expected_route": "HUMAN",
                "actual_route": "HUMAN",
                "expected_escalation": True,
                "actual_escalation": True,
                "passed": True,
                "latency_seconds": 0.10,
                "tokens": 150,
                "assertions": {"route": True, "escalation": True, "security": True, "grounding": True}
            }
        ]

        metrics = metrics_calculator.calculate(mock_results)
        self.assertEqual(metrics.total_scenarios, 2)
        self.assertEqual(metrics.passed_scenarios, 2)
        self.assertEqual(metrics.overall_pass_rate, 100.0)
        self.assertEqual(metrics.routing_accuracy, 100.0)
        self.assertEqual(metrics.grounding_rate, 100.0)
        self.assertEqual(metrics.security_violations, 0)
        self.assertEqual(metrics.escalation_f1, 1.0)


if __name__ == "__main__":
    unittest.main()

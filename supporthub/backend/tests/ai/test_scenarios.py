"""Integration test for all 60 Customer Support Benchmark Scenarios."""
import unittest
from app.scripts.test_scenarios import run_evaluation


class TestAllBenchmarkScenarios(unittest.TestCase):
    """Test 100% scenario pass rate across all 60 scenarios."""

    def test_60_scenarios_execution(self):
        report = run_evaluation()
        self.assertEqual(report["total_scenarios"], 60)
        self.assertEqual(report["total_passed"], 60)
        self.assertEqual(report["overall_accuracy_percentage"], 100.0)
        self.assertEqual(report["status"], "PASSED")


if __name__ == "__main__":
    unittest.main()

"""Report generator formatting markdown, JSON, and CLI summaries."""
import json
from pathlib import Path
from typing import Dict, Any, List
from app.evaluation.metrics import EvaluationMetrics


class ReportGenerator:
    """Generates structured evaluation reports in Markdown and JSON."""

    @staticmethod
    def generate_json(metrics: EvaluationMetrics, detailed_results: List[Dict[str, Any]], filepath: Path) -> None:
        """Save complete structured report to JSON."""
        data = {
            "summary": {
                "total_scenarios": metrics.total_scenarios,
                "passed_scenarios": metrics.passed_scenarios,
                "failed_scenarios": metrics.failed_scenarios,
                "overall_pass_rate_percentage": metrics.overall_pass_rate,
                "routing_accuracy_percentage": metrics.routing_accuracy,
                "grounding_rate_percentage": metrics.grounding_rate,
                "hallucination_rate_percentage": metrics.hallucination_rate,
                "security_violations": metrics.security_violations,
                "escalation_metrics": {
                    "precision": metrics.escalation_precision,
                    "recall": metrics.escalation_recall,
                    "f1": metrics.escalation_f1
                },
                "latency_seconds": {
                    "mean": metrics.latency_mean,
                    "p50": metrics.latency_p50,
                    "p90": metrics.latency_p90,
                    "p99": metrics.latency_p99,
                    "min": metrics.latency_min,
                    "max": metrics.latency_max
                }
            },
            "category_breakdown": metrics.category_breakdown,
            "detailed_results": detailed_results
        }
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def generate_markdown(metrics: EvaluationMetrics, detailed_results: List[Dict[str, Any]], filepath: Path) -> None:
        """Save comprehensive markdown report."""
        lines = [
            "# SupportHub AI Architecture - Phase 9 Evaluation Report",
            "",
            "## 1. Executive Summary",
            "",
            f"- **Total Scenarios Evaluated**: {metrics.total_scenarios}",
            f"- **Passed Scenarios**: {metrics.passed_scenarios}",
            f"- **Failed Scenarios**: {metrics.failed_scenarios}",
            f"- **Overall Pass Rate**: **{metrics.overall_pass_rate}%**",
            f"- **Routing Accuracy**: {metrics.routing_accuracy}%",
            f"- **Grounding Rate**: {metrics.grounding_rate}% (Hallucination Rate: {metrics.hallucination_rate}%)",
            f"- **Security Violations**: **{metrics.security_violations}** (Zero Tolerance Enforced)",
            f"- **Escalation F1 Score**: {metrics.escalation_f1} (Precision: {metrics.escalation_precision}, Recall: {metrics.escalation_recall})",
            f"- **Latency (P50 / P90 / Mean)**: {metrics.latency_p50}s / {metrics.latency_p90}s / {metrics.latency_mean}s",
            "",
            "## 2. Category Performance Breakdown",
            "",
            "| Category | Total | Passed | Failed | Pass Rate |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]

        for cat, stats in metrics.category_breakdown.items():
            lines.append(f"| {cat} | {stats['total']} | {stats['passed']} | {stats['failed']} | {stats['pass_rate']}% |")

        lines.extend([
            "",
            "## 3. Detailed Scenario Outcomes",
            "",
            "| ID | Category | Expected Route | Actual Route | Escalated | Status |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |"
        ])

        for r in detailed_results:
            status = "PASS" if r["passed"] else f"FAIL ({'; '.join(r['failures'])})"
            esc_str = "YES" if r["actual_escalation"] else "NO"
            lines.append(f"| {r['scenario_id']} | {r['category']} | {r['expected_route']} | {r['actual_route']} | {esc_str} | {status} |")

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    @staticmethod
    def print_terminal_summary(metrics: EvaluationMetrics) -> None:
        """Print clean formatted breakdown to standard output."""
        print("\n" + "=" * 90)
        print("                     BENCHMARK EVALUATION CATEGORY BREAKDOWN")
        print("=" * 90)
        print(f"{'Category':<20} | {'Total':<8} | {'Passed':<8} | {'Failed':<8} | {'Pass Rate'}")
        print("-" * 90)
        for cat, stats in metrics.category_breakdown.items():
            print(f"{cat:<20} | {stats['total']:<8} | {stats['passed']:<8} | {stats['failed']:<8} | {stats['pass_rate']:>6.1f}%")
        print("-" * 90)
        print(f"{'OVERALL TOTAL':<20} | {metrics.total_scenarios:<8} | {metrics.passed_scenarios:<8} | {metrics.failed_scenarios:<8} | {metrics.overall_pass_rate:>6.1f}%")
        print("=" * 90)
        print(f"Routing Accuracy:     {metrics.routing_accuracy}%")
        print(f"Grounding Rate:       {metrics.grounding_rate}%")
        print(f"Security Violations:  {metrics.security_violations}")
        print(f"Escalation F1 Score:  {metrics.escalation_f1}")
        print(f"Latency P50 / P90:    {metrics.latency_p50}s / {metrics.latency_p90}s")
        print("=" * 90)


report_generator = ReportGenerator()

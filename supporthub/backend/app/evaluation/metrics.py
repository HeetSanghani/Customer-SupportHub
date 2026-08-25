"""Statistical metrics and aggregation for AI benchmark evaluation."""
import statistics
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class EvaluationMetrics:
    """Comprehensive statistical metrics for an evaluation run."""
    total_scenarios: int = 0
    passed_scenarios: int = 0
    failed_scenarios: int = 0
    overall_pass_rate: float = 0.0
    
    # Pathway Accuracies
    routing_accuracy: float = 0.0
    grounding_rate: float = 0.0
    hallucination_rate: float = 0.0
    security_violations: int = 0
    
    # Escalation Metrics
    escalation_true_positives: int = 0
    escalation_false_positives: int = 0
    escalation_false_negatives: int = 0
    escalation_true_negatives: int = 0
    escalation_precision: float = 0.0
    escalation_recall: float = 0.0
    escalation_f1: float = 0.0
    
    # Latency Metrics (seconds)
    latency_min: float = 0.0
    latency_max: float = 0.0
    latency_mean: float = 0.0
    latency_p50: float = 0.0
    latency_p90: float = 0.0
    latency_p99: float = 0.0
    
    # Category Statistics
    category_breakdown: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Token Usage
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    avg_tokens_per_scenario: float = 0.0


class MetricsCalculator:
    """Computes comprehensive evaluation metrics from execution records."""

    @staticmethod
    def calculate(scenario_results: List[Dict[str, Any]]) -> EvaluationMetrics:
        """Compute full statistical summary from executed scenario results."""
        if not scenario_results:
            return EvaluationMetrics()

        total = len(scenario_results)
        passed = sum(1 for r in scenario_results if r["passed"])
        failed = total - passed
        pass_rate = round((passed / total) * 100, 2)

        routing_correct = sum(1 for r in scenario_results if r["assertions"]["route"])
        routing_acc = round((routing_correct / total) * 100, 2)

        grounded_count = sum(1 for r in scenario_results if r["assertions"]["grounding"])
        grounding_rt = round((grounded_count / total) * 100, 2)
        hallucination_rt = round(100.0 - grounding_rt, 2)

        sec_violations = sum(1 for r in scenario_results if not r["assertions"]["security"])

        # Escalation Confusion Matrix
        tp = fp = fn = tn = 0
        for r in scenario_results:
            exp_esc = r["expected_escalation"]
            act_esc = r["actual_escalation"]
            if exp_esc and act_esc:
                tp += 1
            elif not exp_esc and act_esc:
                fp += 1
            elif exp_esc and not act_esc:
                fn += 1
            else:
                tn += 1

        precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 1.0
        recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 1.0
        f1 = round(2 * (precision * recall) / (precision + recall), 4) if (precision + recall) > 0 else 1.0

        # Latencies
        latencies = [r.get("latency_seconds", 0.001) for r in scenario_results]
        latencies.sort()
        l_min = round(min(latencies), 4)
        l_max = round(max(latencies), 4)
        l_mean = round(statistics.mean(latencies), 4)
        l_p50 = round(statistics.median(latencies), 4)
        l_p90 = round(latencies[int(len(latencies) * 0.90)], 4) if latencies else 0.0
        l_p99 = round(latencies[min(int(len(latencies) * 0.99), len(latencies) - 1)], 4) if latencies else 0.0

        # Category Breakdown
        categories: Dict[str, Dict[str, Any]] = {}
        for r in scenario_results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "passed": 0, "failed": 0, "pass_rate": 0.0}
            categories[cat]["total"] += 1
            if r["passed"]:
                categories[cat]["passed"] += 1
            else:
                categories[cat]["failed"] += 1

        for cat, stats in categories.items():
            stats["pass_rate"] = round((stats["passed"] / stats["total"]) * 100, 1)

        # Tokens
        total_tok = sum(r.get("tokens", 0) for r in scenario_results)
        avg_tok = round(total_tok / total, 1)

        return EvaluationMetrics(
            total_scenarios=total,
            passed_scenarios=passed,
            failed_scenarios=failed,
            overall_pass_rate=pass_rate,
            routing_accuracy=routing_acc,
            grounding_rate=grounding_rt,
            hallucination_rate=hallucination_rt,
            security_violations=sec_violations,
            escalation_true_positives=tp,
            escalation_false_positives=fp,
            escalation_false_negatives=fn,
            escalation_true_negatives=tn,
            escalation_precision=precision,
            escalation_recall=recall,
            escalation_f1=f1,
            latency_min=l_min,
            latency_max=l_max,
            latency_mean=l_mean,
            latency_p50=l_p50,
            latency_p90=l_p90,
            latency_p99=l_p99,
            category_breakdown=categories,
            total_tokens=total_tok,
            avg_tokens_per_scenario=avg_tok
        )


metrics_calculator = MetricsCalculator()

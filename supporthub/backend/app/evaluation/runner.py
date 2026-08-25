"""Evaluation runner orchestrating batch executions."""
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from app.ai.config import settings
from app.evaluation.scenario_loader import scenario_loader, BenchmarkScenario
from app.evaluation.evaluator import scenario_evaluator
from app.evaluation.metrics import metrics_calculator, EvaluationMetrics
from app.evaluation.report import report_generator


class EvaluationRunner:
    """Orchestrates comprehensive benchmark test runs."""

    def __init__(self):
        self.loader = scenario_loader
        self.evaluator = scenario_evaluator
        self.calculator = metrics_calculator
        self.reporter = report_generator

    def run(
        self,
        category: Optional[str] = None,
        limit: Optional[int] = None,
        use_llm: bool = False,
        json_output: Optional[Path] = None,
        md_output: Optional[Path] = None,
        quiet: bool = False
    ) -> EvaluationMetrics:
        """Execute evaluation suite across scenarios."""
        if category:
            scenarios = self.loader.get_by_category(category)
        else:
            scenarios = self.loader.load_all_scenarios()

        if limit:
            scenarios = scenarios[:limit]

        if not quiet:
            print("=" * 90)
            print("       SUPPORTHUB AI ARCHITECTURE - BENCHMARK SCENARIO EVALUATION")
            print("=" * 90)
            print(f"Scenarios to Run: {len(scenarios)}")
            print(f"Mode:             {'REAL LLM (Gemini)' if use_llm else 'DETERMINISTIC SANDBOX'}")
            print(f"Category Filter:  {category or 'ALL (12 Categories)'}")
            print("-" * 90)
            print(f"{'ID':<6} | {'Category':<15} | {'Expected':<12} | {'Actual':<12} | {'Escalated':<10} | {'Status'}")
            print("-" * 90)

        results: List[Dict[str, Any]] = []
        for s in scenarios:
            res = self.evaluator.evaluate_scenario(s, use_llm=use_llm)
            results.append(res)

            if not quiet:
                status_str = "[PASS]" if res["passed"] else f"[FAIL: {'; '.join(res['failures'])}]"
                esc_str = "YES" if res["actual_escalation"] else "NO"
                print(f"{res['scenario_id']:<6} | {res['category']:<15} | {res['expected_route']:<12} | {res['actual_route']:<12} | {esc_str:<10} | {status_str}")

        metrics = self.calculator.calculate(results)

        if not quiet:
            self.reporter.print_terminal_summary(metrics)

        # Output file paths
        out_dir = settings.BASE_DIR / "output"
        out_dir.mkdir(parents=True, exist_ok=True)
        
        target_json = json_output or (out_dir / ("evaluation_report_llm.json" if use_llm else "evaluation_report.json"))
        target_md = md_output or (settings.BASE_DIR / "docs" / ("llm_evaluation_report.md" if use_llm else "evaluation_report.md"))

        self.reporter.generate_json(metrics, results, target_json)
        self.reporter.generate_markdown(metrics, results, target_md)

        if not quiet:
            print(f"\n[+] JSON Report saved to:     {target_json}")
            print(f"[+] Markdown Report saved to: {target_md}\n")

        return metrics


evaluation_runner = EvaluationRunner()

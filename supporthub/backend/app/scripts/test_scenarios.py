"""Complete Benchmark Scenario Evaluation Harness using ScenarioEvaluator."""
import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ai.config import settings
from app.data_access.loader import data_loader
from app.evaluation.scenario_loader import scenario_loader
from app.evaluation.evaluator import scenario_evaluator


def run_evaluation(use_llm: bool = False) -> Dict[str, Any]:
    print("=" * 90)
    print("       SUPPORTHUB AI ARCHITECTURE - BENCHMARK SCENARIO EVALUATION")
    print("=" * 90)

    # Load scenarios
    data_loader.load()
    scenarios = scenario_loader.load_all_scenarios()

    category_stats = {}
    detailed_results = []
    total_passed = 0

    print(f"\n[+] Executing {len(scenarios)} Benchmark Scenarios...\n")
    print(f"{'ID':<6} | {'Category':<15} | {'Expected Route':<15} | {'Actual Route':<12} | {'Escalated':<10} | {'Status'}")
    print("-" * 90)

    for scenario in scenarios:
        sid = scenario.scenario_id
        category = scenario.category
        expected_esc = scenario.expected_escalation or scenario.expected_route == "HUMAN"
        
        if category not in category_stats:
            category_stats[category] = {"total": 0, "passed": 0, "failed": 0}
        category_stats[category]["total"] += 1

        eval_res = scenario_evaluator.evaluate_scenario(scenario, use_llm=use_llm)

        passed = eval_res["passed"]
        failures = eval_res["failures"]
        failure_reason = " | ".join(failures) if failures else ""

        if passed:
            total_passed += 1
            category_stats[category]["passed"] += 1
            status_str = "[PASS]"
        else:
            category_stats[category]["failed"] += 1
            status_str = f"[FAIL: {failure_reason}]"

        is_esc_str = "YES" if eval_res["actual_escalation"] else "NO"
        print(f"{sid:<6} | {category:<15} | {scenario.expected_route:<15} | {eval_res['actual_route']:<12} | {is_esc_str:<10} | {status_str}")

        detailed_results.append({
            "scenario_id": sid,
            "category": category,
            "question": scenario.customer_question,
            "expected_escalation": expected_esc,
            "actual_route": eval_res["actual_route"],
            "escalated": eval_res["actual_escalation"],
            "passed": passed,
            "failure_reason": failure_reason,
            "latency_seconds": eval_res["latency_seconds"],
            "citations_count": eval_res["citations_count"],
            "assertions": eval_res["assertions"],
            "response_preview": eval_res["response_preview"]
        })

    # Summary Calculations
    total_scenarios = len(scenarios)
    overall_accuracy = (total_passed / total_scenarios) * 100 if total_scenarios > 0 else 0.0

    print("\n" + "=" * 90)
    print("                     BENCHMARK EVALUATION CATEGORY BREAKDOWN")
    print("=" * 90)
    print(f"{'Category':<20} | {'Total':<8} | {'Passed':<8} | {'Failed':<8} | {'Pass Rate'}")
    print("-" * 90)
    for cat, stats in category_stats.items():
        rate = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0.0
        print(f"{cat:<20} | {stats['total']:<8} | {stats['passed']:<8} | {stats['failed']:<8} | {rate:>6.1f}%")
    print("-" * 90)
    print(f"{'OVERALL TOTAL':<20} | {total_scenarios:<8} | {total_passed:<8} | {total_scenarios - total_passed:<8} | {overall_accuracy:>6.1f}%")
    print("=" * 90)

    # Historical Tracking & Regression Diff
    output_dir = settings.BASE_DIR / "output"
    history_dir = output_dir / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    report_file = output_dir / "evaluation_report.json"

    history_files = sorted(history_dir.glob("evaluation_report_*.json"))
    prev_report_file = history_files[-1] if history_files else None

    regressions = []
    improvements = []
    net_accuracy_change = 0.0
    has_history = False
    prev_report_name = None

    if prev_report_file:
        has_history = True
        prev_report_name = prev_report_file.name
        try:
            with open(prev_report_file, "r", encoding="utf-8") as pf:
                prev_data = json.load(pf)
                prev_results = {item["scenario_id"]: item["passed"] for item in prev_data.get("detailed_results", [])}
                curr_results = {item["scenario_id"]: item["passed"] for item in detailed_results}

                for sid_item, is_pass in curr_results.items():
                    was_pass = prev_results.get(sid_item)
                    if was_pass is True and not is_pass:
                        regressions.append(sid_item)
                    elif was_pass is False and is_pass:
                        improvements.append(sid_item)

                prev_acc = prev_data.get("overall_accuracy_percentage", 0.0)
                net_accuracy_change = round(overall_accuracy - prev_acc, 2)
        except Exception as e:
            print(f"[!] Warning: Could not parse previous report history: {e}")

    regression_summary = {
        "has_history": has_history,
        "previous_report": prev_report_name,
        "regressions": regressions,
        "improvements": improvements,
        "net_accuracy_change_percentage": net_accuracy_change
    }

    print("\n" + "=" * 90)
    print("                     HISTORICAL REGRESSION & TREND SUMMARY")
    print("=" * 90)
    print(f"Has Previous History : {'Yes (' + prev_report_name + ')' if has_history else 'No (Baseline Run)'}")
    print(f"Net Accuracy Change  : {net_accuracy_change:+.2f}%")
    print(f"Regressions ({len(regressions)})     : {', '.join(regressions) if regressions else 'None'}")
    print(f"Improvements ({len(improvements)})    : {', '.join(improvements) if improvements else 'None'}")
    print("=" * 90)

    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    history_report_file = history_dir / f"evaluation_report_{timestamp_str}.json"

    report_data = {
        "timestamp": timestamp_str,
        "total_scenarios": total_scenarios,
        "total_passed": total_passed,
        "overall_accuracy_percentage": round(overall_accuracy, 2),
        "target_accuracy": "100%",
        "status": "PASSED" if total_passed == total_scenarios and len(regressions) == 0 else "NEEDS_REFINEMENT",
        "regression_summary": regression_summary,
        "category_breakdown": category_stats,
        "detailed_results": detailed_results
    }

    # Write both latest and timestamped historical file
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    with open(history_report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    print(f"\n[+] Latest Evaluation Report saved to: {report_file}")
    print(f"[+] Historical Evaluation Archive saved to: {history_report_file}")

    return report_data


if __name__ == "__main__":
    report = run_evaluation()
    if report.get("regression_summary", {}).get("regressions"):
        print("\n[!] FATAL: Regression detected! Exiting with code 1.")
        sys.exit(1)



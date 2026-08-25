"""Evaluator for single and batch benchmark scenario execution."""
import time
from typing import Dict, Any, Optional
from app.ai.orchestrator import AIOrchestrator, ai_orchestrator
from app.ai.context import context_manager
from app.data_access.loader import data_loader
from app.evaluation.scenario_loader import BenchmarkScenario
from app.evaluation.assertions import assertions


class ScenarioEvaluator:
    """Executes individual scenarios and records assertion outcomes and telemetry."""

    def __init__(self, orchestrator: Optional[AIOrchestrator] = None):
        self.orchestrator = orchestrator or ai_orchestrator

    def evaluate_scenario(
        self,
        scenario: BenchmarkScenario,
        use_llm: bool = False
    ) -> Dict[str, Any]:
        """Execute a single scenario and run all rigorous assertions."""
        sid = scenario.scenario_id
        category = scenario.category
        question = scenario.customer_question
        req_cond = scenario.required_conditions
        conv_id = f"eval_{sid}"

        # Resolve caller customer ID
        caller_cust_id = req_cond.get("customer_id")
        if not caller_cust_id and "order_id" in req_cond:
            ord_rec = data_loader.orders.get(req_cond["order_id"])
            if ord_rec:
                caller_cust_id = ord_rec.customer_id

        start_time = time.time()

        # Handle multi-turn scenarios
        if sid == "M01":
            self.orchestrator.process_message(
                query="Where is my order ORD-013 right now?",
                customer_id=caller_cust_id,
                conversation_id=conv_id,
                use_llm=use_llm
            )
            response = self.orchestrator.process_message(
                query="And what is the carrier tracking number for it?",
                customer_id=caller_cust_id,
                conversation_id=conv_id,
                use_llm=use_llm
            )
        elif sid == "M02":
            self.orchestrator.process_message(
                query="Has my return for ORD-016 been initiated?",
                customer_id=caller_cust_id,
                conversation_id=conv_id,
                use_llm=use_llm
            )
            response = self.orchestrator.process_message(
                query="When will the refund arrive?",
                customer_id=caller_cust_id,
                conversation_id=conv_id,
                use_llm=use_llm
            )
        else:
            response = self.orchestrator.process_message(
                query=question,
                customer_id=caller_cust_id,
                conversation_id=conv_id,
                use_llm=use_llm
            )

        latency = time.time() - start_time

        # Run Assertions
        route_assert = assertions.assert_route(scenario, response)
        esc_assert = assertions.assert_escalation(scenario, response)
        sec_assert = assertions.assert_security_invariance(scenario, response)
        grounding_assert = assertions.assert_grounding(scenario, response)
        multi_topic_assert = assertions.assert_multi_topic(scenario, response)
        esc_context_assert = assertions.assert_escalation_context(scenario, response)

        passed = (
            route_assert.passed and
            esc_assert.passed and
            sec_assert.passed and
            grounding_assert.passed and
            multi_topic_assert.passed and
            esc_context_assert.passed
        )

        failures = []
        if not route_assert.passed:
            failures.append(route_assert.message)
        if not esc_assert.passed:
            failures.append(esc_assert.message)
        if not sec_assert.passed:
            failures.append(sec_assert.message)
        if not grounding_assert.passed:
            failures.append(grounding_assert.message)
        if not multi_topic_assert.passed:
            failures.append(multi_topic_assert.message)
        if not esc_context_assert.passed:
            failures.append(esc_context_assert.message)

        actual_esc = bool(
            response.route_type == "HUMAN" or
            (response.escalation_decision and response.escalation_decision.should_escalate)
        )

        return {
            "scenario_id": sid,
            "category": category,
            "question": question,
            "required_conditions": scenario.required_conditions,
            "expected_route": scenario.expected_route,
            "actual_route": response.route_type,
            "expected_escalation": scenario.expected_escalation or scenario.expected_route == "HUMAN",
            "actual_escalation": actual_esc,
            "passed": passed,
            "failures": failures,
            "latency_seconds": round(latency, 4),
            "is_llm_generated": getattr(response, "is_llm_generated", False),
            "citations_count": len(response.rag_citations),
            "response_preview": response.content[:150],
            "assertions": {
                "route": route_assert.passed,
                "escalation": esc_assert.passed,
                "security": sec_assert.passed,
                "grounding": grounding_assert.passed,
                "multi_topic": multi_topic_assert.passed,
                "escalation_context": esc_context_assert.passed
            }
        }


# Global singleton evaluator
scenario_evaluator = ScenarioEvaluator()

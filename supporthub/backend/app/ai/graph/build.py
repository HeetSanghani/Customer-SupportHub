from __future__ import annotations

from langgraph.graph import END, StateGraph

from . import nodes
from .state import GraphState


def _route_after_escalation(state: GraphState) -> str:
    return "escalate" if state.get("escalated") else "decompose"


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("check_escalation", nodes.check_escalation)
    graph.add_node("decompose_query", nodes.decompose_query)
    graph.add_node("handle_subquestions", nodes.handle_subquestions)
    graph.add_node("aggregate_responses", nodes.aggregate_responses)
    graph.add_node("handle_human_escalation", nodes.handle_human_escalation)

    graph.set_entry_point("check_escalation")

    graph.add_conditional_edges(
        "check_escalation",
        _route_after_escalation,
        {
            "escalate": "handle_human_escalation",
            "decompose": "decompose_query",
        },
    )

    graph.add_edge("decompose_query", "handle_subquestions")
    graph.add_edge("handle_subquestions", "aggregate_responses")
    graph.add_edge("aggregate_responses", END)
    graph.add_edge("handle_human_escalation", END)

    return graph.compile()


compiled_graph = build_graph()

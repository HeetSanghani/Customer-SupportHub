import pytest
import pytest_asyncio
from app.ai.graph.build import compiled_graph
from app.ai.graph.nodes import _hybrid_split
from app.ai.router import ai_router, RouteType

@pytest.mark.asyncio
async def test_multi_question_decomposition_three_intents():
    query = "Show my order, payment and shipment status."
    subs = _hybrid_split(query)
    assert len(subs) == 3
    texts = [s["text"] for s in subs]
    assert "order" in texts[0].lower()
    assert "payment" in texts[1].lower()
    assert "shipment" in texts[2].lower()

@pytest.mark.asyncio
async def test_multi_question_execution_and_aggregation():
    query = "Show my order, payment and shipment status."
    initial_state = {
        "raw_query": query,
        "customer_id": "CUST-001",
        "conversation_id": "conv_test_b2_1",
        "use_llm": False,
        "channel_type": "WEBSITE",
        "sub_questions": [],
        "escalated": False
    }
    res_state = await compiled_graph.ainvoke(initial_state)
    final_resp = res_state.get("final_response")
    assert final_resp is not None
    content = final_resp.content.lower()
    assert "order ord-001" in content
    assert "payment" in content
    assert "shipment" in content

@pytest.mark.asyncio
async def test_multi_question_informational_and_escalation():
    query = "Where is ORD-001, can I return it, and connect me to a human?"
    initial_state = {
        "raw_query": query,
        "customer_id": "CUST-001",
        "conversation_id": "conv_test_b2_1_esc",
        "use_llm": False,
        "channel_type": "WEBSITE",
        "sub_questions": [],
        "escalated": False
    }
    res_state = await compiled_graph.ainvoke(initial_state)
    final_resp = res_state.get("final_response")
    assert final_resp is not None
    assert final_resp.route_type == "HUMAN"
    content = final_resp.content.lower()
    assert "delivered" in content or "ord-001" in content
    assert "transferred your request" in content or "human support representative" in content

@pytest.mark.asyncio
async def test_multi_question_anti_idor_isolation():
    query = "Show my order ORD-001 and ORD-004."
    initial_state = {
        "raw_query": query,
        "customer_id": "CUST-001",
        "conversation_id": "conv_test_b2_1_idor",
        "use_llm": False,
        "channel_type": "WEBSITE",
        "sub_questions": [],
        "escalated": False
    }
    res_state = await compiled_graph.ainvoke(initial_state)
    final_resp = res_state.get("final_response")
    assert final_resp is not None
    content = final_resp.content.lower()
    assert "ord-001" in content
    assert "access denied" in content or "not authorized" in content

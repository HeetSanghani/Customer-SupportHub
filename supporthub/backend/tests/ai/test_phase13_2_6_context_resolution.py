"""Phase 13.2.6 Automated Test Suite — Context Resolution & Remediation Validation.

Covers 20 mandatory test scenarios:
1. Explicit product query
2. Explicit order query
3. Product 'its' pronoun follow-up
4. Product 'it' pronoun follow-up
5. Order 'its' pronoun follow-up
6. Order 'it' pronoun follow-up
7. Product -> Order -> Product domain switch
8. Order -> Product -> Product domain switch
9. Product -> Shipment transition
10. Order -> Shipment transition
11. RAG -> Product explicit update
12. RAG -> Order explicit update
13. Unauthorized entity security denial
14. Unauthorized implicit follow-up isolation
15. Guest private-data query restriction
16. Ambiguous reference handling / clarification
17. Explicit entity precedence over stale context
18. LLM classifier explicit_entities contract
19. Deterministic fallback path context preservation
20. Multi-turn context preservation across valid turns
"""

import pytest
from app.ai.orchestrator import ai_orchestrator
from app.ai.context import ConversationContext
from app.ai.intent import IntentClassifier, LLMIntentClassifier, IntentCategory, IntentResult
from app.ai.router import AIRouter


@pytest.fixture
def clean_context():
    """Returns a fresh conversation context for CUST-001."""
    return ConversationContext(conversation_id="test_sess_p13_2_6", customer_id="CUST-001")


def test_01_explicit_product(clean_context):
    """1. Explicit product query retrieves product details."""
    res = ai_orchestrator.process_message("Tell me about PROD-002.", context_override=clean_context, use_llm=False)
    assert "AeroTab" in res.content or "PROD-002" in res.content
    assert clean_context.active_product_id == "PROD-002"
    assert clean_context.active_order_id is None


def test_02_explicit_order(clean_context):
    """2. Explicit order query retrieves order details."""
    res = ai_orchestrator.process_message("What is the status of ORD-025?", context_override=clean_context, use_llm=False)
    assert "ORD-025" in res.content or "CONFIRMED" in res.content
    assert clean_context.active_order_id == "ORD-025"
    assert clean_context.active_product_id is None


def test_03_product_its_followup(clean_context):
    """3. Product follow-up using 'its': 'Tell me about PROD-002.' -> 'What is its price?'."""
    ai_orchestrator.process_message("Tell me about PROD-002.", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("What is its price?", context_override=clean_context, use_llm=False)
    assert "₹" in res.content or "Price" in res.content or "46,999" in res.content or "AeroTab" in res.content
    assert "ORD-" not in res.content


def test_04_product_it_followup(clean_context):
    """4. Product follow-up using 'it': 'Tell me about PROD-002.' -> 'Is it available?'."""
    ai_orchestrator.process_message("Tell me about PROD-002.", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("Is it available?", context_override=clean_context, use_llm=False)
    assert "IN_STOCK" in res.content or "available" in res.content.lower()
    assert "ORD-" not in res.content


def test_05_order_its_followup(clean_context):
    """5. Order follow-up using 'its': 'What is the status of ORD-025?' -> 'What is its total?'."""
    ai_orchestrator.process_message("What is the status of ORD-025?", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("What is its total?", context_override=clean_context, use_llm=False)
    assert "ORD-025" in res.content or "2,899" in res.content or "₹" in res.content


def test_06_order_it_followup(clean_context):
    """6. Order follow-up using 'it': 'What is the status of ORD-025?' -> 'What carrier is handling it?'."""
    ai_orchestrator.process_message("What is the status of ORD-025?", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("What carrier is handling it?", context_override=clean_context, use_llm=False)
    assert "XpressBees" in res.content or "shipment" in res.content.lower() or "carrier" in res.content.lower()


def test_07_product_order_product_switch(clean_context):
    """7. Domain switch: PROD-002 -> ORD-025 -> 'What is its price?' -> PROD-002."""
    ai_orchestrator.process_message("Tell me about PROD-002.", context_override=clean_context, use_llm=False)
    ai_orchestrator.process_message("What is the status of ORD-025?", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("What is its price?", context_override=clean_context, use_llm=False)
    assert "₹" in res.content or "AeroTab" in res.content or "Price" in res.content
    assert "ORD-025" not in res.content


def test_08_order_product_product_switch(clean_context):
    """8. Domain switch: ORD-025 -> PROD-002 -> 'Is it available?' -> PROD-002."""
    ai_orchestrator.process_message("What is the status of ORD-025?", context_override=clean_context, use_llm=False)
    ai_orchestrator.process_message("Tell me about PROD-002.", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("Is it available?", context_override=clean_context, use_llm=False)
    assert "IN_STOCK" in res.content or "available" in res.content.lower()
    assert "ORD-025" not in res.content


def test_09_product_to_shipment(clean_context):
    """9. Transition: PROD-002 -> 'Where is my shipment?' -> Customer shipment."""
    ai_orchestrator.process_message("Tell me about PROD-002.", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("Where is my shipment?", context_override=clean_context, use_llm=False)
    assert "Shipment" in res.content or "TRK-" in res.content or "DELIVERED" in res.content or "IN_TRANSIT" in res.content
    assert "AeroTab" not in res.content


def test_10_order_to_shipment(clean_context):
    """10. Transition: ORD-025 -> 'Where is my shipment?' -> ORD-025 shipment."""
    ai_orchestrator.process_message("What is the status of ORD-025?", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("Where is my shipment?", context_override=clean_context, use_llm=False)
    assert "Shipment" in res.content or "TRK-" in res.content or "XpressBees" in res.content


def test_11_rag_product_context_update(clean_context):
    """11. RAG query with explicit product updates product context slot."""
    res = ai_orchestrator.process_message("What is the return policy for PROD-002?", context_override=clean_context, use_llm=False)
    assert "return" in res.content.lower() or "policy" in res.content.lower()
    assert clean_context.active_product_id == "PROD-002"


def test_12_rag_order_context_update(clean_context):
    """12. RAG policy query with explicit order updates order context slot."""
    res = ai_orchestrator.process_message("Can I cancel ORD-025 according to your policy?", context_override=clean_context, use_llm=False)
    assert res.content is not None
    assert clean_context.active_order_id == "ORD-025"


def test_13_unauthorized_entity_denial(clean_context):
    """13. Security test: Unauthorized order ORD-003 inquiry is denied and NOT saved in context."""
    res = ai_orchestrator.process_message("What is the status of ORD-003?", context_override=clean_context, use_llm=False)
    assert "Access Denied" in res.content or "not authorized" in res.content.lower()
    assert clean_context.active_order_id is None


def test_14_unauthorized_implicit_followup(clean_context):
    """14. Security test: Implicit follow-up after security denial does NOT leak foreign data."""
    ai_orchestrator.process_message("What is the status of ORD-003?", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("What is its status?", context_override=clean_context, use_llm=False)
    assert "unable to locate" in res.content.lower() or "no active" in res.content.lower() or "please check" in res.content.lower() or "specify" in res.content.lower() or "ord-001" in res.content.lower()
    assert "ORD-003" not in res.content


def test_15_guest_private_data_guard():
    """15. Guest guard: GUEST account cannot access private order data or store active order slots."""
    guest_ctx = ConversationContext(conversation_id="guest_sess", customer_id="GUEST")
    res = ai_orchestrator.process_message("What is the status of ORD-025?", context_override=guest_ctx, use_llm=False)
    assert "log in" in res.content.lower() or "authenticated" in res.content.lower()
    assert guest_ctx.active_order_id is None


def test_16_ambiguous_reference_handling():
    """16. Ambiguous reference in fresh session does not guess random entity."""
    fresh_ctx = ConversationContext(conversation_id="fresh_sess", customer_id="CUST-001")
    res = ai_orchestrator.process_message("What is its price?", context_override=fresh_ctx, use_llm=False)
    assert "unable to locate" in res.content.lower() or "please check" in res.content.lower() or "specify" in res.content.lower() or "which product" in res.content.lower()


def test_17_explicit_entity_precedence(clean_context):
    """17. Explicit entity in query overrides active context slot."""
    ai_orchestrator.process_message("Tell me about PROD-002.", context_override=clean_context, use_llm=False)
    res = ai_orchestrator.process_message("What is the price of PROD-001?", context_override=clean_context, use_llm=False)
    assert "PROD-001" in res.content or "NovaPhone" in res.content
    assert clean_context.active_product_id == "PROD-001"


def test_18_llm_classifier_explicit_entities_contract():
    """18. LLMIntentClassifier populates explicit_entities contract."""
    llm_clf = LLMIntentClassifier()
    res = llm_clf.classify("Tell me about PROD-002.", customer_id="CUST-001", use_llm=False)
    assert "product_id" in res.explicit_entities
    assert res.explicit_entities["product_id"] == "PROD-002"


def test_19_fallback_path_context_preservation():
    """19. Deterministic fallback path in LLMIntentClassifier preserves context_slots."""
    llm_clf = LLMIntentClassifier()
    res = llm_clf.classify("What is its price?", context_slots={"product_id": "PROD-002"}, use_llm=False)
    assert res.category == IntentCategory.PRODUCT
    assert res.entities.get("product_id") == "PROD-002"


def test_20_multiturn_context_preservation(clean_context):
    """20. Multi-turn context remains stable across valid domain turns."""
    ai_orchestrator.process_message("Tell me about PROD-002.", context_override=clean_context, use_llm=False)
    assert clean_context.active_product_id == "PROD-002"
    ai_orchestrator.process_message("What is its price?", context_override=clean_context, use_llm=False)
    assert clean_context.active_product_id == "PROD-002"
    ai_orchestrator.process_message("Is it available?", context_override=clean_context, use_llm=False)
    assert clean_context.active_product_id == "PROD-002"

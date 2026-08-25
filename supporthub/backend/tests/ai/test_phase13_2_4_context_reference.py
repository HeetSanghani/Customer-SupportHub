"""
Phase 13.2.4 — Contextual Reference Resolution Remediation Tests

Verifies the fix for the confirmed Phase 13.2.3 root cause:
  - IntentResult now carries explicit_entities (current-query-only)
  - Orchestrator uses explicit_entities for update_slots_domain_aware()
  - Context-inherited order_id no longer overwrites product domain after product turn

Coverage:
  - IntentResult.explicit_entities field existence and correctness
  - Explicit vs merged entity distinction in classify()
  - Product contextual follow-up (the known failure scenario)
  - Order contextual follow-up (must still work)
  - Product → Order switching
  - Order → Product switching
  - Multi-turn chain: Order → Product → implicit follow-up
  - Multi-turn chain: Product → Shipment → Product → implicit follow-up
  - Security-denied context (must not pollute slots)
  - Unauthorized entity persistence check
  - All Group A-J regression behaviors from the prompt
"""

import uuid
import pytest

from app.ai.orchestrator import AIOrchestrator
from app.ai.context import context_manager
from app.ai.intent import IntentClassifier, IntentCategory


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_classifier = IntentClassifier()


def make_orch():
    return AIOrchestrator(use_llm=False)


def fresh_id():
    return f"ctx_1324_{uuid.uuid4().hex[:8]}"


def run_session(orch, queries, cust_id="CUST-001"):
    """Run queries in a fresh conversation, return list of (response, ctx snapshot)."""
    conv_id = fresh_id()
    results = []
    for q in queries:
        resp = orch.process_message(q, customer_id=cust_id, conversation_id=conv_id)
        ctx = context_manager.get_or_create(conv_id)
        results.append({
            "content": resp.content,
            "route": resp.route_type,
            "active_product_id": ctx.active_product_id,
            "active_order_id": ctx.active_order_id,
        })
    return results


def is_product(content: str) -> bool:
    return any(w in content for w in ["Product:", "Price:", "MRP:", "AeroTab", "NovaPhone", "Pixelite", "PROD-"])


def is_order(content: str) -> bool:
    return "Order " in content and any(w in content for w in ["CONFIRMED", "CANCELLED", "DELIVERED", "ORD-", "₹"])


def is_shipment(content: str) -> bool:
    return any(w in content for w in ["Shipment ", "SHIP-", "XpressBees", "Estimated Delivery", "Tracking Number"])


def is_denied(content: str) -> bool:
    return "Access Denied" in content or "not authorized" in content.lower()


# ---------------------------------------------------------------------------
# Unit Tests: IntentResult.explicit_entities field
# ---------------------------------------------------------------------------

class TestIntentResultExplicitEntities:
    def test_field_exists_on_intent_result(self):
        """IntentResult must have an explicit_entities field."""
        from app.ai.intent import IntentResult, IntentCategory
        result = _classifier.classify("Tell me about PROD-002.")
        assert hasattr(result, "explicit_entities"), "IntentResult must have explicit_entities field"

    def test_explicit_entities_product_only_no_context(self):
        """classify() with no context: explicit_entities should contain product_id only."""
        result = _classifier.classify("Tell me about PROD-002.")
        assert result.explicit_entities.get("product_id") == "PROD-002"
        assert "order_id" not in result.explicit_entities

    def test_explicit_entities_excludes_context_inherited_order(self):
        """With an active order_id in context, explicit_entities must NOT include order_id for a product query."""
        slots = {"order_id": "ORD-025", "product_id": None, "return_id": None, "refund_id": None}
        result = _classifier.classify("Tell me about PROD-002.", context_slots=slots)
        # entities (merged) may contain order_id, but explicit_entities must not
        assert result.explicit_entities.get("product_id") == "PROD-002"
        assert "order_id" not in result.explicit_entities, \
            f"explicit_entities must not contain context-inherited order_id. Got: {result.explicit_entities}"

    def test_entities_merged_still_contains_both(self):
        """entities (merged) must contain both product_id and order_id for tool resolution."""
        slots = {"order_id": "ORD-025", "product_id": None, "return_id": None, "refund_id": None}
        result = _classifier.classify("Tell me about PROD-002.", context_slots=slots)
        assert result.entities.get("product_id") == "PROD-002"
        assert result.entities.get("order_id") == "ORD-025"

    def test_explicit_entities_order_query_has_order_id(self):
        """An explicit order query must have order_id in explicit_entities."""
        result = _classifier.classify("What is the status of ORD-025?")
        assert result.explicit_entities.get("order_id") == "ORD-025"

    def test_explicit_entities_empty_for_implicit_followup(self):
        """A generic follow-up like 'What is its price?' has no explicit entities."""
        result = _classifier.classify("What is its price?")
        assert result.explicit_entities == {} or not result.explicit_entities.get("product_id")

    def test_explicit_entities_not_polluted_by_context_slots(self):
        """After ORD-025 context, 'What is its price?' must NOT have order_id in explicit_entities."""
        slots = {"order_id": "ORD-025", "product_id": "PROD-002"}
        result = _classifier.classify("What is its price?", context_slots=slots)
        # Current query has no explicit ID — explicit_entities must be empty
        assert result.explicit_entities == {}, \
            f"No explicit entity in query → explicit_entities must be empty. Got: {result.explicit_entities}"


# ---------------------------------------------------------------------------
# Integration Tests: Slot Persistence After Fix
# ---------------------------------------------------------------------------

class TestSlotPersistenceAfterFix:
    def test_product_slot_set_after_explicit_product_query(self):
        """After 'Tell me about PROD-002.', active_product_id must be PROD-002."""
        orch = make_orch()
        r = run_session(orch, ["Tell me about PROD-002."])
        assert r[0]["active_product_id"] == "PROD-002"
        assert r[0]["active_order_id"] is None

    def test_product_slot_survives_after_order_preceded(self):
        """The critical bug: after ORD-025 then PROD-002, active_product_id must be PROD-002."""
        orch = make_orch()
        r = run_session(orch, ["What is the status of ORD-025?", "Tell me about PROD-002."])
        t1, t2 = r
        assert t1["active_order_id"] == "ORD-025"  # T1: order set
        assert t2["active_product_id"] == "PROD-002", \
            f"active_product_id must be PROD-002 after product query. Got: {t2['active_product_id']}"
        assert t2["active_order_id"] is None, \
            f"active_order_id must be cleared after product switch. Got: {t2['active_order_id']}"

    def test_order_slot_set_after_explicit_order_query(self):
        """After 'What is the status of ORD-025?', active_order_id must be ORD-025."""
        orch = make_orch()
        r = run_session(orch, ["What is the status of ORD-025?"])
        assert r[0]["active_order_id"] == "ORD-025"
        assert r[0]["active_product_id"] is None


# ---------------------------------------------------------------------------
# Test Groups A–J: Behavioral Requirements from Prompt
# ---------------------------------------------------------------------------

class TestGroupA_ExplicitProduct:
    def test_explicit_product_query(self):
        orch = make_orch()
        r = run_session(orch, ["What is the price of PROD-002?"])
        assert is_product(r[0]["content"]), f"Must be product. Got: {r[0]['content'][:100]}"


class TestGroupB_ExplicitOrder:
    def test_explicit_order_query(self):
        orch = make_orch()
        r = run_session(orch, ["What is the status of ORD-025?"])
        assert is_order(r[0]["content"]), f"Must be order. Got: {r[0]['content'][:100]}"


class TestGroupC_ProductAfterOrder:
    def test_product_after_order(self):
        orch = make_orch()
        r = run_session(orch, ["What is the status of ORD-025?", "What is the price of PROD-002?"])
        assert is_order(r[0]["content"]),   "T1 must be order"
        assert is_product(r[1]["content"]), f"T2 must be product. Got: {r[1]['content'][:100]}"


class TestGroupD_OrderAfterProduct:
    def test_order_after_product(self):
        orch = make_orch()
        r = run_session(orch, ["What is the price of PROD-002?", "What is the status of ORD-025?"])
        assert is_product(r[0]["content"]), "T1 must be product"
        assert is_order(r[1]["content"]),   f"T2 must be order. Got: {r[1]['content'][:100]}"


class TestGroupE_ProductImplicitFollowUp:
    def test_its_price_after_product_no_prior_context(self):
        """Fresh session: 'Tell me about PROD-002.' then 'What is its price?' must return product."""
        orch = make_orch()
        r = run_session(orch, ["Tell me about PROD-002.", "What is its price?"])
        assert is_product(r[0]["content"]), "T1 must be product"
        assert is_product(r[1]["content"]), f"T2 'What is its price?' must be product. Got: {r[1]['content'][:120]}"

    def test_its_price_after_product_preceded_by_order(self):
        """THE KEY FIX: ORD-025 → PROD-002 → 'What is its price?' must return PRODUCT."""
        orch = make_orch()
        r = run_session(orch, [
            "What is the status of ORD-025?",
            "Tell me about PROD-002.",
            "What is its price?",
        ])
        assert is_order(r[0]["content"]),   "T1 must be order"
        assert is_product(r[1]["content"]), "T2 must be product"
        assert is_product(r[2]["content"]), \
            f"T3 'What is its price?' must return PRODUCT (was the known failure). Got: {r[2]['content'][:120]}"
        assert "ORD-025" not in r[2]["content"] or "Price" in r[2]["content"], \
            "T3 must not return ORD-025 order details"


class TestGroupF_ProductImplicitAvailability:
    def test_is_it_available_after_product(self):
        orch = make_orch()
        r = run_session(orch, [
            "What is the status of ORD-025?",
            "Tell me about PROD-002.",
            "Is it available?",
        ])
        assert is_product(r[2]["content"]), \
            f"T3 'Is it available?' must be product. Got: {r[2]['content'][:120]}"


class TestGroupG_ProductMRP:
    def test_explicit_mrp_query_returns_product(self):
        """Explicit MRP query must return correct product."""
        orch = make_orch()
        r = run_session(orch, ["What is the price of PROD-002?"])
        assert is_product(r[0]["content"]), "Explicit price query must return product"
        assert "32,999" in r[0]["content"] or "MRP" in r[0]["content"], \
            f"Must contain MRP info. Got: {r[0]['content'][:120]}"


class TestGroupH_OrderImplicitCarrier:
    def test_carrier_follow_up_after_order(self):
        orch = make_orch()
        r = run_session(orch, ["What is the status of ORD-025?", "What carrier is handling it?"])
        assert is_order(r[0]["content"]), "T1 must be order"
        t2 = r[1]["content"]
        assert is_order(t2) or "XpressBees" in t2, \
            f"T2 carrier follow-up must reference ORD-025. Got: {t2[:120]}"


class TestGroupI_OrderTotal:
    def test_total_follow_up_after_order(self):
        orch = make_orch()
        r = run_session(orch, ["What is the status of ORD-025?", "What is its total?"])
        assert is_order(r[0]["content"]), "T1 must be order"
        assert is_order(r[1]["content"]), \
            f"T2 'What is its total?' must return order. Got: {r[1]['content'][:120]}"


class TestGroupJ_Security:
    def test_denied_order_does_not_become_context(self):
        """ORD-003 (foreign) → denied → 'What is its status?' must NOT return ORD-003 data."""
        orch = make_orch()
        conv_id = fresh_id()
        r1 = orch.process_message("What is the status of ORD-003?", customer_id="CUST-001", conversation_id=conv_id)
        assert is_denied(r1.content), "T1 must be Access Denied"
        ctx = context_manager.get_or_create(conv_id)
        assert ctx.active_order_id != "ORD-003", \
            f"ORD-003 must not be persisted after denial. Got: {ctx.active_order_id}"

        r2 = orch.process_message("What is its status?", customer_id="CUST-001", conversation_id=conv_id)
        assert "ORD-003" not in r2.content or is_denied(r2.content), \
            f"T2 must not leak ORD-003 data. Got: {r2.content[:120]}"


# ---------------------------------------------------------------------------
# Critical Context Scenarios from Prompt
# ---------------------------------------------------------------------------

class TestCriticalScenarios:
    def test_scenario_1_ord_prod_implicit(self):
        """ORD → PROD → implicit price: must return ORDER, PRODUCT, PRODUCT."""
        orch = make_orch()
        r = run_session(orch, [
            "What is the status of ORD-025?",
            "Tell me about PROD-002.",
            "What is its price?",
        ])
        assert is_order(r[0]["content"]),   f"S1 T1: order. Got: {r[0]['content'][:80]}"
        assert is_product(r[1]["content"]), f"S1 T2: product. Got: {r[1]['content'][:80]}"
        assert is_product(r[2]["content"]), f"S1 T3: product (THE KEY FIX). Got: {r[2]['content'][:120]}"

    def test_scenario_2_prod_ord_prod_explicit(self):
        """PROD → ORD → PROD (explicit ID): must return PRODUCT, ORDER, PRODUCT."""
        orch = make_orch()
        r = run_session(orch, [
            "What is the price of PROD-002?",
            "What is the status of ORD-025?",
            "What is the price of PROD-002?",
        ])
        assert is_product(r[0]["content"]), f"S2 T1: product. Got: {r[0]['content'][:80]}"
        assert is_order(r[1]["content"]),   f"S2 T2: order. Got: {r[1]['content'][:80]}"
        assert is_product(r[2]["content"]), f"S2 T3: product. Got: {r[2]['content'][:120]}"

    def test_scenario_3_long_chain(self):
        """PROD-001 → SHIPMENT → PROD-002 → implicit price: T4 must be PROD-002."""
        orch = make_orch()
        r = run_session(orch, [
            "Tell me about PROD-001.",
            "Where is my shipment?",
            "Tell me about PROD-002.",
            "What is its price?",
        ])
        assert is_product(r[0]["content"]),   f"S3 T1: product. Got: {r[0]['content'][:80]}"
        assert is_shipment(r[1]["content"]),  f"S3 T2: shipment. Got: {r[1]['content'][:80]}"
        assert is_product(r[2]["content"]),   f"S3 T3: product. Got: {r[2]['content'][:80]}"
        assert is_product(r[3]["content"]),   f"S3 T4: product (implicit follow-up). Got: {r[3]['content'][:120]}"
        assert "AeroTab" in r[3]["content"] or "PROD-002" in r[3]["content"] or "27,499" in r[3]["content"], \
            f"S3 T4 must reference PROD-002. Got: {r[3]['content'][:120]}"

    def test_scenario_4_ord_prod_availability(self):
        """ORD → PROD → 'Is it available?': T3 must be PRODUCT."""
        orch = make_orch()
        r = run_session(orch, [
            "What is the status of ORD-025?",
            "Tell me about PROD-002.",
            "Is it available?",
        ])
        assert is_order(r[0]["content"]),   f"S4 T1: order. Got: {r[0]['content'][:80]}"
        assert is_product(r[1]["content"]), f"S4 T2: product. Got: {r[1]['content'][:80]}"
        assert is_product(r[2]["content"]), f"S4 T3: product. Got: {r[2]['content'][:120]}"

    def test_scenario_5_security_denied_then_shipment(self):
        """ORD-003 (denied) → 'Where is my shipment?': T2 must be CUST-001's own shipment."""
        orch = make_orch()
        r = run_session(orch, [
            "What is the status of ORD-003?",
            "Where is my shipment?",
        ], cust_id="CUST-001")
        assert is_denied(r[0]["content"]), f"S5 T1: must be denied. Got: {r[0]['content'][:80]}"
        t2 = r[1]["content"]
        assert not is_denied(t2), f"S5 T2: must NOT be denied. Got: {t2[:120]}"
        assert is_shipment(t2) or is_order(t2), f"S5 T2: must return own shipment. Got: {t2[:120]}"
        assert "ORD-003" not in t2, f"S5 T2: must not reference ORD-003. Got: {t2[:120]}"


# ---------------------------------------------------------------------------
# Regression: Phase 13.2.2 key scenarios must still pass
# ---------------------------------------------------------------------------

class TestPhase1322Regression:
    def test_prod_ord_prod_explicit_t3(self):
        """Phase 13.2.2 SC1: PROD → ORD → PROD (explicit) must still return PRODUCT at T3."""
        orch = make_orch()
        r = run_session(orch, [
            "What is the price of PROD-002?",
            "What is the status of ORD-025?",
            "What is the price of PROD-002?",
        ])
        assert is_product(r[2]["content"]), \
            f"13.2.2 regression: T3 must be product. Got: {r[2]['content'][:120]}"

    def test_prod_shipment_prod(self):
        orch = make_orch()
        r = run_session(orch, [
            "Is PROD-001 available?",
            "Where is my shipment?",
            "Tell me about PROD-001",
        ])
        assert is_product(r[0]["content"]),  "T1: product"
        assert is_shipment(r[1]["content"]), "T2: shipment"
        assert is_product(r[2]["content"]),  "T3: product"

    def test_order_then_product_explicit(self):
        orch = make_orch()
        r = run_session(orch, ["What is the status of ORD-025?", "What is the price of PROD-002?"])
        assert is_order(r[0]["content"]),   "T1: order"
        assert is_product(r[1]["content"]), "T2: product"

    def test_product_followup_fresh_session(self):
        """Phase 13.2.2 TestGroup8: product context follow-up in fresh session."""
        orch = make_orch()
        r = run_session(orch, ["Tell me about PROD-002.", "What is its price?"])
        assert is_product(r[0]["content"]), "T1: product"
        assert is_product(r[1]["content"]), "T2: product follow-up via context"

    def test_order_followup(self):
        orch = make_orch()
        r = run_session(orch, ["What is the status of ORD-025?", "What carrier is handling it?"])
        assert is_order(r[0]["content"]),  "T1: order"
        t2 = r[1]["content"]
        assert is_order(t2) or "XpressBees" in t2, "T2: order follow-up"

    def test_unauthorized_slot_not_persisted(self):
        orch = make_orch()
        conv_id = fresh_id()
        orch.process_message("What is the status of ORD-003?", customer_id="CUST-001", conversation_id=conv_id)
        ctx = context_manager.get_or_create(conv_id)
        assert ctx.active_order_id != "ORD-003", "ORD-003 must not be persisted"

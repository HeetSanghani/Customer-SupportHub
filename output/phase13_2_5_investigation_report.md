# Phase 13.2.5 — Implicit Contextual Reference Resolution Investigation Report

**Final Status**: `ROOT_CAUSE_IDENTIFIED`

---

## 1. Executive Summary

This strict read-only investigation investigated why implicit contextual reference queries (e.g. `"What is its price?"`, `"Is it available?"`) fail during manual browser testing, resolving to prior order context (`ORD-025`) instead of current product context (`PROD-002`).

The investigation confirmed that while Phase 13.2.4 successfully isolated explicit entities for `IntentClassifier.classify()`, four specific architectural defects in `LLMIntentClassifier`, `AIRouter`, and `AIOrchestrator` cause `active_order_id` to remain in context or prevent `active_product_id` from being saved during live multi-turn interactions.

---

## 2. Reproduction of Observed Browser Behavior

| Turn | Query | Expected Entity | Actual Entity | Status |
| :---: | :--- | :--- | :--- | :---: |
| 1 | `"What is the status of ORD-025?"` | `ORD-025` | `ORD-025` | PASS |
| 2 | `"Tell me about PROD-002."` | `PROD-002` | `PROD-002` | PASS |
| 3 | `"What is its price?"` | `PROD-002` | **`ORD-025`** | **FAIL** |
| 4 | `"Is it available?"` | `PROD-002` | **`ORD-025`** | **FAIL** |
| 5 | `"What is the status of ORD-025?"` | `ORD-025` | `ORD-025` | PASS |
| 6 | `"What is the price of PROD-002?"` | `PROD-002` | `PROD-002` | PASS |
| 7 | `"What is the status of ORD-003?"` | `ACCESS DENIED` | `ACCESS DENIED` | PASS |
| 8 | `"Where is my shipment?"` | `SHIP-025` | `SHIP-025` | PASS |

---

## 3. Four Confirmed Root Cause Pathways

### Root Cause 1: `LLMIntentClassifier` Omits `explicit_entities` Field
- **File**: `supporthub-ai-architecture/ai/intent.py` (lines 435–443)
- **Function**: `LLMIntentClassifier.classify()`
- **Mechanism**: `LLMIntentClassifier.classify()` constructs and returns `IntentResult(...)` without populating `explicit_entities`. It defaults to `{}`.
- **Effect**: In `AIOrchestrator.process_message()`, line 82 sets `_explicit_entities = route_decision.intent.explicit_entities`, which evaluates to `{}`. Line 169 calls `update_slots_domain_aware({})`. `has_any_explicit` evaluates to `False`, so `update_slots_domain_aware` returns without saving `active_product_id = PROD-002` or clearing `active_order_id = ORD-025`.

### Root Cause 2: `AIRouter` and `LLMIntentClassifier` Discard Product Slots
- **File**: `supporthub-ai-architecture/ai/router.py` (line 87) & `ai/intent.py` (lines 384–448)
- **Functions**: `AIRouter.route()`, `LLMIntentClassifier.classify()`
- **Mechanism**: `AIRouter.route()` extracts `context_slots.get("order_id")` and passes `active_order_id` ONLY to `LLMIntentClassifier.classify()`. It discards `product_id`, `return_id`, and `refund_id`.
- **Effect**: `LLMIntentClassifier` has no parameter or prompt placeholder for `active_product_id`. On fallback (such as Gemini API 429 rate limit or error), it calls `self.fallback.classify(query, context_slots={"active_order_id": active_order_id})`, omitting `product_id`.

### Root Cause 3: `RAG` Route Bypass in `AIOrchestrator`
- **File**: `supporthub-ai-architecture/ai/orchestrator.py` (lines 113–130)
- **Function**: `AIOrchestrator.process_message()`
- **Mechanism**: Queries routed to `RouteType.RAG` (e.g. `"What is the return policy for PROD-002?"`) execute RAG search and return immediately without calling `ctx.update_slots_domain_aware()`.
- **Effect**: If Turn 2 is a RAG query, `PROD-002` is never saved in context, leaving `ORD-025` active.

### Root Cause 4: Absence of Formal Contextual Reference Engine
- **File**: System-wide
- **Mechanism**: There is no dedicated pronoun/reference resolution engine in the architecture. Implicit queries like `"What is its price?"` produce `explicit_entities = {}` and rely entirely on whatever active slot is stored in `ConversationContext`.
- **Effect**: When `active_order_id` is left in context due to Pathways 1, 2, or 3, implicit queries default to `active_order_id`.

---

## 4. Primary Question Answer

**Question**: Is `"What is its price?"` interpreted as Product, Order, or Fallback?  
**Answer**: **C (No reference resolution exists and the system falls back to available context slot)**, combined with **Pathways 1–3 where `active_order_id` was retained in context**.

---

## 5. Security & Authorization Analysis

- Zero-trust security gates (`_check_ownership()` and `security_validator`) remain 100% effective.
- Attempting implicit queries after an unauthorized order inquiry (e.g. `ORD-003`) returns `"unable to locate requested record"` and **never leaks foreign customer data**.

---

## 6. Test Coverage Gap Analysis

Phase 13.2.4 tests passed `32/32` because they ran with `use_llm=False` directly on `IntentClassifier` for `STRUCTURED` routes. They did not test `LLMIntentClassifier` return structures or `RAG` route slot update bypasses.

---

## 7. Mandatory Verification of Git Cleanliness

`git status` audit confirms **ZERO modifications** to production code, tests, or database files.

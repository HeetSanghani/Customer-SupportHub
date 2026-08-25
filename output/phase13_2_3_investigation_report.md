# Phase 13.2.3 — Contextual Reference Resolution Investigation Report

**Final Investigation Status**: `ROOT_CAUSE_IDENTIFIED`  
**Investigation Mode**: `READ-ONLY — ZERO PRODUCTION/TEST/DATABASE MODIFICATIONS`  
**Git Status**: No tracked files modified during investigation  

---

## 1. Executive Summary

Phase 13.2.3 investigated a new manual validation failure discovered after Phase 13.2.2 was implemented: the implicit follow-up query `"What is its price?"` after `"Tell me about PROD-002."` returned the ORD-025 order response instead of the PROD-002 product response.

The root cause was identified with full execution trace evidence. It is a secondary design gap in Phase 13.2.2's implementation, **not** a regression of the explicit entity isolation fix.

The bug is located in `ai/orchestrator.py` line 79, where `_explicit_entities` is assigned from `route_decision.intent.entities` — the **merged** (explicit + context-inherited) dictionary — instead of the **explicit-only** entities. This causes `update_slots_domain_aware()` to receive both `product_id` (explicit) and `order_id` (context-inherited) simultaneously, and since both `if new_product_id:` and `if new_order_id:` blocks execute independently, the order block overwrites and clears the product slot last.

---

## 2. Exact Root Cause

> **`AIOrchestrator.process_message()` at line 79 assigns `_explicit_entities = route_decision.intent.entities`, which is the MERGED entity dictionary (explicit + context-inherited). `update_slots_domain_aware()` receives both `product_id: PROD-002` and `order_id: ORD-025`. Its `if new_product_id:` block sets `active_product_id = PROD-002` and clears `active_order_id`. But its independent `if new_order_id:` block then re-sets `active_order_id = ORD-025` and clears `active_product_id = None`. The product slot is destroyed. The subsequent implicit follow-up finds only `order_id` in context, triggering ORDER_INQUIRY.**

---

## 3. Detailed Execution Trace (Failure Path)

**Precondition**: `active_order_id = ORD-025` from an earlier order turn in the same session.

### Turn 2: `"Tell me about PROD-002."`

| Step | Location | Input | Output |
| :--- | :--- | :--- | :--- |
| Entity extraction | `classify()` | query text | `explicit_entities = {product_id: PROD-002}` |
| Context merging | `classify()` | slots | `context_entities = {order_id: ORD-025}` |
| Merged entities | `classify()` | both | `entities = {order_id: ORD-025, product_id: PROD-002}` → stored on `IntentResult.entities` |
| Orchestrator line 79 | `process_message()` | `IntentResult.entities` | `_explicit_entities = {order_id: ORD-025, product_id: PROD-002}` ← **WRONG: merged** |
| Slot update — product branch | `update_slots_domain_aware()` | `new_product_id = PROD-002` | `active_product_id = PROD-002`, `active_order_id = None` ✅ |
| Slot update — order branch | `update_slots_domain_aware()` | `new_order_id = ORD-025` | `active_order_id = ORD-025`, **`active_product_id = None`** ❌ |
| **Context after Turn 2** | `ConversationContext` | — | `active_product_id = None`, `active_order_id = ORD-025` |

### Turn 3: `"What is its price?"`

| Step | Value |
| :--- | :--- |
| `explicit_entities` | `{}` (no regex match) |
| `context_entities` | `{order_id: ORD-025}` |
| `_context_only_order` | `True` |
| `classify()` result | `ORDER_INQUIRY` |
| Tool called | `get_order(ORD-025)` |
| Response | Order ORD-025 — **WRONG** ❌ |

---

## 4. Why Phase 13.2.2 Tests Passed

`TestGroup8ProductFollowUp.test_product_follow_up_inherits_context` ran:
```
Turn 1: "Tell me about PROD-002."
Turn 2: "What is its price?"
```
in a **fresh conversation with no prior order turn**. `active_order_id = None` throughout, so `update_slots_domain_aware` only saw `product_id` in the merged dict and correctly set `active_product_id = PROD-002`. The failure precondition (active order context before the product turn) was absent from all Phase 13.2.2 tests.

---

## 5. Security Impact

- **No data leakage**: `_check_ownership()` remains active and correctly blocks any foreign customer data.
- **SC10 verified**: After CUST-001 is denied ORD-003, `revert_slots()` correctly restores `active_order_id = None`. Subsequent implicit references return no-data, not foreign customer data.
- **No security boundary violation.**

---

## 6. Scenario Matrix Summary

| Scenario | Query Sequence | Expected | Actual | Status |
| :---: | :--- | :--- | :--- | :---: |
| SC1 | ORD-025 → PROD-002 → `"What is its price?"` | Product | Order ORD-025 | ❌ |
| SC2 | ORD-025 → PROD-002 → `"Is it available?"` | Product | Order ORD-025 | ❌ |
| SC3 | ORD-025 → PROD-002 → `"What is its MRP?"` | Product | Order ORD-025 | ❌ |
| SC4 | ORD-025 → `"What carrier is handling it?"` | Order | Order ORD-025 | ✅ |
| SC5 | ORD-025 → `"What is its total?"` | Order | Order ORD-025 | ✅ |
| SC6 | ORD-025 → PROD-002 → `"Price of PROD-002?"` | Product | Product PROD-002 | ✅ |
| SC7 | ORD-025 → ORD-025 | Order | Order ORD-025 | ✅ |
| SC8 | ORD-025 → PROD-002 → `"What is the price?"` | Product | Order ORD-025 | ❌ |
| SC9 | PROD-002 → `"What about it?"` | Product | No-data fallback | ⚠️ |
| SC10 | ORD-003 (denied) → `"What is its status?"` | Denied → No data | Denied → No data | ✅ |

---

## 7. Recommended Remediation

**File**: `ai/orchestrator.py` — change line 79  
**File**: `ai/intent.py` — add `explicit_entities` field to `IntentResult`

**Approach A** (recommended):
1. Add `explicit_entities: Dict[str, Any] = field(default_factory=dict)` to `IntentResult`.
2. In `classify()`, assign `explicit_entities` before returning.
3. Change orchestrator line 79: `_explicit_entities = route_decision.intent.explicit_entities`

**Approach B** (simpler, no dataclass change):
1. Change orchestrator line 79: `_explicit_entities = intent_classifier.extract_entities(query)`

`update_slots_domain_aware()` itself does **not** need to change — its logic is correct when given the right input.

---

**Investigation Status**: `ROOT_CAUSE_IDENTIFIED`

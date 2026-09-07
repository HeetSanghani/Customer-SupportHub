# Subquestion Decomposition Documentation

## Overview
Subquestion decomposition isolates multiple intents within a single user message while preserving operational phrases (such as "delivered but not received").

## Pattern Rules
`_hybrid_split` in `app/ai/graph/nodes.py` uses heuristic pattern matching to split:
- Semicolons (`;) and newlines (`\n`).
- Conjunctions linking status requests (`order, payment and shipment`, `order status and payment status`).
- Human handoff requests (`connect me to a human`).

## Max Bounds & Guardrails
- **`MAX_SUB_QUESTIONS`**: 5 subquestions maximum per turn to prevent performance degradation or infinite graph loops.
- **Entity Propagation**: Entities extracted from the full query (such as `order_id` or `product_id`) propagate to subquestions lacking explicit entity IDs.

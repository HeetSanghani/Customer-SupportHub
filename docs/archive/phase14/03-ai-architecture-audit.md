# 03 — supporthub-ai-architecture Audit

## Overview
Detailed audit of the core AI architecture repository (`supporthub-ai-architecture`).

## Component Breakdown
1. **`ai/router.py`**:
   - `AIRouter`: 5-tier hybrid routing hierarchy (1. Security Guard -> 2. Escalation Guard -> 3. Hybrid Engine -> 4. RAG Knowledge -> 5. Structured Data).
2. **`ai/intent.py`**:
   - `RegexIntentClassifier` & `LLMIntentClassifier`: Pattern-based and LLM-driven intent classification.
3. **`ai/orchestrator.py`**:
   - `AIOrchestrator`: Main entry point. Handles `process_message()`, context updates, explicit vs inherited entity slot validation, tool execution, security authorization, and response synthesis.
4. **`ai/context.py`**:
   - `ConversationContext`: In-memory multi-turn session tracking (`active_customer_id`, `active_order_id`, `active_product_id`, `active_shipment_id`). Implements turn-based slot TTL and context isolation.
5. **`ai/tools.py`**:
   - `ToolRegistry`: Registers business domain tools (`get_customer`, `get_order`, `get_product`, `get_payment`, `get_shipment`, `get_return`, `get_refund`).
6. **`ai/security.py`**:
   - `AISecurityGuard`: Zero-trust security checker enforcing customer ownership boundaries and prompt injection defenses.
7. **`data_access/`**:
   - `MySQLBusinessDB`: PyMySQL connection pool manager for MySQL `supporthub_business` database.
   - `MySQLRepository`: Parameterized SQL query executor.
   - Service classes (`CustomerService`, `OrderService`, `ProductService`, `PaymentService`, `ShipmentService`, `ReturnService`, `RefundService`).
8. **`integration/adapters/shopkart.py`**:
   - `ShopKartBusinessDataAdapter`: Implements standard business data adapter contract.

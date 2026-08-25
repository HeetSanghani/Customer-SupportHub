# SupportHub Phase 11 — Live Chat AI Integration Implementation Plan

**Document Version:** 1.0.0  
**Status:** Ready for Implementation  
**Author:** AI Integration Pair Programmer  
**Target:** Live Chat Channel (Website) Only  

---

## 1. Implementation Overview & Objectives

The primary objective of Phase 11 is to integrate the validated `supporthub-ai-architecture` into SupportHub's **Website Live Chat** channel without regressing any existing functionality or affecting non-Live Chat channels.

### Key Milestones:
1. **Develop `LiveChatAIAdapter`**: Create a clean service in `app/services/ai/live_chat_adapter.py` that implements normalization, orchestration, persistence, escalation management, and WebSocket broadcasting.
2. **Hook WebSocket Chat Router**: Connect `app/routers/ws/chat.py` to `LiveChatAIAdapter` for all customer Live Chat interactions.
3. **Implement End-to-End Test Suite**: Create `tests/test_live_chat_ai_e2e.py` covering product, order, payment, return, security, multi-turn, and escalation scenarios.
4. **Execute Full Test Suite**: Verify 100% test pass rate across both SupportHub backend (all 70+ tests) and AI Architecture (all 67 tests).
5. **Produce Validation Report**: Document final quality metrics, latency, and test findings in `docs/phase11/05-validation-report.md`.

---

## 2. Detailed File Modifications & New Additions

### [NEW] `supporthub/backend/app/services/ai/live_chat_adapter.py`
- **Class**: `LiveChatAIAdapter`
- **Methods**:
  - `__init__(self, tenant_id: str = "shopkart")`: Initializes adapter and AI orchestrator instance.
  - `async def process_live_chat_message(self, session: AsyncSession, ticket_id: str, message_body: str, use_llm: bool = False)`: Main execution method.
  - `_map_to_normalized_inbound(...)`: Converts SupportHub models to `NormalizedInboundMessage`.
  - `_handle_escalation(...)`: Updates `Ticket.status = TicketStatus.escalated`, sets priority and category, records handoff.
  - `_handle_resolution(...)`: Detects closure/resolution, updates `Ticket.status = TicketStatus.resolved`, triggers CSAT delivery.
  - `_broadcast_ai_events(...)`: Dispatches `message`, `inbox_update`, and `ticket_update` events via `manager`.

### [MODIFY] `supporthub/backend/app/routers/ws/chat.py`
- **Change**: Replace legacy inline `process_ai_reply` logic with `LiveChatAIAdapter().process_live_chat_message(ticket_id, body)`.
- **Safety**: WhatsApp and Instagram outbound forwarders remain completely unchanged.

### [NEW] `supporthub/backend/tests/test_live_chat_ai_e2e.py`
- **Test Cases**:
  - `test_live_chat_product_inquiry`: Validates ShopKart product query resolution.
  - `test_live_chat_order_status`: Validates order tracking tool execution.
  - `test_live_chat_payment_inquiry`: Validates payment detail retrieval.
  - `test_live_chat_return_policy_rag`: Validates policy RAG response.
  - `test_live_chat_security_prompt_injection`: Validates injection denial.
  - `test_live_chat_caller_ownership_security`: Validates cross-customer data privacy.
  - `test_live_chat_human_escalation`: Validates automatic ticket status mutation to `escalated`.
  - `test_live_chat_multi_turn_continuity`: Validates slot and context retention across turns.

---

## 3. Risk Assessment & Mitigation Strategies

| Potential Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| **Import / Path Resolution Issues** | Medium | Use robust `sys.path` injection in `live_chat_adapter.py` to ensure seamless loading of `supporthub-ai-architecture`. |
| **Async Session Conflicts** | Low | Instantiate a dedicated `AsyncSessionLocal()` inside background task to prevent event loop blocking or session collision. |
| **Regression in Non-Live Chat Channels**| High | Strict scoping: Zero code edits to WhatsApp, Instagram, Facebook, or Email webhook routes. |
| **WebSocket Broadcast Failure** | Low | Defensive `try...except` around broadcast calls to ensure message persistence succeeds even if a socket disconnects. |

---

## 4. Rollback Strategy

1. If any issues arise, the changes are isolated to `app/services/ai/live_chat_adapter.py` and the `ws/chat.py` trigger call.
2. Git checkpoint ensures instant revert to `0306135` if required.

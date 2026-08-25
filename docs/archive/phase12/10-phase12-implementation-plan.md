# 10 — Sub-Phase Implementation Roadmap

## Executive Summary
This document outlines the recommended step-by-step sub-phase implementation order for executing Phase 12 implementation after explicit user authorization.

---

## Proposed Sub-Phase Breakdown

```
Phase 12.1: Identity Model Linkage (User.customer_id)
    │
    ▼
Phase 12.2: Live Chat Adapter Hardening (Trusted Customer Context)
    │
    ▼
Phase 12.3: WebSocket Room Ownership Guard (Anti-IDOR Protection)
    │
    ▼
Phase 12.4: Data Access & Ownership Check Extension (Shipment Resolution)
    │
    ▼
Phase 12.5: Anonymous vs Authenticated Behavior Enforcement
    │
    ▼
Phase 12.6: Frontend Protected Route & Login UI Integration
    │
    ▼
Phase 12.7: End-to-End Security Validation & Regression Suite Execution
```

---

## Detailed Sub-Phase Specifications

### Phase 12.1 — Identity Model Linkage
- Formalize `customer_id` relationship on `User` model.
- Populate synthetic customer mapping in database seed script (`clean_and_seed.py`).

### Phase 12.2 — Live Chat Adapter Hardening
- Refactor `LiveChatAIAdapter._resolve_customer_id()` to extract trusted `user.customer_id` directly from authenticated session.
- Disallow unverified email fallback matching.

### Phase 12.3 — WebSocket Room Ownership Guard
- Update `websocket_chat()` in `app/routers/ws/chat.py` to assert `ticket.customer_id == user.id` (or `user.role in (agent, admin)`).
- Close unauthorized WebSocket connection attempts with error code `4003`.

### Phase 12.4 — Data Access & Ownership Extension
- Extend `AIOrchestrator._check_ownership()` to trace `Shipment.order_id` → `Order.customer_id`.
- Ensure all customer-sensitive tools enforce pre-synthesis authorization checks.

### Phase 12.5 — Anonymous Query Handling
- Update `AIRouter` and `LiveChatAIAdapter` to intercept order/payment/shipment queries from `GUEST` users.
- Return structured prompt: *"Please log in to your account to view your order, payment, or shipment details."*

### Phase 12.6 — Frontend Auth UX Integration
- Protect live chat interface with `AuthGuard`.
- Pass JWT token in WebSocket connection string `ws://.../ws/chat/{ticket_id}?token={token}`.

### Phase 12.7 — Security & Regression Suite
- Rerun 78 backend tests, 67 AI tests, 8 Live Chat E2E tests, and 35 validation scenarios.
- Execute new cross-customer boundary & security test suite.

# 12 — Final Phase 12 Architecture Blueprint

## Executive Summary
This document provides the definitive architectural blueprint for Phase 12 Customer Authentication & Personalized AI Support.

---

## Complete End-to-End System Architecture

```
                                  CUSTOMER
                                     │
                                     ▼
                              LOGIN / REGISTER
                        (POST /api/v1/auth/login)
                                     │
                                     ▼
                            AUTHENTICATION JWT
                        (Bearer Token / ?token=)
                                     │
                                     ▼
                              USER IDENTITY
                        (User.id / User.role)
                                     │
                                     ▼
                            CUSTOMER IDENTITY
                     (User.customer_id e.g. CUST-001)
                                     │
                                     ▼
                           LIVE CHAT WEBSOCKET
                        (/ws/chat/{ticket_id})
                      [Room Ownership Verified]
                                     │
                                     ▼
                                AI ROUTER
                            (ai/router.py)
                                     │
      ┌──────────────────────────────┼──────────────────────────────┐
      ▼                              ▼                              ▼
 CATEGORY 1: STRUCTURED     CATEGORY 2: POLICY RAG        CATEGORY 5: ESCALATION
  - get_customer_orders       - Vector Search KbArticles     - Escalation Evaluator
  - get_order / get_payment   - Policy Guidance              - Mutate Ticket Priority
  - get_shipment / get_return                                - WebSocket Agent Broadcast
      │                              │                              │
      ▼                              │                              │
OWNERSHIP SECURITY GATEWAY           │                              │
  - caller_id == owner_id?           │                              │
      │                              │                              │
      └──────────────────────────────┼──────────────────────────────┘
                                     ▼
                          RESPONSE SYNTHESIZER
                       (Deterministic / Gemini)
                                     │
                                     ▼
                            REAL-TIME RESPONSE
                         (Broadcast to WebSocket)
                                     │
                                     ▼
                                  CUSTOMER
```

---

## Architectural Decision Records (ADRs)

1. **ADR-01: Reuse Existing Authentication System**: SupportHub's existing OAuth2/JWT implementation (`app/routers/auth.py` and `app/dependencies.py`) will be reused without creating a secondary authentication system.
2. **ADR-02: Server-Side Customer Identity Resolution**: Customer identity is extracted strictly from the validated server-side JWT session (`User.customer_id`), rendering identity spoofing via chat prompts impossible.
3. **ADR-03: Pre-Synthesis Authorization Gate**: Ownership verification (`_check_ownership`) occurs before any structured entity snippet is passed to the response synthesizer or LLM, ensuring authorization is never delegated to the AI model.
4. **ADR-04: WebSocket Room Guarding**: Room-level ownership validation (`ticket.customer_id == user.id`) is enforced at the WebSocket handshake to eliminate room hijacking (IDOR).

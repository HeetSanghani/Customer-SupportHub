# SupportHub AI Integration Layer (`integration/`)

## 1. Overview
The `integration/` package defines the contract boundaries, adapters, and security guards required to integrate the **SupportHub AI Architecture Sandbox** with the production **Customer-SupportHub** backend without requiring invasive modifications.

```
+-------------------------------------------------------------------------------+
|                       EXISTING SUPPORTHUB APPLICATION                         |
|   (Webhooks: WhatsApp, Instagram, Messenger, Email, WebChat | Ticketing CRM) |
+-------------------------------------------------------------------------------+
                                       |
                                       v
+-------------------------------------------------------------------------------+
|                      INTEGRATION BOUNDARY & NORMALIZATION                     |
|   - NormalizedInboundMessage: Unified schema across all 5 channels            |
|   - CustomerIdentity & AuthContext: Scoped identity and RBAC claims           |
|   - TenantSecurityGuard: Absolute multi-tenant isolation boundary             |
+-------------------------------------------------------------------------------+
                                       |
                                       v
+-------------------------------------------------------------------------------+
|                         SUPPORTHUB AI ARCHITECTURE CORE                       |
|   (Security Gateway -> Intent -> Deterministic Router -> Tools/RAG -> LLM)   |
+-------------------------------------------------------------------------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
+------------------------------------+   +------------------------------------+
|        NORMALIZED AI RESULT        |   |       HUMAN TICKET HANDOFF         |
|   - Grounded Response Text         |   |   - Ticket Status -> Escalated     |
|   - Policy / Article Citations     |   |   - Handoff Dossier & Priority     |
|   - Telemetry & Confidence         |   |   - Assigned Agent / Department    |
+------------------------------------+   +------------------------------------+
                   |                                       |
                   v                                       v
+------------------------------------+   +------------------------------------+
|    OUTBOUND CHANNEL DISPATCH       |   |      AGENT DASHBOARD / INBOX       |
|    (WhatsApp, IG, FB, Email, Web)  |   |      (SupportHub Ticket Detail)    |
+------------------------------------+   +------------------------------------+
```

---

## 2. Directory Architecture

```
integration/
├── contracts/               # Typed data contracts decoupling AI core from DB/HTTP
│   ├── customer.py          # Customer identity and authentication state
│   ├── conversation.py      # Conversation turn and session containers
│   ├── message.py           # Inbound message normalization across 5 channels
│   ├── ticket.py            # Support ticket model & escalation handoff payload
│   ├── business_data.py     # Business data access contract (Orders, Products, etc.)
│   ├── rag.py               # Multi-tenant RAG search contracts & citations
│   └── ai_result.py         # Standardized AI output format
│
├── security/
│   └── tenant_boundary.py   # TenantSecurityGuard enforcing multi-tenant isolation
│
└── adapters/
    ├── shopkart.py          # Adapter for audited ShopKart synthetic data
    └── mock_supporthub.py   # Mock SupportHub system for end-to-end integration tests
```

---

## 3. Core Philosophy & Invariants

1. **Channel Agnostic**: Inbound messages from WhatsApp, Instagram, Facebook Messenger, Email, and Website chat normalize to a uniform `NormalizedInboundMessage`.
2. **Strict Multi-Tenancy**: Every data query and RAG search is filtered by `tenant_id`. Cross-tenant queries raise `TenantIsolationViolationError`.
3. **Deterministic Escalation Handoff**: If an escalation trigger fires, autonomous AI handling halts, the ticket is transitioned to `escalated`, and a structured `TicketHandoffPayload` is emitted.

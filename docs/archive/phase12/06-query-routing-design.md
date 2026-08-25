# 06 — 5-Category Query Routing Design

## Executive Summary
This document specifies the design for classifying incoming customer queries into five primary processing categories with mandatory authorization rules.

---

## 1. Category Breakdown & Routing Logic

```
                                  INCOMING QUERY
                                        │
                                        ▼
                                   AI ROUTER
                                        │
    ┌────────────────┬──────────────────┼──────────────────┬────────────────┐
    ▼                ▼                  ▼                  ▼                ▼
CATEGORY 1       CATEGORY 2         CATEGORY 3         CATEGORY 4       CATEGORY 5
Customer Data    Policy RAG         General KB         Hybrid           Escalation
    │                │                  │                  │                │
Auth Required?   Auth Required?     Auth Required?     Auth Required?   Auth Required?
   YES               NO                 NO              PARTIAL            NO
    │                │                  │                  │                │
    ▼                ▼                  ▼                  ▼                ▼
Structured       Vector RAG         FAQ Search         Order Data       Human Queue
Tool Execution   Article Search     Quick Reply        + Policy RAG     Handoff
```

---

## 2. Category Specifications

### Category 1: Customer Data (Structured)
- **Examples**: *"Where is my order?"*, *"Show my recent payment"*, *"What items did I buy?"*
- **Auth Requirement**: **MANDATORY AUTHENTICATION**.
- **Data Source**: ShopKart Structured Database via `ToolRegistry` (`get_customer_orders`, `get_order`, `get_payment_by_order`, `get_shipment_by_order`).
- **Authorization**: Caller MUST match resource owner ID (`owner_id == caller_customer_id`).

### Category 2: Company Policy (RAG)
- **Examples**: *"What is your return policy?"*, *"How long does refund processing take?"*, *"What is the warranty period?"*
- **Auth Requirement**: Public / Unauthenticated allowed.
- **Data Source**: Vector Database RAG Pipeline (`KbArticle` embeddings).

### Category 3: General Knowledge / FAQ
- **Examples**: *"How do I reset my password?"*, *"What payment methods do you support?"*
- **Auth Requirement**: Public / Unauthenticated allowed.
- **Data Source**: Knowledge Base articles, FAQs, Quick Replies.

### Category 4: Hybrid (Structured Data + Policy RAG)
- **Examples**: *"Can I return the phone I bought in order ORD-001?"*, *"Is my order ORD-013 eligible for replacement?"*
- **Auth Requirement**: **MANDATORY AUTHENTICATION** for the structured portion (`ORD-001` order lookup & purchase date check), public for policy window evaluation (7-day return policy).
- **Data Source**: Order Service + Product Service + Policy RAG.

### Category 5: Sensitive / Urgent / Escalation
- **Examples**: *"I suspect unauthorized activity on my account"*, *"I want to speak to a human manager immediately"*, *"Payment charged twice"*
- **Auth Requirement**: Allowed for both guest and authenticated users.
- **Action**: Bypasses LLM generation, mutates ticket status to `escalated`, assigns priority (`urgent` / `high`), notifies agent queue via WebSocket.

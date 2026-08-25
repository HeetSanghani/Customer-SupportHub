# 05 — Authorization Boundary & Data Isolation Design

## Executive Summary
This document defines the strict cross-customer isolation boundaries required to prevent unauthorized data access across authenticated customers.

---

## 1. Core Authorization Rule

> [!IMPORTANT]
> **Strict Multi-Tenant Customer Isolation Rule**: Customer A (authenticated with `customer_id = CUST-001`) MUST NEVER be permitted to access, view, or modify any resource (Orders, Order Items, Payments, Shipments, Returns, Refunds, Profile Data) belonging to Customer B (`customer_id = CUST-002`), even if Customer A explicitly supplies Customer B's order ID, tracking number, or payment ID in their query.

---

## 2. Layered Authorization Architecture

```
                                USER QUERY
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │     1. AUTHENTICATION       │  Extract & verify JWT token
                     │   (app/dependencies.py)     │  Identify `caller_customer_id`
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │     2. QUERY ROUTER         │  Classify query category
                     │    (ai/router.py)           │  Determine if auth is required
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │     3. TOOL EXECUTION       │  Inject `caller_customer_id`
                     │    (ai/orchestrator.py)     │  Query structured database
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │     4. OWNERSHIP CHECK      │  `owner_id == caller_id` ?
                     │    (ai/security.py)         │  YES → Proceed to Synthesizer
                     └──────────────┬──────────────┘  NO  → SECURITY DENIAL
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │   5. RESPONSE SYNTHESIS     │  LLM receives ONLY authorized
                     │    (ai/response.py)         │  structured data snippet
                     └─────────────────────────────┘
```

---

## 3. Authorization Decision Matrix

| Query Type | Authentication Status | Resource Requested | Resource Owner | Action | Result |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **Return Policy** | Unauthenticated / Guest | RAG Article | N/A (Public) | ALLOW | Return policy content |
| **Own Order (`ORD-001`)** | Authenticated (`CUST-001`) | Order `ORD-001` | `CUST-001` | ALLOW | Return order details |
| **Other Order (`ORD-002`)**| Authenticated (`CUST-001`) | Order `ORD-002` | `CUST-002` | **DENY** | `SECURITY_DENIAL` |
| **Private Order (`ORD-001`)**| Unauthenticated / Guest | Order `ORD-001` | `CUST-001` | **DENY** | Prompt for Login |
| **Payment Status** | Authenticated (`CUST-001`) | Payment `PAY-002` | `CUST-002` | **DENY** | `SECURITY_DENIAL` |
| **Shipment Tracking** | Authenticated (`CUST-001`) | Shipment `SHIP-002` | `CUST-002` | **DENY** | `SECURITY_DENIAL` |

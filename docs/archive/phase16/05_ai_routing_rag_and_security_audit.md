# Phase 16 — AI Routing, RAG & Security Audit

## 1. Multi-Stage AI Pipeline Architecture

```
[ User Message ] ──> [ LiveChatAIAdapter ]
                          │
                          ▼
                     [ AIRouter ]
       ┌──────────────────┼──────────────────┐
       ▼                  ▼                  ▼
 [ STRUCTURED ]         [ RAG ]          [ HYBRID ]
(Order SQL Lookup)  (Policy Vector DB) (Combined Lookup)
       │                  │                  │
       └──────────────────┼──────────────────┘
                          ▼
                 [ ContextBuilder ]
                          │
                          ▼
                  [ ModelAdapter ] ──> [ ResponseParser ]
```

---

## 2. Intent Classification Categories

1. **STRUCTURED**: User requests order status, shipment tracking, payment history, returns, or refunds. Context builder executes isolated SQL queries bounded by `current_user.id`.
2. **RAG**: User asks general store policy or FAQ questions (e.g. return policy, shipping timelines). RAG engine performs pgvector cosine similarity search over `kb_articles`.
3. **HYBRID**: User asks policy questions contextualized by their own order (e.g. *"Can I return order ORD-025 based on your return policy?"*). System combines SQL lookup with RAG vector search.
4. **HUMAN**: User explicitly requests agent assistance or AI confidence falls below threshold. System triggers escalation workflow.

---

## 3. AI Security & Guardrails

- **Prompt Injection Defense**: Input text is filtered before prompt assembly to neutralize instruction overrides.
- **Tenant Context Isolation**: SQL queries are locked to the authenticated user's `customer_id`.
- **Hallucination Containment**: Model prompts instruct strict grounding on returned DB context or KB articles.

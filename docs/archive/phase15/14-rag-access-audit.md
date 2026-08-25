# 14 - RAG Architecture & Data Separation Audit

## RAG Component Inventory
- **Storage**: PostgreSQL table `kb_articles`
- **Vector Column**: `embedding` (`Vector(1536)` via `pgvector` extension)
- **Pipeline Implementation**: `app/rag/pipeline.py`
- **Source Articles**: Public ShopKart FAQs, return policies, shipping terms, warranty guidelines.

## Public vs Private Data Separation

```
                  +-----------------------------------+
                  |         INBOUND QUERY             |
                  +-----------------+-----------------+
                                    |
                                    ▼
                          +-------------------+
                          |    AI Router      |
                          +---------+---------+
                                    |
            +-----------------------+-----------------------+
            | RAG Route                                     | STRUCTURED Route
            ▼                                               ▼
+-----------------------+                       +-----------------------+
|  Public Knowledge Base|                       | Private DB Queries    |
|  (`kb_articles`)      |                       | (`orders`, `payments`)|
+-----------------------+                       +-----------------------+
| Public FAQs           |                       | Server-Side Ownership |
| Return Policies       |                       | Verification          |
| Shipping Info         |                       | (`_check_ownership`)  |
| Warranty Guides       |                       +-----------------------+
+-----------------------+
```

## Security & Privacy Compliance Checklist

| Audit Rule | System Implementation | Compliance |
|------------|-----------------------|------------|
| **No Private Data in Vector Index** | `kb_articles` contains exclusively public documentation. Customer names, orders, PII, and credit card data are strictly excluded from embedding pipelines. | PASS |
| **Guest Access to Public RAG** | Guests (`customer_id="GUEST"`) can query shipping rates, cancellation windows, and general FAQs without logging in. | PASS |
| **Grounded Response Synthesis** | RAG responses synthesize output strictly using retrieved context chunks, preventing hallucination of private user details. | PASS |
| **Cross-Tenant Vector Isolation** | Knowledge articles are partitioned by `company_id` (`COMP-001`), ensuring multi-merchant isolation. | PASS |

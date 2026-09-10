# 🐛 SupportHub AI Platform — Master Bug Tracker

> **Tracking Strategy:** One-by-One Resolution with Isolated Verification & User Sign-Off.  
> **Total Bugs Identified:** 13  
> **Status:** Ready for sequential resolution  

---

## 📋 Complete Bug Backlog Summary

| ID | Title | Priority | Severity | Component | Status |
|:---|:---|:---:|:---:|:---|:---:|
| **BUG-001** | KB Article Creation & Update 500 Crash (Vector Dimension Mismatch) | **P0** | Critical | Knowledge Base / Embeddings | ✅ **FIXED** |
| **BUG-006** | Customer Follow-Up Messages on Tickets Don't Trigger AI Response | **P0** | Critical | Ticket Messaging / Live Chat AI | ✅ **FIXED** |
| **BUG-002** | AI Settings Ephemeral (Lost on Restart) & Missing Field / Methods | **P1** | High | Admin AI Config / Database | ✅ **FIXED** |
| **BUG-003** | Refund Intent Misclassification for Damaged Items | **P1** | High | AI Intent Classifier | ✅ **FIXED** |
| **BUG-004** | Out-of-Domain Factual Inquiries Leak Irrelevant KB Content | **P1** | High | RAG Retrieval / Guardrails | ✅ **FIXED** |
| **BUG-005** | Compound Multi-Question Inputs Only Partially Answered | **P1** | High | AI Query Decomposition | ✅ **FIXED** |
| **BUG-007** | Empty Ticket Subject Accepted Without Validation | **P2** | Medium | Ticket Validation Schemas | ✅ **FIXED** |
| **BUG-008** | Inbound Text Stored Without Server-Side XSS Sanitization | **P2** | Medium | Ticket / Message Ingestion | ⏭️ Deferred |
| **BUG-009** | Automated Test Failure in Account Transactions Test | **P2** | Medium | Test Suite Assertion | ✅ **FIXED** |
| **BUG-013** | Database Customer Lookup Ambiguity for Duplicate Customer IDs | **P2** | Medium | Postgres Business Repository | ✅ **FIXED** |
| **BUG-010** | Zero Quick Replies Seeded for Support Agents | **P3** | Low | Seed Data / Agent Productivity | ✅ **PRESENT IN UI** |
| **BUG-011** | FastAPI `@app.on_event` Deprecation Warning | **P3** | Low | App Lifecycle Handler | ✅ **FIXED** |
| **BUG-012** | Python `datetime.utcnow()` Deprecation Warnings | **P3** | Low | Conversation Repository | ✅ **FIXED** |

---

## 🎯 Sequential Execution Workflow

For every bug in this tracker, we will follow a strict 5-step cycle:
1. **Bug Deep-Dive:** Detail what the bug is, its impact, solution, ripple effects on other functions, and test plan.
2. **User Confirmation:** You review the proposed approach and give the green light.
3. **Targeted Code Edit:** We modify only the code strictly required for that specific bug.
4. **Verification & Testing:** We run targeted automated and API tests to prove the bug is resolved and no regressions occurred.
5. **Confirmation & Next Step:** You confirm the fix works, and we move to the next bug.

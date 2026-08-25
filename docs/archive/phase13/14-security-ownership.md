# 14. Security & Ownership Design

## Pre-LLM Ownership Guard
`AIOrchestrator._check_ownership()` inspects all fetched structured records against `ctx.customer_id` **before** constructing the LLM prompt. If `record.customer_id != ctx.customer_id`, the response is immediately redacted to a permission denial.

# Response Aggregation Documentation

## Overview
`aggregate_responses` in `app/ai/graph/nodes.py` collects sub-question responses generated during graph traversal and synthesizes a unified `AIResponse`.

## Aggregation Strategy
1. **Security Precedence**: Credential exposure, system prompt leaks, or prompt injections immediately override standard responses.
2. **Sub-Question Ordering**: Informational answers (order status, payment details, shipment tracking, RAG policy snippets) are appended in original sub-question sequence.
3. **Escalation Preservation**: If any sub-question triggers human escalation, the final response route is set to `HUMAN`, ticket escalation is recorded, and the human transfer message is appended after the informational blocks.

# 17 — Multi-Turn AI Context Isolation

## Security Rollback
- When an unauthorized query (e.g. `ORD-003`) is denied, the AI context rolls back to safe conversation state.
- Subsequent follow-ups return only caller's own records.

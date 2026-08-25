# 26 — Developer Learning Guide & Reference

## Key Takeaways
1. Always derive caller identity from server-side JWT `current_user`.
2. Never trust client-provided `customer_id` query parameters or body inputs for data ownership checks.
3. Combine REST endpoints with AI Orchestration tools using uniform server-side scoping.

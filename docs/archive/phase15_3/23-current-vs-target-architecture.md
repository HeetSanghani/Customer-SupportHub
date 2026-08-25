# 23 — Current vs Target Architecture Comparison

## Architecture Matrix
- **Before Phase 15.3**: REST API only handled name/email profile updates; orders were only accessible via AI tool calls.
- **After Phase 15.3**: REST API handles full contact/address profile updates + dedicated `/orders/me` REST endpoints + interactive `CustomerOrders.jsx` frontend dashboard.

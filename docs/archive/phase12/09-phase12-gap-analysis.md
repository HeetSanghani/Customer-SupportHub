# 09 — Architecture Gap Analysis

## Executive Summary
This document categorizes all components of Customer Authentication & Personalized AI Support according to their readiness status: `ALREADY EXISTS`, `CAN BE REUSED`, `NEEDS MODIFICATION`, `NEEDS CREATION`, and `NOT REQUIRED`.

---

## Architectural Gap Matrix

| Component | Status | Location / Reference | Action Required |
| :--- | :---: | :--- | :--- |
| **Registration API (`/auth/register`)** | `ALREADY EXISTS` | `app/routers/auth.py:101` | Reuse existing endpoint |
| **Login API (`/auth/login`)** | `ALREADY EXISTS` | `app/routers/auth.py:134` | Reuse existing OAuth2 flow |
| **Token Refresh API (`/auth/refresh`)** | `ALREADY EXISTS` | `app/routers/auth.py:162` | Reuse existing refresh mechanism |
| **User Profile API (`/auth/me`)** | `ALREADY EXISTS` | `app/routers/auth.py:196` | Reuse existing me endpoint |
| **Password Hashing (Bcrypt)** | `ALREADY EXISTS` | `app/routers/auth.py:66` | Reuse existing bcrypt logic |
| **JWT Bearer Auth Dependency** | `ALREADY EXISTS` | `app/dependencies.py:56` | Reuse existing `get_current_user` |
| **WebSocket Auth Dependency** | `ALREADY EXISTS` | `app/dependencies.py:75` | Reuse existing `get_ws_user` |
| **User Model (`User`)** | `CAN BE REUSED` | `app/models/__init__.py:75` | Formally add `customer_id` mapping field |
| **LiveChatAIAdapter Identity Resolution**| `NEEDS MODIFICATION`| `app/services/ai/live_chat_adapter.py:67` | Eliminate soft email lookup; enforce trusted `user.customer_id` |
| **WebSocket Room Authorization** | `NEEDS MODIFICATION`| `app/routers/ws/chat.py:157` | Add `ticket.customer_id == user.id` verification guard |
| **Anonymous User Handling** | `NEEDS CREATION` | `app/services/ai/live_chat_adapter.py` | Prompt unauthenticated users to log in for order queries |
| **Shipment Ownership Verification** | `NEEDS MODIFICATION`| `ai/orchestrator.py:246` | Extend `_check_ownership` to resolve shipment order owner |
| **Frontend Customer Login Page** | `CAN BE REUSED` | `supporthub/frontend/src/` | Ensure Customer role login routes to Customer Live Chat UI |
| **Frontend Protected Live Chat Route** | `NEEDS CREATION` | `supporthub/frontend/src/` | Wrap Live Chat view with `AuthGuard` |
| **WhatsApp/Instagram/Facebook Auth** | `NOT REQUIRED` | N/A | Excluded from Phase 12 scope |

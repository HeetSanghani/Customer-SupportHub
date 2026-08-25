# 07 — Comprehensive Security Threat Model

## Executive Summary
This document analyzes 15 security threat vectors targeting customer authentication, identity authorization, WebSocket communication, and AI orchestration in SupportHub.

---

## Threat Matrix & Mitigation Plan

| # | Threat Vector | Risk Level | Current Defense | Identified Gap | Recommended Mitigation |
| :-: | :--- | :---: | :--- | :--- | :--- |
| **1** | **IDOR (Insecure Direct Object Ref)** | 🔴 HIGH | `_check_ownership` in AI orchestrator | Shipment & Order Item tools bypass direct owner check | Extend `_check_ownership` to resolve shipment order owners |
| **2** | **Customer ID Spoofing** | 🔴 HIGH | `LiveChatAIAdapter._resolve_customer_id` | Fallback uses email matching soft logic | Enforce immutable `user.customer_id` from JWT session |
| **3** | **Order ID Guessing** | 🟠 MED | Security Validator ownership check | Guest users can trigger order lookups | Block structured tools for guest sessions |
| **4** | **Email Enumeration** | 🟡 LOW | Rate limiting on `/auth/register` (10/min) | Registration response states "Email already registered" | Return generic success or standard response |
| **5** | **JWT Token Manipulation** | 🔴 HIGH | HS256 signature verification | None (Secret key configured in `.env`) | Rotate secret key in production & enforce strong entropy |
| **6** | **Expired JWT Token Usage** | 🟠 MED | `jwt.decode` expiration check (`exp`) | None | Handled by `get_current_user` dependency |
| **7** | **Missing Authentication** | 🔴 HIGH | `oauth2_scheme` Bearer dependency | Anonymous live chat can invoke AI without auth | Prompt guest for login on personal queries |
| **8** | **Cross-Customer Data Leakage** | 🔴 HIGH | Security Gateway Interception | LLM context might retain prior user session | Reset `ConversationContext` per ticket session |
| **9** | **Prompt Injection / Jailbreak** | 🔴 HIGH | `SecurityValidator` regex guard | Advanced role reversal tricks | Validate intent before passing prompt to LLM |
| **10**| **Tool Function Abuse** | 🟠 MED | Parameter type checking | AI could call arbitrary tools | Restrict `target_tools` strictly by intent category |
| **11**| **LLM Authorization Bypass** | 🔴 HIGH | Pre-LLM ownership check | LLM could generate data without tools | Perform authorization BEFORE synthesizer receives data |
| **12**| **WebSocket Identity Spoofing** | 🔴 HIGH | `get_ws_user` token validation | WebSocket connects to ANY ticket room without room check | Validate `ticket.customer_id == user.id` in `websocket_chat` |
| **13**| **Conversation Ownership Bypass**| 🔴 HIGH | Room broadcast via manager | User A can join User B's `/ws/chat/{ticket_id}` room | Add room-level authorization guard in `chat.py` |
| **14**| **PII Exposure in Logs** | 🟡 LOW | Log sanitizer in AI architecture | SQLAlchemy engine logs full query arguments | Disable SQL query parameter logging in production |
| **15**| **Sensitive Data Exposure in Context**| 🟠 MED | PII redaction rules | Multi-turn memory retains full phone/address | Mask sensitive credit card/phone digits in memory |

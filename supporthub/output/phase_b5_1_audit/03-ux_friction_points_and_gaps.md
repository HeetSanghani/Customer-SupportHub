# Phase B.5.1 — UX Friction Points & Gap Analysis
**Audit Date:** 2026-09-01 | **Status:** READ-ONLY

---

## Executive Summary

The current Customer Role is a **traditional dashboard-style application** built on a sidebar-first navigation model. While it is functionally complete and production-stable, it has several significant UX friction points that prevent it from delivering a premium, AI-first support experience.

The primary issues fall into **5 categories:**
1. **Navigation friction** — sidebar-first paradigm puts support behind menus
2. **AI invisibility** — the AI is buried inside a "chat" module rather than being the primary interface
3. **Context fragmentation** — orders, returns, and shipments exist in silos with no cross-linking to support
4. **Interaction inconsistency** — two different ways to reply to support (WS in LiveChat, REST in History)
5. **Missing self-service actions** — customers cannot initiate returns, only view them

---

## Friction Point Catalog

### CRITICAL — UX Blockers

#### FP-01: AI is Buried, Not Front-and-Center
- **Current:** Customer must navigate Sidebar → "Live AI Assistant" to access AI
- **Impact:** Customers who don't know the app see a "Dashboard" first, not a support interface
- **Expected (AI-first):** AI chat should be the primary, persistent, always-visible surface
- **Severity:** 🔴 CRITICAL

#### FP-02: No Persistent Chat Bar / Floating AI Widget
- **Current:** AI is locked to `/customer/chat` — leaving that page disconnects the session
- **Impact:** If a customer navigates to "My Orders" mid-conversation, they lose chat context
- **Expected:** Chat should persist across navigation (floating panel or persistent sidebar)
- **Severity:** 🔴 CRITICAL

#### FP-03: Notification Preferences Not Saved
- **Current:** Email/WhatsApp/Marketing toggles in Profile are UI-only, never persisted
- **Impact:** Customer cannot actually configure how they receive notifications
- **Severity:** 🔴 CRITICAL (misleads users)

---

### HIGH — Significant Friction

#### FP-04: Support History vs. Live Chat Are Two Separate Pages (Inconsistency)
- **Current:** `/customer/chat` = real-time WS chat; `/customer/support` = REST-based history viewer with reply
- **Impact:** Two different messaging experiences for the same underlying entity (tickets)
  - Chat history in `/support` feels stale (no WS, requires manual refresh)
  - Customer might reply in `/support` and not receive real-time AI responses
- **Severity:** 🟠 HIGH

#### FP-05: No Return/Refund Initiation
- **Current:** Returns & Refunds page is READ-ONLY — customers can see return records but cannot request a new return
- **Impact:** Customer must go to chat → explain situation → wait for AI/agent to initiate return
- **Expected:** Self-service return initiation form
- **Severity:** 🟠 HIGH

#### FP-06: No Onboarding for New / Unlinked Customers
- **Current:** New customers see dashboard with empty states everywhere
  - "No orders found" — but no explanation of the product flow
  - "Account Unlinked" warning in Orders appears with no actionable next step (just text)
- **Impact:** Poor first-run experience, no guidance
- **Severity:** 🟠 HIGH

#### FP-07: Dashboard is Information-Dense with No AI Personalization
- **Current:** Dashboard shows raw counts (orders=N, shipments=N) with no actionable insights
- **Expected:** "Your order #ORD-123 is expected tomorrow — need help?" type proactive AI prompts
- **Severity:** 🟠 HIGH

#### FP-08: Mobile Layout Not Functional
- **Current:** Fixed 256px sidebar always visible — on mobile (~375px screens) content gets squeezed to ~119px
- **Impact:** Application is unusable on mobile without horizontal scrolling
- **Severity:** 🟠 HIGH

---

### MEDIUM — Notable Friction

#### FP-09: Category Modal for New Chat is Ambiguous
- **Current:** "Billing & Payments", "Technical Issue", "Account & Profile", "General Question"
- **Impact:** Customers are forced to categorize BEFORE explaining their issue (opposite of conversational)
- **Expected (AI-first):** Customer types freely; AI infers category automatically
- **Severity:** 🟡 MEDIUM

#### FP-10: No Estimated Wait Time or Queue Position
- **Current:** When escalated, status shows "Waiting for Human Agent" but no ETA
- **Impact:** Customer has no feedback loop on how long to wait
- **Severity:** 🟡 MEDIUM

#### FP-11: Support History Lacks Search and Filter
- **Current:** All tickets listed as a flat list, no search, no filter by date/status/category
- **Impact:** Customers with many tickets cannot find specific ones
- **Severity:** 🟡 MEDIUM

#### FP-12: My Orders Has No Search / Sort
- **Current:** Orders displayed in API response order
- **Impact:** Customers with many orders must scroll to find a specific one
- **Severity:** 🟡 MEDIUM

#### FP-13: Tracking Number is Not Clickable / Deeplinked
- **Current:** Tracking number displayed as plain text (e.g., "TRACK-12345")
- **Expected:** Link to carrier tracking page (FedEx, UPS, USPS, DHL)
- **Severity:** 🟡 MEDIUM

#### FP-14: CSAT Widget Only Appears After Resolution
- **Current:** CSAT appears only when ticket is `closed`/`resolved`
- **Expected:** Interim satisfaction check could appear after AI interaction
- **Severity:** 🟡 MEDIUM (missed opportunity)

#### FP-15: Help Center Articles Display as Plain Text
- **Current:** `article.body` is rendered as `whitespace-pre-line` plain text
- **Expected:** Markdown rendering (headers, bold, lists, code blocks)
- **Severity:** 🟡 MEDIUM

---

### LOW — Polish Items

#### FP-16: No Message Search Within Chat Thread
- **Current:** Chat history scrolls linearly with no search
- **Severity:** 🟢 LOW

#### FP-17: File Upload Has No Size Limit UI Feedback
- **Current:** Upload fails silently if file is too large (backend error shown as alert)
- **Severity:** 🟢 LOW

#### FP-18: Breadcrumbs Inconsistent
- **Current:** Shipments, Returns, Security have breadcrumbs; Orders, Profile, Reviews, Help, Chat do NOT
- **Severity:** 🟢 LOW

#### FP-19: Query Key Mismatch (`['me']` vs `['auth','me']`)
- **Current:** Dashboard uses `['me']`, Profile/Orders use `['auth','me']` for same endpoint
- **Impact:** Profile updates don't invalidate Dashboard card (stale name display)
- **Severity:** 🟢 LOW (but causes subtle data staleness)

---

## Current User Journey Map — "Customer Needs Help With Order"

```
Step 1: Customer logs in
   → Sees Dashboard (orders, shipments, tickets count)
   → No proactive AI greeting or suggestion
   
Step 2: Customer notices order issue
   → Clicks "My Orders" in sidebar
   → Finds order #ORD-456 with wrong status
   → No "Get Help With This Order" button on Orders page
   
Step 3: Customer navigates to AI chat
   → Clicks "Live AI Assistant" in sidebar
   → Sees "+ New Chat" button
   → Clicks → Category picker modal appears
   → Selects "Billing & Payments"
   → Creates ticket (new page load to /customer/chat/{id})
   
Step 4: Customer types their order issue
   → AI responds with generic answer
   → Customer wants human agent
   → Clicks "Talk to Human" button
   → Status changes to "Waiting for Human Agent" (no ETA shown)
   
Step 5: Customer gets bored, navigates to Orders
   → WebSocket disconnects
   → Customer misses agent joining notification
   
Step 6: Customer comes back to chat
   → Finds agent message was waiting
   → Conversation resumes
   
Total friction steps: 6 (could be 2 with AI-first design)
```

## Target AI-First User Journey — "Customer Needs Help With Order"

```
Step 1: Customer logs in
   → AI immediately greets: "Hi [Name]! I see your order ORD-456 
     is shipping tomorrow. Anything I can help you with today?"
   
Step 2: Customer types: "My order shows wrong item"
   → AI instantly provides resolution options inline
   → Customer picks: "Start a return"
   → AI creates return request + confirms

Total friction steps: 2
```

---

## Risk Assessment for Redesign

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Breaking existing API contracts | LOW | HIGH | Read-only audit confirmed — all endpoints preserved |
| Losing CSAT data collection | LOW | HIGH | CSAT widget preserved in new design |
| Losing real-time WS connections | MEDIUM | HIGH | WS architecture remains unchanged |
| Breaking auth/role guards | LOW | HIGH | CustomerLayout guard logic unchanged |
| Missing order/shipment data | LOW | MEDIUM | API surface unchanged, only UI changes |
| Missing omnichannel channel flows | MEDIUM | MEDIUM | WhatsApp/Instagram/Email modals must be preserved |

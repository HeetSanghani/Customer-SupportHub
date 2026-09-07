# Phase B.5.1 — Proposed AI-First Information Architecture
**Audit Date:** 2026-09-01 | **Status:** PROPOSAL — Pending User Approval

> ⚠️ This is the architecture proposal document. No code has been modified. All implementation requires explicit user approval.

---

## Design Philosophy: "AI is the Interface"

The new architecture shifts from **"sidebar dashboard + chat as a feature"** to **"conversational AI as the core surface + contextual cards as supporting panels"**.

### 3 Core Principles

1. **AI-first, not AI-assisted:** The AI greeting, message input, and response is what customers see FIRST — not a KPI dashboard.
2. **Context-aware, not context-fragmented:** When a customer asks about order #456, the AI shows the order card inline — no navigation required.
3. **Progressive disclosure:** Advanced features (profile, security, reviews) remain available but are de-emphasized in favor of the support flow.

---

## New Information Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     /customer/*  (New Layout)                   │
├──────────────┬──────────────────────────────────┬───────────────┤
│  LEFT NAV    │     MAIN CONTENT AREA            │  RIGHT PANEL  │
│  (collapsed) │                                  │  (contextual) │
│              │                                  │               │
│  ☰ SupportHub│  [Primary Surface]               │  [Auto-shown] │
│              │                                  │               │
│  🏠 Home     │  ● AI Conversational Center       │  Order Cards  │
│  📦 Orders   │    (default route)               │  Ticket Info  │
│  🚚 Shipping │                                  │  Profile      │
│  ↩ Returns   │  ● Account Overview              │  Summary      │
│  📋 History  │    (minimal, contextual)          │               │
│  👤 Profile  │                                  │               │
│  🔒 Security │  ● Help Center                   │               │
│  ❓ Help     │                                  │               │
│  ⭐ Reviews  │                                  │               │
│              │                                  │               │
└──────────────┴──────────────────────────────────┴───────────────┘
```

---

## New Route Structure

```
/customer/                → ConversationalHome.jsx     (AI chat interface — THE default)
/customer/home            → ConversationalHome.jsx     (same)
/customer/orders          → CustomerOrders.jsx          (PRESERVED, enhanced)
/customer/shipments       → CustomerShipments.jsx       (PRESERVED, enhanced)
/customer/returns         → CustomerReturnsRefunds.jsx  (PRESERVED, + new initiation form)
/customer/history         → CustomerSupportHistory.jsx  (PRESERVED, converted to use WS)
/customer/profile         → CustomerProfile.jsx         (PRESERVED, fix persistence bug)
/customer/security        → CustomerSecuritySettings.jsx (PRESERVED)
/customer/help            → CustomerHelpCenter.jsx       (PRESERVED, + MD rendering)
/customer/reviews         → CustomerReviews.jsx          (PRESERVED)
```

### What Changes vs. What Is Preserved

| Route | Action | Reason |
|---|---|---|
| `/customer/dashboard` | **REPLACED** → `/customer/home` (ConversationalHome) | AI-first landing page |
| `/customer/chat` | **MERGED** into ConversationalHome | Chat IS the home |
| `/customer/chat/:id` | **PRESERVED** as deep-link into ConversationalHome | External links |
| `/customer/orders` | **PRESERVED** + enhanced | Same API, better UX |
| `/customer/shipments` | **PRESERVED** + tracking deeplinks | Same API |
| `/customer/returns` | **PRESERVED** + initiation form | NEW: customer can request returns |
| `/customer/support` | **PRESERVED** + WS-powered replies | Fix REST→WS inconsistency |
| `/customer/profile` | **PRESERVED** + fix notification persistence | Backend: new notifications field |
| `/customer/settings` | **PRESERVED** as-is | Works correctly |
| `/customer/help` | **PRESERVED** + markdown rendering | Minor enhancement |
| `/customer/reviews` | **PRESERVED** as-is | Works correctly |

---

## ConversationalHome.jsx — New Primary Surface

### Layout Design

```
┌────────────────────────────────────────────────────────────┐
│  [Left Panel: 320px]              [Right Panel: flex-1]    │
│                                                            │
│  ┌──────────────────────┐         ┌───────────────────┐   │
│  │ 🤖 SupportHub AI     │         │ [Active Ticket    │   │
│  │ ─────────────────── │         │  conversation or  │   │
│  │ Search / Start...   │         │  AI empty state]  │   │
│  │                      │         │                   │   │
│  │ RECENT CONVERSATIONS │         │                   │   │
│  │ ● Order issue   [2d] │         │ [Context Panel]   │   │
│  │ ● Billing query [5d] │         │ ─────────────── │   │
│  │ ● Return req    [1w] │         │ Related Order:    │   │
│  │                      │         │ #ORD-456 card     │   │
│  │ ─────────────────── │         │ Shipment status   │   │
│  │ QUICK ACTIONS        │         │ Return history    │   │
│  │ [📦 Track Order]     │         └───────────────────┘   │
│  │ [↩ Start Return]     │                                  │
│  │ [❓ Help Center]      │                                  │
│  └──────────────────────┘                                  │
└────────────────────────────────────────────────────────────┘
```

### Key Behavioral Changes

1. **AI Greeting on Load:** "Hi [Name]! I'm your SupportHub AI assistant. How can I help you today?" — with quick reply chips:
   - "Track my order"
   - "Start a return"
   - "Billing question"
   - "Talk to a human"

2. **Context-Aware AI Panel (Right):** When talking about an order, the panel auto-fetches and displays the order card inline — no page navigation needed.

3. **Persistent Chat:** Chat connection maintained while navigating other pages (via React context or global WS store).

4. **Smart Quick Actions:** Based on recent data — if an order is "SHIPPED", show "Track Order" prominently.

---

## New Sidebar Design

### Collapsed-by-default on Mobile

```jsx
// Mobile: hamburger menu toggle
// Desktop: auto-expanded icon + label sidebar
```

### Sidebar Items (Reorganized)

```
[Logo] SupportHub

HOME
  🤖 AI Assistant          ← NEW: primary nav item (replaces Dashboard)

TRANSACTIONS
  📦 My Orders
  🚚 Shipments
  ↩ Returns & Refunds

SUPPORT
  📋 Support History
  ❓ Help Center
  ⭐ My Reviews

ACCOUNT
  👤 Profile
  🔒 Security

CHANNELS (collapsible)
  📱 Connect WhatsApp
  📸 Connect Instagram
  ✉️ Contact Email

──────────────────
[Avatar] User Name
[Logout]
```

---

## Design System Tokens (New)

| Token | Value | Usage |
|---|---|---|
| `--brand-primary` | `#6366F1` (Indigo 500) | Primary actions, AI bubbles |
| `--brand-gradient` | `linear-gradient(135deg, #6366F1, #A855F7)` | Hero elements |
| `--surface-base` | `#0F0F1A` (Dark Navy) | Dark mode base (optional) |
| `--surface-card` | `#FFFFFF` | Card backgrounds |
| `--surface-bg` | `#F6F7FC` | Page background |
| `--text-primary` | `#1C1B2E` | Headings |
| `--text-secondary` | `#6C7089` | Body text |
| `--text-muted` | `#9598B0` | Captions, timestamps |
| `--ai-bubble` | `#F6F7FC` with indigo border | AI message bubbles |
| `--customer-bubble` | `#6366F1` white text | Customer message bubbles |
| `--radius-card` | `16px` | Card border radius |
| `--radius-chat` | `18px` | Chat bubble radius |
| `--shadow-card` | `0 1px 4px rgba(0,0,0,0.06)` | Subtle card shadows |

### Typography (Preserved from existing)
- **Headings:** Plus Jakarta Sans, 700 weight
- **Body:** Inter or system-ui
- **Monospace:** `font-mono` for refs/codes

### Animation Tokens
- **Hover lift:** `translateY(-2px) + shadow-md` on card hover
- **Message appear:** `fadeIn + slideUp` (150ms)
- **Typing indicator:** 3 dots bouncing with staggered delays (already implemented)
- **Page transition:** `fade` (100ms)

---

## Component Architecture Plan

### New Components to Build

| Component | Purpose | Replaces |
|---|---|---|
| `ConversationalHome.jsx` | AI-first landing page | `CustomerDashboard` + `CustomerLiveChat` merged |
| `AIMessageBubble.jsx` | Extracted from ChatPane | Inline in CustomerLiveChat currently |
| `CustomerMessageBubble.jsx` | Extracted from ChatPane | Inline in CustomerLiveChat currently |
| `ContextPanel.jsx` | Right-side contextual info | New — shows order/ticket/shipment cards |
| `QuickActionChips.jsx` | AI greeting suggestion chips | New |
| `ConversationSidebar.jsx` | Left panel with recent chats | Split from CustomerLiveChat |
| `OrderContextCard.jsx` | Mini order card in chat | New |
| `ShipmentContextCard.jsx` | Mini shipment card in chat | New |
| `TicketStatusBanner.jsx` | Current ticket status in header | Extracted from ChatPane header |
| `MobileNavDrawer.jsx` | Hamburger menu for mobile | New — CustomerLayout fix |

### Preserved Components (Zero Change)

| Component | Status |
|---|---|
| `CsatWidget` | ✅ Preserved as-is |
| `CustomerOrders.jsx` | ✅ Preserved as-is |
| `CustomerShipments.jsx` | ✅ Preserved, minor tracking link enhancement |
| `CustomerSecuritySettings.jsx` | ✅ Preserved as-is |
| `CustomerReturnsRefunds.jsx` | ✅ Preserved, new return initiation section added |
| `CustomerProfile.jsx` | ✅ Preserved, fix notification persistence |
| `CustomerReviews.jsx` | ✅ Preserved as-is |
| `CustomerHelpCenter.jsx` | ✅ Preserved, markdown rendering enhancement |
| `ContactEmailModal.jsx` | ✅ Preserved as-is |
| `ContactWhatsAppModal.jsx` | ✅ Preserved as-is |
| `ContactInstagramModal.jsx` | ✅ Preserved as-is |

---

## Backend Changes Required

### Minimal Backend Additions (No Removals)

| Change | Endpoint | Purpose | Risk |
|---|---|---|---|
| Notification preferences persist | `PATCH /auth/me` — add `notification_prefs` JSON field | Fix FP-03 | LOW |
| Customer return initiation | `POST /orders/returns` — customer-facing | Fix FP-05 | MEDIUM |
| Ticket add message via WS | Already exists — fix SupportHistory to use it | Fix FP-04 | LOW |

### Zero Breaking Changes
- All existing endpoints preserved
- No schema removal
- Only additive backend changes

---

## Parity Checklist (Must-Have for Redesign)

| Feature | Must Preserve | Notes |
|---|---|---|
| WebSocket real-time chat | ✅ | New home merges chat |
| Ticket creation (all categories) | ✅ | Quick actions map to same POST |
| Escalation to human | ✅ | Button preserved in new chat UI |
| CSAT rating | ✅ | CsatWidget component unchanged |
| File uploads | ✅ | Same upload endpoint |
| Orders / Shipments / Returns (read) | ✅ | Same pages preserved |
| Profile edit | ✅ | Same page preserved |
| Password change | ✅ | Same page preserved |
| Knowledge base / Help Center | ✅ | Same page preserved |
| Omnichannel modals (WA/IG/Email) | ✅ | Same 3 modals preserved |
| JWT auth + refresh | ✅ | Same auth infrastructure |
| Role guard | ✅ | Same CustomerLayout guard |
| Ticket reopen | ✅ | Same action preserved |

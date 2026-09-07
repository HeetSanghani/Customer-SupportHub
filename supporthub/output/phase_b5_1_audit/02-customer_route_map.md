# Phase B.5.1 — Customer Role Route Map
**Audit Date:** 2026-09-01 | **Status:** READ-ONLY

---

## Route Structure

```
/customer/*          → CustomerLayout.jsx (role-guard: role === 'customer')
│
├── /                → CustomerDashboard.jsx   (default redirect)
├── /dashboard       → CustomerDashboard.jsx
├── /chat            → CustomerLiveChat.jsx    (no ticket selected)
├── /chat/:id        → CustomerLiveChat.jsx    (ticket pre-selected by URL param)
├── /orders          → CustomerOrders.jsx
├── /shipments       → CustomerShipments.jsx
├── /returns         → CustomerReturnsRefunds.jsx
├── /support         → CustomerSupportHistory.jsx
├── /profile         → CustomerProfile.jsx
├── /settings        → CustomerSecuritySettings.jsx
├── /help            → CustomerHelpCenter.jsx
├── /reviews         → CustomerReviews.jsx
└── /*               → <Navigate to="/customer" replace />
```

---

## Route → Component → API Dependency Map

### `/customer/dashboard`
- **Component:** `CustomerDashboard.jsx`
- **React Query Keys:** `['me']`, `['orders','me']`, `['shipments','me']`, `['returns','me']`, `['refunds','me']`, `['tickets','customer']`
- **APIs Called:** `GET /auth/me`, `GET /orders/me`, `GET /orders/shipments/me`, `GET /orders/returns/me`, `GET /orders/refunds/me`, `GET /tickets/`
- **Real-time:** `refetchInterval: 10000` for tickets (via CustomerLayout shared query)

### `/customer/chat` and `/customer/chat/:id`
- **Component:** `CustomerLiveChat.jsx` → `ChatPane` + `CsatWidget`
- **React Query Keys:** `['tickets','customer']`, `['ticket',ticketId]`, `['csat',ticketId]`
- **APIs Called:**
  - `GET /tickets/` — list sidebar
  - `GET /tickets/{id}` — load ticket detail
  - `POST /tickets/` — create new ticket
  - `GET /tickets/{id}/messages` — load history
  - `POST /tickets/{id}/upload` — file upload
  - `POST /tickets/{id}/escalate` — escalate
  - `POST /tickets/{id}/reopen` — reopen
  - `GET /tickets/{id}/csat` — check review
  - `POST /tickets/{id}/csat` — submit review
  - `WS /ws/chat/{id}?token=JWT` — real-time
- **URL Param:** `:id` = ticket UUID

### `/customer/orders`
- **Component:** `CustomerOrders.jsx`
- **React Query Keys:** `['auth','me']`, `['orders','me']`, `['orders', selectedOrderId]`
- **APIs Called:** `GET /auth/me`, `GET /orders/me`, `GET /orders/{orderId}`

### `/customer/shipments`
- **Component:** `CustomerShipments.jsx`
- **React Query Keys:** `['shipments','me']`
- **APIs Called:** `GET /orders/shipments/me`

### `/customer/returns`
- **Component:** `CustomerReturnsRefunds.jsx`
- **React Query Keys:** `['returns','me']`, `['refunds','me']`, `['payments','me']`
- **APIs Called:** `GET /orders/returns/me`, `GET /orders/refunds/me`, `GET /orders/payments/me`

### `/customer/support`
- **Component:** `CustomerSupportHistory.jsx`
- **React Query Keys:** `['tickets','customer']`, `['ticket-messages', selectedTicketId]`
- **APIs Called:** `GET /tickets/`, `GET /tickets/{id}/messages`, `POST /tickets/{id}/messages`
- **Note:** Uses REST for sending replies (not WebSocket)

### `/customer/profile`
- **Component:** `CustomerProfile.jsx`
- **React Query Keys:** `['auth','me']`, `['tickets','customer']`
- **APIs Called:** `GET /auth/me`, `PATCH /auth/me`, `GET /tickets/`
- **Mutations:** `PATCH /auth/me`

### `/customer/settings`
- **Component:** `CustomerSecuritySettings.jsx`
- **APIs Called:** `POST /auth/change-password`
- **React Query Keys:** None (no query, mutation only)

### `/customer/help`
- **Component:** `CustomerHelpCenter.jsx`
- **React Query Keys:** `['customer-kb-articles']`
- **APIs Called:** `GET /knowledge/?published_only=true&limit=100`, `POST /knowledge/{id}/helpful`

### `/customer/reviews`
- **Component:** `CustomerReviews.jsx`
- **React Query Keys:** `['my-csat-reviews']`
- **APIs Called:** `GET /tickets/csat/my-reviews`

---

## Modal Routes (Overlay — no URL change)

| Modal | Trigger | APIs |
|---|---|---|
| `ContactEmailModal` | Sidebar "Contact Email" button | `POST /tickets/` (`channel: 'email'`) |
| `ContactWhatsAppModal` | Sidebar "Connect WhatsApp" button | `POST /tickets/` (`channel: 'whatsapp'`) OR external `wa.me` link |
| `ContactInstagramModal` | Sidebar "Connect Instagram" button | `POST /tickets/` (`channel: 'instagram'`) OR external `ig.me` link |

---

## Navigation Flow Diagram

```
Login (/login)
    ↓ role === 'customer'
CustomerLayout (/customer/*)
    ├── Sidebar (always visible)
    │   ├── Dashboard → /customer/dashboard
    │   ├── AI Assistant → /customer/chat  [+ badge]
    │   ├── My Orders → /customer/orders
    │   ├── Shipments → /customer/shipments
    │   ├── Returns → /customer/returns
    │   ├── Support History → /customer/support
    │   ├── Profile → /customer/profile
    │   ├── Security → /customer/settings
    │   ├── Help Center → /customer/help
    │   ├── Reviews → /customer/reviews
    │   ├── [Modal] WhatsApp
    │   ├── [Modal] Instagram
    │   └── [Modal] Email
    └── User avatar + Logout button

CustomerLiveChat cross-links:
    ├── New chat → category modal → POST → /customer/chat/{new_id}
    ├── Reviews → /customer/reviews
    └── CSAT "View in My Reviews" → /customer/reviews

CustomerDashboard cross-links:
    ├── "View All Orders" → /customer/orders
    ├── "Track Shipments" → /customer/shipments
    ├── "View Support" → /customer/support
    ├── "Edit Profile" → /customer/profile
    └── "Live AI Assistant" → /customer/chat

CustomerOrders cross-links:
    └── Empty state CTA → /customer/chat (anchor href)

CustomerHelpCenter cross-links:
    ├── Articles CTA → /customer/chat
    └── "Still need help?" → /customer/chat
```

---

## Auth Guard Implementation

```jsx
// CustomerLayout.jsx:43
if (!isAuthenticated || role !== 'customer') return <Navigate to="/login" replace />
```

- Uses `useAuthStore()` from Zustand persist store
- Token stored in localStorage key `supporthub-auth`
- 401 responses trigger silent refresh via `client.js` interceptor

---

## Shared Query Key Consistency Audit

| Query Key | Used In | Notes |
|---|---|---|
| `['tickets', 'customer']` | CustomerLayout, Dashboard, LiveChat, Profile, SupportHistory | ✅ Shared correctly |
| `['me']` | CustomerDashboard | ⚠️ Inconsistent — Profile uses `['auth','me']` |
| `['auth','me']` | CustomerProfile, CustomerOrders | ✅ Consistent between these two |
| `['orders','me']` | Dashboard, Orders | ✅ Consistent |
| `['ticket', ticketId]` | ChatPane | ✅ |
| `['csat', ticketId]` | CsatWidget | ✅ |
| `['my-csat-reviews']` | CustomerReviews | ✅ |
| `['customer-kb-articles']` | CustomerHelpCenter | ✅ |

**⚠️ Issue Identified:** `CustomerDashboard` uses `queryKey: ['me']` but `CustomerProfile` and `CustomerOrders` use `queryKey: ['auth', 'me']`. These are two separate cache entries for the same data (`GET /auth/me`). This means profile updates invalidating `['auth','me']` won't refresh the Dashboard's profile card.

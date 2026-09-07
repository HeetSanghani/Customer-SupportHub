# Phase B.5.1 — Customer Feature Inventory Matrix
**Audit Date:** 2026-09-01  
**Auditor:** AI Antigravity (Read-Only)  
**Status:** READ-ONLY — No code modifications made

---

## 1. Navigation Architecture (CustomerLayout.jsx)

| Nav Item | Route | Icon | Condition |
|---|---|---|---|
| Dashboard Overview | `/customer/dashboard` | LayoutDashboard | Always visible |
| Live AI Assistant | `/customer/chat` | MessageSquare | Active ticket badge |
| My Orders | `/customer/orders` | ShoppingBag | Always visible |
| Shipments & Tracking | `/customer/shipments` | Truck | Always visible |
| Returns & Refunds | `/customer/returns` | RotateCcw | Always visible |
| Support History | `/customer/support` | History | Always visible |
| Customer Profile | `/customer/profile` | User | Always visible |
| Security Settings | `/customer/settings` | Lock | Always visible |
| Help Center & FAQs | `/customer/help` | BookOpen | Always visible |
| My Reviews | `/customer/reviews` | Star | Always visible |
| Connect WhatsApp | `(modal)` | Phone | Button in sidebar |
| Connect Instagram | `(modal)` | Instagram | Button in sidebar |
| Contact Email | `(modal)` | Mail | Button in sidebar |

**Total Routes: 10 pages + 3 modal flows**

---

## 2. Feature Inventory — Detailed Matrix

### F-01: Customer Dashboard (`CustomerDashboard.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-01-01 | Welcome banner with name | ✅ Implemented | `GET /auth/me` | Shows customer name + verified badge |
| F-01-02 | Customer ID display | ✅ Implemented | `GET /auth/me` → `customer_id` | Shows "Verified Account (CUST-001)" |
| F-01-03 | Total Orders KPI card | ✅ Implemented | `GET /orders/me` | Count only; no breakdown |
| F-01-04 | Shipment Records KPI card | ✅ Implemented | `GET /orders/shipments/me` | Count only |
| F-01-05 | Returns count + Refund total | ✅ Implemented | `GET /orders/returns/me` + `GET /orders/refunds/me` | Shows total $ refunded |
| F-01-06 | Active ticket count KPI | ✅ Implemented | `GET /tickets/` | Count of non-resolved/closed |
| F-01-07 | Recent 3 orders list | ✅ Implemented | `GET /orders/me` | Shows order_id, date, amount, status |
| F-01-08 | Recent 3 shipments list | ✅ Implemented | `GET /orders/shipments/me` | Shows carrier, tracking, status |
| F-01-09 | Profile summary card (read-only) | ✅ Implemented | `GET /auth/me` | Name, email, phone, address |
| F-01-10 | Active support conversations summary | ✅ Implemented | `GET /tickets/` | Shows last 3 tickets |
| F-01-11 | CTA button → Live AI Assistant | ✅ Implemented | Link to `/customer/chat` | — |
| F-01-12 | Poll tickets every 10 seconds | ✅ Implemented | `refetchInterval: 10000` | Via CustomerLayout |

---

### F-02: Live AI Assistant / Chat (`CustomerLiveChat.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-02-01 | Start new ticket by category | ✅ Implemented | `POST /tickets/` | 4 categories: Billing, Technical, Account, General |
| F-02-02 | Category picker modal | ✅ Implemented | UI state | Opens on "+ New Chat" click |
| F-02-03 | Chat list panel (left sidebar) | ✅ Implemented | `GET /tickets/` | Lists all customer tickets |
| F-02-04 | Filter: Active / Completed / All | ✅ Implemented | Client-side filter | Toggles visible tickets |
| F-02-05 | Click ticket → load conversation | ✅ Implemented | `GET /tickets/{id}/messages` | URL param `/chat/:id` |
| F-02-06 | Real-time WebSocket messaging | ✅ Implemented | `ws://host/ws/chat/{id}?token=JWT` | Persistent connection per ticket |
| F-02-07 | AI typing indicator (dots) | ✅ Implemented | WS `message` event | Shows while AI generating |
| F-02-08 | Agent joined system message | ✅ Implemented | WS `agent_joined` event | Injected as system message |
| F-02-09 | Status badge: AI Active / Escalated / Agent Connected | ✅ Implemented | `ticket.status` + `ticket.agent_id` | Dynamic in chat header |
| F-02-10 | Escalate to Human button | ✅ Implemented | `POST /tickets/{id}/escalate` | Visible when AI-only, not closed |
| F-02-11 | Text message input + Send | ✅ Implemented | WS `send(message)` | Disabled when ticket closed |
| F-02-12 | File/image attachment upload | ✅ Implemented | `POST /tickets/{id}/upload` | Multipart form; embeds link in message |
| F-02-13 | Image preview in chat | ✅ Implemented | Attachment URL parsing | Inline image with fallback |
| F-02-14 | Audio player in chat | ✅ Implemented | Attachment URL parsing | HTML5 audio element |
| F-02-15 | PDF attachment link | ✅ Implemented | Attachment URL parsing | Opens in new tab |
| F-02-16 | Generic file download link | ✅ Implemented | Attachment URL parsing | — |
| F-02-17 | Resolve: "Reopen Conversation" | ✅ Implemented | `POST /tickets/{id}/reopen` | Shown when status = closed/resolved |
| F-02-18 | CSAT widget (star rating) | ✅ Implemented | `POST /tickets/{id}/csat` | Shown after close/resolve |
| F-02-19 | CSAT optional comment field | ✅ Implemented | POST body: `{rating, comment}` | — |
| F-02-20 | CSAT: check if already submitted | ✅ Implemented | `GET /tickets/{id}/csat` | Prevents duplicate submission |
| F-02-21 | CSAT: link to My Reviews | ✅ Implemented | Navigate to `/customer/reviews` | — |
| F-02-22 | Channel badge (Email Inquiry) | ✅ Implemented | `ticket.channel === 'email'` | Visual chip in header |
| F-02-23 | Smart time formatting | ✅ Implemented | `formatSmartTime(ts)` | Relative for recent messages |
| F-02-24 | Ticket ref display | ✅ Implemented | `ticket.ref` | Monospace in header |
| F-02-25 | Auto-select filter when URL opens closed ticket | ✅ Implemented | `useEffect` on `id + tickets` | Switches to "Completed" tab |

---

### F-03: My Orders (`CustomerOrders.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-03-01 | Order history list | ✅ Implemented | `GET /orders/me` | Sorted by API response |
| F-03-02 | Customer ID badge (linked/unlinked) | ✅ Implemented | `GET /auth/me` → `customer_id` | Amber warning if unlinked |
| F-03-03 | Click order → detail panel | ✅ Implemented | `GET /orders/{orderId}` | Toggle expand/collapse |
| F-03-04 | Order detail: items list | ✅ Implemented | `res.data.items[]` | product_name, qty, total_price |
| F-03-05 | Order detail: shipment info | ✅ Implemented | `res.data.shipment` | Carrier, tracking, est. delivery |
| F-03-06 | Order detail: payment status | ✅ Implemented | `res.data.payment` | Status + method |
| F-03-07 | Order detail: grand total | ✅ Implemented | `res.data.order.total_amount` | — |
| F-03-08 | Order status badges (color-coded) | ✅ Implemented | `order.status` | DELIVERED=green, SHIPPED=blue, CANCELLED=red |
| F-03-09 | Empty state + CTA to support | ✅ Implemented | Conditional render | Links to chat |
| F-03-10 | Unlinked account explanation | ✅ Implemented | `customer_id === null` check | Explains why orders are missing |

---

### F-04: Shipments & Tracking (`CustomerShipments.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-04-01 | All shipment records list | ✅ Implemented | `GET /orders/shipments/me` | — |
| F-04-02 | Shipment ID + order reference | ✅ Implemented | `s.shipment_id`, `s.order_id` | — |
| F-04-03 | Carrier name | ✅ Implemented | `s.carrier` | Fallback: "Standard Shipping" |
| F-04-04 | Tracking number | ✅ Implemented | `s.tracking_number` | Fallback: N/A |
| F-04-05 | Estimated delivery date | ✅ Implemented | `s.estimated_delivery_date` | LocaleDateString format |
| F-04-06 | Status badge (DELIVERED/SHIPPED/other) | ✅ Implemented | `s.status` | Color-coded |
| F-04-07 | Breadcrumb to Dashboard | ✅ Implemented | Link component | — |
| F-04-08 | Empty state | ✅ Implemented | Conditional render | — |

---

### F-05: Returns, Refunds & Payments (`CustomerReturnsRefunds.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-05-01 | Return requests list | ✅ Implemented | `GET /orders/returns/me` | With reason + status |
| F-05-02 | Issued refunds list | ✅ Implemented | `GET /orders/refunds/me` | Amount + status |
| F-05-03 | Payment transactions list | ✅ Implemented | `GET /orders/payments/me` | Method + amount + status |
| F-05-04 | Return status badges (APPROVED/REJECTED/PENDING) | ✅ Implemented | `r.status` | Color-coded |
| F-05-05 | Refund amount display ($) | ✅ Implemented | `rf.refund_amount` | Green positive display |
| F-05-06 | Payment method display | ✅ Implemented | `p.method` | — |
| F-05-07 | Breadcrumb to Dashboard | ✅ Implemented | Link component | — |

---

### F-06: Support History (`CustomerSupportHistory.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-06-01 | All tickets list | ✅ Implemented | `GET /tickets/` | With ref, status, channel, category |
| F-06-02 | Select ticket → view thread | ✅ Implemented | `GET /tickets/{id}/messages` | Rendered in right panel |
| F-06-03 | Message thread display | ✅ Implemented | `messages[]` | Grouped by sender_type |
| F-06-04 | Reply to ticket (REST, not WS) | ✅ Implemented | `POST /tickets/{id}/messages` (addMessage) | ⚠️ Uses REST polling, not real-time WS |
| F-06-05 | Ticket status badge | ✅ Implemented | `t.status` | — |
| F-06-06 | Channel + category info | ✅ Implemented | `t.channel`, `t.category` | — |

---

### F-07: Customer Profile (`CustomerProfile.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-07-01 | Profile view (read mode) | ✅ Implemented | `GET /auth/me` | Name, email, phone, address fields |
| F-07-02 | Edit profile toggle | ✅ Implemented | UI state `isEditing` | In-place editing |
| F-07-03 | Save profile changes | ✅ Implemented | `PATCH /auth/me` | All fields |
| F-07-04 | Name, email fields | ✅ Implemented | — | Required fields |
| F-07-05 | Phone number | ✅ Implemented | — | Optional |
| F-07-06 | Full shipping address | ✅ Implemented | address, city, state, postal_code, country | — |
| F-07-07 | Customer ID display (read-only) | ✅ Implemented | `userProfile.customer_id` | Cannot be changed by customer |
| F-07-08 | Avatar initials (auto-generated) | ✅ Implemented | `name.split()` | Gradient purple background |
| F-07-09 | Support ticket stats (total/solved/active) | ✅ Implemented | `GET /tickets/` | 3-column grid |
| F-07-10 | Email notification toggle (UI-only) | ⚠️ Partial | UI state only | Not persisted to backend |
| F-07-11 | WhatsApp notification toggle (UI-only) | ⚠️ Partial | UI state only | Not persisted to backend |
| F-07-12 | Product announcements toggle (UI-only) | ⚠️ Partial | UI state only | Not persisted to backend |
| F-07-13 | Cancel edit (reset to fetched data) | ✅ Implemented | Re-hydrates from `userProfile` | — |
| F-07-14 | Error feedback on save failure | ✅ Implemented | `onError` handler | — |

---

### F-08: Security Settings (`CustomerSecuritySettings.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-08-01 | Change password form | ✅ Implemented | `POST /auth/change-password` | — |
| F-08-02 | Current password field | ✅ Implemented | `current_password` | Required |
| F-08-03 | New password field | ✅ Implemented | `new_password` | Min 8 chars |
| F-08-04 | Confirm password field | ✅ Implemented | `confirm_password` | Must match |
| F-08-05 | Client-side validation | ✅ Implemented | All fields required, min length | Before API call |
| F-08-06 | Success / error feedback | ✅ Implemented | `statusMsg` state | Color-coded alert |

---

### F-09: Help Center & FAQs (`CustomerHelpCenter.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-09-01 | Hero search bar | ✅ Implemented | Client-side filter | Searches title, body, category |
| F-09-02 | Category filter pills | ✅ Implemented | Client-side | All / Billing / Technical / Account / General |
| F-09-03 | Article list with expand/collapse | ✅ Implemented | `GET /knowledge/` | `published_only: true` |
| F-09-04 | Article metadata (views, helpful votes) | ✅ Implemented | `article.views`, `article.helpful_count` | Read from KB |
| F-09-05 | "Helpful" vote button | ✅ Implemented | `POST /knowledge/{id}/helpful` | One vote per session |
| F-09-06 | Live Chat CTA banner | ✅ Implemented | Navigate to `/customer/chat` | — |
| F-09-07 | WhatsApp support banner | ✅ Implemented | `wa.me` link | Direct external link |
| F-09-08 | Search clear button | ✅ Implemented | UI state | — |
| F-09-09 | Empty state + "Ask AI" CTA | ✅ Implemented | Conditional render | — |

---

### F-10: My Reviews (`CustomerReviews.jsx`)

| Feature ID | Feature | Status | Data Source | Notes |
|---|---|---|---|---|
| F-10-01 | CSAT reviews list | ✅ Implemented | `GET /tickets/csat/my-reviews` | — |
| F-10-02 | Star rating display | ✅ Implemented | `rev.rating` | Amber stars |
| F-10-03 | Optional comment display | ✅ Implemented | `rev.comment` | Italic quote style |
| F-10-04 | Ticket subject + ref | ✅ Implemented | `rev.ticket_subject`, `rev.ticket_ref` | — |
| F-10-05 | Click review → open ticket chat | ✅ Implemented | Navigate to `/customer/chat/{ticket_id}` | — |
| F-10-06 | Submission date display | ✅ Implemented | `formatDate(rev.created_at)` | — |
| F-10-07 | Empty state + CTA | ✅ Implemented | No reviews message | — |

---

### F-11: Omnichannel Contact Modals (3 Modals via CustomerLayout)

| Feature ID | Feature | Status | Notes |
|---|---|---|---|
| F-11-01 | WhatsApp Direct Launch (external link) | ✅ Implemented | `wa.me` deep link |
| F-11-02 | WhatsApp Ticket Creation | ✅ Implemented | `POST /tickets/` with `channel: 'whatsapp'` |
| F-11-03 | Instagram Direct Launch (external link) | ✅ Implemented | `ig.me` deep link |
| F-11-04 | Instagram Ticket Creation | ✅ Implemented | `POST /tickets/` with `channel: 'instagram'` |
| F-11-05 | Email Ticket Creation | ✅ Implemented | `POST /tickets/` with `channel: 'email'` |
| F-11-06 | Success state → navigate to ticket thread | ✅ Implemented | All 3 modals |
| F-11-07 | Category selection per modal | ✅ Implemented | general/billing/technical/account |

---

## 3. Complete API Surface — Customer Role

| Method | Endpoint | Used By | Purpose |
|---|---|---|---|
| POST | `/auth/login` | LoginPage | Authenticate customer |
| POST | `/auth/register` | RegisterPage | New account |
| POST | `/auth/refresh` | client.js | Silently refresh JWT |
| GET | `/auth/me` | Dashboard, Profile, Orders | Get own profile |
| PATCH | `/auth/me` | CustomerProfile | Update name/email/address |
| POST | `/auth/change-password` | SecuritySettings | Change password |
| GET | `/tickets/` | All pages | List own tickets |
| GET | `/tickets/{id}` | ChatPane | Get single ticket |
| POST | `/tickets/` | LiveChat, Modals | Create new ticket |
| GET | `/tickets/{id}/messages` | ChatPane, SupportHistory | Load message thread |
| POST | `/tickets/{id}/messages` | SupportHistory | Send reply (REST) |
| POST | `/tickets/{id}/upload` | ChatPane | File attachment |
| POST | `/tickets/{id}/escalate` | ChatPane | Escalate to human |
| POST | `/tickets/{id}/reopen` | ChatPane | Reopen resolved ticket |
| GET | `/tickets/{id}/csat` | CsatWidget | Check if review submitted |
| POST | `/tickets/{id}/csat` | CsatWidget | Submit CSAT rating |
| GET | `/tickets/csat/my-reviews` | CustomerReviews | List own CSAT |
| GET | `/orders/me` | Dashboard, Orders | List own orders |
| GET | `/orders/{orderId}` | CustomerOrders | Order detail + items + shipment |
| GET | `/orders/shipments/me` | Dashboard, Shipments | List own shipments |
| GET | `/orders/returns/me` | Dashboard, Returns | List own returns |
| GET | `/orders/refunds/me` | Dashboard, Returns | List own refunds |
| GET | `/orders/payments/me` | Returns page | List own payments |
| GET | `/knowledge/` | HelpCenter | Published KB articles |
| POST | `/knowledge/{id}/helpful` | HelpCenter | Vote article helpful |
| WS | `/ws/chat/{id}?token=JWT` | ChatPane | Real-time bidirectional chat |

**Total: 23 REST endpoints + 1 WebSocket channel used by Customer Role**

---

## 4. Authentication & Authorization

| Mechanism | Implementation |
|---|---|
| JWT Token | Stored in Zustand `persist` middleware (localStorage key: `supporthub-auth`) |
| Auto-refresh | `client.js` interceptor: 401 → `POST /auth/refresh` silently |
| Role guard | `CustomerLayout.jsx` checks `role === 'customer'` before rendering |
| WS auth | Token passed as query param `?token=JWT` |

---

## 5. Real-time Architecture

| Feature | Transport | Details |
|---|---|---|
| Chat messages | WebSocket | `/ws/chat/{ticketId}` — per-ticket connection |
| Ticket list refresh | Polling | `refetchInterval: 10000ms` in CustomerLayout |
| Ticket status change | WebSocket | `ticket_update` event type |
| Agent joins | WebSocket | `agent_joined` event type |
| CSAT after resolve | WebSocket | `ticket_update` → status triggers UI switch |

---

## 6. Missing / Partial Features (Friction Points)

| Gap ID | Description | Severity | Pages Affected |
|---|---|---|---|
| G-01 | Notification preferences (email/whatsapp/marketing toggles) not persisted | HIGH | CustomerProfile |
| G-02 | Support History reply box uses REST (no live WS); feels inconsistent | MEDIUM | CustomerSupportHistory |
| G-03 | No ticket search or filter in Support History | MEDIUM | CustomerSupportHistory |
| G-04 | No order search / sort / filter in My Orders | LOW | CustomerOrders |
| G-05 | No tracking deeplink (carrier site) from Shipments page | LOW | CustomerShipments |
| G-06 | No return/refund request initiation by customer | HIGH | CustomerReturnsRefunds (READ-ONLY) |
| G-07 | No "estimated resolution time" shown to customer | MEDIUM | CustomerLiveChat |
| G-08 | No proactive notifications (only polling) | MEDIUM | All pages |
| G-09 | No message search within a chat thread | LOW | CustomerLiveChat |
| G-10 | Help Center: KB article body is plain text (no markdown rendering) | LOW | CustomerHelpCenter |
| G-11 | No onboarding flow for new/unlinked customers | HIGH | CustomerDashboard |
| G-12 | Sidebar always visible — no mobile responsive menu | MEDIUM | CustomerLayout |

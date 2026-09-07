# Phase B.5.2 — Conversational UI/UX Architecture & Design System

**Module**: SupportHub Customer-Facing Experience  
**Phase**: B.5.2 — Customer Role Audit & Conversational UI/UX Redesign  
**Date**: September 1, 2026  

---

## 1. Architectural Philosophy

The B.5.2 Customer UI/UX redesign establishes a **Conversation-First Interaction Model**. 

Instead of forcing users through multiple navigational layers and form submissions, SupportHub defaults directly into a unified conversational workspace (`ConversationalHome.jsx`).

```
+-----------------------------------------------------------------------------------+
|                            CustomerHeader.jsx                                     |
|  [S] SupportHub AI SUPPORT (Online)                [?] Help v   (AS) Aarav Sharma v|
+-----------------------------------------------------------------------------------+
|  Conversations (300px) |                  Central Chat Workspace                  |
|  +-------------------+ | +------------------------------------------------------+ |
|  | + New Conversation| | | Header: Ticket TCK-001 | Category | ✨ AI Active      | |
|  |                   | | +------------------------------------------------------+ |
|  | [Active] TCK-001  | | | [AI Bubble]  Hello! How can I assist with your order?| |
|  | [Resolved] TCK-002| | | [User]      Where is shipment TRK-12345?             | |
|  |                   | | | [AI Bubble]  Your package is out for delivery!       | |
|  |                   | | +------------------------------------------------------+ |
|  |                   | | | Sticky Input: [ Type a message...        ] [Paperclip] | |
|  +-------------------+ | +------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

---

## 2. Design Tokens & Styling Guide

The Customer UI/UX follows a clean, modern aesthetic with rich micro-animations and accessibility compliance:

### Palette & Color System
- **Primary Accent**: Indigo `#6366F1` (Hover: `#4F46E5`, Light: `#EEF2FF`)
- **Background**: Soft Gray-Slate `#F8FAFC`
- **Card Surfaces**: Pure White `#FFFFFF` with `#E2E8F0` subtle borders and `shadow-2xs`
- **Text & Contrast**: High-contrast Slate `#0F172A` (Primary headers), `#64748B` (Secondary text)
- **Status Badges**:
  - `✨ AI Active`: Indigo background `#EEF2FF`, Text `#4338CA`
  - `Human Agent`: Emerald background `#ECFDF5`, Text `#047857`
  - `Escalated`: Amber background `#FFFBEB`, Text `#B45309`
  - `Resolved/Closed`: Slate background `#F1F5F9`, Text `#475569`

### Typography
- Font Family: `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `sans-serif`
- Headers: `font-black` (2xl), `font-bold` (lg/xl) with negative tracking (`tracking-tight`)
- Buttons & Chips: `font-extrabold` (xs/sm) for clear legibility and touch target emphasis

---

## 3. Responsive Breakpoint Behavior

- **Desktop (`>= 1024px`)**: Fixed 300px left conversation drawer + flex-1 central chat workspace.
- **Tablet (`768px - 1023px`)**: Collapsible conversation drawer with toggle button in header.
- **Mobile (`< 768px`)**: Full width single-column layout with sliding slide-over drawer for ticket list and sticky composer at bottom.

---

## 4. Contextual AI Action Protocol

Transactional views expose AI deep-linking triggers that seamlessly pass state into `ConversationalHome`:

```javascript
// Example: Deep-link from CustomerOrders to ConversationalHome
const handleAskAI = (order) => {
  navigate('/customer', {
    state: {
      initialMessage: `I have a question about Order ${order.order_id} placed on ${order.order_date}.`,
      contextCategory: 'Orders',
      orderId: order.order_id
    }
  })
}
```

Upon landing at `/customer`, `ConversationalHome` consumes `location.state` to automatically pre-fill the composer or launch a new contextual AI thread.

# 02 — User & Customer Identity Model Mapping Design

## Executive Summary
This document analyzes the relationship between the `User` model in `Customer-SupportHub` and the `Customer` entity in the ShopKart synthetic business dataset (`supporthub-data-generator`).

---

## 1. User Model Inspection (`Customer-SupportHub`)
- **Table Name**: `users` (`app/models/__init__.py`)
- **Primary Key**: `id` (`uuid.UUID`)
- **Key Fields**:
  - `email`: `str` (unique, indexed, max 255)
  - `name`: `str` (max 100)
  - `password_hash`: `str` (bcrypt)
  - `role`: `UserRole` (`customer`, `agent`, `manager`, `admin`)
  - `status`: `UserStatus` (`active`, `invited`, `suspended`)
  - `channel`: `Optional[ChannelType]` (`email`, `website_chat`, `whatsapp`, `instagram`, `facebook`)
  - `channel_customer_id`: `Optional[str]` (stores external channel ID e.g., phone for WhatsApp, IGSID for Instagram, PSID for Facebook, or `CUST-XXX` for ShopKart mapping)
  - `phone`: `Optional[str]`

---

## 2. Customer Model Inspection (`ShopKart Business Dataset`)
- **Dataclass / Schema**: `Customer` (`supporthub-ai-architecture/data_access/base.py`)
- **Primary Key**: `customer_id` (e.g., `CUST-001`, `CUST-002`)
- **Key Fields**:
  - `customer_id`: `str`
  - `company_id`: `str` (e.g. `shopkart`)
  - `first_name` & `last_name`: `str`
  - `email`: `str` (e.g., `aravind.swamy@gmail.com`)
  - `phone`: `str` (e.g., `919876543210`)
  - `address`, `city`, `state`, `postal_code`
  - `account_status`: `str` (`ACTIVE`, `INACTIVE`)

---

## 3. User ↔ Customer Relationship Audit
Currently, the `User` table represents all authenticated users (agents, admins, and registered web customers).
`LiveChatAIAdapter._resolve_customer_id(user)` bridges `User` to `Customer` as follows:

```python
def _resolve_customer_id(self, user: Optional[User]) -> str:
    if not user:
        return "GUEST"

    # Priority 1: Direct link via channel_customer_id if formatted as CUST-XXX
    if user.channel_customer_id and user.channel_customer_id.startswith("CUST-"):
        return user.channel_customer_id

    # Priority 2: Email lookup against ShopKart dataset
    for cid, cust in data_loader.customers.items():
        if user.email and cust.email and user.email.lower() == cust.email.lower():
            return cid

    # Priority 3: Fallback to channel_customer_id or user.id
    if user.channel_customer_id:
        return user.channel_customer_id

    return str(user.id)
```

---

## 4. Identity Mapping Design for Phase 12

> [!IMPORTANT]
> **Identity Mapping Rule**: The system must NOT rely solely on soft email matching during runtime. A explicit, immutable link must be established between `User` and `Customer`.

### Proposed Mapping Schema:
Add an explicit `customer_id` field to the `User` model or formalize `channel_customer_id` when `role == UserRole.customer`:

```
┌──────────────────────────────────────┐       1:1 Link       ┌──────────────────────────────────────┐
│           User (SupportHub)          │ ───────────────────> │        Customer (ShopKart)           │
├──────────────────────────────────────┤                      ├──────────────────────────────────────┤
│ id: UUID (PK)                        │                      │ customer_id: str (PK e.g. CUST-001)  │
│ email: str                           │                      │ company_id: str ("shopkart")         │
│ role: UserRole.customer              │                      │ first_name, last_name: str           │
│ customer_id: Optional[str]           │ ───────────────────> │ email: str                           │
└──────────────────────────────────────┘                      └──────────────────────────────────────┘
```

This ensures that upon authentication (`POST /auth/login`), the JWT payload or `User` session contains the immutable `customer_id` (e.g. `CUST-001`), which is passed directly to `AIOrchestrator` and tool execution layers.

# 06 — Authentication & Identity Audit

## Executive Summary
This report audits the authentication, identity mapping, and session management implementation in `Customer-SupportHub`, verifying token mechanics, role authorization, and identity consolidation.

---

## 1. Authentication Lifecycle

```
User Registration / Seed
    ↓ [Password Hashed via Passlib / BCrypt]
User Stored in PostgreSQL 'users' table
    ↓ [Login Request POST /api/v1/auth/login]
Credentials Verified & TOTP 2FA Checked (if enabled)
    ↓ [Generate JWT Access Token via PyJWT / python-jose]
JWT Token Returned to Client (Expires in 24 hours)
    ↓ [Client Header: Authorization: Bearer <token>]
FastAPI Dependency 'get_current_user' (app/dependencies.py)
    ↓ [Decode JWT & Query User Record]
User Entity Attached to Request State
```

---

## 2. User & Customer Identity Model Structure

The system utilizes a single unified `User` model (`app/models/__init__.py`) to represent both web interface users (Admins, Agents, Customers) and external omnichannel customers:

```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    role: UserRole = Field(default=UserRole.customer)  # admin, agent, customer, manager
    
    # Omnichannel Identity Links
    channel: Optional[ChannelType] = Field(default=None)        # WEBSITE, WHATSAPP, INSTAGRAM, FACEBOOK, EMAIL
    channel_customer_id: Optional[str] = Field(default=None)  # Phone number, IGSID, PSID
    phone: Optional[str] = Field(default=None)
    customer_id: Optional[str] = Field(default=None)          # Links to ShopKart business customer (e.g. CUST_001)
```

---

## 3. Audit Questions Answered

### Q1: Is there only ONE canonical identity architecture?
* **YES**. All user types (admin, agent, customer, guest, WhatsApp user, Instagram user) are anchored to the `User` table in PostgreSQL.

### Q2: Are there duplicate auth systems or legacy user tables?
* **NO**. There are no duplicate user tables or secondary auth middleware. `app/routers/auth.py` is the single source of truth for authentication.

### Q3: How is TOTP 2FA handled?
* `User.totp_secret` stores the secret key. `pyotp` verifies 6-digit codes during login if `totp_enabled` is set to `True`.

---

## 4. Verification Verdict
* **Security & Cleanliness**: **EXCELLENT**. Auth architecture is consolidated, robust, and free of redundant JWT or session layers.

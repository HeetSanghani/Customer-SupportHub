# 02 - Users Table Audit

## Overview
The `users` table in PostgreSQL is the single consolidated table representing both authentication credentials and user profile information across all roles (`customer`, `agent`, `manager`, `admin`).

## Table Schema (`users`)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role userrole NOT NULL DEFAULT 'customer',
    status userstatus NOT NULL DEFAULT 'invited',
    avatar_url TEXT,
    totp_secret VARCHAR,
    totp_enabled BOOLEAN DEFAULT FALSE,
    email_signature TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    channel channeltype,
    channel_customer_id VARCHAR(255),
    phone VARCHAR(30),
    customer_id VARCHAR(100),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(30),
    country VARCHAR(100),
    company_id VARCHAR(100)
);
```

## Field Breakdown & Audit Findings

| Field | Type | Constraint / Index | Audit Findings |
|-------|------|--------------------|----------------|
| `id` | UUID | Primary Key | Used as FK target for `tickets.customer_id`, `orders.customer_id`, `payments.customer_id`, `returns.customer_id`, `refunds.customer_id`, `csat_ratings.customer_id`. |
| `email` | VARCHAR(255) | UNIQUE, INDEX | Primary login credential for web/dashboard users. Required for manual registration. |
| `name` | VARCHAR(100) | NOT NULL | User's full name. |
| `password_hash` | VARCHAR(255) | NOT NULL | Securely hashed password using `bcrypt` (e.g. `$2b$12$...`). For channel-only customers, seeded with placeholder `__channel_customer__`. |
| `role` | UserRole (Enum) | DEFAULT 'customer' | Enum values: `'customer'`, `'agent'`, `'manager'`, `'admin'`. |
| `status` | UserStatus (Enum) | DEFAULT 'invited' | Enum values: `'active'`, `'invited'`, `'suspended'`. Active users can log in; suspended users return 403. |
| `channel` | ChannelType (Enum) | INDEX | Channel source if acquired via social/messaging (`email`, `website_chat`, `whatsapp`, `instagram`, `facebook`). |
| `channel_customer_id` | VARCHAR(255) | INDEX | External channel identifier (e.g. Phone number for WhatsApp `"9104398302"`, IG PSID `"17841..."`, or legacy customer ID `"CUST-001"`). |
| `phone` | VARCHAR(30) | INDEX | Customer telephone number. |
| `customer_id` | VARCHAR(100) | INDEX | String identifier linking to legacy ShopKart Customer ID (e.g., `'CUST-001'`). Nullable for newly registered web users until matched. |
| `address`, `city`, `state`, `postal_code`, `country` | Various | Nullable | Demographics and shipping profile details. |
| `company_id` | VARCHAR(100) | INDEX | Merchant company binding (e.g., `'COMP-001'`). |

## Key Findings & Security Assessment
1. **Password Security**: All standard user passwords are stored using bcrypt hashing. No plaintext passwords exist in `users`.
2. **Channel Users**: Omnichannel users (WhatsApp, Instagram) created via webhook ingest have `password_hash = '__channel_customer__'`, preventing direct password logins while allowing ticket creation.
3. **Identifier Duality**: The primary key `users.id` (UUID) is used as internal database foreign key, whereas `users.customer_id` (VARCHAR `CUST-XXX`) is used as business domain identifier in AI tools and ShopKart reports.

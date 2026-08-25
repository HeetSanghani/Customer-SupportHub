# 02 — Registration Flow

## Flow Diagram
`Browser (POST /auth/register)` -> `Request Validation` -> `Password Min Length (8 chars)` -> `bcrypt Hashing` -> `User Model Creation (PostgreSQL)` -> `Customer ID Resolution (MySQL Lookup by Email)` -> `User-Customer Binding`.

## Key Security Properties
- Passwords stored as `bcrypt` hashes in PostgreSQL.
- Email matching links user to `customer_id` server-side. Clients **cannot spoof** `customer_id`.

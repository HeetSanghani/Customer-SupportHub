# 12 — Anti-IDOR Customer Ownership Enforcement

## Core Principle
- Server derives caller identity from JWT token.
- Query params or request bodies asserting `customer_id` are ignored.

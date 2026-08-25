# 04 — User-Customer Relationship Model

## Identity Linking
- Staff accounts (`agent`, `manager`, `admin`) have `customer_id = NULL`.
- Pre-existing store customers have `customer_id = 'CUST-XXX'`.
- New self-registered customers start with `customer_id = NULL` ("Unlinked Account") until correlated with store purchases.

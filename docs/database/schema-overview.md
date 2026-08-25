# Database Schema & Architecture Overview

## Overview
PostgreSQL 16 is the **sole canonical database engine** for **Customer-SupportHub**. The database name is `supporthub`.

## Key Entity Models & Schema Relationships

```
                     ┌──────────────────┐
                     │      Users       │
                     │    (user_id)     │
                     └────────┬─────────┘
                              │ 1:1 Linkage
                              ▼
                     ┌──────────────────┐
                     │    Customers     │
                     │  (customer_id)   │
                     └────────┬─────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │ 1:N                  │ 1:N                  │ 1:N
       ▼                      ▼                      ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│   Orders    │        │  Payments   │        │   Returns   │
│ (order_id)  │        │(payment_id) │        │ (return_id) │
└──────┬──────┘        └─────────────┘        └──────┬──────┘
       │                                             │
       ├──────────────────────┐                      │ 1:1
       │ 1:N                  │ 1:1                  ▼
       ▼                      ▼               ┌─────────────┐
┌─────────────┐        ┌─────────────┐        │   Refunds   │
│ OrderItems  │        │  Shipments  │        │ (refund_id) │
│(item_id)    │        │(shipment_id)│        └─────────────┘
└─────────────┘        └─────────────┘
```

## Customer Ownership & Data Isolation
- **Direct Ownership**: `orders`, `payments`, `returns` contain a direct `customer_id` foreign key.
- **Indirect Ownership**: `order_items` and `shipments` inherit customer ownership through their parent `order_id`. `refunds` inherit ownership through parent `return_id`.
- **Anti-IDOR Enforcement**: `PostgresBusinessRepository` validates that requested `order_id`, `shipment_id`, `return_id`, or `refund_id` belongs strictly to the authenticated `customer_id`.

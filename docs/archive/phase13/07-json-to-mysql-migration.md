# 07. JSON to MySQL Migration Plan

## 1. Sequential Execution Order
1. `company.json`
2. `categories.json`
3. `sellers.json`
4. `products.json`
5. `customers.json`
6. `orders.json`
7. `order_items.json`
8. `payments.json`
9. `shipments.json`
10. `returns.json`
11. `refunds.json`

## 2. Strategy & ID Preservation
- Maintain exact primary key string IDs (`CUST-001`, `ORD-001`, etc.) to guarantee zero breakage with synthetic test scenarios.
- Rollback mechanism: script executes within atomic SQL transaction block.

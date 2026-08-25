# 04. JSON Data Model Specification

## 1. Data Schema Details
- **Customers**: `customer_id` (str), `first_name` (str), `email` (str), `phone` (str), `address` (str).
- **Orders**: `order_id` (str), `customer_id` (str), `status` (enum), `order_date` (datetime), `total_amount` (float).
- **Payments**: `payment_id` (str), `order_id` (str), `customer_id` (str), `amount` (float), `method` (enum), `status` (enum), `failure_reason` (str).
- **Shipments**: `shipment_id` (str), `order_id` (str), `tracking_number` (str), `carrier` (str), `status` (enum).
- **Returns**: `return_id` (str), `order_id` (str), `order_item_id` (str), `customer_id` (str), `reason` (str).
- **Refunds**: `refund_id` (str), `return_id` (str), `order_id` (str), `customer_id` (str), `refund_amount` (float).

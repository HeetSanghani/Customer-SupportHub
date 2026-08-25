# 06. Data Relationship & Ownership Map

## 1. Direct Ownership Entities (`customer_id`)
- `customers` (`customer_id`)
- `orders` (`customer_id`)
- `payments` (`customer_id`)
- `returns` (`customer_id`)
- `refunds` (`customer_id`)

## 2. Indirect Ownership Traversal Paths
- **Shipments**: `Shipment.shipment_id` → `Shipment.order_id` → `Order.order_id` → `Order.customer_id`
- **Order Items**: `OrderItem.order_item_id` → `OrderItem.order_id` → `Order.order_id` → `Order.customer_id`

## 3. Catalog & Reference Entities (Public/Shared)
- `company`
- `categories`
- `sellers`
- `products`

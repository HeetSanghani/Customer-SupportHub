# 05 — Business Data Source-of-Truth

## Source-of-Truth Mapping Table

| Entity | Generator JSON Location | MySQL 8.0 Table | PostgreSQL Table | Runtime Source of Truth | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **company** | `output/company.json` | `company` | None | **MySQL `company`** | Static company info |
| **categories** | `output/categories.json` | `categories` | None | **MySQL `categories`** | E-commerce categories |
| **sellers** | `output/sellers.json` | `sellers` | None | **MySQL `sellers`** | Seller directory |
| **products** | `output/products.json` | `products` | None | **MySQL `products`** | Product catalog + MRP |
| **customers** | `output/customers.json` | `customers` | None | **MySQL `customers`** | Customer business profile |
| **orders** | `output/orders.json` | `orders` | None | **MySQL `orders`** | Customer orders |
| **order_items**| `output/order_items.json` | `order_items` | None | **MySQL `order_items`** | Line items per order |
| **payments** | `output/payments.json` | `payments` | None | **MySQL `payments`** | Payment transaction records |
| **shipments** | `output/shipments.json` | `shipments` | None | **MySQL `shipments`** | Logistics tracking data |
| **returns** | `output/returns.json` | `returns` | None | **MySQL `returns`** | Product return requests |
| **refunds** | `output/refunds.json` | `refunds` | None | **MySQL `refunds`** | Financial refund records |

## Findings
- **Canonical Runtime Source**: MySQL 8.0 database `supporthub_business`.
- **JSON Role**: Source seed data only. Live application does NOT query JSON files at runtime.

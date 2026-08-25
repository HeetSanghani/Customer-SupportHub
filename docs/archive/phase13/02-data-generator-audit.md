# 02. Data Generator Audit

## 1. Synthetic ShopKart Dataset Summary
The synthetic dataset resides in `supporthub-data-generator/output` as 13 relational JSON entities created by `generate.py` and audited by `audit_dataset.py`.

## 2. Entity Audit Matrix
| Entity | JSON File | Record Count | Primary Key | Key Foreign Keys |
| :--- | :--- | :--- | :--- | :--- |
| Company | `company.json` | 1 | `company_id` | N/A |
| Categories | `categories.json` | 12 | `category_id` | `company_id`, `parent_category_id` |
| Sellers | `sellers.json` | 10 | `seller_id` | `company_id` |
| Products | `products.json` | 40 | `product_id` | `company_id`, `seller_id`, `category_id` |
| Customers | `customers.json` | 25 | `customer_id` | `company_id` |
| Orders | `orders.json` | 25 | `order_id` | `company_id`, `customer_id` |
| Order Items | `order_items.json` | 27 | `order_item_id` | `order_id`, `product_id` |
| Payments | `payments.json` | 27 | `payment_id` | `order_id`, `customer_id` |
| Shipments | `shipments.json` | 25 | `shipment_id` | `order_id` |
| Returns | `returns.json` | 6 | `return_id` | `order_id`, `order_item_id`, `customer_id` |
| Refunds | `refunds.json` | 4 | `refund_id` | `return_id`, `order_id`, `customer_id` |
| Policies | `policies.json` | 10 | `policy_id` | `company_id` |
| Articles | `knowledge_articles.json` | 13 | `article_id` | `company_id` |

## 3. Dataset Audit Status
- Audit Status: **READY** (Passed 100% of relationship, business logic, and policy audit checks).

# Phase 13.2 Manual Validation Bug Investigation Report

**Final Status**: `ROOT_CAUSE_IDENTIFIED`

---

## Executive Summary

An investigation was conducted into the two behavioral issues identified during Phase 13.2 manual validation testing. The root causes for both issues have been conclusively identified without modifying production code, database schema, or data.

---

## Summary of Findings

### Observed Issue 1 — Stale / Incorrect Shipment Response
- **Symptom**: Query 1 (`"Is PROD-001 available?"`) followed by Query 2 (`"Where is my shipment?"`) returns the `PROD-001` product availability response again for Query 2.
- **Root Cause**:
  1. `ai/intent.py` is missing `"where is my shipment"` in the keyword rules for `SHIPMENT_INQUIRY`.
  2. `IntentClassifier.classify()` unconditionally merges context slots (`active_product_id="PROD-001"`) into `entities` at the start of classification.
  3. Because the query does not match steps 1–10, classification falls through to Step 11 (`PRODUCT_INQUIRY`), where `if "product_id" in entities:` evaluates to `True` due to context slot inheritance.
  4. `AIRouter` routes the query to `get_product("PROD-001")`, returning the stale product details.

### Observed Issue 2 — Product MRP Becomes Zero
- **Symptom**: Product queries for `PROD-001` and `PROD-002` return `Price: ₹46,999.00 (MRP: ₹0.00, Discount: 0.0%)`.
- **Root Cause**:
  1. The MySQL `products` database table schema in `supporthub_business` was created without an `mrp` column (`product_id`, `company_id`, `seller_id`, `category_id`, `name`, `brand`, `description`, `price`, `stock_quantity`, `specifications`, `created_at`).
  2. `MySQLRepository.map_product()` executes `row.get("mrp")`, which returns `None` because the column is absent.
  3. `_to_float(None)` converts `None` to `0.0`, resulting in `MRP: ₹0.00` and `Discount: 0.0%` in all product responses.

---

## Detailed System Trace & Evidence

### Issue 1 Trace (Turn 2: "Where is my shipment?")
- **Input Context Slots**: `{'order_id': None, 'product_id': 'PROD-001', 'return_id': None, 'refund_id': None}`
- **Entities Extracted**: `{'product_id': 'PROD-001'}` (inherited from context slots)
- **Detected Intent**: `PRODUCT_INQUIRY` (Category: `product`)
- **Route**: `STRUCTURED`
- **Selected Tools**: `['get_product']`
- **Tool Arguments**: `product_id="PROD-001"`
- **Response Source**: `ResponseSynthesizer.synthesize_structured_response()`

### Issue 2 Database Inspection (`DESCRIBE products;`)
```sql
+---------------------+---------------+------+-----+-------------------+-------------------+
| Field               | Type          | Null | Key | Default           | Extra             |
+---------------------+---------------+------+-----+-------------------+-------------------+
| product_id          | varchar(50)   | NO   | PRI | NULL              |                   |
| company_id          | varchar(50)   | NO   | MUL | NULL              |                   |
| seller_id           | varchar(50)   | NO   | MUL | NULL              |                   |
| category_id         | varchar(50)   | NO   | MUL | NULL              |                   |
| name                | varchar(255)  | NO   |     | NULL              |                   |
| brand               | varchar(100)  | YES  |     | NULL              |                   |
| description         | text          | YES  |     | NULL              |                   |
| price               | decimal(10,2) | NO   |     | NULL              |                   |
| stock_quantity      | int           | YES  |     | 0                 |                   |
| specifications      | json          | YES  |     | NULL              |                   |
| created_at          | timestamp     | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+---------------------+---------------+------+-----+-------------------+-------------------+
```
*Note: Column `mrp` is missing from the table DDL.*

### Data Generator Ground Truth (`output/products.json`)
- `PROD-001`: `price`: `46999.0`, `mrp`: `54999.0`
- `PROD-002`: `price`: `27499.0`, `mrp`: `32999.0`

---

## Responsible Files & Classes

1. **Issue 1**:
   - `supporthub-ai-architecture/ai/intent.py` (`IntentClassifier.classify`)
   - `supporthub-ai-architecture/ai/response.py` (`ResponseSynthesizer.synthesize_structured_response`)
2. **Issue 2**:
   - MySQL `supporthub_business` Database Schema (`products` Table DDL)
   - `supporthub-ai-architecture/data_access/mysql_repository.py` (`MySQLRepository.map_product`)

---

## Independence & Security Status

- **Problem Independence**: The two issues are completely independent.
- **Security Boundaries**: Fully intact. Anti-IDOR, customer-scoped authorization, and prompt-injection defenses operate correctly without vulnerability.

---

## Final Status

`ROOT_CAUSE_IDENTIFIED`

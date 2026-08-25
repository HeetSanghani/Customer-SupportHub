# 03 - Customers Table Audit

## Current Architecture Status: MERGED INTO USERS

In the legacy architecture (prior to Phase 14), the application maintained a separate MySQL `customers` table in `supporthub_business` alongside a PostgreSQL `users` table in `supporthub`.

As of Phase 14/15, **there is NO standalone `customers` table in PostgreSQL**. The `customers` domain model has been completely merged into the single unified `users` table in PostgreSQL.

## Former `customers` Table Schema vs Current `users` Column Mapping

| Legacy MySQL `customers` Column | Unified PostgreSQL `users` Column | Status in Current DB |
|----------------------------------|------------------------------------|----------------------|
| `customer_id` (VARCHAR PK `CUST-001`) | `users.customer_id` (VARCHAR(100)) & `users.id` (UUID PK) | Preserved as indexed column `customer_id` on `users` |
| `company_id` | `users.company_id` | Preserved |
| `first_name` + `last_name` | `users.name` (FULL NAME) | Merged into `name`; split dynamically in repository when mapping to domain objects |
| `email` | `users.email` (UNIQUE) | Preserved |
| `phone` | `users.phone` | Preserved |
| `address` | `users.address` | Preserved |
| `city` | `users.city` | Preserved |
| `state` | `users.state` | Preserved |
| `postal_code` | `users.postal_code` | Preserved |
| `country` | `users.country` | Preserved |
| `account_status` | `users.status` | Mapped to `UserStatus` enum |
| `created_at` | `users.created_at` | Preserved |

## Data Access Layer Translation (`CustomerService` & `MySQLRepository`)
Although the physical SQL table `customers` was removed, domain logic (`app/data_access/customer_service.py` & `mysql_repository.py`) continues to provide `Customer` dataclass instances via SQL queries against the unified `users` table:

```python
# Query from MySQLRepository mapping users row to Customer dataclass:
def get_customer(self, customer_id: str) -> Optional[Customer]:
    with self.db.cursor() as cur:
        if _is_valid_uuid(customer_id):
            cur.execute("SELECT * FROM users WHERE id = %s LIMIT 1;", (customer_id,))
        else:
            cur.execute("SELECT * FROM users WHERE customer_id = %s LIMIT 1;", (customer_id,))
        row = cur.fetchone()
        return self.map_customer(row) if row else None
```

## Audit Conclusion
- Standalone `customers` table count in PostgreSQL: **0 (Table does not exist)**
- Customer entities represented in PostgreSQL `users` table: **352 user rows**
- Business backward compatibility: Fully maintained via `users.customer_id` and repository translation layer.

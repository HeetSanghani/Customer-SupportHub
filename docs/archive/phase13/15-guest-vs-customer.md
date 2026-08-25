# 15. Guest vs Customer Access Control

| Query Type | Guest User | Authenticated Customer |
| :--- | :---: | :---: |
| Company Policy / FAQ | ALLOWED | ALLOWED |
| Product Catalog Search | ALLOWED | ALLOWED |
| Personal Orders / Payments | BLOCKED (Login Required) | ALLOWED (Owned Data Only) |
| Cross-Customer Data Access | BLOCKED | BLOCKED |

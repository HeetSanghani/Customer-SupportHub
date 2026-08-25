# 18. Multi-Tenant Future Design

Supporting multiple client companies (ShopKart, Company A, Company B):
- Composite primary key / index: `tenant_id` + `customer_id`.
- Vector store metadata filtering by `tenant_id`.

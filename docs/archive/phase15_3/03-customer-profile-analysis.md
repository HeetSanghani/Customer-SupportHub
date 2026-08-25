# 03 — Customer Profile Analysis

## Profile Data Boundaries
- Customer profiles allow reading and updating contact information and shipping addresses.
- Security-critical fields (`id`, `customer_id`, `role`, `status`, `password_hash`) are immutable from client endpoints.

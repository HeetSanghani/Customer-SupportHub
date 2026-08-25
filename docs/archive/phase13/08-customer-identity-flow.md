# 08. Customer Identity Flow

## Identity Chain
`SupportHub User (User.id)` → `User.customer_id ("CUST-001")` → `MySQL Customer (customers.customer_id)`

## Behavior Matrix
- **Existing Customer**: Logged in, valid `customer_id` → Personal data access granted.
- **New User**: Registered, `customer_id=None` → Prompted to link e-commerce identity; personal queries blocked by Guest Guard.
- **Guest**: Unauthenticated → Access restricted to public FAQs/policies.

# 17. Database Boundary Decision

## Recommendation: Option B (Separate Databases / Clean Service Boundary)
- **SupportHub Database** (PostgreSQL): Manages operational chat state (`users`, `tickets`, `messages`, `channels`).
- **ShopKart Business Database** (MySQL): Manages e-commerce business data (`customers`, `orders`, `payments`, `products`).
- Interacts purely through defined Python data access interfaces.

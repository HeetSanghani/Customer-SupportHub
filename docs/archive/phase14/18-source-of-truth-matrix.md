# 18 — Source-of-Truth Matrix

| Component / Domain | Current Project | Canonical Source of Truth | Notes |
| :--- | :--- | :--- | :--- |
| **Authentication & Users**| `Customer-SupportHub` | PostgreSQL `users` table | Server-authoritative |
| **Customer Business Data**| `supporthub-ai-architecture` | MySQL `customers` table | Query via PyMySQL repo |
| **Orders & Items** | `supporthub-ai-architecture` | MySQL `orders` / `order_items` | Query via PyMySQL repo |
| **Products & Pricing** | `supporthub-ai-architecture` | MySQL `products` table | Includes MRP column |
| **Payments & Refunds** | `supporthub-ai-architecture` | MySQL `payments` / `refunds` | Masked sensitive fields |
| **Shipments & Logistics** | `supporthub-ai-architecture` | MySQL `shipments` table | Tracking IDs |
| **AI Orchestration** | `supporthub-ai-architecture` | `ai/orchestrator.py` | Primary AI engine |
| **Policy Knowledge Base** | `supporthub-ai-architecture` | `rag/documents/policies/` | Vectorized in pgvector |
| **Quick Replies** | `Customer-SupportHub` | PostgreSQL `quick_replies` table | Managed via Admin API |
| **Tickets & Messages** | `Customer-SupportHub` | PostgreSQL `tickets` / `messages` | Live Chat storage |

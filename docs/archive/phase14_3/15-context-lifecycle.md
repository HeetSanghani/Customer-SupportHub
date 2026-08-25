# 15 — Context Lifecycle

- **Slots**: `active_order_id`, `active_product_id`, `active_return_id`, `active_refund_id`.
- **Domain Isolation**: Product turn clears active order slot to prevent context bleed.
- **Reversion**: Unauthorized entity access reverts slots to pre-turn snapshot.

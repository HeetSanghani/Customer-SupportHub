"""Order data service."""
from typing import Optional, List, Dict, Any
from app.data_access.base import Order, OrderItem
from app.data_access.postgres_business_repository import postgres_business_repository, PostgresBusinessRepository


class OrderService:
    """Service for querying ShopKart orders and line items."""

    def __init__(
        self,
        loader: Optional[Any] = None,
        repository: Optional[PostgresBusinessRepository] = None,
    ):
        self.loader = loader
        self.repo = repository or postgres_business_repository

    def get_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Order]:
        """Fetch order by ID, enforcing customer scoping if customer_id is provided."""
        if self.loader is not None:
            self.loader.load()
            order = self.loader.orders.get(order_id)
            if order and customer_id and customer_id != "ADMIN" and order.customer_id != customer_id:
                return None
            return order
        return self.repo.get_order(order_id, customer_id=customer_id)

    def get_customer_orders(self, customer_id: str) -> List[Order]:
        """Fetch all orders placed by a specific customer."""
        if self.loader is not None:
            self.loader.load()
            return [o for o in self.loader.orders.values() if o.customer_id == customer_id]
        return self.repo.get_customer_orders(customer_id)

    def get_order_items(self, order_id: str, customer_id: Optional[str] = None) -> List[OrderItem]:
        """Fetch line items belonging to an order."""
        if self.loader is not None:
            self.loader.load()
            order = self.get_order(order_id, customer_id=customer_id)
            if not order:
                return []
            return [oi for oi in self.loader.order_items.values() if oi.order_id == order_id]
        return self.repo.get_order_items(order_id, customer_id=customer_id)

    def get_order_full_details(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetch order record along with customer, line items, product, shipment, and payment details."""
        if self.loader is not None:
            self.loader.load()
            order = self.get_order(order_id, customer_id=customer_id)
            if not order:
                return None

            items = self.get_order_items(order_id, customer_id=customer_id)
            items_detail = []
            for item in items:
                product = self.loader.products.get(item.product_id)
                items_detail.append({
                    "order_item_id": item.order_item_id,
                    "product_id": item.product_id,
                    "product_name": product.name if product else "Unknown Product",
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price
                })

            shipment = next((s for s in self.loader.shipments.values() if s.order_id == order_id), None)
            payment = next((p for p in self.loader.payments.values() if p.order_id == order_id), None)

            return {
                "order": order,
                "items": items_detail,
                "shipment": shipment,
                "payment": payment
            }
        return self.repo.get_order_full_details(order_id, customer_id=customer_id)

    def list_all_orders(self) -> List[Order]:
        """Return list of all orders."""
        if self.loader is not None:
            self.loader.load()
            return list(self.loader.orders.values())
        return self.repo.list_all_orders()

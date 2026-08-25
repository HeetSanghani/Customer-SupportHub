"""Shipment and logistics data service."""
from typing import Optional, List, Any
from app.data_access.base import Shipment
from app.data_access.postgres_business_repository import postgres_business_repository, PostgresBusinessRepository


class ShipmentService:
    """Service for querying ShopKart logistics and tracking records."""

    def __init__(
        self,
        loader: Optional[Any] = None,
        repository: Optional[PostgresBusinessRepository] = None,
    ):
        self.loader = loader
        self.repo = repository or postgres_business_repository

    def get_shipment(self, shipment_id: str, customer_id: Optional[str] = None) -> Optional[Shipment]:
        """Fetch shipment by ID, enforcing customer ownership via Order chain."""
        if self.loader is not None:
            self.loader.load()
            ship = self.loader.shipments.get(shipment_id)
            if ship and customer_id and customer_id != "ADMIN":
                order = self.loader.orders.get(ship.order_id)
                if not order or order.customer_id != customer_id:
                    return None
            return ship
        return self.repo.get_shipment(shipment_id, customer_id=customer_id)

    def get_shipment_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Shipment]:
        """Fetch shipment associated with an order ID."""
        if self.loader is not None:
            self.loader.load()
            if customer_id and customer_id != "ADMIN":
                order = self.loader.orders.get(order_id)
                if not order or order.customer_id != customer_id:
                    return None
            for ship in self.loader.shipments.values():
                if ship.order_id == order_id:
                    return ship
            return None
        return self.repo.get_shipment_by_order(order_id, customer_id=customer_id)

    def get_shipment_by_tracking(self, tracking_number: str, customer_id: Optional[str] = None) -> Optional[Shipment]:
        """Fetch shipment by courier tracking number."""
        if self.loader is not None:
            self.loader.load()
            clean_num = tracking_number.strip().upper()
            for ship in self.loader.shipments.values():
                if ship.tracking_number.strip().upper() == clean_num:
                    if customer_id and customer_id != "ADMIN":
                        order = self.loader.orders.get(ship.order_id)
                        if not order or order.customer_id != customer_id:
                            return None
                    return ship
            return None
        return self.repo.get_shipment_by_tracking(tracking_number, customer_id=customer_id)

    def list_all_shipments(self) -> List[Shipment]:
        """Return list of all shipments."""
        if self.loader is not None:
            self.loader.load()
            return list(self.loader.shipments.values())
        return self.repo.list_all_shipments()

"""Refund data service."""
from typing import Optional, List, Any
from app.data_access.base import Refund
from app.data_access.postgres_business_repository import postgres_business_repository, PostgresBusinessRepository


class RefundService:
    """Service for querying ShopKart refund records."""

    def __init__(
        self,
        loader: Optional[Any] = None,
        repository: Optional[PostgresBusinessRepository] = None,
    ):
        self.loader = loader
        self.repo = repository or postgres_business_repository

    def get_refund(self, refund_id: str, customer_id: Optional[str] = None) -> Optional[Refund]:
        """Fetch refund record by ID, enforcing customer ownership."""
        if self.loader is not None:
            self.loader.load()
            ref = self.loader.refunds.get(refund_id)
            if ref and customer_id and customer_id != "ADMIN" and ref.customer_id != customer_id:
                return None
            return ref
        return self.repo.get_refund(refund_id, customer_id=customer_id)

    def get_refund_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Refund]:
        """Fetch refund record associated with an order ID."""
        if self.loader is not None:
            self.loader.load()
            for ref in self.loader.refunds.values():
                if ref.order_id == order_id:
                    if customer_id and customer_id != "ADMIN" and ref.customer_id != customer_id:
                        return None
                    return ref
            return None
        return self.repo.get_refund_by_order(order_id, customer_id=customer_id)

    def get_refund_by_return(self, return_id: str, customer_id: Optional[str] = None) -> Optional[Refund]:
        """Fetch refund record associated with a return ID."""
        if self.loader is not None:
            self.loader.load()
            for ref in self.loader.refunds.values():
                if ref.return_id == return_id:
                    if customer_id and customer_id != "ADMIN" and ref.customer_id != customer_id:
                        return None
                    return ref
            return None
        return self.repo.get_refund_by_return(return_id, customer_id=customer_id)

    def get_customer_refunds(self, customer_id: str) -> List[Refund]:
        """Fetch all refunds issued to a customer."""
        if self.loader is not None:
            self.loader.load()
            return [r for r in self.loader.refunds.values() if r.customer_id == customer_id]
        return self.repo.get_customer_refunds(customer_id)

    def list_all_refunds(self) -> List[Refund]:
        """Return list of all refunds."""
        if self.loader is not None:
            self.loader.load()
            return list(self.loader.refunds.values())
        return self.repo.list_all_refunds()

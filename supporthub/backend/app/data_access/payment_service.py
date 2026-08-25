"""Payment data service."""
from typing import Optional, List, Any
from app.data_access.base import Payment
from app.data_access.postgres_business_repository import postgres_business_repository, PostgresBusinessRepository


class PaymentService:
    """Service for querying ShopKart payment transactions."""

    def __init__(
        self,
        loader: Optional[Any] = None,
        repository: Optional[PostgresBusinessRepository] = None,
    ):
        self.loader = loader
        self.repo = repository or postgres_business_repository

    def get_payment(self, payment_id: str, customer_id: Optional[str] = None) -> Optional[Payment]:
        """Fetch payment by ID, enforcing customer ownership."""
        if self.loader is not None:
            self.loader.load()
            pay = self.loader.payments.get(payment_id)
            if pay and customer_id and customer_id != "ADMIN" and pay.customer_id != customer_id:
                return None
            return pay
        return self.repo.get_payment(payment_id, customer_id=customer_id)

    def get_payment_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Payment]:
        """Fetch payment record associated with an order."""
        if self.loader is not None:
            self.loader.load()
            for pay in self.loader.payments.values():
                if pay.order_id == order_id:
                    if customer_id and customer_id != "ADMIN" and pay.customer_id != customer_id:
                        return None
                    return pay
            return None
        return self.repo.get_payment_by_order(order_id, customer_id=customer_id)

    def get_customer_payments(self, customer_id: str) -> List[Payment]:
        """Fetch all payments initiated by a customer."""
        if self.loader is not None:
            self.loader.load()
            return [p for p in self.loader.payments.values() if p.customer_id == customer_id]
        return self.repo.get_customer_payments(customer_id)

    def list_all_payments(self) -> List[Payment]:
        """Return list of all payments."""
        if self.loader is not None:
            self.loader.load()
            return list(self.loader.payments.values())
        return self.repo.list_all_payments()

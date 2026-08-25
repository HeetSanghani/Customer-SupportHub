"""Return data service."""
from typing import Optional, List, Any
from app.data_access.base import Return
from app.data_access.postgres_business_repository import postgres_business_repository, PostgresBusinessRepository


class ReturnService:
    """Service for querying ShopKart product returns."""

    def __init__(
        self,
        loader: Optional[Any] = None,
        repository: Optional[PostgresBusinessRepository] = None,
    ):
        self.loader = loader
        self.repo = repository or postgres_business_repository

    def get_return(self, return_id: str, customer_id: Optional[str] = None) -> Optional[Return]:
        """Fetch return request by ID, enforcing customer ownership."""
        if self.loader is not None:
            self.loader.load()
            ret = self.loader.returns.get(return_id)
            if ret and customer_id and customer_id != "ADMIN" and ret.customer_id != customer_id:
                return None
            return ret
        return self.repo.get_return(return_id, customer_id=customer_id)

    def get_return_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Return]:
        """Fetch return request associated with an order ID."""
        if self.loader is not None:
            self.loader.load()
            for ret in self.loader.returns.values():
                if ret.order_id == order_id:
                    if customer_id and customer_id != "ADMIN" and ret.customer_id != customer_id:
                        return None
                    return ret
            return None
        return self.repo.get_return_by_order(order_id, customer_id=customer_id)

    def get_customer_returns(self, customer_id: str) -> List[Return]:
        """Fetch all returns requested by a customer."""
        if self.loader is not None:
            self.loader.load()
            return [r for r in self.loader.returns.values() if r.customer_id == customer_id]
        return self.repo.get_customer_returns(customer_id)

    def list_all_returns(self) -> List[Return]:
        """Return list of all return requests."""
        if self.loader is not None:
            self.loader.load()
            return list(self.loader.returns.values())
        return self.repo.list_all_returns()

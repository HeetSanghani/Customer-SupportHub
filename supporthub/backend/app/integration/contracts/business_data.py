"""Standardized abstract interfaces for e-commerce business data access."""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class BusinessDataService(ABC):
    """Base interface for tenant-scoped business data adapters."""

    @abstractmethod
    def get_customer(self, customer_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Fetch customer profile scoped by tenant."""
        pass

    @abstractmethod
    def get_product(self, product_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Fetch product details scoped by tenant."""
        pass

    @abstractmethod
    def search_products(self, query: str, tenant_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search products within tenant catalog."""
        pass

    @abstractmethod
    def get_seller(self, seller_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Fetch merchant profile scoped by tenant."""
        pass

    @abstractmethod
    def get_order(self, order_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Fetch order record scoped by tenant."""
        pass

    @abstractmethod
    def get_customer_orders(self, customer_id: str, tenant_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch orders belonging to a specific customer within a tenant."""
        pass

    @abstractmethod
    def get_order_items(self, order_id: str, tenant_id: str) -> List[Dict[str, Any]]:
        """Fetch order line items scoped by tenant."""
        pass

    @abstractmethod
    def get_payment(self, payment_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Fetch payment transaction record scoped by tenant."""
        pass

    @abstractmethod
    def get_shipment(self, shipment_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Fetch shipment tracking record scoped by tenant."""
        pass

    @abstractmethod
    def get_return(self, return_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Fetch return request record scoped by tenant."""
        pass

    @abstractmethod
    def get_refund(self, refund_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Fetch refund ledger record scoped by tenant."""
        pass

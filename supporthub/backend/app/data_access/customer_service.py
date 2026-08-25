"""Customer data service."""
from typing import Optional, List, Any
from app.data_access.base import Customer
from app.data_access.postgres_business_repository import postgres_business_repository, PostgresBusinessRepository
from app.data_access.loader import DataLoader, data_loader


class CustomerService:
    """Service providing customer data access with automatic fallback between JSON memory cache and DB."""

    def __init__(
        self,
        loader: Optional[Any] = None,
        repository: Optional[PostgresBusinessRepository] = None,
    ):
        self.loader = loader
        self.repo = repository or postgres_business_repository

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Fetch customer profile by ID."""
        if self.loader is not None:
            self.loader.load()
            return self.loader.customers.get(customer_id)
        return self.repo.get_customer(customer_id)

    def search_customer_by_phone(self, phone: str) -> Optional[Customer]:
        """Lookup customer by phone number."""
        if self.loader is not None:
            self.loader.load()
            clean_phone = "".join(filter(str.isdigit, phone))
            for customer in self.loader.customers.values():
                cust_clean = "".join(filter(str.isdigit, customer.phone))
                if cust_clean and (cust_clean == clean_phone or cust_clean.endswith(clean_phone) or clean_phone.endswith(cust_clean)):
                    return customer
            return None
        return self.repo.search_customer_by_phone(phone)

    def search_customer_by_email(self, email: str) -> Optional[Customer]:
        """Lookup customer by email address."""
        if self.loader is not None:
            self.loader.load()
            clean_email = email.strip().lower()
            for customer in self.loader.customers.values():
                if customer.email.strip().lower() == clean_email:
                    return customer
            return None
        return self.repo.search_customer_by_email(email)

    def list_all_customers(self) -> List[Customer]:
        """Return list of all registered customers."""
        if self.loader is not None:
            self.loader.load()
            return list(self.loader.customers.values())
        return self.repo.list_all_customers()

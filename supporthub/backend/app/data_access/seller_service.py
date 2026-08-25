"""Seller data service."""
from typing import Optional, List, Any
from app.data_access.base import Seller
from app.data_access.postgres_business_repository import postgres_business_repository, PostgresBusinessRepository


class SellerService:
    """Service for querying ShopKart seller information."""

    def __init__(
        self,
        loader: Optional[Any] = None,
        repository: Optional[PostgresBusinessRepository] = None,
    ):
        self.loader = loader
        self.repo = repository or postgres_business_repository

    def get_seller(self, seller_id: str) -> Optional[Seller]:
        """Fetch seller profile by ID."""
        if not seller_id:
            return None
        if self.loader is not None:
            self.loader.load()
            sid = seller_id.upper()
            if sid.startswith("SELLER-"):
                sid = sid.replace("SELLER-", "SELL-")
            return self.loader.sellers.get(sid) or self.loader.sellers.get(seller_id)
        return self.repo.get_seller(seller_id)

    def get_seller_by_product(self, product_id: str) -> Optional[Seller]:
        """Fetch the seller associated with a specific product."""
        if self.loader is not None:
            self.loader.load()
            product = self.loader.products.get(product_id)
            if product and product.seller_id:
                return self.loader.sellers.get(product.seller_id)
            return None
        return self.repo.get_seller_by_product(product_id)

    def search_seller_by_name(self, name: str) -> Optional[Seller]:
        """Search seller by name or store brand."""
        if self.loader is not None:
            self.loader.load()
            q = name.lower().strip()
            for s in self.loader.sellers.values():
                if q in s.seller_name.lower():
                    return s
            return None
        return self.repo.search_seller_by_name(name)

    def list_all_sellers(self) -> List[Seller]:
        """Return list of all registered sellers."""
        if self.loader is not None:
            self.loader.load()
            return list(self.loader.sellers.values())
        return self.repo.list_all_sellers()

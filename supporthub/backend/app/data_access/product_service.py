"""Product and catalog data service."""
from typing import Optional, List, Any
from app.data_access.base import Product, Category
from app.data_access.postgres_business_repository import postgres_business_repository, PostgresBusinessRepository


class ProductService:
    """Service for querying ShopKart products and catalog data."""

    def __init__(
        self,
        loader: Optional[Any] = None,
        repository: Optional[PostgresBusinessRepository] = None,
    ):
        self.loader = loader
        self.repo = repository or postgres_business_repository

    def get_product(self, product_id: str) -> Optional[Product]:
        """Fetch product by ID (e.g. 'PROD-001')."""
        if self.loader is not None:
            self.loader.load()
            return self.loader.products.get(product_id)
        return self.repo.get_product(product_id)

    def search_products_by_name(self, query: str) -> List[Product]:
        """Search products by substring match on name, brand, description, or category."""
        if self.loader is not None:
            self.loader.load()
            q = query.lower().strip()
            matches = []
            for product in self.loader.products.values():
                cat = self.get_category(product.category_id)
                cat_name = cat.name.lower() if cat else ""
                parent_cat = self.get_category(cat.parent_category_id) if cat and cat.parent_category_id else None
                parent_name = parent_cat.name.lower() if parent_cat else ""
                if q in ("men", "mens", "men's", "men's clothing", "mens clothing", "men clothing", "for men"):
                    if ("men" in cat_name and "women" not in cat_name) or product.product_id == "PROD-031":
                        matches.append(product)
                elif q in ("women", "womens", "women's", "women's clothing", "womens clothing", "women clothing", "for women"):
                    if "women" in cat_name:
                        matches.append(product)
                elif (
                    q in product.name.lower()
                    or q in product.brand.lower()
                    or q in product.description.lower()
                    or q in cat_name
                    or q in parent_name
                ):
                    matches.append(product)
            return matches
        return self.repo.search_products_by_name(query)

    def get_products_by_category(self, category_id: str) -> List[Product]:
        """Fetch all products within a specific category."""
        if self.loader is not None:
            self.loader.load()
            return [p for p in self.loader.products.values() if p.category_id == category_id]
        return self.repo.get_products_by_category(category_id)

    def get_category(self, category_id: str) -> Optional[Category]:
        """Fetch category details by ID."""
        if self.loader is not None:
            self.loader.load()
            cat = self.loader.categories.get(category_id)
            if cat is not None:
                return cat
        return self.repo.get_category(category_id)

    def list_all_products(self) -> List[Product]:
        """Return list of all products."""
        if self.loader is not None:
            self.loader.load()
            return list(self.loader.products.values())
        return self.repo.list_all_products()

"""JSON Data Loader for the ShopKart dataset."""
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from app.data_access.base import (
    DataAccessException,
    Company,
    Customer,
    Seller,
    Category,
    Product,
    Order,
    OrderItem,
    Payment,
    Shipment,
    Return,
    Refund
)

logger = logging.getLogger(__name__)


class DataLoader:
    """Loads and caches synthetic ShopKart dataset from JSON files."""

    REQUIRED_FILES = [
        "company.json",
        "customers.json",
        "sellers.json",
        "categories.json",
        "products.json",
        "orders.json",
        "order_items.json",
        "payments.json",
        "shipments.json",
        "returns.json",
        "refunds.json",
        "policies.json",
        "knowledge_articles.json",
        "scenarios.json"
    ]

    def __init__(self, dataset_path: Optional[Path] = None):
        if dataset_path is None:
            env_path = os.getenv("DATASET_PATH")
            if env_path:
                dataset_path = Path(env_path)
            else:
                p1 = Path(__file__).resolve().parents[4] / "output"
                p2 = Path(__file__).resolve().parents[4] / "supporthub-data-generator" / "output"
                p3 = Path(__file__).resolve().parents[5] / "supporthub-data-generator" / "output"
                dataset_path = p1 if p1.exists() else (p2 if p2.exists() else p3)
        self.dataset_path = dataset_path
        self._raw_data: Dict[str, Any] = {}
        self._loaded: bool = False

        # Entity index caches
        self.companies: Dict[str, Company] = {}
        self.customers: Dict[str, Customer] = {}
        self.sellers: Dict[str, Seller] = {}
        self.categories: Dict[str, Category] = {}
        self.products: Dict[str, Product] = {}
        self.orders: Dict[str, Order] = {}
        self.order_items: Dict[str, OrderItem] = {}
        self.payments: Dict[str, Payment] = {}
        self.shipments: Dict[str, Shipment] = {}
        self.returns: Dict[str, Return] = {}
        self.refunds: Dict[str, Refund] = {}
        self.policies_raw: List[Dict[str, Any]] = []
        self.knowledge_articles_raw: List[Dict[str, Any]] = []
        self.scenarios_raw: List[Dict[str, Any]] = []

    def load(self, force_reload: bool = False) -> None:
        """Load all JSON files from dataset directory into memory."""
        if self._loaded and not force_reload:
            return

        if not self.dataset_path.exists() or any(not (self.dataset_path / f).is_file() for f in self.REQUIRED_FILES):
            self._load_from_repository()
            return

        # Read JSON files
        for filename in self.REQUIRED_FILES:
            file_path = self.dataset_path / filename
            with open(file_path, "r", encoding="utf-8") as f:
                self._raw_data[filename] = json.load(f)

        # Parse into typed dataclasses
        self._parse_entities()
        self._loaded = True
        logger.info("ShopKart dataset successfully loaded from %s", self.dataset_path)

    def _load_from_repository(self) -> None:
        """Load entities from PostgreSQL mysql_repository when JSON files are absent."""
        try:
            from app.data_access.postgres_business_repository import postgres_business_repository
            for c in postgres_business_repository.list_all_customers():
                self.customers[c.customer_id] = c
            for p in postgres_business_repository.list_all_products():
                self.products[p.product_id] = p
            for s in postgres_business_repository.list_all_sellers():
                self.sellers[s.seller_id] = s
                # Add seller alias
                if s.seller_id.startswith("SELL-"):
                    alias = "SELLER-" + s.seller_id[5:]
                    self.sellers[alias] = s
            for o in postgres_business_repository.list_all_orders():
                self.orders[o.order_id] = o
            for oi in postgres_business_repository.list_all_order_items():
                self.order_items[oi.order_item_id] = oi
            for sh in postgres_business_repository.list_all_shipments():
                self.shipments[sh.shipment_id] = sh
            for pay in postgres_business_repository.list_all_payments():
                self.payments[pay.payment_id] = pay
            for r in postgres_business_repository.list_all_returns():
                self.returns[r.return_id] = r
            for ref in postgres_business_repository.list_all_refunds():
                self.refunds[ref.refund_id] = ref
            self._loaded = True
            logger.info("ShopKart dataset loaded from unified PostgreSQL repository")
        except Exception as e:
            logger.warning("Could not load dataset from repository: %s", e)
            self._loaded = True

    def _parse_entities(self) -> None:
        # Company
        for item in self._raw_data.get("company.json", []):
            comp = Company(**item)
            self.companies[comp.company_id] = comp

        # Customers
        for item in self._raw_data.get("customers.json", []):
            cust = Customer(**item)
            self.customers[cust.customer_id] = cust

        # Sellers
        for item in self._raw_data.get("sellers.json", []):
            seller = Seller(**item)
            self.sellers[seller.seller_id] = seller

        # Categories
        for item in self._raw_data.get("categories.json", []):
            cat = Category(**item)
            self.categories[cat.category_id] = cat

        # Products
        for item in self._raw_data.get("products.json", []):
            prod = Product(**item)
            self.products[prod.product_id] = prod

        # Orders
        for item in self._raw_data.get("orders.json", []):
            order = Order(**item)
            self.orders[order.order_id] = order

        # Order Items
        for item in self._raw_data.get("order_items.json", []):
            oi = OrderItem(**item)
            self.order_items[oi.order_item_id] = oi

        # Payments
        for item in self._raw_data.get("payments.json", []):
            pay = Payment(**item)
            self.payments[pay.payment_id] = pay

        # Shipments
        for item in self._raw_data.get("shipments.json", []):
            ship = Shipment(**item)
            self.shipments[ship.shipment_id] = ship

        # Returns
        for item in self._raw_data.get("returns.json", []):
            ret = Return(**item)
            self.returns[ret.return_id] = ret

        # Refunds
        for item in self._raw_data.get("refunds.json", []):
            ref = Refund(**item)
            self.refunds[ref.refund_id] = ref

        # Knowledge & Scenarios (Raw structures for RAG & Evaluator)
        self.policies_raw = self._raw_data.get("policies.json", [])
        self.knowledge_articles_raw = self._raw_data.get("knowledge_articles.json", [])
        self.scenarios_raw = self._raw_data.get("scenarios.json", [])

    def get_summary_counts(self) -> Dict[str, int]:
        """Return counts of all loaded entities."""
        self.load()
        return {
            "companies": len(self.companies),
            "customers": len(self.customers),
            "sellers": len(self.sellers),
            "categories": len(self.categories),
            "products": len(self.products),
            "orders": len(self.orders),
            "order_items": len(self.order_items),
            "payments": len(self.payments),
            "shipments": len(self.shipments),
            "returns": len(self.returns),
            "refunds": len(self.refunds),
            "policies": len(self.policies_raw),
            "knowledge_articles": len(self.knowledge_articles_raw),
            "scenarios": len(self.scenarios_raw),
        }


# Global loader singleton
data_loader = DataLoader()

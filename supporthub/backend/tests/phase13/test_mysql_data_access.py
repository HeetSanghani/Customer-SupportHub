"""
Phase 13.2 — Real MySQL Data Access Integration Test Suite.

Validates query execution, entity mapping, count consistency, unknown entity handling,
and sensitive field sanitization against the live 'supporthub_business' MySQL 8.0 database.
"""

import pytest
from app.data_access.db import mysql_db
from app.data_access.postgres_business_repository import postgres_business_repository as mysql_repository
from app.data_access import (
    CustomerService,
    ProductService,
    SellerService,
    OrderService,
    PaymentService,
    ShipmentService,
    ReturnService,
    RefundService,
)


def test_mysql_connection_alive():
    """Verify MySQL business database is alive and reachable."""
    assert mysql_db.is_available() is True


def test_entity_counts_against_migrated_mysql():
    """Verify total record counts in PostgreSQL match migrated ShopKart dataset."""
    counts = {}
    with mysql_db.cursor() as cur:
        for table in [
            "company", "categories", "sellers", "products", "users",
            "orders", "order_items", "payments", "shipments", "returns", "refunds"
        ]:
            if table == "users":
                cur.execute("SELECT COUNT(DISTINCT customer_id) AS cnt FROM users WHERE customer_id LIKE 'CUST-%';")
                counts["customers"] = cur.fetchone()["cnt"]
            else:
                cur.execute(f"SELECT COUNT(*) AS cnt FROM {table};")
                counts[table] = cur.fetchone()["cnt"]

    assert counts["company"] == 1
    assert counts["categories"] == 12
    assert counts["sellers"] == 10
    assert counts["products"] == 40
    assert counts["customers"] == 25
    assert counts["orders"] == 24
    assert counts["order_items"] == 26
    assert counts["payments"] == 26
    assert counts["shipments"] == 24
    assert counts["returns"] == 5
    assert counts["refunds"] == 3


def test_customer_service_queries():
    """Verify CustomerService retrieves real PostgreSQL records correctly."""
    cust_svc = CustomerService()
    customers = cust_svc.list_all_customers()
    assert len(customers) >= 25

    c1 = cust_svc.get_customer("CUST-001")
    assert c1 is not None
    assert c1.customer_id == "CUST-001"
    assert c1.full_name == "Aarav Sharma"
    assert c1.email in ("aarav.sharma@example.com", "customer@supporthub.com")

    c_email = cust_svc.search_customer_by_email(c1.email)
    assert c_email is not None
    assert c_email.customer_id == "CUST-001"


def test_product_service_queries():
    """Verify ProductService retrieves real MySQL products and categories."""
    prod_svc = ProductService()
    products = prod_svc.list_all_products()
    assert len(products) == 40

    p1 = prod_svc.get_product("PROD-001")
    assert p1 is not None
    assert p1.product_id == "PROD-001"
    assert p1.price > 0
    assert isinstance(p1.specifications, dict)

    search_res = prod_svc.search_products_by_name("Wireless")
    assert len(search_res) > 0


def test_seller_service_queries():
    """Verify SellerService retrieves merchant profiles."""
    seller_svc = SellerService()
    sellers = seller_svc.list_all_sellers()
    assert len(sellers) == 10

    s1 = seller_svc.get_seller("SELL-001")
    assert s1 is not None
    assert s1.seller_name == "TechWorld Retail"


def test_order_service_queries():
    """Verify OrderService retrieves real orders and order items."""
    order_svc = OrderService()
    orders = order_svc.list_all_orders()
    assert len(orders) >= 24

    o1 = order_svc.get_order("ORD-001")
    assert o1 is not None
    assert o1.order_id == "ORD-001"
    assert o1.customer_id == "CUST-001"
    assert o1.total_amount == 46999.0

    items = order_svc.get_order_items("ORD-001")
    assert len(items) >= 1
    assert items[0].order_id == "ORD-001"

    details = order_svc.get_order_full_details("ORD-001")
    assert details is not None
    assert details["order"].order_id == "ORD-001"
    assert len(details["items"]) >= 1


def test_payment_shipment_return_refund_services():
    """Verify Payment, Shipment, Return, and Refund services from MySQL."""
    pay_svc = PaymentService()
    ship_svc = ShipmentService()
    ret_svc = ReturnService()
    ref_svc = RefundService()

    pay = pay_svc.get_payment_by_order("ORD-001")
    assert pay is not None
    assert pay.order_id == "ORD-001"
    assert pay.amount == 46999.0

    ship = ship_svc.get_shipment_by_order("ORD-001")
    assert ship is not None
    assert ship.order_id == "ORD-001"
    assert ship.tracking_number.startswith("TRK-")

    ret = ret_svc.get_return("RET-002")
    assert ret is not None
    assert ret.customer_id == "CUST-013"

    ref = ref_svc.get_refund("REF-002")
    assert ref is not None
    assert ref.refund_amount > 0


def test_unknown_entity_handling():
    """Verify querying non-existent IDs returns None without crashing."""
    order_svc = OrderService()
    prod_svc = ProductService()
    pay_svc = PaymentService()
    ship_svc = ShipmentService()
    ret_svc = ReturnService()
    ref_svc = RefundService()

    assert order_svc.get_order("ORD-999") is None
    assert prod_svc.get_product("PROD-999") is None
    assert pay_svc.get_payment("PAY-999") is None
    assert ship_svc.get_shipment_by_tracking("TRK-INVALID") is None
    assert ret_svc.get_return("RET-999") is None
    assert ref_svc.get_refund("REF-999") is None


def test_sensitive_field_sanitization():
    """Verify no secret credentials, CVVs, or PINs are contained in payment objects."""
    pay_svc = PaymentService()
    payments = pay_svc.list_all_payments()
    for pay in payments:
        # Check dataclass attributes
        d = vars(pay)
        assert "cvv" not in d
        assert "pin" not in d
        assert "password" not in d
        assert "card_number" not in d

"""Unit tests for Structured Data Access Layer."""
import unittest
from app.data_access import (
    CustomerService,
    ProductService,
    SellerService,
    OrderService,
    PaymentService,
    ShipmentService,
    ReturnService,
    RefundService
)
from app.data_access.loader import data_loader


class TestDataAccessLayer(unittest.TestCase):
    """Test all 8 typed data services against ShopKart dataset."""

    @classmethod
    def setUpClass(cls):
        data_loader.load()

    def test_customer_service(self):
        service = CustomerService()
        cust = service.get_customer("CUST-001")
        self.assertIsNotNone(cust)
        self.assertEqual(cust.customer_id, "CUST-001")
        self.assertTrue(len(cust.full_name) > 0)
        self.assertTrue("@" in cust.email)

        # Non-existent customer
        none_cust = service.get_customer("CUST-99999")
        self.assertIsNone(none_cust)

    def test_product_service(self):
        service = ProductService()
        prod = service.get_product("PROD-001")
        self.assertIsNotNone(prod)
        self.assertEqual(prod.product_id, "PROD-001")
        self.assertGreater(prod.price, 0)
        self.assertGreaterEqual(prod.stock_quantity, 0)

        # Search
        results = service.search_products_by_name("phone")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_seller_service(self):
        service = SellerService()
        seller = service.get_seller("SELL-001")
        self.assertIsNotNone(seller)
        self.assertEqual(seller.seller_id, "SELL-001")
        self.assertGreaterEqual(seller.rating, 1.0)
        self.assertLessEqual(seller.rating, 5.0)

        # Normalized SELLER-001
        seller_alias = service.get_seller("SELLER-001")
        self.assertIsNotNone(seller_alias)

    def test_order_relational_chain(self):
        order_svc = OrderService()
        ship_svc = ShipmentService()
        pay_svc = PaymentService()

        order = order_svc.get_order("ORD-001")
        self.assertIsNotNone(order)
        self.assertEqual(order.order_id, "ORD-001")
        self.assertGreater(order.total_amount, 0)

        # Line items
        items = order_svc.get_order_items("ORD-001")
        self.assertGreater(len(items), 0)
        self.assertEqual(items[0].order_id, "ORD-001")

        # Shipment
        shipment = ship_svc.get_shipment_by_order("ORD-001")
        self.assertIsNotNone(shipment)
        self.assertEqual(shipment.order_id, "ORD-001")

        # Payment
        payment = pay_svc.get_payment_by_order("ORD-001")
        self.assertIsNotNone(payment)
        self.assertEqual(payment.order_id, "ORD-001")

    def test_returns_and_refunds(self):
        ret_svc = ReturnService()
        ref_svc = RefundService()

        all_returns = ret_svc.list_all_returns()
        self.assertGreater(len(all_returns), 0)

        all_refunds = ref_svc.list_all_refunds()
        self.assertGreater(len(all_refunds), 0)

        sample_ref = all_refunds[0]
        self.assertTrue(sample_ref.refund_id.startswith("REF-"))
        self.assertGreater(sample_ref.refund_amount, 0)


if __name__ == "__main__":
    unittest.main()

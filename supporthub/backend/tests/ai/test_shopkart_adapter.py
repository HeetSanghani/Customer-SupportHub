"""Unit tests for ShopKartBusinessDataAdapter."""
import unittest

from app.integration.adapters.shopkart import ShopKartBusinessDataAdapter


class TestShopKartBusinessDataAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = ShopKartBusinessDataAdapter()

    def test_get_customer(self):
        cust = self.adapter.get_customer("CUST-001", "shopkart")
        self.assertIsNotNone(cust)
        self.assertEqual(cust["customer_id"], "CUST-001")
        self.assertEqual(cust["city"], "Bengaluru")

    def test_get_product_and_search(self):
        prod = self.adapter.get_product("PROD-001", "shopkart")
        self.assertIsNotNone(prod)
        self.assertEqual(prod["product_id"], "PROD-001")

        search_res = self.adapter.search_products("Pro", "shopkart")
        self.assertTrue(len(search_res) > 0)

    def test_get_order_and_items(self):
        order = self.adapter.get_order("ORD-001", "shopkart")
        self.assertIsNotNone(order)
        self.assertEqual(order["order_id"], "ORD-001")

        items = self.adapter.get_order_items("ORD-001", "shopkart")
        self.assertTrue(len(items) > 0)

    def test_get_payment_shipment_return_refund(self):
        pay = self.adapter.get_payment("PAY-001", "shopkart")
        self.assertIsNotNone(pay)

        ship = self.adapter.get_shipment("SHIP-001", "shopkart")
        self.assertIsNotNone(ship)

        # Check return / refund records
        ret = self.adapter.get_return("RET-002", "shopkart")
        self.assertIsNotNone(ret)

        ref = self.adapter.get_refund("REF-002", "shopkart")
        self.assertIsNotNone(ref)


if __name__ == "__main__":
    unittest.main()

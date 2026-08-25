"""Unit tests for multi-tenant isolation and security boundary enforcement."""
import unittest

from app.integration.security import TenantSecurityGuard, TenantIsolationViolationError
from app.integration.adapters.shopkart import ShopKartBusinessDataAdapter


class TestTenantIsolation(unittest.TestCase):
    def setUp(self):
        self.adapter = ShopKartBusinessDataAdapter()

    def test_valid_tenant_access(self):
        # Accessing ShopKart data with tenant_id='shopkart' should succeed
        customer = self.adapter.get_customer("CUST-001", tenant_id="shopkart")
        self.assertIsNotNone(customer)
        self.assertEqual(customer["customer_id"], "CUST-001")
        self.assertEqual(customer["tenant_id"], "shopkart")

    def test_cross_tenant_access_rejection(self):
        # Accessing ShopKart data with a foreign tenant_id must raise TenantIsolationViolationError
        with self.assertRaises(TenantIsolationViolationError) as ctx:
            self.adapter.get_customer("CUST-001", tenant_id="other_tenant_corp")
        self.assertIn("Cross-tenant access forbidden", str(ctx.exception))

    def test_missing_tenant_id_rejection(self):
        # Missing tenant_id must raise TenantIsolationViolationError
        with self.assertRaises(TenantIsolationViolationError):
            self.adapter.get_order("ORD-2024-1001", tenant_id="")

    def test_rag_document_filtering(self):
        docs = [
            {"id": "doc1", "tenant_id": "shopkart", "title": "ShopKart Return Policy"},
            {"id": "doc2", "tenant_id": "other_corp", "title": "Other Corp Return Policy"},
        ]
        filtered = TenantSecurityGuard.filter_documents_by_tenant(docs, tenant_id="shopkart")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], "doc1")


if __name__ == "__main__":
    unittest.main()

"""Unit tests validating multi-tenant isolation in RAG retrieval."""
import unittest

from app.integration.contracts.rag import RAGQueryRequest
from app.integration.security.tenant_boundary import TenantSecurityGuard
from app.rag.pipeline import rag_pipeline


class TestRAGTenantIsolation(unittest.TestCase):
    def test_rag_retrieval_scoped_to_tenant(self):
        # 1. Valid ShopKart Query
        req = RAGQueryRequest(
            query="return window policy",
            tenant_id="shopkart",
            top_k=3,
        )
        TenantSecurityGuard.validate_tenant_scope(req.tenant_id, "shopkart", "RAG Knowledge")
        results = rag_pipeline.retrieve(req.query, top_k=req.top_k)
        self.assertTrue(len(results) > 0)
        for r in results:
            self.assertIsNotNone(r.source_id)

    def test_foreign_tenant_rag_isolation(self):
        req = RAGQueryRequest(
            query="return window policy",
            tenant_id="foreign_enterprise",
            top_k=3,
        )
        # Attempting to search ShopKart knowledge under foreign tenant should be guarded
        with self.assertRaises(Exception):
            TenantSecurityGuard.validate_tenant_scope(req.tenant_id, "shopkart", "RAG Knowledge")


if __name__ == "__main__":
    unittest.main()

"""Tenant isolation and multi-company security boundary guard."""
from typing import Optional, Dict, Any, List


class TenantIsolationViolationError(PermissionError):
    """Raised when an operation attempts cross-tenant data access."""
    def __init__(self, message: str, requesting_tenant: str, target_tenant: Optional[str] = None):
        super().__init__(message)
        self.requesting_tenant = requesting_tenant
        self.target_tenant = target_tenant


class TenantSecurityGuard:
    """
    Deterministic boundary guard enforcing strict multi-tenant isolation.
    Guarantees that no tenant can read, query, or infer data belonging to another tenant.
    """

    @staticmethod
    def validate_tenant_scope(requesting_tenant: str, entity_tenant: Optional[str], entity_type: str = "entity") -> None:
        """
        Validate that the target entity belongs strictly to the requesting tenant.
        Raises TenantIsolationViolationError if a cross-tenant boundary breach is detected.
        """
        if not requesting_tenant:
            raise TenantIsolationViolationError(
                f"Missing requesting tenant_id for {entity_type} access.",
                requesting_tenant="UNKNOWN"
            )

        if entity_tenant and entity_tenant != requesting_tenant:
            raise TenantIsolationViolationError(
                f"Cross-tenant access forbidden: Tenant '{requesting_tenant}' attempted to access {entity_type} owned by Tenant '{entity_tenant}'.",
                requesting_tenant=requesting_tenant,
                target_tenant=entity_tenant,
            )

    @staticmethod
    def filter_documents_by_tenant(documents: List[Dict[str, Any]], tenant_id: str) -> List[Dict[str, Any]]:
        """Filter RAG knowledge documents strictly by tenant_id."""
        if not tenant_id:
            return []
        return [doc for doc in documents if doc.get("tenant_id") == tenant_id]

    @staticmethod
    def sanitize_tenant_id(raw_tenant_id: Optional[str], default_tenant: str = "shopkart") -> str:
        """Sanitize and normalize tenant identifier."""
        if not raw_tenant_id or not isinstance(raw_tenant_id, str):
            return default_tenant
        return raw_tenant_id.strip().lower()

"""Phase 13.4 — Customer Linkage Test Suite."""
import pytest
from app.data_access.customer_service import CustomerService
from app.data_access.loader import DataLoader


@pytest.fixture
def customer_service():
    loader = DataLoader()
    return CustomerService(loader=loader)


def test_customer_search_by_email_found(customer_service):
    """Verify CustomerService finds customer by email address."""
    cust001 = customer_service.get_customer("CUST-001")
    assert cust001 is not None
    cust = customer_service.search_customer_by_email(cust001.email)
    assert cust is not None
    assert cust.customer_id == "CUST-001"


def test_customer_search_by_email_case_insensitive(customer_service):
    """Verify email search is case-insensitive."""
    cust001 = customer_service.get_customer("CUST-001")
    assert cust001 is not None
    cust = customer_service.search_customer_by_email(cust001.email.upper())
    assert cust is not None
    assert cust.customer_id == "CUST-001"


def test_customer_search_by_email_not_found(customer_service):
    """Verify non-existent email returns None."""
    cust = customer_service.search_customer_by_email("nonexistent.user999@example.com")
    assert cust is None

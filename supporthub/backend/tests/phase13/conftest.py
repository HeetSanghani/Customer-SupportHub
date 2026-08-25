"""
tests/phase13/conftest.py

Phase 13 legacy tests relied on an external MySQL database ('supporthub_business')
which was consolidated into the unified PostgreSQL database ('supporthub') during Phase 15.0.

This fixture skips MySQL-dependent legacy tests if MySQL server is not running,
ensuring the unified PostgreSQL test suite runs cleanly.
"""

import pytest
import socket

def is_mysql_available() -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', 3306))
        sock.close()
        return result == 0
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    if not is_mysql_available():
        skip_mysql = pytest.mark.skip(
            reason="Legacy Phase 13 MySQL database ('supporthub_business') decommissioned and consolidated into unified PostgreSQL in Phase 15.0."
        )
        for item in items:
            if "mysql" in item.keywords or "phase13" in str(item.fspath):
                # Skip legacy raw MySQL query files
                filename = item.fspath.basename
                if filename in [
                    "test_business_data.py",
                    "test_database_security.py",
                    "test_financial.py",
                    "test_migration.py",
                    "test_ownership.py",
                    "test_relationships.py",
                    "test_repeatability.py",
                    "test_user_customer_mapping.py",
                ]:
                    item.add_marker(skip_mysql)

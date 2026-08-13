"""
tests/conftest.py

Pytest configuration and async engine/event loop lifecycle fixtures.
Ensures SQLAlchemy async engines dispose pool connections at the end of each test loop
to prevent cross-event-loop connection reuse.
"""

import pytest
import pytest_asyncio
from app.database import engine


@pytest_asyncio.fixture(autouse=True)
async def cleanup_db_connections():
    """Dispose pooled connections after each test so asyncpg connection loops do not leak across tests."""
    yield
    await engine.dispose()

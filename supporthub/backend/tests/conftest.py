"""
tests/conftest.py

Pytest configuration and async engine/event loop lifecycle fixtures.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.database import engine
from app.main import app


@pytest_asyncio.fixture(autouse=True)
async def cleanup_db_connections():
    """Dispose pooled connections after each test so asyncpg connection loops do not leak across tests."""
    yield
    await engine.dispose()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

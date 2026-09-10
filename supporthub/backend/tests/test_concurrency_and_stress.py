"""
Test Suite: High Concurrency, Stress & Connection Stability
Covers:
  - LOAD-01: WebSocket ConnectionManager handling 50+ concurrent client connections and room broadcasts
  - LOAD-02: Concurrent AI query orchestration across 20+ simultaneous threads/tasks
  - LOAD-03: Concurrent authentication and token verification stability
"""
import asyncio
import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import WebSocket

from app.ws.manager import ConnectionManager
from app.ai.orchestrator import AIOrchestrator
from app.routers.auth import create_access_token, ALGORITHM
from app.config import get_settings
from jose import jwt

settings = get_settings()


@pytest.mark.asyncio
async def test_concurrent_websocket_broadcasting():
    """LOAD-01: 50 concurrent WebSocket clients across 10 rooms receive broadcasts cleanly."""
    mgr = ConnectionManager()
    num_rooms = 10
    clients_per_room = 5
    rooms = [str(uuid.uuid4()) for _ in range(num_rooms)]
    all_mocks = []

    # Connect all 50 clients concurrently
    connect_tasks = []
    for room in rooms:
        for _ in range(clients_per_room):
            ws = MagicMock(spec=WebSocket)
            ws.send_json = AsyncMock()
            all_mocks.append((room, ws))
            connect_tasks.append(mgr.connect(room, ws))

    await asyncio.gather(*connect_tasks)

    # Verify all connected
    for room in rooms:
        assert len(mgr._rooms.get(room, [])) == clients_per_room

    # Broadcast to all rooms concurrently
    broadcast_tasks = [
        mgr.broadcast(room, {"event": "new_message", "text": f"Msg in {room}"})
        for room in rooms
    ]
    await asyncio.gather(*broadcast_tasks)

    # Verify each client received the broadcast
    for room, ws in all_mocks:
        assert ws.send_json.await_count == 1

    # Disconnect all clients
    for room, ws in all_mocks:
        mgr.disconnect(room, ws)

    # All rooms should be pruned and clean
    assert len(mgr._rooms) == 0


@pytest.mark.asyncio
async def test_concurrent_ai_chat_pipeline():
    """LOAD-02: 20 simultaneous AI orchestrator requests execute without context collisions."""
    orch = AIOrchestrator(use_llm=False)
    queries = [
        ("Where is my order ORD-001?", "CUST-001"),
        ("Show me all products", "CUST-002"),
        ("Why was my payment declined?", "CUST-003"),
        ("Do you have headphones?", "CUST-004"),
        ("What is the return policy?", "CUST-005"),
    ] * 4  # 20 total queries

    async def process_one(q, cust):
        cid = f"stress_{uuid.uuid4().hex[:8]}"
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, orch.process_message, q, cust, cid)

    tasks = [process_one(q, cust) for q, cust in queries]
    results = await asyncio.gather(*tasks)

    assert len(results) == 20
    for r in results:
        assert r is not None
        assert len(r.content) > 0
        assert r.route_type in ("STRUCTURED", "RAG", "HYBRID", "HUMAN", "ACCOUNT")


@pytest.mark.asyncio
async def test_concurrent_token_validation():
    """LOAD-03: Concurrent JWT generation and verification under high volume."""
    users = [(str(uuid.uuid4()), "customer") for _ in range(50)]

    async def generate_and_verify(user_id, role):
        token = create_access_token(user_id, role)
        decoded = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        assert decoded["sub"] == user_id
        assert decoded["role"] == role
        return True

    tasks = [generate_and_verify(u[0], u[1]) for u in users]
    outcomes = await asyncio.gather(*tasks)
    assert all(outcomes)

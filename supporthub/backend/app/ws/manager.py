"""WebSocket connection manager — room-based broadcast."""
from __future__ import annotations

import uuid
from collections import defaultdict
from typing import Dict, List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # Maps ticket_id → list of active WebSocket connections
        self._rooms: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, ticket_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._rooms[ticket_id].append(websocket)

    def disconnect(self, ticket_id: str, websocket: WebSocket) -> None:
        room = self._rooms.get(ticket_id, [])
        if websocket in room:
            room.remove(websocket)
        if not room:
            self._rooms.pop(ticket_id, None)

    async def broadcast(self, ticket_id: str, data: dict) -> None:
        """Send JSON payload to all connections in a ticket room."""
        dead: List[WebSocket] = []
        for ws in self._rooms.get(ticket_id, []):
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ticket_id, ws)

    async def broadcast_to_agents(self, data: dict) -> None:
        """Broadcast to the shared agent inbox room."""
        await self.broadcast("__agent_inbox__", data)


# Singleton — imported everywhere
manager = ConnectionManager()

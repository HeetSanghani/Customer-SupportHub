"""WebSocket connection manager — room-based broadcast."""
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Dict, List

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # Maps ticket_id → list of active WebSocket connections
        self._rooms: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, ticket_id: str, websocket: WebSocket) -> None:
        """Register a connected WebSocket in a ticket room, preventing duplicate registration."""
        room = self._rooms[ticket_id]
        if websocket not in room:
            room.append(websocket)
        logger.info(
            "[WS SERVER] Client registered | ticket=%s | clients_in_room=%d | active_rooms=%d",
            ticket_id,
            len(room),
            len(self._rooms),
        )

    def disconnect(self, ticket_id: str, websocket: WebSocket) -> None:
        """Safely unregister a WebSocket from a ticket room and prune empty rooms."""
        room = self._rooms.get(ticket_id)
        if room is not None:
            while websocket in room:
                room.remove(websocket)
            if not room:
                self._rooms.pop(ticket_id, None)
        remaining = len(self._rooms.get(ticket_id, []))
        logger.info(
            "[WS SERVER] Client disconnected/removed | ticket=%s | remaining_in_room=%d | active_rooms=%d",
            ticket_id,
            remaining,
            len(self._rooms),
        )

    async def broadcast(self, ticket_id: str, data: dict) -> None:
        """Send JSON payload to all connections in a ticket room, pruning dead sockets safely."""
        clients = list(self._rooms.get(ticket_id, []))
        event_type = data.get("type", "unknown")
        msg_id = data.get("id", "")
        logger.info(
            "[WS SERVER] broadcast start\nticket=%s\nactive_rooms=%s\nmatching_clients=%d",
            ticket_id,
            list(self._rooms.keys()),
            len(clients),
        )
        dead: List[WebSocket] = []
        for ws in clients:
            try:
                await ws.send_json(data)
            except Exception as exc:
                logger.warning(
                    "[WS SERVER] Failed to send to client | ticket=%s | removing stale client | error=%s",
                    ticket_id,
                    exc,
                )
                dead.append(ws)

        for ws in dead:
            self.disconnect(ticket_id, ws)

        clients_sent = len(clients) - len(dead)
        logger.info(
            "[WS SERVER] broadcast success\nticket=%s\nmessage=%s\nclients_sent=%d",
            ticket_id,
            msg_id,
            clients_sent,
        )

    async def broadcast_to_agents(self, data: dict) -> None:
        """Broadcast to the shared agent inbox room."""
        await self.broadcast("__agent_inbox__", data)


# Singleton — imported everywhere
manager = ConnectionManager()


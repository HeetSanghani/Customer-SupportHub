# 06 — Frontend to Backend Flow Audit

- **Frontend**: React application built with Vite (`supporthub/frontend`).
- **API Base URL**: `http://localhost:8000` / `http://localhost:8001`.
- **Auth Storage**: JWT access token stored in memory / local storage.
- **WebSocket Connection**: Initiated to `ws://localhost:8000/ws/chat/{ticket_id}` with `token` query param. Reconnect handlers handle network drops.

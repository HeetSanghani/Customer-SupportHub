# 04 — Nginx Architecture & Reverse Proxy

- **Configuration File**: `supporthub/nginx.conf`
- **Routing Rules**:
  - `/` -> Frontend SPA (`http://frontend:80`)
  - `/api/*` -> FastAPI REST API (`http://backend:8000`)
  - `/auth/*` -> FastAPI Authentication Router (`http://backend:8000`)
  - `/ws/*` -> FastAPI WebSocket Router (`http://backend:8000` with `Upgrade` and `Connection` headers)
  - `/health` -> FastAPI Healthcheck Endpoint

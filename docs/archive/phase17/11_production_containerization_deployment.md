# Phase 17 — 11. Production Containerization & Infrastructure Deployment

## Container Topology
- **Nginx Proxy Container**: Port 80/443 listener with SSL termination and WebSocket pass-through.
- **FastAPI App Container**: Multi-worker Uvicorn process managed by Docker Compose.
- **PostgreSQL Container**: PostgreSQL 15 + `pgvector` extension on dedicated volume.
- **Redis Container**: Memory-bound cache & WebSocket message broker.

# Production Docker Deployment Guide

## Architecture
Production deployment uses Docker Compose to manage 4 isolated container services:
1. **`db`**: PostgreSQL 16 image with `pgvector` extension.
2. **`backend`**: FastAPI application container (Uvicorn / Gunicorn).
3. **`frontend`**: React static assets served via Nginx.
4. **`nginx`**: Reverse proxy handling SSL, static asset serving, and WebSocket proxying (`/ws`).

## Running with Docker Compose
```bash
cd supporthub
docker compose up -d --build
```

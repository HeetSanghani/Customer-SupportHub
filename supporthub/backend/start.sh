#!/bin/bash
set -e

echo "==> Step 1: Initializing database tables & vector extension..."
uv run python -c "
import asyncio
from app.database import init_db
asyncio.run(init_db())
print('==> Database tables verified and created successfully!')
" || echo "Warning: init_db encountered an issue, continuing..."

echo "==> Step 2: Running database migrations..."
uv run alembic upgrade head || echo "Warning: Alembic migration encountered an issue, continuing..."

echo "==> Step 3: Seeding pristine production demo data (Admin, Agents, Tickets)..."
uv run python clean_and_seed.py || echo "Warning: Clean and seed encountered an issue, continuing..."

echo "==> Step 4: Starting Celery worker in background..."
uv run celery -A app.tasks.celery_app worker --loglevel=info --concurrency=1 &

echo "==> Step 5: Starting Uvicorn server on port ${PORT:-8000}..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"

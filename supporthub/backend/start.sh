#!/bin/bash
set -e

echo "==> Running database migrations..."
uv run alembic upgrade head || echo "Warning: Alembic migration encountered an issue, continuing..."

echo "==> Starting Celery worker in background..."
uv run celery -A app.tasks.celery_app worker --loglevel=info --concurrency=1 &

echo "==> Starting Uvicorn server on port ${PORT:-8000}..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"

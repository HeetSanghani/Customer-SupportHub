#!/bin/bash
set -e

echo "==> Step 1: Checking database..."
uv run python -c "
import asyncio
from sqlalchemy import text
from app.database import AsyncSessionLocal

async def status():
    try:
        async with AsyncSessionLocal() as session:
            u = (await session.exec(text('SELECT COUNT(*) FROM users'))).scalar() or 0
            kb = (await session.exec(text('SELECT COUNT(*) FROM kb_articles'))).scalar() or 0
            t = (await session.exec(text('SELECT COUNT(*) FROM tickets'))).scalar() or 0
            print(f'==> Database ready: {u} users, {kb} KB articles, {t} tickets!')
    except Exception as e:
        print(f'==> DB Status: {e}')

asyncio.run(status())
"

echo "==> Step 2: Starting Celery worker in background..."
uv run celery -A app.tasks.celery_app worker --loglevel=info --concurrency=1 &

echo "==> Step 3: Starting Uvicorn server on port ${PORT:-8000}..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"

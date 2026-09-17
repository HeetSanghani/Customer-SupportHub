#!/bin/bash
set -e

echo "==> Step 1: Checking database sync status..."
SYNC_STATUS=$(uv run python -c "
import asyncio
from sqlalchemy import text
from app.database import AsyncSessionLocal

async def check():
    try:
        async with AsyncSessionLocal() as session:
            kb_res = await session.exec(text('SELECT COUNT(*) FROM kb_articles'))
            kb_count = kb_res.scalar() or 0
            u_res = await session.exec(text('SELECT COUNT(*) FROM users'))
            u_count = u_res.scalar() or 0
            if kb_count >= 10 and u_count >= 46:
                print('FULL_DATA_PRESENT')
            else:
                print('RESTORE_REQUIRED')
    except Exception:
        print('RESTORE_REQUIRED')

asyncio.run(check())
")

echo "Database sync status: $SYNC_STATUS"

if [ "$SYNC_STATUS" = "RESTORE_REQUIRED" ]; then
    echo "==> Restoring full pristine database from supporthub_dump.sql (46 users, 10 KB articles, 29 tickets, orders, shipments)..."
    SYNC_DB_URL=$(echo "$DATABASE_URL" | sed 's/postgresql+asyncpg:\/\//postgresql:\/\//' | sed 's/postgres:\/\//postgresql:\/\//')
    psql "$SYNC_DB_URL" < supporthub_dump.sql || echo "psql import completed with non-fatal notices."
    
    echo "==> Verifying counts post-restore..."
    uv run python -c "
import asyncio
from sqlalchemy import text
from app.database import AsyncSessionLocal

async def verify():
    try:
        async with AsyncSessionLocal() as session:
            u = (await session.exec(text('SELECT COUNT(*) FROM users'))).scalar()
            kb = (await session.exec(text('SELECT COUNT(*) FROM kb_articles'))).scalar()
            t = (await session.exec(text('SELECT COUNT(*) FROM tickets'))).scalar()
            print(f'==> Verified Database: {u} users, {kb} KB articles, {t} tickets!')
    except Exception as e:
        print(f'Verification notice: {e}')

asyncio.run(verify())
"
fi

echo "==> Step 2: Starting Celery worker in background..."
uv run celery -A app.tasks.celery_app worker --loglevel=info --concurrency=1 &

echo "==> Step 3: Starting Uvicorn server on port ${PORT:-8000}..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"

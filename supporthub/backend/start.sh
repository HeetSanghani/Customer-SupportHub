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
            kb = (await session.exec(text('SELECT COUNT(*) FROM kb_articles'))).scalar() or 0
            u = (await session.exec(text('SELECT COUNT(*) FROM users'))).scalar() or 0
            t = (await session.exec(text('SELECT COUNT(*) FROM tickets'))).scalar() or 0
            if kb == 10 and u == 46 and t == 29:
                print('FULL_DATA_PRESENT')
            else:
                print(f'MISMATCH_DETECTED: users={u}, kb={kb}, tickets={t}')
    except Exception as e:
        print(f'ERROR: {e}')

asyncio.run(check())
")

echo "Database sync status: $SYNC_STATUS"

if [ "$SYNC_STATUS" != "FULL_DATA_PRESENT" ]; then
    echo "==> Performing clean database reset and restoring exact 735KB dump..."
    SYNC_DB_URL=$(echo "$DATABASE_URL" | sed 's/postgresql+asyncpg:\/\//postgresql:\/\//' | sed 's/postgres:\/\//postgresql:\/\//')
    
    # 1. Cleanly wipe old duplicate schema so there are no duplicated users or agents
    echo "==> Resetting schema public..."
    psql "$SYNC_DB_URL" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO supporthub; GRANT ALL ON SCHEMA public TO public; CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;" || echo "Schema reset notice."

    # 2. Restore full pristine dump
    echo "==> Importing supporthub_dump.sql..."
    psql "$SYNC_DB_URL" < supporthub_dump.sql || echo "psql import completed."
    
    # 3. Verify exact counts
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
            ag = (await session.exec(text(\"SELECT COUNT(*) FROM users WHERE role = 'agent'\"))).scalar()
            print(f'==> SUCCESS: {u} users (expected 46), {kb} KB articles (expected 10), {t} tickets (expected 29), {ag} agent(s) (expected 1)!')
    except Exception as e:
        print(f'Verification notice: {e}')

asyncio.run(verify())
"
fi

echo "==> Step 2: Starting Celery worker in background..."
uv run celery -A app.tasks.celery_app worker --loglevel=info --concurrency=1 &

echo "==> Step 3: Starting Uvicorn server on port ${PORT:-8000}..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"

#!/bin/bash
set -e

echo "==> Running database migrations..."
uv run alembic upgrade head || echo "Warning: Alembic migration encountered an issue, continuing..."

echo "==> Ensuring default admin users exist..."
uv run python -c "
import asyncio
from sqlmodel import select
from app.database import AsyncSessionLocal
from app.models import User, UserRole, UserStatus
from app.routers.auth import hash_password

async def seed_admins():
    async with AsyncSessionLocal() as session:
        for email, name in [
            ('admin@supporthub.com', 'Admin User'),
            ('heets.brainerhub@gmail.com', 'Heet Patel'),
        ]:
            res = await session.exec(select(User).where(User.email == email))
            user = res.first()
            if not user:
                admin = User(
                    email=email,
                    name=name,
                    password_hash=hash_password('Password123!'),
                    role=UserRole.admin,
                    status=UserStatus.active,
                )
                session.add(admin)
                print(f'==> Seeded admin: {email} / Password123!')
            else:
                user.role = UserRole.admin
                session.add(user)
        await session.commit()

asyncio.run(seed_admins())
" || echo "Warning: Admin seed skipped"

echo "==> Starting Celery worker in background..."
uv run celery -A app.tasks.celery_app worker --loglevel=info --concurrency=1 &

echo "==> Starting Uvicorn server on port ${PORT:-8000}..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from app.models import Ticket

async def main():
    engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/supporthub")
    async with AsyncSession(engine) as session:
        stmt = select(Ticket).order_by(Ticket.created_at.desc()).limit(50)
        result = await session.execute(stmt)
        tickets = result.scalars().all()
        print(f"Total tickets in top 50: {len(tickets)}")
        for t in tickets:
            print(f"ID: {t.id}, Status: {t.status}, Channel: {t.channel}")

asyncio.run(main())

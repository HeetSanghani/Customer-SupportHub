import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import Message

async def main():
    engine = create_async_engine("postgresql+asyncpg://supporthub:supporthub_dev@localhost:5433/supporthub")
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Message).order_by(Message.created_at.desc()).limit(5))
        for msg in result.scalars():
            print(f"ID: {msg.id}, Ticket: {msg.ticket_id}, Role: {msg.sender_type}, Body: {msg.body}, Attachments: {msg.attachments}")

asyncio.run(main())

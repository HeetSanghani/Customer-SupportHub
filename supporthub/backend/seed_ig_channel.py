import asyncio
from app.database import AsyncSessionLocal
from app.models import ChannelIntegration, ChannelType

async def main():
    async with AsyncSessionLocal() as session:
        from sqlmodel import select
        stmt = select(ChannelIntegration).where(ChannelIntegration.channel_type == ChannelType.instagram)
        existing = (await session.exec(stmt)).first()
        if existing:
            existing.display_name = "@heets.brainerhub"
            session.add(existing)
            await session.commit()
            print("Updated DB!")

if __name__ == "__main__":
    asyncio.run(main())

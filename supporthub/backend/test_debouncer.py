import asyncio
from uuid import uuid4
from app.database import AsyncSessionLocal
from app.models import Ticket, User, Message, SenderType

async def run():
    from app.services.ai.debouncer import ai_debouncer
    from app.services.instagram.webhook import _execute_ai_for_instagram
    
    async with AsyncSessionLocal() as db:
        # fetch any existing ticket
        from sqlmodel import select
        ticket = (await db.exec(select(Ticket).limit(1))).first()
        if not ticket:
            print("No ticket found")
            return
        print(f"Testing on ticket {ticket.id}")
        try:
            await _execute_ai_for_instagram(ticket.id, "sender123", str(ticket.id))
            print("Execution completed without errors")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run())

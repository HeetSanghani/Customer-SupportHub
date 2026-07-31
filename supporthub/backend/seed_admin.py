import asyncio
from sqlmodel import select
from app.database import get_session, AsyncSessionLocal
from app.models import User, UserRole

async def elevate_user(email: str):
    async with AsyncSessionLocal() as session:
        result = await session.exec(select(User).where(User.email == email))
        user = result.first()
        
        if not user:
            print(f"User with email {email} not found!")
            return
            
        user.role = UserRole.admin
        session.add(user)
        await session.commit()
        print(f"Successfully elevated {email} to ADMIN role.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: uv run seed_admin.py <user_email>")
        sys.exit(1)
        
    email = sys.argv[1]
    asyncio.run(elevate_user(email))

import asyncio
from sqlmodel import select
from app.database import get_session, AsyncSessionLocal
from app.models import User, UserRole, UserStatus
from app.routers.auth import hash_password

async def seed_users():
    users_to_create = [
        {
            "email": "admin@supporthub.com",
            "name": "Admin User",
            "role": UserRole.admin,
        },
        {
            "email": "manager@supporthub.com",
            "name": "Manager User",
            "role": UserRole.manager,
        },
        {
            "email": "agent@supporthub.com",
            "name": "Agent User",
            "role": UserRole.agent,
        },
        {
            "email": "customer@supporthub.com",
            "name": "Customer User",
            "role": UserRole.customer,
        },
    ]

    default_password = "Password123!"

    async with AsyncSessionLocal() as session:
        for u_data in users_to_create:
            result = await session.exec(select(User).where(User.email == u_data["email"]))
            existing_user = result.first()
            
            if existing_user:
                print(f"✅ User {u_data['email']} already exists.")
            else:
                new_user = User(
                    email=u_data["email"],
                    name=u_data["name"],
                    password_hash=hash_password(default_password),
                    role=u_data["role"],
                    status=UserStatus.active,
                )
                session.add(new_user)
                print(f"🚀 Created {u_data['role'].value.upper()} user: {u_data['email']} (Password: {default_password})")
                
        await session.commit()
        print("\n🎉 Database seeding complete!")

if __name__ == "__main__":
    print("Seeding default test accounts...")
    asyncio.run(seed_users())

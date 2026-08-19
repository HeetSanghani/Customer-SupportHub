import asyncio
from clean_and_seed import run_clean_and_seed

if __name__ == "__main__":
    print("🌱 Seeding SupportHub Database with clean production data...")
    asyncio.run(run_clean_and_seed())


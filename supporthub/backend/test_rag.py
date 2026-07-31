import asyncio
from app.database import AsyncSessionLocal
from app.ai import generate_rag_response

async def test_rag():
    try:
        async with AsyncSessionLocal() as session:
            print("Starting RAG test...")
            result = await generate_rag_response(session, "How do I reset my password")
            print("AI Response:", result)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_rag())

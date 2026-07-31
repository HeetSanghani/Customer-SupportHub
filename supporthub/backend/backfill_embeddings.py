import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from app.config import get_settings
from app.models import KbArticle
from app.ai import generate_embedding

async def main():
    settings = get_settings()
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        statement = select(KbArticle)
        result = await session.execute(statement)
        articles = result.scalars().all()
        
        for article in articles:
            print(f"Generating real embedding for: {article.title}")
            text = f"{article.title}\n{article.body}"
            article.embedding = generate_embedding(text)
            session.add(article)
            
        await session.commit()
        print("Updated all articles with real Gemini embeddings!")

if __name__ == "__main__":
    asyncio.run(main())

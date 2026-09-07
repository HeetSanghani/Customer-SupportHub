import asyncio
from sqlmodel import select
from app.rag.retriever import _execute_db_op
from app.models import KbArticle
from app.rag.embeddings import GoogleEmbeddingProvider

async def _backfill(session):
    provider = GoogleEmbeddingProvider()
    stmt = select(KbArticle)
    res = await session.exec(stmt)
    articles = res.all()
    
    for article in articles:
        print(f"Generating real Gemini embedding for: {article.title[:50]}")
        text = f"{article.title}\n{article.body}"
        vec = provider.embed_text(text, task_type="retrieval_document")
        article.embedding = vec
        session.add(article)
        
    await session.commit()
    print(f"Successfully updated {len(articles)} articles with real 768-dim Gemini embeddings!")

if __name__ == "__main__":
    _execute_db_op(_backfill)

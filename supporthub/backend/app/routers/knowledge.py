"""Knowledge Base router — CRUD for KB Articles."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.dependencies import get_current_user, require_role
from app.models import KbArticle, User, UserRole

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

class KbArticleCreate(BaseModel):
    title: str
    category: str
    body: str
    published: bool = True

class KbArticleUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    body: Optional[str] = None
    published: Optional[bool] = None

class KbArticleOut(BaseModel):
    id: str
    title: str
    category: str
    body: str
    views: int
    helpful_count: int
    published: bool
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, a: KbArticle) -> "KbArticleOut":
        return cls(
            id=str(a.id),
            title=a.title,
            category=a.category,
            body=a.body,
            views=a.views,
            helpful_count=a.helpful_count,
            published=a.published,
            created_by=str(a.created_by) if a.created_by else None,
            created_at=a.created_at,
            updated_at=a.updated_at,
        )

from app.ai import generate_embedding

@router.post("/", response_model=KbArticleOut, status_code=201)
async def create_article(
    body: KbArticleCreate,
    current_user: User = Depends(require_role(UserRole.manager)),
    session: AsyncSession = Depends(get_session),
):
    article = KbArticle(
        title=body.title,
        category=body.category,
        body=body.body,
        published=body.published,
        created_by=current_user.id,
        embedding=generate_embedding(body.title + "\n" + body.body)
    )
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return KbArticleOut.from_orm(article)

@router.get("/", response_model=List[KbArticleOut])
async def list_articles(
    category: Optional[str] = None,
    published_only: bool = False,
    skip: int = 0,
    limit: int = Query(50, le=200),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(KbArticle)
    if category:
        stmt = stmt.where(KbArticle.category == category)
    if published_only:
        stmt = stmt.where(KbArticle.published == True)
        
    stmt = stmt.order_by(KbArticle.created_at.desc()).offset(skip).limit(limit)
    result = await session.exec(stmt)
    articles = result.all()
    return [KbArticleOut.from_orm(a) for a in articles]

@router.get("/{article_id}", response_model=KbArticleOut)
async def get_article(
    article_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    article = await session.get(KbArticle, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
        
    # Increment views
    article.views += 1
    session.add(article)
    await session.commit()
    
    return KbArticleOut.from_orm(article)

@router.patch("/{article_id}", response_model=KbArticleOut)
async def update_article(
    article_id: uuid.UUID,
    body: KbArticleUpdate,
    current_user: User = Depends(require_role(UserRole.manager)),
    session: AsyncSession = Depends(get_session),
):
    article = await session.get(KbArticle, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if body.title is not None:
        article.title = body.title
    if body.category is not None:
        article.category = body.category
    if body.body is not None:
        article.body = body.body
    if body.published is not None:
        article.published = body.published
        
    if body.title is not None or body.body is not None:
        article.embedding = generate_embedding(article.title + " " + article.body)

    article.updated_at = datetime.now(timezone.utc)
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return KbArticleOut.from_orm(article)

@router.delete("/{article_id}", status_code=204)
async def delete_article(
    article_id: uuid.UUID,
    current_user: User = Depends(require_role(UserRole.manager)),
    session: AsyncSession = Depends(get_session),
):
    article = await session.get(KbArticle, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
        
    await session.delete(article)
    await session.commit()

@router.post("/{article_id}/helpful", response_model=KbArticleOut)
async def mark_article_helpful(
    article_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    article = await session.get(KbArticle, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.helpful_count += 1
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return KbArticleOut.from_orm(article)

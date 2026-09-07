"""
tests/test_agent_assist.py

Comprehensive test suite for Hardening SupportHub Human-Agent AI Assist (Section 12):
1. Vector similarity search in find_similar_tickets using pgvector <=> cosine similarity.
2. Ticket summarization using AI model adapter with structured exception logging.
3. Grounded reply generation with GroundingValidator integration.
"""

from __future__ import annotations

import uuid
import pytest
from unittest.mock import patch, MagicMock

from sqlmodel import select
from app.database import AsyncSessionLocal
from app.models import Ticket, TicketStatus, TicketChannel, Message, SenderType, User, UserRole
from app.services.ai.ticket_embeddings import ensure_ticket_embedding
from app.routers.tickets import find_similar_tickets, summarize_ticket, suggest_reply


@pytest.mark.asyncio
async def test_find_similar_tickets_pgvector():
    """Test find_similar_tickets uses pgvector cosine similarity search."""
    async with AsyncSessionLocal() as session:
        # 1. Create dummy customer and agent
        res = await session.exec(select(User).where(User.role == UserRole.customer))
        user = res.first()
        if not user:
            user = User(name="Test Customer Assist", email="assistcust@example.com", role=UserRole.customer)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        agent = User(name="Test Agent Assist", email="assistagent@example.com", role=UserRole.agent)

        ref_base = uuid.uuid4().hex[:6]

        # Target Ticket A (open)
        ticket_a = Ticket(
            ref=f"T-A-{ref_base}",
            customer_id=user.id,
            subject="My refund for order #98765 has not arrived yet",
            category="refunds",
            channel=TicketChannel.email,
            status=TicketStatus.open
        )
        session.add(ticket_a)

        # Similar Ticket B (resolved)
        ticket_b = Ticket(
            ref=f"T-B-{ref_base}",
            customer_id=user.id,
            subject="Where is my refund money for purchase 98765?",
            category="refunds",
            channel=TicketChannel.email,
            status=TicketStatus.resolved
        )
        session.add(ticket_b)

        # Dissimilar Ticket C (resolved)
        ticket_c = Ticket(
            ref=f"T-C-{ref_base}",
            customer_id=user.id,
            subject="How do I update my profile account email address?",
            category="account",
            channel=TicketChannel.email,
            status=TicketStatus.resolved
        )
        session.add(ticket_c)

        await session.commit()
        await session.refresh(ticket_a)
        await session.refresh(ticket_b)
        await session.refresh(ticket_c)

        try:
            # Generate real embeddings for ticket_a and ticket_b
            emb_a = await ensure_ticket_embedding(session, ticket_a)
            emb_b = await ensure_ticket_embedding(session, ticket_b)
            assert emb_a is not None
            assert emb_b is not None

            # Execute search
            results = await find_similar_tickets(
                ticket_id=ticket_a.id,
                limit=5,
                current_user=agent,
                session=session
            )

            assert len(results) >= 1
            match_b = next((r for r in results if r.id == str(ticket_b.id)), None)
            assert match_b is not None, f"Ticket B ({ticket_b.id}) not found in search results: {results}"
            assert match_b.is_fallback is False
            assert 0.0 <= match_b.similarity <= 1.0
            assert match_b.similarity not in (0.95, 0.87, 0.79)

        finally:
            await session.delete(ticket_a)
            await session.delete(ticket_b)
            await session.delete(ticket_c)
            await session.commit()


@pytest.mark.asyncio
async def test_summarize_ticket_success_and_caching():
    """Test summarize_ticket generates, caches, and returns a summary."""
    async with AsyncSessionLocal() as session:
        res = await session.exec(select(User).where(User.role == UserRole.customer))
        user = res.first()
        if not user:
            user = User(name="Test Customer S2", email="custs2@example.com", role=UserRole.customer)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        agent = User(name="Test Agent S2", email="agents2@example.com", role=UserRole.agent)

        ref = f"T-SUM-{uuid.uuid4().hex[:6]}"
        ticket = Ticket(
            ref=ref,
            customer_id=user.id,
            subject="Item damaged upon delivery",
            category="returns",
            channel=TicketChannel.email,
            status=TicketStatus.open
        )
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)

        m1 = Message(ticket_id=ticket.id, sender_id=user.id, sender_type=SenderType.customer, body="The box arrived crushed and product broken.")
        m2 = Message(ticket_id=ticket.id, sender_id=user.id, sender_type=SenderType.agent, body="We are sorry! Please send a photo of the damaged box.")
        m3 = Message(ticket_id=ticket.id, sender_id=user.id, sender_type=SenderType.customer, body="Attached photo showing the crack across the screen.")
        session.add_all([m1, m2, m3])
        await session.commit()

        try:
            res_out = await summarize_ticket(ticket_id=ticket.id, current_user=agent, session=session)
            assert res_out.summary is not None
            assert len(res_out.summary) > 10

            await session.refresh(ticket)
            assert ticket.ai_summary == res_out.summary

            # Second call should return cached summary
            res_out_cached = await summarize_ticket(ticket_id=ticket.id, current_user=agent, session=session)
            assert res_out_cached.summary == res_out.summary

        finally:
            await session.delete(m1)
            await session.delete(m2)
            await session.delete(m3)
            await session.delete(ticket)
            await session.commit()


@pytest.mark.asyncio
async def test_summarize_ticket_exception_handling():
    """Test summarize_ticket catches errors, logs exception, and returns fallback summary."""
    async with AsyncSessionLocal() as session:
        res = await session.exec(select(User).where(User.role == UserRole.customer))
        user = res.first()
        if not user:
            user = User(name="Test Customer S2Err", email="custs2err@example.com", role=UserRole.customer)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        agent = User(name="Test Agent S2Err", email="agents2err@example.com", role=UserRole.agent)

        ref = f"T-ERR-{uuid.uuid4().hex[:6]}"
        ticket = Ticket(
            ref=ref,
            customer_id=user.id,
            subject="Order status inquiry",
            category="shipping",
            channel=TicketChannel.email,
            status=TicketStatus.open
        )
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)

        m1 = Message(ticket_id=ticket.id, sender_id=user.id, sender_type=SenderType.customer, body="Where is my order?")
        m2 = Message(ticket_id=ticket.id, sender_id=user.id, sender_type=SenderType.agent, body="Checking with carrier.")
        m3 = Message(ticket_id=ticket.id, sender_id=user.id, sender_type=SenderType.customer, body="Any updates?")
        session.add_all([m1, m2, m3])
        await session.commit()

        try:
            with patch("app.services.ai.model_adapter.get_model_adapter") as mock_adapter:
                adapter_instance = MagicMock()
                adapter_instance.generate.side_effect = RuntimeError("API Rate Limit 429")
                mock_adapter.return_value = adapter_instance

                res_out = await summarize_ticket(ticket_id=ticket.id, current_user=agent, session=session)
                assert res_out.summary is not None
                assert "currently open with 3 messages exchanged" in res_out.summary

        finally:
            await session.delete(m1)
            await session.delete(m2)
            await session.delete(m3)
            await session.delete(ticket)
            await session.commit()


@pytest.mark.asyncio
async def test_suggest_reply_grounding_integration():
    """Test suggest_reply includes grounding score, grounding violations, and is_grounded flag."""
    async with AsyncSessionLocal() as session:
        res = await session.exec(select(User).where(User.role == UserRole.customer))
        user = res.first()
        if not user:
            user = User(name="Test Customer S3", email="custs3@example.com", role=UserRole.customer)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        agent = User(name="Test Agent S3", email="agents3@example.com", role=UserRole.agent)

        ref = f"T-SUG-{uuid.uuid4().hex[:6]}"
        ticket = Ticket(
            ref=ref,
            customer_id=user.id,
            subject="Can I return an item after 14 days?",
            category="returns",
            channel=TicketChannel.email,
            status=TicketStatus.open
        )
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)

        m1 = Message(ticket_id=ticket.id, sender_id=user.id, sender_type=SenderType.customer, body="What is your return window policy?")
        session.add(m1)
        await session.commit()

        try:
            res_out = await suggest_reply(ticket_id=ticket.id, tone="formal", current_user=agent, session=session)
            assert res_out.suggestion is not None
            assert hasattr(res_out, "is_grounded")
            assert hasattr(res_out, "grounding_score")
            assert hasattr(res_out, "grounding_violations")
            assert isinstance(res_out.is_grounded, bool)
            assert 0.0 <= res_out.grounding_score <= 1.0
            assert isinstance(res_out.grounding_violations, list)

        finally:
            await session.delete(m1)
            await session.delete(ticket)
            await session.commit()

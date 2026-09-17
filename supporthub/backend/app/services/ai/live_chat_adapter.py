"""
Live Chat AI Adapter for SupportHub.

Integrates SupportHub Live Chat with the SupportHub AI Architecture (supporthub-ai-architecture).
Responsible for:
  - Normalizing Live Chat messages into NormalizedInboundMessage
  - Invoking AIOrchestrator (intent routing, tools, RAG, security, escalation)
  - Persisting AI responses into PostgreSQL
  - Handling Ticket status mutation on human escalation or case resolution
  - Real-time WebSocket broadcasting via ConnectionManager
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Optional, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import AsyncSessionLocal
from app.models import AuditLog, Message, SenderType, Ticket, TicketPriority, TicketStatus, User
from app.ws.manager import manager
from app.ai.intent import is_resolution_intent

logger = logging.getLogger(__name__)

# Fallback response when an unexpected error occurs
_FALLBACK_REPLY = (
    "I'm sorry, our AI assistant encountered a temporary issue. "
    "A human support representative will assist you shortly."
)


class LiveChatAIAdapter:
    """
    Adapter bridging SupportHub WebSocket Live Chat to the SupportHub AI Architecture.
    """

    def __init__(self, tenant_id: str = "shopkart", use_llm: bool = False) -> None:
        self.tenant_id = tenant_id
        self.use_llm = use_llm
        self._orchestrator = None
        self._init_orchestrator()

    def _init_orchestrator(self) -> None:
        """Initialize the AIOrchestrator from native app.ai.orchestrator."""
        try:
            from app.ai.orchestrator import AIOrchestrator
            self._orchestrator = AIOrchestrator(use_llm=self.use_llm)
            logger.info("[LiveChatAIAdapter] AIOrchestrator initialized successfully.")
        except Exception as exc:
            logger.error("[LiveChatAIAdapter] Failed to initialize AIOrchestrator: %s", exc, exc_info=True)
            self._orchestrator = None

    def _resolve_customer_id(self, user: Optional[User]) -> str:
        """
        Map SupportHub User to ShopKart customer ID if available, otherwise return user identifier.
        """
        if not user:
            return "GUEST"

        # Priority 1: Direct link via explicit user.customer_id
        if hasattr(user, "customer_id") and user.customer_id:
            return user.customer_id

        # Priority 2: Direct link if channel_customer_id is formatted as CUST-XXX
        if user.channel_customer_id and user.channel_customer_id.startswith("CUST-"):
            return user.channel_customer_id

        # Priority 3: Fallback check if user email matches ShopKart customer dataset
        try:
            from data_access.loader import data_loader
            data_loader.load()
            for cid, cust in data_loader.customers.items():
                if user.email and cust.email and user.email.lower() == cust.email.lower():
                    return cid
        except Exception:
            pass

        # If user.channel_customer_id exists, use it
        if user.channel_customer_id:
            return user.channel_customer_id

        return str(user.id)

    async def process_live_chat_message(
        self,
        ticket_id: str,
        message_body: str,
        customer_override_id: Optional[str] = None,
        use_llm: Optional[bool] = None,
    ) -> Optional[Message]:
        """
        Process an incoming customer Live Chat message through the AI architecture.
        Executes in an independent DB session and broadcasts updates via WebSocket.
        """
        active_use_llm = self.use_llm if use_llm is None else use_llm
        logger.info("[LiveChatAIAdapter] Processing Live Chat message for ticket=%s | use_llm=%s", ticket_id, active_use_llm)

        async with AsyncSessionLocal() as session:
            ticket_uuid = UUID(ticket_id)
            ticket = await session.get(Ticket, ticket_uuid)
            if not ticket:
                logger.warning("[LiveChatAIAdapter] Ticket not found: %s", ticket_id)
                return None

            user = await session.get(User, ticket.customer_id) if ticket.customer_id else None
            customer_id_str = customer_override_id or self._resolve_customer_id(user)

            # 0. If conversation is assigned to a human agent, suppress AI generation
            if ticket.agent_id is not None:
                logger.info("[LiveChatAIAdapter] Human agent %s assigned to ticket %s; suppressing AI response.", ticket.agent_id, ticket_id)
                return None

            # 1. Handle Resolution Intent FIRST (customer closing statement marks ticket resolved)
            if is_resolution_intent(message_body):
                ticket.status = TicketStatus.resolved
                ticket.ai_resolved = True
                logger.info("[LiveChatAIAdapter] Ticket %s marked as resolved by user intent.", ticket_id)

                session.add(AuditLog(
                    actor_id=ticket.customer_id,
                    action="ticket.auto_resolved",
                    entity_type="ticket",
                    entity_id=str(ticket.id),
                    ticket_id=ticket.id,
                    diff_json='{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}',
                ))

                resolution_reply = (
                    "I'm glad to hear that you got your answer and your issue has been resolved! "
                    "I have marked this ticket as completed and resolved. "
                    "If you need any further assistance in the future, please feel free to reach out anytime. Have a wonderful day!"
                )
                ai_msg = Message(
                    ticket_id=ticket_uuid,
                    sender_id=None,
                    sender_type=SenderType.ai,
                    body=resolution_reply,
                )
                session.add(ai_msg)
                ticket.updated_at = datetime.now()
                session.add(ticket)

                try:
                    from app.services.csat_delivery import deliver_csat_survey
                    await deliver_csat_survey(session, ticket, user)
                except Exception as e:
                    logger.warning("[LiveChatAIAdapter] Failed to deliver CSAT survey: %s", e)

                await session.commit()
                await session.refresh(ai_msg)
                await session.refresh(ticket)

                await self._broadcast_ai_events(ticket_id, ai_msg, ticket, resolution_reply)
                return ai_msg

            # 2. If conversation is already escalated to a human agent (unassigned), emit hold notice
            if ticket.status == TicketStatus.escalated:
                hold_text = (
                    "Your request is with a human support agent. An agent is reviewing your inquiry "
                    "and will respond shortly."
                )
                ai_msg = Message(
                    ticket_id=ticket_uuid,
                    sender_id=None,
                    sender_type=SenderType.ai,
                    body=hold_text,
                )
                session.add(ai_msg)
                ticket.updated_at = datetime.now()
                session.add(ticket)
                await session.commit()
                await session.refresh(ai_msg)

                await self._broadcast_ai_events(ticket_id, ai_msg, ticket, hold_text)
                return ai_msg
            # 3. Anonymous vs Authenticated Behavior Guard (Phase 12.5)
            # GUEST / Anonymous guard for private data requests
            private_keywords = ["order", "payment", "shipment", "return", "refund", "my account", "my order", "my refund"]
            msg_clean = message_body.lower()
            if customer_id_str == "GUEST" and any(kw in msg_clean for kw in private_keywords):
                login_notice = (
                    "You are currently chatting as a Guest. "
                    "To view your personal order, payment, shipment, return, or refund details, "
                    "please log in to your authenticated ShopKart account."
                )
                ai_msg = Message(
                    ticket_id=ticket_uuid,
                    sender_id=None,
                    sender_type=SenderType.ai,
                    body=login_notice,
                )
                session.add(ai_msg)
                ticket.updated_at = datetime.now()
                session.add(ticket)
                await session.commit()
                await session.refresh(ai_msg)
                await self._broadcast_ai_events(ticket_id, ai_msg, ticket, login_notice)
                return ai_msg

            if not customer_id_str.startswith("CUST-") and any(kw in msg_clean for kw in private_keywords):
                unlinked_notice = (
                    "You don't have any linked orders yet. Please contact support if you believe your account should be linked."
                )
                ai_msg = Message(
                    ticket_id=ticket_uuid,
                    sender_id=None,
                    sender_type=SenderType.ai,
                    body=unlinked_notice,
                )
                session.add(ai_msg)
                ticket.updated_at = datetime.now()
                session.add(ticket)
                await session.commit()
                await session.refresh(ai_msg)
                await self._broadcast_ai_events(ticket_id, ai_msg, ticket, unlinked_notice)
                return ai_msg

            # 4. Invoke AI Orchestrator
            ai_text = _FALLBACK_REPLY
            ai_result = None
            try:
                if self._orchestrator:
                    ai_result = self._orchestrator.process_message(
                        query=message_body,
                        customer_id=customer_id_str,
                        conversation_id=ticket_id,
                        channel_type="WEBSITE",
                        use_llm=active_use_llm,
                    )
                    ai_text = ai_result.content
                else:
                    logger.warning("[LiveChatAIAdapter] AI Orchestrator unavailable, using fallback.")
            except Exception as exc:
                err_str = str(exc)
                logger.error("[LiveChatAIAdapter] Error in AI Orchestration: %s", exc, exc_info=True)
                if "429" in err_str or "quota" in err_str.lower() or "ResourceExhausted" in err_str:
                    ai_text = "I'm sorry, our AI assistant is temporarily unavailable due to high demand. A human agent will assist you shortly."
                else:
                    ai_text = _FALLBACK_REPLY

            # 5. Handle Escalation Decision
            if ai_result and hasattr(ai_result, "escalation_decision") and ai_result.escalation_decision:
                if ai_result.escalation_decision.should_escalate or ai_result.route_type == "HUMAN":
                    ticket.status = TicketStatus.escalated
                    p_str = (ai_result.escalation_decision.priority or "HIGH").upper()
                    if p_str == "URGENT":
                        ticket.priority = TicketPriority.urgent
                    elif p_str == "HIGH":
                        ticket.priority = TicketPriority.high
                    elif p_str == "LOW":
                        ticket.priority = TicketPriority.low
                    else:
                        ticket.priority = TicketPriority.medium

                    ticket.category = "Escalation"
                    logger.info(
                        "[LiveChatAIAdapter] Ticket %s escalated: reason=%s priority=%s",
                        ticket_id,
                        ai_result.escalation_decision.reason,
                        ticket.priority.value,
                    )

            # 5. Persist AI Message & Ticket Timestamp
            ticket.updated_at = datetime.now()
            session.add(ticket)

            ai_msg = Message(
                ticket_id=ticket_uuid,
                sender_id=None,
                sender_type=SenderType.ai,
                body=ai_text,
            )
            session.add(ai_msg)
            await session.commit()
            await session.refresh(ai_msg)
            await session.refresh(ticket)

            # 6. Generate Dynamic Subject Title if needed
            try:
                from app.ai import generate_ai_ticket_subject
                ai_subj = await generate_ai_ticket_subject(session, ticket_id)
                if ai_subj and ticket.subject != ai_subj:
                    ticket.subject = ai_subj
                    session.add(ticket)
                    await session.commit()
                    await session.refresh(ticket)
            except Exception:
                pass

            # 7. Real-Time Broadcasts
            await self._broadcast_ai_events(ticket_id, ai_msg, ticket, ai_text)
            return ai_msg

    async def _broadcast_ai_events(
        self,
        ticket_id: str,
        ai_msg: Message,
        ticket: Ticket,
        ai_text: str,
    ) -> None:
        """Broadcast new AI message, agent inbox preview, and ticket status updates."""
        # Broadcast AI message to the ticket chat room
        await manager.broadcast(ticket_id, {
            "type": "message",
            "id": str(ai_msg.id),
            "ticket_id": ticket_id,
            "sender_id": "AI",
            "sender_name": "Support AI",
            "sender_role": "ai",
            "body": ai_text,
            "created_at": ai_msg.created_at.isoformat(),
        })

        # Broadcast update to the agent dashboard inbox
        await manager.broadcast_to_agents({
            "type": "inbox_update",
            "ticket_id": ticket_id,
            "preview": ai_text[:80],
            "sender_name": "Support AI",
            "subject": ticket.subject or "",
            "status": ticket.status.value,
        })

        # Broadcast ticket status update to the room
        await manager.broadcast(ticket_id, {
            "type": "ticket_update",
            "status": ticket.status.value,
            "subject": ticket.subject or "",
            "ai_resolved": ticket.ai_resolved,
        })


# Global singleton instance for live chat
live_chat_ai_adapter = LiveChatAIAdapter()

"""Mock SupportHub system simulating production message, ticket, and escalation lifecycle."""
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from app.integration.contracts.message import NormalizedInboundMessage, ChannelType, SenderType
from app.integration.contracts.customer import CustomerIdentity, AuthContext
from app.integration.contracts.conversation import ConversationSession
from app.integration.contracts.ticket import TicketRecord, TicketHandoffPayload
from app.integration.contracts.ai_result import NormalizedAIResult, EscalationDetail
from app.integration.contracts.rag import RAGCitation
from app.integration.security.tenant_boundary import TenantSecurityGuard
from app.ai.orchestrator import AIOrchestrator


class MockSupportHubSystem:
    """
    Simulates the integration boundary of the existing SupportHub platform.
    Receives omnichannel messages, manages conversation/ticket state, and executes AI processing.
    """

    def __init__(self, tenant_id: str = "shopkart") -> None:
        self.tenant_id = tenant_id
        self.tickets: Dict[str, TicketRecord] = {}
        self.conversations: Dict[str, ConversationSession] = {}
        self.escalation_handoffs: List[TicketHandoffPayload] = []
        self.outbound_messages: List[Dict[str, Any]] = []
        self.orchestrator = AIOrchestrator()
        self._ticket_counter = 10000

    def _generate_ticket_ref(self) -> str:
        self._ticket_counter += 1
        return f"TCK-{self._ticket_counter}"

    def receive_channel_message(
        self,
        channel: str,
        sender_id: str,
        text: str,
        customer_name: Optional[str] = None,
        conversation_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        use_llm: bool = False,
    ) -> NormalizedAIResult:
        """
        Main entry point simulating inbound webhook delivery from a channel (Web, WhatsApp, IG, FB, Email).
        """
        active_tenant = tenant_id or self.tenant_id
        TenantSecurityGuard.validate_tenant_scope(active_tenant, self.tenant_id, "SupportHub Inbound Channel")

        conv_id = conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        # 1. Normalize Inbound Message
        try:
            channel_enum = ChannelType(channel.lower())
        except ValueError:
            channel_enum = ChannelType.WEBSITE

        normalized_msg = NormalizedInboundMessage(
            message_id=f"msg_{uuid.uuid4().hex[:10]}",
            conversation_id=conv_id,
            customer_id=sender_id,
            tenant_id=active_tenant,
            channel=channel_enum,
            text=text,
            timestamp=now_iso,
            sender_type=SenderType.CUSTOMER,
            metadata=metadata or {},
        )

        # 2. Resolve or Create Conversation Session
        if conv_id not in self.conversations:
            ticket_ref = self._generate_ticket_ref()
            session = ConversationSession(
                conversation_id=conv_id,
                tenant_id=active_tenant,
                customer_id=sender_id,
                channel=channel_enum.value,
                ticket_ref=ticket_ref,
                is_active=True,
                is_escalated=False,
            )
            self.conversations[conv_id] = session

            # Create Ticket Record
            self.tickets[ticket_ref] = TicketRecord(
                ticket_id=str(uuid.uuid4()),
                ticket_ref=ticket_ref,
                tenant_id=active_tenant,
                customer_id=sender_id,
                channel=channel_enum.value,
                status="new",
                priority="medium",
                subject=f"{channel_enum.value.capitalize()} Support Query",
                category="general",
                created_at=now_iso,
                updated_at=now_iso,
            )
        else:
            session = self.conversations[conv_id]

        session.add_turn(
            sender_type="customer",
            text=text,
            timestamp=now_iso,
        )

        # 3. Check if Conversation is already Escalated to Human Agent
        if session.is_escalated:
            handoff_reply = (
                "Your request is with a human support agent. An agent is reviewing your inquiry "
                "and will respond shortly."
            )
            return NormalizedAIResult(
                conversation_id=conv_id,
                customer_id=sender_id,
                tenant_id=active_tenant,
                intent="human_agent_hold",
                route="HUMAN",
                response_text=handoff_reply,
                escalation=EscalationDetail(required=True, reason="Already Escalated to Human Agent"),
            )

        # 4. Invoke AI Orchestrator Core
        ai_resp = self.orchestrator.process_message(
            query=normalized_msg.text,
            customer_id=normalized_msg.customer_id,
            conversation_id=conv_id,
            channel_type=channel_enum.value.upper(),
            use_llm=use_llm,
        )

        # 5. Handle Human Escalation Transition
        is_escalated = False
        escalation_detail = EscalationDetail()
        if ai_resp.escalation_decision and ai_resp.escalation_decision.should_escalate:
            is_escalated = True
            session.is_escalated = True
            ticket = self.tickets.get(session.ticket_ref)
            if ticket:
                ticket.status = "escalated"
                ticket.priority = (ai_resp.escalation_decision.priority or "high").lower()
                ticket.category = "escalation"
                ticket.updated_at = now_iso

            escalation_detail = EscalationDetail(
                required=True,
                reason=ai_resp.escalation_decision.reason,
                department="support",
                priority=ai_resp.escalation_decision.priority,
                summary=ai_resp.escalation_decision.escalation_summary,
                frustration_score=0.9,
            )

            # Record Handoff Payload
            handoff = TicketHandoffPayload(
                ticket_ref=session.ticket_ref,
                tenant_id=active_tenant,
                customer_id=sender_id,
                conversation_id=conv_id,
                reason=ai_resp.escalation_decision.reason,
                department="support",
                priority=ai_resp.escalation_decision.priority,
                summary=ai_resp.escalation_decision.escalation_summary,
                frustration_score=0.9,
                timestamp=now_iso,
            )
            self.escalation_handoffs.append(handoff)

        # 6. Map Citations
        citations = [
            RAGCitation(
                source_id=c.get("source_id", "UNKNOWN"),
                tenant_id=active_tenant,
                title=c.get("title", "Policy Document"),
                category=c.get("category", "policy"),
                chunk_index=c.get("chunk_index", 0),
                score=c.get("score", 0.0),
                snippet="",
            )
            for c in ai_resp.rag_citations
        ]

        # 7. Construct Normalized AI Result
        ai_result = NormalizedAIResult(
            conversation_id=conv_id,
            customer_id=sender_id,
            tenant_id=active_tenant,
            intent=ai_resp.route_type.lower(),
            route=ai_resp.route_type,
            response_text=ai_resp.content,
            is_grounded=ai_resp.is_grounded,
            grounding_violations=ai_resp.grounding_violations,
            escalation=escalation_detail,
            citations=citations,
            confidence=1.0,
            latency_ms=0,
        )

        session.add_turn(
            sender_type="ai",
            text=ai_resp.content,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # 8. Record Simulated Outbound Message
        self.outbound_messages.append({
            "conversation_id": conv_id,
            "channel": channel_enum.value,
            "recipient_id": sender_id,
            "text": ai_resp.content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        return ai_result

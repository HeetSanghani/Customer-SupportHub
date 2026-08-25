"""Ticket and human handoff payload contracts for SupportHub AI."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class TicketRecord:
    """Ticketing record representation in SupportHub."""
    ticket_id: str
    ticket_ref: str  # e.g., TCK-10001
    tenant_id: str
    customer_id: str
    channel: str
    status: str  # 'new', 'open', 'waiting', 'escalated', 'resolved', 'closed'
    priority: str  # 'urgent', 'high', 'medium', 'low'
    subject: str
    category: str
    agent_id: Optional[str] = None
    ai_resolved: bool = False
    ai_summary: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TicketHandoffPayload:
    """Data payload emitted when AI orchestrator escalates a conversation to human agent."""
    ticket_ref: str
    tenant_id: str
    customer_id: str
    conversation_id: str
    reason: str
    department: str
    priority: str
    summary: str
    frustration_score: float = 0.0
    relevant_entity_ids: Dict[str, Any] = field(default_factory=dict)
    transcript: List[Dict[str, str]] = field(default_factory=list)
    timestamp: Optional[str] = None

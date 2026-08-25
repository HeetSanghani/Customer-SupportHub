"""Conversation session and state contracts for SupportHub AI."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class ConversationTurn:
    """A single historical turn in a conversation session."""
    turn_id: str
    sender_type: str  # 'customer', 'agent', 'ai', 'system'
    text: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationSession:
    """Normalized conversation session container across channels and tickets."""
    conversation_id: str
    tenant_id: str
    customer_id: str
    channel: str  # 'website', 'whatsapp', 'instagram', 'facebook', 'email'
    ticket_ref: Optional[str] = None
    is_active: bool = True
    is_escalated: bool = False
    assigned_agent_id: Optional[str] = None
    slots: Dict[str, Any] = field(default_factory=dict)
    history: List[ConversationTurn] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_turn(self, sender_type: str, text: str, timestamp: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.history.append(
            ConversationTurn(
                turn_id=f"turn_{len(self.history) + 1}",
                sender_type=sender_type,
                text=text,
                timestamp=timestamp,
                metadata=metadata or {},
            )
        )

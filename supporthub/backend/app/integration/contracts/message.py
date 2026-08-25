"""Normalized inbound and outbound message contracts for SupportHub AI."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List


class ChannelType(str, Enum):
    WEBSITE = "website"
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    EMAIL = "email"


class SenderType(str, Enum):
    CUSTOMER = "customer"
    AGENT = "agent"
    AI = "ai"
    SYSTEM = "system"


@dataclass
class NormalizedInboundMessage:
    """Channel-agnostic inbound customer message structure."""
    message_id: str
    conversation_id: str
    customer_id: str
    tenant_id: str
    channel: ChannelType
    text: str
    timestamp: str
    sender_type: SenderType = SenderType.CUSTOMER
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    raw_payload: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "customer_id": self.customer_id,
            "tenant_id": self.tenant_id,
            "channel": self.channel.value if isinstance(self.channel, ChannelType) else self.channel,
            "text": self.text,
            "timestamp": self.timestamp,
            "sender_type": self.sender_type.value if isinstance(self.sender_type, SenderType) else self.sender_type,
            "metadata": self.metadata,
        }

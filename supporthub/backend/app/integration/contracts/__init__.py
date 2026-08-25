"""SupportHub AI Integration Contracts Package."""
from app.integration.contracts.customer import CustomerIdentity, AuthContext
from app.integration.contracts.conversation import ConversationSession, ConversationTurn
from app.integration.contracts.message import NormalizedInboundMessage, ChannelType, SenderType
from app.integration.contracts.ticket import TicketRecord, TicketHandoffPayload
from app.integration.contracts.business_data import BusinessDataService
from app.integration.contracts.rag import RAGQueryRequest, RAGCitation, RAGSearchResult
from app.integration.contracts.ai_result import NormalizedAIResult, EscalationDetail

__all__ = [
    "CustomerIdentity",
    "AuthContext",
    "ConversationSession",
    "ConversationTurn",
    "NormalizedInboundMessage",
    "ChannelType",
    "SenderType",
    "TicketRecord",
    "TicketHandoffPayload",
    "BusinessDataService",
    "RAGQueryRequest",
    "RAGCitation",
    "RAGSearchResult",
    "NormalizedAIResult",
    "EscalationDetail",
]

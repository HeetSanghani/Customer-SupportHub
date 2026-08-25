"""SupportHub AI Architecture - Phase 10 Integration Layer."""
from app.integration.contracts import (
    CustomerIdentity,
    AuthContext,
    ConversationSession,
    ConversationTurn,
    NormalizedInboundMessage,
    ChannelType,
    SenderType,
    TicketRecord,
    TicketHandoffPayload,
    BusinessDataService,
    RAGQueryRequest,
    RAGCitation,
    RAGSearchResult,
    NormalizedAIResult,
    EscalationDetail,
)
from app.integration.security import TenantSecurityGuard, TenantIsolationViolationError
from app.integration.adapters import ShopKartBusinessDataAdapter, MockSupportHubSystem

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
    "TenantSecurityGuard",
    "TenantIsolationViolationError",
    "ShopKartBusinessDataAdapter",
    "MockSupportHubSystem",
]

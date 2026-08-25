"""Customer identity and authentication context contracts for SupportHub AI."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class AuthContext:
    """Authentication and authorization state of the requesting user/customer."""
    is_authenticated: bool = False
    auth_method: str = "channel_identity"  # e.g., 'jwt', 'channel_identity', 'guest'
    token_verified: bool = False
    scopes: list[str] = field(default_factory=lambda: ["read:own_profile", "read:own_orders"])
    auth_timestamp: Optional[str] = None


@dataclass
class CustomerIdentity:
    """Normalized customer identity contract decoupled from database schemas."""
    customer_id: str
    tenant_id: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    channel_user_id: Optional[str] = None  # e.g., WhatsApp phone, IG user ID, PSID
    auth_context: AuthContext = field(default_factory=AuthContext)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "tenant_id": self.tenant_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "channel_user_id": self.channel_user_id,
            "is_authenticated": self.auth_context.is_authenticated,
            "metadata": self.metadata,
        }

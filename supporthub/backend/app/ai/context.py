"""In-memory Conversation Context State Machine."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone


@dataclass
class TurnRecord:
    """Represents a single message turn in the conversation."""
    turn_id: int
    role: str                     # "user" | "assistant" | "system"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    intent: Optional[str] = None
    tools_called: List[str] = field(default_factory=list)


@dataclass
class ConversationContext:
    """In-memory session state for tracking multi-turn interactions."""
    conversation_id: str
    customer_id: Optional[str] = None
    channel_type: str = "WEBSITE"
    active_order_id: Optional[str] = None
    active_product_id: Optional[str] = None
    active_return_id: Optional[str] = None
    active_refund_id: Optional[str] = None
    last_order_id: Optional[str] = None
    last_product_id: Optional[str] = None
    previous_intent: Optional[str] = None
    slot_needed: Optional[str] = None
    history: List[TurnRecord] = field(default_factory=list)
    escalated: bool = False
    frustration_score: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_user_message(self, content: str, intent: Optional[str] = None) -> TurnRecord:
        """Record an incoming user message."""
        turn = TurnRecord(
            turn_id=len(self.history) + 1,
            role="user",
            content=content,
            intent=intent
        )
        self.history.append(turn)
        return turn

    def add_assistant_message(
        self,
        content: str,
        tools: Optional[List[str]] = None,
        intent: Optional[str] = None
    ) -> TurnRecord:
        """Record an outgoing assistant response."""
        turn = TurnRecord(
            turn_id=len(self.history) + 1,
            role="assistant",
            content=content,
            intent=intent,
            tools_called=tools or []
        )
        self.history.append(turn)
        return turn

    def get_recent_history(self, limit: int = 5) -> List[TurnRecord]:
        """Return the most recent N turns."""
        return self.history[-limit:] if len(self.history) > limit else self.history

    def update_slots(
        self,
        order_id: Optional[str] = None,
        product_id: Optional[str] = None,
        return_id: Optional[str] = None,
        refund_id: Optional[str] = None
    ) -> None:
        """Update active entity slots in memory (legacy, non-domain-aware)."""
        if order_id:
            self.active_order_id = order_id
            self.last_order_id = order_id
        if product_id:
            self.active_product_id = product_id
            self.last_product_id = product_id
        if return_id:
            self.active_return_id = return_id
        if refund_id:
            self.active_refund_id = refund_id

    def update_slots_domain_aware(
        self,
        explicit_entities: Dict[str, Any],
        authorized: bool = True
    ) -> None:
        """Update entity slots with domain-awareness.

        Rules:
        - Only persists slots for AUTHORIZED entities (Fix #2 — security-guarded context).
        - When an explicit entity of one domain is present in the current query, stale
          slots from UNRELATED domains are cleared (Fix #3 — domain isolation).
        - Legitimate same-domain follow-up context is preserved: if the new query has
          no explicit entities at all, existing slots remain intact.

        Domain groupings (mutually exclusive for clearing purposes):
          PRODUCT_DOMAIN:  product_id
          ORDER_DOMAIN:    order_id
          RETURN_DOMAIN:   return_id
          REFUND_DOMAIN:   refund_id
        """
        if not authorized:
            # Security denied — never persist any entity from this turn.
            return

        _is_guest = (self.customer_id is None or str(self.customer_id).upper() in ("GUEST", ""))

        new_product_id = explicit_entities.get("product_id")
        new_order_id   = None if _is_guest else explicit_entities.get("order_id")
        new_return_id  = None if _is_guest else explicit_entities.get("return_id")
        new_refund_id  = None if _is_guest else explicit_entities.get("refund_id")

        # If no new explicit IDs at all → leave context unchanged (follow-up turn).
        has_any_explicit = any([new_product_id, new_order_id, new_return_id, new_refund_id])
        if not has_any_explicit:
            return

        # Apply domain-isolation clearing: when a new domain arrives, clear active slots of other domains.
        if new_product_id:
            # Switching to PRODUCT domain → clear ORDER / RETURN / REFUND stale slots.
            self.active_product_id = new_product_id
            self.last_product_id   = new_product_id
            self.active_order_id   = None
            self.active_return_id  = None
            self.active_refund_id  = None

        if new_order_id:
            # Switching to ORDER domain → clear PRODUCT / RETURN / REFUND stale slots.
            self.active_order_id   = new_order_id
            self.last_order_id     = new_order_id
            self.active_product_id = None
            self.active_return_id  = None
            self.active_refund_id  = None

        if new_return_id:
            self.active_return_id  = new_return_id
            self.active_product_id = None

        if new_refund_id:
            self.active_refund_id  = new_refund_id
            self.active_product_id = None

    def revert_slots(
        self,
        prev_order_id: Optional[str] = None,
        prev_product_id: Optional[str] = None,
        prev_return_id: Optional[str] = None,
        prev_refund_id: Optional[str] = None
    ) -> None:
        """Revert slots to a previous known-good state after a security denial."""
        self.active_order_id   = prev_order_id
        self.active_product_id = prev_product_id
        self.active_return_id  = prev_return_id
        self.active_refund_id  = prev_refund_id


class ContextManager:
    """Manages active conversation contexts in memory."""

    def __init__(self):
        self._contexts: Dict[str, ConversationContext] = {}

    def get_or_create(
        self,
        conversation_id: str,
        customer_id: Optional[str] = None,
        channel_type: str = "WEBSITE"
    ) -> ConversationContext:
        """Retrieve existing context or instantiate a new one."""
        if conversation_id not in self._contexts:
            self._contexts[conversation_id] = ConversationContext(
                conversation_id=conversation_id,
                customer_id=customer_id,
                channel_type=channel_type
            )
        elif customer_id and not self._contexts[conversation_id].customer_id:
            self._contexts[conversation_id].customer_id = customer_id
        return self._contexts[conversation_id]

    def clear(self, conversation_id: str) -> None:
        """Clear a context from memory."""
        self._contexts.pop(conversation_id, None)

    def clear_all(self) -> None:
        """Clear all active conversation contexts from memory."""
        self._contexts.clear()


# Global context manager singleton
context_manager = ContextManager()

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict


class SubQuestion(TypedDict, total=False):
    """One decomposed piece of the customer's message."""
    id: str
    original_text: str
    normalized_text: str
    text: str  # Backwards compatibility alias for normalized_text
    intent: Optional[Any]
    entities: Dict[str, Any]
    route: Optional[Any]
    context_reference: Dict[str, Any]
    authorization_status: str  # "ALLOWED", "DENIED"
    execution_status: str      # "SUCCESS", "FAILED"
    response: Optional[Any]
    error: Optional[str]


class GraphState(TypedDict, total=False):
    conversation_id: str
    customer_id: Optional[str]
    channel_type: str
    active_order_id: Optional[str]
    active_product_id: Optional[str]
    active_return_id: Optional[str]
    active_refund_id: Optional[str]
    last_order_id: Optional[str]
    last_product_id: Optional[str]
    previous_intent: Optional[str]
    slot_needed: Optional[str]
    frustration_score: int
    metadata: Dict[str, Any]

    raw_query: str
    use_llm: Optional[bool]
    sub_questions: List[SubQuestion]
    escalated: bool
    escalation_decision: Optional[Any]
    final_response: Optional[Any]

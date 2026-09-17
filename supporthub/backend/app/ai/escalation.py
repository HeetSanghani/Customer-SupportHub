import re
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, timezone


@dataclass
class EscalationDecision:
    """Structured dossier for human agent handoff."""
    should_escalate: bool
    reason: str                  # "EXPLICIT_HUMAN_REQUEST", "SUPERVISOR_REQUEST", "ANGRY_SENTIMENT", "REPEATED_UNRESOLVED", "DEADLOCK", "FINANCIAL_DISCREPANCY", "ACCOUNT_SECURITY", "NONE"
    priority: str                # "LOW", "MEDIUM", "HIGH", "URGENT", "CRITICAL"
    escalation_summary: str
    customer_message: str
    customer_id: Optional[str] = None
    conversation_id: Optional[str] = None
    active_order_id: Optional[str] = None
    last_ai_response: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EscalationEvaluator:
    """Evaluates conversation state and messages to trigger human escalation."""

    HUMAN_KEYWORDS = [
        "human agent", "talk to human", "talk to a human", "talk with human", "talk with a human",
        "talk with humen", "talk with humen agent", "talk to humen", "talk to humen agent",
        "talk with agent", "talk to agent", "talk to an agent", "talk with an agent",
        "speak to a representative", "speak with a representative", "speak to representative",
        "speak with representative", "speak to human", "speak with human", "speak to a human",
        "speak with a human", "speak to agent", "speak with agent", "speak to an agent",
        "speak with an agent", "real person", "real human", "actual human", "live person",
        "live agent", "real agent", "customer care executive", "customer care agent",
        "customer support agent", "customer service agent", "human customer agent", "customer agent",
        "human support", "human", "humen", "talk to someone", "talk with someone", "speak to someone",
        "speak with someone", "support agent", "connect me to an agent", "connect me to a human",
        "connect me to human", "connect me with an agent", "connect me with a human", "connect to human",
        "connect with human", "connect to agent", "connect with agent", "connect to customer care",
        "connect with customer care", "transfer me to a human", "transfer me to human",
        "transfer to human", "transfer to a human", "transfer to human agent",
        "transfer to human customer agent", "transfer your request to our human customer agent",
        "transfer my request to human", "transfer request to human",
        "transfer request to our human customer agent", "transfer to customer agent",
        "transfer me to an agent", "transfer to agent", "transfer me to live agent",
        "representative", "stop giving me automated responses", "i want a human", "i want human",
        "i need a human", "i need human", "want human agent", "need human agent",
        "want to talk with", "want to talk to", "can i talk to a human", "can i speak with a human",
        "can i talk to someone", "let me speak to a human", "put me through to an agent",
        "switch to human", "hand over to human", "human representative"
    ]

    HUMAN_PATTERNS = [
        # Match "talk/speak/chat/connect/transfer/handoff with/to (a) human/agent/representative"
        re.compile(
            r"\b(?:talk|speak|chat|connect|transfer|reach|switch|handoff|put\s+me\s+through)\s+(?:with|to|me\s+to|me\s+with|request\s+to|my\s+request\s+to|your\s+request\s+to)?\s*(?:a|an|the|our)?\s*(?:real|live|actual)?\s*(?:hum[ae]n|person|agent|representative|rep|executive|specialist|team)\b",
            re.IGNORECASE
        ),
        # Match "want/need/get/give ... human/agent"
        re.compile(
            r"\b(?:want|need|get|give)\s+(?:to\s+(?:talk|speak|chat)\s+(?:with|to)|a|an)?\s*(?:real|live|actual)?\s*(?:hum[ae]n|person|agent|representative|customer\s+care)\b",
            re.IGNORECASE
        ),
        # Match explicit phrases like "human customer agent", "customer support agent", "real person", "live agent"
        re.compile(
            r"\b(?:hum[ae]n\s+(?:customer\s+)?agent|customer\s+(?:support\s+|care\s+)?agent|real\s+person|live\s+agent|human\s+support|human\s+representative)\b",
            re.IGNORECASE
        ),
        # Match "transfer ... to human"
        re.compile(
            r"\btransfer\s+(?:.*?\s+)?to\s+(?:our\s+|a\s+|an\s+)?hum[ae]n\b",
            re.IGNORECASE
        ),
    ]
    SUPERVISOR_KEYWORDS = [
        "manager", "supervisor", "escalate this", "escalation team", "head of support",
        "senior escalation manager"
    ]
    ANGER_KEYWORDS = [
        "useless", "terrible", "worst service", "worst customer service", "worst", "horrible", "fraud", "pathetic",
        "scam", "cheat", "cheat company", "will sue", "consumer court", "police", "legal action"
    ]
    DEADLOCK_KEYWORDS = [
        "nobody is helping", "stuck for hours", "not answering my question", "loop", "nobody is helping me"
    ]
    REPEATED_KEYWORDS = [
        "4th time", "3rd time", "second time", "contacting again", "still not resolved", "same issue"
    ]

    # Specific operational scenarios that require human intervention
    HIGH_RISK_OPERATIONAL_TRIGGERS = {
        "delivered_not_received": ("Marked delivered but not received by customer", "HIGH"),
        "charged_order_failed": ("Charged from account but order not created", "HIGH"),
        "charged_twice": ("Double payment deduction detected", "URGENT"),
        "lost_shipment": ("Shipment untraceable / stalled in transit", "HIGH"),
        "missed_pickup": ("Return pickup SLA missed by logistics carrier", "MEDIUM"),
        "failed_refund": ("Refund transaction failed in banking network", "HIGH"),
        "refund_discrepancy": ("Discrepancy in processed refund amount vs order total", "HIGH"),
        "account_compromised": ("Suspicious account activity / unauthorized access", "CRITICAL"),
        "counterfeit_seller": ("Counterfeit/fake/used goods dispute against seller", "URGENT")
    }

    def evaluate(
        self,
        query: str,
        customer_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        active_order_id: Optional[str] = None,
        frustration_score: int = 0
    ) -> EscalationDecision:
        """Evaluate if incoming query or session state warrants human escalation."""
        text = query.lower().strip()
        from app.ai.intent import normalize_query_typos
        text_norm = normalize_query_typos(query)

        if not active_order_id:
            m = re.search(r"\bORD-\d{3,5}\b", query, re.IGNORECASE)
            if m:
                active_order_id = m.group(0).upper()

        # 1. Explicit Human Agent Request (H01)
        is_human_request = (
            any(kw in text for kw in self.HUMAN_KEYWORDS) or
            any(kw in text_norm for kw in self.HUMAN_KEYWORDS) or
            any(pat.search(text) for pat in self.HUMAN_PATTERNS) or
            any(pat.search(text_norm) for pat in self.HUMAN_PATTERNS)
        )
        if is_human_request:
            return EscalationDecision(
                should_escalate=True,
                reason="EXPLICIT_HUMAN_REQUEST",
                priority="HIGH",
                escalation_summary="Customer explicitly requested transfer to a human support agent.",
                customer_message=query,
                customer_id=customer_id,
                conversation_id=conversation_id,
                active_order_id=active_order_id
            )

        # 2. Supervisor / Manager Request (H02)
        if any(kw in text for kw in self.SUPERVISOR_KEYWORDS):
            return EscalationDecision(
                should_escalate=True,
                reason="SUPERVISOR_REQUEST",
                priority="URGENT",
                escalation_summary="Customer requested senior manager/supervisor intervention.",
                customer_message=query,
                customer_id=customer_id,
                conversation_id=conversation_id,
                active_order_id=active_order_id
            )

        # 3. High Frustration / Abusive Sentiment / Legal Threat (H03)
        if any(kw in text for kw in self.ANGER_KEYWORDS):
            return EscalationDecision(
                should_escalate=True,
                reason="ANGRY_SENTIMENT",
                priority="HIGH",
                escalation_summary="High customer frustration / legal action notice detected.",
                customer_message=query,
                customer_id=customer_id,
                conversation_id=conversation_id,
                active_order_id=active_order_id
            )

        # 4. Repeated Unresolved Issue (H04)
        if any(kw in text for kw in self.REPEATED_KEYWORDS):
            return EscalationDecision(
                should_escalate=True,
                reason="REPEATED_UNRESOLVED",
                priority="HIGH",
                escalation_summary="Customer reporting repeated contacts regarding the same unresolved issue.",
                customer_message=query,
                customer_id=customer_id,
                conversation_id=conversation_id,
                active_order_id=active_order_id
            )

        # 5. Deadlock / Frustration (H05)
        if any(kw in text for kw in self.DEADLOCK_KEYWORDS):
            return EscalationDecision(
                should_escalate=True,
                reason="DEADLOCK",
                priority="HIGH",
                escalation_summary="Customer reached support deadlock with automated assistant.",
                customer_message=query,
                customer_id=customer_id,
                conversation_id=conversation_id,
                active_order_id=active_order_id
            )

        # 6. Operational High Risk Triggers
        # O08: Delivered but not received
        if ("delivered" in text and ("never received" in text or "not received" in text or "didn't receive" in text)):
            return self._build_op_escalation("delivered_not_received", query, customer_id, conversation_id, active_order_id)
        
        # PAY04: Deducted but order failed
        if ("deducted" in text or "debited" in text) and ("failed" in text or "not placed" in text or "not confirmed" in text):
            return self._build_op_escalation("charged_order_failed", query, customer_id, conversation_id, active_order_id)
        
        # PAY05: Charged twice
        if "charged twice" in text or "double charged" in text or "two charges" in text:
            return self._build_op_escalation("charged_twice", query, customer_id, conversation_id, active_order_id)
        
        # S05: Lost shipment / tracking stalled
        if "not updated in a week" in text or "is it lost" in text or "lost in transit" in text or "not moved for" in text:
            return self._build_op_escalation("lost_shipment", query, customer_id, conversation_id, active_order_id)
        
        # R06: Missed pickup
        if "did not show up on the scheduled pickup" in text or "nobody came to pick up" in text or "courier did not show up" in text:
            return self._build_op_escalation("missed_pickup", query, customer_id, conversation_id, active_order_id)
        
        # F04: Refund failed
        if "refund failed" in text or "failed for return" in text:
            return self._build_op_escalation("failed_refund", query, customer_id, conversation_id, active_order_id)
        
        # F05: Refund discrepancy
        if ("only received" in text and "refund" in text) or "wrong refund amount" in text or "refund amount is less" in text:
            return self._build_op_escalation("refund_discrepancy", query, customer_id, conversation_id, active_order_id)
        
        # A04: Account compromised
        if "logged into my account" in text or "another city" in text or "suspicious login" in text or "unauthorized access" in text:
            return self._build_op_escalation("account_compromised", query, customer_id, conversation_id, active_order_id)
        
        # SE03: Counterfeit or used product dispute
        if "used product instead of a brand new" in text or "fake product" in text or "counterfeit" in text:
            return self._build_op_escalation("counterfeit_seller", query, customer_id, conversation_id, active_order_id)

        # No escalation needed
        return EscalationDecision(
            should_escalate=False,
            reason="NONE",
            priority="LOW",
            escalation_summary="Autonomous resolution pathway.",
            customer_message=query,
            customer_id=customer_id,
            conversation_id=conversation_id,
            active_order_id=active_order_id
        )

    def _build_op_escalation(
        self,
        trigger_key: str,
        query: str,
        customer_id: Optional[str],
        conversation_id: Optional[str],
        active_order_id: Optional[str]
    ) -> EscalationDecision:
        summary, priority = self.HIGH_RISK_OPERATIONAL_TRIGGERS[trigger_key]
        return EscalationDecision(
            should_escalate=True,
            reason=f"OPERATIONAL_{trigger_key.upper()}",
            priority=priority,
            escalation_summary=summary,
            customer_message=query,
            customer_id=customer_id,
            conversation_id=conversation_id,
            active_order_id=active_order_id
        )


escalation_evaluator = EscalationEvaluator()

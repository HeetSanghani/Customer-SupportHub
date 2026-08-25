"""Stable AI Result contract emitted by SupportHub AI Orchestrator."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from app.integration.contracts.rag import RAGCitation


@dataclass
class EscalationDetail:
    """Escalation decision metadata."""
    required: bool = False
    reason: Optional[str] = None
    department: Optional[str] = None
    priority: Optional[str] = None
    summary: Optional[str] = None
    frustration_score: float = 0.0


@dataclass
class NormalizedAIResult:
    """Standardized result produced by the AI orchestrator for any channel."""
    conversation_id: str
    customer_id: str
    tenant_id: str
    intent: str
    route: str  # 'STRUCTURED', 'RAG', 'HYBRID', 'SECURITY', 'HUMAN'
    response_text: str
    is_grounded: bool = True
    grounding_violations: List[str] = field(default_factory=list)
    escalation: EscalationDetail = field(default_factory=EscalationDetail)
    citations: List[RAGCitation] = field(default_factory=list)
    confidence: float = 1.0
    latency_ms: int = 0
    model_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "customer_id": self.customer_id,
            "tenant_id": self.tenant_id,
            "intent": self.intent,
            "route": self.route,
            "response": self.response_text,
            "is_grounded": self.is_grounded,
            "grounding_violations": self.grounding_violations,
            "escalation": {
                "required": self.escalation.required,
                "reason": self.escalation.reason,
                "department": self.escalation.department,
                "priority": self.escalation.priority,
                "summary": self.escalation.summary,
            },
            "citations": [
                {
                    "source_id": c.source_id,
                    "title": c.title,
                    "score": c.score,
                    "snippet": c.snippet,
                }
                for c in self.citations
            ],
            "confidence": self.confidence,
            "latency_ms": self.latency_ms,
            "metadata": self.metadata,
        }

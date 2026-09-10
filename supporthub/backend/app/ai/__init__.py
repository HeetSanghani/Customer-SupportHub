"""SupportHub AI Reasoning, Security, and Orchestration Package."""
import os
from app.ai.context import ConversationContext, TurnRecord, ContextManager, context_manager
from app.ai.intent import IntentCategory, IntentResult, IntentClassifier, intent_classifier
from app.ai.security import SecurityDecision, SecurityValidator, security_validator
from app.ai.escalation import EscalationDecision, EscalationEvaluator, escalation_evaluator
from app.ai.tools import ToolRegistry, tool_registry
from app.ai.router import RouteType, RouteDecision, AIRouter, ai_router
from app.ai.response import AIResponse, ResponseSynthesizer, response_synthesizer
from app.ai.subject import generate_ai_ticket_subject, is_generic_subject, format_subject_from_query
# Lazy imports to break circular dependency with app.rag
_embedding_provider = None

def generate_embedding(text: str) -> list[float]:
    """Generates a 768-dimensional embedding vector for pgvector storage."""
    global _embedding_provider
    if _embedding_provider is None:
        try:
            from app.rag.embeddings import get_embedding_provider
            _embedding_provider = get_embedding_provider()
        except Exception:
            _embedding_provider = None

    if _embedding_provider is not None:
        try:
            vec = _embedding_provider.embed_text(text)
            if vec and len(vec) == 768:
                return vec
            elif vec:
                if len(vec) < 768:
                    return list(vec) + [0.0] * (768 - len(vec))
                return list(vec[:768])
        except Exception:
            pass

    from app.rag.embeddings import _make_fallback_vector
    return _make_fallback_vector(text)

def __getattr__(name: str):
    if name in ("AIOrchestrator", "ai_orchestrator"):
        import app.ai.orchestrator as _orch
        return getattr(_orch, name)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    "ConversationContext",
    "TurnRecord",
    "ContextManager",
    "context_manager",
    "IntentCategory",
    "IntentResult",
    "IntentClassifier",
    "intent_classifier",
    "SecurityDecision",
    "SecurityValidator",
    "security_validator",
    "EscalationDecision",
    "EscalationEvaluator",
    "escalation_evaluator",
    "ToolRegistry",
    "tool_registry",
    "RouteType",
    "RouteDecision",
    "AIRouter",
    "ai_router",
    "AIResponse",
    "ResponseSynthesizer",
    "response_synthesizer",
    "AIOrchestrator",
    "ai_orchestrator",
    "generate_embedding",
    "generate_ai_ticket_subject",
    "is_generic_subject",
    "format_subject_from_query",
]

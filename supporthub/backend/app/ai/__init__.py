"""SupportHub AI Reasoning, Security, and Orchestration Package."""
import os
from app.ai.context import ConversationContext, TurnRecord, ContextManager, context_manager
from app.ai.intent import IntentCategory, IntentResult, IntentClassifier, intent_classifier
from app.ai.security import SecurityDecision, SecurityValidator, security_validator
from app.ai.escalation import EscalationDecision, EscalationEvaluator, escalation_evaluator
from app.ai.tools import ToolRegistry, tool_registry
from app.ai.router import RouteType, RouteDecision, AIRouter, ai_router
from app.ai.response import AIResponse, ResponseSynthesizer, response_synthesizer
# Lazy imports to break circular dependency with app.rag
_embedding_provider = None

def generate_embedding(text: str) -> list[float]:
    """Generates a 1536-dimensional embedding vector for pgvector storage."""
    global _embedding_provider
    if _embedding_provider is None:
        from app.rag.embeddings import LocalVectorEmbeddingProvider
        _embedding_provider = LocalVectorEmbeddingProvider()
    vec = _embedding_provider.embed_text(text)
    if len(vec) < 1536:
        vec.extend([0.0] * (1536 - len(vec)))
    elif len(vec) > 1536:
        vec = vec[:1536]
    return vec

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
]

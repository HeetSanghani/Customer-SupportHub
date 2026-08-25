"""Base provider interface for SupportHub AI LLM integration."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.ai.llm.models import LLMRequest, LLMResponse


class LLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the provider (e.g. 'gemini', 'openai', 'anthropic', 'deterministic_test')."""
        pass

    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Execute a text generation request synchronously."""
        pass

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate structured JSON conforming to a JSON Schema."""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Check provider connectivity and model readiness."""
        pass

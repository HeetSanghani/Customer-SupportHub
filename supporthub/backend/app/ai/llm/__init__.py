"""SupportHub AI LLM Module - Provider-Independent Abstractions."""
from app.ai.llm.models import (
    LLMMessage,
    LLMRole,
    LLMRequest,
    LLMResponse,
    TokenUsage
)
from app.ai.llm.errors import (
    LLMError,
    LLMConfigurationError,
    LLMAuthenticationError,
    LLMConnectionError,
    LLMTimeoutError,
    LLMRateLimitError,
    LLMValidationError,
    LLMContentFilterError
)
from app.ai.llm.base import LLMProvider
from app.ai.llm.provider import (
    GeminiProvider,
    OpenAIProvider,
    DeterministicFallbackProvider,
    get_llm_provider
)
from app.ai.llm.client import LLMClient, llm_client

__all__ = [
    "LLMMessage",
    "LLMRole",
    "LLMRequest",
    "LLMResponse",
    "TokenUsage",
    "LLMError",
    "LLMConfigurationError",
    "LLMAuthenticationError",
    "LLMConnectionError",
    "LLMTimeoutError",
    "LLMRateLimitError",
    "LLMValidationError",
    "LLMContentFilterError",
    "LLMProvider",
    "GeminiProvider",
    "OpenAIProvider",
    "DeterministicFallbackProvider",
    "get_llm_provider",
    "LLMClient",
    "llm_client"
]

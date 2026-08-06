"""
app/services/ai/exceptions.py

Domain exceptions for the AI Orchestration layer.

WHY THESE EXIST:
  Raw LLM SDK exceptions (anthropic.APIError, google.APIError, openai.APIError)
  are provider-specific. If your router catches `anthropic.APIError`, you've
  coupled your HTTP layer to a specific AI vendor.

  These domain exceptions decouple the rest of your application from providers:
    - Router catches: AIProviderError → returns 503
    - Router catches: TokenLimitExceeded → returns 422
    - Orchestrator catches: RateLimitExceeded → triggers retry
    - Tests mock: AIProviderError without importing any SDK

  This is the same pattern as AWS SDK → boto3 exceptions wrapped in domain errors.

HIERARCHY:
  AIError (base)
  ├── AIProviderError      → LLM API call failed (network, auth, server error)
  ├── ContextBuildError    → Failed to assemble LLM context from ConversationContext
  ├── PromptBuildError     → Failed to construct prompt
  ├── ResponseParseError   → LLM returned an unparseable response
  ├── TokenLimitExceeded   → Input or output exceeded token budget
  └── RateLimitExceeded    → Provider rate limit hit (triggers retry)
"""

from __future__ import annotations


class AIError(Exception):
    """Base exception for all AI Orchestration layer errors."""

    def __init__(self, message: str, detail: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail or message


class AIProviderError(AIError):
    """
    Raised when an LLM provider API call fails.

    Wraps provider-specific errors (Anthropic, Gemini, OpenAI) so the rest
    of the codebase never imports provider SDKs directly.

    Attributes:
        provider: "gemini" | "claude" | "openai" | "ollama" | "openrouter"
        status_code: HTTP status from the provider API (if available)
        is_retryable: True if the error warrants an automatic retry
    """

    def __init__(
        self,
        provider: str,
        message: str,
        cause: Exception | None = None,
        status_code: int | None = None,
        is_retryable: bool = False,
    ) -> None:
        self.provider = provider
        self.cause = cause
        self.status_code = status_code
        self.is_retryable = is_retryable
        super().__init__(
            message=f"[{provider}] {message}",
            detail=str(cause) if cause else message,
        )


class ContextBuildError(AIError):
    """
    Raised when the ContextBuilder cannot assemble LLMContext.

    Example causes:
      - ConversationContext is missing required fields
      - History contains corrupted message records
    """

    def __init__(self, reason: str) -> None:
        super().__init__(
            message="Failed to build LLM context",
            detail=reason,
        )


class PromptBuildError(AIError):
    """
    Raised when the PromptBuilder cannot construct the prompt.

    Example causes:
      - System prompt template rendering fails
      - Business rules are undefined
    """

    def __init__(self, reason: str) -> None:
        super().__init__(
            message="Failed to build prompt",
            detail=reason,
        )


class ResponseParseError(AIError):
    """
    Raised when the ResponseParser cannot normalize the LLM's raw output.

    Example causes:
      - LLM returned empty content
      - Expected JSON structure but got plain text
      - Provider returned an unexpected response format
    """

    def __init__(self, provider: str, reason: str, raw_response: str | None = None) -> None:
        self.provider = provider
        self.raw_response = raw_response
        super().__init__(
            message=f"Failed to parse response from {provider}",
            detail=reason,
        )


class TokenLimitExceeded(AIError):
    """
    Raised when the prompt + history exceeds the model's context window.

    The orchestrator should handle this by truncating history and retrying.

    Attributes:
        input_tokens: estimated tokens in the prompt
        max_tokens: the model's maximum context window
    """

    def __init__(self, input_tokens: int, max_tokens: int) -> None:
        self.input_tokens = input_tokens
        self.max_tokens = max_tokens
        super().__init__(
            message="Token limit exceeded",
            detail=(
                f"Input estimated at {input_tokens} tokens, "
                f"but model maximum is {max_tokens} tokens."
            ),
        )


class RateLimitExceeded(AIError):
    """
    Raised when the LLM provider returns a rate limit response (HTTP 429).

    The ModelAdapter catches provider-specific 429s and re-raises as this.
    The orchestrator can then decide to retry with exponential backoff.

    Attributes:
        retry_after_seconds: if the provider sends a Retry-After header
    """

    def __init__(self, provider: str, retry_after_seconds: int | None = None) -> None:
        self.provider = provider
        self.retry_after_seconds = retry_after_seconds
        super().__init__(
            message=f"Rate limit exceeded on {provider}",
            detail=(
                f"Retry after {retry_after_seconds}s"
                if retry_after_seconds
                else "No retry-after header provided."
            ),
        )

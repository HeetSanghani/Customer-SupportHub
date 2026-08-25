"""LLM Exception classes for SupportHub AI Architecture."""


class LLMError(Exception):
    """Base exception for all LLM-related errors."""
    pass


class LLMConfigurationError(LLMError):
    """Raised when LLM provider is not configured or missing required keys."""
    pass


class LLMAuthenticationError(LLMError):
    """Raised when authentication with LLM provider fails."""
    pass


class LLMConnectionError(LLMError):
    """Raised when network connection to LLM provider fails."""
    pass


class LLMTimeoutError(LLMError):
    """Raised when LLM request times out."""
    pass


class LLMRateLimitError(LLMError):
    """Raised when LLM request exceeds rate limits or quota."""
    pass


class LLMValidationError(LLMError):
    """Raised when LLM output cannot be parsed into the expected schema."""
    pass


class LLMContentFilterError(LLMError):
    """Raised when LLM request or response is blocked by safety filters."""
    pass

"""
app/services/whatsapp/exceptions.py

Domain exceptions for the WhatsApp Outbound Delivery Layer.

WHY THIS FILE EXISTS:
  Meta's WhatsApp Cloud API returns various HTTP status codes and error payloads:
    - HTTP 400 with subcode 131030 (Recipient phone number not in allowed list)
    - HTTP 401 (Invalid OAuth access token)
    - HTTP 429 (Rate limit hit / message quota exceeded)
    - HTTP 500/503 (Meta internal server error)

  If your high-level sender or application logic catches raw `httpx.HTTPStatusError`
  or inspects raw JSON dictionaries like `response.json()["error"]["code"]`, your
  application code becomes tightly coupled to Meta's specific HTTP API structure.

  These domain exceptions wrap raw HTTP and Meta API errors into clean, typed
  Python exceptions:
    - Retry logic inspects `is_retryable` flag or exception type.
    - Application controllers catch `WhatsAppProviderError` without importing HTTP libraries.
    - Monitoring/Sentry categorizes errors precisely by domain type.

HIERARCHY:
  WhatsAppDeliveryError (base)
  ├── WhatsAppProviderError    → Meta returned an API error response (4xx/5xx)
  │   ├── AuthenticationError  → Invalid or expired Meta OAuth access token (401/403)
  │   └── RateLimitError       → Meta rate limit or throughput quota exceeded (429)
  ├── FormattingError          → Failed to construct valid Meta JSON payload
  ├── DeliveryFailedError      → Message delivery marked as failed
  └── RetryExhaustedError      → Max retry attempts reached without success
"""

from __future__ import annotations

from typing import Any, Optional


class WhatsAppDeliveryError(Exception):
    """Base exception for all WhatsApp Outbound Delivery Layer errors."""

    def __init__(self, message: str, detail: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail or message


class WhatsAppProviderError(WhatsAppDeliveryError):
    """
    Raised when Meta's Cloud API returns an error response.

    Attributes:
        status_code: HTTP status code from Meta (e.g., 400, 401, 429, 500).
        error_code: Meta-specific sub-code (e.g., 131030, 100, 190).
        error_subcode: Meta-specific detailed subcode.
        is_retryable: True if error represents a transient failure (e.g., 429, 500, 503).
        raw_error: Complete error dictionary returned by Meta.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: Optional[int] = None,
        error_subcode: Optional[int] = None,
        is_retryable: bool = False,
        raw_error: Optional[dict[str, Any]] = None,
    ) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.error_subcode = error_subcode
        self.is_retryable = is_retryable
        self.raw_error = raw_error or {}
        
        detail_msg = f"[HTTP {status_code or '???'} | Meta Code {error_code or '???'}] {message}"
        super().__init__(message=message, detail=detail_msg)


class AuthenticationError(WhatsAppProviderError):
    """
    Raised when Meta rejects the request due to authentication/authorization failure.

    Example: Invalid WHATSAPP_ACCESS_TOKEN, expired token, or token lacks permissions.
    NON-RETRYABLE. Requires engineer intervention or token refresh.
    """

    def __init__(
        self,
        message: str = "Meta WhatsApp authentication failed. Invalid or expired token.",
        status_code: int = 401,
        error_code: Optional[int] = None,
        raw_error: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status_code,
            error_code=error_code,
            is_retryable=False,
            raw_error=raw_error,
        )


class RateLimitError(WhatsAppProviderError):
    """
    Raised when Meta rate-limits the phone number or app account (HTTP 429 / Code 130429).

    RETRYABLE with exponential backoff.
    """

    def __init__(
        self,
        message: str = "Meta WhatsApp Cloud API rate limit exceeded.",
        status_code: int = 429,
        error_code: Optional[int] = None,
        retry_after_seconds: Optional[int] = None,
        raw_error: Optional[dict[str, Any]] = None,
    ) -> None:
        self.retry_after_seconds = retry_after_seconds
        super().__init__(
            message=message,
            status_code=status_code,
            error_code=error_code,
            is_retryable=True,
            raw_error=raw_error,
        )


class FormattingError(WhatsAppDeliveryError):
    """
    Raised when the Outbound Formatter fails to convert domain content into
    a valid Meta API JSON payload.

    Examples:
      - Message text exceeds Meta's 4096 character limit
      - Quick reply buttons exceed 3 buttons or 20 characters per button label
      - Media URL is missing or malformed
    """

    def __init__(self, reason: str) -> None:
        super().__init__(
            message="Failed to format WhatsApp outbound payload",
            detail=reason,
        )


class DeliveryFailedError(WhatsAppDeliveryError):
    """
    Raised when Meta accepts the API call but asynchronously reports delivery failure
    or when the outbound client fails to dispatch the payload after execution.
    """

    def __init__(self, message_id: str, reason: str) -> None:
        self.message_id = message_id
        super().__init__(
            message=f"WhatsApp delivery failed for message {message_id}",
            detail=reason,
        )


class RetryExhaustedError(WhatsAppDeliveryError):
    """
    Raised when all configured retry attempts have been exhausted for a transient error.

    Attributes:
        attempts: Number of total attempts made.
        last_error: The underlying exception from the final attempt.
    """

    def __init__(self, attempts: int, last_error: Exception) -> None:
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(
            message=f"WhatsApp delivery failed after {attempts} retry attempts.",
            detail=str(last_error),
        )

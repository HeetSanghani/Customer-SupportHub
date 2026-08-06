"""
app/services/whatsapp/retry.py

Resilience and Exponential Backoff Retry Engine for Meta API calls.

WHY THIS FILE EXISTS:
  Network calls to external third-party APIs (Meta Cloud API) will intermittently fail due to:
    - Transient network glitches / TCP timeouts
    - Meta rate-limiting (HTTP 429)
    - Meta server-side deployment blips (HTTP 500, 502, 503, 504)

  Without an explicit retry engine, a single transient 503 from Meta would drop
  the outbound customer reply completely.

  However, retrying ALL errors is dangerous:
    - Retrying 401 (Unauthorized) will fail every time and lock accounts.
    - Retrying 400 (Bad Request - invalid phone number format) wastes bandwidth.

  This module executes operations under a configurable `RetryPolicy` using:
    - Strict classification: Transient errors RETRY, Permanent errors FAIL IMMEDIATELY.
    - Exponential backoff: `delay = min(base * (factor ^ attempt), max_delay)`
    - Full Jitter: Randomizes sleep time to avoid thundering herd problem.
"""

from __future__ import annotations

import asyncio
import logging
import random
from typing import Awaitable, Callable, TypeVar

from app.services.whatsapp.exceptions import (
    AuthenticationError,
    RateLimitError,
    RetryExhaustedError,
    WhatsAppProviderError,
)
from app.services.whatsapp.models import RetryPolicy

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RetryExecutor:
    """
    Executes an async function under a given RetryPolicy with exponential backoff + jitter.

    Usage:
        executor = RetryExecutor(policy=RetryPolicy(max_retries=3))
        result = await executor.execute(
            func=client.send_raw_payload,
            payload=payload,
        )
    """

    def __init__(self, policy: RetryPolicy | None = None) -> None:
        self.policy = policy or RetryPolicy()

    async def execute(
        self,
        func: Callable[..., Awaitable[T]],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """
        Execute an async callable with automatic retries for transient errors.

        Args:
            func: The async function to execute.
            *args, **kwargs: Positional and keyword arguments passed to `func`.

        Returns:
            The return value of `func` upon success.

        Raises:
            RetryExhaustedError: If max retries are exceeded for a retryable error.
            WhatsAppProviderError / Exception: Immediately if non-retryable.
        """
        attempt = 0
        last_exception: Exception | None = None

        while attempt <= self.policy.max_retries:
            try:
                return await func(*args, **kwargs)

            except Exception as exc:
                last_exception = exc
                is_retryable = self._should_retry(exc)

                if not is_retryable or attempt >= self.policy.max_retries:
                    if is_retryable:
                        logger.error(
                            "❌ Retry limit exhausted | attempt=%d/%d | error=%s",
                            attempt + 1,
                            self.policy.max_retries + 1,
                            exc,
                        )
                        raise RetryExhaustedError(
                            attempts=attempt + 1,
                            last_error=exc,
                        ) from exc

                    logger.warning(
                        "🛑 Non-retryable error encountered | status=%s | error=%s",
                        getattr(exc, "status_code", "N/A"),
                        exc,
                    )
                    raise exc

                # Calculate backoff delay with full jitter
                delay = self._calculate_delay(attempt, exc)
                attempt += 1

                logger.warning(
                    "⚠️ Transient error on attempt %d/%d — retrying in %.2fs | error=%s",
                    attempt,
                    self.policy.max_retries,
                    delay,
                    exc,
                )

                await asyncio.sleep(delay)

        # Satisfy type checker
        raise RetryExhaustedError(
            attempts=attempt,
            last_error=last_exception or RuntimeError("Unknown retry error"),
        )

    # ─── Helper Methods ───────────────────────────────────────────────────────

    def _should_retry(self, exc: Exception) -> bool:
        """
        Determine if an exception represents a transient failure eligible for retry.

        Rules:
          1. AuthenticationError (401/403) → NEVER RETRY
          2. RateLimitError (429) → ALWAYS RETRY
          3. WhatsAppProviderError with status in `retryable_status_codes` → RETRY
          4. ConnectionError, TimeoutError, OSError → RETRY
          5. Any other exception → DO NOT RETRY
        """
        if isinstance(exc, AuthenticationError):
            return False

        if isinstance(exc, RateLimitError):
            return True

        if isinstance(exc, WhatsAppProviderError):
            if exc.is_retryable:
                return True
            if exc.status_code and exc.status_code in self.policy.retryable_status_codes:
                return True
            return False

        # Generic network / socket errors
        if isinstance(exc, (ConnectionError, TimeoutError, OSError)):
            return True

        return False

    def _calculate_delay(self, attempt: int, exc: Exception) -> float:
        """
        Calculate backoff duration with full jitter.

        Formula:
          backoff = min(base * (factor ^ attempt), max_delay)
          jittered_delay = random.uniform(0, backoff)
        """
        # If rate limit error contains Retry-After, prioritize it
        if isinstance(exc, RateLimitError) and exc.retry_after_seconds:
            return float(exc.retry_after_seconds)

        backoff = min(
            self.policy.base_delay_seconds * (self.policy.exponential_factor ** attempt),
            self.policy.max_delay_seconds,
        )
        # Apply full jitter: uniform random float between 0 and backoff
        return random.uniform(0.5 * backoff, backoff)

"""LLM Client singleton providing resilience, retries, and latency tracking."""
import time
import logging
from typing import Dict, Any, Optional, List

from app.ai.config import settings
from app.ai.llm.base import LLMProvider
from app.ai.llm.provider import get_llm_provider
from app.ai.llm.models import LLMRequest, LLMResponse, LLMMessage, LLMRole
from app.ai.llm.errors import LLMError, LLMTimeoutError, LLMRateLimitError, LLMConfigurationError

logger = logging.getLogger("supporthub.llm")


class LLMClient:
    """Enterprise client managing LLM invocations with retry & error handling."""

    def __init__(self, provider: Optional[LLMProvider] = None, max_retries: int = 2):
        self._provider = provider
        self.max_retries = max_retries
        self.call_history: List[Dict[str, Any]] = []

    @property
    def provider(self) -> LLMProvider:
        if self._provider is None:
            self._provider = get_llm_provider()
        return self._provider

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> LLMResponse:
        """Send a single prompt with system instruction."""
        messages = [LLMMessage(role=LLMRole.USER, content=prompt)]
        req = LLMRequest(
            messages=messages,
            temperature=temperature if temperature is not None else settings.LLM_TEMPERATURE,
            max_tokens=max_tokens or settings.LLM_MAX_TOKENS,
            system_instruction=system_instruction
        )
        return self.execute_request(req)

    def generate_chat(
        self,
        messages: List[LLMMessage],
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> LLMResponse:
        """Execute multi-turn chat generation."""
        req = LLMRequest(
            messages=messages,
            temperature=temperature if temperature is not None else settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            system_instruction=system_instruction
        )
        return self.execute_request(req)

    def execute_request(self, request: LLMRequest) -> LLMResponse:
        """Execute request with retries and exponential backoff."""
        attempt = 0
        last_error = None

        while attempt <= self.max_retries:
            try:
                start = time.time()
                response = self.provider.generate(request)
                latency = time.time() - start

                # Log call metadata safely (never log API keys or raw credentials)
                self._record_telemetry(
                    method="generate",
                    model=response.model,
                    tokens=response.usage.total_tokens,
                    latency=latency,
                    status="SUCCESS"
                )
                return response

            except (LLMTimeoutError, LLMRateLimitError) as e:
                attempt += 1
                last_error = e
                if attempt <= self.max_retries:
                    time.sleep(1.0 * (2 ** (attempt - 1)))
                else:
                    break
            except Exception as e:
                last_error = e
                break

        self._record_telemetry(
            method="generate",
            model=getattr(self.provider, "model", "unknown"),
            tokens=0,
            latency=0.0,
            status="FAILED",
            error=str(last_error)
        )
        raise LLMError(f"LLM generation failed after {attempt} retries: {last_error}")

    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate verified structured JSON."""
        attempt = 0
        last_error = None

        while attempt <= self.max_retries:
            try:
                start = time.time()
                data = self.provider.generate_structured(
                    prompt=prompt,
                    schema=schema,
                    system_instruction=system_instruction
                )
                latency = time.time() - start
                self._record_telemetry(
                    method="structured",
                    model=getattr(self.provider, "model", "unknown"),
                    tokens=0,
                    latency=latency,
                    status="SUCCESS"
                )
                return data
            except Exception as e:
                attempt += 1
                last_error = e
                if attempt <= self.max_retries:
                    time.sleep(1.0 * (2 ** (attempt - 1)))
                else:
                    break

        raise LLMError(f"LLM structured generation failed: {last_error}")

    def health_check(self) -> Dict[str, Any]:
        """Run health check against active provider."""
        return self.provider.health_check()

    def _record_telemetry(
        self,
        method: str,
        model: str,
        tokens: int,
        latency: float,
        status: str,
        error: Optional[str] = None
    ) -> None:
        """Store internal telemetry record without PII or secret keys."""
        record = {
            "timestamp": time.time(),
            "method": method,
            "provider": self.provider.provider_name,
            "model": model,
            "tokens": tokens,
            "latency_seconds": round(latency, 4),
            "status": status,
            "error": error
        }
        self.call_history.append(record)
        if len(self.call_history) > 1000:
            self.call_history.pop(0)


# Global singleton LLM client
llm_client = LLMClient()

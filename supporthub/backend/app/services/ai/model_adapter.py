"""
app/services/ai/model_adapter.py

Model-agnostic LLM interface — the Adapter Pattern.

THE CENTRAL DESIGN DECISION:
  Every LLM provider has a different Python SDK, different API format,
  different error types, and different response structures.

  Without an adapter layer, your code looks like:
    if config.provider == "openai":
        response = openai_client.chat.completions.create(...)
        text = response.choices[0].message.content
    elif config.provider == "gemini":
        response = model.generate_content(...)
        text = response.text
    elif config.provider == "claude":
        response = anthropic_client.messages.create(...)
        text = response.content[0].text

  This means: every place you call an LLM has this if/elif chain.
  Change providers → rewrite everywhere.

  WITH THE ADAPTER PATTERN:
    adapter = get_model_adapter()     # returns the configured provider
    raw = await adapter.generate(prompt)  # always same signature

  The orchestrator calls adapter.generate(). It never knows which provider
  is behind it. Switch from Gemini to Claude: change one .env variable.

RETRY STRATEGY:
  Retries belong in the adapter, not in controllers or the orchestrator.
  Each adapter knows its provider's retry-safe error codes (429, 503).
  The orchestrator just calls generate() and gets back a result or an exception.

EXTENSIBILITY FOR STREAMING:
  The generate() method signature returns a raw dict (not a stream).
  To add streaming later, add generate_stream() which yields chunks.
  The orchestrator can call generate_stream() without any changes to the
  ContextBuilder, PromptBuilder, or ResponseParser.
"""

from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

from app.services.ai.exceptions import AIProviderError, RateLimitExceeded
from app.services.ai.models import Prompt

logger = logging.getLogger(__name__)

# ─── Retry Configuration ──────────────────────────────────────────────────────

_MAX_RETRIES = 3
_RETRY_BASE_DELAY = 1.0   # seconds
_RETRY_MAX_DELAY = 8.0    # seconds


async def _exponential_backoff(attempt: int) -> None:
    """
    Wait with exponential backoff + jitter before retrying.

    WHY JITTER:
      If 100 workers all retry at exactly the same time (after 2s, 4s, 8s),
      they create a "thundering herd" that overwhelms the API again.
      Adding random jitter staggers the retries across a time window.
    """
    import random
    delay = min(_RETRY_BASE_DELAY * (2 ** attempt), _RETRY_MAX_DELAY)
    jitter = random.uniform(0, delay * 0.1)
    await asyncio.sleep(delay + jitter)


# ─── Abstract Base ────────────────────────────────────────────────────────────

class AIModelAdapter(ABC):
    """
    Abstract base class for all LLM provider adapters.

    All concrete adapters MUST implement generate().
    The orchestrator only knows about this interface — never concrete types.

    This is the Dependency Inversion Principle (the D in SOLID):
      High-level modules (Orchestrator) depend on abstractions (AIModelAdapter),
      not concrete implementations (GeminiAdapter, ClaudeAdapter).
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique identifier for this provider (e.g. 'gemini', 'claude')."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Full model name used in API calls (e.g. 'gemini-flash-lite-latest')."""
        ...

    @abstractmethod
    async def _call_provider(self, prompt: Prompt) -> dict[str, Any]:
        """
        Make the actual API call to the LLM provider.

        Returns a raw dict with at minimum:
          {
            "text": str,           # the generated text
            "input_tokens": int,
            "output_tokens": int,
            "finish_reason": str,  # "stop" | "length" | "content_filter"
          }

        Raises:
            AIProviderError: On non-retryable failures.
            RateLimitExceeded: On HTTP 429.
        """
        ...

    async def generate(self, prompt: Prompt) -> dict[str, Any]:
        """
        Generate a response with automatic retry on retryable errors.

        This is the PUBLIC interface called by the orchestrator.
        It wraps _call_provider() with retry logic.

        Returns: same dict as _call_provider()
        Raises:
            AIProviderError: After all retries exhausted.
            RateLimitExceeded: If provider is rate-limited.
        """
        last_error: Optional[Exception] = None

        for attempt in range(_MAX_RETRIES):
            try:
                start = time.monotonic()
                result = await self._call_provider(prompt)
                elapsed_ms = int((time.monotonic() - start) * 1000)
                result["latency_ms"] = elapsed_ms

                logger.info(
                    "LLM call succeeded | provider=%s | model=%s | attempt=%d | ms=%d | "
                    "in_tokens=%s | out_tokens=%s",
                    self.provider_name,
                    self.model_name,
                    attempt + 1,
                    elapsed_ms,
                    result.get("input_tokens", "?"),
                    result.get("output_tokens", "?"),
                )
                return result

            except RateLimitExceeded as exc:
                last_error = exc
                logger.warning(
                    "Rate limit hit | provider=%s | attempt=%d/%d | retry_after=%s",
                    self.provider_name,
                    attempt + 1,
                    _MAX_RETRIES,
                    exc.retry_after_seconds,
                )
                if attempt < _MAX_RETRIES - 1:
                    wait = exc.retry_after_seconds or (2 ** attempt)
                    await asyncio.sleep(min(wait, _RETRY_MAX_DELAY))
                    continue
                raise

            except AIProviderError as exc:
                last_error = exc
                if not exc.is_retryable or attempt >= _MAX_RETRIES - 1:
                    logger.error(
                        "LLM call failed (non-retryable or max retries) | "
                        "provider=%s | attempt=%d/%d | error=%s",
                        self.provider_name,
                        attempt + 1,
                        _MAX_RETRIES,
                        exc.message,
                    )
                    raise

                logger.warning(
                    "LLM call failed (retryable) | provider=%s | attempt=%d/%d | error=%s",
                    self.provider_name,
                    attempt + 1,
                    _MAX_RETRIES,
                    exc.message,
                )
                await _exponential_backoff(attempt)

        # Should not reach here, but satisfy type checker
        raise last_error or AIProviderError(self.provider_name, "Max retries exhausted")


# ─── Gemini Adapter ───────────────────────────────────────────────────────────

class GeminiAdapter(AIModelAdapter):
    """
    Adapter for Google's Gemini API (via google-generativeai SDK).

    Uses the existing Gemini setup in app/ai.py configuration.
    Reuses the same API key already configured in settings.
    """

    def __init__(self, model: str = "gemini-flash-lite-latest") -> None:
        self._model_name = model

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self._model_name

    async def _call_provider(self, prompt: Prompt) -> dict[str, Any]:
        """Call Gemini API with the assembled prompt."""
        try:
            import google.generativeai as genai
            from app.config import get_settings
            settings = get_settings()

            if settings.gemini_api_key:
                genai.configure(api_key=settings.gemini_api_key)

            # Models to attempt in order of preference
            candidate_models = [self._model_name]
            fallback_models = ["gemini-flash-lite-latest", "gemini-flash-latest", "gemini-3.5-flash-lite", "gemini-3.5-flash"]
            for m in fallback_models:
                if m not in candidate_models:
                    candidate_models.append(m)

            last_exc = None
            for model_to_use in candidate_models:
                try:
                    # Build Gemini-compatible content list (system + messages)
                    model = genai.GenerativeModel(
                        model_name=model_to_use,
                        system_instruction=prompt.system,
                        generation_config={
                            "temperature": prompt.temperature,
                            "max_output_tokens": prompt.max_tokens,
                        }
                    )

                    # Convert messages to Gemini format
                    gemini_messages = []
                    for i, msg in enumerate(prompt.messages):
                        role = "user" if msg["role"] == "user" else "model"
                        parts = [msg["content"]]
                        # Append images to the last message if available
                        if i == len(prompt.messages) - 1 and role == "user":
                            # 1. Local image files
                            if getattr(prompt, "image_paths", None):
                                import PIL.Image
                                for p in prompt.image_paths:
                                    try:
                                        img = PIL.Image.open(p)
                                        parts.append(img)
                                    except Exception as e:
                                        logger.error(f"Failed to load image {p} for Gemini: {e}")
                            # 2. Remote image URLs (Facebook/Instagram CDN)
                            if getattr(prompt, "image_urls", None):
                                import httpx as _httpx
                                import io
                                import PIL.Image
                                for img_url in prompt.image_urls:
                                    try:
                                        async with _httpx.AsyncClient(timeout=10.0) as img_client:
                                            img_resp = await img_client.get(img_url)
                                        if img_resp.status_code == 200:
                                            img = PIL.Image.open(io.BytesIO(img_resp.content))
                                            parts.append(img)
                                            logger.info("Loaded remote image for Gemini vision | url=%s", img_url[:80])
                                        else:
                                            logger.warning("Failed to fetch remote image for Gemini | status=%d | url=%s", img_resp.status_code, img_url[:80])
                                    except Exception as e:
                                        logger.error(f"Failed to load remote image {img_url[:80]} for Gemini: {e}")
                        gemini_messages.append({"role": role, "parts": parts})

                    # Make the API call
                    chat = model.start_chat(history=gemini_messages[:-1] if len(gemini_messages) > 1 else [])
                    response = await chat.send_message_async(
                        gemini_messages[-1]["parts"] if gemini_messages else ""
                    )

                    # Extract token usage (Gemini provides this in usage_metadata)
                    usage_meta = getattr(response, "usage_metadata", None)
                    input_tokens = getattr(usage_meta, "prompt_token_count", 0) or 0
                    output_tokens = getattr(usage_meta, "candidates_token_count", 0) or 0

                    # Extract finish reason
                    finish_reason = "stop"
                    if hasattr(response, "candidates") and response.candidates:
                        candidate = response.candidates[0]
                        fr = getattr(candidate, "finish_reason", None)
                        if fr:
                            fr_name = getattr(fr, "name", str(fr)).lower()
                            if "max" in fr_name or "length" in fr_name:
                                finish_reason = "length"
                            elif "safety" in fr_name or "filter" in fr_name:
                                finish_reason = "content_filter"

                    return {
                        "text": response.text,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "finish_reason": finish_reason,
                    }

                except Exception as m_exc:
                    last_exc = m_exc
                    err_text = str(m_exc).lower()
                    if "429" in err_text or "quota" in err_text or "404" in err_text or "not found" in err_text or "no longer available" in err_text:
                        logger.warning(
                            "Gemini model '%s' failed (%s) — trying fallback candidate.",
                            model_to_use,
                            m_exc,
                        )
                        continue
                    raise m_exc

            if last_exc:
                raise last_exc

            raise AIProviderError(provider="gemini", message="All candidate Gemini models failed.")

        except Exception as exc:
            error_str = str(exc).lower()
            is_rate_limit = "429" in error_str or "quota" in error_str or "rate" in error_str
            is_retryable = is_rate_limit or "500" in error_str or "503" in error_str

            if is_rate_limit:
                raise RateLimitExceeded(provider="gemini") from exc

            raise AIProviderError(
                provider="gemini",
                message=f"Gemini API call failed: {exc}",
                cause=exc,
                is_retryable=is_retryable,
            ) from exc


# ─── Claude Adapter ───────────────────────────────────────────────────────────

class ClaudeAdapter(AIModelAdapter):
    """
    Adapter for Anthropic's Claude API.

    Requires: anthropic>=0.34.0 (already in pyproject.toml)
    Requires: ANTHROPIC_API_KEY in .env
    """

    def __init__(self, model: str = "claude-haiku-4-5") -> None:
        self._model_name = model

    @property
    def provider_name(self) -> str:
        return "claude"

    @property
    def model_name(self) -> str:
        return self._model_name

    async def _call_provider(self, prompt: Prompt) -> dict[str, Any]:
        """Call Anthropic Claude API."""
        try:
            import anthropic
            from app.config import get_settings
            settings = get_settings()

            client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

            import base64
            import mimetypes
            
            claude_messages = list(prompt.messages)
            
            if getattr(prompt, "image_paths", None) and claude_messages:
                last_msg = claude_messages[-1]
                if last_msg["role"] == "user":
                    content_blocks = [{"type": "text", "text": last_msg["content"]}]
                    for p in prompt.image_paths:
                        try:
                            with open(p, "rb") as f:
                                b64_data = base64.b64encode(f.read()).decode("utf-8")
                            mime_type = mimetypes.guess_type(p)[0] or "image/jpeg"
                            content_blocks.append({
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": mime_type,
                                    "data": b64_data,
                                }
                            })
                        except Exception as e:
                            logger.error(f"Failed to load image {p} for Claude: {e}")
                    claude_messages[-1] = {"role": "user", "content": content_blocks}

            response = await client.messages.create(
                model=self._model_name,
                system=prompt.system,
                messages=claude_messages,
                temperature=prompt.temperature,
                max_tokens=prompt.max_tokens,
            )

            text = response.content[0].text if response.content else ""
            usage = response.usage

            return {
                "text": text,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "finish_reason": response.stop_reason or "stop",
            }

        except Exception as exc:
            error_str = str(exc).lower()
            is_rate_limit = "429" in str(getattr(exc, "status_code", "")) or "rate" in error_str
            is_retryable = is_rate_limit or "529" in str(getattr(exc, "status_code", ""))

            if is_rate_limit:
                raise RateLimitExceeded(provider="claude") from exc

            raise AIProviderError(
                provider="claude",
                message=f"Claude API call failed: {exc}",
                cause=exc,
                is_retryable=is_retryable,
            ) from exc


# ─── Mock Adapter (for testing) ───────────────────────────────────────────────

class MockAdapter(AIModelAdapter):
    """
    A deterministic mock adapter for unit testing.

    NEVER call real APIs in unit tests.
    This adapter returns a predictable response, making tests fast,
    free, and reproducible regardless of API availability.

    Usage in tests:
        adapter = MockAdapter(response_text="Test response from AI")
        orchestrator = AIOrchestrator(session, adapter=adapter)
    """

    def __init__(
        self,
        response_text: str = "Thank you for contacting support. How can I help you today?",
        input_tokens: int = 150,
        output_tokens: int = 30,
        finish_reason: str = "stop",
        should_raise: Exception | None = None,
    ) -> None:
        self._response_text = response_text
        self._input_tokens = input_tokens
        self._output_tokens = output_tokens
        self._finish_reason = finish_reason
        self._should_raise = should_raise

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model_name(self) -> str:
        return "mock-model-v1"

    async def _call_provider(self, prompt: Prompt) -> dict[str, Any]:
        if self._should_raise:
            raise self._should_raise
        await asyncio.sleep(0.001)  # Simulate tiny latency
        return {
            "text": self._response_text,
            "input_tokens": self._input_tokens,
            "output_tokens": self._output_tokens,
            "finish_reason": self._finish_reason,
        }


# ─── Adapter Factory ──────────────────────────────────────────────────────────

def get_model_adapter(provider: str | None = None) -> AIModelAdapter:
    """
    Factory function that returns the configured LLM adapter.

    Called once per request. Provider selected from:
      1. `provider` argument (explicit override — useful for testing)
      2. Settings (AI_PROVIDER env variable)
      3. Fallback: Gemini (cheapest, fastest for support use cases)

    Adding a new provider:
      1. Create a new class inheriting AIModelAdapter
      2. Implement provider_name, model_name, _call_provider()
      3. Add a case in the dict below
      4. Set AI_PROVIDER=yourprovider in .env

    That's it. Zero changes to the orchestrator.
    """
    from app.config import get_settings
    settings = get_settings()

    # Determine provider
    resolved_provider = (
        provider
        or getattr(settings, "ai_provider", None)
        or _auto_detect_provider(settings)
    )

    adapters: dict[str, AIModelAdapter] = {
        "gemini": GeminiAdapter(model=getattr(settings, "ai_default_model", "gemini-flash-lite-latest")),
        "claude": ClaudeAdapter(model=getattr(settings, "ai_default_model", "claude-haiku-4-5")),
        "mock": MockAdapter(),
    }

    adapter = adapters.get(resolved_provider)
    if adapter is None:
        logger.warning(
            "Unknown AI provider '%s' — falling back to Gemini.", resolved_provider
        )
        adapter = adapters["gemini"]

    logger.debug(
        "AI adapter selected | provider=%s | model=%s",
        adapter.provider_name,
        adapter.model_name,
    )
    return adapter


def _auto_detect_provider(settings) -> str:
    """
    Automatically select provider based on which API key is configured.
    Priority: Claude > Gemini (Claude is generally more capable for support).
    """
    if getattr(settings, "anthropic_api_key", ""):
        return "claude"
    if getattr(settings, "gemini_api_key", ""):
        return "gemini"
    logger.warning(
        "No LLM API key configured. Using mock adapter. "
        "Set ANTHROPIC_API_KEY or GEMINI_API_KEY in .env"
    )
    return "mock"

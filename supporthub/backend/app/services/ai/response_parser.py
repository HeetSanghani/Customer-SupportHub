"""
app/services/ai/response_parser.py

Normalizes the raw LLM provider response dict into a typed AIResponse.

SINGLE RESPONSIBILITY:
  Takes the raw dict returned by any ModelAdapter._call_provider() and
  produces a fully-typed, validated AIResponse.

  The rest of the application ONLY sees AIResponse.
  It NEVER sees raw Gemini responses, raw Anthropic responses, etc.

WHY THIS EXISTS (not just using the dict directly):
  1. The rest of your application would couple to raw dict key names.
     If Gemini changes "text" to "content" in their response, you'd fix 10 files.
     With ResponseParser, you fix ONE file.

  2. Validation: the parser ensures the response is non-empty, not a safety block,
     and within expected quality bounds. Bad responses trigger the fallback.

  3. Confidence scoring: we can heuristically score response confidence based on
     finish_reason, response length, and presence of uncertainty phrases.
     Later, this can be replaced by a dedicated classifier model.

  4. Clean data contract: AIResponse is a frozen dataclass with named fields.
     Much easier to log, serialize, and debug than a raw dict.
"""

from __future__ import annotations

import logging
from typing import Any

from app.services.ai.exceptions import ResponseParseError
from app.services.ai.models import AIResponse, ModelInfo, Prompt, TokenUsage

logger = logging.getLogger(__name__)

# Phrases that indicate the AI is uncertain — lower confidence score
_UNCERTAINTY_PHRASES = [
    "i don't know",
    "i'm not sure",
    "i cannot",
    "i can't",
    "i don't have",
    "not able to",
    "unable to",
    "please contact",
    "human agent",
    "i don't have enough information",
]

# Safety block finish reasons
_SAFETY_FINISH_REASONS = {"content_filter", "safety", "blocked"}

# Minimum response length to be considered valid (in characters)
_MIN_RESPONSE_LENGTH = 10

# Fallback message when AI fails or returns invalid response
_FALLBACK_RESPONSE = (
    "Thank you for reaching out! Our support team has received your message "
    "and will get back to you shortly."
)


class ResponseParser:
    """
    Parses and validates raw LLM provider responses into AIResponse objects.

    Usage:
        parser = ResponseParser()
        ai_response = parser.parse(
            raw_response={"text": "...", "input_tokens": 150, ...},
            prompt=prompt,
            provider="gemini",
            model_name="gemini-flash-lite-latest",
        )
    """

    def parse(
        self,
        raw_response: dict[str, Any],
        prompt: Prompt,
        provider: str,
        model_name: str,
        latency_ms: int = 0,
    ) -> AIResponse:
        """
        Parse and validate a raw provider response dict into AIResponse.

        Args:
            raw_response: The dict returned by ModelAdapter._call_provider().
            prompt: The Prompt used to generate this response (for versioning).
            provider: Provider name ("gemini", "claude", "mock").
            model_name: Full model name.
            latency_ms: Wall-clock time of the API call.

        Returns:
            AIResponse — fully normalized and validated.

        Raises:
            ResponseParseError: Only on truly unexpected errors. Normal failures
                                (empty text, safety block) return a fallback AIResponse.
        """
        try:
            model_info = ModelInfo(
                provider=provider,
                model_name=model_name,
                prompt_version=prompt.version,
                system_hash=prompt.system_hash,
                temperature=prompt.temperature,
                max_tokens=prompt.max_tokens,
            )

            usage = TokenUsage(
                input_tokens=raw_response.get("input_tokens", 0),
                output_tokens=raw_response.get("output_tokens", 0),
                total_tokens=(
                    raw_response.get("input_tokens", 0)
                    + raw_response.get("output_tokens", 0)
                ),
            )

            finish_reason = raw_response.get("finish_reason", "stop")
            raw_text = (raw_response.get("text") or "").strip()

            # ── Validate and potentially fallback ────────────────────────────
            response_text, error = self._validate_response(
                text=raw_text,
                finish_reason=finish_reason,
                provider=provider,
            )

            # ── Score confidence ─────────────────────────────────────────────
            confidence = self._score_confidence(
                text=response_text,
                finish_reason=finish_reason,
                is_fallback=error is not None,
            )

            return AIResponse(
                response_text=response_text,
                model=model_info,
                usage=usage,
                finish_reason=finish_reason,
                latency_ms=latency_ms,
                confidence=confidence,
                error=error,
            )

        except (ResponseParseError, KeyError, TypeError, ValueError):
            raise
        except Exception as exc:
            raise ResponseParseError(
                provider=provider,
                reason=f"Unexpected parse error: {exc}",
                raw_response=str(raw_response),
            ) from exc

    # ─── Private Helpers ─────────────────────────────────────────────────────

    def _validate_response(
        self,
        text: str,
        finish_reason: str,
        provider: str,
    ) -> tuple[str, str | None]:
        """
        Validate the response text. Returns (text_to_use, error_or_None).

        Rules:
          - Empty text → fallback
          - Safety block → fallback (log it)
          - Too short → fallback
          - Truncated (finish_reason=length) → use as-is, but log warning
        """
        # Safety block
        if finish_reason in _SAFETY_FINISH_REASONS:
            logger.warning(
                "LLM response blocked by safety filters | provider=%s | finish_reason=%s",
                provider,
                finish_reason,
            )
            return _FALLBACK_RESPONSE, f"safety_block:{finish_reason}"

        # Empty response
        if not text:
            logger.warning("LLM returned empty response | provider=%s", provider)
            return _FALLBACK_RESPONSE, "empty_response"

        # Too short to be useful
        if len(text) < _MIN_RESPONSE_LENGTH:
            logger.warning(
                "LLM response too short (%d chars) | provider=%s | text=%r",
                len(text),
                provider,
                text,
            )
            return _FALLBACK_RESPONSE, f"response_too_short:{len(text)}_chars"

        # Truncated (not necessarily an error, but worth logging)
        if finish_reason == "length":
            logger.warning(
                "LLM response truncated by token limit | provider=%s | text_len=%d",
                provider,
                len(text),
            )

        return text, None

    def _score_confidence(
        self,
        text: str,
        finish_reason: str,
        is_fallback: bool,
    ) -> float:
        """
        Heuristic confidence score between 0.0 and 1.0.

        Scoring rules:
          - Fallback response → 0.0 (AI failed)
          - Safety block / truncated → 0.3
          - Contains uncertainty phrases → 0.6
          - Clean, normal response → 1.0

        In production, replace this with a dedicated classifier model that
        scores responses against KB articles and factual accuracy criteria.
        """
        if is_fallback:
            return 0.0

        if finish_reason in _SAFETY_FINISH_REASONS:
            return 0.3

        if finish_reason == "length":
            return 0.5

        text_lower = text.lower()
        uncertainty_count = sum(
            1 for phrase in _UNCERTAINTY_PHRASES if phrase in text_lower
        )

        if uncertainty_count >= 2:
            return 0.5
        elif uncertainty_count == 1:
            return 0.7

        return 1.0

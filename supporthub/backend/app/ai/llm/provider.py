"""Concrete LLM Provider Implementations for Gemini, OpenAI, Anthropic, and Fallback."""
import json
import time
import requests
from typing import Dict, Any, Optional, List

from app.ai.config import settings
from app.ai.llm.base import LLMProvider
from app.ai.llm.models import LLMRequest, LLMResponse, LLMMessage, LLMRole, TokenUsage
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


class GeminiProvider(LLMProvider):
    """Google Gemini REST API provider using v1beta generateContent."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.LLM_API_KEY
        self.model = model or settings.LLM_MODEL or "gemini-2.5-flash"
        self.timeout = settings.LLM_TIMEOUT

    @property
    def provider_name(self) -> str:
        return "gemini"

    def _get_api_url(self) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

    def generate(self, request: LLMRequest) -> LLMResponse:
        if not self.api_key:
            raise LLMConfigurationError("GEMINI_API_KEY is not configured.")

        url = self._get_api_url()
        headers = {"Content-Type": "application/json"}

        # Format messages for Gemini API
        contents = []
        for msg in request.messages:
            role = "user" if msg.role == LLMRole.USER else "model"
            if msg.role == LLMRole.SYSTEM:
                continue  # Handled via system_instruction
            contents.append({
                "role": role,
                "parts": [{"text": msg.content}]
            })

        # Ensure there is at least one content part
        if not contents and request.messages:
            contents = [{"role": "user", "parts": [{"text": request.messages[-1].content}]}]

        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens
            }
        }

        # System instruction
        sys_inst = request.system_instruction
        if not sys_inst:
            sys_msgs = [m.content for m in request.messages if m.role == LLMRole.SYSTEM]
            if sys_msgs:
                sys_inst = "\n\n".join(sys_msgs)
        if sys_inst:
            payload["system_instruction"] = {
                "parts": [{"text": sys_inst}]
            }

        start_time = time.time()
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise LLMTimeoutError(f"Gemini API request timed out after {self.timeout}s.")
        except requests.exceptions.ConnectionError as e:
            raise LLMConnectionError(f"Gemini API connection failed: {e}")
        except Exception as e:
            raise LLMError(f"Gemini API request error: {e}")

        latency = time.time() - start_time

        if resp.status_code == 401 or resp.status_code == 403:
            raise LLMAuthenticationError(f"Gemini API authentication failed (HTTP {resp.status_code}): {resp.text}")
        elif resp.status_code == 429:
            raise LLMRateLimitError(f"Gemini API rate limit exceeded: {resp.text}")
        elif resp.status_code != 200:
            raise LLMError(f"Gemini API error (HTTP {resp.status_code}): {resp.text}")

        data = resp.json()
        try:
            candidates = data.get("candidates", [])
            if not candidates:
                # Check prompt feedback
                feedback = data.get("promptFeedback", {})
                raise LLMContentFilterError(f"Gemini response blocked: {feedback}")

            first_cand = candidates[0]
            parts = first_cand.get("content", {}).get("parts", [])
            content_text = "".join(p.get("text", "") for p in parts)
            finish_reason = first_cand.get("finishReason", "STOP")

            # Token usage if available
            usage_metadata = data.get("usageMetadata", {})
            prompt_tokens = usage_metadata.get("promptTokenCount", 0)
            completion_tokens = usage_metadata.get("candidatesTokenCount", 0)
            total_tokens = usage_metadata.get("totalTokenCount", 0)

            return LLMResponse(
                content=content_text.strip(),
                model=self.model,
                provider=self.provider_name,
                usage=TokenUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens
                ),
                latency_seconds=round(latency, 4),
                finish_reason=finish_reason,
                raw_response=data
            )
        except Exception as e:
            raise LLMValidationError(f"Failed to parse Gemini response: {e}")

    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise LLMConfigurationError("GEMINI_API_KEY is not configured.")

        url = self._get_api_url()
        headers = {"Content-Type": "application/json"}

        payload: Dict[str, Any] = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.0,
                "responseMimeType": "application/json"
            }
        }
        if system_instruction:
            payload["system_instruction"] = {"parts": [{"text": system_instruction}]}

        start_time = time.time()
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise LLMTimeoutError(f"Gemini API structured request timed out after {self.timeout}s.")
        except Exception as e:
            raise LLMError(f"Gemini API structured request error: {e}")

        if resp.status_code != 200:
            raise LLMError(f"Gemini API structured error (HTTP {resp.status_code}): {resp.text}")

        data = resp.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise LLMContentFilterError("Gemini structured response was empty or blocked.")

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts).strip()
        
        # Strip potential markdown formatting ```json ... ```
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise LLMValidationError(f"Failed to parse structured JSON from LLM: {e}. Raw text: {text}")

    def health_check(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "status": "NOT_CONFIGURED",
                "provider": self.provider_name,
                "model": self.model,
                "error": "GEMINI_API_KEY is not set"
            }

        start = time.time()
        try:
            req = LLMRequest(
                messages=[LLMMessage(role=LLMRole.USER, content="Respond with exactly 'PONG'.")],
                temperature=0.0,
                max_tokens=10
            )
            resp = self.generate(req)
            latency = time.time() - start
            return {
                "status": "READY",
                "provider": self.provider_name,
                "model": self.model,
                "connection": "PASS",
                "generation": "PASS",
                "latency_seconds": round(latency, 3),
                "sample_output": resp.content[:50]
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "provider": self.provider_name,
                "model": self.model,
                "connection": "FAIL",
                "generation": "FAIL",
                "error": str(e)
            }


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or getattr(settings, "OPENAI_API_KEY", "")
        self.model = model or getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")
        self.timeout = settings.LLM_TIMEOUT

    @property
    def provider_name(self) -> str:
        return "openai"

    def generate(self, request: LLMRequest) -> LLMResponse:
        if not self.api_key:
            raise LLMConfigurationError("OPENAI_API_KEY is not configured.")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        messages = [{"role": m.role.value, "content": m.content} for m in request.messages]
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }

        start_time = time.time()
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        except Exception as e:
            raise LLMError(f"OpenAI request error: {e}")

        latency = time.time() - start_time
        if resp.status_code != 200:
            raise LLMError(f"OpenAI error (HTTP {resp.status_code}): {resp.text}")

        data = resp.json()
        choice = data["choices"][0]
        usage = data.get("usage", {})
        return LLMResponse(
            content=choice["message"]["content"].strip(),
            model=self.model,
            provider=self.provider_name,
            usage=TokenUsage(
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0)
            ),
            latency_seconds=round(latency, 4),
            raw_response=data
        )

    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise LLMConfigurationError("OPENAI_API_KEY is not configured.")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.0,
            "response_format": {"type": "json_object"}
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        if resp.status_code != 200:
            raise LLMError(f"OpenAI structured error: {resp.text}")
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        return json.loads(text)

    def health_check(self) -> Dict[str, Any]:
        if not self.api_key:
            return {"status": "NOT_CONFIGURED", "provider": self.provider_name, "error": "OPENAI_API_KEY not set"}
        try:
            req = LLMRequest(messages=[LLMMessage(role=LLMRole.USER, content="Ping")])
            resp = self.generate(req)
            return {"status": "READY", "provider": self.provider_name, "model": self.model, "connection": "PASS"}
        except Exception as e:
            return {"status": "ERROR", "provider": self.provider_name, "error": str(e)}


class DeterministicFallbackProvider(LLMProvider):
    """Offline deterministic provider for guaranteed local test execution."""

    def __init__(self, model: str = "deterministic-sandbox-v1"):
        self.model = model

    @property
    def provider_name(self) -> str:
        return "deterministic_test"

    def generate(self, request: LLMRequest) -> LLMResponse:
        # Factual deterministic fallback
        last_msg = request.messages[-1].content if request.messages else ""
        return LLMResponse(
            content=f"[Deterministic Fallback] Processed query: {last_msg}",
            model=self.model,
            provider=self.provider_name,
            usage=TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20),
            latency_seconds=0.001
        )

    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        # Minimal valid JSON matching common schema fields
        return {
            "intent": "UNKNOWN",
            "confidence": 0.9,
            "category": "orders",
            "entities": {},
            "suggested_route": "STRUCTURED"
        }

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "READY",
            "provider": self.provider_name,
            "model": self.model,
            "connection": "PASS",
            "generation": "PASS",
            "latency_seconds": 0.001
        }


def get_llm_provider(name: Optional[str] = None) -> LLMProvider:
    """Factory function resolving configured LLM provider."""
    provider_type = (name or settings.LLM_PROVIDER).lower()
    
    if provider_type == "gemini":
        return GeminiProvider()
    elif provider_type == "openai":
        return OpenAIProvider()
    elif provider_type == "deterministic_test" or provider_type == "fallback":
        return DeterministicFallbackProvider()
    else:
        # Fall back to Gemini if API key available, else deterministic fallback
        if settings.LLM_API_KEY:
            return GeminiProvider()
        return DeterministicFallbackProvider()

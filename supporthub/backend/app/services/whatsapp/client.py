"""
app/services/whatsapp/client.py

Low-Level HTTP API Client for Meta's WhatsApp Cloud API.

THE SINGLE RESPONSIBILITY RULE:
  This is the ONLY file in the entire application allowed to execute direct
  HTTP POST requests to Meta Graph API endpoints.

  It has ZERO business logic:
    - It doesn't know about tickets, conversations, or AI.
    - It doesn't format text or build prompts.
    - It takes a validated Meta JSON dict, sends it over HTTP, and parses the outcome.

META API ENDPOINT STRUCTURE:
  POST https://graph.facebook.com/{META_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages
  Headers:
    Authorization: Bearer {WHATSAPP_ACCESS_TOKEN}
    Content-Type: application/json

SUCCESSFUL RESPONSE FROM META (HTTP 200/201):
  {
    "messaging_product": "whatsapp",
    "contacts": [{"input": "919876543210", "wa_id": "919876543210"}],
    "messages": [{"id": "wamid.HBgLOTE5ODc2NTQzMjEwFQIAERgSQURBMDM3ODU2RTA1MzA3QzUA"}]
  }

ERROR RESPONSE FROM META (HTTP 4xx / 5xx):
  {
    "error": {
      "message": "(#131030) Recipient phone number not in allowed list",
      "type": "OAuthException",
      "code": 131030,
      "error_data": {"messaging_product": "whatsapp", "details": "..."},
      "fbtrace_id": "A1b2C3d4E5f6"
    }
  }
"""

from __future__ import annotations

import logging
import time
from typing import Any, Optional

import httpx

from app.config import get_settings
from app.services.whatsapp.exceptions import (
    AuthenticationError,
    RateLimitError,
    WhatsAppProviderError,
)
from app.services.whatsapp.models import ProviderResponse

logger = logging.getLogger(__name__)

DEFAULT_META_VERSION = "v20.0"
DEFAULT_TIMEOUT_SECONDS = 10.0


class MetaWhatsAppClient:
    """
    HTTP client wrapper for Meta WhatsApp Cloud API.

    Usage:
        client = MetaWhatsAppClient()
        response = await client.send_payload(payload)
    """

    def __init__(
        self,
        phone_number_id: Optional[str] = None,
        access_token: Optional[str] = None,
        api_version: str = DEFAULT_META_VERSION,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        import os
        from dotenv import load_dotenv
        load_dotenv(override=True)

        settings = get_settings()
        self.phone_number_id = (
            phone_number_id
            or os.environ.get("WHATSAPP_PHONE_ID")
            or getattr(settings, "whatsapp_phone_id", "")
            or getattr(settings, "whatsapp_phone_number_id", "")
        )
        self.access_token = (
            access_token
            or os.environ.get("WHATSAPP_ACCESS_TOKEN")
            or getattr(settings, "whatsapp_access_token", "")
            or getattr(settings, "meta_app_token", "")
            or getattr(settings, "page_access_token", "")
        )
        self.api_version = api_version
        self.timeout = timeout
        self._external_client = client

    @property
    def base_url(self) -> str:
        return f"https://graph.facebook.com/{self.api_version}"

    @property
    def messages_endpoint(self) -> str:
        return f"{self.base_url}/{self.phone_number_id}/messages"

    async def send_payload(self, payload: dict[str, Any]) -> ProviderResponse:
        """
        Execute an HTTP POST to Meta's `/messages` endpoint.

        Args:
            payload: Pre-formatted Meta JSON payload from `WhatsAppPayloadFormatter`.

        Returns:
            ProviderResponse containing `provider_message_id` (wamid) and latency.

        Raises:
            AuthenticationError: On HTTP 401/403.
            RateLimitError: On HTTP 429.
            WhatsAppProviderError: On HTTP 400 / 500 / other errors.
        """
        if not self.phone_number_id:
            raise AuthenticationError(
                message="WHATSAPP_PHONE_ID is not configured in settings or environment."
            )

        if not self.access_token:
            raise AuthenticationError(
                message="WHATSAPP_ACCESS_TOKEN is not configured in settings or environment."
            )

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        start_time = time.monotonic()

        try:
            if self._external_client:
                res = await self._external_client.post(
                    self.messages_endpoint,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout,
                )
            else:
                async with httpx.AsyncClient(timeout=self.timeout) as http_client:
                    res = await http_client.post(
                        self.messages_endpoint,
                        json=payload,
                        headers=headers,
                    )

            latency_ms = int((time.monotonic() - start_time) * 1000)

            # Handle HTTP & Meta-level errors
            return self._parse_http_response(res, latency_ms)

        except (AuthenticationError, RateLimitError, WhatsAppProviderError):
            raise

        except httpx.TimeoutException as exc:
            logger.warning("Meta API request timed out after %.1fs", self.timeout)
            raise WhatsAppProviderError(
                message=f"Meta API call timed out ({self.timeout}s)",
                status_code=504,
                is_retryable=True,
                cause=exc,
            ) from exc

        except httpx.RequestError as exc:
            logger.error("Meta HTTP network connection error: %s", exc)
            raise WhatsAppProviderError(
                message=f"Network error connecting to Meta API: {exc}",
                status_code=503,
                is_retryable=True,
                cause=exc,
            ) from exc

    # ─── Response Parsing & Error Mapping ─────────────────────────────────────

    def _parse_http_response(
        self,
        res: httpx.Response,
        latency_ms: int,
    ) -> ProviderResponse:
        """
        Parse httpx response and map status codes/subcodes to domain objects or exceptions.
        """
        try:
            data = res.json()
        except Exception:
            data = {"raw": res.text}

        status_code = res.status_code

        # ── SUCCESS (200 / 201) ───────────────────────────────────────────────
        if status_code in (200, 201):
            messages = data.get("messages", [])
            wamid = messages[0].get("id") if messages else None

            logger.info(
                "✅ Meta message sent successfully | wamid=%s | latency=%dms",
                wamid,
                latency_ms,
            )

            return ProviderResponse(
                success=True,
                provider_message_id=wamid,
                status_code=status_code,
                raw_response=data,
            )

        # ── ERROR HANDLING ───────────────────────────────────────────────────
        error_info = data.get("error", {})
        error_message = error_info.get("message", res.text)
        error_code = error_info.get("code")
        error_subcode = error_info.get("error_subcode")

        logger.error(
            "❌ Meta API error | status=%d | code=%s | subcode=%s | msg=%s",
            status_code,
            error_code,
            error_subcode,
            error_message,
        )

        # 1. Auth failure (401, 403, or Meta OAuth code 190)
        if status_code in (401, 403) or error_code in (190, 102):
            raise AuthenticationError(
                message=f"Meta authentication error: {error_message}",
                status_code=status_code,
                error_code=error_code,
                raw_error=data,
            )

        # 2. Rate limits (429 or Meta rate limit subcodes 130429, 80007)
        if status_code == 429 or error_code in (130429, 80007):
            raise RateLimitError(
                message=f"Meta rate limit hit: {error_message}",
                status_code=429,
                error_code=error_code,
                raw_error=data,
            )

        # 3. Transient server errors (500, 502, 503, 504)
        is_retryable = status_code in (500, 502, 503, 504)

        raise WhatsAppProviderError(
            message=error_message,
            status_code=status_code,
            error_code=error_code,
            error_subcode=error_subcode,
            is_retryable=is_retryable,
            raw_error=data,
        )

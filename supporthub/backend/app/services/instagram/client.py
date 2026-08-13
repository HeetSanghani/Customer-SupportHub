"""
app/services/instagram/client.py

Low-Level Async HTTP API Client for Meta's Instagram Graph API.

THE SINGLE RESPONSIBILITY RULE:
  This file is responsible ONLY for direct HTTP requests to Meta's Instagram Graph API
  (https://graph.instagram.com).
  It has ZERO database or frontend coupling.

META INSTAGRAM API ENDPOINT STRUCTURE:
  POST https://graph.instagram.com/{api_version}/me/messages
  Headers:
    Authorization: Bearer {INSTAGRAM_ACCESS_TOKEN}
    Content-Type: application/json

SUCCESSFUL RESPONSE FROM META (HTTP 200/201):
  {
    "recipient_id": "17841400000000000",
    "message_id": "aWdfbWVzc2FnZV9pZDoxNzg0MTQwMDAwMDAwMDAwMA=="
  }

ERROR RESPONSE FROM META (HTTP 4xx / 5xx):
  {
    "error": {
      "message": "(#100) Param recipient[id] must be a valid IGSID",
      "type": "OAuthException",
      "code": 100,
      "error_subcode": 2534015,
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
    FormattingError,
    RateLimitError,
    WhatsAppProviderError as InstagramProviderError,
)
from app.services.whatsapp.models import ProviderResponse

logger = logging.getLogger(__name__)

DEFAULT_INSTAGRAM_HOST = "https://graph.instagram.com"
DEFAULT_META_VERSION = "v19.0"
DEFAULT_TIMEOUT_SECONDS = 10.0
MAX_TEXT_LENGTH = 1000  # Instagram DM text length limit


class MetaInstagramClient:
    """
    HTTP client wrapper for Meta Instagram Graph API (Instagram Login flow).

    Usage:
        client = MetaInstagramClient()
        response = await client.send_text_message(recipient_igsid="1784...", text="Hello!")
    """

    def __init__(
        self,
        access_token: Optional[str] = None,
        account_id: Optional[str] = None,
        api_version: str = DEFAULT_META_VERSION,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        settings = get_settings()
        self.access_token = (
            access_token
            if access_token is not None
            else getattr(settings, "instagram_access_token", "")
        )
        self.account_id = (
            account_id
            if account_id is not None
            else getattr(settings, "instagram_account_id", "")
        )
        self.api_version = api_version
        self.timeout = timeout
        self._external_client = client

    @property
    def base_url(self) -> str:
        return f"{DEFAULT_INSTAGRAM_HOST}/{self.api_version}"

    @property
    def messages_endpoint(self) -> str:
        return f"{self.base_url}/me/messages"

    def _redact_token_from_string(self, text: str) -> str:
        """Helper to ensure tokens are never leaked in exception details or logs."""
        if self.access_token and self.access_token in text:
            return text.replace(self.access_token, "[REDACTED_INSTAGRAM_TOKEN]")
        return text

    async def send_text_message(
        self,
        recipient_igsid: str,
        text: str,
    ) -> ProviderResponse:
        """
        Send an outbound text DM to an Instagram user.

        Args:
            recipient_igsid: Instagram-scoped user ID (from incoming webhook).
            text: Message body text (max 1000 characters).

        Returns:
            ProviderResponse containing provider_message_id and status_code.

        Raises:
            FormattingError: If recipient_igsid or text is empty or invalid.
            AuthenticationError: On HTTP 401/403 or invalid token.
            RateLimitError: On HTTP 429.
            InstagramProviderError: On HTTP 400 / 500 / other errors.
        """
        # 1. Validation
        if not recipient_igsid or not recipient_igsid.strip():
            raise FormattingError("recipient_igsid must not be empty.")

        if not text or not text.strip():
            raise FormattingError("Message text must not be empty.")

        if len(text) > MAX_TEXT_LENGTH:
            raise FormattingError(
                f"Message text exceeds Instagram maximum length of {MAX_TEXT_LENGTH} characters (got {len(text)})."
            )

        if not self.access_token:
            raise AuthenticationError(
                message="INSTAGRAM_ACCESS_TOKEN is not configured in settings or passed explicitly.",
                status_code=401,
            )

        # 2. Build Request
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "recipient": {"id": recipient_igsid.strip()},
            "message": {"text": text},
        }

        start_time = time.monotonic()

        # 3. Execute HTTP Call
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
            return self._parse_http_response(res, latency_ms)

        except (AuthenticationError, RateLimitError, InstagramProviderError, FormattingError):
            raise

        except httpx.TimeoutException as exc:
            logger.warning("Instagram API request timed out after %.1fs", self.timeout)
            raise InstagramProviderError(
                message=f"Instagram API call timed out ({self.timeout}s)",
                status_code=504,
                is_retryable=True,
                cause=exc,
            ) from exc

        except httpx.RequestError as exc:
            clean_err = self._redact_token_from_string(str(exc))
            logger.error("Instagram HTTP network connection error: %s", clean_err)
            raise InstagramProviderError(
                message=f"Network error connecting to Instagram API: {clean_err}",
                status_code=503,
                is_retryable=True,
                cause=exc,
            ) from exc

    def _parse_http_response(
        self,
        res: httpx.Response,
        latency_ms: int,
    ) -> ProviderResponse:
        """Parse httpx response and map status codes to ProviderResponse or domain exceptions."""
        try:
            data = res.json()
        except Exception:
            data = {"raw": res.text}

        status_code = res.status_code

        # ── SUCCESS (200 / 201) ───────────────────────────────────────────────
        if status_code in (200, 201):
            msg_id = data.get("message_id")
            recip_id = data.get("recipient_id")

            logger.info(
                "✅ Instagram message sent successfully | message_id=%s | recipient=%s | latency=%dms",
                msg_id,
                recip_id,
                latency_ms,
            )

            return ProviderResponse(
                success=True,
                provider_message_id=msg_id,
                status_code=status_code,
                raw_response=data,
            )

        # ── ERROR HANDLING ───────────────────────────────────────────────────
        error_info = data.get("error", {})
        error_message = self._redact_token_from_string(error_info.get("message", res.text))
        error_code = error_info.get("code")
        error_subcode = error_info.get("error_subcode")

        logger.error(
            "❌ Instagram API error | status=%d | code=%s | subcode=%s | msg=%s",
            status_code,
            error_code,
            error_subcode,
            error_message,
        )

        # 1. Auth failure (401, 403, or Meta OAuth code 190 / 102)
        if status_code in (401, 403) or error_code in (190, 102):
            raise AuthenticationError(
                message=f"Instagram authentication error: {error_message}",
                status_code=status_code,
                error_code=error_code,
                raw_error=data,
            )

        # 2. Rate limits (429 or Meta rate limit subcodes 130429, 80007)
        if status_code == 429 or error_code in (130429, 80007):
            raise RateLimitError(
                message=f"Instagram rate limit hit: {error_message}",
                status_code=429,
                error_code=error_code,
                raw_error=data,
            )

        # 3. Client / Provider errors
        is_retryable = status_code in (500, 502, 503, 504)

        raise InstagramProviderError(
            message=error_message,
            status_code=status_code,
            error_code=error_code,
            error_subcode=error_subcode,
            is_retryable=is_retryable,
            raw_error=data,
        )

    async def get_user_profile(
        self,
        user_igsid: str,
    ) -> dict[str, Any]:
        """
        Fetch Instagram user profile (name, username, profile_pic) using the IGSID.

        Meta Instagram Graph API Endpoint:
            GET https://graph.instagram.com/v19.0/{user_igsid}?fields=name,username,profile_pic

        Returns dict with keys:
            - id: str
            - name: Optional[str] (e.g. "Heet Sanghani")
            - username: Optional[str] (e.g. "_heet_patel_3108")
            - profile_pic: Optional[str] (URL to user avatar)
        """
        if not user_igsid or not str(user_igsid).strip():
            return {}

        if not self.access_token:
            logger.warning("Cannot fetch Instagram profile: INSTAGRAM_ACCESS_TOKEN is not configured.")
            return {}

        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        params = {
            "fields": "id,name,username,profile_pic"
        }
        clean_id = str(user_igsid).strip()
        url = f"{self.base_url}/{clean_id}"

        try:
            if self._external_client:
                res = await self._external_client.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=self.timeout,
                )
            else:
                async with httpx.AsyncClient(timeout=self.timeout) as http_client:
                    res = await http_client.get(
                        url,
                        headers=headers,
                        params=params,
                    )

            if res.status_code in (200, 201):
                data = res.json()
                logger.info(
                    "✅ Fetched Instagram user profile for %s: name=%r, username=%r",
                    clean_id,
                    data.get("name"),
                    data.get("username"),
                )
                return data
            else:
                logger.warning(
                    "Failed to fetch Instagram profile for %s (HTTP %d): %s",
                    clean_id,
                    res.status_code,
                    self._redact_token_from_string(res.text),
                )
                return {}
        except Exception as exc:
            logger.warning("Error fetching Instagram profile for %s: %s", clean_id, exc)
            return {}


"""
app/services/whatsapp/auth.py

Security layer for Meta WhatsApp Cloud API webhook authentication.

Responsibilities:
  1. Verify Token validation  — proves the GET handshake came from Meta.
  2. HMAC-SHA256 Signature    — proves each POST payload came from Meta
                                and was not tampered with in transit.

WHY TWO SEPARATE CHECKS?
  - Verify Token is used ONCE at webhook registration time (GET).
  - Signature is used on EVERY incoming message (POST).
  - They serve different threat models:
      * Verify Token  → prevents someone from "claiming" your webhook URL.
      * HMAC Signature → prevents someone from sending fake messages
                         to your endpoint, or replaying captured payloads.

PRODUCTION NOTE:
  Always use hmac.compare_digest() for ALL secret comparisons.
  Python's == operator short-circuits, enabling timing attacks.
  hmac.compare_digest() runs in constant time regardless of input.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
from typing import Optional

from fastapi import Header, HTTPException, Request, status

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


# ──────────────────────────────────────────────────────────────────────────────
# Verify Token Validation
# ──────────────────────────────────────────────────────────────────────────────

def validate_verify_token(
    hub_mode: Optional[str],
    hub_verify_token: Optional[str],
) -> bool:
    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)
    expected_token: str = (
        os.environ.get("WHATSAPP_VERIFY_TOKEN")
        or os.environ.get("META_VERIFY_TOKEN")
        or getattr(settings, "whatsapp_verify_token", "")
        or getattr(settings, "meta_verify_token", "")
    )

    if not expected_token:
        logger.critical(
            "META_VERIFY_TOKEN is not set in environment variables. "
            "All webhook verification requests will be rejected."
        )
        return False

    if hub_mode != "subscribe":
        logger.warning(
            "Webhook verification failed: hub.mode='%s' (expected 'subscribe')",
            hub_mode,
        )
        return False

    if not hub_verify_token:
        logger.warning("Webhook verification failed: hub.verify_token is missing.")
        return False

    token_valid = hmac.compare_digest(
        hub_verify_token.encode("utf-8"),
        expected_token.encode("utf-8"),
    )

    if not token_valid:
        logger.warning(
            "Webhook verification failed: verify_token mismatch. "
            "Received='%s...', Expected='%s...'",
            hub_verify_token[:4],
            expected_token[:4],
        )
        return False

    return True


# ──────────────────────────────────────────────────────────────────────────────
# HMAC Signature Verification
# ──────────────────────────────────────────────────────────────────────────────

async def verify_whatsapp_signature(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(
        default=None,
        alias="X-Hub-Signature-256",
    ),
) -> bytes:

    raw_body: bytes = await request.body()

    # =========================================================================
    # DEBUG (temporary)
    # =========================================================================
    print("\n" + "=" * 100)
    print("INCOMING WHATSAPP WEBHOOK")
    print("=" * 100)

    print("\nHEADERS:")
    for key, value in request.headers.items():
        print(f"{key}: {value}")

    print("\nRAW BODY:")
    try:
        print(raw_body.decode("utf-8"))
    except Exception:
        print(raw_body)

    print("\nENV VALUES:")
    print("META_APP_SECRET :", repr(settings.meta_app_secret))
    print("BODY LENGTH     :", len(raw_body))
    print("HEADER SIGNATURE:", x_hub_signature_256)

    print("=" * 100 + "\n")
    # =========================================================================

    import os
    from dotenv import load_dotenv
    load_dotenv(override=True)
    app_secret: str = os.environ.get("META_APP_SECRET") or getattr(settings, "meta_app_secret", "")

    if not app_secret:
        if settings.is_production:
            logger.critical(
                "META_APP_SECRET is not set in production! "
                "Rejecting all incoming WhatsApp webhooks."
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Webhook signature verification is not configured.",
            )

        logger.warning(
            "META_APP_SECRET not configured — skipping signature check "
            "(development mode only)."
        )
        return raw_body

    if not x_hub_signature_256:
        logger.warning(
            "WhatsApp webhook POST missing X-Hub-Signature-256 header."
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing webhook signature.",
        )

    if not x_hub_signature_256.startswith("sha256="):
        logger.warning(
            "Malformed X-Hub-Signature-256 header: %s",
            x_hub_signature_256,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Malformed webhook signature.",
        )

    received_signature = x_hub_signature_256.removeprefix("sha256=")

    computed_signature = hmac.new(
        key=app_secret.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256,
    ).hexdigest()

    print("COMPUTED SIGNATURE :", computed_signature)
    print("RECEIVED SIGNATURE :", received_signature)

    if not hmac.compare_digest(received_signature, computed_signature):
        logger.warning(
            "WhatsApp webhook signature mismatch — request body may have "
            "been tampered with or did not originate from Meta."
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid webhook signature.",
        )

    logger.info("WhatsApp webhook signature verified successfully.")

    return raw_body
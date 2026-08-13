"""
app/services/instagram/auth.py

Security layer for Instagram Webhook authentication.
Uses INSTAGRAM_APP_SECRET (falling back to META_APP_SECRET if not set) for HMAC-SHA256 signature verification.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
from typing import Optional

from fastapi import Header, HTTPException, Request, status
from dotenv import load_dotenv

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def verify_instagram_signature(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(
        default=None,
        alias="X-Hub-Signature-256",
    ),
) -> bytes:
    """
    Validates the X-Hub-Signature-256 header sent by Meta Instagram webhooks.
    Computes HMAC-SHA256 over raw request body bytes using INSTAGRAM_APP_SECRET or META_APP_SECRET.
    Returns raw request bytes if valid; raises HTTP 403 if invalid or missing.
    """
    raw_body: bytes = await request.body()

    load_dotenv(override=True)
    app_secret: str = (
        getattr(settings, "instagram_app_secret", "")
        or os.environ.get("INSTAGRAM_APP_SECRET", "")
        or getattr(settings, "meta_app_secret", "")
        or os.environ.get("META_APP_SECRET", "")
    )

    if not app_secret:
        if settings.is_production:
            logger.critical("INSTAGRAM_APP_SECRET / META_APP_SECRET is not configured in production!")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Instagram webhook signature verification is not configured.",
            )

        logger.warning("No Instagram app secret configured — skipping signature check (development mode only).")
        return raw_body

    if not x_hub_signature_256:
        logger.warning("Instagram webhook POST missing X-Hub-Signature-256 header.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing webhook signature.",
        )

    if not x_hub_signature_256.startswith("sha256="):
        logger.warning("Malformed X-Hub-Signature-256 header format.")
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

    if not hmac.compare_digest(received_signature, computed_signature):
        logger.warning("Instagram webhook signature mismatch — invalid HMAC digest.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid webhook signature.",
        )

    logger.info("Instagram webhook signature verified successfully.")
    return raw_body

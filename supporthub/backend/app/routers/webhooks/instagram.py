"""
app/routers/webhooks/instagram.py

FastAPI Webhook Router for Meta Instagram Direct (Instagram Login).
Handles GET handshake verification and POST message ingestion.
"""

from __future__ import annotations

import json
import logging
from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request, Response, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.services.whatsapp.auth import validate_verify_token
from app.services.instagram.auth import verify_instagram_signature
from app.services.instagram.webhook import process_instagram_webhook_background

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/instagram", tags=["webhooks-instagram"])


# ─── GET /webhooks/instagram — Meta Webhook Verification Handshake ───────────

@router.get(
    "",
    summary="Meta Instagram Webhook Verification",
    description="Handshake endpoint called by Meta when configuring webhooks in Meta App Dashboard.",
    response_class=Response,
)
async def verify_instagram_webhook(
    hub_mode: Optional[str] = Query(default=None, alias="hub.mode"),
    hub_challenge: Optional[str] = Query(default=None, alias="hub.challenge"),
    hub_verify_token: Optional[str] = Query(default=None, alias="hub.verify_token"),
) -> Response:
    """
    GET Webhook Verification Endpoint.
    Validates hub.verify_token against settings.meta_verify_token and returns hub.challenge as text/plain.
    """
    is_valid = validate_verify_token(
        hub_mode=hub_mode,
        hub_verify_token=hub_verify_token,
    )

    if not is_valid:
        logger.warning(
            "Instagram webhook verification FAILED | mode=%s | token_prefix=%s",
            hub_mode,
            (hub_verify_token or "")[:4],
        )
        return Response(
            content="Forbidden: invalid verify token or mode.",
            status_code=status.HTTP_403_FORBIDDEN,
            media_type="text/plain",
        )

    logger.info("Instagram webhook verification SUCCEEDED | challenge=%s", hub_challenge)
    return Response(
        content=str(hub_challenge or ""),
        status_code=status.HTTP_200_OK,
        media_type="text/plain",
    )


# ─── POST /webhooks/instagram — Ingest Webhook Messages ──────────────────────

@router.post(
    "",
    summary="Receive Instagram Messages from Meta",
    status_code=status.HTTP_200_OK,
    description="Validates X-Hub-Signature-256 HMAC, returns 200 OK immediately, and queues background task.",
)
async def receive_instagram_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    raw_body: Annotated[bytes, Depends(verify_instagram_signature)],
) -> dict:
    """
    POST Ingestion Endpoint.
    Validates HMAC-SHA256 signature using `verify_whatsapp_signature`.
    Returns HTTP 200 OK immediately and schedules background processing.
    """
    try:
        payload = json.loads(raw_body)
    except (json.JSONDecodeError, ValueError) as exc:
        logger.error("Instagram webhook received invalid JSON: %s", exc)
        return {"status": "ok", "note": "invalid_json_skipped"}

    if not isinstance(payload, dict):
        return {"status": "ok", "note": "non_dict_payload_skipped"}

    if payload.get("object") != "instagram":
        logger.debug("Instagram webhook ignored: object != 'instagram'")
        return {"status": "ok", "note": "ignored_object_type"}

    # Schedule background processing (User, Ticket, Message creation)
    background_tasks.add_task(
        process_instagram_webhook_background,
        payload=payload,
    )

    return {"status": "ok"}

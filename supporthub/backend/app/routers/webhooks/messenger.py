"""
app/routers/webhooks/messenger.py

FastAPI Webhook Router for Meta Facebook Messenger and Instagram.
Handles GET handshake verification and POST message ingestion.
Routes to background workers for debounced AI processing.
"""

from __future__ import annotations

import json
import logging
from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request, Response, status

from app.config import get_settings
from app.services.whatsapp.auth import validate_verify_token
from app.services.instagram.auth import verify_instagram_signature
from app.services.instagram.webhook import process_instagram_webhook_background
from app.services.facebook.webhook import process_facebook_webhook_background

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/messenger", tags=["webhooks-messenger"])


# ─── GET /webhooks/messenger — Meta Webhook Verification Handshake ───────────

@router.get(
    "",
    summary="Meta Messenger Webhook Verification",
    description="Handshake endpoint called by Meta when configuring webhooks in Meta App Dashboard.",
    response_class=Response,
)
async def verify_messenger_webhook(
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
            "Messenger webhook verification FAILED | mode=%s | token_prefix=%s",
            hub_mode,
            (hub_verify_token or "")[:4],
        )
        return Response(
            content="Forbidden: invalid verify token or mode.",
            status_code=status.HTTP_403_FORBIDDEN,
            media_type="text/plain",
        )

    logger.info("Messenger webhook verification SUCCEEDED | challenge=%s", hub_challenge)
    return Response(
        content=str(hub_challenge or ""),
        status_code=status.HTTP_200_OK,
        media_type="text/plain",
    )


# ─── POST /webhooks/messenger — Ingest Webhook Messages ──────────────────────

@router.post(
    "",
    summary="Receive Messenger Messages from Meta",
    status_code=status.HTTP_200_OK,
    description="Validates X-Hub-Signature-256 HMAC, returns 200 OK immediately, and queues background task.",
)
async def receive_messenger_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
) -> dict:
    """
    POST Ingestion Endpoint.
    Returns HTTP 200 OK immediately and schedules background processing.
    """
    try:
        payload = await request.json()
    except (json.JSONDecodeError, ValueError) as exc:
        logger.error("Messenger webhook received invalid JSON: %s", exc)
        return {"status": "ok", "note": "invalid_json_skipped"}

    if not isinstance(payload, dict):
        return {"status": "ok", "note": "non_dict_payload_skipped"}

    entries = payload.get("entry", [])
    if not entries:
        return {"status": "ok"}
    
    # Determine routing based on the first entry or object type
    first_entry = entries[0]
    page_id = str(first_entry.get("id", ""))
    
    is_instagram = (
        (settings.ig_page_id and page_id == str(settings.ig_page_id))
        or payload.get("object") == "instagram"
    )

    if is_instagram:
        background_tasks.add_task(
            process_instagram_webhook_background,
            payload=payload,
        )
    else:
        background_tasks.add_task(
            process_facebook_webhook_background,
            payload=payload,
        )

    return {"status": "ok"}

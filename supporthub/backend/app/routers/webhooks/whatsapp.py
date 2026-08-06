"""
app/routers/webhooks/whatsapp.py

HTTP layer for Meta WhatsApp Cloud API webhook endpoints.

This router is intentionally thin — it handles ONLY:
  - HTTP routing
  - Query parameter / header extraction
  - Delegating to services (auth, webhook orchestration)

It does NOT contain business logic. That lives in:
  app/services/whatsapp/auth.py       ← security
  app/services/whatsapp/parser.py     ← payload parsing
  app/services/whatsapp/webhook.py    ← orchestration
  app/services/whatsapp/sender.py     ← outbound messages

WHY THIS SEPARATION MATTERS:
  In a production SaaS, routers change frequently (versioning, new fields,
  auth changes). Services are stable. Keeping them separate means you can
  add a v2 router or a CLI trigger without duplicating business logic.
"""

from __future__ import annotations

import json
import logging
from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request, Response, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.services.whatsapp.auth import validate_verify_token, verify_whatsapp_signature

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/whatsapp", tags=["webhooks-whatsapp"])


# ─── GET /webhooks/whatsapp — Webhook Verification Handshake ─────────────────

@router.get(
    "",
    summary="Meta WhatsApp Webhook Verification",
    description=(
        "One-time handshake endpoint called by Meta when you register your webhook URL. "
        "Returns hub.challenge as plain text if the verify token matches."
    ),
    response_class=Response,
)
async def verify_whatsapp_webhook(
    hub_mode: Optional[str] = Query(default=None, alias="hub.mode"),
    hub_challenge: Optional[str] = Query(default=None, alias="hub.challenge"),
    hub_verify_token: Optional[str] = Query(default=None, alias="hub.verify_token"),
) -> Response:
    """
    Meta Webhook Verification Endpoint.

    Meta calls this endpoint when you:
      1. Add/edit your webhook URL in the Meta App Dashboard
      2. Subscribe to new webhook fields

    The flow:
      - Meta sends GET with hub.mode, hub.challenge, hub.verify_token
      - We verify the token matches our META_VERIFY_TOKEN secret
      - If valid: respond with hub.challenge as plain text → Meta confirms webhook
      - If invalid: respond with 403 → Meta will show an error in the Dashboard

    PRODUCTION TIP:
      hub.challenge is a random integer as a string. Meta compares it with
      what you echo back. Return it as plain text, NOT as JSON.
      Returning {"challenge": "..."} will FAIL the verification.
    """
    is_valid = validate_verify_token(
        hub_mode=hub_mode,
        hub_verify_token=hub_verify_token,
    )

    if not is_valid:
        logger.warning(
            "WhatsApp webhook verification FAILED | mode=%s | token_prefix=%s",
            hub_mode,
            (hub_verify_token or "")[:4],
        )
        return Response(
            content="Forbidden: invalid verify token or mode.",
            status_code=status.HTTP_403_FORBIDDEN,
            media_type="text/plain",
        )

    logger.info(
        "WhatsApp webhook verification SUCCEEDED | challenge=%s",
        hub_challenge,
    )

    # CRITICAL: Return the challenge as plain text exactly as Meta sent it.
    return Response(
        content=str(hub_challenge or ""),
        status_code=status.HTTP_200_OK,
        media_type="text/plain",
    )


# ─── POST /webhooks/whatsapp — Receive Incoming Messages ─────────────────────

@router.post(
    "",
    summary="Receive WhatsApp Messages from Meta",
    status_code=status.HTTP_200_OK,
    description=(
        "Receives inbound WhatsApp messages from Meta Cloud API. "
        "Validates HMAC-SHA256 signature, parses payload, and processes "
        "the conversation in the background."
    ),
)
async def receive_whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    raw_body: Annotated[bytes, Depends(verify_whatsapp_signature)],
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Meta Webhook POST — Incoming Messages.

    IMPORTANT — Always return 200 immediately:
      Meta expects a 200 OK within 20 seconds. If your server takes longer
      (e.g., AI is slow, DB is under load), Meta will retry the webhook.
      Retries cause duplicate message processing.

      Solution: Use BackgroundTasks to process the message AFTER returning 200.
      This decouples the Meta HTTP contract from your processing time.

    The signature is validated by the `verify_whatsapp_signature` dependency
    before this function body even runs. If the signature is invalid, FastAPI
    returns 403 automatically.

    Processing pipeline (runs in background):
      1. Parse raw payload → IncomingMessage (normalized internal model)
      2. Find or create Customer record
      3. Find or create Ticket (open conversation thread)
      4. Store customer message in DB
      5. Send to AI Agent → get reply
      6. Store AI reply in DB
      7. Send reply back to customer via WhatsApp Send API
    """
    # Import here to avoid circular imports (webhook.py imports models/session)
    from app.services.whatsapp.webhook import process_whatsapp_payload

    # Parse JSON from already-read raw body (avoid reading request.body() again)
    try:
        payload = json.loads(raw_body)
    except (json.JSONDecodeError, ValueError) as exc:
        logger.error("WhatsApp webhook received invalid JSON: %s", exc)
        # Still return 200 to prevent Meta from retrying a bad payload
        return {"status": "ok", "note": "invalid_json_skipped"}

    # Enqueue processing as a background task.
    # The HTTP response is returned to Meta BEFORE the processing begins.
    background_tasks.add_task(
        process_whatsapp_payload,
        payload=payload,
    )

    # Meta only cares that we return 200. The body content is ignored by Meta.
    return {"status": "ok"}

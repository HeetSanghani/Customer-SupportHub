"""
app/services/whatsapp/formatter.py

Outbound Payload Formatter for Meta's WhatsApp Cloud API.

WHY THIS FILE EXISTS:
  Meta's WhatsApp Cloud API expects specific, strict JSON payload structures
  depending on the message type (text, image, document, interactive buttons, template).

  Example Meta Text Payload:
    {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": "919876543210",
      "type": "text",
      "text": {"preview_url": false, "body": "Hello"}
    }

  Example Meta Interactive Quick Reply Payload:
    {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": "919876543210",
      "type": "interactive",
      "interactive": {
        "type": "button",
        "body": {"text": "How was our service?"},
        "action": {
          "buttons": [
            {"type": "reply", "reply": {"id": "btn_1", "title": "Great!"}},
            {"type": "reply", "reply": {"id": "btn_2", "title": "Needs Work"}}
          ]
        }
      }
    }

  Without a dedicated formatter, this JSON construction logic scatters into
  HTTP clients or senders, leading to hardcoded strings and fragile code.

  This file acts as a Builder / Strategy engine that transforms internal
  domain objects (`OutgoingMessage` or `AIResponse`) into strict Meta-compliant dicts.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from app.services.ai.models import AIResponse
from app.services.whatsapp.exceptions import FormattingError
from app.services.whatsapp.models import OutgoingMessage

# Meta limits
MAX_TEXT_LENGTH = 4096
MAX_QUICK_REPLY_BUTTONS = 3
MAX_BUTTON_TITLE_LENGTH = 20


class WhatsAppPayloadFormatter:
    """
    Constructs Meta WhatsApp Cloud API JSON payloads from domain objects.

    Usage:
        formatter = WhatsAppPayloadFormatter()
        payload = formatter.format_outgoing(outgoing_msg)
        # OR
        payload = formatter.format_ai_response(ai_response, recipient_phone="919876543210")
    """

    def format_ai_response(
        self,
        ai_response: AIResponse,
        recipient_phone: str,
    ) -> dict[str, Any]:
        """
        Format a standard AIResponse object into a WhatsApp text payload.
        """
        clean_phone = self.normalize_phone(recipient_phone)
        text_body = ai_response.response_text or ""

        if not text_body.strip():
            raise FormattingError("AIResponse text body is empty.")

        return self.format_text(clean_phone, text_body)

    def format_outgoing(self, message: OutgoingMessage) -> dict[str, Any]:
        """
        Format a generic OutgoingMessage domain object into a Meta JSON payload.
        Dispatches to the appropriate builder based on `message.message_type`.
        """
        clean_phone = self.normalize_phone(message.recipient_phone)
        msg_type = (message.message_type or "text").lower()

        formatters = {
            "text": lambda: self.format_text(clean_phone, message.text_body or ""),
            "image": lambda: self.format_media("image", clean_phone, message.media_url, message.caption),
            "document": lambda: self.format_media("document", clean_phone, message.media_url, message.caption),
            "audio": lambda: self.format_media("audio", clean_phone, message.media_url),
            "video": lambda: self.format_media("video", clean_phone, message.media_url, message.caption),
            "interactive": lambda: self.format_interactive(clean_phone, message.text_body or "", message.interactive_components),
            "template": lambda: self.format_template(clean_phone, message.template_name, message.template_language),
        }

        builder = formatters.get(msg_type)
        if not builder:
            raise FormattingError(f"Unsupported outbound message type: '{msg_type}'")

        return builder()

    # ─── Individual Type Formatters ───────────────────────────────────────────

    def format_text(self, recipient_phone: str, text: str) -> dict[str, Any]:
        """Format a plain text message."""
        clean_text = self._sanitize_and_truncate_text(text)
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": clean_text,
            },
        }

    def format_media(
        self,
        media_type: str,
        recipient_phone: str,
        media_url: Optional[str],
        caption: Optional[str] = None,
    ) -> dict[str, Any]:
        """Format an image, document, video, or audio media message."""
        if not media_url:
            raise FormattingError(f"Media URL is required for {media_type} messages.")

        media_payload: dict[str, Any] = {"link": media_url}
        if caption and media_type in ("image", "document", "video"):
            media_payload["caption"] = caption[:1024]  # Meta media caption limit

        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": media_type,
            media_type: media_payload,
        }

    def format_interactive(
        self,
        recipient_phone: str,
        body_text: str,
        components: Optional[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Format quick reply buttons or list messages.

        Expected components structure for buttons:
          {
            "type": "button",
            "buttons": [
               {"id": "btn_1", "title": "Yes"},
               {"id": "btn_2", "title": "No"}
            ]
          }
        """
        if not components or "buttons" not in components:
            raise FormattingError("Interactive components must contain a 'buttons' list.")

        buttons_raw = components["buttons"]
        if len(buttons_raw) > MAX_QUICK_REPLY_BUTTONS:
            raise FormattingError(
                f"WhatsApp interactive buttons limit exceeded ({len(buttons_raw)} > {MAX_QUICK_REPLY_BUTTONS})."
            )

        formatted_buttons = []
        for btn in buttons_raw:
            title = btn.get("title", "")[:MAX_BUTTON_TITLE_LENGTH]
            btn_id = btn.get("id") or f"btn_{len(formatted_buttons)}"
            formatted_buttons.append({
                "type": "reply",
                "reply": {
                    "id": btn_id,
                    "title": title,
                },
            })

        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text[:1024]},
                "action": {"buttons": formatted_buttons},
            },
        }

    def format_template(
        self,
        recipient_phone: str,
        template_name: Optional[str],
        language_code: str = "en_US",
    ) -> dict[str, Any]:
        """Format an approved Meta HSM Template message."""
        if not template_name:
            raise FormattingError("Template name is required for template messages.")

        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
            },
        }

    # ─── Phone Number Normalization ───────────────────────────────────────────

    @staticmethod
    def normalize_phone(phone: str) -> str:
        """
        Normalize phone numbers to standard Meta format (digits only).

        Example:
          "+91 98765-43210" → "919876543210"
          "09876543210"     → "9876543210"
        """
        if not phone:
            raise FormattingError("Recipient phone number is required.")

        # Strip all non-digit characters
        digits = re.sub(r"\D", "", phone)
        # Strip leading zeros
        digits = digits.lstrip("0")

        if len(digits) < 7 or len(digits) > 15:
            raise FormattingError(
                f"Invalid phone number length ({len(digits)} digits): '{phone}'."
            )

        return digits

    # ─── Text Sanitization ───────────────────────────────────────────────────

    @staticmethod
    def _sanitize_and_truncate_text(text: str) -> str:
        """Sanitize whitespace and enforce Meta 4096 character limit."""
        clean = (text or "").strip()
        if len(clean) > MAX_TEXT_LENGTH:
            clean = clean[: MAX_TEXT_LENGTH - 3] + "..."
        return clean

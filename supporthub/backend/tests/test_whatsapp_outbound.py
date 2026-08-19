"""Unit tests for WhatsApp outbound payload formatting and validation."""
from __future__ import annotations

import pytest
from app.services.whatsapp.formatter import WhatsAppPayloadFormatter
from app.services.whatsapp.models import OutgoingMessage, DeliveryStatus
from app.services.whatsapp.exceptions import FormattingError


def test_phone_normalization():
    assert WhatsAppPayloadFormatter.normalize_phone("+91-98765-43210") == "919876543210"
    assert WhatsAppPayloadFormatter.normalize_phone("09876543210") == "9876543210"
    assert WhatsAppPayloadFormatter.normalize_phone("91 98765 43210") == "919876543210"


def test_phone_validation():
    with pytest.raises(FormattingError):
        WhatsAppPayloadFormatter.normalize_phone("123")  # Too short


def test_build_text_payload():
    formatter = WhatsAppPayloadFormatter()
    payload = formatter.format_text("919876543210", "Hello there!")
    assert payload["messaging_product"] == "whatsapp"
    assert payload["to"] == "919876543210"
    assert payload["type"] == "text"
    assert payload["text"]["body"] == "Hello there!"


def test_build_interactive_button_payload():
    formatter = WhatsAppPayloadFormatter()
    components = {
        "buttons": [
            {"id": "btn_yes", "title": "Yes, resolved"},
            {"id": "btn_no", "title": "Need agent"},
        ]
    }
    payload = formatter.format_interactive(
        "919876543210",
        body_text="Did this answer your question?",
        components=components,
    )
    assert payload["type"] == "interactive"
    assert payload["interactive"]["type"] == "button"
    assert len(payload["interactive"]["action"]["buttons"]) == 2


def test_interactive_button_limit():
    formatter = WhatsAppPayloadFormatter()
    components = {
        "buttons": [
            {"id": f"btn_{i}", "title": f"Option {i}"} for i in range(4)
        ]
    }
    with pytest.raises(FormattingError):
        formatter.format_interactive(
            "919876543210",
            body_text="Choose one",
            components=components,
        )

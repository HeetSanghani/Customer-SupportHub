"""Unit tests for WhatsApp webhook verification and payload parsing."""
from __future__ import annotations

import json
from datetime import datetime, timezone
import pytest
from app.services.whatsapp.parser import parse_whatsapp_payload
from app.services.channels.models import Channel, MessageType


def text_payload(msg_id="wamid.TEST001", from_phone="919876543210", text="Hello I need help"):
    return {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "116803970401834",
            "changes": [{
                "field": "messages",
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {"display_phone_number": "15551234567", "phone_number_id": "123456789"},
                    "contacts": [{"profile": {"name": "Heet Patel"}, "wa_id": from_phone}],
                    "messages": [{
                        "id": msg_id,
                        "from": from_phone,
                        "timestamp": "1722918000",
                        "type": "text",
                        "text": {"body": text}
                    }]
                }
            }]
        }]
    }


def test_whatsapp_parse_text_message():
    result = parse_whatsapp_payload(text_payload())
    assert len(result.messages) == 1
    m = result.messages[0]
    assert m.channel == Channel.whatsapp
    assert m.message_type == MessageType.text
    assert m.customer_channel_id == "919876543210"
    assert m.customer_name == "Heet Patel"
    assert m.text == "Hello I need help"
    assert m.channel_message_id == "wamid.TEST001"
    assert m.phone_number_id == "123456789"


def test_whatsapp_parse_status_update_ignored():
    status_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "xxx",
            "changes": [{
                "field": "messages",
                "value": {
                    "metadata": {"phone_number_id": "123"},
                    "statuses": [{
                        "id": "wamid.out1",
                        "status": "delivered",
                        "timestamp": "1722918005",
                        "recipient_id": "919876543210"
                    }]
                }
            }]
        }]
    }
    result = parse_whatsapp_payload(status_payload)
    assert len(result.messages) == 0


def test_whatsapp_parse_image_attachment():
    img_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "xxx",
            "changes": [{
                "field": "messages",
                "value": {
                    "metadata": {"phone_number_id": "123"},
                    "contacts": [{"profile": {"name": "Heet"}, "wa_id": "919876543210"}],
                    "messages": [{
                        "id": "wamid.IMG1",
                        "from": "919876543210",
                        "timestamp": "1722918010",
                        "type": "image",
                        "image": {
                            "id": "media_abc",
                            "mime_type": "image/jpeg",
                            "sha256": "deadbeef",
                            "caption": "Damaged product"
                        }
                    }]
                }
            }]
        }]
    }
    result = parse_whatsapp_payload(img_payload)
    assert len(result.messages) == 1
    m = result.messages[0]
    assert m.message_type == MessageType.image
    assert len(m.attachments) == 1
    assert m.attachments[0].media_id == "media_abc"
    assert m.attachments[0].mime_type == "image/jpeg"
    assert m.text == "Damaged product"


def test_whatsapp_parse_document_attachment():
    doc_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "xxx",
            "changes": [{
                "field": "messages",
                "value": {
                    "metadata": {"phone_number_id": "123"},
                    "contacts": [{"profile": {"name": "Heet"}, "wa_id": "919876543210"}],
                    "messages": [{
                        "id": "wamid.DOC1",
                        "from": "919876543210",
                        "timestamp": "1722918015",
                        "type": "document",
                        "document": {
                            "id": "doc_xyz",
                            "mime_type": "application/pdf",
                            "filename": "invoice.pdf",
                            "caption": "My invoice"
                        }
                    }]
                }
            }]
        }]
    }
    result = parse_whatsapp_payload(doc_payload)
    assert len(result.messages) == 1
    m = result.messages[0]
    assert m.message_type == MessageType.document
    assert m.attachments[0].filename == "invoice.pdf"
    assert m.attachments[0].mime_type == "application/pdf"


def test_whatsapp_parse_location_message():
    loc_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "xxx",
            "changes": [{
                "field": "messages",
                "value": {
                    "metadata": {"phone_number_id": "123"},
                    "contacts": [{"profile": {"name": "Heet"}, "wa_id": "919876543210"}],
                    "messages": [{
                        "id": "wamid.LOC1",
                        "from": "919876543210",
                        "timestamp": "1722918020",
                        "type": "location",
                        "location": {
                            "latitude": 23.0225,
                            "longitude": 72.5714,
                            "name": "Ahmedabad Airport",
                            "address": "SVPIA"
                        }
                    }]
                }
            }]
        }]
    }
    result = parse_whatsapp_payload(loc_payload)
    assert len(result.messages) == 1
    m = result.messages[0]
    assert m.message_type == MessageType.location
    assert m.location is not None
    assert m.location.latitude == 23.0225
    assert m.location.name == "Ahmedabad Airport"


def test_whatsapp_parse_reaction_skipped():
    react_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "xxx",
            "changes": [{
                "field": "messages",
                "value": {
                    "metadata": {"phone_number_id": "123"},
                    "contacts": [{"profile": {"name": "Heet"}, "wa_id": "919876543210"}],
                    "messages": [{
                        "id": "wamid.REACT1",
                        "from": "919876543210",
                        "timestamp": "1722918025",
                        "type": "reaction",
                        "reaction": {"message_id": "wamid.PREV", "emoji": "👍"}
                    }]
                }
            }]
        }]
    }
    result = parse_whatsapp_payload(react_payload)
    assert len(result.messages) == 0


def test_whatsapp_parse_interactive_button():
    btn_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "xxx",
            "changes": [{
                "field": "messages",
                "value": {
                    "metadata": {"phone_number_id": "123"},
                    "contacts": [{"profile": {"name": "Heet"}, "wa_id": "919876543210"}],
                    "messages": [{
                        "id": "wamid.BTN1",
                        "from": "919876543210",
                        "timestamp": "1722918030",
                        "type": "interactive",
                        "interactive": {
                            "type": "button_reply",
                            "button_reply": {"id": "btn_1", "title": "Track my order"}
                        }
                    }]
                }
            }]
        }]
    }
    result = parse_whatsapp_payload(btn_payload)
    assert len(result.messages) == 1
    m = result.messages[0]
    assert m.message_type == MessageType.interactive
    assert m.text == "Track my order"


def test_whatsapp_parse_wrong_object_error():
    result = parse_whatsapp_payload({"object": "instagram_business_account", "entry": []})
    assert len(result.messages) == 0
    assert len(result.errors) > 0


def test_whatsapp_parse_missing_id_skipped():
    no_id_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "xxx",
            "changes": [{
                "field": "messages",
                "value": {
                    "metadata": {"phone_number_id": "123"},
                    "contacts": [{"profile": {"name": "Heet"}, "wa_id": "919876543210"}],
                    "messages": [{"from": "919876543210", "timestamp": "1722918000", "type": "text", "text": {"body": "no id"}}]
                }
            }]
        }]
    }
    result = parse_whatsapp_payload(no_id_payload)
    assert len(result.messages) == 0


def test_whatsapp_parse_batched_messages():
    batch_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "xxx",
            "changes": [{
                "field": "messages",
                "value": {
                    "metadata": {"phone_number_id": "123"},
                    "contacts": [{"profile": {"name": "Heet"}, "wa_id": "919876543210"}],
                    "messages": [
                        {"id": "wamid.BATCH1", "from": "919876543210", "timestamp": "1722918000", "type": "text", "text": {"body": "First message"}},
                        {"id": "wamid.BATCH2", "from": "919876543210", "timestamp": "1722918001", "type": "text", "text": {"body": "Second message"}},
                    ]
                }
            }]
        }]
    }
    result = parse_whatsapp_payload(batch_payload)
    assert len(result.messages) == 2
    assert result.messages[0].text == "First message"
    assert result.messages[1].text == "Second message"

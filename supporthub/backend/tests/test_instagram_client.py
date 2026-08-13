"""
tests/test_instagram_client.py

Standalone asyncio unit test suite for MetaInstagramClient.
Uses httpx.MockTransport to test without live Meta HTTP requests or external dependencies.
Ensures zero token exposure, correct validation, and accurate error mapping.
"""

import asyncio
import json
import httpx

from app.services.instagram.client import MetaInstagramClient, MAX_TEXT_LENGTH
from app.services.whatsapp.exceptions import (
    AuthenticationError,
    FormattingError,
    RateLimitError,
    WhatsAppProviderError as InstagramProviderError,
)

TEST_IGSID = "17841400000000000"
TEST_TOKEN = "IGAA_TEST_MOCK_TOKEN_12345"


async def test_send_text_message_success():
    """Test 1: Successful text message send."""
    mock_response_data = {
        "recipient_id": TEST_IGSID,
        "message_id": "aWdfbWVzc2FnZV9pZDoxNzg0MTQwMDAwMDAwMDAwMA=="
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.host == "graph.instagram.com"
        assert request.url.path == "/v19.0/me/messages"
        assert request.headers["Authorization"] == f"Bearer {TEST_TOKEN}"
        
        body = json.loads(request.content.decode("utf-8"))
        assert body["recipient"]["id"] == TEST_IGSID
        assert body["message"]["text"] == "Hello from unit test"

        return httpx.Response(200, json=mock_response_data)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        res = await client.send_text_message(recipient_igsid=TEST_IGSID, text="Hello from unit test")

    assert res.success is True
    assert res.provider_message_id == "aWdfbWVzc2FnZV9pZDoxNzg0MTQwMDAwMDAwMDAwMA=="
    assert res.status_code == 200


async def test_missing_token_raises_auth_error():
    """Test 2: Missing access token raises AuthenticationError."""
    transport = httpx.MockTransport(lambda req: httpx.Response(500))
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token="", client=http_client)
        try:
            await client.send_text_message(recipient_igsid=TEST_IGSID, text="Hello")
            assert False, "Expected AuthenticationError was not raised"
        except AuthenticationError as exc:
            assert "INSTAGRAM_ACCESS_TOKEN is not configured" in str(exc) or "INSTAGRAM_ACCESS_TOKEN is not configured" in exc.detail


async def test_empty_recipient_id_raises_formatting_error():
    """Test 3: Empty recipient ID raises FormattingError."""
    transport = httpx.MockTransport(lambda req: httpx.Response(500))
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        try:
            await client.send_text_message(recipient_igsid="", text="Hello")
            assert False, "Expected FormattingError was not raised"
        except FormattingError as exc:
            assert "recipient_igsid must not be empty" in exc.detail


async def test_empty_text_raises_formatting_error():
    """Test 4: Empty text raises FormattingError."""
    transport = httpx.MockTransport(lambda req: httpx.Response(500))
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        try:
            await client.send_text_message(recipient_igsid=TEST_IGSID, text="")
            assert False, "Expected FormattingError was not raised"
        except FormattingError as exc:
            assert "Message text must not be empty" in exc.detail


async def test_exceed_max_length_raises_formatting_error():
    """Test 5: Exceeding text limit raises FormattingError."""
    transport = httpx.MockTransport(lambda req: httpx.Response(500))
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        long_text = "a" * (MAX_TEXT_LENGTH + 1)
        try:
            await client.send_text_message(recipient_igsid=TEST_IGSID, text=long_text)
            assert False, "Expected FormattingError was not raised"
        except FormattingError as exc:
            assert f"exceeds Instagram maximum length of {MAX_TEXT_LENGTH}" in exc.detail


async def test_http_400_raises_provider_error():
    """Test 6: HTTP 400 Bad Request raises InstagramProviderError."""
    mock_error_data = {
        "error": {
            "message": "(#100) Param recipient[id] must be a valid IGSID",
            "type": "OAuthException",
            "code": 100
        }
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json=mock_error_data)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        try:
            await client.send_text_message(recipient_igsid=TEST_IGSID, text="Hello")
            assert False, "Expected InstagramProviderError was not raised"
        except InstagramProviderError as exc:
            assert exc.status_code == 400
            assert exc.error_code == 100


async def test_http_401_raises_auth_error():
    """Test 7: HTTP 401 Unauthorized raises AuthenticationError."""
    mock_error_data = {
        "error": {
            "message": "Invalid OAuth access token",
            "type": "OAuthException",
            "code": 190
        }
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json=mock_error_data)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        try:
            await client.send_text_message(recipient_igsid=TEST_IGSID, text="Hello")
            assert False, "Expected AuthenticationError was not raised"
        except AuthenticationError as exc:
            assert exc.status_code == 401
            assert exc.error_code == 190


async def test_http_403_raises_auth_error():
    """Test 8: HTTP 403 Forbidden raises AuthenticationError."""
    mock_error_data = {
        "error": {
            "message": "(#200) Permissions error",
            "type": "OAuthException",
            "code": 200
        }
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json=mock_error_data)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        try:
            await client.send_text_message(recipient_igsid=TEST_IGSID, text="Hello")
            assert False, "Expected AuthenticationError was not raised"
        except AuthenticationError as exc:
            assert exc.status_code == 403


async def test_http_429_raises_rate_limit_error():
    """Test 9: HTTP 429 Rate Limit raises RateLimitError."""
    mock_error_data = {
        "error": {
            "message": "Application request limit reached",
            "type": "OAuthException",
            "code": 429
        }
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json=mock_error_data)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        try:
            await client.send_text_message(recipient_igsid=TEST_IGSID, text="Hello")
            assert False, "Expected RateLimitError was not raised"
        except RateLimitError as exc:
            assert exc.status_code == 429


async def test_http_500_raises_retryable_provider_error():
    """Test 10: HTTP 500 Internal Error raises retryable ProviderError."""
    mock_error_data = {
        "error": {
            "message": "An unknown error occurred",
            "type": "OAuthException",
            "code": 2
        }
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json=mock_error_data)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        try:
            await client.send_text_message(recipient_igsid=TEST_IGSID, text="Hello")
            assert False, "Expected InstagramProviderError was not raised"
        except InstagramProviderError as exc:
            assert exc.status_code == 500
            assert exc.is_retryable is True


async def test_token_redacted_in_exceptions():
    """Test 11: Secret access token is never leaked in error messages."""
    secret_token = "IGAA_SUPER_SECRET_TOKEN_DO_NOT_LEAK"
    mock_error_data = {
        "error": {
            "message": f"Error with token {secret_token} on request",
            "type": "OAuthException",
            "code": 190
        }
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json=mock_error_data)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=secret_token, client=http_client)
        try:
            await client.send_text_message(recipient_igsid=TEST_IGSID, text="Hello")
            assert False, "Expected AuthenticationError was not raised"
        except AuthenticationError as exc:
            err_str = str(exc)
            assert secret_token not in err_str
            assert "[REDACTED_INSTAGRAM_TOKEN]" in err_str


async def test_get_user_profile_success():
    """Test 12: Successful user profile retrieval from Meta Graph API."""
    mock_profile = {
        "id": TEST_IGSID,
        "name": "Heet Sanghani",
        "username": "_heet_patel_3108",
        "profile_pic": "https://instagram.example.com/pic.jpg",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.host == "graph.instagram.com"
        assert request.url.path == f"/v19.0/{TEST_IGSID}"
        assert request.headers["Authorization"] == f"Bearer {TEST_TOKEN}"
        return httpx.Response(200, json=mock_profile)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = MetaInstagramClient(access_token=TEST_TOKEN, client=http_client)
        data = await client.get_user_profile(TEST_IGSID)

    assert data.get("name") == "Heet Sanghani"
    assert data.get("username") == "_heet_patel_3108"
    assert data.get("profile_pic") == "https://instagram.example.com/pic.jpg"


async def main():
    tests = [
        test_send_text_message_success,
        test_missing_token_raises_auth_error,
        test_empty_recipient_id_raises_formatting_error,
        test_empty_text_raises_formatting_error,
        test_exceed_max_length_raises_formatting_error,
        test_http_400_raises_provider_error,
        test_http_401_raises_auth_error,
        test_http_403_raises_auth_error,
        test_http_429_raises_rate_limit_error,
        test_http_500_raises_retryable_provider_error,
        test_token_redacted_in_exceptions,
        test_get_user_profile_success,
    ]
    print("==================================================")
    print("      RUNNING INSTAGRAM CLIENT UNIT TESTS         ")
    print("==================================================")
    for test in tests:
        await test()
        print(f"  ✅ PASSED: {test.__name__}")
    print("\nALL INSTAGRAM CLIENT UNIT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())


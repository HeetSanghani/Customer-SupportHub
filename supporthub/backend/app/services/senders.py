import logging
import httpx
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

print("=== MAILGUN DEBUG ===")
print("API KEY:", repr(settings.mailgun_api_key))
print("DOMAIN:", repr(settings.mailgun_domain))
print("======================")


import asyncio

async def send_email_reply(to_email: str, subject: str, body: str, ticket_ref: str = None) -> bool:
    """Sends an outbound email reply using Mailgun HTTP API with exponential backoff retry."""
    ref_tag = f"[{ticket_ref}] " if ticket_ref else ""
    if not settings.mailgun_api_key or not settings.mailgun_domain:
        logger.warning(f"{ref_tag}Mailgun API key or domain not configured; skipping email dispatch.")
        return False

    if settings.mailgun_is_sandbox:
        logger.warning(
            f"{ref_tag}Outbound email is using Mailgun sandbox domain ({settings.mailgun_domain}). "
            "Outbound emails may land in Spam or require authorized recipient verification in Mailgun dashboard."
        )

    url = f"https://api.mailgun.net/v3/{settings.mailgun_domain}/messages"
    auth = ("api", settings.mailgun_api_key)
    
    email_subject = subject if subject.lower().startswith("re:") else f"Re: {subject}"
    from_address = f"SupportHub <support@{settings.mailgun_domain}>"

    data = {
        "from": from_address,
        "to": to_email,
        "subject": email_subject,
        "text": body,
    }

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, auth=auth, data=data)
                if response.status_code == 200:
                    logger.info(f"{ref_tag}Mailgun email successfully sent to {to_email} (attempt {attempt})")
                    return True
                
                logger.error(f"{ref_tag}Mailgun API error ({response.status_code}) on attempt {attempt}/{max_attempts}: {response.text}")
                # Retry on 5xx server errors or rate limits
                if response.status_code >= 500 or response.status_code == 429:
                    if attempt < max_attempts:
                        await asyncio.sleep(2 ** attempt)
                        continue
                return False
        except (httpx.TransportError, httpx.TimeoutException) as exc:
            logger.error(f"{ref_tag}Transport/Network error sending email via Mailgun (attempt {attempt}/{max_attempts}): {exc}")
            if attempt < max_attempts:
                await asyncio.sleep(2 ** attempt)
                continue
            return False
        except Exception as exc:
            logger.error(f"{ref_tag}Unexpected exception sending email via Mailgun: {exc}")
            return False

    return False


async def send_whatsapp_reply(to_phone: str, text: str) -> bool:
    """Sends an outbound WhatsApp message using Meta Cloud API."""
    if not settings.whatsapp_phone_id or not settings.meta_app_token:
        logger.warning("WhatsApp Phone ID or Meta App Token not configured; skipping WhatsApp dispatch.")
        return False

    url = f"https://graph.facebook.com/v19.0/{settings.whatsapp_phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {settings.meta_app_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": text},
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code in (200, 201):
                logger.info(f"WhatsApp message successfully sent to {to_phone}")
                return True
            else:
                logger.error(f"WhatsApp Meta API error ({response.status_code}): {response.text}")
                return False
    except Exception as exc:
        logger.error(f"Failed to send WhatsApp message: {exc}")
        return False


async def send_messenger_reply(recipient_id: str, text: str, page_access_token: str = None) -> bool:
    """Sends an outbound Facebook Messenger or Instagram message using Meta Graph API."""
    token = page_access_token or settings.page_access_token
    if not token:
        logger.warning("Page Access Token not configured; skipping Messenger/Instagram dispatch.")
        return False

    url = "https://graph.facebook.com/v19.0/me/messages"
    params = {"access_token": token}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, params=params, json=payload)
            if response.status_code in (200, 201):
                logger.info(f"Messenger/Instagram message successfully sent to recipient {recipient_id}")
                return True
            else:
                logger.error(f"Messenger Meta API error ({response.status_code}): {response.text}")
                return False
    except Exception as exc:
        logger.error(f"Failed to send Messenger/Instagram message: {exc}")
        return False




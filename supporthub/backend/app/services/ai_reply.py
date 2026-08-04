import logging
import os
import httpx
from app.config import get_settings
from app.ai import generate_chat_response

logger = logging.getLogger(__name__)
settings = get_settings()


async def generate_ai_reply(conversation_history: list[dict]) -> str:
    """
    Generates an automated AI response based on ticket conversation history.
    conversation_history list structure:
    [{"role": "user" | "assistant" | "system", "content": "..."}, ...]
    """
    system_prompt = "You are a helpful customer support assistant for SupportHub. Be concise and friendly."
    openai_key = settings.openai_api_key or os.environ.get("OPENAI_API_KEY")

    # If OpenAI API Key is provided, use OpenAI Chat Completions API
    if openai_key:
        try:
            messages = [{"role": "system", "content": system_prompt}] + conversation_history
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {openai_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 300,
                    },
                )
                if response.status_code == 200:
                    data = response.json()
                    reply = data["choices"][0]["message"]["content"].strip()
                    return reply
                else:
                    logger.error(f"OpenAI API error ({response.status_code}): {response.text}")
        except Exception as exc:
            logger.error(f"Failed to generate OpenAI reply: {exc}")

    # Fallback to existing Gemini AI implementation if OpenAI is unavailable
    try:
        context_str = "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in conversation_history])
        full_prompt = f"{system_prompt}\n\nConversation History:\n{context_str}\n\nAssistant:"
        reply = await generate_chat_response(full_prompt)
        return reply.strip()
    except Exception as exc:
        logger.error(f"Failed to generate Gemini fallback reply: {exc}")
        return "Thank you for reaching out to SupportHub! A support representative will review your message shortly."

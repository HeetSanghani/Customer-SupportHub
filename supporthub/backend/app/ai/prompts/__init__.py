"""Prompt templates package for SupportHub AI."""
from app.ai.prompts.system import SHOPKART_SYSTEM_PROMPT
from app.ai.prompts.intent import INTENT_CLASSIFICATION_PROMPT, INTENT_EXTRACTION_SCHEMA
from app.ai.prompts.response import RESPONSE_SYNTHESIS_PROMPT
from app.ai.prompts.escalation import ESCALATION_EVALUATION_PROMPT

__all__ = [
    "SHOPKART_SYSTEM_PROMPT",
    "INTENT_CLASSIFICATION_PROMPT",
    "INTENT_EXTRACTION_SCHEMA",
    "RESPONSE_SYNTHESIS_PROMPT",
    "ESCALATION_EVALUATION_PROMPT"
]

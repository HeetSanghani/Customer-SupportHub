"""
app/services/ai/prompt_builder.py

Constructs the final prompt from LLMContext.

SINGLE RESPONSIBILITY:
  This module is a pure string-formatting engine.
  It receives an LLMContext, applies business rules and formatting,
  and returns a Prompt object ready to be sent to any LLM.

  It NEVER:
    - Calls an LLM (that's model_adapter.py)
    - Reads from the database (that's context_builder.py)
    - Knows what channel the message came from (irrelevant at this layer)

WHY A DEDICATED PROMPT BUILDER:
  Without it, prompt logic scatters into adapters, routers, and services.
  Then A/B testing a prompt change requires touching 5 files.

  With a dedicated PromptBuilder:
    - Changing the tone? One file.
    - Adding safety rules? One file.
    - A/B testing system prompts? Subclass PromptBuilder.
    - Testing that the prompt contains the customer name? Unit test one class.

PROMPT VERSIONING:
  Every Prompt has a version string. When you change the system prompt,
  increment the version. The repository stores the version with every
  AI response, so you can compare: did responses improve after v1.1?

  In production (Intercom, Freshdesk), prompt versions are tied to A/B
  experiments. Each version runs on a percentage of traffic, and response
  quality metrics determine the winner.

SYSTEM PROMPT DESIGN:
  A production-quality system prompt has these sections:
  1. ROLE     — who the AI is
  2. RULES    — what it must/must not do (safety, scope, escalation)
  3. TONE     — how it should communicate
  4. CONTEXT  — customer name, channel, conversation state
  5. OUTPUT   — how to format the response

  This structure is used by Anthropic's Constitutional AI, OpenAI's system
  prompt best practices, and all major enterprise AI deployments.
"""

from __future__ import annotations

import logging

from app.services.ai.exceptions import PromptBuildError
from app.services.ai.models import LLMContext, Prompt

logger = logging.getLogger(__name__)

# Current prompt version — increment when system prompt changes
PROMPT_VERSION = "v1.0"

# Model configuration defaults
DEFAULT_TEMPERATURE = 0.4    # Low = more predictable/consistent (good for support)
DEFAULT_MAX_TOKENS = 500     # Enough for a helpful reply, not so long it rambles
DEFAULT_MODEL = "gemini-flash-lite-latest"


class PromptBuilder:
    """
    Builds a versioned Prompt from an LLMContext.

    Usage:
        builder = PromptBuilder()
        prompt = builder.build(llm_context)

    To customize for a specific use case (e.g., e-commerce), subclass and
    override _build_system_prompt() or _build_business_rules().
    """

    def build(
        self,
        llm_context: LLMContext,
        model_name: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> Prompt:
        """
        Build a versioned, production-ready Prompt.

        Args:
            llm_context: Clean context from ContextBuilder.
            model_name: Which model this prompt targets.
            temperature: LLM temperature (0=deterministic, 1=creative).
            max_tokens: Maximum response length in tokens.

        Returns:
            Prompt — immutable, versionable, loggable.

        Raises:
            PromptBuildError: If context is missing required fields.
        """
        try:
            system = self._build_system_prompt(llm_context)
            messages = self._build_messages(llm_context)

            prompt = Prompt(
                system=system,
                messages=messages,
                version=PROMPT_VERSION,
                temperature=temperature,
                max_tokens=max_tokens,
                model_name=model_name,
                image_paths=llm_context.image_paths,
            )

            logger.debug(
                "Prompt built | version=%s | history_msgs=%d | est_tokens=%d | "
                "system_hash=%s",
                prompt.version,
                len(llm_context.history),
                prompt.estimated_input_tokens,
                prompt.system_hash,
            )

            return prompt

        except PromptBuildError:
            raise
        except Exception as exc:
            raise PromptBuildError(f"Unexpected error building prompt: {exc}") from exc

    # ─── System Prompt ────────────────────────────────────────────────────────

    def _build_system_prompt(self, ctx: LLMContext) -> str:
        role_section = self._build_role_section(ctx)
        rules_section = self._build_business_rules(ctx)
        tone_section = self._build_tone_section(ctx)
        context_section = self._build_context_section(ctx)
        kb_section = self._build_kb_section(ctx)
        output_section = self._build_output_section(ctx)

        sections = [role_section, rules_section, tone_section, context_section]
        if kb_section:
            sections.append(kb_section)
        sections.append(output_section)

        return "\n\n".join(sections).strip()

    def _build_role_section(self, ctx: LLMContext) -> str:
        channel_desc = f" for {ctx.channel.upper()}" if ctx.channel else ""
        return (
            "## ROLE\n"
            f"You are a helpful, professional AI support agent for SupportHub{channel_desc}. "
            "Your goal is to understand the customer's issue and provide a clear, "
            "accurate, and friendly response."
        )

    def _build_business_rules(self, ctx: LLMContext) -> str:
        rules = [
            "## RULES (NEVER VIOLATE THESE)",
            "1. NEVER invent information. NEVER invent company policies, prices, discounts, or terms not provided in context.",
            "2. NEVER claim an action was performed (e.g. 'I refunded your money' or 'I processed your return') unless confirmed in context.",
            "3. NEVER make promises about refunds, timelines, or policies unless stated explicitly in context.",
            "4. NEVER share another customer's information.",
            "5. NEVER pretend to be human if the customer sincerely asks if they are talking to an AI.",
            "6. If the customer is very angry, frustrated, or requests a human — suggest escalation.",
            "7. Stay on topic. Do not discuss politics, religion, or unrelated subjects.",
            "8. If the conversation has resolved the issue — confirm and close warmly.",
        ]

        if ctx.ticket_priority in ("urgent", "high"):
            rules.append(
                "9. This ticket is marked HIGH PRIORITY. Treat this as urgent. "
                "Acknowledge the urgency immediately."
            )

        return "\n".join(rules)

    def _build_tone_section(self, ctx: LLMContext) -> str:
        channel = ctx.channel
        base_tone = "professional yet conversational"

        if ctx.tone == "friendly":
            base_tone = "warm, enthusiastic, and highly approachable"
        elif ctx.tone == "shorter":
            base_tone = "extremely brief, direct, and to the point"
        elif ctx.tone == "professional":
            base_tone = "formal, precise, and polite"
        elif channel == "instagram":
            base_tone = "friendly, concise, and approachable for Instagram Direct Messages"
        elif channel == "whatsapp":
            base_tone = "friendly, concise, and conversational — like a knowledgeable friend"
        elif channel == "email":
            base_tone = "professional, clear, and structured"

        welcome_note = ""
        if ctx.is_new_customer:
            welcome_note = (
                "\nThis is the customer's FIRST interaction. Start with a warm welcome "
                "and introduce yourself briefly."
            )
        elif ctx.is_new_conversation:
            welcome_note = (
                "\nThis is a new conversation from a returning customer. "
                "Greet them appropriately without re-introducing from scratch."
            )

        return f"## TONE\nBe {base_tone}.{welcome_note}"

    def _build_context_section(self, ctx: LLMContext) -> str:
        lines = [
            "## CURRENT CONTEXT",
            f"Customer Name: {ctx.customer_name}",
            f"Channel: {ctx.channel.upper()}",
            f"Conversation Reference: {ctx.conversation_ref}",
            f"Conversation Status: {ctx.ticket_status}",
            f"Priority: {ctx.ticket_priority}",
        ]

        if ctx.ticket_subject:
            lines.append(f"Subject: {ctx.ticket_subject}")
        if ctx.ticket_category:
            lines.append(f"Category: {ctx.ticket_category}")

        if ctx.current_message_type != "text":
            lines.append(
                f"Message Type: {ctx.current_message_type} "
                f"(the customer sent a non-text message, handle gracefully)"
            )

        return "\n".join(lines)

    def _build_kb_section(self, ctx: LLMContext) -> str | None:
        if not ctx.kb_context:
            return None
        return f"## VERIFIED KNOWLEDGE BASE & POLICIES\n{ctx.kb_context}"

    def _build_output_section(self, ctx: LLMContext) -> str:
        lines = [
            "## OUTPUT FORMAT",
            "- Write in plain text. Do NOT use markdown formatting (no **, no ##, no bullets with -).",
            "- Use short paragraphs.",
        ]
        if ctx.channel == "instagram":
            lines.append("- This response is tailored for Instagram Direct Messages. Keep it plain text, concise, and friendly. Do NOT use markdown headings.")
        elif ctx.channel == "whatsapp":
            lines.append("- Be concise. Customers on WhatsApp prefer short, clear replies.")
        lines.extend([
            "- Address the customer by their first name if known.",
            "- End with a clear next step or a question if more info is needed."
        ])
        return "\n".join(lines)

    # ─── Message History ──────────────────────────────────────────────────────

    def _build_messages(self, ctx: LLMContext) -> list[dict]:
        """
        Build the full messages list for the LLM.

        Structure:
          [ ...history messages..., {"role": "user", "content": <current message>} ]

        The current message is always the LAST item, clearly marked as the
        message the customer just sent. This is what the LLM responds to.
        """
        messages = list(ctx.history)  # Copy history

        # Append the current incoming message
        current_content = ctx.current_message
        if ctx.current_message_type != "text":
            # Add context about what type of media was sent
            current_content = (
                f"{ctx.current_message}\n"
                f"[Note: The customer sent a {ctx.current_message_type} message. "
                f"Acknowledge it appropriately.]"
            )

        messages.append({"role": "user", "content": current_content})
        return messages

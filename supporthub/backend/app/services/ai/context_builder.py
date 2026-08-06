"""
app/services/ai/context_builder.py

Translates ConversationContext (ORM-rich, DB-coupled) into
LLMContext (clean, serialization-safe, AI-ready).

SINGLE RESPONSIBILITY:
  This file does EXACTLY one thing: extract and format relevant information
  from the ConversationContext for the LLM.

  It makes decisions like:
    - How many history messages to include (token budget)
    - What to use as the "current message" (text, or a description of media)
    - How to represent a customer with no name
    - Whether this is a new vs. returning customer scenario

WHY THIS LAYER MUST EXIST:
  Without it, the PromptBuilder would receive ORM objects. The PromptBuilder
  would then directly access ticket.customer.name — tightly coupling the
  prompt logic to the database schema.

  With ContextBuilder as a translator:
    - PromptBuilder only sees LLMContext (plain strings)
    - If you rename the DB column from 'name' to 'display_name', only
      ContextBuilder needs updating — not the PromptBuilder or ModelAdapter
    - You can unit test PromptBuilder with a mocked LLMContext, no DB needed

PRODUCTION EXAMPLE:
  Intercom's AI layer has a "Conversation Enrichment" step that does exactly
  this — it fetches contact attributes, conversation tags, and custom data
  fields, then packages them into a structured context object before the
  prompt is constructed.

TOKEN BUDGET MANAGEMENT:
  Every LLM has a context window limit (tokens). Including all 500 messages
  in the history would exceed any model's limit. The ContextBuilder decides
  how many messages to include based on:
    1. How many characters each message contains
    2. The model's estimated token budget for history
    3. Always including at least the most recent N messages for coherence
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.services.ai.exceptions import ContextBuildError
from app.services.ai.models import LLMContext

if TYPE_CHECKING:
    from app.services.conversations.models import ConversationContext

logger = logging.getLogger(__name__)

# Approximate character budget for history (4 chars ≈ 1 token, ~400 tokens for history)
_HISTORY_CHAR_BUDGET = 1600
# Always include at least this many recent messages, even if over budget
_MIN_HISTORY_MESSAGES = 3
# Maximum number of history messages to consider (prevents scanning 500+ messages)
_MAX_HISTORY_MESSAGES = 30


class ContextBuilder:
    """
    Translates ConversationContext → LLMContext.

    Usage:
        builder = ContextBuilder()
        llm_context = builder.build(conversation_context)
    """

    def build(self, ctx: "ConversationContext") -> LLMContext:
        """
        Build an LLMContext from a ConversationContext.

        Args:
            ctx: The rich context object from Step 3A (Conversation Service).

        Returns:
            LLMContext — a clean, AI-ready context object.

        Raises:
            ContextBuildError: If required fields are missing or malformed.
        """
        try:
            return LLMContext(
                customer_name=self._get_customer_name(ctx),
                customer_channel_id=self._get_channel_id(ctx),
                channel=ctx.channel.value,
                conversation_ref=ctx.conversation_ref,
                is_new_customer=ctx.is_new_customer,
                is_new_conversation=ctx.is_new_conversation,
                ticket_status=self._get_ticket_status(ctx),
                ticket_priority=self._get_ticket_priority(ctx),
                history=self._build_history(ctx),
                current_message=self._get_current_message(ctx),
                current_message_type=ctx.incoming_message.message_type.value,
            )
        except ContextBuildError:
            raise
        except Exception as exc:
            raise ContextBuildError(
                f"Unexpected error building LLM context: {exc}"
            ) from exc

    # ─── Private Helpers ─────────────────────────────────────────────────────

    def _get_customer_name(self, ctx: "ConversationContext") -> str:
        """
        Extract customer display name with fallback chain.

        Priority: DB name → channel_customer_id → "Customer"
        We NEVER say "Unknown" to the LLM — the AI would echo it to the customer.
        """
        name = (ctx.customer.name or "").strip()
        if name and name != "__channel_customer__":
            return name
        channel_id = getattr(ctx.customer, "channel_customer_id", "") or ""
        if channel_id:
            return f"Customer ({channel_id[-4:]})"  # last 4 digits of phone for privacy
        return "Customer"

    def _get_channel_id(self, ctx: "ConversationContext") -> str:
        """Customer's identifier on the originating channel."""
        return getattr(ctx.customer, "channel_customer_id", "") or ""

    def _get_ticket_status(self, ctx: "ConversationContext") -> str:
        """Ticket status as a plain string."""
        status = ctx.ticket.status
        return status.value if hasattr(status, "value") else str(status)

    def _get_ticket_priority(self, ctx: "ConversationContext") -> str:
        """Ticket priority as a plain string."""
        priority = ctx.ticket.priority
        return priority.value if hasattr(priority, "value") else str(priority)

    def _get_current_message(self, ctx: "ConversationContext") -> str:
        """
        Extract the text content of the current incoming message.

        For non-text messages (images, audio, documents), generate a
        human-readable description so the AI knows what arrived.

        This is important because the AI cannot see the actual media file —
        it only sees text. We tell it what type of media arrived so it can
        acknowledge it appropriately.
        """
        incoming = ctx.incoming_message
        msg_type = incoming.message_type.value

        if incoming.text and incoming.text.strip():
            return incoming.text.strip()

        # Generate descriptive text for non-text messages
        descriptions = {
            "image": "📷 [Customer sent an image]",
            "audio": "🎤 [Customer sent a voice message]",
            "video": "🎬 [Customer sent a video]",
            "document": "📄 [Customer sent a document]",
            "location": "📍 [Customer shared their location]",
            "sticker": "🎭 [Customer sent a sticker]",
            "interactive": "[Customer selected an option]",
        }

        # If there's an attachment with a caption, include it
        if incoming.attachments and incoming.attachments[0].caption:
            caption = incoming.attachments[0].caption
            return f"{descriptions.get(msg_type, '[Media message]')} — Caption: {caption}"

        return descriptions.get(msg_type, f"[{msg_type} message]")

    def _build_history(self, ctx: "ConversationContext") -> list[dict]:
        """
        Build a trimmed conversation history respecting the token budget.

        Strategy:
          1. Start from the MOST RECENT messages (most contextually relevant)
          2. Walk backwards until we hit the character budget
          3. Always include at least _MIN_HISTORY_MESSAGES messages
          4. Reverse to restore chronological order for the LLM

        This "recency-first" strategy ensures the LLM always sees the most
        recent context even if the full history would exceed token limits.
        """
        # Get AI-formatted history from ConversationContext
        full_history = ctx.history_for_ai

        if not full_history:
            return []

        # Cap at maximum to prevent scanning huge histories
        candidate_messages = full_history[-_MAX_HISTORY_MESSAGES:]

        if len(candidate_messages) <= _MIN_HISTORY_MESSAGES:
            return candidate_messages

        # Walk backwards, accumulating characters
        included = []
        char_count = 0

        for msg in reversed(candidate_messages):
            msg_chars = len(msg.get("content", ""))

            # Always include minimum messages
            if len(included) < _MIN_HISTORY_MESSAGES:
                included.append(msg)
                char_count += msg_chars
                continue

            # Stop if we'd exceed the budget
            if char_count + msg_chars > _HISTORY_CHAR_BUDGET:
                break

            included.append(msg)
            char_count += msg_chars

        # Restore chronological order
        result = list(reversed(included))

        if len(result) < len(full_history):
            logger.debug(
                "History trimmed from %d to %d messages for token budget | ref=%s",
                len(full_history),
                len(result),
                ctx.conversation_ref,
            )

        return result

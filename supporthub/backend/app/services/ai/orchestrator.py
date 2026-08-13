"""
app/services/ai/orchestrator.py

The AI Orchestration Layer — coordinates the full AI response pipeline.

THIS IS THE CONDUCTOR, NOT THE PERFORMER.
  The orchestrator's job is to call each specialist in the right order.
  It does NOT:
    - Build prompts (that's prompt_builder.py)
    - Call LLMs (that's model_adapter.py)
    - Parse responses (that's response_parser.py)
    - Write to the DB (that's repository.py)

  It ONLY coordinates.

THE PIPELINE:
  1. Build LLM context (ContextBuilder)
  2. Build prompt (PromptBuilder)
  3. Call LLM (ModelAdapter)
  4. Parse response (ResponseParser)
  5. Store AI message (AIRepository)
  6. Return AIResponse

DEPENDENCY INJECTION:
  The orchestrator accepts its dependencies via constructor injection.
  This is the 'D' in SOLID — Dependency Inversion Principle.

  WHY DI MATTERS HERE:
    - Unit tests inject MockAdapter → no real API calls, no cost, instant
    - A/B tests inject different PromptBuilders to compare strategies
    - Production injects GeminiAdapter or ClaudeAdapter via get_model_adapter()

  Bad pattern (tightly coupled):
    class AIOrchestrator:
        def __init__(self):
            self.adapter = GeminiAdapter()  # hardcoded

  Good pattern (loosely coupled):
    class AIOrchestrator:
        def __init__(self, adapter: AIModelAdapter):
            self.adapter = adapter          # injected

    # Caller decides which adapter:
    orchestrator = AIOrchestrator(adapter=get_model_adapter())

ERROR HANDLING STRATEGY:
  The orchestrator catches AI errors and returns a fallback AIResponse
  rather than propagating exceptions to the webhook pipeline.

  WHY: If the AI fails, we should NOT crash the entire webhook handler.
  The customer message is already stored. The conversation is tracked.
  We should still send a graceful fallback reply to the customer.

  This is the difference between:
    "Your message could not be processed" (bad UX — customer confused)
    "Thank you, our team will reply shortly" (good UX — customer knows help is coming)
"""

from __future__ import annotations

import logging
import time
from typing import Optional, TYPE_CHECKING

from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.ai.context_builder import ContextBuilder
from app.services.ai.exceptions import (
    AIError,
    AIProviderError,
    ContextBuildError,
    PromptBuildError,
    RateLimitExceeded,
    ResponseParseError,
)
from app.services.ai.model_adapter import AIModelAdapter, get_model_adapter
from app.services.ai.models import AIResponse, ModelInfo, Prompt, TokenUsage
from app.services.ai.prompt_builder import PromptBuilder
from app.services.ai.repository import AIRepository
from app.services.ai.response_parser import ResponseParser

if TYPE_CHECKING:
    from app.services.conversations.models import ConversationContext

logger = logging.getLogger(__name__)

# Fallback response when AI completely fails
_FALLBACK_RESPONSE_TEXT = (
    "Thank you for reaching out! Our support team has received your message "
    "and will get back to you shortly."
)


class AIOrchestrator:
    """
    Coordinates the full AI response generation pipeline.

    Usage (in webhook.py):
        orchestrator = AIOrchestrator(session=session)
        ai_response = await orchestrator.generate(conversation_context)

    Usage (in tests — no real API calls):
        from app.services.ai.model_adapter import MockAdapter
        orchestrator = AIOrchestrator(session=session, adapter=MockAdapter())
        ai_response = await orchestrator.generate(conversation_context)
    """

    def __init__(
        self,
        session: AsyncSession,
        adapter: Optional[AIModelAdapter] = None,
        context_builder: Optional[ContextBuilder] = None,
        prompt_builder: Optional[PromptBuilder] = None,
        response_parser: Optional[ResponseParser] = None,
        repository: Optional[AIRepository] = None,
    ) -> None:
        self._session = session
        self._adapter = adapter or get_model_adapter()
        self._context_builder = context_builder or ContextBuilder()
        self._prompt_builder = prompt_builder or PromptBuilder()
        self._response_parser = response_parser or ResponseParser()
        self._repository = repository or AIRepository()

    async def generate_for_ticket(
        self,
        ticket: any,
        messages: list[any],
        customer: any = None,
        kb_context: Optional[str] = None,
        tone: Optional[str] = "standard",
    ) -> AIResponse:
        """
        Generate an AI response directly for a Ticket + Message list (used by agent suggested reply routes).
        """
        start_time = time.monotonic()
        try:
            llm_context = self._context_builder.build_from_ticket(
                ticket=ticket,
                messages=messages,
                customer=customer,
                kb_context=kb_context,
                tone=tone,
            )
            prompt = self._prompt_builder.build(
                llm_context=llm_context,
                model_name=self._adapter.model_name,
            )
            raw_response = await self._adapter.generate(prompt)
            latency_ms = int(raw_response.get("latency_ms", 0) or ((time.monotonic() - start_time) * 1000))
            ai_response = self._response_parser.parse(
                raw_response=raw_response,
                prompt=prompt,
                provider=self._adapter.provider_name,
                model_name=self._adapter.model_name,
                latency_ms=latency_ms,
            )
            return ai_response
        except Exception as exc:
            logger.error("AI generate_for_ticket error: %s", exc, exc_info=True)
            return self._build_fallback_response(
                adapter=self._adapter,
                error=str(exc),
                latency_ms=int((time.monotonic() - start_time) * 1000),
            )

    async def generate(self, ctx: "ConversationContext") -> AIResponse:
        """
        Run the full AI pipeline for a ConversationContext.

        ALWAYS returns an AIResponse — even if the AI fails.
        Failures result in a fallback AIResponse with error field set.

        Args:
            ctx: ConversationContext from the Conversation Service (Step 3A).

        Returns:
            AIResponse: Normalized AI response, ready for the Sender (Step 3C).
        """
        start_time = time.monotonic()

        try:
            return await self._run_pipeline(ctx)

        except (ContextBuildError, PromptBuildError) as exc:
            logger.error(
                "AI pipeline setup failed | ref=%s | stage=%s | error=%s",
                ctx.conversation_ref,
                type(exc).__name__,
                exc.message,
                exc_info=True,
            )
            return self._build_fallback_response(
                adapter=self._adapter,
                error=str(exc),
                latency_ms=int((time.monotonic() - start_time) * 1000),
            )

        except (AIProviderError, RateLimitExceeded, ResponseParseError) as exc:
            logger.error(
                "AI provider/parse failure | ref=%s | error=%s",
                ctx.conversation_ref,
                exc.message,
                exc_info=True,
            )
            return self._build_fallback_response(
                adapter=self._adapter,
                error=str(exc),
                latency_ms=int((time.monotonic() - start_time) * 1000),
            )

        except Exception as exc:
            logger.error(
                "Unexpected AI pipeline error | ref=%s | error=%s",
                ctx.conversation_ref,
                exc,
                exc_info=True,
            )
            return self._build_fallback_response(
                adapter=self._adapter,
                error=f"unexpected:{exc}",
                latency_ms=int((time.monotonic() - start_time) * 1000),
            )

    # ─── Pipeline Steps ───────────────────────────────────────────────────────

    async def _run_pipeline(self, ctx: "ConversationContext") -> AIResponse:
        """Execute the 5-step AI pipeline."""

        # ── Step 1: Build LLM context ──────────────────────────────────────
        llm_context = self._context_builder.build(ctx)
        logger.debug(
            "LLM context built | ref=%s | history_msgs=%d | msg_type=%s",
            ctx.conversation_ref,
            len(llm_context.history),
            llm_context.current_message_type,
        )

        # ── Step 2: Build prompt ────────────────────────────────────────────
        prompt = self._prompt_builder.build(
            llm_context=llm_context,
            model_name=self._adapter.model_name,
        )
        logger.debug(
            "Prompt built | version=%s | est_tokens=%d | system_hash=%s",
            prompt.version,
            prompt.estimated_input_tokens,
            prompt.system_hash,
        )

        # ── Step 3: Call LLM ────────────────────────────────────────────────
        raw_response = await self._adapter.generate(prompt)
        latency_ms = raw_response.get("latency_ms", 0)

        # ── Step 4: Parse & normalize response ─────────────────────────────
        ai_response = self._response_parser.parse(
            raw_response=raw_response,
            prompt=prompt,
            provider=self._adapter.provider_name,
            model_name=self._adapter.model_name,
            latency_ms=latency_ms,
        )

        logger.info(
            "AI response generated | ref=%s | provider=%s | model=%s | "
            "tokens=%d+%d | latency=%dms | confidence=%.2f | fallback=%s",
            ctx.conversation_ref,
            ai_response.model.provider,
            ai_response.model.model_name,
            ai_response.usage.input_tokens,
            ai_response.usage.output_tokens,
            ai_response.latency_ms,
            ai_response.confidence,
            ai_response.is_fallback,
        )

        # ── Step 5: Store AI message ────────────────────────────────────────
        await self._store_response(ctx, ai_response)

        return ai_response

    async def _store_response(
        self,
        ctx: "ConversationContext",
        ai_response: AIResponse,
    ) -> None:
        """
        Persist the AI response to the database.

        Runs inside a new implicit transaction so a storage failure doesn't
        affect the ai_response that's already been generated.
        """
        try:
            record = self._repository.build_record(
                ai_response=ai_response,
                ticket_id=str(ctx.ticket.id),
            )
            await self._repository.store(session=self._session, record=record)
            await self._session.commit()

        except Exception as exc:
            logger.error(
                "Failed to store AI message | ref=%s | error=%s",
                ctx.conversation_ref,
                exc,
                exc_info=True,
            )
            # Don't re-raise — the AI response is still valid even if storage failed.
            # The customer will still receive the reply.
            # A monitoring alert should fire here in production.

    # ─── Fallback Builder ─────────────────────────────────────────────────────

    @staticmethod
    def _build_fallback_response(
        adapter: AIModelAdapter,
        error: str,
        latency_ms: int,
    ) -> AIResponse:
        """
        Build a safe fallback AIResponse when the pipeline fails.

        This ensures the Sender (Step 3C) always has a message to send.
        The error field is set so the caller knows it's a fallback.
        """
        from app.services.ai.prompt_builder import PROMPT_VERSION
        return AIResponse(
            response_text=_FALLBACK_RESPONSE_TEXT,
            model=ModelInfo(
                provider=adapter.provider_name,
                model_name=adapter.model_name,
                prompt_version=PROMPT_VERSION,
                system_hash="fallback",
                temperature=0.0,
                max_tokens=0,
            ),
            usage=TokenUsage(input_tokens=0, output_tokens=0, total_tokens=0),
            finish_reason="error",
            latency_ms=latency_ms,
            confidence=0.0,
            error=error,
        )

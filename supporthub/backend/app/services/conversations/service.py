"""
app/services/conversations/service.py

Business Logic layer for Conversation Management.

RESPONSIBILITY:
  This layer knows WHAT to do and WHEN.
  It does NOT know HOW to execute SQL (that's repository.py).
  It does NOT know about HTTP (that's the router).

  It orchestrates this exact flow for every incoming message:

    1. IDEMPOTENCY CHECK
       Look up channel_message_id in WebhookEvent table.
       If found → raise DuplicateMessageError (return 200 immediately, no processing).
       If not   → create WebhookEvent(processed=False) as a "claim".

    2. FIND OR CREATE CUSTOMER
       Look up User by (channel, channel_customer_id).
       If found → optionally update display name.
       If not   → create new User record.

    3. FIND OR CREATE CONVERSATION
       Look up open Ticket for (customer_id, channel).
       If found → use it (customer is continuing a thread).
       If not   → create a new Ticket (new conversation).

    4. STORE INCOMING MESSAGE
       Create a Message row linked to the Ticket.
       Sets external_message_id = channel_message_id for secondary dedup.

    5. FETCH HISTORY
       Load previous messages in this ticket for AI context.

    6. ASSEMBLE ConversationContext
       Bundle everything into one object and return it.

    7. MARK WEBHOOK EVENT AS PROCESSED
       Update WebhookEvent.processed = True with processing time.

TRANSACTION SAFETY:
  Steps 1–4 happen inside a single DB transaction.
  If ANY step fails, the entire transaction rolls back.
  This means you'll never have:
    - A Customer with no Conversation
    - A Message with no Ticket
    - A WebhookEvent marked as claimed but no data stored

  This is called ATOMICITY — all-or-nothing.

  Step 5 (history fetch) and Step 7 (mark processed) run after the
  main transaction commits, as they are read-only or clean-up operations.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.channels.models import Channel, IncomingMessage
from app.services.conversations.exceptions import (
    ConversationError,
    DuplicateMessageError,
    ValidationError,
)
from app.services.conversations.models import ConversationContext
from app.services.conversations.repository import (
    ConversationRepository,
    CustomerRepository,
    MessageRepository,
    WebhookEventRepository,
)

logger = logging.getLogger(__name__)


class ConversationService:
    """
    Orchestrates the full incoming-message processing pipeline.

    Usage (from webhook.py background task):

        service = ConversationService(session)
        try:
            context = await service.process_incoming(incoming_message)
            # context is now ready for Step 3B (AI)
        except DuplicateMessageError:
            logger.info("Duplicate — already processed, skipping.")
            return
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def process_incoming(
        self,
        incoming: IncomingMessage,
    ) -> ConversationContext:
        """
        Main entry point. Processes one IncomingMessage through the full pipeline.

        Returns a ConversationContext ready for AI orchestration (Step 3B).
        Raises DuplicateMessageError if this message was already processed.
        Raises ValidationError if the message is missing required fields.
        """
        # ── Validate required fields ───────────────────────────────────────
        if not incoming.channel_message_id:
            raise ValidationError("channel_message_id", "Message ID is required for idempotency.")
        if not incoming.customer_channel_id:
            raise ValidationError("customer_channel_id", "Customer ID is required.")

        start_time = time.monotonic()
        webhook_event_id: Optional[uuid.UUID] = None

        try:
            # ── STEP 1: Idempotency check + claim ─────────────────────────
            # All DB writes happen in a single atomic transaction.
            # If anything fails, the whole transaction rolls back.
            async with self._session.begin():
                webhook_event = await self._claim_or_reject(incoming)
                webhook_event_id = webhook_event.id

                # ── STEP 2: Find or create customer ───────────────────────
                customer, is_new_customer = await self._find_or_create_customer(incoming)

                # ── STEP 3: Find or create conversation ───────────────────
                ticket, is_new_conversation = await self._find_or_create_conversation(
                    customer=customer,
                    incoming=incoming,
                )

                # ── STEP 4: Store the incoming message ────────────────────
                await MessageRepository.create_incoming(
                    session=self._session,
                    ticket=ticket,
                    customer=customer,
                    incoming=incoming,
                )

                # Touch ticket updated_at so inbox sorting is correct
                await ConversationRepository.update_last_message_at(
                    session=self._session,
                    ticket=ticket,
                )

            # Transaction committed ✓

            # ── STEP 5: Fetch conversation history ─────────────────────────
            # Read-only, runs after commit. History excludes the just-stored
            # message because AI should see prior context, not the current msg.
            history = await MessageRepository.get_history(
                session=self._session,
                ticket_id=ticket.id,
                limit=50,
            )
            # Remove the last item — it's the message we just stored (current)
            if history and history[-1].channel_message_id == incoming.channel_message_id:
                history = history[:-1]

            # ── STEP 6: Assemble ConversationContext ───────────────────────
            context = ConversationContext(
                customer=customer,
                ticket=ticket,
                incoming_message=incoming,
                history=history,
                channel=incoming.channel,
                is_new_customer=is_new_customer,
                is_new_conversation=is_new_conversation,
                webhook_event_id=webhook_event_id,
            )

            # ── STEP 7: Mark webhook event as processed ────────────────────
            processing_ms = int((time.monotonic() - start_time) * 1000)
            await self._mark_event_processed(
                webhook_event=webhook_event,
                processing_ms=processing_ms,
            )

            logger.info(
                "Conversation pipeline complete | ref=%s | customer=%s | "
                "new_customer=%s | new_conversation=%s | history_len=%d | ms=%d",
                context.conversation_ref,
                context.customer_display_name,
                is_new_customer,
                is_new_conversation,
                len(history),
                processing_ms,
            )

            return context

        except DuplicateMessageError:
            # Re-raise — caller handles this as a successful no-op
            raise

        except ConversationError:
            # Re-raise domain exceptions unchanged
            raise

        except Exception as exc:
            # Unexpected error: log with full traceback, mark event as failed
            logger.error(
                "Unexpected error in conversation pipeline | message_id=%s | error=%s",
                incoming.channel_message_id,
                exc,
                exc_info=True,
            )
            # Attempt to mark the webhook event as failed (best-effort)
            if webhook_event_id:
                try:
                    event = await WebhookEventRepository.find_by_event_id(
                        self._session, incoming.channel_message_id
                    )
                    if event:
                        await WebhookEventRepository.mark_processed(
                            self._session, event, error=str(exc)
                        )
                        await self._session.commit()
                except Exception:
                    pass  # Don't mask the original exception
            raise

    # ─── Private Helpers ─────────────────────────────────────────────────────

    async def _claim_or_reject(self, incoming: IncomingMessage):
        """
        Attempt to claim this message_id for processing.

        IDEMPOTENCY MECHANISM:
          We use a "claim then process" pattern:
            1. INSERT webhook_event(event_id=msg_id, processed=False)
               → If INSERT succeeds: we have the exclusive claim, proceed.
               → If INSERT fails (UNIQUE violation): another process already
                 claimed it → raise DuplicateMessageError.

          This handles even concurrent race conditions:
            - Two webhook retries arrive simultaneously
            - Both try to INSERT with the same event_id
            - DB UNIQUE constraint guarantees only ONE succeeds
            - The other gets IntegrityError → DuplicateMessageError → 200 OK

          This is the "optimistic locking" pattern for idempotency.
        """
        # First check if already processed (fast path)
        existing = await WebhookEventRepository.find_by_event_id(
            self._session,
            incoming.channel_message_id,
        )
        if existing:
            logger.info(
                "Duplicate webhook event detected | event_id=%s | already_processed=%s",
                incoming.channel_message_id,
                existing.processed,
            )
            raise DuplicateMessageError(
                channel_message_id=incoming.channel_message_id,
                channel=incoming.channel.value,
            )

        # Claim this message_id (INSERT with UNIQUE constraint)
        event = await WebhookEventRepository.create(
            session=self._session,
            event_id=incoming.channel_message_id,
            channel=incoming.channel,
            raw_payload=incoming.raw_payload,
        )
        logger.debug("Claimed webhook event | event_id=%s", incoming.channel_message_id)
        return event

    async def _find_or_create_customer(self, incoming: IncomingMessage):
        """
        Find existing customer or create a new one.

        Returns (customer, is_new_customer).
        If customer exists and their name changed, updates it.
        """
        customer = await CustomerRepository.find_by_channel_id(
            session=self._session,
            channel=incoming.channel,
            channel_customer_id=incoming.customer_channel_id,
        )

        if customer:
            # Update name if changed (WhatsApp users can change their profile name)
            await CustomerRepository.update_name_if_changed(
                session=self._session,
                customer=customer,
                new_name=incoming.customer_name,
            )
            logger.debug(
                "Existing customer found | id=%s | name=%s",
                customer.id,
                customer.name,
            )
            return customer, False

        # New customer — create record
        customer = await CustomerRepository.create(
            session=self._session,
            incoming=incoming,
        )
        logger.info(
            "New customer created | id=%s | channel=%s | channel_id=%s",
            customer.id,
            incoming.channel.value,
            incoming.customer_channel_id,
        )
        return customer, True

    async def _find_or_create_conversation(self, customer, incoming: IncomingMessage):
        """
        Find existing open conversation or create a new one.

        Returns (ticket, is_new_conversation).

        CONVERSATION LIFECYCLE:
          - Customer sends message → find open ticket → append to it
          - No open ticket → create new ticket (new conversation)
          - Agent resolves ticket → status = resolved
          - Customer sends ANOTHER message → new ticket (new conversation)

          This models real WhatsApp behavior: the chat thread is continuous,
          but support "conversations" are bounded by resolution events.
        """
        ticket = await ConversationRepository.find_open(
            session=self._session,
            customer_id=customer.id,
            channel=incoming.channel,
        )

        if ticket:
            logger.debug(
                "Existing open conversation found | ref=%s | status=%s",
                ticket.ref,
                ticket.status,
            )
            return ticket, False

        # No open conversation → start a new one
        ticket = await ConversationRepository.create(
            session=self._session,
            customer=customer,
            incoming=incoming,
        )
        logger.info(
            "New conversation created | ref=%s | customer_id=%s",
            ticket.ref,
            customer.id,
        )
        return ticket, True

    async def _mark_event_processed(
        self,
        webhook_event,
        processing_ms: int,
    ) -> None:
        """Mark the WebhookEvent as successfully processed."""
        try:
            await WebhookEventRepository.mark_processed(
                session=self._session,
                event=webhook_event,
                processing_ms=processing_ms,
            )
            await self._session.commit()
        except Exception as exc:
            logger.warning(
                "Failed to mark webhook event as processed | error=%s", exc
            )
            # Non-fatal: the main transaction already committed

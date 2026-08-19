"""
app/tasks/automation_tasks.py

Automation rule evaluation — runs on new tickets/messages in background.
"""

import asyncio
import logging
import uuid
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.automation_tasks.evaluate_automations", bind=True, max_retries=2)
def evaluate_automations(self, ticket_id: str, event_type: str = "ticket_created", message_body: str = None):
    """
    Evaluate all active automation rules against the given ticket asynchronously.
    """
    from app.database import AsyncSessionLocal
    from app.models import Ticket
    from app.services.automations.engine import evaluate_ticket_automations

    async def _run():
        try:
            ticket_uuid = uuid.UUID(ticket_id) if isinstance(ticket_id, str) else ticket_id
            async with AsyncSessionLocal() as session:
                ticket = await session.get(Ticket, ticket_uuid)
                if not ticket or ticket.deleted_at:
                    return
                results = await evaluate_ticket_automations(
                    session=session,
                    ticket=ticket,
                    event_type=event_type,
                    message_body=message_body,
                )
                logger.info(f"[Automation Task] Evaluated {len(results)} rules on ticket {ticket.ref}")
        except Exception as exc:
            logger.error(f"[Automation Task] Error evaluating ticket {ticket_id}: {exc}")

    asyncio.run(_run())

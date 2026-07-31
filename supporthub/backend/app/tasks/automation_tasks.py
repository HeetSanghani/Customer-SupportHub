"""Automation rule evaluation — runs on every new ticket/message."""
from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.automation_tasks.evaluate_automations", bind=True, max_retries=2)
def evaluate_automations(self, ticket_id: str):
    """
    Evaluate all active automation rules against the given ticket.
    Rules are sorted by priority (lower = evaluated first).
    Phase 12: full rule engine. For now: hardcoded behaviors.
    """
    from sqlalchemy import create_engine
    from sqlmodel import Session, select
    from app.config import get_settings
    from app.models import Ticket, Automation, TicketStatus

    settings = get_settings()
    sync_url = settings.database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
    engine = create_engine(sync_url)

    with Session(engine) as session:
        ticket = session.get(Ticket, ticket_id)
        if not ticket or ticket.deleted_at:
            return

        automations = session.exec(
            select(Automation)
            .where(Automation.is_active == True)
            .order_by(Automation.priority)
        ).all()

        for auto in automations:
            # Phase 12: parse trigger_json + action_json and evaluate
            print(f"[Automation] Evaluating '{auto.name}' on {ticket.ref}")

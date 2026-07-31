"""Notification delivery — email + in-app via Postmark."""
from __future__ import annotations

from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.notification_tasks.send_sla_breach_notification", bind=True, max_retries=3)
def send_sla_breach_notification(self, ticket_id: str):
    """Send SLA breach alert to assigned agent and manager."""
    from sqlalchemy import create_engine
    from sqlmodel import Session
    from app.config import get_settings
    from app.models import Ticket

    settings = get_settings()
    sync_url = settings.database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
    engine = create_engine(sync_url)

    with Session(engine) as session:
        ticket = session.get(Ticket, ticket_id)
        if not ticket:
            return

        # TODO: send via Postmark when email is configured
        # For now, log the notification
        print(f"[SLA BREACH] Ticket {ticket.ref} breached SLA. Agent: {ticket.agent_id}")


@celery_app.task(name="app.tasks.notification_tasks.send_csat_survey", bind=True, max_retries=3)
def send_csat_survey(self, ticket_id: str, customer_email: str, customer_name: str, ticket_ref: str):
    """Send post-resolution CSAT survey email to customer."""
    from app.config import get_settings
    settings = get_settings()

    # TODO: implement Postmark email send
    print(f"[CSAT] Survey sent to {customer_email} for {ticket_ref}")


@celery_app.task(name="app.tasks.notification_tasks.send_invite_email", bind=True, max_retries=3)
def send_invite_email(self, email: str, name: str, invite_token: str):
    """Send team invitation email with signup link."""
    from app.config import get_settings
    settings = get_settings()

    signup_url = f"{settings.frontend_url}/invite?token={invite_token}"
    print(f"[INVITE] Sending invite to {email}: {signup_url}")

"""Notification delivery — email + in-app via configured email provider."""
from __future__ import annotations

import asyncio
import logging
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.notification_tasks.send_sla_breach_notification", bind=True, max_retries=3)
def send_sla_breach_notification(self, ticket_id: str):
    """Send SLA breach alert to assigned agent and manager."""
    from sqlalchemy import create_engine
    from sqlmodel import Session
    from app.config import get_settings
    from app.models import Ticket, User
    from app.services.senders import send_email_reply

    settings = get_settings()
    sync_url = settings.database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
    engine = create_engine(sync_url)

    with Session(engine) as session:
        ticket = session.get(Ticket, ticket_id)
        if not ticket:
            return

        agent = session.get(User, ticket.agent_id) if ticket.agent_id else None
        agent_email = agent.email if agent else settings.support_contact_email
        agent_name = agent.name if agent else "Support Team"

        logger.warning(f"[SLA BREACH] Ticket {ticket.ref} breached SLA. Notifying {agent_email}")
        
        subject = f"URGENT: SLA Breach Warning for Ticket [{ticket.ref}]"
        body = (
            f"Hello {agent_name},\n\n"
            f"Ticket [{ticket.ref}] ({ticket.subject}) has exceeded its SLA threshold and requires immediate attention.\n\n"
            f"Priority: {ticket.priority}\n"
            f"Channel: {ticket.channel}\n"
            f"Status: {ticket.status}\n\n"
            f"Please review this ticket on SupportHub: {settings.frontend_url}\n"
        )
        
        if agent_email:
            try:
                asyncio.run(send_email_reply(to_email=agent_email, subject=subject, body=body, ticket_ref=ticket.ref))
            except Exception as e:
                logger.error(f"Failed to send SLA breach email: {e}")


@celery_app.task(name="app.tasks.notification_tasks.send_csat_survey", bind=True, max_retries=3)
def send_csat_survey(self, ticket_id: str, customer_email: str, customer_name: str, ticket_ref: str):
    """Send post-resolution CSAT survey email to customer."""
    from app.config import get_settings
    from app.services.senders import send_email_reply

    settings = get_settings()
    rating_url = f"{settings.backend_url}/api/v1/tickets/{ticket_id}/rate-email?rating=5"
    subject = f"How was your support experience? [{ticket_ref}]"
    body = (
        f"Hi {customer_name},\n\n"
        f"Your support ticket [{ticket_ref}] has been resolved.\n\n"
        f"We'd love to get your feedback! Please rate your experience using the link below:\n"
        f"{rating_url}\n\n"
        f"Thank you for choosing SupportHub."
    )

    logger.info(f"[CSAT] Sending survey email to {customer_email} for {ticket_ref}")
    try:
        asyncio.run(send_email_reply(to_email=customer_email, subject=subject, body=body, ticket_ref=ticket_ref))
    except Exception as e:
        logger.error(f"Failed to send CSAT email: {e}")


@celery_app.task(name="app.tasks.notification_tasks.send_invite_email", bind=True, max_retries=3)
def send_invite_email(self, email: str, name: str, invite_token: str):
    """Send team invitation email with signup link."""
    from app.config import get_settings
    from app.services.senders import send_email_reply

    settings = get_settings()
    signup_url = f"{settings.frontend_url}/register?invite={invite_token}"
    subject = "You're invited to join SupportHub"
    body = (
        f"Hello {name},\n\n"
        f"You have been invited to join the SupportHub support team.\n\n"
        f"Click the link below to set up your account and get started:\n"
        f"{signup_url}\n\n"
        f"Welcome aboard!"
    )

    logger.info(f"[INVITE] Sending team invite to {email}")
    try:
        asyncio.run(send_email_reply(to_email=email, subject=subject, body=body))
    except Exception as e:
        logger.error(f"Failed to send invite email: {e}")

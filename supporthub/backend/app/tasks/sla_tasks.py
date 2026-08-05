"""SLA breach detection — runs every 5 minutes via Celery Beat."""
from __future__ import annotations

from datetime import datetime, timezone

from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.sla_tasks.check_sla_breaches", bind=True, max_retries=3)
def check_sla_breaches(self):
    """
    Scan open tickets whose sla_due_at has passed and mark them breached.
    Triggers notification to assigned agent + manager.
    Uses a sync DB session (Celery workers are sync).
    """
    from sqlalchemy import create_engine
    from sqlmodel import Session, select, and_
    from app.config import get_settings
    from app.models import Ticket, TicketStatus

    settings = get_settings()
    # Use sync URL for Celery (replace asyncpg with psycopg2)
    sync_url = settings.database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")

    engine = create_engine(sync_url, pool_pre_ping=True)
    now = datetime.now(timezone.utc)

    with Session(engine) as session:
        stmt = select(Ticket).where(
            and_(
                Ticket.sla_due_at <= now,
                Ticket.sla_breached == False,
                Ticket.deleted_at.is_(None),
                Ticket.status.not_in([TicketStatus.resolved, TicketStatus.closed]),
            )
        )
        breached = session.exec(stmt).all()

        for ticket in breached:
            ticket.sla_breached = True
            ticket.updated_at = now
            session.add(ticket)

            # Queue notification (don't block this task)
            from app.tasks.notification_tasks import send_sla_breach_notification
            send_sla_breach_notification.delay(str(ticket.id))

        session.commit()
        return {"breached_count": len(breached), "checked_at": now.isoformat()}

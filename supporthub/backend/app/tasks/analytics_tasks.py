"""Nightly analytics rollup — pre-aggregates dashboard stats."""
from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.analytics_tasks.nightly_rollup", bind=True)
def nightly_rollup(self):
    """
    Pre-compute daily stats: tickets by channel, CSAT avg, SLA compliance,
    resolution rate, AI vs human split. Stored to a stats table (Phase 10).
    """
    from datetime import datetime, timedelta
    from sqlalchemy import create_engine, func
    from sqlmodel import Session, select
    from app.config import get_settings
    from app.models import Ticket, CsatRating, TicketStatus

    settings = get_settings()
    sync_url = settings.database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
    engine = create_engine(sync_url)
    yesterday = datetime.utcnow().date() - timedelta(days=1)

    with Session(engine) as session:
        total = session.exec(
            select(func.count(Ticket.id)).where(
                func.date(Ticket.created_at) == yesterday
            )
        ).one()
        resolved = session.exec(
            select(func.count(Ticket.id)).where(
                func.date(Ticket.created_at) == yesterday,
                Ticket.status == TicketStatus.resolved,
            )
        ).one()

        print(f"[Rollup] {yesterday}: {total} tickets, {resolved} resolved")
        # Phase 10: write to daily_stats table
        return {"date": str(yesterday), "total": total, "resolved": resolved}


@celery_app.task(name="app.tasks.automation_tasks.check_channel_health")
def check_channel_health():
    """Ping each connected channel and update status. Alert admin on failure."""
    print("[Channel Health] Checking all channel integrations...")
    # Phase 13: implement Meta API + Postmark health pings

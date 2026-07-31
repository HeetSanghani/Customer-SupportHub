"""Celery app + task definitions for SupportHub background jobs."""
from __future__ import annotations

from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "supporthub",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.tasks.sla_tasks",
        "app.tasks.analytics_tasks",
        "app.tasks.notification_tasks",
        "app.tasks.automation_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# ─── Beat Schedule ────────────────────────────────────────────────────────────
celery_app.conf.beat_schedule = {
    # Check SLA breaches every 5 minutes
    "check-sla-every-5-min": {
        "task": "app.tasks.sla_tasks.check_sla_breaches",
        "schedule": 300,  # seconds
    },
    # Nightly analytics rollup at 2:00 AM UTC
    "nightly-analytics-rollup": {
        "task": "app.tasks.analytics_tasks.nightly_rollup",
        "schedule": crontab(hour=2, minute=0),
    },
    # Channel health check every 30 minutes
    "channel-health-check": {
        "task": "app.tasks.automation_tasks.check_channel_health",
        "schedule": 1800,
    },
}

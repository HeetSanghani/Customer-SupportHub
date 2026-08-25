# Phase 17 — 30. Production Operations Playbook

## Routine Maintenance
- **Weekly**: Rotate log files, inspect PostgreSQL query execution plans.
- **Monthly**: Test database backup restore in staging environment.
- **Scaling Out**: Increase Uvicorn worker count in Docker Compose or deploy horizontal pod autoscalers (HPA) in Kubernetes.

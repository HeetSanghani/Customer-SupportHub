# Phase 17 — 31. Incident Response & Emergency Procedures

## Emergency Contacts & Playbook
1. **Severity 1 (System Down)**: Trigger PagerDuty alert; inspect container logs with `docker compose logs -f backend`.
2. **Severity 2 (AI Degradation)**: Toggle fallback switch to bypass Gemini LLM and direct all traffic to manual human agent queue.

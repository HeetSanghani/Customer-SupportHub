# Phase 17 — 29. Developer Onboarding & Architecture Learning Guide

## Setup Quickstart
1. **Clone & Setup**: `git clone ... && cd supporthub/backend`
2. **Environment**: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
3. **Database**: Start PostgreSQL with `pgvector` extension; run `alembic upgrade head`.
4. **Testing**: Execute full regression suite with `pytest`.

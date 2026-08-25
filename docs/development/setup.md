# Development Setup Guide

## Quickstart

### Prerequisites
- Python 3.13+
- Node.js 18+ & npm
- PostgreSQL 16 with `pgvector` extension
- `uv` package manager (`pip install uv`)

### Backend Setup
```bash
cd supporthub/backend
uv sync
cp .env.production.example .env
uv run python clean_and_seed.py
uv run uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd supporthub/frontend
npm install
npm run dev
```

### Running Tests
```bash
cd supporthub/backend
uv run pytest
```

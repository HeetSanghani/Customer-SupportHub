# 🚀 SupportHub — New Machine Setup Guide

This guide sets up **SupportHub** on a fresh desktop in ~10 minutes. The database dump (`supporthub_dump.sql`) is committed to this repo so you get all users, tickets, KB articles, and settings automatically.

---

## 📋 Prerequisites

Install these tools on the new machine before starting:

| Tool | Install | Notes |
|---|---|---|
| **Git** | `sudo apt install git` | To clone the repo |
| **Docker & Docker Compose** | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) | Runs Postgres & Redis |
| **uv** (Python runner) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | Runs FastAPI backend |
| **Node.js v18+** | [nodejs.org](https://nodejs.org/) | Runs React frontend |
| **ngrok** | `sudo snap install ngrok` | Exposes backend to webhooks |

---

## 🗂️ 1. Clone the Repository

```bash
git clone <your-github-repo-url>
cd Customer-SupportHub
```

> After cloning you will already have `supporthub_dump.sql` — **no manual database transfer needed**.

---

## 🔐 2. Set Up Environment Variables

The `.env` file contains API keys and is **not committed to Git** (for security). Copy the template and fill in your credentials:

```bash
cd supporthub/backend
cp .env.example .env
```

Then open `.env` and fill in:

```env
# ─── Required for core functionality ───────────────────
DATABASE_URL=postgresql+asyncpg://supporthub:supporthub_dev@localhost:5433/supporthub
REDIS_URL=redis://localhost:6381/0
SECRET_KEY=your_random_secret_key_here   # generate with: openssl rand -hex 32

# ─── AI (Gemini) ───────────────────────────────────────
GEMINI_API_KEY=your_gemini_api_key_here

# ─── Email (Mailgun) ───────────────────────────────────
MAILGUN_DOMAIN=your_mailgun_domain
MAILGUN_API_KEY=your_mailgun_api_key

# ─── Optional (WhatsApp / Instagram / Facebook) ────────
META_APP_ID=
META_APP_SECRET=
META_VERIFY_TOKEN=your_webhook_verify_token
WHATSAPP_PHONE_ID=
```

> 💡 All other values can stay as their defaults for local development.

---

## 🐳 3. Start Docker Infrastructure

This starts the PostgreSQL database (with pgvector) and Redis cache:

```bash
cd supporthub
docker compose up -d db redis
```

Verify containers are running and healthy:
```bash
docker ps
# You should see: supporthub_db (pgvector:pg16) and supporthub_redis (redis:7-alpine)
```

---

## 💾 4. Restore Database from Dump

Restore all database tables, users, orders, products, vector embeddings, and tickets with one command:

```bash
# From the project root (Customer-SupportHub/)
./scripts/restore_db.sh
```

*(Alternatively, via manual docker command:)*
```bash
cat supporthub_dump.sql | docker exec -i supporthub_db psql -U supporthub -d supporthub
```

> ✅ This restores:
> - Full e-commerce catalog (products, categories, sellers, orders, shipments, returns)
> - Staff & customer accounts (Admin, Manager, Agent, Customer)
> - Knowledge Base articles with 59 pre-computed pgvector embeddings
> - Omnichannel tickets, message threads, automations, and canned responses

---

## ✅ 5. Start All Services

Open **4 separate terminals** and run one command in each:

### Terminal 1 — Backend API
```bash
cd supporthub/backend
uv run uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend Dev Server
```bash
cd supporthub/frontend
npm install        # only needed on first run
npm run dev
```

### Terminal 3 — ngrok Tunnel (for Email/WhatsApp Webhooks)
```bash
ngrok config add-authtoken <your_ngrok_authtoken>   # first time only
ngrok http 8000
```

> After ngrok starts, copy the `https://xxxx.ngrok.io` URL and update:
> - **Mailgun**: Receiving → Routes → Destination → `https://xxxx.ngrok.io/api/v1/webhooks/email`
> - **Meta Console**: Webhooks → Callback URL → `https://xxxx.ngrok.io/api/v1/webhooks/whatsapp`

---

## 🔑 6. Login Credentials

Once running, open **http://localhost:5173** in your browser:

| Role | Email | Password |
|---|---|---|
| 👤 Customer | `customer@supporthub.com` | `Password123!` |
| 🎧 Agent | `agent@supporthub.com` | `Password123!` |
| 📊 Manager | `manager@supporthub.com` | `Password123!` |
| ⚙️ Admin | `admin@supporthub.com` | `Password123!` |

---

## 🔄 7. Creating a New Database Dump (Before Pushing to GitHub)

Whenever you make changes to database records or schema and want to commit them to Git:

```bash
# From the project root
./scripts/dump_db.sh
git add supporthub_dump.sql
git commit -m "chore: update database dump"
git push origin main
```

---

## 🆘 Troubleshooting

| Issue | Fix |
|---|---|
| `docker compose up` fails | Make sure Docker Desktop is running |
| `psql: error: connection refused` | Wait 10s for the DB container to be healthy, then retry |
| `npm run dev` fails | Run `npm install` first inside `supporthub/frontend/` |
| `uv: command not found` | Run `curl -LsSf https://astral.sh/uv/install.sh \| sh` and re-open terminal |
| Backend 500 errors | Check `.env` file exists and `ANTHROPIC_API_KEY` is set |

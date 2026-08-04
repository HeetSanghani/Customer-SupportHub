# 🚀 SupportHub - New Machine Setup Guide

This guide walks you through setting up **SupportHub** on a fresh/new desktop machine. Since Git only syncs source code — not secrets (`.env`), database state, Docker volumes, or ngrok tunnels — follow these instructions step-by-step.

---

## 📥 1. Clone & Initial Setup

**1. Clone the repository:**
```bash
git clone <your-repository-url>
cd "ai powered customer"
```

**2. Verify folder structure:**
```
.
├── supporthub/
│   ├── backend/       # FastAPI application
│   ├── frontend/      # React + Vite dashboard
│   └── docker-compose.yml
└── test.md
```

---

## 🔐 2. Environment Variables (.env)

> ⚠️ **IMPORTANT**: `.env` files contain sensitive API keys and database credentials. They are intentionally excluded from Git control and **must NEVER be committed to GitHub**.

To set up environment variables on the new machine:

### Option A: Direct Copy from Old Machine (Recommended)
Transfer your existing `.env` file via USB flash drive, a secure secret manager (1Password, Bitwarden), or SSH/SCP:

```bash
# Example SSH/SCP command from your new machine:
scp user@old-machine-ip:"/path/to/supporthub/backend/.env" ./supporthub/backend/.env
```

### Option B: Create from `.env.example`
Copy the template file in the backend directory and manually populate your API keys:

```bash
cd supporthub/backend
cp .env.example .env
# Open .env and fill in your real credentials (OPENAI_API_KEY, MAILGUN_API_KEY, etc.)
```

---

## 🐳 3. Docker & Database Setup

When running Docker on a new machine, `docker compose up -d` initializes a **FRESH, EMPTY PostgreSQL database** because Docker volumes do not transfer via Git.

**Start Docker containers:**
```bash
cd supporthub
docker compose up -d
```

Choose one of the following two paths to populate data:

### Option A: Fresh Start (Seed Data)
Run the seed scripts to populate database tables with initial system configurations, demo accounts, tickets, and CSAT records:

```bash
cd supporthub/backend
uv run python seed_db.py
uv run python seed_admin.py
uv run python seed_tickets_csat.py
```

### Option B: Migrate Existing Database Data
To transfer all existing tickets, users, and customer messages from your old machine:

**1. On your OLD machine (Export PostgreSQL dump):**
```bash
docker exec -t supporthub-db pg_dump -U supporthub -d supporthub > supporthub_dump.sql
```

**2. Transfer `supporthub_dump.sql` to your NEW machine** (via SCP, USB, etc.).

**3. On your NEW machine (Import dump):**
Using default credentials from `DATABASE_URL` (`postgresql+asyncpg://supporthub:supporthub_dev@localhost:5433/supporthub`):
```bash
cat supporthub_dump.sql | docker exec -i supporthub-db psql -U supporthub -d supporthub
```

---

## 🌐 4. ngrok Setup & Webhook Re-configuration

External webhook services (Mailgun, Meta WhatsApp/Messenger) cannot send requests directly to `localhost`. You must use `ngrok` to expose backend port `8001`.

**1. Install & Authenticate ngrok on New Machine:**
```bash
# Ubuntu/Linux Snap:
sudo snap install ngrok

# Authenticate with your existing ngrok token (works across multiple machines):
ngrok config add-authtoken <your_ngrok_authtoken>
```

**2. Start ngrok Tunnel:**
```bash
ngrok http 8001
```

**3. Update Webhook URLs:**
Because free ngrok accounts generate a **NEW random domain** on every restart, update your callback URLs in external dashboards:

- **Mailgun**: Go to **Receiving → Routes → Destination** field:
  `POST https://<new-ngrok-url>/api/v1/webhooks/email`
- **Meta Developer Console**: Go to **Webhooks → Callback URL**:
  `GET/POST https://<new-ngrok-url>/api/v1/webhooks/whatsapp`
  `GET/POST https://<new-ngrok-url>/api/v1/webhooks/messenger`

---

## ✅ 5. Full Step-by-Step Checklist

Follow these steps in order when setting up a fresh desktop:

1. **Clone Repo**:
   ```bash
   git clone <repo-url> && cd "ai powered customer"
   ```
2. **Set Up `.env`**:
   ```bash
   cp supporthub/backend/.env.example supporthub/backend/.env
   # Add your real API keys inside supporthub/backend/.env
   ```
3. **Start Infrastructure Containers (Terminal 1)**:
   ```bash
   cd supporthub && docker compose up -d
   ```
4. **Seed Database**:
   ```bash
   cd supporthub/backend
   uv run python seed_db.py
   uv run python seed_admin.py
   uv run python seed_tickets_csat.py
   ```
5. **Start Backend Server (Terminal 2)**:
   ```bash
   cd supporthub/backend
   uv run uvicorn app.main:app --reload --port 8001
   ```
6. **Start Frontend Dev Server (Terminal 3)**:
   ```bash
   cd supporthub/frontend
   npm install
   npm run dev
   ```
7. **Start ngrok Tunnel (Terminal 4)**:
   ```bash
   ngrok http 8001
   ```
8. **Update Webhook Provider Dashboards**:
   Copy the new ngrok HTTPS URL to Mailgun Routes & Meta Webhook callback configuration.

# SupportHub — AI Omnichannel Customer Support Platform

> Full-stack production application: FastAPI backend + React frontend + PostgreSQL + Redis + Celery + WhatsApp Cloud API

---

## 💻 Quick Start (Local Dev)

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.12+ with `uv`

---

### Terminal 1 — Start Database & Redis
```bash
cd supporthub
docker compose up -d
```

### Terminal 2 — Start Backend (FastAPI)
```bash
cd supporthub/backend
uv run uvicorn app.main:app --reload --port 8001
```

> API docs: `http://localhost:8001/api/docs`

### Terminal 3 — Start Frontend (React)
```bash
cd supporthub/frontend
npm run dev
```

> App: `http://localhost:5173`

---

## 📲 WhatsApp Cloud API Setup Guide

To connect live WhatsApp messaging to SupportHub:

1. **Get Meta Credentials**:
   - Go to [Meta for Developers](https://developers.facebook.com/) → **WhatsApp → API Setup**.
   - Copy **Phone Number ID** and **Access Token**.

2. **Configure `.env`** (`supporthub/backend/.env`):
   ```env
   WHATSAPP_PHONE_ID=1296854793505632
   WHATSAPP_ACCESS_TOKEN=your_token_here
   WHATSAPP_VERIFY_TOKEN=supporthub_webhook_verify_token_2026
   ```

3. **Start Webhook Tunnel**:
   ```bash
   ngrok http 8001
   ```

4. **Register Webhook in Meta Dashboard**:
   - **Callback URL**: `https://<ngrok-domain>.ngrok-free.app/api/v1/webhooks/whatsapp`
   - **Verify Token**: `supporthub_webhook_verify_token_2026`
   - Subscribe to **`messages`** under Webhook Fields.

5. **Features Built & Verified**:
   - ✅ Real-time inbound webhook handling & customer auto-creation.
   - ✅ Gemini RAG AI automated response generation & live WhatsApp outbound delivery.
   - ✅ AI-powered dynamic topic subject generation (3–6 word titles).
   - ✅ Auto-resolution intent detection (*"close this chat"*, *"thanks, that fixed it"* $\rightarrow$ `status: resolved`).
   - ✅ Instant WebSocket sync across agent inboxes.

---

## 📁 Project Structure

```
supporthub/
├── backend/         FastAPI + SQLModel + Celery + Meta WhatsApp Service
├── frontend/        React + Vite + TypeScript + Tailwind
├── docker-compose.yml  PostgreSQL 16 (pgvector) + Redis 7
└── .github/workflows/  CI pipelines
```

---

## 🔑 Demo Account Credentials

Password for all accounts: `Password123!`

- **Admin**: `admin@supporthub.com`
- **Manager**: `manager@supporthub.com`
- **Agent**: `agent@supporthub.com`
- **Customer**: `customer@supporthub.com`

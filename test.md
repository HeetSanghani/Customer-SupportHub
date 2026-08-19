# 🚀 SupportHub Testing & Verification Guide

This document outlines how to run automated unit/integration test suites as well as manually test Omnichannel integrations (WhatsApp, Instagram, Facebook Messenger, Email, Live Chat) and AI features of SupportHub.

---

## 🧪 1. Running Automated Tests

SupportHub includes a consolidated **pytest** suite with 70 passing tests covering all core systems:

```bash
cd supporthub/backend
uv run pytest
```

To run tests with detailed output:
```bash
uv run pytest -v
```

To run a specific test suite:
```bash
uv run pytest tests/test_whatsapp_parser.py
uv run pytest tests/test_conversations.py
uv run pytest tests/test_ai_orchestrator.py
uv run pytest tests/test_automations.py
```

---

## 💻 2. How to Run the Project Locally

**1. Start Database & Redis (Docker)**
```bash
cd supporthub
docker compose up -d
```

**2. Start Backend API (FastAPI)**
```bash
cd supporthub/backend
uv run uvicorn app.main:app --reload --port 8001
```

**3. Start Frontend Dashboard (React / Vite)**
```bash
cd supporthub/frontend
npm run dev
```

**4. Start Webhook Tunnel (ngrok)**
```bash
ngrok http 8001
```

---

## 🌐 3. Webhook Testing URLs

If you are running `ngrok http 8001` locally, configure these URLs in your provider dashboards:

- **WhatsApp Webhook URL**: `GET/POST {ngrok_url}/api/v1/webhooks/whatsapp`
- **Instagram Webhook URL**: `GET/POST {ngrok_url}/api/v1/webhooks/instagram`
- **Facebook Messenger Webhook URL**: `GET/POST {ngrok_url}/api/v1/webhooks/messenger`
- **Mailgun Email Webhook URL**: `POST {ngrok_url}/api/v1/webhooks/email`
- **ngrok Local Web Inspector**: `http://127.0.0.1:4040` (Inspect & replay incoming webhook payloads live)

---

## 📲 4. End-to-End Live Testing

### 1. WhatsApp Testing
1. Send a WhatsApp message from your personal phone to your Meta Test Number.
2. The incoming message triggers:
   - Automated Customer & Ticket creation in SupportHub.
   - Dynamic AI Subject Generation.
   - Live WebSocket updates to the Agent Unified Inbox.
3. If you reply *"close this chat"* or *"thanks, that fixed it"* as the customer, the AI will automatically:
   - Mark the ticket as `resolved` (`ai_resolved = true`).
   - Push a real-time CSAT Survey message back to your WhatsApp app!

### 2. Email Testing (Mailgun)
1. Send an email to your Mailgun Sandbox Inbound Address (e.g., `test@sandbox...mailgun.org`).
2. Go to the Agent Dashboard in SupportHub and reply to the newly created ticket.
3. Mark the ticket as **Resolved**.
4. You should receive a final email with a 1-5 star HTML CSAT Survey. Clicking a star will record the rating in the system.

### 3. Instagram & Facebook Messenger Testing
1. Send a Direct Message to the connected Instagram or Facebook test page.
2. The message will appear instantly in the Agent Inbox with avatar and thread continuity.
3. The AI assistant can automatically reply or suggest replies to the agent based on Knowledge Base RAG.

---

## 🔗 5. Useful Dashboard URLs

- **Frontend Dashboard** : `http://localhost:5173`
- **Backend API Base** : `http://localhost:8001`
- **Swagger API Docs** : `http://localhost:8001/api/docs`
- **ngrok Local Web Inspector** : `http://127.0.0.1:4040`

---

## 🔑 6. Test Accounts

Password for all accounts : `Password123!`

- **Admin Email** : `admin@supporthub.com`
- **Manager Email** : `manager@supporthub.com`
- **Agent Email** : `agent@supporthub.com`
- **Customer Email** : `customer@supporthub.com`

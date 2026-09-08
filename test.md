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
uv run uvicorn app.main:app --reload --port 8000
```

**3. Start Frontend Dashboard (React / Vite)**
```bash
cd supporthub/frontend
npm run dev
```

**4. Start Webhook Tunnel (ngrok)**
```bash
ngrok http 8000
```

**5. Start Database Explorer UI (Port 8090)**
```bash
fuser -k 8090/tcp 2>/dev/null; sleep 1; cd supporthub/backend && uv run python ../../db_explorer.py
```

---

## 🌐 3. Webhook Testing URLs

If you are running `ngrok http 8000` locally, configure these URLs in your provider dashboards:

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
- **Backend API Base** : `http://localhost:8000`
- **Swagger API Docs** : `http://localhost:8000/api/docs`
- **Database Explorer UI** : `http://localhost:8090`
- **ngrok Local Web Inspector** : `http://127.0.0.1:4040`

---

## 🔑 6. Test Accounts

Default password for all accounts : `Password123!`

| Name | Email | Role | Customer ID | Phone | Status |
| --- | --- | --- | --- | --- | --- |
| **Admin User** | `admin@supporthub.com` | `admin` | N/A | `+1 (555) 010-0001` | Active |
| **Manager User** | `manager@supporthub.com` | `manager` | N/A | `+1 (555) 010-0003` | Active |
| **Agent User** | `agent@supporthub.com` | `agent` | N/A | `+1 (555) 010-0005` | Active |
| **Aarav Sharma** | `customer@supporthub.com` | `customer` | `CUST-001` | `+91-9876543210` | Active |
| **Sarah Johnson** | `sarah.j@example.com` | `customer` | `CUST-002` | `+1 (555) 234-5678` | Active |
| **Rohan Verma** | `rohan.verma@example.com` | `customer` | `CUST-003` | `+91-9811234567` | Active |
| **Ananya Reddy** | `ananya.reddy@example.com` | `customer` | `CUST-004` | `+91-9440123456` | Active |
| **Vikram Iyer** | `vikram.iyer@example.com` | `customer` | `CUST-005` | `+91-9840123456` | Active |
| **Sneha Kulkarni** | `sneha.kulkarni@example.com` | `customer` | `CUST-006` | `+91-9764123456` | Active |
| **Rajesh Banerjee** | `rajesh.banerjee@example.com` | `customer` | `CUST-007` | `+91-9830123456` | Active |
| **Kavita Deshmukh** | `kavita.deshmukh@example.com` | `customer` | `CUST-008` | `+91-9822123456` | Active |
| **Aditya Nair** | `aditya.nair@example.com` | `customer` | `CUST-009` | `+91-9847123456` | Active |
| **Neha Gupta** | `neha.gupta@example.com` | `customer` | `CUST-010` | `+91-9810123456` | Active |
| **Siddharth Choudhury** | `siddharth.c@example.com` | `customer` | `CUST-011` | `+91-9435123456` | Active |
| **Pooja Joshi** | `pooja.joshi@example.com` | `customer` | `CUST-012` | `+91-9414123456` | Active |
| **Manish Tiwari** | `manish.tiwari@example.com` | `customer` | `CUST-013` | `+91-9450123456` | Active |
| **Deepika Rao** | `deepika.rao@example.com` | `customer` | `CUST-014` | `+91-9844123456` | Active |
| **Karan Mehta** | `karan.mehta@example.com` | `customer` | `CUST-015` | `+91-9879123456` | Active |
| **Meera Menon** | `meera.menon@example.com` | `customer` | `CUST-016` | `+91-9846123456` | Active |
| **Arjun Kapoor** | `arjun.kapoor@example.com` | `customer` | `CUST-017` | `+91-9818123456` | Active |
| **Ritu Agarwal** | `ritu.agarwal@example.com` | `customer` | `CUST-018` | `+91-9331123456` | Active |
| **Amit Singhania** | `amit.singhania@example.com` | `customer` | `CUST-019` | `+91-9826123456` | Active |
| **Shweta Bhatia** | `shweta.bhatia@example.com` | `customer` | `CUST-020` | `+91-9814123456` | Active |
| **Rahul Dravid** | `rahul.d@example.com` | `customer` | `CUST-021` | `+91-9880123456` | Active |
| **Divya Srivastava** | `divya.sri@example.com` | `customer` | `CUST-022` | `+91-9415123456` | Active |
| **Gaurav Saxena** | `gaurav.saxena@example.com` | `customer` | `CUST-023` | `+91-9829123456` | Active |
| **Suresh Pandey** | `suresh.pandey@example.com` | `customer` | `CUST-024` | `+91-9871123456` | Active |
| **Tanya Malhotra** | `tanya.malhotra@example.com` | `customer` | `CUST-025` | `+91-9811987654` | Active |


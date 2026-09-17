# 🚀 SupportHub — Enterprise AI Omnichannel Customer Support Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg?style=flat&logo=React&logoColor=black)](https://reactjs.org)
[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF.svg?style=flat&logo=Vite&logoColor=white)](https://vitejs.dev)
[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-3776AB.svg?style=flat&logo=Python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1.svg?style=flat&logo=PostgreSQL&logoColor=white)](https://www.postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7+-DC382D.svg?style=flat&logo=Redis&logoColor=white)](https://redis.io)
[![Tests](https://img.shields.io/badge/Tests-687%20Passing-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org)

**SupportHub** is a production-grade, AI-first omnichannel customer support platform designed for modern enterprise workflows. It connects all customer touchpoints (**WhatsApp Cloud API, Instagram Direct, Facebook Messenger, Inbound/Outbound Email via Mailgun, and Website Live Chat**) into a unified, real-time agent dashboard powered by advanced multi-model AI reasoning.

---

## 🌟 Key Platform Features

### 1. 🤖 Advanced Multi-Model AI Orchestration
- **Multi-Provider Adapter Engine**: Seamlessly switch or fallback between **Google Gemini (2.5 Flash / Flash Lite)**, **Anthropic Claude (Sonnet / Haiku)**, and **OpenAI (GPT-4o)** with zero code changes.
- **Vision OCR & Image Reasoning**: Ingest customer screenshots, invoices, and damaged product photos directly from WhatsApp, Instagram, or Email attachments and extract relevant text and context automatically.
- **RAG Knowledge Base**: Semantic knowledge base retrieval with pgvector that injects accurate company policies, shipping rules, and troubleshooting procedures directly into LLM prompts.
- **Smart Debouncing System**: Automatically batches rapid-fire user messages within configurable debounce windows (e.g., 5 seconds) to prevent redundant AI API calls and disjointed responses.
- **Dynamic Subject & Category Generation**: Analyzes inbound customer conversation context to generate crisp ticket subjects and classify urgency/category in real time.
- **Automated Resolution Intent Detection**: Recognizes when customer queries are successfully answered (e.g., *"Thanks, that fixed it!"*) and initiates auto-closure flows.

### 2. 📲 True Omnichannel Inboxes
- **WhatsApp Cloud API**: Full support for rich text, media attachments (images, PDFs, voice notes), interactive quick reply buttons, and webhook delivery status tracking (`sent`, `delivered`, `read`).
- **Instagram Direct Messages**: Two-way messaging integration with avatar synchronization, attachment rendering, and direct agent reply triggers.
- **Facebook Messenger**: Webhook processing with thread continuity, customer profile mapping, and outbound message dispatch.
- **Email Inbound & Outbound (Mailgun)**: Ingests inbound MIME emails, preserves HTML/plain-text threads, extracts attachments, and sends outbound email responses with DKIM/SPF compliance.
- **Website Live Chat**: Low-latency customer live chat widget powered by persistent WebSockets and instant AI co-pilot replies.

### 3. ⚡ Real-Time WebSocket Infrastructure
- **Connection Management**: Robust connection lifecycle manager preventing memory leaks and stale connection handles.
- **Broadcast Isolation**: Pub/sub event broadcasting scoped to specific ticket threads and global agent inbox queues.
- **Live Typing & Status Sync**: Instant sync for ticket assignment, priority changes, internal agent notes, and new incoming messages.

### 4. 🛠️ Workflow Automation Engine
- **Visual Rule Builder**: Create triggers (e.g., *On Ticket Created*, *On Message Received*), condition logic (channel, priority, sentiment, keywords), and automated actions (*Assign to Team*, *Send Macro Reply*, *Change Priority*, *Tag Ticket*).
- **Dry-Run Simulation**: Test and dry-run automation rules against historical tickets before enabling them in production.

### 5. ⭐ Real-Time CSAT & Analytics
- **Multi-Channel CSAT Delivery**: Dispatches 1-5 star interactive satisfaction surveys to customers across WhatsApp interactive buttons, email links, and in-chat ratings upon ticket resolution.
- **Executive Analytics Dashboard**: Real-time metrics for First Response Time (FRT), Mean Time to Resolution (MTTR), CSAT distribution, channel volume breakdowns, and AI deflection rates.

---

## 🏛️ System Architecture

```
                       ┌─────────────────────────────────────────────────────────┐
                       │                   Customer Channels                     │
                       │  WhatsApp · Instagram · Messenger · Email · Live Chat   │
                       └────────────────────────────┬────────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                FastAPI Backend Service                                 │
│                                                                                        │
│  ┌───────────────────────┐   ┌───────────────────────┐   ┌──────────────────────────┐  │
│  │   Webhook Handlers    │──▶│  Conversation Engine  │──▶│    AI Orchestrator       │  │
│  │ (Meta, Mailgun, Chat) │   │ (Deduplication, Match)│   │(Context + Prompt + Vision│  │
│  └───────────────────────┘   └───────────────────────┘   └─────────────┬────────────┘  │
│                                                                        │               │
│  ┌───────────────────────┐   ┌───────────────────────┐                 │               │
│  │  Automations Engine   │   │  CSAT Delivery Layer  │◀────────────────┘               │
│  │ (Triggers & Actions)  │   │  (Multi-Channel Push) │                                 │
│  └───────────────────────┘   └───────────────────────┘                                 │
│                                                                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                     WebSocket Hub & Real-Time Connection Manager                 │  │
│  └────────────────────────────────────────┬─────────────────────────────────────────┘  │
└───────────────────────────────────────────┼────────────────────────────────────────────┘
                                            │
                                            ▼
                       ┌─────────────────────────────────────────┐
                       │         React Agent Dashboard           │
                       │  Unified Inbox · Live Chat · Analytics  │
                       └─────────────────────────────────────────┘
```

---

## 💻 Tech Stack

- **Backend**: Python 3.12 / 3.13, FastAPI, SQLModel (Async SQLAlchemy ORM), Pydantic v2, Uvicorn, AnyIO, LangGraph.
- **Frontend**: React 18, Vite 6, Tailwind CSS v4, Lucide Icons, Zustand, React Router v7, TanStack Query.
- **Database & Cache**: PostgreSQL 16 + pgvector (Relational Data + Vector Search), Redis 7 (Pub/Sub & Caching, Celery broker).
- **AI & LLM Services**: Google Gemini API (`google-generativeai`), Anthropic Claude SDK, OpenAI SDK.
- **Testing & Tooling**: Pytest, Pytest-Asyncio, Ruff, uv (Python package manager).

---

## 🏁 Quick Start & Local Setup

### 1. Prerequisites
- **Git** (`sudo apt install git`)
- **Docker & Docker Compose** ([Docker Engine](https://docs.docker.com/engine/install/))
- **uv** Python package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Node.js v18+ & npm** ([NodeJS](https://nodejs.org))
- **ngrok** (for local webhook forwarding: `sudo snap install ngrok` or via brew/choco)

---

### 2. Clone the Repository
```bash
git clone https://github.com/heet-brainerhub/Customer-SupportHub.git
cd Customer-SupportHub
```

---

### 3. Configure Environment Variables
Copy `.env.example` to `.env` inside `supporthub/backend/`:
```bash
cd supporthub/backend
cp .env.example .env
```

Edit `supporthub/backend/.env` with your API keys:
```env
# Database & Redis (matches docker-compose.yml defaults)
DATABASE_URL=postgresql+asyncpg://supporthub:supporthub_dev@localhost:5433/supporthub
REDIS_URL=redis://localhost:6381/0
SECRET_KEY=generate_with_openssl_rand_hex_32

# AI Models (Gemini — primary, Claude / OpenAI — optional fallback)
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here   # optional

# Email Inbound / Outbound (Mailgun)
MAILGUN_DOMAIN=your_domain.mailgun.org
MAILGUN_API_KEY=your_mailgun_api_key

# Meta Omnichannel (WhatsApp / Instagram / Facebook)
META_APP_ID=your_meta_app_id
META_APP_SECRET=your_meta_app_secret
META_VERIFY_TOKEN=your_webhook_verification_token
WHATSAPP_PHONE_ID=your_whatsapp_phone_id
PAGE_ACCESS_TOKEN=your_page_access_token
```

---

### 4. Start Infrastructure (Postgres & Redis)
```bash
cd supporthub
docker compose up -d db redis
```

Verify containers are running:
```bash
docker ps
# Expected: supporthub_db (port 5433) and supporthub_redis (port 6381)
```

---

### 5. Restore Database with Demo Data
Instantly load all users, tickets, KB articles, orders, and settings:
```bash
# From the project root:
./scripts/restore_db.sh
```

Or manually:
```bash
cat supporthub_dump.sql | docker exec -i supporthub_db psql -U supporthub -d supporthub
```

Alternatively, run a fresh programmatic seed:
```bash
cd supporthub/backend
uv run python clean_and_seed.py
```

---

### 6. Run the Application

Open **3 terminal windows**:

#### Terminal 1 — FastAPI Backend
```bash
cd supporthub/backend
uv run uvicorn app.main:app --reload --port 8000
```
*API Swagger docs: `http://localhost:8000/api/docs`*

#### Terminal 2 — React Frontend
```bash
cd supporthub/frontend
npm install
npm run dev
```
*App UI: `http://localhost:5173`*

#### Terminal 3 — ngrok Webhook Tunnel
```bash
ngrok http 8000
```
*Forward your ngrok HTTPS URL to Meta and Mailgun webhooks.*

---

## 🔑 Default Login Credentials

All seeded demo accounts use the password: `Password123!`

| Role | Email | Permissions / Features |
|---|---|---|
| 👑 **Admin** | `admin@supporthub.com` | Channel Integrations, Team Management, Global Config |
| 📊 **Manager** | `manager@supporthub.com` | Workflow Automations, Analytics Dashboard, SLA Audits |
| 🎧 **Agent** | `agent@supporthub.com` | Omnichannel Inboxes, AI Co-Pilot, Internal Notes |
| 👤 **Customer** | `customer@supporthub.com` | Customer Live Chat & Ticket Portal |

---

## 🧪 Testing & Quality Assurance

The project includes a comprehensive automated test suite with **687 tests** covering AI orchestration, parser logic, webhook idempotency, rate limiting, customer journey flows, security hardening, WebSocket events, and end-to-end conversation lifecycles:

```bash
cd supporthub/backend
uv run pytest
```

Key test modules:

```
tests/
├── ai/
│   ├── test_catalog_and_category_search.py    # Product search & catalog AI
│   ├── test_escalation.py                     # AI escalation logic
│   └── test_resolution_intent.py              # Resolution intent detection
├── phase13/                                   # Phase 13 feature tests
├── test_ai_orchestrator.py                    # Multi-model orchestration
├── test_automations.py                        # Workflow automation rules
├── test_conversations.py                      # Ticket matching & dedup
├── test_copilot_hitl.py                       # Human-in-the-loop AI co-pilot
├── test_instagram_ai.py                       # Instagram AI handling
├── test_instagram_client.py                   # Instagram Graph API client
├── test_instagram_webhook.py                  # Instagram webhook processing
├── test_live_chat_ai_e2e.py                   # Live chat AI end-to-end
├── test_messenger_webhook.py                  # Facebook Messenger webhook
├── test_phase12_6_remediation.py              # Phase 12 security remediation
├── test_phase12_security.py                   # Security & auth hardening
├── test_phase15_1_hardening.py               # Platform hardening tests
├── test_phase15_2_customer_journey.py         # Full customer journey e2e
├── test_phase15_3_profile_orders.py           # Profile & order management
├── test_phase15_4_customer_account_transactions.py  # Transactions e2e
├── test_phase15_5_support_conversation_lifecycle.py # Support lifecycle e2e
├── test_websocket.py                          # WebSocket connection manager
├── test_whatsapp_outbound.py                  # WhatsApp outbound messaging
└── test_whatsapp_parser.py                    # WhatsApp message parser
```

To build and validate the frontend production bundle:
```bash
cd supporthub/frontend
npm run build
```

---

## 📡 Webhook Integration Endpoints

Configure the following endpoints on your external provider dashboards:

| Provider | Endpoint URL | Description |
|---|---|---|
| **WhatsApp Cloud API** | `/api/v1/webhooks/whatsapp` | Inbound customer messages & delivery status updates |
| **Instagram Messaging**| `/api/v1/webhooks/instagram`| Inbound Instagram Direct Messages & story replies |
| **Facebook Messenger** | `/api/v1/webhooks/messenger`| Inbound Facebook Page messages |
| **Mailgun Inbound**    | `/api/v1/webhooks/email`    | Inbound customer emails and thread replies |
| **Live Chat WebSocket**| `/ws/chat/{ticket_id}`      | Real-time bi-directional agent/customer live chat |

---

## 📂 Project Directory Structure

```
Customer-SupportHub/
├── supporthub/
│   ├── docker-compose.yml              # PostgreSQL, Redis, Nginx containers
│   ├── nginx.conf                      # Nginx reverse proxy config
│   ├── backend/
│   │   ├── pyproject.toml              # Python dependencies & pytest configuration
│   │   ├── alembic/                    # Database migration scripts
│   │   ├── clean_and_seed.py           # Database purge & full seed script
│   │   ├── restore_real_data.py        # Real sample customer dataset restore
│   │   ├── restore_seed_customers.py   # Customer seed script
│   │   ├── seed_admin.py               # Admin user seeder
│   │   ├── tests/                      # Pytest suite (687 tests)
│   │   │   ├── ai/                     # AI-specific tests
│   │   │   ├── phase13/                # Phase 13 feature tests
│   │   │   ├── test_ai_orchestrator.py
│   │   │   ├── test_automations.py
│   │   │   ├── test_conversations.py
│   │   │   ├── test_copilot_hitl.py
│   │   │   ├── test_instagram_ai.py
│   │   │   ├── test_instagram_client.py
│   │   │   ├── test_instagram_webhook.py
│   │   │   ├── test_live_chat_ai_e2e.py
│   │   │   ├── test_messenger_webhook.py
│   │   │   ├── test_phase12_6_remediation.py
│   │   │   ├── test_phase12_security.py
│   │   │   ├── test_phase15_1_hardening.py
│   │   │   ├── test_phase15_2_customer_journey.py
│   │   │   ├── test_phase15_3_profile_orders.py
│   │   │   ├── test_phase15_4_customer_account_transactions.py
│   │   │   ├── test_phase15_5_support_conversation_lifecycle.py
│   │   │   ├── test_websocket.py
│   │   │   ├── test_whatsapp_outbound.py
│   │   │   └── test_whatsapp_parser.py
│   │   └── app/
│   │       ├── main.py                 # FastAPI application entrypoint
│   │       ├── config.py               # Pydantic v2 application settings
│   │       ├── database.py             # Async database session & engine
│   │       ├── ai/                     # LangGraph AI orchestration
│   │       ├── models/                 # SQLModel database schemas
│   │       ├── routers/                # REST & Webhook endpoints
│   │       ├── services/               # Core business services
│   │       │   ├── ai/                 # Multi-model orchestrator & prompt engine
│   │       │   ├── channels/           # Inbound message models & media handlers
│   │       │   ├── conversations/      # Ticket matching & deduplication service
│   │       │   ├── csat_delivery.py    # Multi-channel CSAT survey delivery
│   │       │   ├── facebook/           # Meta Messenger client & handlers
│   │       │   ├── instagram/          # Instagram Graph API client & handlers
│   │       │   └── whatsapp/           # Meta WhatsApp Cloud API client & senders
│   │       ├── rag/                    # RAG retrieval pipeline
│   │       └── ws/                     # WebSocket connection manager
│   └── frontend/
│       ├── package.json                # Frontend dependencies & scripts
│       ├── vite.config.js              # Vite configuration & proxy settings
│       └── src/
│           ├── api/                    # Axios API clients
│           ├── components/             # Reusable inbox & layout components
│           ├── pages/                  # Admin, Manager, Agent & Customer views
│           ├── store/                  # Zustand authentication & state store
│           └── utils/                  # Date & string utility formatters
├── scripts/
│   ├── dump_db.sh                      # Export current DB to supporthub_dump.sql
│   └── restore_db.sh                   # Restore DB from supporthub_dump.sql
├── supporthub_dump.sql                 # Complete database snapshot (clean demo data)
├── SETUP_NEW_MACHINE.md                # 10-minute setup guide for fresh machines
└── README.md                           # This file
```

---

## 🔄 Updating the Database Dump

Whenever you change database records and want to commit the updated state:

```bash
# From the project root
./scripts/dump_db.sh
git add supporthub_dump.sql
git commit -m "chore: update database dump"
git push origin main
```

---

## 📄 License & Contributing

Distributed under the MIT License. Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

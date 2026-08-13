# SupportHub — AI Omnichannel Customer Support Platform

SupportHub is an enterprise-grade AI-powered Customer Support Platform with full Omnichannel integration (Email, WhatsApp, Instagram, Website Chat), Real-Time WebSockets, RAG (Retrieval-Augmented Generation), Automated Ticket Resolution Intent Recognition, Dynamic Topic Subject Generation, and Real-time CSAT Delivery.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Docker & Docker Compose** (for PostgreSQL & Redis)
- **Node.js v18+** (for React Frontend)
- **uv** (for Python FastAPI Backend)
- **ngrok** (for receiving webhooks locally)

### 2. Environment Setup
```bash
cd supporthub/backend
cp .env.example .env
```
Edit `.env` and configure your API keys (Gemini, Mailgun, Meta WhatsApp/Instagram).
*See `SETUP_NEW_MACHINE.md` for detailed instructions on getting these keys.*

### 3. Start Database & Cache
```bash
cd supporthub
docker compose up -d
```
*(Optional) If you want to load the pre-seeded demo data, run:*
`cat supporthub_dump.sql | docker exec -i supporthub_db psql -U supporthub -d supporthub`

### 4. Start FastAPI Backend
```bash
cd supporthub/backend
uv run uvicorn app.main:app --reload --port 8001
```

### 5. Start React Frontend
```bash
cd supporthub/frontend
npm install
npm run dev
```

### 6. Start Webhook Tunnel (ngrok)
```bash
ngrok http 8001
```
Use the generated `https://xxxx.ngrok.io` URL to configure your Meta and Mailgun webhooks.

---

## 🔑 Login Credentials

Password for all pre-seeded demo accounts: `Password123!`

| Role | Email |
|---|---|
| Admin | `admin@supporthub.com` |
| Manager | `manager@supporthub.com` |
| Agent | `agent@supporthub.com` |
| Customer | `customer@supporthub.com` |

---

## 📲 Omnichannel Setup Overview

### 1. WhatsApp & Instagram Integration (Meta Cloud API)
Configure these in your `.env`:
- `WHATSAPP_PHONE_ID` and `META_APP_TOKEN` (for WhatsApp Outbound)
- `INSTAGRAM_PAGE_ID` and `PAGE_ACCESS_TOKEN` (for Instagram Outbound)
- Webhook URL in Meta Console: `https://<your-ngrok-subdomain>.ngrok-free.app/api/v1/webhooks/whatsapp` (and `/instagram`)

### 2. Email Integration (Mailgun)
Configure these in your `.env`:
- `MAILGUN_DOMAIN` and `MAILGUN_API_KEY`
- Webhook URL in Mailgun: `https://<your-ngrok-subdomain>.ngrok-free.app/api/v1/webhooks/email`

---

## ✨ Features

- 📩 **Omnichannel Webhooks**: Receive customer messages instantly from Email, WhatsApp, and Instagram.
- 🤖 **Gemini AI RAG Replies**: Automated context-aware response generation with suggested agent replies.
- 🏷️ **Dynamic AI Subject Generation**: Analyzes conversation context and automatically assigns topic titles.
- 🔒 **Resolution Intent Detection**: Auto-closes tickets when the customer says "thanks, that fixed it".
- 📈 **Real-time CSAT Delivery**: Automatically sends 1-5 star surveys to the customer's channel upon ticket resolution.
- ⚡ **WebSocket Live Dashboard**: Real-time sync across all agent inboxes.

# SupportHub — AI Omnichannel Customer Support Platform

SupportHub is an enterprise-grade AI-powered Customer Support Platform with full WhatsApp Cloud API integration, Real-Time WebSockets, RAG (Retrieval-Augmented Generation), Automated Ticket Resolution Intent Recognition, and Dynamic Topic Subject Generation.

---

## 🚀 Quick Start Guide

### 1. Start Database & Cache (Docker)
```bash
cd supporthub
docker compose up -d
```

### 2. Start FastAPI Backend
```bash
cd supporthub/backend
uv run uvicorn app.main:app --reload --port 8001
```

### 3. Start React Frontend
```bash
cd supporthub/frontend
npm run dev
```

---

## 📲 How to Connect WhatsApp (Meta Cloud API Setup)

### Step 1: Obtain Meta WhatsApp Credentials
1. Go to the [Meta Developer Dashboard](https://developers.facebook.com/) and open your **WhatsApp Business App**.
2. Go to **WhatsApp → API Setup**.
3. Copy your **Phone Number ID** (e.g. `1296854793505632`) and your **Access Token**.

### Step 2: Configure Environment File
In `supporthub/backend/.env`, set:
```env
WHATSAPP_PHONE_ID=1296854793505632
WHATSAPP_ACCESS_TOKEN=your_meta_access_token
WHATSAPP_VERIFY_TOKEN=supporthub_webhook_verify_token_2026
```

### Step 3: Start Webhook Tunnel (ngrok)
Expose backend port 8001 to the public internet:
```bash
ngrok http 8001
```

### Step 4: Configure Webhook in Meta Console
1. In Meta Developer Console, go to **WhatsApp → Configuration**.
2. Set **Callback URL**: `https://<your-ngrok-subdomain>.ngrok-free.app/api/v1/webhooks/whatsapp`
3. Set **Verify Token**: `supporthub_webhook_verify_token_2026`
4. Save and subscribe to the **`messages`** webhook field.

### Step 5: End-to-End Features Verified
- 📩 **Real-Time Webhook Processing**: Instant receipt of WhatsApp customer messages.
- 🤖 **Gemini AI RAG Replies**: Automated response generation & outbound delivery to WhatsApp.
- 🏷️ **Dynamic AI Subject Generation**: Analyzes conversation context and automatically assigns a 3–6 word topic title (e.g., *"Password reset and chat closure"*).
- 🔒 **Resolution Intent Detection**: Automatically marks tickets as `resolved` and `ai_resolved = true` when customer requests to end/close the chat.
- ⚡ **WebSocket Live Dashboard Updates**: Real-time sync across agent inboxes.

---

## 🔑 Login Credentials

Password for all pre-seeded demo accounts: `Password123!`

| Role | Email |
|---|---|
| Admin | `admin@supporthub.com` |
| Manager | `manager@supporthub.com` |
| Agent | `agent@supporthub.com` |
| Customer | `customer@supporthub.com` |

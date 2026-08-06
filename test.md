# 🚀 SupportHub Quick Start & Credentials

## 💻 How to Run the Project

**1. Database & Redis (Docker)**
```bash
cd supporthub
docker compose up -d
```

**2. Backend (FastAPI)**
```bash
cd supporthub/backend
uv run uvicorn app.main:app --reload --port 8001
```

**3. Frontend (React/Vite)**
```bash
cd supporthub/frontend
npm run dev
```

---

## 📲 Meta WhatsApp Cloud API Integration Setup

Follow these exact steps to connect WhatsApp to SupportHub for live inbound and AI outbound customer support:

### Step 1: Meta Developer Credentials Setup
1. Go to [Meta Developers Portal](https://developers.facebook.com/) and open your **Business App**.
2. Navigate to **WhatsApp → API Setup**:
   - Copy the **Phone Number ID** (e.g., `1296854793505632`).
   - Copy the **Temporary Access Token** (or create a permanent **System User Access Token** in Meta Business Manager).

### Step 2: Configure Environment Variables
In `supporthub/backend/.env`, set the following parameters:
```env
WHATSAPP_PHONE_ID=1296854793505632
WHATSAPP_ACCESS_TOKEN=your_meta_access_token_here
WHATSAPP_VERIFY_TOKEN=supporthub_webhook_verify_token_2026
```

### Step 3: Start Webhook Tunnel (ngrok)
Run ngrok to expose your local FastAPI backend (port `8001`) to Meta:
```bash
ngrok http 8001
```

### Step 4: Configure Webhook in Meta Console
1. In Meta Developer Portal, go to **WhatsApp → Configuration**.
2. Click **Edit Webhook**:
   - **Callback URL**: `https://<YOUR_NGROK_SUBDOMAIN>.ngrok-free.app/api/v1/webhooks/whatsapp`
   - **Verify Token**: `supporthub_webhook_verify_token_2026`
3. Click **Verify and Save**.
4. In **Webhook Fields**, click **Manage** and subscribe to **`messages`**.

### Step 5: Live Testing
1. Send a WhatsApp message from your personal phone to the Meta Test Number.
2. The incoming message triggers:
   - Automated Customer & Ticket creation in SupportHub.
   - Dynamic AI Subject Generation summarizing the chat topic.
   - Gemini RAG AI response generation.
   - Outbound reply delivered straight back to your WhatsApp app!
3. If you reply *"close this chat"* or *"thanks, that fixed it"*, the backend will automatically set `ticket.status = resolved` and `ai_resolved = true` with live UI WebSocket updates!

---

## 🌐 Webhook Testing URLs & Inspection

- **WhatsApp Webhook URL**: `GET/POST {ngrok_url}/api/v1/webhooks/whatsapp`
- **Mailgun Email Webhook URL**: `POST {ngrok_url}/api/v1/webhooks/email`
- **ngrok Local Web Inspector**: `http://127.0.0.1:4040` (Inspect & replay incoming webhook payloads live)

---

## 🔗 Useful Dashboard URLs

- **Frontend Dashboard** : `http://localhost:5173`
- **Backend API Base** : `http://localhost:8001`
- **Swagger API Docs** : `http://localhost:8001/api/docs`
- **ngrok Local Web Inspector** : `http://127.0.0.1:4040`

---

## 🔑 Test Accounts

Password for all accounts : `Password123!`

- **Admin Email** : `admin@supporthub.com`
- **Manager Email** : `manager@supporthub.com`
- **Agent Email** : `agent@supporthub.com`
- **Customer Email** : `customer@supporthub.com`

---

## 📧 Mailgun Sandbox (Email Setup)

- **Sandbox Domain** : `sandbox54bf194097414b04809437336c4b5e19.mailgun.org`
- **Test Inbound Address** : `test@sandbox54bf194097414b04809437336c4b5e19.mailgun.org`
- **Authorized Recipient** : `heets.brainerhub@gmail.com`

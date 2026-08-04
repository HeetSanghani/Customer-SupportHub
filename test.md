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

## 🌐 Webhook Testing (ngrok)

> **Note**: ngrok is required to expose your local FastAPI backend (port 8001) to external webhook providers (Mailgun, Meta) since external services cannot reach `localhost` directly.

**Command to start ngrok:**
```bash
ngrok http 8001
```

- **Terminals Required**: Run this in a **separate (4th) terminal** alongside Docker, backend, and frontend terminals.
- **Dynamic URLs**: The free ngrok plan generates a **NEW random URL** every time it restarts. After restarting ngrok, update the webhook URL in:
  - **Mailgun**: Receiving → Routes → Destination field
  - **Meta Developer Console**: Webhooks → Callback URL (WhatsApp / Messenger setup)
- **Webhook Endpoint Path Structure**:
  - `POST {ngrok_url}/api/v1/webhooks/email`
  - `GET/POST {ngrok_url}/api/v1/webhooks/whatsapp`
  - `GET/POST {ngrok_url}/api/v1/webhooks/messenger`
- **💡 Debugging Tip**: Open `http://127.0.0.1:4040` (ngrok's local web inspector) in your browser to inspect and replay incoming webhook HTTP requests in real-time.

## 🔗 Useful URLs

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

## 📧 Mailgun Sandbox (Testing)

- **Sandbox Domain** : `sandbox54bf194097414b04809437336c4b5e19.mailgun.org`
- **Test Inbound Address** : `test@sandbox54bf194097414b04809437336c4b5e19.mailgun.org`
- **Authorized Recipient** : `heets.brainerhub@gmail.com`
- **Note** : Outbound emails sent from this sandbox domain may land in your Gmail **Spam** folder. This is expected behavior due to zero sending domain reputation on Mailgun sandbox domains, not a bug.

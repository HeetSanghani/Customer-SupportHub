# 01 — System Entry Points

## Entry Points
1. **HTTP REST API**: FastAPI Application in `app/main.py`
   - `/auth/register`, `/auth/login`, `/auth/me` (`app/routers/auth.py`)
   - `/api/v1/quick-replies` (`app/routers/quick_replies.py`)
   - Webhook integrations (Instagram, Facebook Messenger, WhatsApp)
2. **WebSocket Real-time Chat**:
   - `/ws/chat/{ticket_id}` (`app/routers/ws/chat.py`)

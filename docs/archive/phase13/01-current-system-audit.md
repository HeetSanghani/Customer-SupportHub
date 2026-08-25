# 01. Current Customer-SupportHub Audit

## 1. System Overview
Customer-SupportHub is a full-stack omnichannel customer support application built with FastAPI (backend) and React/Vite (frontend). It supports real-time ticketing, Live Chat widgets, automated AI responses, and customer authentication.

## 2. Technical Stack Audit
- **Backend Framework**: FastAPI (Python 3.13)
- **Frontend Framework**: React 18 with Vite and Vanilla/Tailwind CSS
- **Database Engine**: PostgreSQL 16 (`postgresql+asyncpg://supporthub:supporthub_dev@localhost:5433/supporthub`)
- **ORM / Data Access**: SQLModel / SQLAlchemy (Async engine)
- **Real-Time Layer**: WebSockets (`/ws/chat/{ticket_id}`, `ConnectionManager` in `app/ws/router.py`)
- **Authentication**: OAuth2 Password Bearer with JWT Access/Refresh tokens (`app/routers/auth.py`)

## 3. Core Models & Database Entities (`app/models.py`)
- **User**: Stores system users (`id` UUID, `email`, `password_hash`, `role`, `customer_id`, `status`)
- **Ticket**: Stores support tickets (`id` UUID, `ticket_number`, `customer_id`, `status`, `channel`, `assigned_agent_id`)
- **Message**: Stores ticket messages (`id` UUID, `ticket_id`, `sender_id`, `sender_type`, `body`, `created_at`)
- **Channel**: Configures communication channels (Live Chat, WhatsApp, Instagram, Facebook)
- **AutomationRule**: Configures routing and auto-assignment rules

## 4. Customer Identity Mapping
- `User.customer_id` acts as the trusted identity link binding a SupportHub user to their e-commerce business persona (e.g., `CUST-001`).
- Enforced server-side in auth and WebSocket connection handshake.

## 5. AI Integration Boundary
- Integrated with `supporthub-ai-architecture` via `LiveChatAIAdapter` (`app/services/ai/live_chat_adapter.py`).
- Bridges inbound WebSocket/HTTP messages to `AIOrchestrator.process_message()`.

# 02 — Customer-SupportHub Detailed Audit

## Overview
Detailed audit of the primary production repository (`Customer-SupportHub`).

## Directory Structure & Component Mapping
- **Frontend (`supporthub/frontend`)**:
  - React 18 SPA built with Vite.
  - Contains Customer Live Chat view, Admin Global Inbox, Channel Integrations (WhatsApp, Instagram, Facebook, Email), Quick Reply Manager, and Analytics.
- **Backend Core (`supporthub/backend/app`)**:
  - `main.py`: FastAPI application entry point, CORS configuration, API router registration (`auth`, `tickets`, `users`, `quick_replies`, `ws`).
  - `models/__init__.py`: SQLModel schemas for PostgreSQL application data (`User`, `Ticket`, `Message`, `CsatRating`, `ChannelIntegration`, `Macro`, `QuickReply`, `Automation`).
  - `routers/`: REST API endpoints (`auth.py`, `tickets.py`, `users.py`, `quick_replies.py`).
  - `ws/`: WebSocket connection manager (`chat.py`) and connection registry (`manager.py`).
  - `services/ai/live_chat_adapter.py`: Dynamic runtime adapter linking WebSocket messages to `supporthub-ai-architecture` via `sys.path`.
- **Legacy AI Component (`supporthub/backend/app/ai.py`)**:
  - Contains initial Phase 6 Gemini RAG function (`generate_rag_response`).
  - **Status**: UNUSED at runtime; replaced by `LiveChatAIAdapter` and `supporthub-ai-architecture`.
- **Databases Accessed**:
  - **PostgreSQL (Port 5433)**: Direct SQLAlchemy/SQLModel async connections for SupportHub users, tickets, messages, channels.
  - **MySQL (Port 3306)**: Indirect access via `supporthub-ai-architecture` data access layer.

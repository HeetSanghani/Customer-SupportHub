# Phase 16 — System Architecture Map

## 1. Executive Summary

Customer-SupportHub is a production-grade, multi-tenant AI omnichannel customer support platform built on a unified PostgreSQL database infrastructure. This document outlines the end-to-end architecture across all system layers:

1. **Frontend Tier**: React 18 SPA (Vite + Tailwind CSS + Zustand + React Query + Lucide).
2. **API Tier**: FastAPI Async Web Application (SQLModel + AsyncSession + Pydantic + PyJWT + Passlib/Bcrypt).
3. **Database Tier**: Single Canonical PostgreSQL Database (`supporthub`), holding all ecommerce business domain tables and AI support domain tables.
4. **AI Pipeline**: Multi-Stage Hybrid AI Routing System (`AIRouter` -> `AIOrchestrator` -> `ContextBuilder` -> `ModelAdapter` -> `ResponseParser` -> `AIRepository`).
5. **Real-time Lifecycle**: ASGI WebSockets gateway (`app/routers/ws.py`) handling real-time ticket room event broadcasting, escalation, agent-join notifications, and status transitions.

---

## 2. High-Level System Architecture Diagram

```
[ BROWSER (React 18 + Vite) ]
             │
   HTTP / REST (Bearer JWT)   WebSocket (wss://)
             │                       │
             ▼                       ▼
    [ NGINX Reverse Proxy / Vite Dev Server ]
             │                       │
             └───────────┬───────────┘
                         ▼
          [ FastAPI Application Engine ]
           ├── Auth / JWT Middleware
           ├── Customer Transaction Routers
           ├── AI Live Chat Router
           └── Real-time WebSocket Gateway
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
[ AI Orchestrator & RAG Engine ]     [ AsyncSession ORM ]
  ├── Vector Knowledge Index           │ (SQLModel)
  └── Customer Context Builder         ▼
                        [ Unified PostgreSQL DB ]
```

# Phase 17 — 01. System Operational Architecture Map

## Overview
The Customer-SupportHub platform operates a high-availability, microservices-ready monolithic backend built on Python FastAPI, paired with a React Single-Page Application (SPA) frontend, Nginx reverse proxy, PostgreSQL DB with `pgvector`, and Redis caching/broker infrastructure.

```
                  ┌────────────────────────┐
                  │      React SPA UI      │
                  └───────────┬────────────┘
                              │ HTTPS / WSS
                  ┌───────────▼────────────┐
                  │      Nginx Proxy       │
                  └─────┬──────────────┬───┘
                        │ /api/v1      │ /ws
           ┌────────────▼──────────────▼────────────┐
           │        FastAPI Core Application       │
           └─────┬─────────────┬─────────────┬──────┘
                 │ DB Query    │ Cache/PubSub│ Gemini AI
           ┌─────▼───────┐ ┌───▼─────────┐ ┌─▼─────────────┐
           │ PostgreSQL  │ │ Redis Cache │ │ Google Gemini │
           │  pgvector   │ │ & Pub/Sub   │ │ Flash Lite    │
           └─────────────┘ └─────────────┘ └───────────────┘
```

## Architectural Highlights
- **Unified Backend**: Single codebase servicing REST APIs (`/api/v1/*`) and WebSockets (`/ws/*`).
- **Data Layer**: PostgreSQL with `pgvector` extension for vector embeddings, relational customer models, and full support history.
- **Background Operations**: Thread pool and isolated `AsyncSession` background tasks for Gemini AI classification, auto-reply generation, and automated escalation.
- **Security Invariants**: Token-based authentication (JWT), role-based access control (RBAC), and strict Customer ID binding across all customer data endpoints.

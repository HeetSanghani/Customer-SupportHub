# 26 - Final Phase 15.0 Architecture Blueprint

## Architectural Blueprint Overview
The final Phase 15.0 architecture represents a production-grade, highly secure omnichannel support ecosystem built on top of a single, unified PostgreSQL database (`supporthub`).

```
                                  +---------------------------------------+
                                  |     React 18 + Vite Frontend Portal   |
                                  |     (Zustand + Axios Interceptors)    |
                                  +-------------------+-------------------+
                                                      |
                                     HTTP / REST      |      WebSocket
                                     Bearer JWT       |     ?token=<jwt>
                                                      v
                                  +---------------------------------------+
                                  |          FastAPI Backend Engine       |
                                  |   (app/routers/auth.py & ws/chat.py)  |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |       RBAC & Dependency Layer         |
                                  | (_get_user_from_token, require_role)  |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |      AI & Security Orchestrator       |
                                  | (LiveChatAIAdapter + _check_ownership)|
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |      Unified PostgreSQL `supporthub`  |
                                  |      (24 Tables including `users`)    |
                                  +---------------------------------------+
```

## Core Architecture Guarantees
1. **Single Source of Truth**: All identities (Customer, Agent, Manager, Admin) reside in PostgreSQL `users`.
2. **Deterministic Ownership Enforcement**: Multi-layer security guarantees zero IDOR vulnerabilities across HTTP endpoints, WebSockets, and AI Tool executions.
3. **Omnichannel Continuity**: Support channels (WhatsApp, Instagram, Messenger, Email, Web Chat) collapse into a single unified customer profile without compromising authentication boundaries.

# Phase 17 — 12. API Reference & Contract Standard

## Core API Endpoints
- `POST /api/v1/auth/token` - Authenticate user & issue JWT
- `GET /api/v1/auth/me` - Fetch authenticated user profile
- `GET /api/v1/tickets/` - List tickets (filtered by ownership)
- `POST /api/v1/tickets/` - Create support ticket
- `GET /api/v1/tickets/{id}/messages` - List ticket messages
- `POST /api/v1/tickets/{id}/messages` - Send ticket message (REST API)
- `POST /api/v1/tickets/{id}/accept` - Assign ticket to active agent
- `POST /api/v1/tickets/{id}/resolve` - Mark ticket as resolved
- `POST /api/v1/csat/` - Submit customer satisfaction rating

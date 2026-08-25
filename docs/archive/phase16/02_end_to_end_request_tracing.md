# Phase 16 — End-To-End Request Tracing Guide

## 1. Flow Tracing Overview

This document details the exact sequence of technical steps executed when a user interacts with Customer-SupportHub from opening the browser to receiving real-time AI and human support.

---

## 2. Traced Request Flows

### Flow A: User Registration & Identity Provisioning
1. User submits details at `/register` (`POST /api/v1/auth/register`).
2. FastAPI validates request schema (`UserCreate`).
3. Password is hashed using `bcrypt` via `passlib.context.CryptContext`.
4. User record is created in PostgreSQL `users` table with `role = customer` and `status = active`.
5. Automatic linking creates/updates `customer_id` mapping.

### Flow B: Authentication & Token Issuance
1. User submits credentials at `/login` (`POST /api/v1/auth/login`).
2. System checks `bcrypt.verify(password, user.password_hash)`.
3. PyJWT generates signed JWT Bearer token containing `sub: user_id`, `role`, and expiration (`exp`).
4. React frontend saves token in Zustand `authStore` with persistent storage.

### Flow C: Live AI Chat Query Execution
1. User types query: *"What is the status of ORD-025?"* in `CustomerLiveChat.jsx`.
2. Frontend sends payload over WebSocket or REST (`POST /api/v1/tickets/{id}/messages`).
3. `LiveChatAIAdapter` receives message and invokes `AIOrchestrator.generate_for_ticket()`.
4. `AIRouter` classifies intent as `STRUCTURED` (order domain).
5. `ContextBuilder` extracts customer identity from JWT (`current_user.id`) and fetches order `ORD-025` from PostgreSQL.
6. `ModelAdapter` generates response based on accurate PostgreSQL data.
7. Response is returned to frontend and broadcast over WebSocket.

### Flow D: Human Escalation & Agent Join
1. User clicks "Talk to Human".
2. Endpoint `POST /api/v1/tickets/{id}/escalate` updates ticket status to `escalated`.
3. Agent accepts ticket via `POST /api/v1/tickets/{id}/accept`.
4. WebSocket gateway broadcasts `agent_joined` event to ticket room.
5. AI bot responses are automatically suppressed while agent is connected.
6. Agent resolves ticket (`POST /api/v1/tickets/{id}/resolve`) and triggers CSAT survey widget.

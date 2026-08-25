# Phase 17 — 06. Real-Time WebSocket & Agent Handoff Architecture

## WebSocket Implementation
- **Route**: `/ws/chat/{ticket_id}`
- **Protocol**: WSS (WebSocket Secure) over Nginx reverse proxy.
- **Broadcasting**: Real-time pub/sub manager handles incoming/outgoing chat messages across customer, agent, and AI bot interfaces.

## Agent Handoff Trigger
- Triggered when customer requests a human representative or AI confidence drops below threshold.
- Ticket status updates to `open`, notifying active support agents via agent portal event streams.

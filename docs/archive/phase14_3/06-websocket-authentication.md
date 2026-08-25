# 06 — WebSocket Authentication

- **Endpoint**: `/ws/chat/{ticket_id}`
- **Authentication**: JWT token sent via query parameter or authorization header.
- **Ticket Ownership Enforcement**: Connection is closed with `4003 Forbidden` if customer attempts to connect to a ticket belonging to another user.

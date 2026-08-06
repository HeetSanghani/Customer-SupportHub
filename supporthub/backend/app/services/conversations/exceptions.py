"""
app/services/conversations/exceptions.py

Domain exceptions for the Conversation Management layer.

WHY CUSTOM EXCEPTIONS MATTER IN PRODUCTION:
  Without them, your services raise generic Python exceptions (ValueError,
  RuntimeError, Exception). The router then has no way to distinguish:
    - "Message already processed" (correct, return 200)
    - "DB is down" (server error, return 503)
    - "Customer phone is invalid" (client error, return 400)

  With domain exceptions, each layer has clear responsibilities:
    - Repository raises: DuplicateMessageError, DatabaseError
    - Service raises:    CustomerNotFound, ConversationNotFound, ValidationError
    - Router catches:   specific exceptions → correct HTTP status codes

  This is how Intercom, Stripe, and all mature SaaS backends are structured.
  The exception hierarchy IS your error contract between architectural layers.

HIERARCHY:
  ConversationError (base)
  ├── DuplicateMessageError     → 200 OK (idempotent success, already processed)
  ├── CustomerNotFound          → 404
  ├── ConversationNotFound      → 404
  ├── ValidationError           → 422
  └── DatabaseError             → 503
"""

from __future__ import annotations


class ConversationError(Exception):
    """
    Base exception for the Conversation Management layer.
    All domain exceptions inherit from this for easy catch-all handling.
    """
    def __init__(self, message: str, detail: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail or message


class DuplicateMessageError(ConversationError):
    """
    Raised when a channel_message_id has already been processed.

    WHY THIS IS NOT AN ERROR:
      This is an expected, normal condition in production. Meta retries
      webhook delivery multiple times. When we detect a duplicate, the correct
      response is to return 200 OK immediately (idempotent success), NOT to
      return an error code (which would cause further retries).

    Usage:
      raise DuplicateMessageError(
          channel_message_id="wamid.HBgM...",
          channel="whatsapp",
      )
    """
    def __init__(self, channel_message_id: str, channel: str) -> None:
        self.channel_message_id = channel_message_id
        self.channel = channel
        super().__init__(
            message=f"Duplicate message detected",
            detail=f"Message '{channel_message_id}' from channel '{channel}' was already processed.",
        )


class CustomerNotFound(ConversationError):
    """
    Raised when a customer lookup fails and auto-creation is explicitly disabled.

    In normal flow, customers are always found-or-created, so this should
    only be raised in administrative or manual lookup contexts.
    """
    def __init__(self, channel: str, channel_customer_id: str) -> None:
        self.channel = channel
        self.channel_customer_id = channel_customer_id
        super().__init__(
            message=f"Customer not found",
            detail=f"No customer with id='{channel_customer_id}' on channel='{channel}'.",
        )


class ConversationNotFound(ConversationError):
    """
    Raised when an open conversation lookup fails and auto-creation is disabled.
    """
    def __init__(self, customer_id: str, channel: str) -> None:
        self.customer_id = customer_id
        self.channel = channel
        super().__init__(
            message=f"Conversation not found",
            detail=f"No open conversation for customer='{customer_id}' on channel='{channel}'.",
        )


class ValidationError(ConversationError):
    """
    Raised when input data fails domain validation before hitting the database.

    Examples:
      - IncomingMessage missing required fields
      - Phone number format invalid
      - Channel not supported
    """
    def __init__(self, field: str, reason: str) -> None:
        self.field = field
        self.reason = reason
        super().__init__(
            message=f"Validation failed for '{field}'",
            detail=reason,
        )


class DatabaseError(ConversationError):
    """
    Raised when a database operation fails unexpectedly.

    Wraps SQLAlchemy/asyncpg exceptions with domain context so upper layers
    don't need to import SQLAlchemy error types.
    """
    def __init__(self, operation: str, cause: Exception | None = None) -> None:
        self.operation = operation
        self.cause = cause
        super().__init__(
            message=f"Database error during '{operation}'",
            detail=str(cause) if cause else None,
        )

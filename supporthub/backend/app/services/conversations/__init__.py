"""
app/services/conversations/

Conversation Management layer — the core of omnichannel support.

Modules:
  exceptions.py   — Domain exceptions raised by this layer
  models.py       — ConversationContext (rich return object)
  repository.py   — Raw DB access: queries, inserts, idempotency checks
  service.py      — Business logic: find-or-create, lifecycle management
"""

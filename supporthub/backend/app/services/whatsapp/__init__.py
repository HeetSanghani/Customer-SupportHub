"""
WhatsApp Business Cloud API service package.

Sub-modules:
  auth      — Webhook verify-token validation & HMAC-SHA256 signature verification
  parser    — Raw Meta payload → IncomingMessage internal model
  sender    — Outbound WhatsApp message dispatch with retry strategy
  webhook   — Orchestration: store message, call AI, send reply
"""

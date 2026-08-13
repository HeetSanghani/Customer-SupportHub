"""
app/services/ai/models.py

Domain data models for the AI Orchestration layer.

These are pure Python dataclasses — NO ORM, NO SQLModel, NO Pydantic.
They are in-memory value objects that pass data between layers.

WHY NOT USE PYDANTIC HERE:
  Pydantic is for validation at API boundaries (HTTP request/response).
  Inside the service layer, we use plain dataclasses for:
    - Zero validation overhead (data is already validated at the webhook boundary)
    - Frozen (immutable) objects prevent accidental mutation between steps
    - No JSON serialization overhead

FLOW OF DATA:
  ConversationContext
    → ContextBuilder → LLMContext
    → PromptBuilder  → Prompt
    → ModelAdapter   → raw provider response dict
    → ResponseParser → AIResponse
    → AIRepository   → AIMessageRecord (stored)
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ─── LLMContext ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class LLMContext:
    """
    Structured context assembled from ConversationContext for the LLM.

    WHY THIS LAYER EXISTS (not just using ConversationContext directly):
      ConversationContext is the full ORM-rich context with Ticket objects,
      User objects, and database references. The LLM doesn't need any of that.

      LLMContext is a clean, serialization-safe object containing only the
      information the LLM needs to generate a response. No ORM objects.
      No database references. Pure strings and simple types.

      This makes the ContextBuilder the single point of "translation"
      between the DB world and the AI world.

    Fields:
      customer_name: Used in the system prompt and greeting logic.
      customer_channel_id: Phone number / email / PSID. Useful for personalization.
      channel: "whatsapp" | "email" | "instagram" etc.
      conversation_ref: "TCK-10023" — included in AI logs for traceability.
      is_new_customer: Signals AI to give a welcome message.
      is_new_conversation: Signals AI to introduce itself.
      ticket_status: "new" | "open" | "waiting" — AI may adjust tone.
      ticket_priority: "medium" | "high" | "urgent" — AI escalates accordingly.
      history: Chronological list of {"role": "user"|"assistant", "content": "..."}
      current_message: The text the customer just sent.
      current_message_type: "text" | "image" | "audio" — affects AI handling.
    """
    customer_name: str
    customer_channel_id: str
    channel: str
    conversation_ref: str
    is_new_customer: bool
    is_new_conversation: bool
    ticket_status: str
    ticket_priority: str
    history: list[dict]           # [{"role": "user"|"assistant", "content": "..."}]
    current_message: str          # The current customer message text
    current_message_type: str     # MessageType value
    kb_context: Optional[str] = None
    ticket_subject: Optional[str] = None
    ticket_category: Optional[str] = None
    tone: Optional[str] = None
    image_paths: list[str] = field(default_factory=list)


# ─── Prompt ───────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Prompt:
    """
    The assembled prompt ready to be sent to an LLM.

    WHY PROMPT IS A VALUE OBJECT:
      This lets you log, store, version, and replay prompts independently.
      In production (Intercom AI, Freshdesk AI), every prompt is stored
      so you can:
        - Debug why the AI said something
        - A/B test prompt versions
        - Roll back to a previous prompt if a new version performs worse
        - Calculate token costs post-hoc

    Fields:
      system: The system instruction (role, tone, rules, KB context).
      messages: The conversation history in OpenAI chat format.
      version: A human-readable prompt version string (e.g. "v1.0").
      system_hash: SHA256 of the system prompt — for diff comparison.
      temperature: LLM temperature setting used for this prompt.
      max_tokens: Output token budget.
      model_name: Which model this prompt was designed for.
    """
    system: str
    messages: list[dict]          # [{"role": "...", "content": "..."}]
    version: str = "v1.0"
    temperature: float = 0.4
    max_tokens: int = 500
    model_name: str = "gemini-flash-lite-latest"
    image_paths: list[str] = field(default_factory=list)

    @property
    def system_hash(self) -> str:
        """SHA256 of the system prompt for version diffing."""
        return hashlib.sha256(self.system.encode()).hexdigest()[:16]

    @property
    def total_message_chars(self) -> int:
        """Rough character count for token estimation (1 token ≈ 4 chars)."""
        return sum(len(m.get("content", "")) for m in self.messages) + len(self.system)

    @property
    def estimated_input_tokens(self) -> int:
        """Rough token estimate: characters / 4."""
        return self.total_message_chars // 4


# ─── Token Usage ─────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class TokenUsage:
    """
    Token consumption metrics from a single LLM call.

    WHY TRACK TOKENS:
      - Cost calculation: input_tokens * price_per_input + output_tokens * price_per_output
      - Budget enforcement: reject calls that would exceed monthly token budget
      - Optimization: long history → trim earlier messages to reduce cost
      - Analytics: which conversation types consume the most tokens

    Pricing reference (approximate, check provider docs for current rates):
      Gemini Flash:  $0.075/1M input, $0.30/1M output
      Claude Haiku:  $0.25/1M input,  $1.25/1M output
      GPT-4o-mini:   $0.15/1M input,  $0.60/1M output
    """
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    @property
    def estimated_cost_usd(self) -> float:
        """
        Rough cost estimate in USD using Gemini Flash pricing.
        Override per-adapter with actual provider pricing.
        """
        input_cost = (self.input_tokens / 1_000_000) * 0.075
        output_cost = (self.output_tokens / 1_000_000) * 0.30
        return round(input_cost + output_cost, 8)


# ─── Model Info ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ModelInfo:
    """Metadata about the LLM that generated the response."""
    provider: str          # "gemini" | "claude" | "openai" | "ollama"
    model_name: str        # "gemini-flash-lite-latest" | "claude-haiku-4-5" etc.
    prompt_version: str    # "v1.0"
    system_hash: str       # First 16 chars of SHA256(system_prompt)
    temperature: float
    max_tokens: int


# ─── AIResponse ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class AIResponse:
    """
    Normalized AI response — the OUTPUT of Step 3B and INPUT of Step 3C.

    WHY NORMALIZE LLM RESPONSES:
      Every LLM provider returns a different response structure:
        - OpenAI:    response.choices[0].message.content
        - Anthropic: response.content[0].text
        - Gemini:    response.text (or response.parts[0].text)

      If your Sender layer reads OpenAI's response format directly, you're
      locked into OpenAI forever. If you switch to Gemini, you rewrite the Sender.

      AIResponse is the universal contract. The Sender only sees AIResponse.
      It never knows which LLM generated the text.

    Fields:
      response_text: The actual reply to send to the customer.
      model: ModelInfo — which model, version, temperature, prompt hash.
      usage: TokenUsage — tokens consumed, estimated cost.
      finish_reason: "stop" | "length" | "content_filter" | "error"
      latency_ms: Wall-clock time of the LLM API call in milliseconds.
      confidence: Float 0.0–1.0. Currently heuristic; can be replaced by classifier.
      error: If generation failed, contains the error message. response_text will be
             the fallback message.
    """
    response_text: str
    model: ModelInfo
    usage: TokenUsage
    finish_reason: str = "stop"
    latency_ms: int = 0
    confidence: float = 1.0
    error: Optional[str] = None

    @property
    def is_fallback(self) -> bool:
        """True if the AI failed and we returned a fallback message."""
        return self.error is not None

    @property
    def was_truncated(self) -> bool:
        """True if the LLM stopped due to token limit (not natural end)."""
        return self.finish_reason == "length"


# ─── AI Message Record ────────────────────────────────────────────────────────

@dataclass
class AIMessageRecord:
    """
    What gets persisted to the database after an AI response is generated.

    This is NOT a SQLModel class — it's a plain dataclass that the
    AIRepository converts into a Message ORM object before saving.

    WHY SEPARATE FROM AIResponse:
      AIResponse is an immutable value object for pipeline data flow.
      AIMessageRecord is mutable and carries DB-specific fields (ticket_id, etc.)
      that the AIResponse doesn't need to know about.
    """
    ticket_id: str
    response_text: str
    model_name: str
    provider: str
    prompt_version: str
    system_hash: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    finish_reason: str
    confidence: float
    estimated_cost_usd: float
    error: Optional[str] = None
    created_at: Optional[datetime] = None

"""Data models for provider-independent LLM interactions."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class LLMRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class LLMMessage:
    """A message in an LLM conversation history."""
    role: LLMRole
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None


@dataclass
class TokenUsage:
    """Token consumption statistics for an LLM invocation."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0


@dataclass
class LLMRequest:
    """Encapsulates all parameters for an LLM generation request."""
    messages: List[LLMMessage]
    temperature: float = 0.0
    max_tokens: int = 1000
    model: Optional[str] = None
    response_format: Optional[Dict[str, Any]] = None
    stop_sequences: List[str] = field(default_factory=list)
    system_instruction: Optional[str] = None


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""
    content: str
    model: str
    provider: str
    usage: TokenUsage = field(default_factory=TokenUsage)
    latency_seconds: float = 0.0
    finish_reason: str = "stop"
    raw_response: Optional[Dict[str, Any]] = None
    structured_data: Optional[Dict[str, Any]] = None

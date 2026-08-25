# 08 — AI Source-of-Truth

## Component Mapping & Active Runtime Path

| Component | Project Location | Runtime Status | Canonical File | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **LiveChatAIAdapter**| `Customer-SupportHub` | **ACTIVE** | `app/services/ai/live_chat_adapter.py` | Bridge to AI engine |
| **AIOrchestrator** | `supporthub-ai-architecture` | **ACTIVE** | `ai/orchestrator.py` | Core orchestration logic |
| **AIRouter** | `supporthub-ai-architecture` | **ACTIVE** | `ai/router.py` | 5-tier hybrid router |
| **IntentClassifiers**| `supporthub-ai-architecture` | **ACTIVE** | `ai/intent.py` | Pattern + LLM classifiers |
| **ConversationContext**|`supporthub-ai-architecture` | **ACTIVE** | `ai/context.py` | Session context tracking |
| **ToolRegistry** | `supporthub-ai-architecture` | **ACTIVE** | `ai/tools.py` | Domain tool executions |
| **AISecurityGuard** | `supporthub-ai-architecture` | **ACTIVE** | `ai/security.py` | Zero-trust ownership guard |
| **ResponseSynthesizer**|`supporthub-ai-architecture` | **ACTIVE** | `ai/response.py` | Grounded response generation |
| **Legacy `app/ai.py`** | `Customer-SupportHub` | **UNUSED** | `app/ai.py` | Phase 6 legacy Gemini code |

## Consolidation Target
- Core AI engine modules in `supporthub-ai-architecture/ai` and `data_access` should be moved into `Customer-SupportHub/supporthub/backend/app/ai/` during Phase 14 consolidation.

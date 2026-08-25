"""Central AI Orchestrator coordinating all pipeline stages with LLM reasoning and deterministic authority."""
from typing import Dict, Any, Optional
from app.ai.context import context_manager, ConversationContext
from app.ai.router import ai_router, AIRouter, RouteDecision
from app.ai.tools import tool_registry, ToolRegistry
from app.rag.pipeline import rag_pipeline, RAGPipeline
from app.ai.security import security_validator, SecurityValidator
from app.ai.response import response_synthesizer, llm_response_synthesizer, LLMResponseSynthesizer, ResponseSynthesizer, AIResponse
from app.data_access.customer_service import CustomerService
from app.ai.graph.build import compiled_graph
from app.ai.graph.state import GraphState


class AIOrchestrator:
    """End-to-end orchestration pipeline for SupportHub AI."""

    def __init__(
        self,
        router: Optional[AIRouter] = None,
        tools: Optional[ToolRegistry] = None,
        rag: Optional[RAGPipeline] = None,
        security: Optional[SecurityValidator] = None,
        synthesizer: Optional[ResponseSynthesizer] = None,
        llm_synthesizer: Optional[LLMResponseSynthesizer] = None,
        use_llm: bool = False
    ):
        self.router = router or ai_router
        self.tools = tools or tool_registry
        self.rag = rag or rag_pipeline
        self.security = security or security_validator
        self.synthesizer = synthesizer or response_synthesizer
        self.llm_synthesizer = llm_synthesizer or llm_response_synthesizer
        self.use_llm = use_llm
        self.customer_service = CustomerService()

    def process_message(
        self,
        query: str,
        customer_id: Optional[str] = None,
        conversation_id: str = "conv_default",
        channel_type: str = "WEBSITE",
        context_override: Optional[ConversationContext] = None,
        use_llm: Optional[bool] = None
    ) -> AIResponse:
        """Process an incoming user message through the LangGraph execution graph."""
        active_use_llm = self.use_llm if use_llm is None else use_llm

        # 1. Context Resolution
        ctx = context_override or context_manager.get_or_create(
            conversation_id=conversation_id,
            customer_id=customer_id,
            channel_type=channel_type
        )
        if context_override:
            context_manager._contexts[conversation_id] = context_override
        ctx.add_user_message(query)

        # 2. Build initial graph state from context and request
        initial_state: GraphState = {
            "conversation_id": conversation_id,
            "customer_id": ctx.customer_id,
            "channel_type": channel_type,
            "active_order_id": ctx.active_order_id,
            "active_product_id": ctx.active_product_id,
            "active_return_id": ctx.active_return_id,
            "active_refund_id": ctx.active_refund_id,
            "last_order_id": getattr(ctx, "last_order_id", None),
            "last_product_id": getattr(ctx, "last_product_id", None),
            "previous_intent": getattr(ctx, "previous_intent", None),
            "slot_needed": getattr(ctx, "slot_needed", None),
            "frustration_score": getattr(ctx, "frustration_score", 0),
            "metadata": getattr(ctx, "metadata", {}),
            "raw_query": query,
            "use_llm": active_use_llm,
        }

        # 3. Execute LangGraph compiled workflow
        result_state = compiled_graph.invoke(initial_state)
        final_resp: AIResponse = result_state["final_response"]

        # 4. Context Post-Processing
        if result_state.get("escalated"):
            ctx.escalated = True

        intent_str = None
        if final_resp.security_decision:
            intent_str = "SECURITY_DENIAL"
        elif final_resp.escalation_decision:
            intent_str = "HUMAN_ESCALATION"
        else:
            sub_questions = result_state.get("sub_questions", [])
            if sub_questions and sub_questions[0].get("intent"):
                intent_str = sub_questions[0]["intent"].intent_name
            else:
                intent_str = final_resp.route_type

        ctx.add_assistant_message(final_resp.content, intent=intent_str)
        return final_resp


# Global Orchestrator instance
ai_orchestrator = AIOrchestrator(use_llm=False)


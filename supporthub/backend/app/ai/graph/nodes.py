from __future__ import annotations

import re
from typing import List, Dict, Any, Optional

from app.ai.escalation import escalation_evaluator
from app.ai.router import AIRouter, RouteType, RouteDecision
from app.ai.response import (
    response_synthesizer,
    llm_response_synthesizer,
    AIResponse,
)
from app.ai.security import security_validator
from app.ai.tools import tool_registry
from app.rag.pipeline import rag_pipeline
from app.ai.context import context_manager
from app.data_access.customer_service import CustomerService

from .state import GraphState, SubQuestion

_router = AIRouter()
_customer_service = CustomerService()


def check_escalation(state: GraphState) -> GraphState:
    active_order_id = state.get("active_order_id")
    if not active_order_id and state.get("raw_query"):
        import re
        match = re.search(r'\b(ORD-\d+)\b', state["raw_query"], re.IGNORECASE)
        if match:
            active_order_id = match.group(1).upper()

    decision = escalation_evaluator.evaluate(
        query=state["raw_query"],
        customer_id=state.get("customer_id"),
        conversation_id=state.get("conversation_id"),
        active_order_id=active_order_id,
    )
    state["escalation_decision"] = decision
    state["escalated"] = decision.should_escalate
    if active_order_id:
        state["active_order_id"] = active_order_id
    return state


def decompose_query(state: GraphState) -> GraphState:
    texts = _naive_split(state["raw_query"])
    state["sub_questions"] = [
        {"text": t, "intent": None, "route": None, "response": None} for t in texts
    ]
    return state


def _naive_split(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return [text]

    # Heuristic splitting on multiple ?, ;, newlines, "and", "also"
    if text.count("?") > 1:
        parts = [p.strip() + "?" for p in text.split("?") if p.strip()]
        parts = [re.sub(r'\?+$', '?', p) for p in parts]
        if len(parts) > 1:
            return parts

    if ";" in text:
        parts = [p.strip() for p in text.split(";") if p.strip()]
        if len(parts) > 1:
            return parts

    if "\n" in text:
        parts = [p.strip() for p in text.split("\n") if p.strip()]
        if len(parts) > 1:
            return parts

    # 4. Split on multi-intent clause conjunctions (e.g. ", and can I also", ", and also", ", also", " and additionally")
    pattern = r',?\s*(?:and\s+)?(?:can\s+i\s+)?\b(?:also|additionally)\b|,\s*and\s+can\s+i\b'
    parts = re.split(pattern, text, flags=re.IGNORECASE)
    parts = [p.strip(" ,.") for p in parts if p.strip(" ,.")]
    if len(parts) > 1:
        # Prepend 'Can I ' if part lost its question prefix
        cleaned_parts = []
        for i, p in enumerate(parts):
            if i > 0 and not p.lower().startswith(("where", "what", "can", "how", "is", "does", "will", "when")):
                p = "Can I " + p
            cleaned_parts.append(p)
        return cleaned_parts

    return [text]


def handle_subquestions(state: GraphState) -> GraphState:
    context_slots = {
        "order_id": state.get("active_order_id"),
        "product_id": state.get("active_product_id"),
        "return_id": state.get("active_return_id"),
        "refund_id": state.get("active_refund_id"),
    }

    for sub in state["sub_questions"]:
        route_decision = _router.route(
            query=sub["text"],
            customer_id=state.get("customer_id"),
            conversation_id=state.get("conversation_id"),
            context_slots=context_slots,
            use_llm=state.get("use_llm"),
        )
        sub["route"] = route_decision
        sub["intent"] = route_decision.intent
        sub["response"] = _handle_single_route(route_decision, sub["text"], state)

    return state


def _get_customer_name(customer_id: Optional[str]) -> str:
    customer_name = "Customer"
    if customer_id and customer_id != "GUEST":
        try:
            cust_rec = _customer_service.get_customer(customer_id)
            if cust_rec:
                customer_name = cust_rec.full_name
        except Exception:
            pass
    return customer_name


def _get_history_str(conversation_id: Optional[str]) -> str:
    if not conversation_id:
        return ""
    ctx = context_manager.get_or_create(conversation_id=conversation_id)
    turns = ctx.get_recent_history(limit=3)
    return "\n".join([f"{t.role.upper()}: {t.content}" for t in turns[:-1]]) if len(turns) > 1 else ""


def _handle_single_route(route_decision: RouteDecision, query: str, state: GraphState) -> AIResponse:
    if route_decision.route_type == RouteType.SECURITY:
        return response_synthesizer.synthesize_security_response(route_decision.security_decision)

    if route_decision.route_type == RouteType.HUMAN:
        return response_synthesizer.synthesize_escalation_response(route_decision.escalation_decision)

    if route_decision.route_type == RouteType.RAG:
        return _handle_rag_route(route_decision, query, state)

    if route_decision.route_type == RouteType.STRUCTURED:
        return _handle_structured_route(route_decision, query, state)

    if route_decision.route_type == RouteType.HYBRID:
        return _handle_hybrid_route(route_decision, query, state)

    return AIResponse(
        content="I am here to assist with your ShopKart inquiries. Could you please provide more details?",
        route_type="UNKNOWN"
    )


def _handle_rag_route(route_decision: RouteDecision, query: str, state: GraphState) -> AIResponse:
    _explicit_entities = route_decision.intent.explicit_entities if route_decision.intent else {}
    conversation_id = state.get("conversation_id")
    if conversation_id and _explicit_entities:
        ctx = context_manager.get_or_create(
            conversation_id=conversation_id,
            customer_id=state.get("customer_id"),
            channel_type=state.get("channel_type", "WEBSITE")
        )
        ctx.update_slots_domain_aware(_explicit_entities, authorized=True)

    rag_res = rag_pipeline.query(route_decision.rag_query or query)
    customer_id = state.get("customer_id")
    active_use_llm = state.get("use_llm", False)

    if active_use_llm:
        customer_name = _get_customer_name(customer_id)
        history_str = _get_history_str(conversation_id)
        return llm_response_synthesizer.synthesize(
            query=query,
            route_type="RAG",
            rag_result=rag_res,
            customer_id=customer_id or "GUEST",
            customer_name=customer_name,
            conversation_history=history_str,
            use_llm=True
        )
    else:
        return response_synthesizer.synthesize_rag_response(query, rag_res)


def _handle_structured_route(route_decision: RouteDecision, query: str, state: GraphState) -> AIResponse:
    from app.ai.intent import IntentCategory as _IC
    _PRIVATE_CATEGORIES = {
        _IC.ORDERS, _IC.PAYMENTS, _IC.SHIPMENTS,
        _IC.RETURNS, _IC.REFUNDS, _IC.ACCOUNT, _IC.UNKNOWN
    }
    customer_id = state.get("customer_id")
    conversation_id = state.get("conversation_id") or "conv_default"
    _is_guest = (customer_id is None or str(customer_id).upper() in ("GUEST", ""))

    if _is_guest and route_decision.intent and route_decision.intent.category in _PRIVATE_CATEGORIES:
        login_msg = (
            "To view your personal order, payment, shipment, return, or refund details, "
            "please log in to your authenticated account first."
        )
        return AIResponse(content=login_msg, route_type="STRUCTURED", is_grounded=True)

    ctx = context_manager.get_or_create(
        conversation_id=conversation_id,
        customer_id=customer_id,
        channel_type=state.get("channel_type", "WEBSITE")
    )

    _pre_turn_order_id   = ctx.active_order_id
    _pre_turn_product_id = ctx.active_product_id
    _pre_turn_return_id  = ctx.active_return_id
    _pre_turn_refund_id  = ctx.active_refund_id

    structured_data = _execute_tools(route_decision, state, ctx)
    auth_violation = _check_ownership(structured_data, customer_id, route_decision)
    if auth_violation:
        ctx.revert_slots(
            prev_order_id=_pre_turn_order_id,
            prev_product_id=_pre_turn_product_id,
            prev_return_id=_pre_turn_return_id,
            prev_refund_id=_pre_turn_refund_id
        )
        return response_synthesizer.synthesize_security_response(auth_violation)

    _explicit_entities = route_decision.intent.explicit_entities if route_decision.intent else {}
    ctx.update_slots_domain_aware(_explicit_entities, authorized=True)

    active_use_llm = state.get("use_llm", False)
    if active_use_llm:
        customer_name = _get_customer_name(customer_id)
        history_str = _get_history_str(conversation_id)
        return llm_response_synthesizer.synthesize(
            query=query,
            route_type="STRUCTURED",
            structured_data=structured_data,
            customer_id=customer_id or "GUEST",
            customer_name=customer_name,
            conversation_history=history_str,
            use_llm=True
        )
    else:
        intent_name = route_decision.intent.intent_name if route_decision.intent else "UNKNOWN"
        return response_synthesizer.synthesize_structured_response(
            intent_name=intent_name,
            data=structured_data,
            query=query
        )


def _handle_hybrid_route(route_decision: RouteDecision, query: str, state: GraphState) -> AIResponse:
    customer_id = state.get("customer_id")
    conversation_id = state.get("conversation_id") or "conv_default"
    ctx = context_manager.get_or_create(
        conversation_id=conversation_id,
        customer_id=customer_id,
        channel_type=state.get("channel_type", "WEBSITE")
    )

    _pre_turn_order_id   = ctx.active_order_id
    _pre_turn_product_id = ctx.active_product_id
    _pre_turn_return_id  = ctx.active_return_id
    _pre_turn_refund_id  = ctx.active_refund_id

    structured_data = _execute_tools(route_decision, state, ctx)
    rag_res = rag_pipeline.query(route_decision.rag_query or query)

    auth_violation = _check_ownership(structured_data, customer_id, route_decision)
    if auth_violation:
        ctx.revert_slots(
            prev_order_id=_pre_turn_order_id,
            prev_product_id=_pre_turn_product_id,
            prev_return_id=_pre_turn_return_id,
            prev_refund_id=_pre_turn_refund_id
        )
        return response_synthesizer.synthesize_security_response(auth_violation)

    _explicit_entities = route_decision.intent.explicit_entities if route_decision.intent else {}
    ctx.update_slots_domain_aware(_explicit_entities, authorized=True)

    active_use_llm = state.get("use_llm", False)
    if active_use_llm:
        customer_name = _get_customer_name(customer_id)
        history_str = _get_history_str(conversation_id)
        return llm_response_synthesizer.synthesize(
            query=query,
            route_type="HYBRID",
            structured_data=structured_data,
            rag_result=rag_res,
            customer_id=customer_id or "GUEST",
            customer_name=customer_name,
            conversation_history=history_str,
            use_llm=True
        )
    else:
        return response_synthesizer.synthesize_hybrid_response(
            structured_data=structured_data,
            rag_result=rag_res,
            query=query
        )


def _execute_tools(decision: RouteDecision, state: GraphState, ctx: Any) -> Dict[str, Any]:
    data = {}
    ent = decision.intent.entities if decision.intent else {}
    order_id = ent.get("order_id") or state.get("active_order_id") or getattr(ctx, "active_order_id", None) or state.get("last_order_id") or getattr(ctx, "last_order_id", None)
    product_id = ent.get("product_id") or state.get("active_product_id") or getattr(ctx, "active_product_id", None) or state.get("last_product_id") or getattr(ctx, "last_product_id", None)
    return_id = ent.get("return_id") or state.get("active_return_id") or getattr(ctx, "active_return_id", None)
    refund_id = ent.get("refund_id") or state.get("active_refund_id") or getattr(ctx, "active_refund_id", None)
    seller_id = ent.get("seller_id")
    customer_id = ent.get("customer_id") or state.get("customer_id") or getattr(ctx, "customer_id", None)

    for tool in decision.target_tools:
        try:
            if tool == "get_order" and order_id:
                data["order"] = tool_registry.get_order(order_id)
            elif tool == "get_order_items" and order_id:
                data["order_items"] = tool_registry.get_order_items(order_id)
            elif tool == "get_shipment_by_order":
                if order_id:
                    data["shipment"] = tool_registry.get_shipment_by_order(order_id)
                elif customer_id:
                    c_orders = tool_registry.get_customer_orders(customer_id)
                    if c_orders:
                        data["customer_orders"] = c_orders
                        first_ord = c_orders[0]
                        oid = first_ord.get("order_id") if isinstance(first_ord, dict) else getattr(first_ord, "order_id", None)
                        if oid:
                            data["shipment"] = tool_registry.get_shipment_by_order(oid)
            elif tool == "get_shipment_by_tracking" and ent.get("tracking_number"):
                data["shipment"] = tool_registry.get_shipment_by_tracking(ent["tracking_number"])
            elif tool == "get_product" and product_id:
                data["product"] = tool_registry.get_product(product_id)
            elif tool == "get_seller" and seller_id:
                data["seller"] = tool_registry.get_seller(seller_id)
            elif tool == "get_seller" and product_id and not seller_id:
                data["seller"] = tool_registry.get_seller_by_product(product_id)
            elif tool == "get_payment_by_order" and order_id:
                data["payment"] = tool_registry.get_payment_by_order(order_id)
            elif tool == "get_payment" and ent.get("payment_id"):
                data["payment"] = tool_registry.get_payment(ent["payment_id"])
            elif tool == "get_return" and return_id:
                data["return"] = tool_registry.get_return(return_id)
            elif tool == "get_return_by_order" and order_id:
                data["return"] = tool_registry.get_return_by_order(order_id)
            elif tool == "get_refund" and refund_id:
                data["refund"] = tool_registry.get_refund(refund_id)
            elif tool == "get_refund_by_order" and order_id:
                data["refund"] = tool_registry.get_refund_by_order(order_id)
            elif tool == "get_refund_by_return" and return_id:
                data["refund"] = tool_registry.get_refund_by_return(return_id)
            elif tool == "get_customer" and customer_id:
                data["customer"] = tool_registry.get_customer(customer_id)
            elif tool == "get_customer_orders" and customer_id:
                data["customer_orders"] = tool_registry.get_customer_orders(customer_id)
        except Exception:
            pass

    return data


def _check_ownership(data: Dict[str, Any], caller_customer_id: Optional[str], decision: Optional[RouteDecision] = None) -> Optional[Any]:
    if not caller_customer_id or caller_customer_id.upper() in ("ADMIN", "GUEST"):
        return None

    for entity_type in ["order", "payment", "return", "refund"]:
        record = data.get(entity_type)
        if record and isinstance(record, dict):
            owner = record.get("customer_id")
            if not owner and "order_id" in record:
                try:
                    o_rec = tool_registry.get_order(record["order_id"])
                    if o_rec and isinstance(o_rec, dict):
                        owner = o_rec.get("customer_id")
                except Exception:
                    pass
            if owner and owner.upper() != caller_customer_id.upper():
                return security_validator.validate_resource_ownership(
                    caller_customer_id=caller_customer_id,
                    resource_owner_id=owner,
                    resource_type=entity_type
                )

    if decision and decision.intent and decision.intent.entities and caller_customer_id and caller_customer_id != "GUEST":
        cust_orders = tool_registry.get_customer_orders(caller_customer_id)
        cust_order_ids = [
            o.get("order_id") if isinstance(o, dict) else getattr(o, "order_id", None)
            for o in (cust_orders or [])
        ]
        
        req_order_id = decision.intent.entities.get("order_id")
        if req_order_id:
            try:
                o_rec = tool_registry.get_order(req_order_id)
                if o_rec and isinstance(o_rec, dict):
                    owner = o_rec.get("customer_id")
                    if owner and owner.upper() != caller_customer_id.upper():
                        return security_validator.validate_resource_ownership(
                            caller_customer_id=caller_customer_id,
                            resource_owner_id=owner,
                            resource_type="order"
                        )
                elif req_order_id not in cust_order_ids:
                    return security_validator.validate_resource_ownership(
                        caller_customer_id=caller_customer_id,
                        resource_owner_id="OTHER_CUSTOMER",
                        resource_type="order"
                    )
            except Exception:
                pass

        req_return_id = decision.intent.entities.get("return_id")
        if req_return_id:
            try:
                r_rec = tool_registry.get_return(req_return_id)
                if r_rec and isinstance(r_rec, dict):
                    owner = r_rec.get("customer_id")
                    if owner and owner.upper() != caller_customer_id.upper():
                        return security_validator.validate_resource_ownership(
                            caller_customer_id=caller_customer_id,
                            resource_owner_id=owner,
                            resource_type="return"
                        )
            except Exception:
                pass

        req_refund_id = decision.intent.entities.get("refund_id")
        if req_refund_id:
            try:
                rf_rec = tool_registry.get_refund(req_refund_id)
                if rf_rec and isinstance(rf_rec, dict):
                    owner = rf_rec.get("customer_id")
                    if owner and owner.upper() != caller_customer_id.upper():
                        return security_validator.validate_resource_ownership(
                            caller_customer_id=caller_customer_id,
                            resource_owner_id=owner,
                            resource_type="refund"
                        )
            except Exception:
                pass

    return None


def aggregate_responses(state: GraphState) -> GraphState:
    sub_questions: List[SubQuestion] = state.get("sub_questions", [])
    responses: List[AIResponse] = [sq["response"] for sq in sub_questions if sq.get("response")]

    if not responses:
        raise RuntimeError("aggregate_responses called with no sub-answers to merge")

    # Prioritize SECURITY denial or HUMAN escalation if present in sub-responses
    for r in responses:
        if r.route_type in ("SECURITY", "HUMAN"):
            state["final_response"] = r
            return state

    if len(responses) == 1:
        state["final_response"] = responses[0]
        return state

    merged_content = "\n\n".join(r.content for r in responses)
    merged_citations = [c for r in responses for c in r.rag_citations]
    merged_structured: dict = {}
    for r in responses:
        merged_structured.update(r.structured_data)
    merged_grounded = all(r.is_grounded for r in responses)
    merged_violations = [v for r in responses for v in r.grounding_violations]

    state["final_response"] = AIResponse(
        content=merged_content,
        route_type="HYBRID",
        structured_data=merged_structured,
        rag_citations=merged_citations,
        is_grounded=merged_grounded,
        grounding_violations=merged_violations,
        is_llm_generated=any(r.is_llm_generated for r in responses),
    )
    return state


def handle_human_escalation(state: GraphState) -> GraphState:
    decision = state["escalation_decision"]
    resp = response_synthesizer.synthesize_escalation_response(decision)
    state["final_response"] = resp
    return state

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
    sub_objs = _hybrid_split(state["raw_query"], use_llm=state.get("use_llm", False))
    state["sub_questions"] = sub_objs
    return state


def _extract_entities_from_text(text: str) -> Dict[str, str]:
    entities = {}
    ord_match = re.search(r'\b(?:ORD|ORDER)[-_# ]*(\d{1,5})\b', text, re.IGNORECASE)
    if ord_match:
        entities["order_id"] = f"ORD-{ord_match.group(1).zfill(3)}"

    prod_match = re.search(r'\b(?:PROD|PRODUCT)[-_# ]*(\d{1,5})\b', text, re.IGNORECASE)
    if prod_match:
        entities["product_id"] = f"PROD-{prod_match.group(1).zfill(3)}"

    ret_match = re.search(r'\b(?:RET|RETURN)[-_# ]*(\d{1,5})\b', text, re.IGNORECASE)
    if ret_match:
        entities["return_id"] = f"RET-{ret_match.group(1).zfill(3)}"

    ref_match = re.search(r'\b(?:REF|REFUND)[-_# ]*(\d{1,5})\b', text, re.IGNORECASE)
    if ref_match:
        entities["refund_id"] = f"REF-{ref_match.group(1).zfill(3)}"

    return entities


def _hybrid_split(text: str, use_llm: bool = False) -> List[Dict[str, Any]]:
    text_clean = text.strip()
    if not text_clean:
        return [{"id": "sq_1", "original_text": text, "normalized_text": text, "text": text, "entities": {}}]

    MAX_SUB_QUESTIONS = 5

    # 1. Fast-Path: single short question (< 8 words and no multi-clause triggers)
    words = text_clean.split()
    triggers = ["?", ";", "\n", " and ", ", and ", " also ", " additionally ", ", plus "]
    has_trigger = any(tr in text_clean.lower() for tr in triggers) or text_clean.count("?") > 1
    if len(words) < 8 and not has_trigger:
        entities = _extract_entities_from_text(text_clean)
        return [{
            "id": "sq_1",
            "original_text": text_clean,
            "normalized_text": text_clean,
            "text": text_clean,
            "entities": entities,
        }]

    # 2. Rule-Based Heuristic Parser
    parts: List[str] = []
    if ";" in text_clean:
        parts = [p.strip() for p in text_clean.split(";") if p.strip()]
    elif "\n" in text_clean:
        parts = [p.strip() for p in text_clean.split("\n") if p.strip()]
    else:
        pattern = r"\?+\s*(?=[A-Za-z0-9])|,\s*and\s+(?:can\s+i\s+|also\s+|additionally\s+)?|,\s*(?:also|additionally)\s+|\band\s+(?=(?:order|payment|shipment|return|refund|status|what|where|how|can\s+i|could\s+you|please|show|tell|connect|transfer|check|track|i\s+want|i\s+need|ord-|ret-|ref-|prod-)\b)|,\s+(?=(?:order|payment|shipment|return|refund|status|get\s+me|what|where|how|can|show|tell|connect|transfer|check|track|ord-|ret-|ref-|prod-)\b)"
        raw_parts = [p.strip(" ,.?") for p in re.split(pattern, text_clean, flags=re.IGNORECASE) if p.strip(" ,.?")]
        if len(raw_parts) > 1:
            parts = raw_parts
        elif text_clean.count("?") > 1:
            parts = [p.strip() + "?" for p in text_clean.split("?") if p.strip()]

    if not parts:
        parts = [text_clean]

    # Enforce MAX_SUB_QUESTIONS limit
    parts = parts[:MAX_SUB_QUESTIONS]

    # Deduplicate while preserving order
    seen = set()
    unique_parts = []
    for p in parts:
        p_norm = p.lower().strip(" ?,.")
        if p_norm not in seen:
            seen.add(p_norm)
            unique_parts.append(p)

    # Convert to structured SubQuestion objects & extract entities
    sub_questions = []

    for idx, p in enumerate(unique_parts):
        local_entities = _extract_entities_from_text(p)
        merged_entities = local_entities if len(unique_parts) > 1 else (_extract_entities_from_text(text_clean) or local_entities)

        sub_questions.append({
            "id": f"sq_{idx+1}",
            "original_text": p,
            "normalized_text": p,
            "text": p,
            "entities": merged_entities,
        })

    return sub_questions


def _naive_split(text: str) -> List[str]:
    sub_objs = _hybrid_split(text)
    return [sq["text"] for sq in sub_objs]


def handle_subquestions(state: GraphState) -> GraphState:
    conversation_id = state.get("conversation_id")
    customer_id = state.get("customer_id")

    ctx = context_manager.get_or_create(conversation_id=conversation_id) if conversation_id else None

    # Pre-turn slots
    active_order_id = state.get("active_order_id") or (ctx.active_order_id if ctx else None)
    active_product_id = state.get("active_product_id") or (ctx.active_product_id if ctx else None)
    active_return_id = state.get("active_return_id") or (ctx.active_return_id if ctx else None)
    active_refund_id = state.get("active_refund_id") or (ctx.active_refund_id if ctx else None)

    for idx, sub in enumerate(state["sub_questions"]):
        sub_text = sub.get("normalized_text") or sub.get("text", "")
        sub_id = sub.get("id") or f"sq_{idx+1}"
        sub["id"] = sub_id
        sub["original_text"] = sub.get("original_text") or sub_text
        sub["normalized_text"] = sub_text
        sub["text"] = sub_text

        # Sub-question specific context slots (scoped to entities in sub-question)
        sub_entities = sub.get("entities", {})
        sub_text_lower = sub_text.lower()
        context_keywords = ("it", "my order", "the order", "this order", "that order", "my return", "my refund", "my item", "where is it", "cancel it", "return it")
        uses_context = any(kw in sub_text_lower for kw in context_keywords)

        sub_slots = {
            "order_id": sub_entities.get("order_id") or (active_order_id if uses_context else None),
            "product_id": sub_entities.get("product_id") or (active_product_id if uses_context else None),
            "return_id": sub_entities.get("return_id") or (active_return_id if uses_context else None),
            "refund_id": sub_entities.get("refund_id") or (active_refund_id if uses_context else None),
        }
        sub["context_reference"] = dict(sub_slots)

        try:
            route_decision = _router.route(
                query=sub_text,
                customer_id=customer_id,
                conversation_id=conversation_id,
                context_slots=sub_slots,
                use_llm=state.get("use_llm"),
            )
            sub["route"] = route_decision
            sub["intent"] = route_decision.intent

            # Handle Human escalation route
            if route_decision.route_type == RouteType.HUMAN:
                state["escalated"] = True
                if not state.get("escalation_decision"):
                    state["escalation_decision"] = route_decision.escalation_decision

            # Execute route handler
            response = _handle_single_route(route_decision, sub_text, state)

            if response.route_type == "SECURITY":
                sub["authorization_status"] = "DENIED"
                sub["execution_status"] = "SECURITY_BLOCKED"
            else:
                sub["authorization_status"] = "ALLOWED"
                sub["execution_status"] = "SUCCESS"

            sub["response"] = response

        except Exception as exc:
            sub["execution_status"] = "FAILED"
            sub["error"] = str(exc)
            sub["response"] = AIResponse(
                content="I encountered an issue retrieving information for this part of your query.",
                route_type="HYBRID",
                is_grounded=False,
            )

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

    clean_q = (route_decision.rag_query or query).strip(" ?!.")
    rag_res = rag_pipeline.query(clean_q)
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


def _extract_product_search_term(query: str) -> str:
    q_clean = query.lower()
    q_clean_alpha = " ".join(re.sub(r"[^\w\s]", " ", q_clean).split())

    known_categories = [
        ("mobiles & tablets", ["mobiles and tablets", "mobiles & tablets", "mobile & tablet", "mobile and tablet", "mobiles", "mobile", "tablets", "tablet", "smartphones", "smartphone", "phones", "phone"]),
        ("laptops & computers", ["laptops and computers", "laptops & computers", "laptop & computer", "laptop and computer", "laptops", "laptop", "computers", "computer"]),
        ("audio & headphones", ["audio and headphones", "audio & headphones", "audio", "headphones", "headphone", "earbuds", "earbud", "earphones", "earphone", "speakers", "speaker"]),
        ("kitchen & dining", ["kitchen and dining", "kitchen & dining", "kitchen", "dining"]),
        ("home furniture", ["home furniture", "furniture"]),
        ("home appliances", ["home appliances", "appliances", "appliance"]),
        ("mens clothing", [
            "men's clothing", "mens clothing", "men clothing",
            "gifting for men", "gifts for men", "gift for men", "products for men",
            "for men", "for mens", "for him", "men's", "mens", "men", "male"
        ]),
        ("womens clothing", [
            "women's clothing", "womens clothing", "women clothing",
            "gifting for women", "gifts for women", "gift for women", "products for women",
            "for women", "for womens", "for her", "women's", "womens", "women",
            "female", "ladies"
        ]),
        ("footwear", ["footwear", "footwears", "shoes", "shoe", "sandals"]),
        ("electronics", ["electronics", "electronic"]),
        ("home & kitchen", ["home and kitchen", "home & kitchen"]),
        ("fashion & lifestyle", ["fashion and lifestyle", "fashion & lifestyle", "fashion", "lifestyle"]),
    ]

    for cat_name, aliases in known_categories:
        for alias in aliases:
            if re.search(r"\b" + re.escape(alias) + r"\b", q_clean_alpha):
                if cat_name == "mens clothing":
                    return "men"
                if cat_name == "womens clothing":
                    return "women"
                return alias

    term = q_clean_alpha
    for stopw in [
        "do you have", "do you sell", "do you offer", "what kind of", "show me",
        "tell me about", "tell me", "give me info of", "give me info on", "give me info",
        "give me", "i want", "can i buy", "can i see", "search for", "search",
        "gifting for", "gifts for", "gift for", "gifting", "gifts", "gift", "ideas for",
        "info of", "info on", "information of", "information on", "details of",
        "details on", "information", "info", "details", "detail", "every", "all of", "all",
        "what", "are", "available", "products", "product", "items", "item", "in our store",
        "in your store", "in the store", "in store", "for sale", "for", "in", "at", "the",
        "a", "an", "your", "our", "category", "categories", "of", "about"
    ]:
        term = re.sub(r"\b" + re.escape(stopw) + r"\b", " ", term)
    term = " ".join(term.split()).strip()
    return term or q_clean.strip()


def _execute_tools(decision: RouteDecision, state: GraphState, ctx: Any) -> Dict[str, Any]:
    data = {}
    ent = decision.intent.entities if decision.intent else {}
    q_lower = (state.get("raw_query") or "").lower()
    has_explicit_order = bool(re.search(r'\bORD-\d+\b', state.get("raw_query") or "", re.IGNORECASE))

    # Ensure product queries do not collide with all_orders
    is_product_focused = any(w in q_lower for w in ["product", "products", "item", "items", "catalog", "browse"]) and not any(w in q_lower for w in ["my order", "my orders", "ordered", "order items", "inside order"])

    is_all_orders_query = not is_product_focused and not has_explicit_order and (
        any(w in q_lower for w in [
            "all order", "all orders", "my orders", "my all orders",
            "where is my orders", "where are my orders", "what are my orders",
            "show my orders", "show all orders", "list my orders", "list all orders",
            "every order", "order history", "how many orders", "all of my orders",
            "info of my all orders", "info of all my orders", "info on all my orders"
        ]) or (
            ("where" in q_lower or "track" in q_lower or "status" in q_lower or "give" in q_lower or "show" in q_lower)
            and ("orders" in q_lower or "my all orders" in q_lower)
        )
    )

    has_category_filter = any(w in q_lower for w in [
        "electronic", "electronics", "mobile", "mobiles", "tablet", "tablets",
        "phone", "phones", "laptop", "laptops", "computer", "computers", "audio",
        "headphone", "headphones", "earbud", "earbuds", "speaker", "speakers",
        "kitchen", "cookware", "furniture", "chair", "desk", "appliance", "appliances",
        "clothing", "shirt", "jeans", "dress", "footwear", "shoe", "shoes",
        "men", "mens", "women", "womens", "male", "female"
    ])

    has_targeted_filter = has_category_filter or any(p in q_lower for p in [" for ", " in ", " under ", " with ", " called ", " named "])

    q_words = set(re.sub(r'[^\w\s]', ' ', q_lower).split())
    has_product_word = bool(q_words & {"product", "products", "item", "items", "catalog"})
    has_all_or_info = bool(q_words & {"all", "every", "info", "information", "details", "list", "show", "browse", "catalog", "sell", "have", "offer"})

    is_all_products_query = (
        (has_product_word and has_all_or_info and not has_targeted_filter) or
        any(w in q_lower for w in [
            "all product", "all products", "catalog", "what products", "list products",
            "show products", "show me products", "products do you have", "what do you sell",
            "browse products", "show all products", "give me info of all products",
            "give me info of your all products", "all products info", "product list",
            "available products", "tell me all products", "what can i buy", "what items do you sell",
            "all info of your products", "all info of products", "info of your products", "info of products",
            "your products", "info about products"
        ])
    ) and not has_targeted_filter

    if is_all_orders_query:
        order_id = None
    else:
        order_id = ent.get("order_id") or state.get("active_order_id") or getattr(ctx, "active_order_id", None) or state.get("last_order_id") or getattr(ctx, "last_order_id", None)

    product_id = ent.get("product_id") or state.get("active_product_id") or getattr(ctx, "active_product_id", None) or state.get("last_product_id") or getattr(ctx, "last_product_id", None)
    return_id = ent.get("return_id") or state.get("active_return_id") or getattr(ctx, "active_return_id", None)
    refund_id = ent.get("refund_id") or state.get("active_refund_id") or getattr(ctx, "active_refund_id", None)
    seller_id = ent.get("seller_id")
    customer_id = ent.get("customer_id") or state.get("customer_id") or getattr(ctx, "customer_id", None)

    # Pre-fetch detailed customer orders if is_all_orders_query
    if is_all_orders_query and customer_id:
        try:
            c_orders = tool_registry.get_customer_orders(customer_id)
            if c_orders:
                detailed_orders = []
                for o in c_orders:
                    oid = o.get("order_id") if isinstance(o, dict) else getattr(o, "order_id", None)
                    if oid:
                        o_dict = dict(o) if isinstance(o, dict) else o.__dict__.copy()
                        o_dict["shipment"] = tool_registry.get_shipment_by_order(oid)
                        o_dict["items"] = tool_registry.get_order_items(oid)
                        detailed_orders.append(o_dict)
                    data["customer_orders_detailed"] = detailed_orders
                    data["customer_orders"] = c_orders
        except Exception:
            pass

    for tool in decision.target_tools:
        try:
            if tool == "list_all_products" or (is_all_products_query and tool in ("get_product", "search_products")):
                data["catalog_products"] = tool_registry.list_all_products()
            elif tool == "search_products":
                if data.get("product") or data.get("catalog_products"):
                    continue
                if is_all_products_query:
                    data["catalog_products"] = tool_registry.list_all_products()
                    continue
                if product_id:
                    full_p = tool_registry.get_product(product_id)
                    if full_p:
                        data["product"] = full_p
                        if ctx:
                            ctx.active_product_id = product_id
                        continue

                search_term = _extract_product_search_term(q_lower)
                matches = tool_registry.search_products(search_term, limit=40)
                if not matches and search_term.endswith("s"):
                    matches = tool_registry.search_products(search_term[:-1], limit=40)
                if not matches:
                    stopwords_fallback = {
                        "what", "kind", "have", "sell", "offer", "show", "tell", "about",
                        "your", "store", "shop", "every", "products", "product", "items",
                        "item", "give", "info", "with", "from", "that", "this", "help",
                        "need", "want", "more", "some", "like", "also", "please", "could",
                        "would", "category", "categories", "many", "much", "good", "best"
                    }
                    words = [w for w in re.sub(r'[^\w\s]', '', q_lower).split() if len(w) > 3 and w not in stopwords_fallback]
                    for w in words:
                        matches = tool_registry.search_products(w, limit=40)
                        if not matches and w.endswith("s"):
                            matches = tool_registry.search_products(w[:-1], limit=40)
                        if matches:
                            break
                if matches:
                    is_info_query = any(k in q_lower for k in ["info", "tell me about", "details", "detail", "about", "specs", "specification", "specifications", "price", "warranty", "return", "cost", "feature"])
                    is_category_browsing = any(k in q_lower for k in ["show all", "list", "browse", "every product", "products in", "products for", "category", "categories"])
                    if len(matches) == 1 or (is_info_query and not is_category_browsing):
                        best_match = matches[0]
                        if len(matches) > 1 and search_term:
                            best_match = next((m for m in matches if search_term == m["name"].lower() or search_term in m["name"].lower()), None)
                            if not best_match:
                                best_match = next((m for m in matches if m["name"].lower() in search_term), matches[0])
                        target_pid = best_match["product_id"]
                        full_p = tool_registry.get_product(target_pid)
                        if full_p:
                            data["product"] = full_p
                            if ctx:
                                ctx.active_product_id = target_pid
                        else:
                            data["search_products"] = matches
                    else:
                        data["search_products"] = matches
                elif is_all_products_query:
                    data["catalog_products"] = tool_registry.list_all_products()
                else:
                    data["search_products"] = []
            elif tool == "get_order":
                if order_id:
                    data["order"] = tool_registry.get_order(order_id, customer_id=customer_id)
                elif not is_all_orders_query and customer_id:
                    c_orders = tool_registry.get_customer_orders(customer_id)
                    if c_orders:
                        data["customer_orders"] = c_orders
                        first_ord = c_orders[0]
                        oid = first_ord.get("order_id") if isinstance(first_ord, dict) else getattr(first_ord, "order_id", None)
                        if oid:
                            data["order"] = tool_registry.get_order(oid, customer_id=customer_id)
            elif tool == "get_order_items" and order_id:
                data["order_items"] = tool_registry.get_order_items(order_id)
            elif tool == "get_shipment_by_order":
                if order_id:
                    data["shipment"] = tool_registry.get_shipment_by_order(order_id)
                elif not is_all_orders_query and customer_id:
                    c_orders = tool_registry.get_customer_orders(customer_id)
                    if c_orders:
                        data["customer_orders"] = c_orders
                        first_ord = c_orders[0]
                        oid = first_ord.get("order_id") if isinstance(first_ord, dict) else getattr(first_ord, "order_id", None)
                        if oid:
                            data["shipment"] = tool_registry.get_shipment_by_order(oid)
            elif tool == "get_customer_orders" and customer_id:
                c_orders = tool_registry.get_customer_orders(customer_id)
                data["customer_orders"] = c_orders
                if not data.get("customer_orders_detailed") and c_orders:
                    detailed_orders = []
                    for o in c_orders:
                        oid = o.get("order_id") if isinstance(o, dict) else getattr(o, "order_id", None)
                        if oid:
                            o_dict = dict(o) if isinstance(o, dict) else o.__dict__.copy()
                            o_dict["shipment"] = tool_registry.get_shipment_by_order(oid)
                            o_dict["items"] = tool_registry.get_order_items(oid)
                            detailed_orders.append(o_dict)
                    data["customer_orders_detailed"] = detailed_orders
            elif tool == "get_shipment_by_tracking" and ent.get("tracking_number"):
                data["shipment"] = tool_registry.get_shipment_by_tracking(ent["tracking_number"])
            elif tool == "get_product":
                if product_id:
                    data["product"] = tool_registry.get_product(product_id)
                elif is_all_products_query:
                    data["catalog_products"] = tool_registry.list_all_products()
                else:
                    search_term = _extract_product_search_term(q_lower)
                    matches = tool_registry.search_products(search_term, limit=40)
                    if not matches and search_term.endswith("s"):
                        matches = tool_registry.search_products(search_term[:-1], limit=40)
                    if not matches:
                        stopwords_fallback = {
                            "what", "kind", "have", "sell", "offer", "show", "tell", "about",
                            "your", "store", "shop", "every", "products", "product", "items",
                            "item", "give", "info", "with", "from", "that", "this", "help",
                            "need", "want", "more", "some", "like", "also", "please", "could",
                            "would", "category", "categories", "many", "much", "good", "best"
                        }
                        words = [w for w in re.sub(r'[^\w\s]', '', q_lower).split() if len(w) > 3 and w not in stopwords_fallback]
                        for w in words:
                            matches = tool_registry.search_products(w, limit=40)
                            if not matches and w.endswith("s"):
                                matches = tool_registry.search_products(w[:-1], limit=40)
                            if matches:
                                break
                    if matches:
                        is_info_query = any(k in q_lower for k in ["info", "tell me about", "details", "detail", "about", "specs", "specification", "specifications", "price", "warranty", "return", "cost", "feature"])
                        is_category_browsing = any(k in q_lower for k in ["show all", "list", "browse", "every product", "products in", "products for", "category", "categories"])
                        if len(matches) == 1 or (is_info_query and not is_category_browsing):
                            best_match = matches[0]
                            if len(matches) > 1 and search_term:
                                best_match = next((m for m in matches if search_term == m["name"].lower() or search_term in m["name"].lower() or m["name"].lower() in search_term), matches[0])
                            target_pid = best_match["product_id"]
                            full_p = tool_registry.get_product(target_pid)
                            if full_p:
                                data["product"] = full_p
                                if ctx:
                                    ctx.active_product_id = target_pid
                            else:
                                data["search_products"] = matches
                        else:
                            data["search_products"] = matches
                    elif is_all_products_query:
                        data["catalog_products"] = tool_registry.list_all_products()
                    else:
                        data["search_products"] = []
            elif tool == "get_seller" and seller_id:
                data["seller"] = tool_registry.get_seller(seller_id)
            elif tool == "get_seller" and product_id and not seller_id:
                data["seller"] = tool_registry.get_seller_by_product(product_id)
            elif tool == "get_payment_by_order":
                if order_id:
                    data["payment"] = tool_registry.get_payment_by_order(order_id)
                elif customer_id:
                    c_orders = tool_registry.get_customer_orders(customer_id)
                    if c_orders:
                        data["customer_orders"] = c_orders
                        first_ord = c_orders[0]
                        oid = first_ord.get("order_id") if isinstance(first_ord, dict) else getattr(first_ord, "order_id", None)
                        if oid:
                            data["payment"] = tool_registry.get_payment_by_order(oid)
            elif tool == "get_payment" and ent.get("payment_id"):
                data["payment"] = tool_registry.get_payment(ent["payment_id"])
            elif tool == "get_return" and return_id:
                data["return"] = tool_registry.get_return(return_id)
            elif tool == "get_return_by_order":
                if order_id:
                    data["return"] = tool_registry.get_return_by_order(order_id)
                elif customer_id:
                    c_orders = tool_registry.get_customer_orders(customer_id)
                    if c_orders:
                        data["customer_orders"] = c_orders
                        first_ord = c_orders[0]
                        oid = first_ord.get("order_id") if isinstance(first_ord, dict) else getattr(first_ord, "order_id", None)
                        if oid:
                            data["return"] = tool_registry.get_return_by_order(oid)
            elif tool == "get_refund" and refund_id:
                data["refund"] = tool_registry.get_refund(refund_id)
            elif tool == "get_refund_by_order":
                if order_id:
                    data["refund"] = tool_registry.get_refund_by_order(order_id)
                elif customer_id:
                    c_orders = tool_registry.get_customer_orders(customer_id)
                    if c_orders:
                        data["customer_orders"] = c_orders
                        first_ord = c_orders[0]
                        oid = first_ord.get("order_id") if isinstance(first_ord, dict) else getattr(first_ord, "order_id", None)
                        if oid:
                            data["refund"] = tool_registry.get_refund_by_order(oid)
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
                if o_rec:
                    owner = o_rec.get("customer_id") if isinstance(o_rec, dict) else getattr(o_rec, "customer_id", None)
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
                if r_rec:
                    owner = r_rec.get("customer_id") if isinstance(r_rec, dict) else getattr(r_rec, "customer_id", None)
                    if owner and owner.upper() != caller_customer_id.upper():
                        return security_validator.validate_resource_ownership(
                            caller_customer_id=caller_customer_id,
                            resource_owner_id=owner,
                            resource_type="return"
                        )
                else:
                    return security_validator.validate_resource_ownership(
                        caller_customer_id=caller_customer_id,
                        resource_owner_id="OTHER_CUSTOMER",
                        resource_type="return"
                    )
            except Exception:
                pass

        req_refund_id = decision.intent.entities.get("refund_id")
        if req_refund_id:
            try:
                rf_rec = tool_registry.get_refund(req_refund_id)
                if rf_rec:
                    owner = rf_rec.get("customer_id") if isinstance(rf_rec, dict) else getattr(rf_rec, "customer_id", None)
                    if owner and owner.upper() != caller_customer_id.upper():
                        return security_validator.validate_resource_ownership(
                            caller_customer_id=caller_customer_id,
                            resource_owner_id=owner,
                            resource_type="refund"
                        )
                else:
                    return security_validator.validate_resource_ownership(
                        caller_customer_id=caller_customer_id,
                        resource_owner_id="OTHER_CUSTOMER",
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

    # Tag citations on each sub-question response with source sub-question index and text
    for idx, sq in enumerate(sub_questions):
        resp = sq.get("response")
        if not resp or not resp.rag_citations:
            continue
        sub_text = sq.get("text", "")
        tagged_citations = []
        for citation in resp.rag_citations:
            c_copy = dict(citation)
            c_copy["sub_question_index"] = idx
            c_copy["sub_question_text"] = sub_text
            tagged_citations.append(c_copy)
        resp.rag_citations = tagged_citations

    if len(responses) == 1:
        state["final_response"] = responses[0]
        return state

    # Separate responses by route type
    info_responses = [r for r in responses if r.route_type not in ("SECURITY", "HUMAN")]
    escalation_responses = [r for r in responses if r.route_type == "HUMAN"]
    security_responses = [r for r in responses if r.route_type == "SECURITY"]

    # Prompt injections override everything — zero tolerance for malicious attacks or leaks
    injection_responses = [
        r for r in security_responses
        if r.security_decision and getattr(r.security_decision, "reason", "") in ("PROMPT_INJECTION", "INJECTION_ATTACK", "DATA_EXFILTRATION")
    ]
    if injection_responses:
        state["final_response"] = injection_responses[0]
        return state

    if not info_responses and not escalation_responses and security_responses:
        state["final_response"] = security_responses[0]
        return state

    if not info_responses and escalation_responses:
        state["final_response"] = escalation_responses[0]
        return state

    # Combine content from all responses in sub-question order
    content_blocks = []
    for sq in sub_questions:
        resp = sq.get("response")
        if resp and resp.content:
            content_blocks.append(resp.content)

    merged_content = "\n\n".join(content_blocks)
    merged_citations = [c for r in responses for c in (r.rag_citations or [])]
    merged_structured: dict = {}
    for r in responses:
        if r.structured_data:
            merged_structured.update(r.structured_data)

    merged_grounded = all(r.is_grounded for r in responses)
    merged_violations = [v for r in responses for v in (r.grounding_violations or [])]

    esc_dec = state.get("escalation_decision")
    if not esc_dec and escalation_responses:
        esc_dec = escalation_responses[0].escalation_decision

    overall_route = "HUMAN" if escalation_responses else "HYBRID"
    state["final_response"] = AIResponse(
        content=merged_content,
        route_type=overall_route,
        structured_data=merged_structured,
        rag_citations=merged_citations,
        escalation_decision=esc_dec,
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

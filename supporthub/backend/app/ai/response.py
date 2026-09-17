"""Response builder and ground-truth synthesizer with LLM reasoning and deterministic validation."""
import json
import logging
import re
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from app.ai.security import SecurityDecision
from app.ai.escalation import EscalationDecision
from app.ai.grounding import grounding_validator
from app.ai.llm import llm_client
from app.ai.prompts.response import RESPONSE_SYNTHESIS_PROMPT

logger = logging.getLogger("supporthub.response")


# ─── W02: Payment failure-reason sanitizer ───────────────────────────────────
# Raw payment records may contain internal auth/banking terminology (e.g.
# "Bank server timeout during OTP authentication"). This should NOT be surfaced
# verbatim to customers — it is neither a credential leak nor fully user-facing.
# We normalise only the wording; the original record is never mutated.
_FAILURE_REASON_REWRITES = [
    # OTP / authentication step references
    ("otp authentication", "bank authentication step"),
    ("otp verification", "bank authentication step"),
    (" otp", " authentication step"),
    # Other tech-internal phrases that are confusing to customers
    ("3ds authentication", "bank authentication step"),
    ("3d secure", "bank authentication step"),
]

def _sanitize_payment_failure_reason(raw_reason: str) -> str:
    """Return a customer-facing version of a payment failure reason.

    Replaces internal authentication terminology with neutral phrasing.
    The original payment record is never altered.
    """
    if not raw_reason:
        return raw_reason
    sanitized = raw_reason
    lower = raw_reason.lower()
    for pattern, replacement in _FAILURE_REASON_REWRITES:
        if pattern in lower:
            # Case-insensitive replace while preserving the rest of the string
            import re as _re
            sanitized = _re.sub(
                _re.escape(pattern), replacement, sanitized, flags=_re.IGNORECASE
            )
            # Refresh lower for subsequent patterns
            lower = sanitized.lower()
    return sanitized
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class AIResponse:
    """Consolidated response object emitted by the SupportHub AI Orchestrator."""
    content: str
    route_type: str              # "STRUCTURED", "RAG", "HYBRID", "SECURITY", "HUMAN"
    structured_data: Dict[str, Any] = field(default_factory=dict)
    rag_citations: List[Dict[str, Any]] = field(default_factory=list)
    security_decision: Optional[SecurityDecision] = None
    escalation_decision: Optional[EscalationDecision] = None
    is_grounded: bool = True
    grounding_violations: List[str] = field(default_factory=list)
    context_updates: Dict[str, Any] = field(default_factory=dict)
    is_llm_generated: bool = False


class ResponseSynthesizer:
    """Synthesizes factual, grounded customer support responses deterministically."""

    def synthesize_security_response(self, decision: SecurityDecision) -> AIResponse:
        """Construct response for security denial / credential interception."""
        return AIResponse(
            content=decision.message,
            route_type="SECURITY",
            security_decision=decision,
            is_grounded=True
        )

    def synthesize_escalation_response(self, decision: EscalationDecision) -> AIResponse:
        """Construct response when escalating to a human support agent."""
        msg = (
            f"I have transferred your request to our senior support team ({decision.priority} priority: {decision.escalation_summary}). "
            "A human support representative is reviewing your case details and will assist you shortly."
        )
        return AIResponse(
            content=msg,
            route_type="HUMAN",
            escalation_decision=decision,
            is_grounded=True
        )

    def synthesize_rag_response(self, query: str, rag_result: Dict[str, Any]) -> AIResponse:
        """Construct response using retrieved RAG knowledge."""
        if not rag_result.get("has_knowledge"):
            return AIResponse(
                content="I could not find specific documentation regarding your query in our knowledge base. Would you like me to connect you with an agent?",
                route_type="RAG",
                is_grounded=False
            )

        citations = rag_result.get("citations", [])
        top_citation = citations[0] if citations else {}
        top_score = top_citation.get("score", 0.0)

        # Off-topic and irrelevant query guard: redirect politely to ShopKart support
        q_low = query.lower()
        off_topic_phrases = [
            "poem", "poetry", "write a song", "write a story", "tell me a joke", "tell a joke", "joke",
            "weather", "recipe", "cook", "who are you", "what is your name", "capital of", "who invented",
            "who is the president", "who won", "write code", "python script", "meaning of life",
            "how many countries", "history of", "tell me about history", "translate", "solve this math"
        ]
        core_keywords = [
            "order", "refund", "return", "cancel", "ship", "deliver", "delivery", "pay", "payment",
            "prod-", "ord-", "track", "warranty", "invoice", "address", "account", "login", "password",
            "otp", "item", "exchange", "replacement", "shopkart", "policy", "seller", "cart", "price",
            "discount", "coupon", "cod", "cost", "stock", "spec", "brand", "help", "support", "service",
            "faq", "guideline", "shipping", "charge", "upi", "card", "bank",
            # Product category keywords
            "product", "shirt", "jeans", "denim", "dress", "kurta", "trousers", "shoes", "shoe",
            "laptop", "phone", "mobile", "tablet", "headphone", "earbuds", "speaker", "monitor",
            "keyboard", "mouse", "tv", "television", "vacuum", "purifier", "fryer", "mixer",
            "chair", "desk", "table", "furniture", "cookware", "bottle", "serum", "cream", "shampoo",
            "sunscreen", "trimmer", "toothbrush", "dryer", "microphone", "cooktop", "induction",
            # Info / enquiry phrases
            "info", "information", "all info", "give me info", "full info", "details",
        ]
        is_off_topic = any(w in q_low for w in off_topic_phrases)
        has_core_kw = any(k in q_low for k in core_keywords)

        if is_off_topic or not has_core_kw or top_score <= 0.0:
            return AIResponse(
                content="I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?",
                route_type="RAG",
                rag_citations=citations,
                is_grounded=True
            )

        source_title = top_citation.get("title", "ShopKart Policy")
        source_id = top_citation.get("source_id", "KB")

        chunks = rag_result.get("retrieved_chunks", [])
        body_text = chunks[0].text if chunks else ""

        content = f"According to ShopKart's {source_title} ({source_id}):\n\n{body_text}"
        return AIResponse(
            content=content,
            route_type="RAG",
            rag_citations=citations,
            is_grounded=True
        )

    def synthesize_structured_response(
        self,
        intent_name: str,
        data: Dict[str, Any],
        query: str
    ) -> AIResponse:
        q_lower = query.lower()
        has_explicit_order_id = bool(re.search(r'\bORD-\d+\b', query, re.IGNORECASE))
        is_all_orders_query = not has_explicit_order_id and (
            any(w in q_lower for w in [
                "all order", "all orders", "my orders", "all info", "my all orders",
                "where is my orders", "where are my orders", "what are my orders",
                "show my orders", "show all orders", "list my orders", "list all orders",
                "every order", "order history", "how many orders", "all of my orders",
                "info of my all orders", "info of all my orders", "info on all my orders"
            ]) or (
                ("where" in q_lower or "track" in q_lower or "status" in q_lower or "info" in q_lower or "give" in q_lower or "show" in q_lower)
                and ("orders" in q_lower or "my all orders" in q_lower)
            )
        )

        # All Orders Inquiry (Multi-order response)
        c_orders = data.get("customer_orders_detailed") or data.get("customer_orders")
        if (is_all_orders_query or ("customer_orders" in data and "order" not in data)) and c_orders is not None:
            if not c_orders:
                return AIResponse(
                    content="You do not have any orders placed under your account yet.",
                    route_type="STRUCTURED",
                    structured_data=data,
                    is_grounded=True
                )

            sections = []
            for ord_item in c_orders:
                oid = ord_item.get("order_id") if isinstance(ord_item, dict) else getattr(ord_item, "order_id", "")
                ostatus = ord_item.get("status") if isinstance(ord_item, dict) else getattr(ord_item, "status", "UNKNOWN")
                ototal = ord_item.get("total_amount", 0) if isinstance(ord_item, dict) else getattr(ord_item, "total_amount", 0)

                shipment = ord_item.get("shipment")
                if not shipment and oid:
                    try:
                        from app.ai.tools import tool_registry
                        shipment = tool_registry.get_shipment_by_order(oid)
                    except Exception:
                        shipment = None

                items = ord_item.get("items")
                if items is None and oid:
                    try:
                        from app.ai.tools import tool_registry
                        items = tool_registry.get_order_items(oid)
                    except Exception:
                        items = []

                header_line = f"Order {oid} status: **{ostatus}** (Total: ₹{ototal:,.2f})."

                order_block = [header_line]
                if items:
                    item_strs = []
                    for it in items:
                        p_name = it.get("product_name") if isinstance(it, dict) else getattr(it, "product_name", "Product")
                        qty = it.get("quantity", 1) if isinstance(it, dict) else getattr(it, "quantity", 1)
                        item_strs.append(f"{p_name} (Qty {qty})")
                    order_block.append(f"Items: {', '.join(item_strs)}.")

                if shipment:
                    s_id = shipment.get("shipment_id", "")
                    s_status = shipment.get("status", "")
                    s_carrier = shipment.get("carrier", "")
                    s_trk = shipment.get("tracking_number", "")
                    s_est = shipment.get("estimated_delivery_date") or shipment.get("actual_delivery_date") or ""
                    del_text = f", Estimated Delivery: {s_est}" if s_est else ""
                    if s_status.upper() == "DELIVERED" and shipment.get("actual_delivery_date"):
                        del_text = f", Estimated Delivery: {shipment.get('actual_delivery_date')}"
                    order_block.append(f"Shipment {s_id} for order {oid} is **{s_status}** via {s_carrier} (Tracking: {s_trk}{del_text}).")
                else:
                    order_block.append(f"Shipment for order {oid} is **PROCESSING** (preparing for dispatch).")

                sections.append("\n".join(order_block))

            content = "\n\n".join(sections)
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        is_product_info_query = any(w in q_lower for w in [
            "product", "products", "item", "items", "sku", "skus",
            "product info", "product information", "product detail", "product details",
            "itemized", "what did i order", "what is inside", "whats inside", "what items"
        ])

        # Multi-Entity Structured Aggregation
        active_entities = [k for k in ("order", "payment", "shipment", "return", "refund") if data.get(k)]
        if len(active_entities) > 1 and not is_product_info_query and ("and" in q_lower or "," in q_lower or intent_name == "UNKNOWN" or len(q_lower.split()) > 4):
            sections = []
            if "order" in data and data["order"]:
                o = data["order"]
                o_id = o.get('order_id') if isinstance(o, dict) else getattr(o, 'order_id', '')
                o_status = o.get('status') if isinstance(o, dict) else getattr(o, 'status', '')
                o_total = o.get('total_amount', 0) if isinstance(o, dict) else getattr(o, 'total_amount', 0)
                sections.append(f"Order {o_id} status: **{o_status}** (Total: ₹{o_total:,.2f}).")
            if "payment" in data and data["payment"]:
                pay = data["payment"]
                raw_fail = pay.get("failure_reason") or ""
                safe_fail = _sanitize_payment_failure_reason(raw_fail)
                fail_reason = f" Reason: {safe_fail}." if safe_fail else ""
                sections.append(f"Payment for order {pay.get('order_id')} is **{pay.get('status')}** via {pay.get('method')} (Ref: {pay.get('transaction_reference')}).{fail_reason}")
            if "shipment" in data and data["shipment"]:
                s = data["shipment"]
                sections.append(f"Shipment {s.get('shipment_id')} for order {s.get('order_id')} is **{s.get('status')}** via {s.get('carrier')} (Tracking: {s.get('tracking_number')}, Estimated Delivery: {s.get('estimated_delivery_date')}).")
            if "return" in data and data["return"]:
                ret = data["return"]
                sections.append(f"Return request {ret.get('return_id')} for order {ret.get('order_id')} is **{ret.get('status')}** (Reason: {ret.get('reason')}).")
            if "refund" in data and data["refund"]:
                ref = data["refund"]
                sections.append(f"Refund {ref.get('refund_id')} for order {ref.get('order_id')} is **{ref.get('status')}** (Amount: ₹{ref.get('refund_amount'):,.2f} via {ref.get('refund_method')}).")

            if sections:
                return AIResponse(
                    content="\n\n".join(sections),
                    route_type="STRUCTURED",
                    structured_data=data,
                    is_grounded=True
                )

        # Seller Priority
        if "seller" in data and data["seller"] and ("seller" in q_lower or "who sells" in q_lower or intent_name == "SELLER_INQUIRY"):
            sel = data["seller"]
            content = f"Seller: {sel.get('seller_name')} (Rating: {sel.get('rating')}/5.0, City: {sel.get('city')}, State: {sel.get('state')})."
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Refund Priority
        if "refund" in data and data["refund"] and ("refund" in q_lower or intent_name == "REFUND_INQUIRY"):
            ref = data["refund"]
            content = (
                f"Refund {ref.get('refund_id')} for order {ref.get('order_id')} is {ref.get('status')}. "
                f"Amount: ₹{ref.get('refund_amount'):,.2f} via {ref.get('refund_method')}. Expected date: {ref.get('expected_date')}."
            )
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Return Priority
        if "return" in data and data["return"] and ("return" in q_lower or intent_name == "RETURN_INQUIRY"):
            ret = data["return"]
            content = (
                f"Return request {ret.get('return_id')} for order {ret.get('order_id')} is {ret.get('status')}. "
                f"Reason: {ret.get('reason')}."
            )
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Shipment Priority
        if "shipment" in data and data["shipment"] and ("shipment" in q_lower or "tracking" in q_lower or "courier" in q_lower or intent_name == "SHIPMENT_INQUIRY") and not is_product_info_query:
            s = data["shipment"]
            content = (
                f"Shipment {s.get('shipment_id')} for order {s.get('order_id')} is {s.get('status')} via {s.get('carrier')}. "
                f"Tracking Number: {s.get('tracking_number')}. Estimated Delivery: {s.get('estimated_delivery_date')}."
            )
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        if intent_name == "SHIPMENT_INQUIRY" and ("shipment" not in data or not data["shipment"]) and not is_product_info_query:
            content = "I could not find an active shipment record for your account. Please provide your Order ID or Tracking Number if you need tracking details."
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Payment Priority
        if "payment" in data and data["payment"] and ("payment" in q_lower or "paid" in q_lower or intent_name == "PAYMENT_INQUIRY") and not is_product_info_query:
            pay = data["payment"]
            ref_info = ""
            if "refund" in data and data["refund"]:
                ref = data["refund"]
                ref_info = f" Associated Refund: {ref.get('refund_id')} is {ref.get('status')} (Amount: ₹{ref.get('refund_amount'):,.2f})."
            raw_fail = pay.get("failure_reason") or ""
            safe_fail = _sanitize_payment_failure_reason(raw_fail)
            fail_reason = f" Reason: {safe_fail}." if safe_fail else ""

            content = (
                f"Payment for order {pay.get('order_id')} is {pay.get('status')}. "
                f"Amount: ₹{pay.get('amount'):,.2f} via {pay.get('method')} (Ref: {pay.get('transaction_reference')}).{fail_reason}{ref_info}"
            )
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Customer Orders List / Ambiguity
        if "customer_orders" in data and data["customer_orders"] and "order" not in data:
            c_orders = data["customer_orders"]
            if isinstance(c_orders, list) and len(c_orders) > 0:
                if len(c_orders) == 1:
                    data["order"] = c_orders[0]
                else:
                    ord_ids = [o.get("order_id") for o in c_orders if isinstance(o, dict) and "order_id" in o]
                    content = f"You have multiple orders ({', '.join(ord_ids)}). Please specify which order ID you are inquiring about."
                    return AIResponse(
                        content=content,
                        route_type="STRUCTURED",
                        structured_data=data,
                        is_grounded=True
                    )

        # All Products Catalog Response
        if "catalog_products" in data and data["catalog_products"]:
            products = data["catalog_products"]
            by_category: Dict[str, list] = {}
            for prod in products:
                cat = prod.get("category_name") or "General"
                by_category.setdefault(cat, []).append(prod)

            sections = ["Here is an overview of popular products currently available in our ShopKart catalog:\n"]
            category_icons = {
                "Electronics": "⚡", "Mobiles": "📱", "Tablets": "📱", "Audio": "🎧",
                "Headphones": "🎧", "Computers": "💻", "Laptops": "💻",
                "Kitchen": "🍳", "Dining": "🍳", "Home & Kitchen": "🍳",
                "Furniture": "🪑", "Home Furniture": "🪑",
                "Appliances": "🏠", "Home Appliances": "🏠",
                "Men": "👔", "Women": "👗", "Clothing": "👕", "Fashion": "✨",
                "Footwear": "👟", "Shoes": "👟"
            }

            for cat_name, p_list in by_category.items():
                icon = next((v for k, v in category_icons.items() if k.lower() in cat_name.lower()), "🛍️")
                sections.append(f"### {icon} {cat_name}")
                for p in p_list:
                    p_id = p.get("product_id", "")
                    p_name = p.get("name", "Product")
                    p_price = p.get("price", 0)
                    p_disc = p.get("discount_percentage", 0)
                    p_stock = p.get("stock_quantity", 0)
                    p_status = "OUT_OF_STOCK" if p_stock <= 0 else p.get("availability_status", "IN_STOCK")
                    disc_str = f" ({p_disc}% off)" if p_disc > 0 else ""
                    sections.append(
                        f"• **{p_name}** (`{p_id}`) — **₹{p_price:,.2f}**{disc_str} | Status: *{p_status}* ({p_stock} in stock)"
                    )
                sections.append("")

            sections.append("💡 *Tip: Ask for full specs, pricing, or warranty details on any item by specifying its name or ID (e.g., `Tell me about PROD-001`).*")
            content = "\n".join(sections)
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Product Search / Category Filtered Results
        if "search_products" in data and data["search_products"] and "product" not in data:
            products = data["search_products"]
            is_info_q = any(k in q_lower for k in ["info", "tell me about", "details", "detail", "about", "specs", "specification", "specifications", "price", "warranty", "return policy", "spec", "cost", "feature"])
            is_multi_listing_q = any(k in q_lower for k in ["show all", "list", "browse", "catalog", "every product", "products in", "products for", "categories", "category"])
            if (len(products) == 1 or (is_info_q and not is_multi_listing_q)) and products:
                from app.ai.tools import tool_registry
                single_p = tool_registry.get_product(products[0]["product_id"])
                if single_p:
                    data["product"] = single_p
                    del data["search_products"]
                    return self.synthesize_structured_response(intent_name, data, query)

            by_category: Dict[str, list] = {}
            for prod in products:
                cat = prod.get("category_name") or "General"
                by_category.setdefault(cat, []).append(prod)

            category_icons = {
                "Electronics": "⚡", "Mobiles": "📱", "Tablets": "📱", "Audio": "🎧",
                "Headphones": "🎧", "Computers": "💻", "Laptops": "💻",
                "Kitchen": "🍳", "Dining": "🍳", "Home & Kitchen": "🍳",
                "Furniture": "🪑", "Home Furniture": "🪑",
                "Appliances": "🏠", "Home Appliances": "🏠",
                "Men": "👔", "Women": "👗", "Clothing": "👕", "Fashion": "✨",
                "Footwear": "👟", "Shoes": "👟"
            }

            if len(by_category) > 1:
                sections = [f"Found {len(products)} matching product(s) across {len(by_category)} categories in our store:\n"]
                for cat_name, p_list in by_category.items():
                    icon = next((v for k, v in category_icons.items() if k.lower() in cat_name.lower()), "🛍️")
                    sections.append(f"### {icon} {cat_name}")
                    for p in p_list:
                        p_id = p.get("product_id", "")
                        p_name = p.get("name", "Product")
                        p_brand = p.get("brand", "")
                        p_price = p.get("price", 0)
                        p_mrp = p.get("mrp", 0)
                        p_disc = p.get("discount_percentage", 0)
                        p_stock = p.get("stock_quantity", 0)
                        p_status = "OUT_OF_STOCK" if p_stock <= 0 else p.get("availability_status", "IN_STOCK")
                        disc_str = f" (MRP: ₹{p_mrp:,.2f}, {p_disc}% off)" if p_disc > 0 else ""
                        sections.append(
                            f"• **{p_name}** (`{p_id}`) by *{p_brand}* — **₹{p_price:,.2f}**{disc_str}\n"
                            f"   Status: *{p_status}* ({p_stock} available)"
                        )
                    sections.append("")
            else:
                sections = [f"Found {len(products)} matching product(s) in our store:\n"]
                for p in products:
                    p_id = p.get("product_id", "")
                    p_name = p.get("name", "Product")
                    p_brand = p.get("brand", "")
                    p_price = p.get("price", 0)
                    p_mrp = p.get("mrp", 0)
                    p_disc = p.get("discount_percentage", 0)
                    p_stock = p.get("stock_quantity", 0)
                    p_status = "OUT_OF_STOCK" if p_stock <= 0 else p.get("availability_status", "IN_STOCK")
                    p_cat = p.get("category_name", "")
                    disc_str = f" (MRP: ₹{p_mrp:,.2f}, {p_disc}% off)" if p_disc > 0 else ""
                    sections.append(
                        f"• **{p_name}** (`{p_id}`) by *{p_brand}* — **₹{p_price:,.2f}**{disc_str}\n"
                        f"   Category: {p_cat} | Status: *{p_status}* ({p_stock} available)"
                    )
            sections.append("💡 *Ask me about any specific Product ID or model for warranty, return policies, and full technical specifications!*")
            content = "\n".join(sections)
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Product Search / Category Filtered Results (Empty match fallback)
        if "search_products" in data and not data["search_products"] and "product" not in data:
            return AIResponse(
                content=(
                    "We couldn't find any products matching your query in our store.\n\n"
                    "💡 *You can ask 'Show all products' to explore our complete catalog, or browse popular categories like Mobiles, Laptops, Audio, Men's Clothing, Women's Clothing, Footwear, or Electronics.*"
                ),
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Product Response (Direct Product entity search e.g. PROD-001)
        if "product" in data and data["product"] and "order" not in data:
            p = data["product"]
            p_id = p.get('product_id') if isinstance(p, dict) else getattr(p, 'product_id', '')
            p_name = p.get('name') if isinstance(p, dict) else getattr(p, 'name', '')
            p_brand = p.get('brand') if isinstance(p, dict) else getattr(p, 'brand', '')
            p_price = p.get('price', 0) if isinstance(p, dict) else getattr(p, 'price', 0)
            p_mrp = p.get('mrp', 0) if isinstance(p, dict) else getattr(p, 'mrp', 0)
            p_disc = p.get('discount_percentage', 0) if isinstance(p, dict) else getattr(p, 'discount_percentage', 0)
            p_stock = p.get('stock_quantity', 0) if isinstance(p, dict) else getattr(p, 'stock_quantity', 0)
            p_avail_raw = p.get('availability_status') if isinstance(p, dict) else getattr(p, 'availability_status', '')
            p_avail = "OUT_OF_STOCK" if p_stock <= 0 else (p_avail_raw or "IN_STOCK")
            p_warranty_avail = p.get('warranty_available') if isinstance(p, dict) else getattr(p, 'warranty_available', False)
            p_warranty_period = p.get('warranty_period') if isinstance(p, dict) else getattr(p, 'warranty_period', None)
            p_return_eligible = p.get('return_eligible') if isinstance(p, dict) else getattr(p, 'return_eligible', True)
            p_return_window = p.get('return_window_days') if isinstance(p, dict) else getattr(p, 'return_window_days', 7)

            p_desc = p.get('description') if isinstance(p, dict) else getattr(p, 'description', '')
            p_company = p.get('company_id') if isinstance(p, dict) else getattr(p, 'company_id', '')
            p_seller = p.get('seller_id') if isinstance(p, dict) else getattr(p, 'seller_id', '')
            p_cat_id = p.get('category_id') if isinstance(p, dict) else getattr(p, 'category_id', '')
            p_cat_name = p.get('category_name') if isinstance(p, dict) else getattr(p, 'category_name', '')
            p_replacement_eligible = p.get('replacement_eligible') if isinstance(p, dict) else getattr(p, 'replacement_eligible', False)
            p_specs = p.get('specifications') if isinstance(p, dict) else getattr(p, 'specifications', {})

            if isinstance(p_specs, str):
                try:
                    import json
                    p_specs = json.loads(p_specs)
                except Exception:
                    p_specs = {}

            # Fallback for description/company/seller if missing from dict
            if (not p_desc or not p_company) and p_id:
                try:
                    from app.data_access.product_service import ProductService
                    full_p = ProductService().get_product(p_id)
                    if full_p:
                        if not p_desc:
                            p_desc = getattr(full_p, 'description', '')
                        if not p_company:
                            p_company = getattr(full_p, 'company_id', '')
                        if not p_seller:
                            p_seller = getattr(full_p, 'seller_id', '')
                except Exception:
                    pass

            q_low = query.lower()
            if "warranty" in q_low or "guarantee" in q_low:
                if p_warranty_avail and p_warranty_period:
                    content = (
                        f"Yes! **{p_name}** ({p_id}) comes with a **{p_warranty_period}**.\n"
                        f"Brand: {p_brand} • Price: ₹{p_price:,.2f} • Availability: {p_avail}."
                    )
                else:
                    content = (
                        f"Product **{p_name}** ({p_id}) does not include a separate manufacturer warranty.\n"
                        f"Brand: {p_brand} • Price: ₹{p_price:,.2f} • Availability: {p_avail}."
                    )
            elif "return" in q_low or "returnable" in q_low:
                status_str = f"eligible for return within {p_return_window} days" if p_return_eligible else "non-returnable"
                content = (
                    f"**{p_name}** ({p_id}) is **{status_str}**.\n"
                    f"Brand: {p_brand} • Price: ₹{p_price:,.2f} • Availability: {p_avail}."
                )
            else:
                lines = []
                lines.append(f"Product: **{p_name}** (`{p_id}`) by **{p_brand}**.")
                if p_cat_name or p_cat_id:
                    cat_display = f"{p_cat_name} (`{p_cat_id}`)" if (p_cat_name and p_cat_id) else (p_cat_name or f"`{p_cat_id}`")
                    lines.append(f"Category: {cat_display}")

                if p_desc:
                    lines.append("")
                    lines.append("📝 **Overview:**")
                    lines.append(p_desc)

                lines.append("")
                lines.append("💰 **Pricing & Availability:**")
                disc_str = f", Discount: {p_disc}%" if p_disc > 0 else ""
                lines.append(f"• **Price:** ₹{p_price:,.2f} (MRP: ₹{p_mrp:,.2f}{disc_str})")
                lines.append(f"• **Availability:** {p_avail} (In Stock: {p_stock})")

                if p_specs and isinstance(p_specs, dict) and len(p_specs) > 0:
                    lines.append("")
                    lines.append("⚙️ **Technical Specifications:**")
                    for k, v in p_specs.items():
                        lines.append(f"• **{k}:** {v}")

                lines.append("")
                lines.append("🛡️ **Policies & Store Details:**")
                if p_return_eligible:
                    repl_note = " (Replacement available)" if p_replacement_eligible else ""
                    lines.append(f"• **Return Policy:** Eligible for return within {p_return_window} days{repl_note}")
                else:
                    lines.append("• **Return Policy:** Non-returnable")

                if p_warranty_avail and p_warranty_period:
                    lines.append(f"• **Warranty:** {p_warranty_period}")
                else:
                    lines.append("• **Warranty:** Standard manufacturer coverage")

                ref_parts = []
                if p_seller:
                    ref_parts.append(f"Seller ID: `{p_seller}`")
                if p_company:
                    ref_parts.append(f"Company ID: `{p_company}`")
                if ref_parts:
                    lines.append(f"• **Reference IDs:** {' • '.join(ref_parts)}")

                content = "\n".join(lines)
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Order Response — query-aware: answer the SPECIFIC question asked
        if "order" in data and data["order"]:
            o = data["order"]
            o_id = o.get('order_id') if isinstance(o, dict) else getattr(o, 'order_id', '')
            o_status = o.get('status') if isinstance(o, dict) else getattr(o, 'status', '')
            o_total = o.get('total_amount', 0) if isinstance(o, dict) else getattr(o, 'total_amount', 0)

            items = data.get("order_items", [])
            if not items and o_id:
                try:
                    from app.ai.tools import tool_registry
                    items = tool_registry.get_order_items(o_id)
                    data["order_items"] = items
                except Exception:
                    items = []

            formatted_items = []
            for it in items:
                p_id = it.get('product_id') if isinstance(it, dict) else getattr(it, 'product_id', '')
                p_name = it.get('product_name') if isinstance(it, dict) else getattr(it, 'product_name', 'Product')
                qty = it.get('quantity') if isinstance(it, dict) else getattr(it, 'quantity', 1)
                unit_price = it.get('unit_price', 0) if isinstance(it, dict) else getattr(it, 'unit_price', 0)
                total_price = it.get('total_price', 0) if isinstance(it, dict) else getattr(it, 'total_price', 0)
                formatted_items.append(
                    f"• **{p_name}**\n"
                    f"   SKU: `{p_id}` • Qty: {qty} • Price: **₹{unit_price:,.2f}** (Total: **₹{total_price:,.2f}**)"
                )

            item_names = [
                f"{it.get('product_name', it.get('product_id', ''))} (Qty {it.get('quantity', 1)})" if isinstance(it, dict) else f"{getattr(it, 'product_id', '')} (Qty {getattr(it, 'quantity', 1)})"
                for it in items
            ] if items else []

            s = data.get("shipment")
            s_status = s.get('status') if isinstance(s, dict) else getattr(s, 'status', '') if s else ""
            s_carrier = s.get('carrier') if isinstance(s, dict) else getattr(s, 'carrier', '') if s else ""
            s_tracking = s.get('tracking_number') if isinstance(s, dict) else getattr(s, 'tracking_number', '') if s else ""
            s_est = s.get('estimated_delivery_date', 'N/A') if isinstance(s, dict) else getattr(s, 'estimated_delivery_date', 'N/A') if s else "N/A"

            # "product / item / sku / product info / product details / items in order" → focus on product line items
            if is_product_info_query:
                if formatted_items:
                    items_list_str = "\n\n".join(formatted_items)
                    content = (
                        f"Order **{o_id}** — Product Details\n\n"
                        f"📦 **Items Included:**\n"
                        f"{items_list_str}\n\n"
                        f"📌 **Order Summary:**\n"
                        f"• Status: **{o_status}**\n"
                        f"• Total Amount: **₹{o_total:,.2f}**"
                    )
                else:
                    content = (
                        f"Order **{o_id}** — Product Details\n\n"
                        f"• Status: **{o_status}**\n"
                        f"• Total Amount: **₹{o_total:,.2f}**\n\n"
                        f"No itemized product breakdown recorded."
                    )

            # "where is my order / where / tracking / shipment" → focus on location & carrier
            elif any(w in q_lower for w in ["where", "track", "tracking", "carrier", "location", "shipment", "courier", "delivery date", "when will"]):
                if s:
                    content = (
                        f"Your order {o_id} is currently **{s_status}** "
                        f"with {s_carrier} (Tracking: {s_tracking}). "
                        f"Estimated delivery: {s_est}."
                    )
                else:
                    content = (
                        f"Your order {o_id} is **{o_status}**. "
                        f"No active shipment tracking is available yet."
                    )

            # "price / cost / how much / total / amount" → focus on price & items
            elif any(w in q_lower for w in ["price", "cost", "how much", "total", "amount", "charge", "paid"]):
                if formatted_items:
                    items_str = "\n\n" + "\n".join(formatted_items)
                    content = f"Order **{o_id}** total is **₹{o_total:,.2f}**.{items_str}"
                else:
                    items_str = f" Items ordered: {', '.join(item_names)}." if item_names else ""
                    content = f"Order {o_id} total is **₹{o_total:,.2f}**.{items_str}"

            # "cancel / cancellation" → explain cancellation options for THIS specific order
            elif any(w in q_lower for w in ["cancel", "cancle", "cancellation"]):
                status = (o_status or "").upper()
                ship_status = (s_status or "").upper()

                if status in ["CANCELLED", "CANCELED"]:
                    content = f"Order **{o_id}** is already **CANCELLED**."
                elif status in ["DELIVERED"]:
                    content = f"Order **{o_id}** is already **DELIVERED** and cannot be cancelled. You can request a return within 7 days from **Returns & Refunds**."
                elif status in ["SHIPPED", "DISPATCHED", "IN_TRANSIT"] or ship_status in ["SHIPPED", "DISPATCHED", "IN_TRANSIT", "OUT_FOR_DELIVERY"]:
                    content = (
                        f"Order **{o_id}** is currently **{status or ship_status}**. "
                        f"Since it has already been dispatched, online self-service cancellation is locked. "
                        f"You can refuse delivery when the courier arrives or initiate a return after delivery."
                    )
                else:  # PLACED, CONFIRMED, PROCESSING
                    content = (
                        f"Order **{o_id}** is currently **{status}** (not yet dispatched). "
                        f"You can cancel this order free of charge directly from **My Orders** in your ShopKart profile, or ask our support team to process the cancellation."
                    )

            # "status / update / progress" → focus on order state
            elif any(w in q_lower for w in ["status", "update", "progress"]):
                ship_note = f" Shipped via {s_carrier} ({s_status})." if s else ""
                content = (
                    f"Order {o_id} status: **{o_status}**.{ship_note}"
                )

            # Default: concise general summary
            else:
                ship_info = (
                    f" Carrier: {s_carrier} (Tracking: {s_tracking}), Status: {s_status}."
                    if s else ""
                )
                items_info = f" Items: {', '.join(item_names)}." if item_names else ""
                content = (
                    f"Order {o_id} is currently **{o_status}** "
                    f"with a total of ₹{o_total:,.2f}.{ship_info}{items_info}"
                )

            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # If any single entity was found in data
        for k in ["seller", "shipment", "payment", "refund", "return", "product", "order"]:
            if k in data and data[k]:
                val = data[k]
                return AIResponse(
                    content=f"Record {k}: {val}",
                    route_type="STRUCTURED",
                    structured_data=data,
                    is_grounded=True
                )

        # Fallback if entity not found
        return AIResponse(
            content="I was unable to locate the requested record in our system. Please check the ID or contact support.",
            route_type="STRUCTURED",
            structured_data=data,
            is_grounded=False
        )

    def synthesize_hybrid_response(
        self,
        structured_data: Dict[str, Any],
        rag_result: Dict[str, Any],
        query: str
    ) -> AIResponse:
        """Construct response combining structured entity state and policy text."""
        citations = rag_result.get("citations", [])
        policy_title = citations[0]["title"] if citations else "Platform Policy"

        order = structured_data.get("order")
        product = structured_data.get("product")
        shipment = structured_data.get("shipment")
        refund = structured_data.get("refund")
        return_obj = structured_data.get("return")

        if not any([order, product, shipment, refund, return_obj]):
            # Missing entity in structured_data
            clarification = (
                "Please specify the Order ID or Product ID you wish to inquire about "
                "so I can check your account eligibility against our policies."
            )
            return AIResponse(
                content=clarification,
                route_type="HYBRID",
                structured_data=structured_data,
                rag_citations=citations,
                is_grounded=True
            )

        details = []
        if order:
            o_id = order.get('order_id') if isinstance(order, dict) else getattr(order, 'order_id', '')
            o_stat = order.get('status') if isinstance(order, dict) else getattr(order, 'status', '')
            details.append(f"Order {o_id} is currently {o_stat}")
        if product:
            p_name = product.get('name') if isinstance(product, dict) else getattr(product, 'name', '')
            p_price = product.get('price', 0) if isinstance(product, dict) else getattr(product, 'price', 0)
            details.append(f"Product {p_name} (Price: ₹{p_price:,.2f})")
        if shipment:
            s_stat = shipment.get('status') if isinstance(shipment, dict) else getattr(shipment, 'status', '')
            s_carr = shipment.get('carrier') if isinstance(shipment, dict) else getattr(shipment, 'carrier', '')
            details.append(f"Shipment status: {s_stat} via {s_carr}")
        if refund:
            r_id = refund.get('refund_id') if isinstance(refund, dict) else getattr(refund, 'refund_id', '')
            r_stat = refund.get('status') if isinstance(refund, dict) else getattr(refund, 'status', '')
            r_amt = refund.get('refund_amount', 0) if isinstance(refund, dict) else getattr(refund, 'refund_amount', getattr(refund, 'amount', 0))
            details.append(f"Refund {r_id} status: {r_stat} (Amount: ₹{r_amt:,.2f})")
        if return_obj:
            ret_id = return_obj.get('return_id') if isinstance(return_obj, dict) else getattr(return_obj, 'return_id', '')
            ret_stat = return_obj.get('status') if isinstance(return_obj, dict) else getattr(return_obj, 'status', '')
            details.append(f"Return {ret_id} status: {ret_stat}")

        entity_summary = ". ".join(details)
        policy_text = rag_result.get("retrieved_chunks", [None])[0]
        policy_snippet = policy_text.text if policy_text else ""

        # Custom handling for order cancellation queries in HYBRID route
        if order and any(w in query.lower() for w in ["cancel", "cancle", "cancellation"]):
            status = (order.get("status") or "").upper()
            ship_status = (shipment.get("status") or "").upper() if shipment else ""
            ord_id = order.get("order_id")
            if status in ["CANCELLED", "CANCELED"]:
                content = f"Order **{ord_id}** is already **CANCELLED**."
            elif status in ["DELIVERED"]:
                content = f"Order **{ord_id}** is currently **DELIVERED** and cannot be cancelled. You can request a return within 7 days from **Returns & Refunds**."
            elif status in ["SHIPPED", "DISPATCHED", "IN_TRANSIT"] or ship_status in ["SHIPPED", "DISPATCHED", "IN_TRANSIT", "OUT_FOR_DELIVERY"]:
                content = (
                    f"Order **{ord_id}** is currently **{status or ship_status}**. "
                    f"Since it has already been dispatched, online self-service cancellation is locked. "
                    f"You can refuse delivery when the courier arrives, or initiate a return after delivery."
                )
            else:  # PLACED, CONFIRMED, PROCESSING
                content = (
                    f"Order **{ord_id}** is currently **{status}** (not yet dispatched). "
                    f"You can cancel this order free of charge directly from **My Orders** in your ShopKart profile, or ask our support team to process the cancellation."
                )
            return AIResponse(
                content=content,
                route_type="HYBRID",
                structured_data=structured_data,
                rag_citations=citations,
                is_grounded=True
            )

        # Custom handling for product warranty queries in HYBRID route
        if product and any(w in query.lower() for w in ["warranty", "guarantee"]):
            p_name = product.get('name') if isinstance(product, dict) else getattr(product, 'name', '')
            p_id = product.get('product_id') if isinstance(product, dict) else getattr(product, 'product_id', '')
            p_warranty_avail = product.get('warranty_available') if isinstance(product, dict) else getattr(product, 'warranty_available', False)
            p_warranty_period = product.get('warranty_period') if isinstance(product, dict) else getattr(product, 'warranty_period', None)
            if p_warranty_avail and p_warranty_period:
                content = (
                    f"Yes! **{p_name}** ({p_id}) includes a **{p_warranty_period}**.\n\n"
                    f"To claim warranty support, please present your ShopKart invoice at an authorized brand service center, or contact our support team for warranty assistance."
                )
            else:
                content = (
                    f"Product **{p_name}** ({p_id}) does not include a separate manufacturer warranty.\n"
                    f"However, it is covered by ShopKart's standard return & replacement policy if it arrives defective or damaged."
                )
            return AIResponse(
                content=content,
                route_type="HYBRID",
                structured_data=structured_data,
                rag_citations=citations,
                is_grounded=True
            )

        # Custom handling for product return eligibility queries in HYBRID route
        if product and any(w in query.lower() for w in ["return", "returnable", "return window"]):
            p_name = product.get('name') if isinstance(product, dict) else getattr(product, 'name', '')
            p_id = product.get('product_id') if isinstance(product, dict) else getattr(product, 'product_id', '')
            p_ret_elig = product.get('return_eligible') if isinstance(product, dict) else getattr(product, 'return_eligible', True)
            p_ret_win = product.get('return_window_days') if isinstance(product, dict) else getattr(product, 'return_window_days', 7)
            if p_ret_elig:
                content = (
                    f"Yes, **{p_name}** ({p_id}) is eligible for return within **{p_ret_win} days** of delivery.\n\n"
                    f"Items must be unused, in original packaging with all tags intact. You can initiate a return directly from **My Orders**."
                )
            else:
                content = (
                    f"Product **{p_name}** ({p_id}) is marked as **Non-Returnable** for category hygiene or safety standards.\n"
                    f"If the item arrives damaged or defective, please contact support within 48 hours for a replacement."
                )
            return AIResponse(
                content=content,
                route_type="HYBRID",
                structured_data=structured_data,
                rag_citations=citations,
                is_grounded=True
            )

        # Custom handling for damaged product / refund requests in HYBRID route
        if any(w in query.lower() for w in ["damaged", "defective", "broken", "want a refund", "request a refund", "claim a refund", "refund for my order", "refund my order", "refund"]):
            # Check if customer explicitly requested an order ID in their query
            req_m = re.findall(r"\b(?:ORD|ORDER)[-_# ]*(\d{1,5})\b", query, re.IGNORECASE)
            req_order_id = f"ORD-{req_m[0].zfill(3)}" if req_m else None

            ord_id = order.get('order_id') if isinstance(order, dict) else getattr(order, 'order_id', None) if order else None

            # If customer specifically specified an order ID that doesn't exist or doesn't belong to them
            if req_order_id and (not ord_id or ord_id != req_order_id):
                content = (
                    f"I was unable to find order **{req_order_id}** under your account. "
                    f"Please verify the order number in **My Orders** or check if you placed it under a different account."
                )
                return AIResponse(
                    content=content,
                    route_type="HYBRID",
                    structured_data=structured_data,
                    rag_citations=citations,
                    is_grounded=True
                )

            ref_id = refund.get('refund_id') if isinstance(refund, dict) else getattr(refund, 'refund_id', None) if refund else None
            ret_id = return_obj.get('return_id') if isinstance(return_obj, dict) else getattr(return_obj, 'return_id', None) if return_obj else None

            if ref_id:
                r_stat = refund.get('status') if isinstance(refund, dict) else getattr(refund, 'status', '')
                r_amt = refund.get('refund_amount', 0) if isinstance(refund, dict) else getattr(refund, 'refund_amount', 0)
                content = (
                    f"A refund ({ref_id}) for order **{ord_id}** is currently in status **{r_stat}** (Amount: ₹{r_amt:,.2f}).\n\n"
                    f"Doorstep refunds are credited within 2 to 4 hours of physical pickup. Warehouse return refunds are credited within 24 to 48 hours."
                )
            elif ret_id:
                ret_stat = return_obj.get('status') if isinstance(return_obj, dict) else getattr(return_obj, 'status', '')
                content = (
                    f"Return request **{ret_id}** for order **{ord_id}** is currently **{ret_stat}**.\n\n"
                    f"Our courier partner will pick up the item and your replacement or refund will be initiated immediately upon pickup."
                )
            else:
                ord_ref = f"for order **{ord_id}** " if ord_id else ""
                content = (
                    f"If you received a damaged or defective product {ord_ref}, you are fully eligible for a **Free Replacement** or **Full Refund** under ShopKart's Return & Refund Policy.\n\n"
                    f"**How to request your replacement or refund:**\n"
                    f"1. Go to **My Orders** in your ShopKart profile.\n"
                    f"2. Select **'Request Return / Replacement'** on your delivered order.\n"
                    f"3. Select **'Damaged/Defective'** as the reason and choose **Replacement** or **Refund**.\n"
                    f"4. Our courier partner will pick up the item from your doorstep. Refunds are initiated within 2 to 4 hours of pickup."
                )
            return AIResponse(
                content=content,
                route_type="HYBRID",
                structured_data=structured_data,
                rag_citations=citations,
                is_grounded=True
            )

        chunks = rag_result.get("retrieved_chunks") or []
        policy_text = chunks[0] if chunks else None
        policy_snippet = policy_text.text if policy_text else ""

        if policy_snippet:
            content = (
                f"Your record: {entity_summary}.\n\n"
                f"According to ShopKart's {policy_title}:\n\n"
                f"{policy_snippet}"
            )
        else:
            content = f"Your record: {entity_summary}."
        return AIResponse(
            content=content,
            route_type="HYBRID",
            structured_data=structured_data,
            rag_citations=citations,
            is_grounded=True
        )


class LLMResponseSynthesizer:
    """Synthesizes customer answers using real LLM reasoning validated by GroundingValidator."""

    def __init__(self, fallback: Optional[ResponseSynthesizer] = None):
        self.fallback = fallback or ResponseSynthesizer()

    def synthesize(
        self,
        query: str,
        route_type: str,
        structured_data: Optional[Dict[str, Any]] = None,
        rag_result: Optional[Dict[str, Any]] = None,
        customer_id: str = "GUEST",
        customer_name: str = "Customer",
        conversation_history: str = "",
        security_decision: Optional[SecurityDecision] = None,
        escalation_decision: Optional[EscalationDecision] = None,
        use_llm: bool = True
    ) -> AIResponse:
        """Synthesize a verified, grounded AI response."""
        # 1. Security Denials & Escalations are deterministic
        if security_decision and not security_decision.is_allowed:
            return self.fallback.synthesize_security_response(security_decision)

        if escalation_decision and escalation_decision.should_escalate:
            return self.fallback.synthesize_escalation_response(escalation_decision)

        # 2. If LLM is disabled or offline, use deterministic synthesizer
        if not use_llm:
            if route_type == "RAG":
                return self.fallback.synthesize_rag_response(query, rag_result or {})
            elif route_type == "HYBRID":
                return self.fallback.synthesize_hybrid_response(structured_data or {}, rag_result or {}, query)
            else:
                return self.fallback.synthesize_structured_response("INQUIRY", structured_data or {}, query)

        # 3. Format context for LLM
        formatted_struct = json.dumps(structured_data, indent=2, default=str) if structured_data else "None"
        formatted_rag = ""
        citations = []
        if rag_result and rag_result.get("has_knowledge"):
            citations = rag_result.get("citations", [])
            chunks = rag_result.get("retrieved_chunks", [])
            for ch in chunks[:2]:
                formatted_rag += f"[{ch.source_id}] {ch.title}:\n{ch.text}\n\n"
        if not formatted_rag:
            formatted_rag = "None"

        prompt = RESPONSE_SYNTHESIS_PROMPT.format(
            query=query,
            customer_id=customer_id,
            customer_name=customer_name,
            structured_data=formatted_struct,
            rag_knowledge=formatted_rag,
            conversation_history=conversation_history or "None"
        )

        try:
            llm_resp = llm_client.generate(
                prompt=prompt,
                system_instruction="You are SupportHub AI. Answer the customer strictly using provided facts."
            )
            raw_text = llm_resp.content.strip()

            # 4. Grounding Validation
            grounding = grounding_validator.validate(
                response_text=raw_text,
                structured_data=structured_data,
                rag_citations=citations,
                query=query
            )

            if grounding.is_grounded:
                return AIResponse(
                    content=raw_text,
                    route_type=route_type,
                    structured_data=structured_data or {},
                    rag_citations=citations,
                    is_grounded=True,
                    is_llm_generated=True
                )
            else:
                logger.warning(f"LLM response failed grounding validation: {grounding.violations}. Falling back to deterministic.")
                # Fallback to deterministic synthesis if grounding fails
                det_resp = self._call_fallback(route_type, query, structured_data, rag_result)
                det_resp.grounding_violations = grounding.violations
                det_resp.is_grounded = True
                return det_resp

        except Exception as e:
            logger.warning(f"LLM response generation failed ({e}). Falling back to deterministic response.")
            return self._call_fallback(route_type, query, structured_data, rag_result)

    def _call_fallback(
        self,
        route_type: str,
        query: str,
        structured_data: Optional[Dict[str, Any]],
        rag_result: Optional[Dict[str, Any]]
    ) -> AIResponse:
        if route_type == "RAG":
            return self.fallback.synthesize_rag_response(query, rag_result or {})
        elif route_type == "HYBRID":
            return self.fallback.synthesize_hybrid_response(structured_data or {}, rag_result or {}, query)
        else:
            return self.fallback.synthesize_structured_response("INQUIRY", structured_data or {}, query)


# Global singletons
response_synthesizer = ResponseSynthesizer()
llm_response_synthesizer = LLMResponseSynthesizer(response_synthesizer)

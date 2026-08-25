"""Response builder and ground-truth synthesizer with LLM reasoning and deterministic validation."""
import json
import logging
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
        """Construct response from verified structured database records."""
        q_lower = query.lower()

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
        if "shipment" in data and data["shipment"] and ("shipment" in q_lower or "tracking" in q_lower or "courier" in q_lower or intent_name == "SHIPMENT_INQUIRY"):
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

        if intent_name == "SHIPMENT_INQUIRY" and ("shipment" not in data or not data["shipment"]):
            content = "I could not find an active shipment record for your account. Please provide your Order ID or Tracking Number if you need tracking details."
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Payment Priority
        if "payment" in data and data["payment"] and ("payment" in q_lower or "paid" in q_lower or intent_name == "PAYMENT_INQUIRY"):
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

        # Product Response
        if "product" in data and data["product"]:
            p = data["product"]
            p_name = p.get('name') if isinstance(p, dict) else getattr(p, 'name', '')
            p_brand = p.get('brand') if isinstance(p, dict) else getattr(p, 'brand', '')
            p_price = p.get('price', 0) if isinstance(p, dict) else getattr(p, 'price', 0)
            p_mrp = p.get('mrp', 0) if isinstance(p, dict) else getattr(p, 'mrp', 0)
            p_disc = p.get('discount_percentage', 0) if isinstance(p, dict) else getattr(p, 'discount_percentage', 0)
            p_avail = p.get('availability_status') if isinstance(p, dict) else getattr(p, 'availability_status', '')
            p_stock = p.get('stock_quantity') if isinstance(p, dict) else getattr(p, 'stock_quantity', 0)
            content = (
                f"Product: {p_name} by {p_brand}.\n"
                f"Price: ₹{p_price:,.2f} (MRP: ₹{p_mrp:,.2f}, Discount: {p_disc}%).\n"
                f"Availability: {p_avail} (In Stock: {p_stock})."
            )
            return AIResponse(
                content=content,
                route_type="STRUCTURED",
                structured_data=data,
                is_grounded=True
            )

        # Order Response — query-aware: answer the SPECIFIC question asked
        if "order" in data and data["order"]:
            o = data["order"]
            s = data.get("shipment")
            items = data.get("order_items", [])
            item_names = [
                f"{it.get('product_id') if isinstance(it, dict) else getattr(it, 'product_id', '')} (Qty {it.get('quantity') if isinstance(it, dict) else getattr(it, 'quantity', 1)})"
                for it in items
            ] if items else []

            o_id = o.get('order_id') if isinstance(o, dict) else getattr(o, 'order_id', '')
            o_status = o.get('status') if isinstance(o, dict) else getattr(o, 'status', '')
            o_total = o.get('total_amount', 0) if isinstance(o, dict) else getattr(o, 'total_amount', 0)

            s_status = s.get('status') if isinstance(s, dict) else getattr(s, 'status', '') if s else ""
            s_carrier = s.get('carrier') if isinstance(s, dict) else getattr(s, 'carrier', '') if s else ""
            s_tracking = s.get('tracking_number') if isinstance(s, dict) else getattr(s, 'tracking_number', '') if s else ""
            s_est = s.get('estimated_delivery_date', 'N/A') if isinstance(s, dict) else getattr(s, 'estimated_delivery_date', 'N/A') if s else "N/A"

            # "where is my order / where / tracking / shipment" → focus on location & carrier
            if any(w in q_lower for w in ["where", "track", "tracking", "carrier", "location", "shipment", "courier", "delivery date", "when will"]):
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
                items_str = f" Items ordered: {', '.join(item_names)}." if item_names else ""
                content = (
                    f"Order {o_id} total is **₹{o_total:,.2f}**.{items_str}"
                )

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

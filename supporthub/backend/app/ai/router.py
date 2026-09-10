"""AI Router for classifying queries into execution pathways."""
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any

from app.ai.intent import IntentCategory, IntentResult, intent_classifier, llm_intent_classifier, normalize_query_typos
from app.ai.security import SecurityDecision, security_validator
from app.ai.escalation import EscalationDecision, escalation_evaluator

logger = logging.getLogger("supporthub.router")


class RouteType(str, Enum):
    STRUCTURED = "STRUCTURED"
    RAG = "RAG"
    HYBRID = "HYBRID"
    SECURITY = "SECURITY"
    HUMAN = "HUMAN"


@dataclass
class RouteDecision:
    """Decision determining the execution pathway for a customer query."""
    route_type: RouteType
    intent: IntentResult
    target_tools: List[str] = field(default_factory=list)
    rag_query: Optional[str] = None
    security_decision: Optional[SecurityDecision] = None
    escalation_decision: Optional[EscalationDecision] = None
    rationale: str = ""


class AIRouter:
    """Routes incoming queries into STRUCTURED, RAG, HYBRID, SECURITY, or HUMAN pipelines."""

    def __init__(self, use_llm_intent: bool = False):
        self.classifier = intent_classifier
        self.llm_classifier = llm_intent_classifier
        self.security = security_validator
        self.escalator = escalation_evaluator
        self.use_llm_intent = use_llm_intent

    def route(
        self,
        query: str,
        customer_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        context_slots: Optional[Dict[str, Any]] = None,
        use_llm: Optional[bool] = None
    ) -> RouteDecision:
        """Evaluate query and context to generate a deterministic routing decision.
        
        SECURITY & ESCALATION GATES REMAIN AUTHORITATIVE BEFORE AND AFTER LLM PROCESSING.
        """
        # 1. Authoritative Security Check (Deterministic zero-trust gateway)
        sec_decision = self.security.validate_inbound_query(query, caller_customer_id=customer_id)
        if not sec_decision.is_allowed:
            return RouteDecision(
                route_type=RouteType.SECURITY,
                intent=IntentResult(category=IntentCategory.SECURITY, intent_name="SECURITY_DENIAL", confidence=1.0),
                security_decision=sec_decision,
                rationale=f"Security violation detected: {sec_decision.reason}"
            )

        # 2. Authoritative Escalation Check (Deterministic SLA & sentiment gate)
        esc_decision = self.escalator.evaluate(
            query=query,
            customer_id=customer_id,
            conversation_id=conversation_id,
            active_order_id=context_slots.get("order_id") if context_slots else None
        )
        if esc_decision.should_escalate:
            return RouteDecision(
                route_type=RouteType.HUMAN,
                intent=IntentResult(category=IntentCategory.ESCALATION, intent_name="HUMAN_ESCALATION", confidence=1.0),
                escalation_decision=esc_decision,
                rationale=f"Escalation condition met: {esc_decision.reason}"
            )

        # 3. Intent Classification (LLM or Deterministic)
        should_use_llm = self.use_llm_intent if use_llm is None else use_llm
        if should_use_llm:
            intent = self.llm_classifier.classify(
                query=query,
                customer_id=customer_id or "GUEST",
                active_order_id=context_slots.get("order_id") if context_slots else None,
                active_product_id=context_slots.get("product_id") if context_slots else None,
                active_return_id=context_slots.get("return_id") if context_slots else None,
                active_refund_id=context_slots.get("refund_id") if context_slots else None,
                context_slots=context_slots,
                use_llm=True
            )
        else:
            intent = self.classifier.classify(query, context_slots=context_slots)

        text = normalize_query_typos(query)

        # 4. Check for Hybrid Queries first if explicit entity or entity context or hybrid intent is present
        has_explicit_id = any(k in text for k in ["ord-", "prod-", "ret-", "ref-"])
        has_active_context_entity = bool(
            context_slots and (
                context_slots.get("order_id") or context_slots.get("product_id") or
                context_slots.get("return_id") or context_slots.get("refund_id")
            )
        )
        has_entity_ref = has_explicit_id or has_active_context_entity

        is_hybrid = False
        target_tools = []
        rag_query = None

        if ("can i cancel" in text or "cancel my" in text or "cancel order" in text or "i want to cancel" in text or "cancellation" in text or "cancel policy" in text) and (has_entity_ref or intent.category == IntentCategory.ORDERS):
            is_hybrid = True
            target_tools = ["get_order", "get_shipment_by_order"]
            rag_query = "Order cancellation policy before dispatch"
        elif ("can i return" in text or "return window" in text or ("return policy" in text and has_entity_ref) or "return request" in text or "return " in text) and (has_entity_ref or intent.category in (IntentCategory.RETURNS, IntentCategory.PRODUCT)):
            is_hybrid = True
            target_tools = ["get_order", "get_product", "get_return_by_order"]
            rag_query = "Return policy window and conditions"
        elif any(w in text for w in ["damaged", "defective", "broken", "want a refund", "request a refund", "claim a refund", "refund my order", "refund for my order", "how can i get a refund", "how do i get a refund", "how to get a refund", "get a refund", "can i get a refund", "need a refund"]) or (
            ("refund delayed" in text or ("refund policy" in text and has_entity_ref) or "refund timeline" in text or "taking so long to process" in text) and (has_entity_ref or intent.category in (IntentCategory.REFUNDS, IntentCategory.PAYMENTS))
        ):
            is_hybrid = True
            target_tools = ["get_order", "get_refund_by_order", "get_refund", "get_return_by_order"]
            rag_query = "Product Replacement and Exchange Process for damaged or defective items and refund policy"
        elif has_entity_ref and any(w in text for w in ["payment options", "payment methods", "payment supported", "how to pay"]):
            is_hybrid = True
            target_tools = ["get_order", "get_shipment_by_order", "get_payment_by_order"]
            rag_query = "Payment methods and accepted options policy"
        elif intent.category == IntentCategory.PRODUCT and any(w in text for w in ["warranty", "guarantee"]):
            is_hybrid = True
            target_tools = ["get_product"]
            rag_query = "ShopKart Warranty Policy and How to Claim Manufacturer Warranty"
        elif intent.category == IntentCategory.PRODUCT and any(w in text for w in ["return", "fit", "modal innerwear", "password", "reset"]):
            is_hybrid = True
            target_tools = ["get_product"]
            rag_query = "Product return policy and password reset guide"
        elif intent.category == IntentCategory.SHIPMENTS and "change delivery address" in text:
            is_hybrid = True
            target_tools = ["get_shipment_by_order"]
            rag_query = "How to change delivery address for order"
        elif intent.category == IntentCategory.PAYMENTS and "pending" in text:
            is_hybrid = True
            target_tools = ["get_payment_by_order"]
            rag_query = "Payment pending auto reconciliation"

        if is_hybrid:
            return RouteDecision(
                route_type=RouteType.HYBRID,
                intent=intent,
                target_tools=target_tools,
                rag_query=rag_query,
                security_decision=sec_decision,
                escalation_decision=esc_decision,
                rationale="Hybrid query requiring both transactional entity state and policy verification."
            )

        # 5. Pure RAG Knowledge Base Queries (Policies, Account How-Tos, FAQs)
        rag_patterns = [
            "cancellation policy", "cancellation rules", "cancel policy", "how does cancellation work",
            "return policy of shopkart", "return policy", "return window for electronics",
            "how long does a upi refund take", "upi refund",
            "how long does a refund take", "how long does it take to get a refund", "refund timeline",
            "when will i get my refund", "when will i receive my refund", "refund turnaround",
            "how does shopkart refund", "refund policy", "how do refunds work", "refund process",
            "how do i return an item", "until what point can an order be cancelled",
            "standard delivery take to metro", "how does shopkart refund money",
            "payment methods are supported", "forgot my shopkart password",
            "how do i reset it", "not receiving the login otp",
            "update my default delivery address", "how can i update",
            # General warranty policy patterns
            "warranty policy", "claim warranty", "warranty coverage", "how to claim warranty",
            # Damaged / defective / missing items
            "damaged product", "damaged item", "received broken", "defective item", "wrong product",
            "wrong item", "delivered but not received", "did not receive my order", "package not delivered",
            "delivery delayed", "order delayed", "shipment delayed",
            # Cancellation & Return guides
            "how to cancel an order", "cancel an order", "step-by-step guide to request a return",
            "exchange policy", "replacement policy",
            # Payment failure troubleshooting
            "payment declined", "payment failed", "why was my payment declined",
            "money deducted", "transaction failed", "card declined", "payment error", "deducted from bank",
            "what to do when payment fails", "payment unconfirmed",
            # W05: general payment-capability FAQ patterns
            "what payment methods", "which payment methods", "what payment options",
            "which payment options", "can i pay using", "can i pay with",
            "do you accept", "which cards", "cash on delivery",
            "payment options available", "modes of payment", "accepted payment",
            "payment modes", "how can i pay", "how do i pay",
        ]
        if any(pat in text for pat in rag_patterns) or intent.category in (IntentCategory.GENERAL_POLICY, IntentCategory.ACCOUNT) or intent.suggested_route == "RAG":
            rag_q = query
            if any(w in text for w in ["payment declined", "payment failed", "why was my payment declined", "money deducted", "transaction failed", "card declined"]):
                rag_q = "What to Do When Payment Fails or Money is Deducted and ShopKart Payment Policy"
            return RouteDecision(
                route_type=RouteType.RAG,
                intent=intent,
                rag_query=rag_q,
                security_decision=sec_decision,
                escalation_decision=esc_decision,
                rationale="General informational / policy query routed directly to RAG knowledge retrieval."
            )

        # 6. Structured Data Cases: Specific entity status, pricing, tracking
        is_all_prods = any(w in text for w in [
            "all product", "all products", "catalog", "what products", "list products",
            "show products", "show me products", "products do you have", "what do you sell",
            "browse products", "show all products", "give me info of all products",
            "all products info", "product list", "available products", "tell me all products",
            "what can i buy", "what items do you sell"
        ])
        is_prod_search = any(w in text for w in [
            "phone", "phones", "mobile", "laptop", "laptops", "headphone", "headphones",
            "tablet", "tablets", "cooktop", "induction", "keyboard", "mouse", "speaker",
            "do you have", "do you sell", "search product", "search for"
        ]) and intent.category == IntentCategory.PRODUCT and not has_explicit_id

        if is_all_prods:
            product_tools = ["list_all_products"]
        elif is_prod_search:
            product_tools = ["search_products"]
        else:
            product_tools = ["get_product", "search_products"]

        tools_map = {
            IntentCategory.PRODUCT: product_tools,
            IntentCategory.ORDERS: ["get_order", "get_shipment_by_order", "get_order_items", "get_customer_orders"],
            IntentCategory.PAYMENTS: ["get_payment_by_order", "get_refund_by_order", "get_payment"],
            IntentCategory.SHIPMENTS: ["get_shipment_by_order", "get_shipment_by_tracking", "get_customer_orders"],
            IntentCategory.RETURNS: ["get_return", "get_return_by_order"],
            IntentCategory.REFUNDS: ["get_refund", "get_refund_by_order", "get_refund_by_return", "get_payment_by_order", "get_order"],
            IntentCategory.SELLER: ["get_product", "get_seller"],
            IntentCategory.ACCOUNT: ["get_customer"],
            IntentCategory.MULTI_TURN: ["get_order", "get_shipment_by_order", "get_return_by_order", "get_refund_by_order"]
        }

        selected_tools = tools_map.get(intent.category, ["get_order"])
        return RouteDecision(
            route_type=RouteType.STRUCTURED,
            intent=intent,
            target_tools=selected_tools,
            security_decision=sec_decision,
            escalation_decision=esc_decision,
            rationale="Transactional entity query routed to structured data access services."
        )


ai_router = AIRouter(use_llm_intent=False)

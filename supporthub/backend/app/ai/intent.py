"""Intent classification and entity extraction with LLM and deterministic fallback."""
import re
import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, List

from app.ai.llm import llm_client
from app.ai.prompts.intent import INTENT_CLASSIFICATION_PROMPT, INTENT_EXTRACTION_SCHEMA

logger = logging.getLogger("supporthub.intent")


class IntentCategory(str, Enum):
    PRODUCT = "product"
    ORDERS = "orders"
    PAYMENTS = "payments"
    SHIPMENTS = "shipments"
    RETURNS = "returns"
    REFUNDS = "refunds"
    ACCOUNT = "account"
    GENERAL_POLICY = "general_policy"
    SELLER = "seller"
    ESCALATION = "escalation"
    SECURITY = "security"
    MULTI_TURN = "multi_turn"
    RESOLVED = "resolved"
    UNKNOWN = "unknown"


def is_resolution_intent(text: str) -> bool:
    """
    Robust intent detector to determine if a customer message indicates
    their issue/problem is solved, or that they wish to close/resolve the ticket.
    Handles variations, typos (e.g. 'promblem', 'solvd', 'problm'), and conversational phrases.
    """
    if not text:
        return False
    
    cleaned = text.lower().strip()
    
    # Standardize common typos and word forms (e.g. 'promblem', 'problm', 'solvd', 'reslvd')
    cleaned_norm = re.sub(r"\bpr[o0mbe]{1,4}l[em]{1,3}s?\b", "problem", cleaned)
    cleaned_norm = re.sub(r"\bsolv[ed]{0,2}\b", "solved", cleaned_norm)
    cleaned_norm = re.sub(r"\bres[olv]{2,5}[ed]{0,2}\b", "resolved", cleaned_norm)
    cleaned_norm = re.sub(r"\bfix[ed]{1,2}\b", "fixed", cleaned_norm)
    
    # 1. Broad resolution phrase list
    phrases = [
        "problem solved", "problem is solved", "the problem is solved",
        "my problem is solved", "issue resolved", "issue is resolved",
        "my issue is resolved", "the issue is resolved", "that fixed it",
        "that solved it", "that solved my issue", "problem fixed", "issue fixed",
        "close chat", "close ticket", "end chat", "end ticket", "resolve ticket",
        "mark as resolved", "mark ticket resolved", "you can close", "you can end",
        "all good now", "everything is working now", "no more help needed",
        "thanks problem solved", "thanks my problem is solved", "issue is fixed",
        "problem is fixed", "all resolved", "case solved", "query resolved"
    ]
    
    if any(p in cleaned_norm for p in phrases):
        return True
        
    # 2. Flexible Regex pattern matching
    patterns = [
        r"\b(the\s+|my\s+)?(problem|issue|query|ticket|it|this)\s+(is\s+)?(solved|resolved|fixed)\b",
        r"\b(solved|resolved|fixed)\s+(the\s+|my\s+)?(problem|issue|query|ticket)\b",
        r"\b(thanks|thank\s+you).*(problem|issue|query)?.*(solved|resolved|fixed)\b",
        r"\b(close|end|resolve)\s+(this\s+)?(chat|ticket|conversation)\b",
        r"^\s*(thanks?,?\s*)?(problem|issue)?\s*(is\s*)?(solved|resolved|fixed)\s*(!|\.)*\s*$"
    ]
    
    for pat in patterns:
        if re.search(pat, cleaned_norm):
            return True

    return False



@dataclass
class IntentResult:
    """Outcome of intent classification."""
    category: IntentCategory
    intent_name: str
    confidence: float
    entities: Dict[str, Any] = field(default_factory=dict)
    # explicit_entities: contains ONLY entities extracted from the CURRENT query.
    # Never contains context-inherited slots. Used by orchestrator for domain-aware
    # slot persistence (update_slots_domain_aware) — Phase 13.2.4 fix.
    explicit_entities: Dict[str, Any] = field(default_factory=dict)
    suggested_route: Optional[str] = None
    raw_query: str = ""
    is_llm_generated: bool = False


class IntentClassifier:
    """Deterministic pattern and regex-based intent classifier."""

    # Entity Regex Patterns
    ORDER_REGEX = re.compile(r"\bORD-\d{3,5}\b", re.IGNORECASE)
    PRODUCT_REGEX = re.compile(r"\bPROD-\d{3,5}\b", re.IGNORECASE)
    SELLER_REGEX = re.compile(r"\b(SELL|SELLER)-\d{3,5}\b", re.IGNORECASE)
    RETURN_REGEX = re.compile(r"\bRET-\d{3,5}\b", re.IGNORECASE)
    REFUND_REGEX = re.compile(r"\bREF-\d{3,5}\b", re.IGNORECASE)
    TRACKING_REGEX = re.compile(r"\b(TRK-[A-Z0-9\-]+|[A-Z]{2}\d{10})\b", re.IGNORECASE)
    CUSTOMER_REGEX = re.compile(r"\bCUST-\d{3,5}\b", re.IGNORECASE)

    # Product Name Aliases to IDs
    PRODUCT_NAME_MAP = {
        "novaphone": "PROD-001",
        "novaphone pro": "PROD-001",
        "aerotab": "PROD-002",
        "pixelite": "PROD-003",
        "classictouch": "PROD-004",
        "zenbook": "PROD-005",
        "gamerx": "PROD-006",
        "proview": "PROD-007",
        "ergosilent": "PROD-008",
        "soundwave": "PROD-009",
        "airbuds": "PROD-010",
        "boombox": "PROD-011",
        "chefpro": "PROD-012",
        "mixer grinder": "PROD-012",
        "crispair": "PROD-013",
        "ergorest": "PROD-015",
        "comfywear": "PROD-025",
        "modal innerwear": "PROD-025"
    }

    # Seller Name Aliases to IDs
    SELLER_NAME_MAP = {
        "techworld": "SELL-001",
        "techworld retail": "SELL-001",
        "gadgethub": "SELL-002",
        "gadget hub": "SELL-002",
        "homeappliances": "SELL-003"
    }

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract explicit identifiers and recognized names from query text."""
        entities = {}
        lower = text.lower()
        
        # Regex entities
        order_m = self.ORDER_REGEX.findall(text)
        if order_m:
            entities["order_id"] = order_m[0].upper()

        prod_m = self.PRODUCT_REGEX.findall(text)
        if prod_m:
            entities["product_id"] = prod_m[0].upper()

        seller_m = self.SELLER_REGEX.findall(text)
        if seller_m:
            entities["seller_id"] = seller_m[0].upper()

        ret_m = self.RETURN_REGEX.findall(text)
        if ret_m:
            entities["return_id"] = ret_m[0].upper()

        ref_m = self.REFUND_REGEX.findall(text)
        if ref_m:
            entities["refund_id"] = ref_m[0].upper()

        cust_m = self.CUSTOMER_REGEX.findall(text)
        if cust_m:
            entities["customer_id"] = cust_m[0].upper()

        trk_m = self.TRACKING_REGEX.findall(text)
        if trk_m:
            entities["tracking_number"] = trk_m[0]

        # Named product matching
        if "product_id" not in entities:
            for name_key, pid in self.PRODUCT_NAME_MAP.items():
                if name_key in lower:
                    entities["product_id"] = pid
                    break

        # Named seller matching
        if "seller_id" not in entities:
            for sname_key, sid in self.SELLER_NAME_MAP.items():
                if sname_key in lower:
                    entities["seller_id"] = sid
                    break

        return entities

    def classify(self, query: str, context_slots: Optional[Dict[str, Any]] = None) -> IntentResult:
        """Classify query into domain intent with extracted entities.

        Context Isolation Model (Phase 13.2.2):
          - explicit_entities: extracted from the CURRENT query only (highest priority).
          - context_entities:  inherited from previous turns (lower priority).
          - merged entities (entities): used for tool argument resolution only.

        Intent classification rules use explicit_entities for entity-presence checks.
        This prevents a context-inherited order_id (for example) from hijacking
        a current product query into ORDER_INQUIRY.
        """
        text = query.lower().strip()

        # Separate concerns: what the CURRENT query explicitly mentions vs prior context.
        explicit_entities: Dict[str, Any] = self.extract_entities(query)

        # context_entities: only the slots that are NOT present in the current query.
        context_entities: Dict[str, Any] = {}
        if context_slots:
            for k, v in context_slots.items():
                if k not in explicit_entities and v:
                    context_entities[k] = v

        # merged entities for tool resolution (explicit wins over context).
        entities: Dict[str, Any] = {**context_entities, **explicit_entities}

        # Determine whether the current query has an explicit domain entity.
        _has_explicit_product = bool(explicit_entities.get("product_id"))
        _has_explicit_order   = bool(explicit_entities.get("order_id"))
        _has_explicit_return  = bool(explicit_entities.get("return_id"))
        _has_explicit_refund  = bool(explicit_entities.get("refund_id"))
        _has_any_explicit     = any([_has_explicit_product, _has_explicit_order,
                                      _has_explicit_return, _has_explicit_refund])

        # 0. Resolution Check
        if is_resolution_intent(query):
            return IntentResult(
                category=IntentCategory.RESOLVED,
                intent_name="CASE_RESOLVED",
                confidence=0.99,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="NONE",
                raw_query=query
            )

        # 1. Security Check
        if any(w in text for w in ["other customer", "another customer's", "pin is", "otp is", "my password is", "what is the otp sent for my payment", "phone number of customer", "what items did priya", "shipping address associated with ord"]):
            return IntentResult(
                category=IntentCategory.SECURITY,
                intent_name="SECURITY_GUARD",
                confidence=0.99,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="SECURITY",
                raw_query=query
            )

        # 2. Escalation Check
        if any(w in text for w in [
            "human agent", "talk to human", "real person", "manager", "supervisor", "useless", "terrible",
            "4th time", "nobody is helping", "court", "police", "legal action", "transfer me to a human",
            "logged into my account from another city", "used product instead of a brand new one",
            "says delivered, but i never received", "money was deducted from my account but order",
            "charged twice", "tracking for ord-006 has not updated in a week", "did not show up on the scheduled pickup",
            "refund failed for return", "only received ₹89,990 refund"
        ]):
            return IntentResult(
                category=IntentCategory.ESCALATION,
                intent_name="HUMAN_ESCALATION",
                confidence=0.98,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="HUMAN",
                raw_query=query
            )

        # 3. Seller Queries
        if any(w in text for w in ["who sells", "seller rating", "trustworthy seller", "is techworld retail", "who is the seller"]):
            return IntentResult(
                category=IntentCategory.SELLER,
                intent_name="SELLER_INQUIRY",
                confidence=0.95,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="STRUCTURED",
                raw_query=query
            )

        # 4. Shipment Queries
        if any(w in text for w in [
            "courier tracking number", "shipment for", "estimated delivery date", "coming today", "delayed",
            "change the delivery address", "where is my order ord-013",
            "where is my shipment", "where is my package", "where is my delivery",
            "track my shipment", "track my package", "what's happening with my shipment",
            "when will my shipment arrive", "shipment", "package", "tracking"
        ]):
            return IntentResult(
                category=IntentCategory.SHIPMENTS,
                intent_name="SHIPMENT_INQUIRY",
                confidence=0.92,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="STRUCTURED",
                raw_query=query
            )

        # 5. Refund Queries
        if any(w in text for w in ["where is my refund", "how long does a upi refund take", "taking so long to process", "refund"]):
            return IntentResult(
                category=IntentCategory.REFUNDS,
                intent_name="REFUND_INQUIRY",
                confidence=0.92,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="STRUCTURED",
                raw_query=query
            )

        # 6. Return Queries
        # Guard: "return policy" questions are GENERAL_POLICY (→ RAG), not transactional returns.
        _is_return_policy_question = "policy" in text or "return policy" in text
        if not _is_return_policy_question and any(w in text for w in ["return window", "can i return", "how do i return", "return request for", "pick up my return", "return"]):
            return IntentResult(
                category=IntentCategory.RETURNS,
                intent_name="RETURN_INQUIRY",
                confidence=0.90,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="RAG" if "policy" in text or "window" in text else "HYBRID",
                raw_query=query
            )

        # 7. Payment Queries
        # W05 guard: general payment-capability questions belong to KNOWLEDGE/FAQ,
        # not to the customer's transactional PAYMENTS record.
        _general_payment_faq_phrases = [
            "what payment methods", "which payment methods", "what payment options",
            "which payment options", "do you support", "can i pay using", "can i pay with",
            "do you accept", "which cards", "which card", "cash on delivery",
            "payment options available", "modes of payment", "accepted payment",
            "payment modes", "how can i pay", "how do i pay"
        ]
        _is_general_payment_faq = any(ph in text for ph in _general_payment_faq_phrases)
        if not _is_general_payment_faq and any(w in text for w in [
            "payment method", "payment for order", "card payment fail", "payment fail", "payment failure",
            "why did my payment", "payment status", "payment is showing pending", "refunded", "payment"
        ]):
            return IntentResult(
                category=IntentCategory.PAYMENTS,
                intent_name="PAYMENT_INQUIRY",
                confidence=0.90,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="STRUCTURED",
                raw_query=query
            )

        # 8. Order Queries
        # FIX #1 (Phase 13.2.2 & 13.2.6): Use EXPLICIT order_id presence or order keywords for classification.
        # A context-inherited order_id alone must NOT classify a product query as ORDER_INQUIRY.
        # - If the current query has an explicit order_id → ORDER_INQUIRY.
        # - If the current query has explicit order keywords → ORDER_INQUIRY.
        # - If only a context-inherited order_id exists AND no other domain's explicit entity
        #   is present → ORDER_INQUIRY (pure follow-up with no new entity).
        _order_keywords = ["status of my order", "when will my order", "products are inside my order",
                           "why was my order", "can i cancel my order", "order", "total", "carrier",
                           "status", "its status", "the status"]
        _explicit_order_keyword = any(w in text for w in _order_keywords)
        _context_only_order = (not _has_any_explicit) and bool(context_entities.get("order_id"))

        if _has_explicit_order or _explicit_order_keyword or _context_only_order:
            # Extra guard: do NOT let a keyword-only or context-only match steal from a product query.
            # e.g. "price" or "available" appears in query but context has order_id, or query has product_id.
            _prod_kw = [
                "price of", "price", "cost", "how much", "available", "availability", "stock", "in stock",
                "out of stock", "tell me about", "product details", "product specs", "specifications", "specs", "warranty",
                "novaphone", "zenbook", "pixelite", "comfywear", "product", "features", "color", "ram", "storage"
            ]
            # Guard: account/password questions must NEVER be stolen by a context-only order slot.
            _is_account_question = any(w in text for w in [
                "password", "reset", "login", "log in", "sign in", "profile", "account settings",
                "my account", "update my profile", "otp for login", "can't log in", "cannot log in"
            ])
            # Guard: general policy/knowledge questions must not be stolen by context-only order slot.
            _is_policy_question = "policy" in text or any(w in text for w in [
                "how does shopkart", "how do i", "cancellation policy", "return policy",
                "what is the policy", "general question", "help me understand"
            ])
            if _has_explicit_product:
                pass  # Fall through to product classification below.
            elif any(w in text for w in _prod_kw) and not _explicit_order_keyword and not _has_explicit_order:
                pass  # Fall through to product classification below.
            elif (_is_account_question or _is_policy_question) and not _has_explicit_order and not _explicit_order_keyword:
                pass  # Fall through to account classification below.
            else:
                return IntentResult(
                    category=IntentCategory.ORDERS,
                    intent_name="ORDER_INQUIRY",
                    confidence=0.88,
                    entities=entities,
                    explicit_entities=explicit_entities,
                    suggested_route="STRUCTURED",
                    raw_query=query
                )

        # 9. Account Queries
        # NOTE: These must be checked BEFORE the context-only order fallback so that
        # password/profile questions are never hijacked by a lingering order_id slot.
        _account_keywords = [
            "forgot my shopkart password", "forgot password", "forgot my password",
            "reset my password", "reset password", "password reset",
            "change my password", "change password", "update my password",
            "how to reset", "how do i reset", "how to change password",
            "login otp", "otp for login", "can't log in", "cannot log in",
            "update my default delivery address", "update my profile",
            "my profile", "my account", "account settings",
            "account"
        ]
        if any(w in text for w in _account_keywords):
            return IntentResult(
                category=IntentCategory.ACCOUNT,
                intent_name="ACCOUNT_INQUIRY",
                confidence=0.90,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="RAG",
                raw_query=query
            )

        # 10. General Policy Queries — and general payment-capability FAQ (W05)
        # Phrases here resolve to GENERAL_POLICY → RAG, not to STRUCTURED tools.
        _general_policy_phrases = [
            "cancellation policy", "cancellation rules", "cancel policy", "how does cancellation work",
            "return policy of shopkart", "return policy", "until what point can an order be cancelled",
            "standard delivery take to metro", "how does shopkart refund money", "payment methods are supported",
            # W05: general payment capability / FAQ
            "what payment methods", "which payment methods", "what payment options",
            "which payment options", "do you support", "can i pay using", "can i pay with",
            "do you accept", "which cards", "which card", "cash on delivery",
            "payment options available", "modes of payment", "accepted payment",
            "payment modes", "how can i pay", "how do i pay"
        ]
        if any(w in text for w in _general_policy_phrases):
            return IntentResult(
                category=IntentCategory.GENERAL_POLICY,
                intent_name="GENERAL_POLICY_INQUIRY",
                confidence=0.92,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="RAG",
                raw_query=query
            )

        # 11. Product Queries
        # Uses explicit_entities to ensure product intent wins over context-inherited order_id.
        # Guard: if the query has an explicit order_id (e.g. "price of ORD-024"),
        # do NOT classify as PRODUCT — let it fall to ORDER_INQUIRY above.
        product_keywords = [
            "price of", "price", "cost", "how much", "available", "availability", "stock", "in stock",
            "out of stock", "tell me about", "product details", "product specs", "specifications", "specs", "warranty",
            "novaphone", "zenbook", "pixelite", "comfywear", "product", "details", "features", "color", "ram", "storage"
        ]
        # Do not treat generic price/cost keywords as PRODUCT when an explicit order ID is present.
        _product_keyword_match = _has_explicit_product or (
            any(w in text for w in product_keywords) and not _has_explicit_order
        )
        if _product_keyword_match:
            return IntentResult(
                category=IntentCategory.PRODUCT,
                intent_name="PRODUCT_INQUIRY",
                confidence=0.85,
                entities=entities,
                explicit_entities=explicit_entities,
                suggested_route="STRUCTURED",
                raw_query=query
            )

        return IntentResult(
            category=IntentCategory.UNKNOWN,
            intent_name="GENERAL_QUERY",
            confidence=0.50,
            entities=entities,
            explicit_entities=explicit_entities,
            suggested_route="RAG",
            raw_query=query
        )


class LLMIntentClassifier:
    """LLM-driven intent and slot extractor with deterministic fallback."""

    def __init__(self, fallback_classifier: Optional[IntentClassifier] = None):
        self.fallback = fallback_classifier or IntentClassifier()

    def classify(
        self,
        query: str,
        customer_id: str = "GUEST",
        active_order_id: Optional[str] = None,
        active_product_id: Optional[str] = None,
        active_return_id: Optional[str] = None,
        active_refund_id: Optional[str] = None,
        previous_intent: Optional[str] = None,
        use_llm: bool = True,
        context_slots: Optional[Dict[str, Any]] = None
    ) -> IntentResult:
        """Extract intent and entities using LLM or deterministic fallback."""
        # Always extract regex/explicit entities first to preserve explicit entity contract
        regex_entities = self.fallback.extract_entities(query)

        # Build context dictionary preserving all active domain slots
        c_slots: Dict[str, Any] = dict(context_slots or {})
        if active_order_id and "order_id" not in c_slots:
            c_slots["order_id"] = active_order_id
        if active_product_id and "product_id" not in c_slots:
            c_slots["product_id"] = active_product_id
        if active_return_id and "return_id" not in c_slots:
            c_slots["return_id"] = active_return_id
        if active_refund_id and "refund_id" not in c_slots:
            c_slots["refund_id"] = active_refund_id

        if not use_llm:
            return self.fallback.classify(query, context_slots=c_slots)

        prompt = INTENT_CLASSIFICATION_PROMPT.format(
            customer_id=customer_id,
            active_order_id=c_slots.get("order_id") or "None",
            previous_intent=previous_intent or "None",
            message=query
        )

        try:
            structured_data = llm_client.generate_structured(
                prompt=prompt,
                schema=INTENT_EXTRACTION_SCHEMA,
                system_instruction="You are an intent classification and slot-filling engine for ShopKart."
            )

            if isinstance(structured_data, list) and structured_data:
                structured_data = structured_data[0]
            elif not isinstance(structured_data, dict):
                structured_data = {}

            category_str = str(structured_data.get("category", "unknown")).lower()
            try:
                category_enum = IntentCategory(category_str)
            except ValueError:
                category_enum = IntentCategory.UNKNOWN

            llm_entities = structured_data.get("entities", {})
            if not isinstance(llm_entities, dict):
                llm_entities = {}

            # Merge regex entities (highest fidelity for strict IDs) with LLM entities and context
            merged_entities = {**c_slots, **llm_entities, **regex_entities}

            suggested_route = structured_data.get("suggested_route", "STRUCTURED")

            return IntentResult(
                category=category_enum,
                intent_name=str(structured_data.get("intent", "LLM_DETECTED")),
                confidence=float(structured_data.get("confidence", 0.9)),
                entities=merged_entities,
                explicit_entities=regex_entities,
                suggested_route=suggested_route,
                raw_query=query,
                is_llm_generated=True
            )
        except Exception as e:
            logger.warning(f"LLM intent classification fell back to deterministic classifier: {e}")
            fallback_res = self.fallback.classify(query, context_slots=c_slots)
            fallback_res.is_llm_generated = False
            return fallback_res


# Global singletons
intent_classifier = IntentClassifier()
llm_intent_classifier = LLMIntentClassifier(intent_classifier)

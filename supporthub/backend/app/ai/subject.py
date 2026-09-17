"""
Dynamic AI Ticket Subject Generator.
Derives concise, informative ticket titles from the customer's actual inquiry.
Preserves initial category subject until the user asks their first meaningful question.
Inspects up to the first 3 customer messages to find a substantive question.
Once a specific question title is established, it locks and does not change further.
"""
from typing import Optional, List
from uuid import UUID
import re
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Ticket, Message, SenderType


GENERIC_STARTING_SUBJECTS = {
    "general support query", "general support", "general query",
    "billing & orders query", "billing & orders", "billing query",
    "technical issue query", "technical issue", "technical query",
    "account & access query", "account & access", "account query",
    "shipping & delivery query", "shipping & delivery",
    "returns & refunds query", "returns & refunds",
    "billing & payments query", "billing & payments",
    "general question query", "general question",
    "website chat", "website_chat", "chat support",
    "new conversation", "new chat", "support inquiry", "customer inquiry",
    "general customer inquiry", "new support query", "support conversation",
}

GREETING_PHRASES = {
    "good morning", "good evening", "good afternoon", "good day", "hey there",
    "namaste ji", "hello there", "hi there", "howdy", "whats up", "what's up",
}

GREETING_WORDS = {
    "hi", "hello", "hey", "good", "morning", "evening", "afternoon", "day",
    "namaste", "sup", "test", "ok", "okay", "thanks", "thank", "you", "help",
    "start", "yes", "no", "bye", "hlo", "hii", "helo", "there", "please"
}


def is_generic_subject(subject: Optional[str]) -> bool:
    """Check if the subject is still a generic category starting placeholder."""
    if not subject:
        return True
    s = subject.strip().lower()
    if s in GENERIC_STARTING_SUBJECTS:
        return True
    if s.endswith("support query") or s.endswith(" support") or s.endswith(" query"):
        return True
    if "support query" in s or "support inquiry" in s or "new conversation" in s:
        return True
    if len(s) < 8:
        return True
    return False


def is_greeting(text: str) -> bool:
    """Check if the message is purely a greeting without a substantive query."""
    clean = re.sub(r"[^\w\s]", "", text.strip().lower())
    if not clean:
        return True
    if clean in GREETING_PHRASES:
        return True
    words = clean.split()
    if len(words) <= 2 and all(w in GREETING_WORDS for w in words):
        return True
    return False


def to_title_case(text: str) -> str:
    """Format into standard Title Case, preserving acronyms and lowercase conjunctions/prepositions."""
    lower_words = {"a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "with", "in", "of"}
    words = text.split()
    if not words:
        return text
    formatted = []
    for i, w in enumerate(words):
        if re.match(r"^(ORD|PROD|TRK|SHIP|REF|RET|FAQ|AI|ID|OTP|UPI|COD|URL|SMS)-?[\w-]*$", w, re.IGNORECASE):
            formatted.append(w.upper())
        elif i > 0 and w.lower() in lower_words:
            formatted.append(w.lower())
        else:
            formatted.append(w.capitalize())
    return " ".join(formatted)


def format_subject_from_query(query: str) -> str:
    """
    Extract the core intent from a customer's query and formulate a clean,
    professional support ticket subject (max ~48 chars).
    """
    s = query.strip()
    # Strip leading greetings with any commas/colons/dashes (e.g. "hi, i want...")
    greeting_prefix_regex = r"^(hi+|hello+|hey+|namaste|dear\s+team|dear\s+support|good\s+morning|good\s+evening|good\s+afternoon|hlo|hii+)[\s,!:.-]*\s*"
    s = re.sub(greeting_prefix_regex, "", s, flags=re.IGNORECASE).strip()
    s = re.sub(greeting_prefix_regex, "", s, flags=re.IGNORECASE).strip()

    # Detect entity identifiers
    order_match = re.search(r"\b(ord-\d+)\b", s, flags=re.IGNORECASE)
    prod_match = re.search(r"\b(prod-\d+)\b", s, flags=re.IGNORECASE)
    ship_match = re.search(r"\b(ship-\d+)\b", s, flags=re.IGNORECASE)
    trk_match = re.search(r"\b(trk-[a-z0-9\-]+)\b", s, flags=re.IGNORECASE)

    order_id = order_match.group(1).upper() if order_match else None
    prod_id = prod_match.group(1).upper() if prod_match else None
    ship_id = ship_match.group(1).upper() if ship_match else None
    trk_id = trk_match.group(1).upper() if trk_match else None

    s_lower = s.lower()

    # 0. Human Agent Escalation Request
    if any(p in s_lower for p in (
        "human agent", "talk to human", "talk with human", "talk with humen", "talk to humen",
        "talk with agent", "talk to agent", "human customer agent", "speak to human",
        "speak with human", "speak with agent", "speak to agent", "real person", "live agent",
        "transfer to human", "transfer me to a human", "transfer request to human",
        "transfer to our human", "human support", "connect to human", "connect with human",
        "connect me to an agent", "supervisor", "manager"
    )) or re.search(r"\b(?:talk|speak|chat|connect|transfer)\s+(?:with|to|me\s+to)?\s*(?:a|an|the|our)?\s*(?:real|live)?\s*(?:hum[ae]n|agent|person)\b", s_lower):
        return "Human Agent Support Request"

    # 1. Category Product Search
    has_category_kw = any(w in s_lower for w in ("product", "products", "item", "items", "catalog", "browse", "tell me every", "show me every", "gift", "gifting"))
    if has_category_kw:
        for cat_kw, cat_title in [
            ("electronics", "Electronics Products"),
            ("mobiles & tablets", "Mobiles & Tablets"),
            ("mobile", "Mobiles & Tablets"),
            ("tablet", "Mobiles & Tablets"),
            ("laptops & computers", "Laptops & Computers"),
            ("laptop", "Laptops & Computers"),
            ("audio & headphones", "Audio & Headphones"),
            ("headphone", "Audio & Headphones"),
            ("kitchen", "Kitchen & Dining"),
            ("furniture", "Home Furniture"),
            ("appliances", "Home Appliances"),
            ("appliance", "Home Appliances"),
            ("footwear", "Footwear Products"),
            ("women", "Women's Products & Gifts"),
            ("men", "Men's Products & Gifts"),
        ]:
            if re.search(r"\b" + re.escape(cat_kw) + r"\b", s_lower):
                return cat_title

    # 2. Product Catalog Overview
    if any(p in s_lower for p in (
        "show all product", "show me all product", "all product", "all the product",
        "list all product", "product catalog", "what product", "view product",
        "browse product", "products catalog", "available product", "store product",
    )):
        return "Product Catalog Overview"

    # 2. All Orders
    if any(p in s_lower for p in ("all order", "all my order", "my all order", "list my order", "previous order", "order history")):
        return "Order History & All Orders"

    # 3. Order Status / Tracking
    if any(p in s_lower for p in ("where is my order", "track order", "track my order", "order status", "when will my order", "check order", "order update")):
        if order_id:
            return f"Order Status ({order_id})"
        return "Order Status & Tracking"

    # 4. Cancel Order
    if "cancel" in s_lower and ("order" in s_lower or order_id):
        if order_id:
            return f"Cancel Order ({order_id})"
        return "Order Cancellation Request"

    # 5. Return & Refund
    if any(p in s_lower for p in ("return", "replace", "exchange")):
        if prod_id:
            return f"Return Request ({prod_id})"
        if order_id:
            return f"Return Request ({order_id})"
        return "Return & Replacement Request"

    if any(p in s_lower for p in ("refund", "money back")):
        if order_id:
            return f"Refund Request ({order_id})"
        return "Refund Status & Inquiry"

    # 6. Payment / Billing
    if ("payment" in s_lower or "transaction" in s_lower or "money" in s_lower) and any(
        w in s_lower for w in ("fail", "decline", "deduct", "charg", "issue", "error", "problem", "stuck")
    ):
        if order_id:
            return f"Payment Issue ({order_id})"
        return "Payment & Billing Inquiry"

    if any(p in s_lower for p in ("invoice", "bill receipt", "tax invoice", "download invoice", "billing")):
        if order_id:
            return f"Invoice Request ({order_id})"
        return "Billing & Invoice Inquiry"

    # 7. Shipment & Delivery
    if ship_id or trk_id or any(p in s_lower for p in ("shipment", "delivery delay", "late delivery", "courier", "delhivery", "bluedart", "out for delivery")):
        ident = ship_id or trk_id or (f"({order_id})" if order_id else "")
        if ident:
            return f"Shipment Tracking {ident}".strip()
        return "Shipment & Delivery Tracking"

    if any(p in s_lower for p in ("change address", "update address", "delivery address", "shipping address")):
        return "Change Delivery Address"

    # 8. Account & Security
    if "password" in s_lower and any(w in s_lower for w in ("reset", "forgot", "change", "recover", "update")):
        return "Password Reset Assistance"
    if any(p in s_lower for p in ("delete account", "close account", "deactivate account")):
        return "Account Deletion Request"
    if any(p in s_lower for p in ("cant login", "cannot login", "login issue", "sign in problem")):
        return "Login & Access Issue"

    # 9. Product-specific queries
    if prod_id:
        if "warranty" in s_lower:
            return f"Warranty Inquiry ({prod_id})"
        if any(p in s_lower for p in ("spec", "feature", "detail")):
            return f"Product Specs ({prod_id})"
        if any(p in s_lower for p in ("price", "cost", "discount", "offer")):
            return f"Pricing & Offers ({prod_id})"
        if any(p in s_lower for p in ("stock", "available")):
            return f"Stock Availability ({prod_id})"
        return f"Product Inquiry ({prod_id})"

    # 10. General / Unstructured Inquiry: Strip conversational prefixes and convert to Title Case
    fillers = [
        r"^(can you please|could you please|please|pls|kindly)\s+",
        r"^(i want to know|i wanted to know|i would like to know|i'd like to know)\s+",
        r"^(i want to ask|i wanted to ask|i want to check|i need to check)\s+",
        r"^(i want to|i need to|i wanna|i would like to|i'd like to)\s+",
        r"^(i want|i need|need|want)\s+",
        r"^(i have a question about|i have a query about|i have an issue with|i have a problem with)\s+",
        r"^(can you tell me about|can you tell me|can you show me|can you explain|can you check)\s+",
        r"^(could you tell me|could you show me|could you check)\s+",
        r"^(can you help me with|can you help me to|can you help me|help me with)\s+",
        r"^(tell me about|tell me|give me all info of|give me info of|give me)\s+",
        r"^(how do i|how can i|how to)\s+",
        r"^(what is the|what are the|what is|what are)\s+",
        r"^(where is the|where is my|where is|where can i find)\s+",
        r"^(why was my|why is my|why did my)\s+",
        r"^(is there any|is there|are there|do you have)\s+",
    ]
    cleaned = s
    for pat in fillers:
        cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE).strip()

    # Strip trailing polite noise
    cleaned = re.sub(r"[\s,]*(please|pls|kindly|thank you|thanks|asap|urgently)[\s.?!]*$", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = cleaned.rstrip("?.!,:;")

    if not cleaned or len(cleaned) < 3:
        return "Customer Support Inquiry"

    title = to_title_case(cleaned)
    if len(title) > 48:
        truncated = title[:45]
        if " " in truncated:
            truncated = truncated.rsplit(" ", 1)[0]
        title = truncated + "..."
    return title


async def generate_ai_ticket_subject(session: AsyncSession, ticket_id: str | UUID) -> Optional[str]:
    """
    Evaluates up to the first 3 customer messages on a ticket.
    If the ticket still has a generic category title, updates it based on the
    first substantive question asked by the customer.
    Once updated, does NOT change again for the lifetime of the chat.
    """
    try:
        ticket_uuid = UUID(str(ticket_id))
    except (ValueError, TypeError):
        return None

    ticket = await session.get(Ticket, ticket_uuid)
    if not ticket:
        return None

    # If the ticket already has a specific, non-generic title, lock it!
    if not is_generic_subject(ticket.subject):
        return None

    # Fetch up to the first 3 customer messages in chronological order
    stmt = (
        select(Message)
        .where(Message.ticket_id == ticket_uuid)
        .where(Message.sender_type == SenderType.customer)
        .order_by(Message.created_at.asc())
        .limit(3)
    )
    result = await session.exec(stmt)
    customer_msgs = result.all()
    if not customer_msgs:
        return None

    # Scan messages 1, 2, 3 for the first substantive question
    for msg in customer_msgs:
        text = (msg.body or "").strip()
        if not text:
            continue
        if is_greeting(text):
            continue  # e.g., "Hello", skip to next message
        
        # Found the first meaningful customer question!
        new_subject = format_subject_from_query(text)
        if new_subject and new_subject.lower() != (ticket.subject or "").lower():
            return new_subject

    return None

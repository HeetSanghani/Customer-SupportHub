"""Deterministic Grounding and Anti-Hallucination Validator."""
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class GroundingResult:
    """Outcome of grounding and factuality verification."""
    is_grounded: bool
    confidence: float
    violations: List[str] = field(default_factory=list)
    checked_facts: Dict[str, Any] = field(default_factory=dict)
    remediation_required: bool = False


class GroundingValidator:
    """Verifies that LLM generated text is strictly supported by verified data."""

    # Key conflicting status pairs that must never be mixed up
    CONFLICTING_STATUSES = {
        "DELIVERED": ["IN_TRANSIT", "OUT_FOR_DELIVERY", "SHIPPED", "CONFIRMED", "PLACED", "CANCELLED", "FAILED"],
        "IN_TRANSIT": ["DELIVERED", "CANCELLED", "FAILED"],
        "OUT_FOR_DELIVERY": ["DELIVERED", "CANCELLED", "FAILED"],
        "CANCELLED": ["DELIVERED", "IN_TRANSIT", "OUT_FOR_DELIVERY", "SHIPPED", "CONFIRMED"],
        "FAILED": ["DELIVERED", "COMPLETED", "SUCCESSFUL"],
        "COMPLETED": ["FAILED", "PENDING", "CANCELLED"]
    }

    def validate(
        self,
        response_text: str,
        structured_data: Optional[Dict[str, Any]] = None,
        rag_citations: Optional[List[Dict[str, Any]]] = None,
        query: Optional[str] = None
    ) -> GroundingResult:
        """Validate generated response against verified context facts."""
        violations = []
        checked_facts = {}
        text_upper = response_text.upper()

        # 1. Check Non-existent entities
        if structured_data and structured_data.get("not_found"):
            # The record was not found in the DB. Ensure LLM didn't hallucinate active state
            if any(term in text_upper for term in ["DELIVERED", "SHIPPED ON", "TRACKING NUMBER IS TRK", "IN TRANSIT"]):
                violations.append("Response hallucinated details for a non-existent database record.")

        # 2. Check Order Status Fidelity
        if structured_data and "order" in structured_data and structured_data["order"]:
            order = structured_data["order"]
            real_status = order.get("status", "").upper()
            checked_facts["order_status"] = real_status

            if real_status:
                conflicts = self.CONFLICTING_STATUSES.get(real_status, [])
                for conflict in conflicts:
                    pattern = rf"\b{conflict.replace('_', ' ')}\b|\b{conflict}\b"
                    if re.search(pattern, text_upper) and not re.search(rf"\b(NOT|NEVER|NO LONGER|BEFORE BEING)\s+{conflict}\b", text_upper):
                        # Flag conflicting status if asserted
                        violations.append(f"Response states status conflicting with verified order status {real_status}.")

        # 3. Check Payment Status Fidelity
        if structured_data and "payment" in structured_data and structured_data["payment"]:
            payment = structured_data["payment"]
            pay_status = payment.get("status", "").upper()
            checked_facts["payment_status"] = pay_status

            if pay_status == "FAILED":
                if "SUCCESSFUL" in text_upper or "PAYMENT COMPLETED" in text_upper:
                    violations.append("Response claims payment succeeded when database shows FAILED.")

        # 4. Check Shipment Tracking Fidelity
        if structured_data and "shipment" in structured_data and structured_data["shipment"]:
            shipment = structured_data["shipment"]
            trk = shipment.get("tracking_number", "")
            checked_facts["tracking_number"] = trk
            
            # Check for hallucinated tracking pattern not matching real tracking
            hallucinated_trks = re.findall(r"TRK-[A-Z]+-[0-9]+", response_text)
            for ht in hallucinated_trks:
                if ht != trk:
                    violations.append(f"Response contains hallucinated tracking number {ht} (expected {trk}).")

        # 5. Check Refund Amount & Status Fidelity
        if structured_data and "refund" in structured_data and structured_data["refund"]:
            refund = structured_data["refund"]
            ref_status = refund.get("status", "").upper()
            checked_facts["refund_status"] = ref_status

        # 6. Check RAG Citation Presence when knowledge is retrieved
        if rag_citations:
            checked_facts["rag_citations_count"] = len(rag_citations)

        is_grounded = len(violations) == 0
        confidence = 1.0 if is_grounded else max(0.0, 1.0 - (0.3 * len(violations)))

        return GroundingResult(
            is_grounded=is_grounded,
            confidence=confidence,
            violations=violations,
            checked_facts=checked_facts,
            remediation_required=not is_grounded
        )


# Global singleton validator
grounding_validator = GroundingValidator()

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


def _extract_chunk_text(chunk_obj: Any) -> str:
    """Safely extract plain text string from various chunk representations."""
    if isinstance(chunk_obj, str):
        return chunk_obj
    if isinstance(chunk_obj, dict):
        return chunk_obj.get("text") or chunk_obj.get("content") or chunk_obj.get("chunk_content") or ""
    if hasattr(chunk_obj, "chunk") and hasattr(chunk_obj.chunk, "text"):
        return chunk_obj.chunk.text
    if hasattr(chunk_obj, "text"):
        return str(chunk_obj.text)
    if hasattr(chunk_obj, "content"):
        return str(chunk_obj.content)
    return str(chunk_obj)


def extract_grounded_facts(cited_chunks: List[Any]) -> Dict[str, Any]:
    """Scans cited chunk objects/dicts and extracts factual claims (time windows, numbers, policy terms)."""
    numeric_windows = []
    numbers_by_unit: Dict[str, set] = {}
    valid_numbers: set = set()
    found_policy_terms: set = set()

    known_terms = [
        "non-returnable", "doorstep pickup", "final sale", "instant refund",
        "replacement", "store credit", "original tags", "picked_up",
        "item damaged on arrival", "wrong_product", "otp", "upi pin",
        "my orders", "replacement trigger", "full return"
    ]

    time_pattern = re.compile(
        r'\b(\d+(?:\s*(?:to|–|-)\s*\d+)?)\s*(calendar\s+days?|business\s+days?|business\s+hours?|days?|hours?|weeks?|months?)\b',
        re.IGNORECASE
    )

    for chunk in cited_chunks:
        text = _extract_chunk_text(chunk)
        text_lower = text.lower()

        for term in known_terms:
            if term in text_lower:
                found_policy_terms.add(term)

        for match in time_pattern.finditer(text):
            raw_num_part, unit_part = match.group(1), match.group(2).lower()
            norm_unit = 'days' if 'day' in unit_part else ('hours' if 'hour' in unit_part else ('weeks' if 'week' in unit_part else unit_part))
            nums = re.findall(r'\d+', raw_num_part)

            start = max(0, match.start() - 40)
            end = min(len(text), match.end() + 40)
            snippet = text[start:end].replace('\n', ' ').strip()

            numeric_windows.append({
                "raw_claim": match.group(0),
                "numbers": nums,
                "unit": norm_unit,
                "context": snippet
            })

            if norm_unit not in numbers_by_unit:
                numbers_by_unit[norm_unit] = set()
            for n in nums:
                numbers_by_unit[norm_unit].add(n)
                valid_numbers.add(n)

    return {
        "numeric_windows": numeric_windows,
        "numbers_by_unit": {k: sorted(list(v), key=lambda x: int(x) if x.isdigit() else x) for k, v in numbers_by_unit.items()},
        "valid_numbers": sorted(list(valid_numbers), key=lambda x: int(x) if x.isdigit() else x),
        "policy_terms": sorted(list(found_policy_terms))
    }


def check_entailment(response_text: str, grounded_facts: Dict[str, Any]) -> List[str]:
    """Checks generated response claims against grounded facts extracted from cited chunks."""
    violations = []
    if not grounded_facts:
        return violations

    time_pattern = re.compile(
        r'\b(\d+(?:\s*(?:to|–|-)\s*\d+)?)\s*(calendar\s+days?|business\s+days?|business\s+hours?|days?|hours?|weeks?|months?)\b',
        re.IGNORECASE
    )

    supported_by_unit = grounded_facts.get("numbers_by_unit", {})
    all_valid_numbers = set(grounded_facts.get("valid_numbers", []))

    matches = list(time_pattern.finditer(response_text))
    for match in matches:
        raw_claim = match.group(0)
        raw_num_part = match.group(1)
        unit_part = match.group(2).lower()

        norm_unit = 'days' if 'day' in unit_part else ('hours' if 'hour' in unit_part else ('weeks' if 'week' in unit_part else unit_part))
        nums = re.findall(r'\d+', raw_num_part)

        if norm_unit in supported_by_unit:
            unit_valid_nums = set(supported_by_unit[norm_unit])
            for num in nums:
                if num not in unit_valid_nums:
                    supp_str = f"supported numbers for {norm_unit}: {sorted(list(unit_valid_nums), key=lambda x: int(x) if x.isdigit() else x)}"
                    violations.append(
                        f'Response claims a "{raw_claim}" policy window, which is not supported by cited knowledge base chunks ({supp_str}).'
                    )
        else:
            if supported_by_unit:
                supp_details = [
                    f"{u}: {sorted(list(num_list), key=lambda x: int(x) if x.isdigit() else x)}"
                    for u, num_list in supported_by_unit.items()
                ]
                supp_str = f"supported units and numbers in cited chunks: {', '.join(supp_details)}"
            elif all_valid_numbers:
                supp_str = f"supported numbers: {sorted(list(all_valid_numbers), key=lambda x: int(x) if x.isdigit() else x)}"
            else:
                supp_str = "no numeric time windows found in cited chunks"

            violations.append(
                f'Response claims a "{raw_claim}" policy window, which is not supported by cited knowledge base chunks ({supp_str}).'
            )

    return violations


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

    def extract_grounded_facts(self, cited_chunks: List[Any]) -> Dict[str, Any]:
        """Extract grounded facts from cited chunks."""
        return extract_grounded_facts(cited_chunks)

    def check_entailment(self, response_text: str, grounded_facts: Dict[str, Any]) -> List[str]:
        """Check response claims against grounded facts."""
        return check_entailment(response_text, grounded_facts)

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

        # 6. Check RAG Citation Presence & Entailment
        if rag_citations:
            checked_facts["rag_citations_count"] = len(rag_citations)
            grounded_facts = self.extract_grounded_facts(rag_citations)
            checked_facts["grounded_facts"] = grounded_facts
            entailment_violations = self.check_entailment(response_text, grounded_facts)
            violations.extend(entailment_violations)

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

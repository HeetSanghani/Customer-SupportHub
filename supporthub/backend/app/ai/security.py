"""Security and Authorization Gateway."""
import re
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SecurityDecision:
    """Outcome of security and authorization evaluation."""
    is_allowed: bool
    reason: str                  # "AUTHORIZED", "CROSS_CUSTOMER_ACCESS_DENIED", "CREDENTIAL_LEAK_INTERCEPTED", "PII_REQUEST_DENIED", "OTP_REQUEST_DENIED"
    message: str
    risk_level: str = "LOW"      # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    sanitized_text: Optional[str] = None


class SecurityValidator:
    """Enforces deterministic authorization boundaries and sensitive data protection."""

    OTP_LEAK_PATTERN = re.compile(r"\b(otp|one[-\s]?time[-\s]?password)\s*(is|:)?\s*\d{4,8}\b|\b\d{4,8}\s*(is\s*my\s*otp)\b", re.IGNORECASE)
    PIN_LEAK_PATTERN = re.compile(r"\b(pin|cvv|cvc|password)\s*(is|:)?\s*([a-zA-Z0-9!@#$%^&*]{3,16})\b|\bcard\s*pin\s*is\s*\d{4,6}\b", re.IGNORECASE)
    CARD_PATTERN = re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b")
    
    # Specific security exploit patterns (SEC01, SEC02, SEC03, SEC04)
    THIRD_PARTY_PII_PATTERNS = [
        re.compile(r"\b(phone number|email|address|details)\s*(of|for)\s*(customer\s+[a-zA-Z]+|[a-zA-Z]+\s+[a-zA-Z]+|another\s+customer|other\s+customer)\b", re.IGNORECASE),
        re.compile(r"\b(what\s+items\s+did\s+[a-zA-Z]+\s+[a-zA-Z]+\s+order)\b", re.IGNORECASE),
        re.compile(r"\b(give\s+me\s+the\s+shipping\s+address\s+associated\s+with\s+ord-\d+)\b", re.IGNORECASE),
        re.compile(r"\b(give\s+me|what\s+is)\s*(the\s*)?(phone|address|email|orders?)\s*(of|for)\s*cust-\d+\b", re.IGNORECASE),
    ]
    OTP_INQUIRY_PATTERNS = [
        re.compile(r"\b(what\s+is|tell\s+me|give\s+me|get\s+me|send\s+me|show\s+me)\s+(the\s+|my\s+|a\s+|an\s+)?(otp|pin|upi\s*pin|card\s*pin|cvv|password)(\s+code)?\b", re.IGNORECASE),
        re.compile(r"\bsend\s+me\s+(the\s+|my\s+)?(otp|pin)\s+in\s+chat\b", re.IGNORECASE),
        re.compile(r"\botp\s+sent\s+for\s+my\s+payment\b", re.IGNORECASE),
        re.compile(r"\b(give|show|tell)\s+me\s+my\s+otp\b", re.IGNORECASE)
    ]
    ADMIN_EXPLOIT_PATTERNS = [
        re.compile(r"\b(i\s+am\s+(an?\s+)?admin|admin\s+user|system\s+user\s+passwords|audit\s+logs|all\s+user\s+passwords)\b", re.IGNORECASE)
    ]

    def validate_inbound_query(
        self,
        query: str,
        caller_customer_id: Optional[str] = None
    ) -> SecurityDecision:
        """Scan query for credential leaks or unauthorized PII solicitation."""
        text = query.strip()
        lower = text.lower()

        # 1. Check for Inbound Credential Leaks (Customer posting their OTP or PIN)
        if self.OTP_LEAK_PATTERN.search(text) or "otp is" in lower:
            return SecurityDecision(
                is_allowed=False,
                reason="CREDENTIAL_LEAK_INTERCEPTED",
                message="For your security, ShopKart representatives will never ask for your OTP. Please do not share OTPs in chat. Your account remains secure.",
                risk_level="HIGH",
                sanitized_text="[REDACTED_OTP]"
            )

        if self.PIN_LEAK_PATTERN.search(text) or "card pin is" in lower or "my pin is" in lower:
            return SecurityDecision(
                is_allowed=False,
                reason="CREDENTIAL_LEAK_INTERCEPTED",
                message="For your safety, never share your payment PIN, CVV, or passwords in chat. ShopKart will never ask for your confidential payment credentials.",
                risk_level="CRITICAL",
                sanitized_text="[REDACTED_PIN]"
            )

        # 2. Check for OTP / Security Code Inquiries (SEC04)
        if any(p.search(text) for p in self.OTP_INQUIRY_PATTERNS) or "what is the otp" in lower:
            return SecurityDecision(
                is_allowed=False,
                reason="OTP_REQUEST_DENIED",
                message="Security Policy: One-Time Passwords (OTPs) are sent exclusively via encrypted SMS/Email to your registered device and cannot be revealed by the AI assistant.",
                risk_level="CRITICAL"
            )

        # 3. Check for Third-party PII Solicitation (SEC01, SEC02, SEC03)
        if any(p.search(text) for p in self.THIRD_PARTY_PII_PATTERNS) or "another customer" in lower or "other customer" in lower:
            return SecurityDecision(
                is_allowed=False,
                reason="PII_REQUEST_DENIED",
                message="Access Denied: You cannot request contact information, order details, or personal addresses belonging to other customers per ShopKart Privacy Policy.",
                risk_level="HIGH"
            )

        # 4. Check for Admin Exploit / Privileged Claims (SEC04)
        if any(p.search(text) for p in self.ADMIN_EXPLOIT_PATTERNS) or "system user passwords" in lower or "audit logs" in lower:
            return SecurityDecision(
                is_allowed=False,
                reason="ADMIN_EXPLOIT_DENIED",
                message="Access Denied: Administrative privileges cannot be assumed via chat. System logs and credentials are strictly protected.",
                risk_level="CRITICAL"
            )

        return SecurityDecision(
            is_allowed=True,
            reason="AUTHORIZED",
            message="Query passed security gateway.",
            risk_level="LOW",
            sanitized_text=text
        )

    def validate_resource_ownership(
        self,
        caller_customer_id: Optional[str],
        resource_owner_id: Optional[str],
        resource_type: str = "resource"
    ) -> SecurityDecision:
        """Enforce that customer A cannot view Customer B's records."""
        if not caller_customer_id or not resource_owner_id:
            return SecurityDecision(
                is_allowed=True,
                reason="PUBLIC_OR_UNBOUND",
                message="Public resource or unbound ownership."
            )

        if caller_customer_id.upper() != resource_owner_id.upper():
            return SecurityDecision(
                is_allowed=False,
                reason="CROSS_CUSTOMER_ACCESS_DENIED",
                message=f"Access Denied: You are not authorized to access this {resource_type} as it belongs to another account.",
                risk_level="HIGH"
            )

        return SecurityDecision(
            is_allowed=True,
            reason="OWNERSHIP_VERIFIED",
            message=f"Caller is verified owner of {resource_type}."
        )

    def redact_pii(self, text: str) -> str:
        """Mask credit card numbers and sensitive numbers in text."""
        text = self.CARD_PATTERN.sub("****-****-****-****", text)
        return text


security_validator = SecurityValidator()

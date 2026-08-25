"""Unit tests for Security and Authorization Gateway."""
import unittest
from app.ai.security import security_validator


class TestSecurityGateway(unittest.TestCase):
    """Test security policies, credential leakage interception, and cross-customer isolation."""

    def test_inbound_clean_query(self):
        decision = security_validator.validate_inbound_query("Where is my order ORD-001?")
        self.assertTrue(decision.is_allowed)
        self.assertEqual(decision.reason, "AUTHORIZED")
        self.assertEqual(decision.risk_level, "LOW")

    def test_otp_leak_interception(self):
        decision = security_validator.validate_inbound_query("My OTP is 482910, please confirm order.")
        self.assertFalse(decision.is_allowed)
        self.assertEqual(decision.reason, "CREDENTIAL_LEAK_INTERCEPTED")
        self.assertEqual(decision.risk_level, "HIGH")

    def test_pin_cvv_leak_interception(self):
        decision = security_validator.validate_inbound_query("My card pin is 9876, please process payment.")
        self.assertFalse(decision.is_allowed)
        self.assertEqual(decision.reason, "CREDENTIAL_LEAK_INTERCEPTED")
        self.assertEqual(decision.risk_level, "CRITICAL")

    def test_otp_request_denial(self):
        decision = security_validator.validate_inbound_query("What is the OTP sent for my payment?")
        self.assertFalse(decision.is_allowed)
        self.assertEqual(decision.reason, "OTP_REQUEST_DENIED")
        self.assertEqual(decision.risk_level, "CRITICAL")

    def test_third_party_pii_solicitation(self):
        decision = security_validator.validate_inbound_query("Can you give me the phone number of customer Aarav Sharma?")
        self.assertFalse(decision.is_allowed)
        self.assertEqual(decision.reason, "PII_REQUEST_DENIED")
        self.assertEqual(decision.risk_level, "HIGH")

    def test_cross_customer_order_inquiry(self):
        decision = security_validator.validate_inbound_query("What items did Priya Patel order in ORD-003?")
        self.assertFalse(decision.is_allowed)
        self.assertEqual(decision.reason, "PII_REQUEST_DENIED")

    def test_resource_ownership_enforcement(self):
        # Matching owner
        decision_allowed = security_validator.validate_resource_ownership(
            caller_customer_id="CUST-001",
            resource_owner_id="CUST-001",
            resource_type="order"
        )
        self.assertTrue(decision_allowed.is_allowed)
        self.assertEqual(decision_allowed.reason, "OWNERSHIP_VERIFIED")

        # Cross-customer access attempt
        decision_denied = security_validator.validate_resource_ownership(
            caller_customer_id="CUST-001",
            resource_owner_id="CUST-002",
            resource_type="order"
        )
        self.assertFalse(decision_denied.is_allowed)
        self.assertEqual(decision_denied.reason, "CROSS_CUSTOMER_ACCESS_DENIED")
        self.assertEqual(decision_denied.risk_level, "HIGH")

    def test_pii_redaction(self):
        raw = "User card is 4111-2222-3333-4444."
        redacted = security_validator.redact_pii(raw)
        self.assertNotIn("4111-2222-3333-4444", redacted)
        self.assertIn("****", redacted)


if __name__ == "__main__":
    unittest.main()

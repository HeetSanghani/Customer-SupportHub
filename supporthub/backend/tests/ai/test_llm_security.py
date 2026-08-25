"""Security tests for LLM abstraction and orchestration."""
import unittest
from app.ai.orchestrator import ai_orchestrator
from app.ai.security import security_validator
from app.ai.llm import llm_client, GeminiProvider, TokenUsage, LLMResponse


class TestLLMSecurity(unittest.TestCase):
    """Test suite ensuring absolute zero-trust security invariance with LLM integration."""

    def test_credential_interception_before_llm(self):
        """Ensure OTP, UPI PIN, and CVV queries are intercepted before reaching LLM."""
        queries = [
            "My OTP is 849201, please approve my order.",
            "Can you tell me the UPI PIN to pay for ORD-001?",
            "My card CVV is 992, process my payment.",
            "My password is secret123, update my account."
        ]
        for q in queries:
            resp = ai_orchestrator.process_message(q, customer_id="CUST-001", use_llm=True)
            self.assertEqual(resp.route_type, "SECURITY", f"Failed to intercept credential in: {q}")
            self.assertTrue(
                "never" in resp.content.lower() or "security" in resp.content.lower() or "cannot be revealed" in resp.content.lower(),
                f"Unexpected denial message: {resp.content}"
            )

    def test_cross_customer_data_access_denial(self):
        """Ensure caller cannot query another customer's order even with LLM reasoning."""
        # ORD-001 belongs to CUST-001
        # CUST-002 tries to access ORD-001
        resp = ai_orchestrator.process_message(
            query="Give me the address and tracking details for order ORD-001.",
            customer_id="CUST-002",
            conversation_id="conv_cross_cust_test",
            use_llm=True
        )
        self.assertEqual(resp.route_type, "SECURITY")
        self.assertIn("Access Denied", resp.content)

    def test_telemetry_does_not_leak_api_keys(self):
        """Ensure internal logging and telemetry history do not expose API keys."""
        llm_client._record_telemetry(
            method="generate",
            model="gemini-2.5-flash",
            tokens=50,
            latency=0.5,
            status="SUCCESS"
        )
        last_rec = llm_client.call_history[-1]
        self.assertNotIn("api_key", str(last_rec).lower())
        self.assertNotIn("authorization", str(last_rec).lower())


if __name__ == "__main__":
    unittest.main()

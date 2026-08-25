"""Tests for GroundingValidator and hallucination detection."""
import unittest
from app.ai.grounding import GroundingValidator, GroundingResult


class TestHallucinationAndGrounding(unittest.TestCase):
    """Test suite ensuring GroundingValidator flags conflicting or hallucinated statements."""

    def setUp(self):
        self.validator = GroundingValidator()

    def test_status_conflict_detection(self):
        """Detect when response claims DELIVERED for an IN_TRANSIT order."""
        fake_response = "Your order ORD-013 was DELIVERED yesterday to your home."
        verified_data = {
            "order": {"order_id": "ORD-013", "status": "IN_TRANSIT"}
        }

        result = self.validator.validate(fake_response, structured_data=verified_data)
        self.assertFalse(result.is_grounded)
        self.assertTrue(result.remediation_required)
        self.assertTrue(any("conflicting" in v.lower() for v in result.violations))

    def test_tracking_number_hallucination(self):
        """Detect when response creates a fabricated tracking number."""
        fake_response = "Your package is on its way with tracking number TRK-DELHIVERY-999999."
        verified_data = {
            "shipment": {"tracking_number": "TRK-DELHIVERY-100013", "status": "IN_TRANSIT"}
        }

        result = self.validator.validate(fake_response, structured_data=verified_data)
        self.assertFalse(result.is_grounded)
        self.assertTrue(any("hallucinated tracking" in v.lower() for v in result.violations))

    def test_payment_failure_grounding(self):
        """Detect when response claims successful payment for a failed transaction."""
        fake_response = "Great news! Your payment was SUCCESSFUL and confirmed."
        verified_data = {
            "payment": {"status": "FAILED", "order_id": "ORD-009"}
        }

        result = self.validator.validate(fake_response, structured_data=verified_data)
        self.assertFalse(result.is_grounded)
        self.assertTrue(any("failed" in v.lower() for v in result.violations))

    def test_perfect_grounded_response(self):
        """Valid response matching database facts must pass without violations."""
        valid_response = "Your order ORD-013 is IN_TRANSIT with tracking number TRK-DELHIVERY-100013."
        verified_data = {
            "order": {"order_id": "ORD-013", "status": "IN_TRANSIT"},
            "shipment": {"tracking_number": "TRK-DELHIVERY-100013", "status": "IN_TRANSIT"}
        }

        result = self.validator.validate(valid_response, structured_data=verified_data)
        self.assertTrue(result.is_grounded)
        self.assertEqual(len(result.violations), 0)
        self.assertEqual(result.confidence, 1.0)


if __name__ == "__main__":
    unittest.main()

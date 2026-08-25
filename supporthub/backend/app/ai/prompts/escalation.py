"""Prompt templates for LLM-assisted escalation and sentiment evaluation."""

ESCALATION_EVALUATION_PROMPT = """Analyze the customer message for frustration, anger, legal threats, supervisor requests, or critical support deadlocks.

Customer Message:
"{message}"

Previous Turns Summary:
{turns_summary}

Determine if this interaction requires human agent handoff:
1. Is there an explicit request for a human or supervisor?
2. Is the customer threatening legal action, consumer court, or fraud complaint?
3. Is the customer expressing severe anger or repetitive unresolved deadlock?

Return JSON:
{
    "should_escalate": true/false,
    "urgency": "LOW" | "MEDIUM" | "HIGH" | "URGENT",
    "reason": "Clear explanation of escalation trigger",
    "sentiment": "NEUTRAL" | "FRUSTRATED" | "ANGRY" | "SATISFIED"
}
"""

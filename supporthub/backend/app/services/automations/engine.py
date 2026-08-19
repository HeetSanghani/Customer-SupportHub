"""
app/services/automations/engine.py

Production Workflow Automation Engine.
Evaluates active automation rules against tickets and executes configured actions.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import (
    Automation,
    Message,
    SenderType,
    Ticket,
    TicketChannel,
    TicketPriority,
    TicketStatus,
    User,
    UserRole,
    AuditLog,
)

logger = logging.getLogger(__name__)


def _matches_conditions(
    trigger_cfg: Dict[str, Any],
    ticket: Ticket,
    event_type: str,
    message_body: Optional[str] = None,
) -> bool:
    """Evaluates whether a ticket meets all trigger conditions."""
    # 1. Event Type Check
    rule_event = trigger_cfg.get("event_type", "any")
    if rule_event != "any" and rule_event != event_type:
        return False

    conditions = trigger_cfg.get("conditions", {})
    if not conditions:
        return True

    # 2. Channel Condition
    allowed_channels = conditions.get("channels") or conditions.get("channel")
    if allowed_channels:
        if isinstance(allowed_channels, str):
            allowed_channels = [allowed_channels]
        ticket_chan = ticket.channel.value if hasattr(ticket.channel, "value") else str(ticket.channel)
        if ticket_chan.lower() not in [c.lower() for c in allowed_channels]:
            return False

    # 3. Priority Condition
    target_priorities = conditions.get("priorities") or conditions.get("priority")
    if target_priorities:
        if isinstance(target_priorities, str):
            target_priorities = [target_priorities]
        ticket_prio = ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority)
        if ticket_prio.lower() not in [p.lower() for p in target_priorities]:
            return False

    # 4. Status Condition
    target_statuses = conditions.get("statuses") or conditions.get("status")
    if target_statuses:
        if isinstance(target_statuses, str):
            target_statuses = [target_statuses]
        ticket_stat = ticket.status.value if hasattr(ticket.status, "value") else str(ticket.status)
        if ticket_stat.lower() not in [s.lower() for s in target_statuses]:
            return False

    # 5. Category Condition
    target_categories = conditions.get("categories") or conditions.get("category")
    if target_categories:
        if isinstance(target_categories, str):
            target_categories = [target_categories]
        ticket_cat = ticket.category or ""
        if ticket_cat.lower() not in [c.lower() for c in target_categories]:
            return False

    # 6. Sentiment Condition
    target_sentiments = conditions.get("sentiments") or conditions.get("sentiment")
    if target_sentiments:
        if isinstance(target_sentiments, str):
            target_sentiments = [target_sentiments]
        ticket_senti = ticket.sentiment or ""
        if ticket_senti.lower() not in [s.lower() for s in target_sentiments]:
            return False

    # 7. Keyword / Phrase Substring Matching
    keywords = conditions.get("keywords") or conditions.get("keyword")
    if keywords:
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(",") if k.strip()]
        search_text = f"{ticket.subject or ''} {message_body or ''}".lower()
        has_match = any(kw.lower() in search_text for kw in keywords)
        if not has_match:
            return False

    return True


async def evaluate_ticket_automations(
    session: AsyncSession,
    ticket: Ticket,
    event_type: str = "ticket_created",
    message_body: Optional[str] = None,
    dry_run: bool = False,
) -> List[Dict[str, Any]]:
    """
    Evaluates all active automation rules against a ticket in priority order.
    If dry_run is True, returns simulated outcomes without persisting changes.
    """
    results: List[Dict[str, Any]] = []

    # Fetch active automations sorted by priority
    stmt = (
        select(Automation)
        .where(Automation.is_active == True)
        .order_by(Automation.priority.asc())
    )
    automations = (await session.exec(stmt)).all()

    if not automations:
        return results

    changes_made = False
    applied_actions_summary = []

    for rule in automations:
        try:
            trigger_cfg = json.loads(rule.trigger_json) if isinstance(rule.trigger_json, str) else rule.trigger_json
            action_cfg = json.loads(rule.action_json) if isinstance(rule.action_json, str) else rule.action_json
        except Exception as err:
            logger.warning("[Automation] Invalid JSON in rule %s: %s", rule.name, err)
            continue

        if not _matches_conditions(trigger_cfg, ticket, event_type, message_body):
            results.append({
                "rule_id": str(rule.id),
                "rule_name": rule.name,
                "matched": False,
                "actions": [],
            })
            continue

        # Rule Matched! Apply Actions
        executed_actions = []

        # Action: Set Priority
        if new_priority := action_cfg.get("set_priority"):
            try:
                ticket.priority = TicketPriority(new_priority)
                executed_actions.append(f"Set priority to '{new_priority}'")
                changes_made = True
            except Exception:
                pass

        # Action: Set Status
        if new_status := action_cfg.get("set_status"):
            try:
                ticket.status = TicketStatus(new_status)
                if new_status == "resolved":
                    ticket.ai_resolved = True
                executed_actions.append(f"Set status to '{new_status}'")
                changes_made = True
            except Exception:
                pass

        # Action: Set Category
        if new_category := action_cfg.get("set_category"):
            ticket.category = str(new_category)
            executed_actions.append(f"Set category to '{new_category}'")
            changes_made = True

        # Action: Assign Agent
        if assign_agent := action_cfg.get("assign_agent"):
            if assign_agent == "round_robin":
                # Find active agent with lowest ticket count
                agent_stmt = select(User).where(User.role == UserRole.agent, User.status == "active")
                agents = (await session.exec(agent_stmt)).all()
                if agents:
                    chosen_agent = agents[0]
                    ticket.agent_id = chosen_agent.id
                    executed_actions.append(f"Auto-assigned to agent '{chosen_agent.name}'")
                    changes_made = True
            elif isinstance(assign_agent, str) and assign_agent not in ("", "none", "unassigned"):
                try:
                    ticket.agent_id = uuid.UUID(assign_agent)
                    executed_actions.append(f"Assigned to agent ID {assign_agent}")
                    changes_made = True
                except Exception:
                    pass

        # Action: Send Automated / Canned Reply
        canned_reply = action_cfg.get("send_canned_reply") or action_cfg.get("auto_reply")
        if canned_reply and not dry_run:
            auto_msg = Message(
                ticket_id=ticket.id,
                sender_id=None,
                sender_type=SenderType.ai,
                body=str(canned_reply),
            )
            session.add(auto_msg)
            executed_actions.append(f"Dispatched automated reply: '{canned_reply[:40]}...'")
            changes_made = True

        # Action: Auto-Resolve Ticket
        if action_cfg.get("auto_resolve") and not dry_run:
            ticket.status = TicketStatus.resolved
            ticket.ai_resolved = True
            executed_actions.append("Marked ticket as resolved")
            changes_made = True

        results.append({
            "rule_id": str(rule.id),
            "rule_name": rule.name,
            "matched": True,
            "actions": executed_actions,
        })
        applied_actions_summary.extend(executed_actions)

        # If rule stops further evaluation
        if action_cfg.get("stop_further_evaluation", False):
            break

    if changes_made and not dry_run:
        ticket.updated_at = datetime.now()
        session.add(ticket)

        # Add Audit Log
        audit = AuditLog(
            action="automation.evaluated",
            entity_type="ticket",
            entity_id=str(ticket.id),
            ticket_id=ticket.id,
            diff_json=json.dumps({"actions": applied_actions_summary, "event_type": event_type}),
        )
        session.add(audit)
        await session.commit()
        await session.refresh(ticket)

        # Real-time WebSocket Broadcast
        try:
            from app.ws.manager import manager
            ticket_id_str = str(ticket.id)
            await manager.broadcast(ticket_id_str, {
                "type": "ticket_updated",
                "ticket_id": ticket_id_str,
                "status": ticket.status.value,
                "priority": ticket.priority.value,
                "category": ticket.category,
                "agent_id": str(ticket.agent_id) if ticket.agent_id else None,
            })
            await manager.broadcast_to_agents({
                "type": "inbox_update",
                "ticket_id": ticket_id_str,
                "status": ticket.status.value,
                "preview": f"Automations applied: {', '.join(applied_actions_summary[:2])}",
                "subject": ticket.subject,
            })
        except Exception as ws_err:
            logger.warning("[Automation WS] Broadcast failed: %s", ws_err)

    return results


async def get_default_automation_templates(created_by_id: uuid.UUID) -> List[Automation]:
    """Generates industry best-practice default automation rules for seeding."""
    now = datetime.now()
    return [
        Automation(
            name="Urgent Outage & Emergency Escalation",
            trigger_json=json.dumps({
                "event_type": "any",
                "conditions": {
                    "keywords": ["outage", "server down", "crash", "emergency", "system unavailable", "data loss"],
                },
            }),
            action_json=json.dumps({
                "set_priority": "urgent",
                "set_status": "escalated",
                "set_category": "Emergency Outage",
                "send_canned_reply": "We have detected an urgent system issue reported in your ticket. Our senior engineering response team has been immediately alerted.",
            }),
            is_active=True,
            priority=10,
            created_by=created_by_id,
            created_at=now,
            updated_at=now,
        ),
        Automation(
            name="Refund & Billing Auto-Categorization",
            trigger_json=json.dumps({
                "event_type": "ticket_created",
                "conditions": {
                    "keywords": ["refund", "billing", "invoice", "charge", "charged twice", "subscription cancel"],
                },
            }),
            action_json=json.dumps({
                "set_category": "Billing & Refunds",
                "set_priority": "high",
            }),
            is_active=True,
            priority=20,
            created_by=created_by_id,
            created_at=now,
            updated_at=now,
        ),
        Automation(
            name="VIP WhatsApp Support Routing",
            trigger_json=json.dumps({
                "event_type": "ticket_created",
                "conditions": {
                    "channels": ["whatsapp"],
                },
            }),
            action_json=json.dumps({
                "set_priority": "high",
                "set_category": "Mobile Priority",
            }),
            is_active=True,
            priority=30,
            created_by=created_by_id,
            created_at=now,
            updated_at=now,
        ),
        Automation(
            name="Negative Customer Sentiment Alert",
            trigger_json=json.dumps({
                "event_type": "any",
                "conditions": {
                    "sentiments": ["negative", "frustrated", "angry"],
                },
            }),
            action_json=json.dumps({
                "set_priority": "high",
                "set_status": "escalated",
            }),
            is_active=True,
            priority=40,
            created_by=created_by_id,
            created_at=now,
            updated_at=now,
        ),
        Automation(
            name="After-Hours Automated Acknowledgment",
            trigger_json=json.dumps({
                "event_type": "ticket_created",
                "conditions": {
                    "channels": ["email", "instagram", "facebook", "web"],
                },
            }),
            action_json=json.dumps({
                "send_canned_reply": "Thank you for reaching SupportHub! We have received your inquiry and our support team will respond promptly.",
            }),
            is_active=True,
            priority=50,
            created_by=created_by_id,
            created_at=now,
            updated_at=now,
        ),
    ]

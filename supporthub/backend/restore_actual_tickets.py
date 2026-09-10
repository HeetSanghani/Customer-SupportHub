import asyncio
import re
import uuid
from datetime import datetime
from sqlmodel import select, delete
from app.database import AsyncSessionLocal
from app.models import (
    User, UserRole, UserStatus,
    Ticket, TicketStatus, TicketPriority, TicketChannel,
    Message, SenderType,
    CsatRating, AuditLog
)

DUMP_PATH = "/home/python/Projects/Customer-SupportHub/supporthub_dump.sql"

def parse_dump_table(table_name):
    rows = []
    with open(DUMP_PATH, "r", encoding="utf-8") as f:
        in_table = False
        columns = []
        for line in f:
            if line.startswith(f"COPY public.{table_name} "):
                in_table = True
                m = re.search(r"\((.*?)\)", line)
                if m:
                    columns = [c.strip() for c in m.group(1).split(",")]
                continue
            if in_table:
                if line.strip() == r"\.":
                    break
                vals = line.rstrip("\n").split("\t")
                row = {}
                for col, val in zip(columns, vals):
                    row[col] = None if val == r"\N" else val
                rows.append(row)
    return rows

def parse_dt(val):
    if not val:
        return None
    # Remove timezone suffix like +00 if present or parse
    val = val.split("+")[0]
    try:
        return datetime.fromisoformat(val)
    except Exception:
        return None

async def restore_actual_data():
    print("🔄 Reading and parsing supporthub_dump.sql...")
    dump_users = parse_dump_table("users")
    dump_tickets = parse_dump_table("tickets")
    dump_messages = parse_dump_table("messages")
    dump_csats = parse_dump_table("csat_ratings")

    dump_user_map = {u["id"]: u for u in dump_users}

    async with AsyncSessionLocal() as session:
        # 1. Fetch Agent User
        agent_user = (await session.exec(select(User).where(User.email == "agent@supporthub.com"))).first()
        if not agent_user:
            raise RuntimeError("Agent User (agent@supporthub.com) not found in database!")
        agent_id = agent_user.id

        # 2. Delete any synthetic / seeded tickets created from clean_and_seed
        print("🗑️ Removing synthetic tickets created during clean_and_seed...")
        current_tickets = (await session.exec(select(Ticket))).all()
        for t in current_tickets:
            await session.exec(delete(CsatRating).where(CsatRating.ticket_id == t.id))
            await session.exec(delete(Message).where(Message.ticket_id == t.id))
            await session.delete(t)
        await session.commit()
        print("✅ Cleared existing synthetic tickets.")

        # 3. Ensure all users referenced by the original tickets and messages exist in the database
        needed_uids = set()
        for t in dump_tickets:
            if t.get("customer_id"):
                needed_uids.add(t["customer_id"])
        for m in dump_messages:
            if m.get("sender_id"):
                needed_uids.add(m["sender_id"])

        print(f"👥 Checking {len(needed_uids)} required user records...")
        for uid in needed_uids:
            # Skip Emma Wilson if in needed_uids (her tickets/messages will be assigned to agent_user)
            u_dump = dump_user_map.get(uid)
            if u_dump and u_dump.get("email") == "emma.wilson@supporthub.com":
                continue

            existing_u = await session.get(User, uuid.UUID(uid))
            if not existing_u and u_dump:
                # Insert missing user record from dump
                role_str = u_dump.get("role", "customer")
                try:
                    role_enum = UserRole(role_str)
                except Exception:
                    role_enum = UserRole.customer

                status_str = u_dump.get("status", "active")
                try:
                    status_enum = UserStatus(status_str)
                except Exception:
                    status_enum = UserStatus.active

                new_user = User(
                    id=uuid.UUID(uid),
                    email=u_dump.get("email", f"user_{uid[:8]}@example.com"),
                    name=u_dump.get("name", "Customer"),
                    password_hash=u_dump.get("password_hash") or "$2b$12$Xdx3.OlMYmoNgCSJ7yjVNesdEJ5eIeCKvaN6vZPsvDaNO8jvNXgs2",
                    role=role_enum,
                    status=status_enum,
                    avatar_url=u_dump.get("avatar_url"),
                    phone=u_dump.get("phone"),
                    channel=u_dump.get("channel"),
                    channel_customer_id=u_dump.get("channel_customer_id"),
                    customer_id=u_dump.get("customer_id"),
                    created_at=parse_dt(u_dump.get("created_at")) or datetime.now(),
                    updated_at=parse_dt(u_dump.get("updated_at")) or datetime.now(),
                )
                session.add(new_user)
        await session.commit()
        print("✅ Required users verified and restored.")

        # 4. Restore all 79 original actual tickets
        print(f"🎫 Restoring {len(dump_tickets)} actual tickets...")
        for t_data in dump_tickets:
            t_id = uuid.UUID(t_data["id"])
            cust_id = uuid.UUID(t_data["customer_id"]) if t_data.get("customer_id") else None

            # All agent assignments routed to Agent User
            assigned_agent_id = agent_id if t_data.get("agent_id") else None

            # Channel enum
            ch_val = t_data.get("channel", "website_chat")
            try:
                ch_enum = TicketChannel(ch_val)
            except Exception:
                ch_enum = TicketChannel.website_chat

            # Status enum
            st_val = t_data.get("status", "open")
            try:
                st_enum = TicketStatus(st_val)
            except Exception:
                st_enum = TicketStatus.open

            # Priority enum
            pr_val = t_data.get("priority", "medium")
            try:
                pr_enum = TicketPriority(pr_val)
            except Exception:
                pr_enum = TicketPriority.medium

            ticket_obj = Ticket(
                id=t_id,
                ref=t_data.get("ref") or f"TCK-{str(t_id)[:5]}",
                customer_id=cust_id,
                agent_id=assigned_agent_id,
                subject=t_data.get("subject") or "Support Request",
                category=t_data.get("category") or "general",
                channel=ch_enum,
                status=st_enum,
                priority=pr_enum,
                sla_due_at=parse_dt(t_data.get("sla_due_at")),
                sla_breached=(t_data.get("sla_breached") == "t"),
                sentiment=t_data.get("sentiment"),
                ai_confidence=float(t_data["ai_confidence"]) if t_data.get("ai_confidence") else None,
                ai_resolved=(t_data.get("ai_resolved") == "t"),
                ai_summary=t_data.get("ai_summary"),
                deleted_at=parse_dt(t_data.get("deleted_at")),
                created_at=parse_dt(t_data.get("created_at")) or datetime.now(),
                updated_at=parse_dt(t_data.get("updated_at")) or datetime.now(),
            )
            session.add(ticket_obj)

        await session.commit()
        print(f"✅ Restored {len(dump_tickets)} actual tickets!")

        # 5. Restore all original messages
        print(f"💬 Restoring {len(dump_messages)} actual messages...")
        for m_data in dump_messages:
            m_id = uuid.UUID(m_data["id"])
            t_id = uuid.UUID(m_data["ticket_id"])
            
            # Sender type
            stype_val = m_data.get("sender_type", "customer")
            try:
                stype_enum = SenderType(stype_val)
            except Exception:
                stype_enum = SenderType.customer

            # Sender ID: if agent was Emma Wilson, assign to Agent User
            s_id = None
            if m_data.get("sender_id"):
                raw_sid = m_data["sender_id"]
                u_dump = dump_user_map.get(raw_sid)
                if u_dump and u_dump.get("email") == "emma.wilson@supporthub.com":
                    s_id = agent_id
                elif stype_enum == SenderType.agent:
                    s_id = agent_id
                else:
                    s_id = uuid.UUID(raw_sid)

            msg_obj = Message(
                id=m_id,
                ticket_id=t_id,
                sender_id=s_id,
                sender_type=stype_enum,
                body=m_data.get("body") or "",
                body_html=m_data.get("body_html"),
                attachments=m_data.get("attachments"),
                external_message_id=m_data.get("external_message_id"),
                created_at=parse_dt(m_data.get("created_at")) or datetime.now(),
            )
            session.add(msg_obj)

        await session.commit()
        print(f"✅ Restored {len(dump_messages)} actual messages!")

        # 6. Restore CSAT ratings
        print(f"⭐ Restoring {len(dump_csats)} CSAT ratings...")
        for c_data in dump_csats:
            c_id = uuid.UUID(c_data["id"])
            t_id = uuid.UUID(c_data["ticket_id"])
            cust_id = uuid.UUID(c_data["customer_id"])
            rating_val = int(c_data.get("rating", 5))

            csat_obj = CsatRating(
                id=c_id,
                ticket_id=t_id,
                customer_id=cust_id,
                rating=rating_val,
                comment=c_data.get("comment"),
                created_at=parse_dt(c_data.get("created_at")) or datetime.now(),
            )
            session.add(csat_obj)

        await session.commit()
        print(f"✅ Restored {len(dump_csats)} CSAT ratings!")

        # 7. Ensure Emma Wilson is permanently absent
        emma = (await session.exec(select(User).where(User.email == "emma.wilson@supporthub.com"))).first()
        if emma:
            await session.delete(emma)
            await session.commit()

        print("\n🎉 Actual tickets and conversations fully restored from supporthub_dump.sql!")

if __name__ == "__main__":
    asyncio.run(restore_actual_data())

import asyncio
import uuid
import random
from datetime import datetime, timedelta, timezone
from sqlmodel import select
from app.database import AsyncSessionLocal
from app.models import User, UserRole, Ticket, TicketStatus, TicketPriority, TicketChannel, CsatRating

async def seed_data():
    async with AsyncSessionLocal() as session:
        # 1. Fetch existing users
        res = await session.exec(select(User))
        users = res.all()
        
        customers = [u for u in users if u.role == UserRole.customer]
        agents = [u for u in users if u.role == UserRole.agent]

        if not customers:
            print("No customers found. Creating default customer...")
            from app.routers.auth import hash_password
            cust = User(
                email="john.smith@example.com",
                name="John Smith",
                password_hash=hash_password("Password123!"),
                role=UserRole.customer,
                status="active"
            )
            session.add(cust)
            await session.commit()
            await session.refresh(cust)
            customers = [cust]

        if not agents:
            print("No agents found. Creating default agent...")
            from app.routers.auth import hash_password
            agent = User(
                email="emma.wilson@supporthub.com",
                name="Emma Wilson",
                password_hash=hash_password("Password123!"),
                role=UserRole.agent,
                status="active"
            )
            session.add(agent)
            await session.commit()
            await session.refresh(agent)
            agents = [agent]

        # Ensure additional customers for rich CSAT data
        customer_names = [
            ("Sarah Johnson", "sarah.j@example.com"),
            ("Rahul Sharma", "rahul.s@example.com"),
            ("Priya Patel", "priya.p@example.com"),
            ("Alex Thomas", "alex.t@example.com"),
            ("David Brown", "david.b@example.com"),
            ("Michael Chen", "michael.c@example.com"),
            ("Elena Rostova", "elena.r@example.com")
        ]

        for name, email in customer_names:
            r = await session.exec(select(User).where(User.email == email))
            if not r.first():
                from app.routers.auth import hash_password
                u = User(
                    email=email,
                    name=name,
                    password_hash=hash_password("Password123!"),
                    role=UserRole.customer,
                    status="active"
                )
                session.add(u)
                await session.commit()
                customers.append(u)

        # 2. Check existing tickets
        r_t = await session.exec(select(Ticket))
        existing_tickets = r_t.all()

        sample_tickets = [
            # Email channel
            {"subject": "Need corporate invoice with GSTIN number", "category": "Billing", "channel": TicketChannel.email, "status": TicketStatus.resolved, "priority": TicketPriority.medium, "ai_resolved": True},
            {"subject": "App crashes when uploading high-res profile photo", "category": "Technical", "channel": TicketChannel.email, "status": TicketStatus.open, "priority": TicketPriority.urgent, "ai_resolved": False},
            {"subject": "Request for annual plan tax certificate", "category": "Billing", "channel": TicketChannel.email, "status": TicketStatus.closed, "priority": TicketPriority.low, "ai_resolved": True},
            {"subject": "Enterprise SSO SAML integration setup guide", "category": "Technical", "channel": TicketChannel.email, "status": TicketStatus.new, "priority": TicketPriority.high, "ai_resolved": False},
            
            # Website Chat channel
            {"subject": "Two-factor authentication login code not arriving", "category": "Technical", "channel": TicketChannel.website_chat, "status": TicketStatus.resolved, "priority": TicketPriority.high, "ai_resolved": False},
            {"subject": "Inquiry about Pro Plan seat upgrade discount", "category": "Sales", "channel": TicketChannel.website_chat, "status": TicketStatus.open, "priority": TicketPriority.medium, "ai_resolved": True},
            {"subject": "Password reset token expired error", "category": "Technical", "channel": TicketChannel.website_chat, "status": TicketStatus.resolved, "priority": TicketPriority.medium, "ai_resolved": True},
            {"subject": "Chat widget styling customization in dark mode", "category": "General", "channel": TicketChannel.website_chat, "status": TicketStatus.waiting, "priority": TicketPriority.low, "ai_resolved": False},

            # WhatsApp channel
            {"subject": "Order #88213 stuck in Processing status", "category": "Orders", "channel": TicketChannel.whatsapp, "status": TicketStatus.waiting, "priority": TicketPriority.medium, "ai_resolved": False},
            {"subject": "Delivery address modification request for #88240", "category": "Orders", "channel": TicketChannel.whatsapp, "status": TicketStatus.resolved, "priority": TicketPriority.high, "ai_resolved": False},
            {"subject": "WhatsApp notification subscription confirmation", "category": "General", "channel": TicketChannel.whatsapp, "status": TicketStatus.closed, "priority": TicketPriority.low, "ai_resolved": True},

            # Instagram channel
            {"subject": "Refund not received after 10 business days", "category": "Refund", "channel": TicketChannel.instagram, "status": TicketStatus.escalated, "priority": TicketPriority.urgent, "ai_resolved": False},
            {"subject": "Influencer partnership discount code verification", "category": "Sales", "channel": TicketChannel.instagram, "status": TicketStatus.resolved, "priority": TicketPriority.medium, "ai_resolved": True},

            # Facebook channel
            {"subject": "Downgrade plan request before next billing cycle", "category": "Billing", "channel": TicketChannel.facebook, "status": TicketStatus.open, "priority": TicketPriority.medium, "ai_resolved": False},
            {"subject": "Facebook Messenger bot automation query", "category": "Technical", "channel": TicketChannel.facebook, "status": TicketStatus.resolved, "priority": TicketPriority.low, "ai_resolved": True},
        ]

        created_tickets = []
        for i, st in enumerate(sample_tickets):
            # generate reference
            ref = f"TCK-10{234 + i}"
            existing = await session.exec(select(Ticket).where(Ticket.ref == ref))
            if existing.first():
                continue
            
            cust = random.choice(customers)
            ag = random.choice(agents) if st["status"] != TicketStatus.new else None

            ticket = Ticket(
                ref=ref,
                customer_id=cust.id,
                agent_id=ag.id if ag else None,
                subject=st["subject"],
                category=st["category"],
                channel=st["channel"],
                status=st["status"],
                priority=st["priority"],
                ai_resolved=st["ai_resolved"],
                created_at=datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 120))
            )
            session.add(ticket)
            created_tickets.append(ticket)

        await session.commit()
        print(f"Created {len(created_tickets)} sample tickets across channels.")

        # 3. Add CSAT Ratings for resolved/closed tickets
        r_all_tickets = await session.exec(select(Ticket))
        all_t = r_all_tickets.all()
        resolved_tickets = [t for t in all_t if t.status in (TicketStatus.resolved, TicketStatus.closed)]

        csat_comments = [
            (5, "Super fast resolution! The AI agent resolved my invoice update in less than 2 minutes."),
            (5, "Emma was extremely helpful on live chat and fixed my account settings immediately."),
            (5, "Outstanding support! Received my bypass link quickly and was able to log back in."),
            (4, "Good overall response. The issue was solved well within the SLA timeline."),
            (5, "Very smooth process. Highly impressed with the omnichannel support experience."),
            (4, "Clear instructions provided by the agent. Thank you!"),
            (5, "The instant resolution saved me so much time today. Great job SupportHub!"),
            (3, "Took a bit longer to connect to an agent during peak hours, but resolved satisfactorily."),
            (5, "Excellent service and friendly support team."),
            (4, "Prompt response on WhatsApp!")
        ]

        csat_created = 0
        for idx, t in enumerate(resolved_tickets):
            # check if csat exists for ticket
            r_c = await session.exec(select(CsatRating).where(CsatRating.ticket_id == t.id))
            if not r_c.first():
                rating, comment = csat_comments[idx % len(csat_comments)]
                csat = CsatRating(
                    ticket_id=t.id,
                    customer_id=t.customer_id,
                    rating=rating,
                    comment=comment,
                    created_at=t.created_at + timedelta(minutes=random.randint(10, 60))
                )
                session.add(csat)
                csat_created += 1

        await session.commit()
        print(f"Created {csat_created} CSAT ratings with customer reviews.")

        # 4. Seed Channel Integrations if empty
        from app.models import ChannelIntegration, ChannelType, ChannelStatus
        r_channels = await session.exec(select(ChannelIntegration))
        if not r_channels.all():
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            default_channels = [
                ChannelIntegration(channel_type=ChannelType.email, display_name="support@supporthub.com", status=ChannelStatus.connected, weekly_volume=2, created_at=now, updated_at=now),
                ChannelIntegration(channel_type=ChannelType.website_chat, display_name="chat.supporthub.com", status=ChannelStatus.connected, weekly_volume=12, created_at=now, updated_at=now),
            ]
            for ch in default_channels:
                session.add(ch)
            await session.commit()
            print("Seeded real connected channel integrations (Email & Website Chat).")

if __name__ == "__main__":
    asyncio.run(seed_data())

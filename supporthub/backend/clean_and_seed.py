import asyncio
import uuid
import random
from datetime import datetime, timedelta, timezone
from sqlmodel import select
from app.database import AsyncSessionLocal
from app.models import (
    User, UserRole, UserStatus,
    Ticket, TicketStatus, TicketPriority, TicketChannel,
    Message, SenderType,
    CsatRating,
    AuditLog,
    EmailLog,
    Automation,
    Macro,
    QuickReply,
    KbArticle,
    ChannelIntegration, ChannelType, ChannelStatus
)
from app.routers.auth import hash_password

async def run_clean_and_seed():
    async with AsyncSessionLocal() as session:
        print("🧹 Starting Database Cleanup & Pristine Seeding...")

        # 1. Fetch Admin user to reassign system-level foreign keys
        admin_res = await session.exec(select(User).where(User.email == "admin@supporthub.com"))
        admin_user = admin_res.first()
        if not admin_user:
            admin_user = User(
                email="admin@supporthub.com",
                name="Admin User",
                password_hash=hash_password("Password123!"),
                role=UserRole.admin,
                status=UserStatus.active,
            )
            session.add(admin_user)
            await session.commit()
            await session.refresh(admin_user)

        # Reassign Automations, Macros, KB Articles to Admin User
        automations = (await session.exec(select(Automation))).all()
        for a in automations:
            a.created_by = admin_user.id
            session.add(a)

        kb_articles = (await session.exec(select(KbArticle))).all()
        for kb in kb_articles:
            kb.created_by = admin_user.id
            session.add(kb)

        await session.commit()
        print("✅ System references updated to primary admin.")

        # 2. Define clean set of allowed users
        allowed_users_data = [
            # Admins
            {"email": "admin@supporthub.com", "name": "Admin User", "role": UserRole.admin, "phone": "+1 (555) 010-0001"},
            {"email": "heets.brainerhub@gmail.com", "name": "Heet Patel", "role": UserRole.admin, "phone": "+1 (555) 010-0002"},
            
            # Managers
            {"email": "manager@supporthub.com", "name": "Manager User", "role": UserRole.manager, "phone": "+1 (555) 010-0003"},
            {"email": "priya.p@example.com", "name": "Priya Patel", "role": UserRole.manager, "phone": "+1 (555) 010-0004"},

            # Agents (Single dedicated agent)
            {"email": "agent@supporthub.com", "name": "Agent User", "role": UserRole.agent, "phone": "+1 (555) 010-0005"},

            # Customers (Canonical 25 seed customers)
            {"email": "customer@supporthub.com", "name": "Aarav Sharma", "role": UserRole.customer, "phone": "+91-9876543210", "customer_id": "CUST-001", "address": "Flat 402, Green Glen Layout, Outer Ring Road, Bellandur", "city": "Bengaluru", "state": "Karnataka", "postal_code": "560103", "country": "India"},
            {"email": "sarah.j@example.com", "name": "Sarah Johnson", "role": UserRole.customer, "phone": "+1 (555) 234-5678", "customer_id": "CUST-002"},
            {"email": "rohan.verma@example.com", "name": "Rohan Verma", "role": UserRole.customer, "phone": "+91-9811234567", "customer_id": "CUST-003", "city": "New Delhi", "state": "Delhi", "country": "India"},
            {"email": "ananya.reddy@example.com", "name": "Ananya Reddy", "role": UserRole.customer, "phone": "+91-9440123456", "customer_id": "CUST-004", "city": "Hyderabad", "state": "Telangana", "country": "India"},
            {"email": "vikram.iyer@example.com", "name": "Vikram Iyer", "role": UserRole.customer, "phone": "+91-9840123456", "customer_id": "CUST-005", "city": "Chennai", "state": "Tamil Nadu", "country": "India"},
            {"email": "sneha.kulkarni@example.com", "name": "Sneha Kulkarni", "role": UserRole.customer, "phone": "+91-9764123456", "customer_id": "CUST-006", "city": "Pune", "state": "Maharashtra", "country": "India"},
            {"email": "rajesh.banerjee@example.com", "name": "Rajesh Banerjee", "role": UserRole.customer, "phone": "+91-9830123456", "customer_id": "CUST-007", "city": "Kolkata", "state": "West Bengal", "country": "India"},
            {"email": "kavita.deshmukh@example.com", "name": "Kavita Deshmukh", "role": UserRole.customer, "phone": "+91-9822123456", "customer_id": "CUST-008", "city": "Pune", "state": "Maharashtra", "country": "India"},
            {"email": "aditya.nair@example.com", "name": "Aditya Nair", "role": UserRole.customer, "phone": "+91-9847123456", "customer_id": "CUST-009", "city": "Kochi", "state": "Kerala", "country": "India"},
            {"email": "neha.gupta@example.com", "name": "Neha Gupta", "role": UserRole.customer, "phone": "+91-9810123456", "customer_id": "CUST-010", "city": "Gurugram", "state": "Haryana", "country": "India"},
            {"email": "siddharth.c@example.com", "name": "Siddharth Choudhury", "role": UserRole.customer, "phone": "+91-9435123456", "customer_id": "CUST-011", "city": "Guwahati", "state": "Assam", "country": "India"},
            {"email": "pooja.joshi@example.com", "name": "Pooja Joshi", "role": UserRole.customer, "phone": "+91-9414123456", "customer_id": "CUST-012", "city": "Jaipur", "state": "Rajasthan", "country": "India"},
            {"email": "manish.tiwari@example.com", "name": "Manish Tiwari", "role": UserRole.customer, "phone": "+91-9450123456", "customer_id": "CUST-013", "city": "Lucknow", "state": "Uttar Pradesh", "country": "India"},
            {"email": "deepika.rao@example.com", "name": "Deepika Rao", "role": UserRole.customer, "phone": "+91-9844123456", "customer_id": "CUST-014", "city": "Bengaluru", "state": "Karnataka", "country": "India"},
            {"email": "karan.mehta@example.com", "name": "Karan Mehta", "role": UserRole.customer, "phone": "+91-9879123456", "customer_id": "CUST-015", "city": "Ahmedabad", "state": "Gujarat", "country": "India"},
            {"email": "meera.menon@example.com", "name": "Meera Menon", "role": UserRole.customer, "phone": "+91-9846123456", "customer_id": "CUST-016", "city": "Thiruvananthapuram", "state": "Kerala", "country": "India"},
            {"email": "arjun.kapoor@example.com", "name": "Arjun Kapoor", "role": UserRole.customer, "phone": "+91-9818123456", "customer_id": "CUST-017", "city": "Noida", "state": "Uttar Pradesh", "country": "India"},
            {"email": "ritu.agarwal@example.com", "name": "Ritu Agarwal", "role": UserRole.customer, "phone": "+91-9331123456", "customer_id": "CUST-018", "city": "Kolkata", "state": "West Bengal", "country": "India"},
            {"email": "amit.singhania@example.com", "name": "Amit Singhania", "role": UserRole.customer, "phone": "+91-9826123456", "customer_id": "CUST-019", "city": "Indore", "state": "Madhya Pradesh", "country": "India"},
            {"email": "shweta.bhatia@example.com", "name": "Shweta Bhatia", "role": UserRole.customer, "phone": "+91-9814123456", "customer_id": "CUST-020", "city": "Chandigarh", "state": "Chandigarh", "country": "India"},
            {"email": "rahul.d@example.com", "name": "Rahul Dravid", "role": UserRole.customer, "phone": "+91-9880123456", "customer_id": "CUST-021", "city": "Bengaluru", "state": "Karnataka", "country": "India"},
            {"email": "divya.sri@example.com", "name": "Divya Srivastava", "role": UserRole.customer, "phone": "+91-9415123456", "customer_id": "CUST-022", "city": "Lucknow", "state": "Uttar Pradesh", "country": "India"},
            {"email": "gaurav.saxena@example.com", "name": "Gaurav Saxena", "role": UserRole.customer, "phone": "+91-9829123456", "customer_id": "CUST-023", "city": "Jaipur", "state": "Rajasthan", "country": "India"},
            {"email": "suresh.pandey@example.com", "name": "Suresh Pandey", "role": UserRole.customer, "phone": "+91-9871123456", "customer_id": "CUST-024", "city": "Gurugram", "state": "Haryana", "country": "India"},
            {"email": "tanya.malhotra@example.com", "name": "Tanya Malhotra", "role": UserRole.customer, "phone": "+91-9811987654", "customer_id": "CUST-025", "city": "New Delhi", "state": "Delhi", "country": "India"},
            {"email": "alex.t@example.com", "name": "Alex Turner", "role": UserRole.customer, "phone": "+1 (555) 345-6789", "customer_id": "CUST-026"},
            {"email": "michael.c@example.com", "name": "Michael Chen", "role": UserRole.customer, "phone": "+1 (555) 456-7890", "customer_id": "CUST-027"},
            {"email": "rahul.s@example.com", "name": "Rahul Sharma", "role": UserRole.customer, "phone": "+91-9899123456", "customer_id": "CUST-028"},
            {"email": "david.b@example.com", "name": "David Brown", "role": UserRole.customer, "phone": "+1 (555) 567-8901", "customer_id": "CUST-029"},
            {"email": "elena.r@example.com", "name": "Elena Rostova", "role": UserRole.customer, "phone": "+1 (555) 678-9012", "customer_id": "CUST-030"},
            {"email": "mihirk.brainerhub@gmail.com", "name": "Mihir", "role": UserRole.customer},

            # Omnichannel Customer Profiles
            {"email": "whatsapp_919824052103@channel.supporthub.internal", "name": "👑 Heet Sanghani 👑", "role": UserRole.customer, "phone": "+91 98240 52103", "channel": "whatsapp", "channel_customer_id": "919824052103"},
            {"email": "instagram_2308674163238603@supporthub.local", "name": "Heet Sanghani", "role": UserRole.customer, "channel": "instagram", "channel_customer_id": "2308674163238603"},
            {"email": "messenger_38499898592930667@supporthub.local", "name": "Heet Sanghani", "role": UserRole.customer, "channel": "facebook", "channel_customer_id": "38499898592930667"},
            {"email": "instagram_1038307988929264@supporthub.local", "name": "Akash Soni", "role": UserRole.customer, "channel": "instagram", "channel_customer_id": "1038307988929264"},
            {"email": "instagram_3186178738258152@supporthub.local", "name": "Mihir Kanzariya", "role": UserRole.customer, "channel": "instagram", "channel_customer_id": "3186178738258152"},
            {"email": "instagram_26806233522386775@supporthub.local", "name": "Zaru Patel", "role": UserRole.customer, "channel": "instagram", "channel_customer_id": "26806233522386775"},
        ]

        allowed_emails = {u["email"] for u in allowed_users_data}

        # 3. Clean up all tickets, messages, CSATs, and audit logs to start fresh with pristine data
        print("🗑️ Purging legacy tickets, messages, CSAT ratings, and audit logs...")
        await session.exec(select(CsatRating))
        csats = (await session.exec(select(CsatRating))).all()
        for c in csats:
            await session.delete(c)

        msgs = (await session.exec(select(Message))).all()
        for m in msgs:
            await session.delete(m)

        audits = (await session.exec(select(AuditLog))).all()
        for a in audits:
            await session.delete(a)

        email_logs = (await session.exec(select(EmailLog))).all()
        for el in email_logs:
            await session.delete(el)

        tickets = (await session.exec(select(Ticket))).all()
        for t in tickets:
            await session.delete(t)

        await session.commit()
        print("✅ Cleaned old ticket and message artifacts.")

        # 4. Remove extraneous / junk users
        all_db_users = (await session.exec(select(User))).all()
        deleted_user_count = 0
        for u in all_db_users:
            if u.email not in allowed_emails:
                await session.delete(u)
                deleted_user_count += 1

        await session.commit()
        print(f"✅ Removed {deleted_user_count} extraneous test users.")

        # 5. Ensure all allowed users exist and are properly configured
        user_map = {}
        for u_data in allowed_users_data:
            existing = (await session.exec(select(User).where(User.email == u_data["email"]))).first()
            if not existing:
                new_u = User(
                    email=u_data["email"],
                    name=u_data["name"],
                    password_hash=hash_password("Password123!"),
                    role=u_data["role"],
                    status=UserStatus.active,
                    phone=u_data.get("phone"),
                    channel=u_data.get("channel"),
                    channel_customer_id=u_data.get("channel_customer_id"),
                    customer_id=u_data.get("customer_id"),
                    address=u_data.get("address"),
                    city=u_data.get("city"),
                    state=u_data.get("state"),
                    postal_code=u_data.get("postal_code"),
                    country=u_data.get("country"),
                )
                session.add(new_u)
                await session.commit()
                await session.refresh(new_u)
                user_map[u_data["email"]] = new_u
            else:
                existing.name = u_data["name"]
                existing.role = u_data["role"]
                existing.status = UserStatus.active
                if "phone" in u_data:
                    existing.phone = u_data["phone"]
                if "channel" in u_data:
                    existing.channel = u_data["channel"]
                if "channel_customer_id" in u_data:
                    existing.channel_customer_id = u_data["channel_customer_id"]
                if "customer_id" in u_data:
                    existing.customer_id = u_data["customer_id"]
                if "address" in u_data:
                    existing.address = u_data["address"]
                if "city" in u_data:
                    existing.city = u_data["city"]
                if "state" in u_data:
                    existing.state = u_data["state"]
                if "postal_code" in u_data:
                    existing.postal_code = u_data["postal_code"]
                if "country" in u_data:
                    existing.country = u_data["country"]
                session.add(existing)
                await session.commit()
                await session.refresh(existing)
                user_map[u_data["email"]] = existing

        print(f"✅ Pristine user directory established ({len(user_map)} users).")

        # 6. Seed Helpful Macros
        existing_macros = (await session.exec(select(Macro))).all()
        if not existing_macros:
            sample_macros = [
                Macro(
                    title="Warm Greeting & Acknowledgment",
                    category="General",
                    body="Hello {{customer.name}}!\n\nThank you for reaching out to SupportHub. I am reviewing your inquiry right now and will assist you step by step.\n\nBest regards,\n{{agent.name}}",
                    created_by=admin_user.id
                ),
                Macro(
                    title="Password Reset Instructions",
                    category="Technical",
                    body="Hi {{customer.name}},\n\nTo reset your password, please navigate to Settings > Security and click 'Request Password Reset'. A secure verification link will be sent to your registered email address.\n\nLet us know if you need further help!\n{{agent.name}}",
                    created_by=admin_user.id
                ),
                Macro(
                    title="Invoice & Billing Receipt Dispatched",
                    category="Billing",
                    body="Hi {{customer.name}},\n\nI have generated and attached the updated tax invoice with your company details. You can also download it at any time from your Billing Dashboard.\n\nBest regards,\nSupportHub Billing Team",
                    created_by=admin_user.id
                ),
                Macro(
                    title="Ticket Resolution & Feedback Request",
                    category="General",
                    body="Hello {{customer.name}},\n\nI am glad we were able to resolve your inquiry today. I will mark this ticket as resolved. Please take a quick moment to rate your support experience!\n\nHave a wonderful day,\n{{agent.name}}",
                    created_by=admin_user.id
                ),
            ]
            for m in sample_macros:
                session.add(m)
            await session.commit()
            print("✅ Canned Macros created.")

        # 6b. Seed Quick Reply Templates
        existing_qr = (await session.exec(select(QuickReply))).all()
        if not existing_qr:
            sample_qr = [
                QuickReply(
                    category="Billing",
                    keyword_pattern="refund, money back, credit",
                    response_text="Your refund has been processed and should appear in 5-7 business days.",
                    priority=1,
                ),
                QuickReply(
                    category="Orders",
                    keyword_pattern="track, order status, where is my order",
                    response_text="I checked your order status — it is currently in transit. You can track your shipment live under the Orders tab in your dashboard.",
                    priority=2,
                ),
                QuickReply(
                    category="Returns",
                    keyword_pattern="return, replace, exchange",
                    response_text="To initiate a return, visit your Orders page, select your order, and click Request Return. Items can be returned within 30 days of delivery.",
                    priority=3,
                ),
                QuickReply(
                    category="Shipping",
                    keyword_pattern="delivery, shipping, courier",
                    response_text="Standard delivery takes 3–5 business days for metro areas and 5–7 business days for non-metro locations.",
                    priority=4,
                ),
                QuickReply(
                    category="Billing",
                    keyword_pattern="refund policy, cancel refund",
                    response_text="Refunds are initiated within 2 to 4 hours of courier pickup for damaged items, and credited to your original payment method.",
                    priority=5,
                ),
            ]
            for qr in sample_qr:
                session.add(qr)
            await session.commit()
            print("✅ Quick Reply templates created.")

        # 7. Seed Pristine Tickets Across All 5 Channels
        agent_user = user_map["agent@supporthub.com"]
        agent_emma = agent_user  # All agent assignments go to Agent User
        cust_sarah = user_map["sarah.j@example.com"]
        cust_alex = user_map["alex.t@example.com"]
        cust_michael = user_map["michael.c@example.com"]
        cust_rahul = user_map["rahul.s@example.com"]
        cust_david = user_map["david.b@example.com"]
        cust_elena = user_map["elena.r@example.com"]
        cust_user = user_map["customer@supporthub.com"]
        cust_heet_wa = user_map["whatsapp_919824052103@channel.supporthub.internal"]
        cust_heet_ig = user_map["instagram_2308674163238603@supporthub.local"]
        cust_heet_fb = user_map["messenger_38499898592930667@supporthub.local"]
        cust_akash_ig = user_map["instagram_1038307988929264@supporthub.local"]
        cust_mihir_ig = user_map["instagram_3186178738258152@supporthub.local"]
        cust_zaru_ig = user_map["instagram_26806233522386775@supporthub.local"]

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        ticket_seeds = [
            # === EMAIL TICKETS ===
            {
                "ref": "TCK-10101",
                "customer": cust_sarah,
                "agent": agent_emma,
                "subject": "Need corporate tax invoice with GSTIN breakdown",
                "category": "Billing",
                "channel": TicketChannel.email,
                "status": TicketStatus.resolved,
                "priority": TicketPriority.medium,
                "ai_resolved": False,
                "sentiment": "positive",
                "ai_confidence": 0.94,
                "created_hours_ago": 36,
                "messages": [
                    (SenderType.customer, cust_sarah.id, "Hi Support Team, Could you please generate and email us our updated corporate tax invoice including our GSTIN registration for our annual audit? Thank you!"),
                    (SenderType.agent, agent_emma.id, "Hello Sarah! I have generated the updated corporate invoice with your GSTIN credentials and attached it to your account billing records. You can also view it in your dashboard."),
                    (SenderType.customer, cust_sarah.id, "Received, that was very fast and accurate. Thank you Emma!")
                ],
                "csat": (5, "Super fast resolution! Emma was extremely helpful and polite.")
            },
            {
                "ref": "TCK-10102",
                "customer": cust_michael,
                "agent": agent_user,
                "subject": "Enterprise SSO SAML 2.0 Integration Setup Guide",
                "category": "Technical",
                "channel": TicketChannel.email,
                "status": TicketStatus.open,
                "priority": TicketPriority.high,
                "ai_resolved": False,
                "sentiment": "neutral",
                "ai_confidence": 0.88,
                "created_hours_ago": 8,
                "messages": [
                    (SenderType.customer, cust_michael.id, "Hello, We are currently configuring Okta SAML 2.0 authentication for our enterprise team. Could you share the SP metadata XML and ACS URL?"),
                    (SenderType.agent, agent_user.id, "Hi Michael, Thanks for reaching out. Here is the direct link to our SAML Configuration Guide along with the metadata endpoint: https://supporthub.com/docs/sso. Please let us know if you need assistance configuring claims.")
                ]
            },
            {
                "ref": "TCK-10103",
                "customer": cust_elena,
                "agent": None,
                "subject": "Annual subscription discount inquiry for non-profit",
                "category": "Sales",
                "channel": TicketChannel.email,
                "status": TicketStatus.new,
                "priority": TicketPriority.low,
                "ai_resolved": False,
                "sentiment": "positive",
                "ai_confidence": 0.91,
                "created_hours_ago": 2,
                "messages": [
                    (SenderType.customer, cust_elena.id, "Good day SupportHub team, We represent an educational non-profit organization. Do you offer special non-profit tier pricing or annual discounts?"),
                    (SenderType.ai, None, "Hello Elena! Thank you for contacting SupportHub Email Support regarding your non-profit pricing inquiry. We offer up to 40% discount for registered non-profits. Our sales team will reach out shortly!")
                ]
            },
            {
                "ref": "TCK-10104",
                "customer": cust_user,
                "agent": agent_emma,
                "subject": "Assistance with account email change and 2FA transfer",
                "category": "Account",
                "channel": TicketChannel.email,
                "status": TicketStatus.closed,
                "priority": TicketPriority.medium,
                "ai_resolved": True,
                "sentiment": "positive",
                "ai_confidence": 0.96,
                "created_hours_ago": 50,
                "messages": [
                    (SenderType.customer, cust_user.id, "Hello, I am changing my company email address and need to transfer my 2FA authenticator app to a new phone."),
                    (SenderType.ai, None, "Hi there! I have sent a secure 2FA reset link to your verified recovery email address. Please follow the instructions to pair your new authenticator app."),
                    (SenderType.customer, cust_user.id, "Successfully paired my new phone. Thanks for the instant assistance!")
                ],
                "csat": (5, "The AI assistant resolved my 2FA reset in seconds! Incredible experience.")
            },

            # === LIVE CHAT TICKETS ===
            {
                "ref": "TCK-10201",
                "customer": cust_alex,
                "agent": agent_emma,
                "subject": "Two-Factor Authentication login code delay",
                "category": "Technical",
                "channel": TicketChannel.website_chat,
                "status": TicketStatus.resolved,
                "priority": TicketPriority.high,
                "ai_resolved": False,
                "sentiment": "positive",
                "ai_confidence": 0.93,
                "created_hours_ago": 24,
                "messages": [
                    (SenderType.customer, cust_alex.id, "Hi, my 2FA SMS code is taking several minutes to arrive when trying to log in from my laptop."),
                    (SenderType.agent, agent_emma.id, "Hello Alex! I checked the SMS gateway status and initiated a fallback code for your account. You can also switch to an Authenticator app (TOTP) for zero latency."),
                    (SenderType.customer, cust_alex.id, "Logged in now and switched to Google Authenticator. Appreciate the fast help!")
                ],
                "csat": (5, "Emma solved my login problem immediately on chat. 5 stars!")
            },
            {
                "ref": "TCK-10202",
                "customer": cust_david,
                "agent": agent_user,
                "subject": "Pro Plan Seat Upgrade and Add-on Billing",
                "category": "Billing",
                "channel": TicketChannel.website_chat,
                "status": TicketStatus.waiting,
                "priority": TicketPriority.medium,
                "ai_resolved": False,
                "sentiment": "neutral",
                "ai_confidence": 0.89,
                "created_hours_ago": 6,
                "messages": [
                    (SenderType.customer, cust_david.id, "Hi, we want to add 5 more support agent seats to our Pro subscription. What will be the prorated charge for the remaining 18 days?"),
                    (SenderType.agent, agent_user.id, "Hello David! Adding 5 seats for the remaining 18 days will be prorated at $42.50 total. Would you like me to apply the upgrade to your billing profile?")
                ]
            },
            {
                "ref": "TCK-10203",
                "customer": cust_user,
                "agent": None,
                "subject": "Chat widget color styling customization in Dark Mode",
                "category": "General",
                "channel": TicketChannel.website_chat,
                "status": TicketStatus.resolved,
                "priority": TicketPriority.low,
                "ai_resolved": True,
                "sentiment": "positive",
                "ai_confidence": 0.97,
                "created_hours_ago": 18,
                "messages": [
                    (SenderType.customer, cust_user.id, "Can we customize the chat widget accent color to match our brand's dark theme?"),
                    (SenderType.ai, None, "Hello! Yes, you can customize your live chat widget accent color and dark mode theme from Admin Settings > Channels > Live Chat > Appearance. You can set any custom HEX color code!"),
                    (SenderType.customer, cust_user.id, "Found the setting and configured our brand HEX color. Looks great!")
                ],
                "csat": (4, "Clear instructions from the automated assistant.")
            },
            {
                "ref": "TCK-10204",
                "customer": cust_rahul,
                "agent": None,
                "subject": "How to export CSV customer survey reports",
                "category": "General",
                "channel": TicketChannel.website_chat,
                "status": TicketStatus.new,
                "priority": TicketPriority.low,
                "ai_resolved": False,
                "sentiment": "neutral",
                "ai_confidence": 0.92,
                "created_hours_ago": 1,
                "messages": [
                    (SenderType.customer, cust_rahul.id, "Hi there, where can managers export the CSAT customer survey reports in CSV format?"),
                    (SenderType.ai, None, "Hello Rahul! You can export CSAT and agent performance reports in CSV format directly from the Manager Analytics dashboard by clicking the 'Export CSV' button in the top right corner.")
                ]
            },

            # === WHATSAPP TICKETS ===
            {
                "ref": "TCK-10301",
                "customer": cust_heet_wa,
                "agent": agent_emma,
                "subject": "Order #88213 Delivery Tracking & Expedited Shipping",
                "category": "Orders",
                "channel": TicketChannel.whatsapp,
                "status": TicketStatus.resolved,
                "priority": TicketPriority.high,
                "ai_resolved": False,
                "sentiment": "positive",
                "ai_confidence": 0.95,
                "created_hours_ago": 28,
                "messages": [
                    (SenderType.customer, cust_heet_wa.id, "Hello! Can you check the live tracking status for my shipment #88213? Need it delivered before Friday."),
                    (SenderType.agent, agent_emma.id, "Hello Heet! Your package #88213 is in transit with FedEx Express (Tracking: FDX-9920148). Estimated delivery is Thursday afternoon by 2:00 PM."),
                    (SenderType.customer, cust_heet_wa.id, "Awesome! Thanks for the quick update on WhatsApp 🙏")
                ],
                "csat": (5, "Prompt and clear update on WhatsApp! Loved the instant response.")
            },
            {
                "ref": "TCK-10302",
                "customer": cust_rahul,
                "agent": agent_user,
                "subject": "Request to update delivery address for shipment #88240",
                "category": "Orders",
                "channel": TicketChannel.whatsapp,
                "status": TicketStatus.resolved,
                "priority": TicketPriority.medium,
                "ai_resolved": False,
                "sentiment": "positive",
                "ai_confidence": 0.91,
                "created_hours_ago": 14,
                "messages": [
                    (SenderType.customer, cust_rahul.id, "Hi, I made a typo in my street number for order #88240. Can I update it to 42 Orchard Boulevard?"),
                    (SenderType.agent, agent_user.id, "Hi Rahul, I have updated the shipping destination for #88240 with the courier to 42 Orchard Boulevard. You will receive an SMS confirmation shortly."),
                    (SenderType.customer, cust_rahul.id, "Thank you so much for fixing it before it was dispatched!")
                ],
                "csat": (5, "Saved my package from being delivered to the wrong address. Thank you!")
            },
            {
                "ref": "TCK-10303",
                "customer": cust_david,
                "agent": None,
                "subject": "WhatsApp notification preferences & automated alerts",
                "category": "General",
                "channel": TicketChannel.whatsapp,
                "status": TicketStatus.closed,
                "priority": TicketPriority.low,
                "ai_resolved": True,
                "sentiment": "positive",
                "ai_confidence": 0.98,
                "created_hours_ago": 40,
                "messages": [
                    (SenderType.customer, cust_david.id, "Can I receive real-time ticket resolution alerts directly on WhatsApp?"),
                    (SenderType.ai, None, "Hello David! Yes, automated WhatsApp notifications are active for your account. You will receive instant updates whenever an agent replies or resolves your ticket."),
                    (SenderType.customer, cust_david.id, "Perfect, thank you!")
                ],
                "csat": (4, "Very convenient WhatsApp integration.")
            },
            {
                "ref": "TCK-10304",
                "customer": cust_heet_wa,
                "agent": agent_emma,
                "subject": "Payment confirmation and invoice receipt for Pro Plan",
                "category": "Billing",
                "channel": TicketChannel.whatsapp,
                "status": TicketStatus.open,
                "priority": TicketPriority.medium,
                "ai_resolved": False,
                "sentiment": "neutral",
                "ai_confidence": 0.90,
                "created_hours_ago": 4,
                "messages": [
                    (SenderType.customer, cust_heet_wa.id, "Hey team, I just renewed our Pro Plan via WhatsApp link. Could you send the PDF receipt?"),
                    (SenderType.agent, agent_emma.id, "Hi Heet! We received your payment confirmation for the Pro Plan renewal. I am preparing your PDF tax receipt right now.")
                ]
            },

            # === INSTAGRAM TICKETS ===
            {
                "ref": "TCK-10401",
                "customer": cust_akash_ig,
                "agent": agent_emma,
                "subject": "Instagram DM Inquiry: Influencer Partner Program",
                "category": "Sales",
                "channel": TicketChannel.instagram,
                "status": TicketStatus.resolved,
                "priority": TicketPriority.medium,
                "ai_resolved": False,
                "sentiment": "positive",
                "ai_confidence": 0.93,
                "created_hours_ago": 22,
                "messages": [
                    (SenderType.customer, cust_akash_ig.id, "Hey! Loved your product demo on reels. How do I apply for your creator partnership and affiliate program?"),
                    (SenderType.agent, agent_emma.id, "Hi Akash! We would love to collaborate. You can apply directly through our Creator Portal at https://supporthub.com/creators with your media kit. Feel free to DM us if you have any questions!"),
                    (SenderType.customer, cust_akash_ig.id, "Submitted our application! Thanks Emma ✨")
                ],
                "csat": (5, "Super friendly response on Instagram DM!")
            },
            {
                "ref": "TCK-10402",
                "customer": cust_heet_ig,
                "agent": agent_user,
                "subject": "Product Return and Exchange Policy inquiry",
                "category": "Orders",
                "channel": TicketChannel.instagram,
                "status": TicketStatus.waiting,
                "priority": TicketPriority.medium,
                "ai_resolved": False,
                "sentiment": "neutral",
                "ai_confidence": 0.89,
                "created_hours_ago": 10,
                "messages": [
                    (SenderType.customer, cust_heet_ig.id, "Hi, I received my order yesterday but need to exchange for a different size. What is the return window?"),
                    (SenderType.agent, agent_user.id, "Hello Heet! We offer 30-day hassle-free returns and exchanges. Please share your order number and desired size, and I will generate a prepaid return shipping label for you.")
                ]
            },
            {
                "ref": "TCK-10403",
                "customer": cust_mihir_ig,
                "agent": None,
                "subject": "Instagram DM: Promo Code Verification",
                "category": "Billing",
                "channel": TicketChannel.instagram,
                "status": TicketStatus.resolved,
                "priority": TicketPriority.low,
                "ai_resolved": True,
                "sentiment": "positive",
                "ai_confidence": 0.96,
                "created_hours_ago": 30,
                "messages": [
                    (SenderType.customer, cust_mihir_ig.id, "Is the 'SUMMER25' promo code active for the annual starter plan?"),
                    (SenderType.ai, None, "Hello Mihir! Yes, promo code 'SUMMER25' is valid through the end of this month and gives 25% off all annual plans at checkout."),
                    (SenderType.customer, cust_mihir_ig.id, "Worked like a charm, just subscribed!")
                ],
                "csat": (5, "Instant help on Instagram.")
            },
            {
                "ref": "TCK-10404",
                "customer": cust_zaru_ig,
                "agent": agent_emma,
                "subject": "Urgent refund status inquiry for returned item #9021",
                "category": "Billing",
                "channel": TicketChannel.instagram,
                "status": TicketStatus.escalated,
                "priority": TicketPriority.urgent,
                "ai_resolved": False,
                "sentiment": "neutral",
                "ai_confidence": 0.87,
                "created_hours_ago": 12,
                "messages": [
                    (SenderType.customer, cust_zaru_ig.id, "Hello, I dropped off my return parcel 8 business days ago but haven't received my refund confirmation. Can someone check?"),
                    (SenderType.agent, agent_emma.id, "Hi Zaru! I have escalated your return tracking to our warehouse logistics team to inspect and release the refund immediately.")
                ]
            },

            # === FACEBOOK MESSENGER TICKETS ===
            {
                "ref": "TCK-10501",
                "customer": cust_heet_fb,
                "agent": agent_emma,
                "subject": "Facebook Messenger inquiry on automated chatbot rules",
                "category": "Technical",
                "channel": TicketChannel.facebook,
                "status": TicketStatus.resolved,
                "priority": TicketPriority.medium,
                "ai_resolved": False,
                "sentiment": "positive",
                "ai_confidence": 0.94,
                "created_hours_ago": 16,
                "messages": [
                    (SenderType.customer, cust_heet_fb.id, "Hi, does SupportHub support AI automated replies on Facebook Page Messenger directly?"),
                    (SenderType.agent, agent_emma.id, "Hello Heet! Yes! SupportHub seamlessly integrates with Facebook Messenger to provide instant AI auto-replies, smart debouncing, and agent escalation right from your unified inbox."),
                    (SenderType.customer, cust_heet_fb.id, "Tested it out and works smoothly. Thank you!")
                ],
                "csat": (5, "Great omnichannel experience across Facebook Messenger.")
            },
            {
                "ref": "TCK-10502",
                "customer": cust_alex,
                "agent": agent_user,
                "subject": "Plan downgrade inquiry before next monthly renewal",
                "category": "Billing",
                "channel": TicketChannel.facebook,
                "status": TicketStatus.open,
                "priority": TicketPriority.medium,
                "ai_resolved": False,
                "sentiment": "neutral",
                "ai_confidence": 0.88,
                "created_hours_ago": 5,
                "messages": [
                    (SenderType.customer, cust_alex.id, "Hi SupportHub, I would like to adjust our subscription tier before the next renewal on the 28th. What happens to our historical ticket data?"),
                    (SenderType.agent, agent_user.id, "Hello Alex! If you downgrade tiers, all your historical ticket records, customer profiles, and analytics reports remain 100% intact and searchable.")
                ]
            },
            {
                "ref": "TCK-10503",
                "customer": cust_michael,
                "agent": None,
                "subject": "Customer feedback on new live chat interface",
                "category": "General",
                "channel": TicketChannel.facebook,
                "status": TicketStatus.closed,
                "priority": TicketPriority.low,
                "ai_resolved": True,
                "sentiment": "positive",
                "ai_confidence": 0.97,
                "created_hours_ago": 48,
                "messages": [
                    (SenderType.customer, cust_michael.id, "Just wanted to say the new live chat design and fast response time is fantastic! Keep up the great work."),
                    (SenderType.ai, None, "Hi Michael! Thank you so much for your kind words and feedback. We are committed to making your support experience as smooth and enjoyable as possible!"),
                ],
                "csat": (5, "Excellent interface and responsiveness.")
            }
        ]

        # Insert tickets, messages, and CSATs
        for t_seed in ticket_seeds:
            created_dt = now - timedelta(hours=t_seed["created_hours_ago"])
            t = Ticket(
                ref=t_seed["ref"],
                customer_id=t_seed["customer"].id,
                agent_id=t_seed["agent"].id if t_seed["agent"] else None,
                subject=t_seed["subject"],
                category=t_seed["category"],
                channel=t_seed["channel"],
                status=t_seed["status"],
                priority=t_seed["priority"],
                ai_resolved=t_seed["ai_resolved"],
                sentiment=t_seed["sentiment"],
                ai_confidence=t_seed["ai_confidence"],
                created_at=created_dt,
                updated_at=created_dt + timedelta(minutes=random.randint(15, 60))
            )
            session.add(t)
            await session.flush()
            await session.refresh(t)

            # Insert messages
            msg_dt = created_dt
            for sender_type, sender_id, body in t_seed["messages"]:
                m = Message(
                    ticket_id=t.id,
                    sender_id=sender_id,
                    sender_type=sender_type,
                    body=body,
                    created_at=msg_dt
                )
                session.add(m)
                msg_dt += timedelta(minutes=random.randint(2, 10))

            # Insert CSAT if available
            if "csat" in t_seed:
                rating_val, comment_str = t_seed["csat"]
                csat = CsatRating(
                    ticket_id=t.id,
                    customer_id=t_seed["customer"].id,
                    rating=rating_val,
                    comment=comment_str,
                    created_at=msg_dt + timedelta(minutes=5)
                )
                session.add(csat)

        await session.commit()
        print(f"✅ Created {len(ticket_seeds)} pristine tickets across Email, Live Chat, WhatsApp, Instagram, Facebook.")

        # 8. Ensure ChannelIntegrations have beautiful display names
        channels = (await session.exec(select(ChannelIntegration))).all()
        channel_configs = {
            ChannelType.email: {"name": "support@supporthub.com", "status": ChannelStatus.connected, "vol": 18},
            ChannelType.website_chat: {"name": "chat.supporthub.com", "status": ChannelStatus.connected, "vol": 24},
            ChannelType.whatsapp: {"name": "+1 (555) 019-2834", "status": ChannelStatus.connected, "vol": 15},
            ChannelType.instagram: {"name": "@heets.brainerhub", "status": ChannelStatus.connected, "vol": 12},
            ChannelType.facebook: {"name": "SupportHub Official", "status": ChannelStatus.connected, "vol": 9},
        }

        existing_types = {c.channel_type: c for c in channels}
        for ch_type, conf in channel_configs.items():
            if ch_type in existing_types:
                ch = existing_types[ch_type]
                ch.display_name = conf["name"]
                ch.status = conf["status"]
                ch.weekly_volume = conf["vol"]
                ch.updated_at = now
                session.add(ch)
            else:
                new_ch = ChannelIntegration(
                    channel_type=ch_type,
                    display_name=conf["name"],
                    status=conf["status"],
                    weekly_volume=conf["vol"],
                    created_at=now,
                    updated_at=now
                )
                session.add(new_ch)

        await session.commit()
        print("✅ Channel integrations configured with clean display names.")

        print("\n✨ Database successfully cleaned and populated with pristine, professional production data! ✨")

if __name__ == "__main__":
    asyncio.run(run_clean_and_seed())

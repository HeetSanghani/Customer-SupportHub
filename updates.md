🔴 High Priority (Core Functionality)
Agent Dashboard — Real Inbox The agent side currently shows a blank/white space. The inbox should show all active tickets assigned to that agent, with the ability to view/reply in real-time (just like the customer chat).

Agent Manual Reply Agents should be able to type and send their own messages into a ticket chat — not just the AI. This is critical for escalated tickets where the AI hands off to a human.

Dashboard Analytics — Live Data The "Total Tickets", "AI Resolved", "Open", "Escalated" cards are currently static/placeholder. Connect them to real DB aggregation queries.

🟡 Medium Priority (Polish & UX)
CSAT (Customer Satisfaction) Rating After a ticket is marked resolved, show the customer a 1-5 star rating prompt — "How satisfied were you with our support?" This data is already in your DB schema (csat_ratings table).

Ticket History / Audit Log Show a timeline of what happened in a ticket: created → escalated → resolved, with timestamps. Useful for both agents and managers.

Customer Profile Page The "Customer Profile" link in the sidebar exists but likely has no content. Add name, email, ticket history, and a way to edit display name.

Notification Badge Show a badge on the "Live Chat" sidebar item when there's an AI response waiting (unread message count).

🟢 Lower Priority (Nice to Have)
Knowledge Base (KB) Admin UI Agents/admins can currently add KB articles via API only. Build a simple UI to create, edit, and publish KB articles that the AI uses for RAG responses.

Manager/Admin Dashboard A separate view with charts: tickets over time, AI resolution rate, average response time, CSAT scores.

Email Notifications When a ticket is escalated or a new message arrives, send the customer/agent an email (Postmark is already configured in .env).
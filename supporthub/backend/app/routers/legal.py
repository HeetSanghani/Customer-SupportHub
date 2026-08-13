"""
app/routers/legal.py

Public Meta Compliance Router for Customer-SupportHub.
Provides unauthenticated GET endpoints for Privacy Policy, Terms of Service, and Data Deletion Instructions.
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.config import get_settings

router = APIRouter(tags=["legal"])


def _get_contact_email() -> str:
    settings = get_settings()
    return (
        getattr(settings, "support_contact_email", "")
        or getattr(settings, "postmark_from_email", "")
        or "support@yourdomain.com"
    )

COMMON_CSS = """
<style>
    :root {
        --primary: #6366f1;
        --primary-hover: #4f46e5;
        --bg: #0f172a;
        --card-bg: #1e293b;
        --text: #f8fafc;
        --text-muted: #94a3b8;
        --border: #334155;
    }
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: var(--bg);
        color: var(--text);
        line-height: 1.6;
        padding: 2rem 1rem;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 2.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    header {
        border-bottom: 1px solid var(--border);
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
    }
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }
    h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .last-updated {
        font-size: 0.875rem;
        color: var(--text-muted);
    }
    nav {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    nav a {
        color: var(--primary);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
    }
    nav a:hover {
        text-decoration: underline;
    }
    section {
        margin-bottom: 1.8rem;
    }
    h2 {
        font-size: 1.25rem;
        color: var(--primary);
        margin-bottom: 0.75rem;
    }
    p, li {
        color: var(--text-muted);
        font-size: 0.975rem;
        margin-bottom: 0.75rem;
    }
    ul {
        padding-left: 1.5rem;
    }
    .contact-box {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid var(--primary);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1.5rem;
    }
    .contact-box p {
        color: var(--text);
        margin: 0;
    }
    footer {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border);
        text-align: center;
        font-size: 0.85rem;
        color: var(--text-muted);
    }
</style>
"""


@router.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy():
    contact_email = _get_contact_email()
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Customer-Support</title>
    {COMMON_CSS}
</head>
<body>
    <div class="container">
        <header>
            <div class="app-title">Customer-Support</div>
            <h1>Privacy Policy</h1>
            <div class="last-updated">Last Updated: August 10, 2026</div>
            <nav>
                <a href="/privacy-policy">Privacy Policy</a>
                <a href="/terms-of-service">Terms of Service</a>
                <a href="/data-deletion">Data Deletion</a>
            </nav>
        </header>

        <section>
            <h2>1. Introduction</h2>
            <p>Welcome to Customer-Support. This Privacy Policy outlines how we collect, use, and handle customer communication data during the operation and testing of our customer support platform.</p>
        </section>

        <section>
            <h2>2. Information We Collect</h2>
            <p>To provide customer support tools, our platform processes customer inquiry data, including:</p>
            <ul>
                <li><strong>Instagram / Meta Messaging Data:</strong> User IDs (IGSID), display names, and direct message contents sent to connected Instagram Business Accounts.</li>
                <li><strong>WhatsApp Integration Data:</strong> Phone numbers, customer profile names, and incoming support message contents.</li>
                <li><strong>Email & Support Communication Data:</strong> Sender email addresses, subject lines, and message body text.</li>
                <li><strong>Support Ticket Metadata:</strong> Ticket creation timestamps, resolution statuses, and category assignments.</li>
            </ul>
        </section>

        <section>
            <h2>3. How We Use Information</h2>
            <p>We process collected information strictly for:</p>
            <ul>
                <li>Routing and organizing incoming customer support messages into support tickets.</li>
                <li>Displaying tickets to customer support agents and facilitating support communication.</li>
                <li>Testing and evaluating channel integration workflows during development.</li>
            </ul>
        </section>

        <section>
            <h2>4. Third-Party Services & Integrations</h2>
            <p>Customer-Support integrates with third-party service providers to send and receive messages, including Meta (Instagram Direct and WhatsApp Business API) and email communication providers. Data passed to third parties is limited to what is necessary for message routing and delivery.</p>
        </section>

        <section>
            <h2>5. Data Storage & Security</h2>
            <p>Customer data is stored securely in encrypted databases. We implement standard technical and organizational security measures to protect data against unauthorized access, loss, or disclosure.</p>
        </section>

        <section>
            <h2>6. Data Retention & User Rights</h2>
            <p>We retain support interaction data only as long as necessary to process support inquiries or maintain support records. Users have the right to request deletion or modification of their support records at any time.</p>
        </section>

        <div class="contact-box">
            <p><strong>Contact Us:</strong> If you have questions regarding this Privacy Policy or wish to exercise data rights, please contact us at: <code>{contact_email}</code></p>
        </div>

        <footer>
            &copy; 2026 Customer-Support Platform. All rights reserved.
        </footer>
    </div>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/terms-of-service", response_class=HTMLResponse)
async def terms_of_service():
    contact_email = _get_contact_email()
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service - Customer-Support</title>
    {COMMON_CSS}
</head>
<body>
    <div class="container">
        <header>
            <div class="app-title">Customer-Support</div>
            <h1>Terms of Service</h1>
            <div class="last-updated">Last Updated: August 10, 2026</div>
            <nav>
                <a href="/privacy-policy">Privacy Policy</a>
                <a href="/terms-of-service">Terms of Service</a>
                <a href="/data-deletion">Data Deletion</a>
            </nav>
        </header>

        <section>
            <h2>1. Acceptance of Terms</h2>
            <p>By interacting with or utilizing Customer-Support integrations (including Instagram Messaging and WhatsApp channels), you agree to these Terms of Service.</p>
        </section>

        <section>
            <h2>2. Description of Service</h2>
            <p>Customer-Support provides a multi-channel support platform designed to consolidate customer inquiries from Instagram, WhatsApp, and Email into an agent-facing management system.</p>
        </section>

        <section>
            <h2>3. Acceptable Use</h2>
            <p>Users and messaging callers agree not to submit malicious content, spam, automated abuse, or illegal material through connected support channels.</p>
        </section>

        <section>
            <h2>4. Third-Party Integrations</h2>
            <p>Our platform interfaces with Meta platforms (Instagram API with Instagram Login, Meta Webhooks) and email providers. Use of these integrations is subject to Meta's Terms of Service and API Policies.</p>
        </section>

        <section>
            <h2>5. Service Availability & Limitation of Liability</h2>
            <p>Customer-Support is provided on an "AS IS" and "AS AVAILABLE" basis for evaluation and operational support. We do not guarantee uninterrupted uptime during development or testing phases.</p>
        </section>

        <div class="contact-box">
            <p><strong>Questions or Support:</strong> For inquiries regarding these Terms of Service, please reach out to: <code>{contact_email}</code></p>
        </div>

        <footer>
            &copy; 2026 Customer-Support Platform. All rights reserved.
        </footer>
    </div>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/data-deletion", response_class=HTMLResponse)
async def data_deletion():
    contact_email = _get_contact_email()
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Data Deletion Instructions - Customer-Support</title>
    {COMMON_CSS}
</head>
<body>
    <div class="container">
        <header>
            <div class="app-title">Customer-Support</div>
            <h1>User Data Deletion Instructions</h1>
            <div class="last-updated">Last Updated: August 10, 2026</div>
            <nav>
                <a href="/privacy-policy">Privacy Policy</a>
                <a href="/terms-of-service">Terms of Service</a>
                <a href="/data-deletion">Data Deletion</a>
            </nav>
        </header>

        <section>
            <h2>User Data Deletion Policy</h2>
            <p>Customer-Support respects your privacy and rights regarding personal data. If you have interacted with our platform through Instagram Direct, WhatsApp, or Email, you may request full deletion of your customer record and message history.</p>
        </section>

        <section>
            <h2>How to Request Data Deletion</h2>
            <p>To request the deletion of your personal data and support ticket history, please follow these steps:</p>
            <ul>
                <li>Send an email to <code>{contact_email}</code> with the subject line <strong>"Data Deletion Request"</strong>.</li>
                <li>Include your Instagram Username, Instagram Scoped ID (IGSID), WhatsApp Phone Number, or Email Address used when contacting support.</li>
                <li>Our support team will verify your identity and process the deletion of your record within 30 days.</li>
            </ul>
        </section>

        <section>
            <h2>Meta / Instagram Application Data Deletion</h2>
            <p>If you wish to remove Customer-Support access from your Instagram or Facebook account:</p>
            <ul>
                <li>Go to your Instagram account Settings & Privacy.</li>
                <li>Navigate to <strong>Website Permissions</strong> &gt; <strong>Apps and Websites</strong>.</li>
                <li>Locate <strong>Customer-Support</strong> and click <strong>Remove</strong>.</li>
            </ul>
        </section>

        <section>
            <h2>What Information Will Be Removed</h2>
            <p>Upon verification and processing of a deletion request, we will remove:</p>
            <ul>
                <li>Your customer user profile record and synthetic identifiers.</li>
                <li>All associated message body content and stored attachments.</li>
                <li>Associated support ticket conversation histories.</li>
            </ul>
        </section>

        <div class="contact-box">
            <p><strong>Submit Deletion Request:</strong> Email us directly at: <code>{contact_email}</code></p>
        </div>

        <footer>
            &copy; 2026 Customer-Support Platform. All rights reserved.
        </footer>
    </div>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)

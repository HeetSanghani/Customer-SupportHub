# Developer Learning Guide — Customer-SupportHub Architecture

Welcome to the **Customer-SupportHub** system guide! This guide explains how the entire application works in simple, clear terms using real code references.

---

## 1. What Happens When a Customer Registers?
- **Endpoint**: `POST /auth/register` in `app/routers/auth.py`
- **Validation**: Passwords must be at least 8 characters long.
- **Security**: The password is hashed using `bcrypt` (`hash_password(password)`).
- **Identity Linkage**: The system looks up the registering email address in the MySQL `customers` table (`supporthub_business`). If a matching customer is found, its `customer_id` (e.g., `CUST-001`) is bound to the new PostgreSQL `User` record. Clients cannot pass or spoof `customer_id`.

## 2. What Happens When a Customer Logs In?
- **Endpoint**: `POST /auth/login` in `app/routers/auth.py`
- **Verification**: `verify_password(plain_password, user.password_hash)` checks the credentials.
- **Token Generation**: Generates an `HS256` JWT access token (`create_access_token(user.id, user.role)`).
- **Identity Retrieval**: When the client presents this token in headers or query parameters, `get_current_user` decodes the token and loads the authenticated `User` object, including their bound `customer_id`.

## 3. Why Are Both PostgreSQL and MySQL Used?
- **PostgreSQL**: Stores application-level operational data: user credentials, JWT sessions, chat tickets, messages, quick replies, and vector embeddings for dynamic knowledge base articles (`KbArticle`).
- **MySQL 8.0 (`supporthub_business`)**: Acts as the single source of truth for all e-commerce business data: company info, categories, sellers, products, customers, orders, order items, payments, shipments, returns, and refunds.

## 4. Why Is RAG Separate from MySQL?
- **MySQL**: Holds structured relational database records (orders, prices, tracking numbers, stock levels).
- **RAG (`app/rag/`)**: Handles unstructured policy documents (`knowledge_base/policies/policies.json` like Return Policy, Warranty Policy) and general Knowledge Base articles (`knowledge_base/articles/knowledge_articles.json`).

## 5. How Does the AI Decide MySQL vs RAG vs Hybrid?
The central pipeline is managed by `AIOrchestrator` (`app/ai/orchestrator.py`):
1. **Context Resolution**: `context_manager` resolves or creates a `ConversationContext`.
2. **Intent Classification & Routing**: `AIRouter` (`app/ai/router.py`) classifies the query intent:
   - `STRUCTURED`: Needs relational database data from MySQL (e.g., "Where is my order?").
   - `RAG`: Needs policy document retrieval (e.g., "What is your return policy?").
   - `HYBRID`: Needs both MySQL data and RAG policy rules (e.g., "Can I cancel ORD-025 according to your policy?").
   - `HUMAN`: Needs human agent handoff.
   - `SECURITY`: Violates security rules.

## 6. How Does Security & Ownership Validation Work?
- **Ownership Verification**: Before returning business data, `AIOrchestrator._check_ownership()` checks if the fetched order, payment, shipment, return, or refund record belongs to `ctx.customer_id`.
- **Cross-Customer Defense**: If `caller_customer_id != resource_owner_id`, access is immediately denied (`SECURITY_DENIAL` / `Access Denied`), and any context slots created during that turn are reverted to prevent context poisoning.

## 7. How Does a Guest Differ from an Authenticated User?
- **Guest Users (`customer_id = None` or `GUEST`)**: Can access public company policies, general FAQs, and public product specs. Any attempt to access private transactional data (orders, shipments, payments) is denied with a prompt requesting them to log in first (`GUEST_PRIVATE_DENIED`).
- **Authenticated Users**: Can access their own personal orders, shipments, payments, returns, and refunds seamlessly.

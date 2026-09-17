--
-- PostgreSQL database dump
--

-- \restrict WVVQKilai0qfhEiBNhYUJXz8ruseAERGowBh7R2NPlxSxYL3r5UPrQLvB7AIJK0

-- Dumped from database version 16.14 (Debian 16.14-1.pgdg12+1)
-- Dumped by pg_dump version 17.10 (Ubuntu 17.10-0ubuntu0.25.10.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.tickets DROP CONSTRAINT IF EXISTS tickets_customer_id_fkey;
ALTER TABLE IF EXISTS ONLY public.tickets DROP CONSTRAINT IF EXISTS tickets_agent_id_fkey;
ALTER TABLE IF EXISTS ONLY public.ticket_embeddings DROP CONSTRAINT IF EXISTS ticket_embeddings_ticket_id_fkey;
ALTER TABLE IF EXISTS ONLY public.shipments DROP CONSTRAINT IF EXISTS shipments_order_fk;
ALTER TABLE IF EXISTS ONLY public.sellers DROP CONSTRAINT IF EXISTS sellers_company_fk;
ALTER TABLE IF EXISTS ONLY public.returns DROP CONSTRAINT IF EXISTS returns_order_fk;
ALTER TABLE IF EXISTS ONLY public.returns DROP CONSTRAINT IF EXISTS returns_item_fk;
ALTER TABLE IF EXISTS ONLY public.returns DROP CONSTRAINT IF EXISTS returns_customer_fk;
ALTER TABLE IF EXISTS ONLY public.refunds DROP CONSTRAINT IF EXISTS refunds_return_fk;
ALTER TABLE IF EXISTS ONLY public.refunds DROP CONSTRAINT IF EXISTS refunds_order_fk;
ALTER TABLE IF EXISTS ONLY public.refunds DROP CONSTRAINT IF EXISTS refunds_customer_fk;
ALTER TABLE IF EXISTS ONLY public.products DROP CONSTRAINT IF EXISTS products_seller_fk;
ALTER TABLE IF EXISTS ONLY public.products DROP CONSTRAINT IF EXISTS products_company_fk;
ALTER TABLE IF EXISTS ONLY public.products DROP CONSTRAINT IF EXISTS products_category_fk;
ALTER TABLE IF EXISTS ONLY public.payments DROP CONSTRAINT IF EXISTS payments_order_fk;
ALTER TABLE IF EXISTS ONLY public.payments DROP CONSTRAINT IF EXISTS payments_customer_fk;
ALTER TABLE IF EXISTS ONLY public.orders DROP CONSTRAINT IF EXISTS orders_customer_fk;
ALTER TABLE IF EXISTS ONLY public.orders DROP CONSTRAINT IF EXISTS orders_company_fk;
ALTER TABLE IF EXISTS ONLY public.order_items DROP CONSTRAINT IF EXISTS order_items_product_fk;
ALTER TABLE IF EXISTS ONLY public.order_items DROP CONSTRAINT IF EXISTS order_items_order_fk;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_ticket_id_fkey;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_sender_id_fkey;
ALTER TABLE IF EXISTS ONLY public.macros DROP CONSTRAINT IF EXISTS macros_created_by_fkey;
ALTER TABLE IF EXISTS ONLY public.kb_articles DROP CONSTRAINT IF EXISTS kb_articles_created_by_fkey;
ALTER TABLE IF EXISTS ONLY public.email_logs DROP CONSTRAINT IF EXISTS email_logs_ticket_id_fkey;
ALTER TABLE IF EXISTS ONLY public.csat_ratings DROP CONSTRAINT IF EXISTS csat_ratings_ticket_id_fkey;
ALTER TABLE IF EXISTS ONLY public.csat_ratings DROP CONSTRAINT IF EXISTS csat_ratings_customer_id_fkey;
ALTER TABLE IF EXISTS ONLY public.categories DROP CONSTRAINT IF EXISTS categories_parent_fk;
ALTER TABLE IF EXISTS ONLY public.categories DROP CONSTRAINT IF EXISTS categories_company_fk;
ALTER TABLE IF EXISTS ONLY public.automations DROP CONSTRAINT IF EXISTS automations_created_by_fkey;
ALTER TABLE IF EXISTS ONLY public.audit_log DROP CONSTRAINT IF EXISTS audit_log_ticket_id_fkey;
ALTER TABLE IF EXISTS ONLY public.audit_log DROP CONSTRAINT IF EXISTS audit_log_actor_id_fkey;
DROP INDEX IF EXISTS public.ix_webhook_events_received_at;
DROP INDEX IF EXISTS public.ix_webhook_events_processed;
DROP INDEX IF EXISTS public.ix_webhook_events_event_id;
DROP INDEX IF EXISTS public.ix_webhook_events_channel;
DROP INDEX IF EXISTS public.ix_users_phone;
DROP INDEX IF EXISTS public.ix_users_email;
DROP INDEX IF EXISTS public.ix_users_customer_id;
DROP INDEX IF EXISTS public.ix_users_company_id;
DROP INDEX IF EXISTS public.ix_users_channel_customer_id;
DROP INDEX IF EXISTS public.ix_users_channel;
DROP INDEX IF EXISTS public.ix_tickets_status;
DROP INDEX IF EXISTS public.ix_tickets_sla_due_at;
DROP INDEX IF EXISTS public.ix_tickets_ref;
DROP INDEX IF EXISTS public.ix_tickets_priority;
DROP INDEX IF EXISTS public.ix_tickets_customer_id;
DROP INDEX IF EXISTS public.ix_tickets_created_at;
DROP INDEX IF EXISTS public.ix_tickets_channel;
DROP INDEX IF EXISTS public.ix_tickets_category;
DROP INDEX IF EXISTS public.ix_tickets_agent_id;
DROP INDEX IF EXISTS public.ix_ticket_embeddings_vector;
DROP INDEX IF EXISTS public.ix_ticket_embeddings_ticket_id;
DROP INDEX IF EXISTS public.ix_quick_replies_tenant_id;
DROP INDEX IF EXISTS public.ix_quick_replies_category;
DROP INDEX IF EXISTS public.ix_messages_ticket_id;
DROP INDEX IF EXISTS public.ix_messages_external_message_id;
DROP INDEX IF EXISTS public.ix_messages_created_at;
DROP INDEX IF EXISTS public.ix_kb_chunk_embeddings_vector;
DROP INDEX IF EXISTS public.ix_kb_chunk_embeddings_source_type;
DROP INDEX IF EXISTS public.ix_kb_chunk_embeddings_source_id;
DROP INDEX IF EXISTS public.ix_kb_chunk_embeddings_chunk_id;
DROP INDEX IF EXISTS public.ix_kb_chunk_embeddings_category;
DROP INDEX IF EXISTS public.ix_kb_articles_title;
DROP INDEX IF EXISTS public.ix_kb_articles_category;
DROP INDEX IF EXISTS public.ix_email_templates_name;
DROP INDEX IF EXISTS public.ix_email_logs_ticket_id;
DROP INDEX IF EXISTS public.ix_email_logs_status;
DROP INDEX IF EXISTS public.ix_email_logs_recipient_email;
DROP INDEX IF EXISTS public.ix_email_logs_created_at;
DROP INDEX IF EXISTS public.ix_csat_ratings_ticket_id;
DROP INDEX IF EXISTS public.ix_csat_ratings_customer_id;
DROP INDEX IF EXISTS public.ix_audit_log_ticket_id;
DROP INDEX IF EXISTS public.ix_audit_log_entity_type;
DROP INDEX IF EXISTS public.ix_audit_log_entity_id;
DROP INDEX IF EXISTS public.ix_audit_log_created_at;
DROP INDEX IF EXISTS public.ix_audit_log_actor_id;
DROP INDEX IF EXISTS public.ix_audit_log_action;
ALTER TABLE IF EXISTS ONLY public.webhook_events DROP CONSTRAINT IF EXISTS webhook_events_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.tickets DROP CONSTRAINT IF EXISTS tickets_pkey;
ALTER TABLE IF EXISTS ONLY public.ticket_embeddings DROP CONSTRAINT IF EXISTS ticket_embeddings_ticket_id_key;
ALTER TABLE IF EXISTS ONLY public.ticket_embeddings DROP CONSTRAINT IF EXISTS ticket_embeddings_pkey;
ALTER TABLE IF EXISTS ONLY public.shipments DROP CONSTRAINT IF EXISTS shipments_pkey;
ALTER TABLE IF EXISTS ONLY public.sellers DROP CONSTRAINT IF EXISTS sellers_pkey;
ALTER TABLE IF EXISTS ONLY public.returns DROP CONSTRAINT IF EXISTS returns_pkey;
ALTER TABLE IF EXISTS ONLY public.refunds DROP CONSTRAINT IF EXISTS refunds_pkey;
ALTER TABLE IF EXISTS ONLY public.quick_replies DROP CONSTRAINT IF EXISTS quick_replies_pkey;
ALTER TABLE IF EXISTS ONLY public.products DROP CONSTRAINT IF EXISTS products_pkey;
ALTER TABLE IF EXISTS ONLY public.payments DROP CONSTRAINT IF EXISTS payments_pkey;
ALTER TABLE IF EXISTS ONLY public.orders DROP CONSTRAINT IF EXISTS orders_pkey;
ALTER TABLE IF EXISTS ONLY public.order_items DROP CONSTRAINT IF EXISTS order_items_pkey;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_pkey;
ALTER TABLE IF EXISTS ONLY public.macros DROP CONSTRAINT IF EXISTS macros_pkey;
ALTER TABLE IF EXISTS ONLY public.kb_chunk_embeddings DROP CONSTRAINT IF EXISTS kb_chunk_embeddings_pkey;
ALTER TABLE IF EXISTS ONLY public.kb_articles DROP CONSTRAINT IF EXISTS kb_articles_pkey;
ALTER TABLE IF EXISTS ONLY public.email_templates DROP CONSTRAINT IF EXISTS email_templates_pkey;
ALTER TABLE IF EXISTS ONLY public.email_logs DROP CONSTRAINT IF EXISTS email_logs_pkey;
ALTER TABLE IF EXISTS ONLY public.csat_ratings DROP CONSTRAINT IF EXISTS csat_ratings_pkey;
ALTER TABLE IF EXISTS ONLY public.company DROP CONSTRAINT IF EXISTS company_pkey;
ALTER TABLE IF EXISTS ONLY public.channel_integrations DROP CONSTRAINT IF EXISTS channel_integrations_pkey;
ALTER TABLE IF EXISTS ONLY public.channel_integrations DROP CONSTRAINT IF EXISTS channel_integrations_channel_type_key;
ALTER TABLE IF EXISTS ONLY public.categories DROP CONSTRAINT IF EXISTS categories_pkey;
ALTER TABLE IF EXISTS ONLY public.automations DROP CONSTRAINT IF EXISTS automations_pkey;
ALTER TABLE IF EXISTS ONLY public.audit_log DROP CONSTRAINT IF EXISTS audit_log_pkey;
ALTER TABLE IF EXISTS ONLY public.alembic_version DROP CONSTRAINT IF EXISTS alembic_version_pkc;
ALTER TABLE IF EXISTS ONLY public.ai_settings DROP CONSTRAINT IF EXISTS ai_settings_pkey;
DROP TABLE IF EXISTS public.webhook_events;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.tickets;
DROP TABLE IF EXISTS public.ticket_embeddings;
DROP TABLE IF EXISTS public.shipments;
DROP TABLE IF EXISTS public.sellers;
DROP TABLE IF EXISTS public.returns;
DROP TABLE IF EXISTS public.refunds;
DROP TABLE IF EXISTS public.quick_replies;
DROP TABLE IF EXISTS public.products;
DROP TABLE IF EXISTS public.payments;
DROP TABLE IF EXISTS public.orders;
DROP TABLE IF EXISTS public.order_items;
DROP TABLE IF EXISTS public.messages;
DROP TABLE IF EXISTS public.macros;
DROP TABLE IF EXISTS public.kb_chunk_embeddings;
DROP TABLE IF EXISTS public.kb_articles;
DROP TABLE IF EXISTS public.email_templates;
DROP TABLE IF EXISTS public.email_logs;
DROP TABLE IF EXISTS public.csat_ratings;
DROP TABLE IF EXISTS public.company;
DROP TABLE IF EXISTS public.channel_integrations;
DROP TABLE IF EXISTS public.categories;
DROP TABLE IF EXISTS public.automations;
DROP TABLE IF EXISTS public.audit_log;
DROP TABLE IF EXISTS public.alembic_version;
DROP TABLE IF EXISTS public.ai_settings;
DROP TYPE IF EXISTS public.userstatus;
DROP TYPE IF EXISTS public.userrole;
DROP TYPE IF EXISTS public.ticketstatus;
DROP TYPE IF EXISTS public.ticketpriority;
DROP TYPE IF EXISTS public.ticketchannel;
DROP TYPE IF EXISTS public.sendertype;
DROP TYPE IF EXISTS public.channeltype;
DROP TYPE IF EXISTS public.channelstatus;
-- DROP EXTENSION IF EXISTS vector;
--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS '';


--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


--
-- Name: channelstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.channelstatus AS ENUM (
    'connected',
    'needs_attention',
    'disconnected'
);


--
-- Name: channeltype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.channeltype AS ENUM (
    'email',
    'website_chat',
    'whatsapp',
    'instagram',
    'facebook'
);


--
-- Name: sendertype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.sendertype AS ENUM (
    'customer',
    'agent',
    'ai',
    'system'
);


--
-- Name: ticketchannel; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.ticketchannel AS ENUM (
    'email',
    'website_chat',
    'whatsapp',
    'instagram',
    'facebook'
);


--
-- Name: ticketpriority; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.ticketpriority AS ENUM (
    'urgent',
    'high',
    'medium',
    'low'
);


--
-- Name: ticketstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.ticketstatus AS ENUM (
    'new',
    'open',
    'waiting',
    'escalated',
    'resolved',
    'closed'
);


--
-- Name: userrole; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.userrole AS ENUM (
    'customer',
    'agent',
    'manager',
    'admin'
);


--
-- Name: userstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.userstatus AS ENUM (
    'active',
    'invited',
    'suspended'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ai_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_settings (
    id integer NOT NULL,
    enabled boolean NOT NULL,
    auto_resolve boolean NOT NULL,
    suggest_replies boolean NOT NULL,
    auto_summary boolean NOT NULL,
    sentiment_detection boolean NOT NULL,
    confidence_threshold double precision NOT NULL,
    model_name character varying(100) NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: audit_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_log (
    id uuid NOT NULL,
    actor_id uuid,
    action character varying(100) NOT NULL,
    entity_type character varying(100) NOT NULL,
    entity_id character varying(100),
    ticket_id uuid,
    diff_json text,
    ip_address character varying(45),
    created_at timestamp without time zone NOT NULL
);


--
-- Name: automations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.automations (
    id uuid NOT NULL,
    name character varying(200) NOT NULL,
    trigger_json text,
    action_json text,
    is_active boolean NOT NULL,
    priority integer NOT NULL,
    created_by uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categories (
    category_id character varying(50) NOT NULL,
    company_id character varying(50) NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    parent_category_id character varying(50)
);


--
-- Name: channel_integrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.channel_integrations (
    id uuid NOT NULL,
    channel_type public.channeltype NOT NULL,
    status public.channelstatus NOT NULL,
    credentials_encrypted text,
    display_name character varying(200),
    weekly_volume integer NOT NULL,
    last_checked_at timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    config_json text
);


--
-- Name: company; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.company (
    company_id character varying(50) NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    website character varying(255),
    support_email character varying(255),
    support_phone character varying(50),
    default_currency character varying(10) DEFAULT 'USD'::character varying,
    country character varying(100),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: csat_ratings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.csat_ratings (
    id uuid NOT NULL,
    ticket_id uuid NOT NULL,
    customer_id uuid NOT NULL,
    rating integer NOT NULL,
    comment text,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: email_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_logs (
    id uuid NOT NULL,
    ticket_id uuid,
    recipient_email character varying(255) NOT NULL,
    subject character varying(500) NOT NULL,
    status character varying(50) NOT NULL,
    error_detail text,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: email_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_templates (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    subject_pattern character varying(300) NOT NULL,
    body_html text,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: kb_articles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kb_articles (
    id uuid NOT NULL,
    title character varying(300) NOT NULL,
    category character varying(100) NOT NULL,
    body text,
    views integer NOT NULL,
    helpful_count integer NOT NULL,
    published boolean NOT NULL,
    created_by uuid,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    embedding public.vector(768)
);


--
-- Name: kb_chunk_embeddings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kb_chunk_embeddings (
    id uuid NOT NULL,
    chunk_id character varying(255) NOT NULL,
    source_id character varying(255) NOT NULL,
    source_type character varying(100) NOT NULL,
    title character varying(300) NOT NULL,
    category character varying(100) NOT NULL,
    content text,
    embedding public.vector(768),
    created_at timestamp without time zone NOT NULL
);


--
-- Name: macros; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.macros (
    id uuid NOT NULL,
    title character varying(200) NOT NULL,
    body text,
    category character varying(100),
    created_by uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messages (
    id uuid NOT NULL,
    ticket_id uuid NOT NULL,
    sender_id uuid,
    sender_type public.sendertype NOT NULL,
    body text,
    attachments text,
    created_at timestamp without time zone NOT NULL,
    external_message_id character varying(255),
    body_html text
);


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_items (
    order_item_id character varying(50) NOT NULL,
    order_id character varying(50) NOT NULL,
    product_id character varying(50) NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(10,2) NOT NULL,
    total_price numeric(10,2) NOT NULL
);


--
-- Name: orders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.orders (
    order_id character varying(50) NOT NULL,
    company_id character varying(50) NOT NULL,
    customer_id uuid NOT NULL,
    status character varying(50) NOT NULL,
    order_date timestamp without time zone DEFAULT now(),
    total_amount numeric(10,2) NOT NULL,
    shipping_address text,
    cancellation_reason text,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


--
-- Name: payments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.payments (
    payment_id character varying(50) NOT NULL,
    order_id character varying(50) NOT NULL,
    customer_id uuid NOT NULL,
    amount numeric(10,2) NOT NULL,
    method character varying(50) NOT NULL,
    status character varying(50) NOT NULL,
    transaction_reference character varying(100),
    payment_date timestamp without time zone DEFAULT now(),
    failure_reason text
);


--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    product_id character varying(50) NOT NULL,
    company_id character varying(50) NOT NULL,
    seller_id character varying(50) NOT NULL,
    category_id character varying(50) NOT NULL,
    name character varying(255) NOT NULL,
    brand character varying(100),
    description text,
    price numeric(10,2) NOT NULL,
    mrp numeric(10,2),
    stock_quantity integer DEFAULT 0,
    specifications jsonb,
    created_at timestamp without time zone DEFAULT now()
);


--
-- Name: quick_replies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.quick_replies (
    id uuid NOT NULL,
    tenant_id character varying(100) NOT NULL,
    category character varying(100) NOT NULL,
    keyword_pattern character varying(500) NOT NULL,
    response_text text,
    priority integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: refunds; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.refunds (
    refund_id character varying(50) NOT NULL,
    return_id character varying(50) NOT NULL,
    order_id character varying(50) NOT NULL,
    customer_id uuid NOT NULL,
    refund_amount numeric(10,2) NOT NULL,
    status character varying(50) NOT NULL,
    initiated_at timestamp without time zone DEFAULT now(),
    expected_date date,
    completed_at timestamp without time zone
);


--
-- Name: returns; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.returns (
    return_id character varying(50) NOT NULL,
    order_id character varying(50) NOT NULL,
    order_item_id character varying(50) NOT NULL,
    customer_id uuid NOT NULL,
    reason text NOT NULL,
    status character varying(50) NOT NULL,
    requested_at timestamp without time zone DEFAULT now(),
    pickup_date date,
    completed_at timestamp without time zone
);


--
-- Name: sellers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sellers (
    seller_id character varying(50) NOT NULL,
    company_id character varying(50) NOT NULL,
    seller_name character varying(255) NOT NULL,
    email character varying(255),
    phone character varying(50),
    city character varying(100),
    state character varying(100),
    rating numeric(3,2),
    joined_date date,
    status character varying(50)
);


--
-- Name: shipments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.shipments (
    shipment_id character varying(50) NOT NULL,
    order_id character varying(50) NOT NULL,
    tracking_number character varying(100),
    carrier character varying(100),
    status character varying(50) NOT NULL,
    estimated_delivery_date date,
    actual_delivery_date date,
    shipped_at timestamp without time zone,
    delivered_at timestamp without time zone
);


--
-- Name: ticket_embeddings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ticket_embeddings (
    id uuid NOT NULL,
    ticket_id uuid NOT NULL,
    embedding public.vector(768) NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: tickets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets (
    id uuid NOT NULL,
    ref character varying NOT NULL,
    customer_id uuid NOT NULL,
    agent_id uuid,
    subject character varying(500) NOT NULL,
    category character varying(100) NOT NULL,
    channel public.ticketchannel NOT NULL,
    status public.ticketstatus NOT NULL,
    priority public.ticketpriority NOT NULL,
    sla_due_at timestamp without time zone,
    sla_breached boolean NOT NULL,
    sentiment character varying(50),
    ai_confidence double precision,
    ai_resolved boolean NOT NULL,
    ai_summary text,
    deleted_at timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    name character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role public.userrole NOT NULL,
    status public.userstatus NOT NULL,
    avatar_url text,
    totp_secret character varying,
    totp_enabled boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    email_signature text,
    channel public.channeltype,
    channel_customer_id character varying(255) DEFAULT NULL::character varying,
    phone character varying(30) DEFAULT NULL::character varying,
    customer_id character varying,
    address text,
    city character varying(100),
    state character varying(100),
    postal_code character varying(30),
    country character varying(100),
    company_id character varying(100)
);


--
-- Name: webhook_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.webhook_events (
    id uuid NOT NULL,
    event_id character varying(500) NOT NULL,
    channel public.channeltype NOT NULL,
    processed boolean NOT NULL,
    error text,
    processing_ms integer,
    raw_payload text,
    received_at timestamp without time zone NOT NULL,
    processed_at timestamp without time zone
);


--
-- Data for Name: ai_settings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ai_settings (id, enabled, auto_resolve, suggest_replies, auto_summary, sentiment_detection, confidence_threshold, model_name, updated_at) FROM stdin;
1	t	t	t	t	t	0.85	claude-sonnet-4-5	2026-09-09 15:26:29.775381
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
20260827_ticket_embeddings
\.


--
-- Data for Name: audit_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.audit_log (id, actor_id, action, entity_type, entity_id, ticket_id, diff_json, ip_address, created_at) FROM stdin;
b1748152-fd0a-4077-8775-d3d8c63dfd0a	\N	automation.evaluated	ticket	b78e3d69-f0e0-4b36-866f-a1fe0c012eaa	b78e3d69-f0e0-4b36-866f-a1fe0c012eaa	{"actions": ["Set priority to 'high'", "Set category to 'Billing & Refunds'"], "event_type": "ticket_created"}	\N	2026-09-09 17:05:05.185459
d6a2deb7-5bc8-462c-bda0-a38b630ca1ec	\N	automation.evaluated	ticket	c025e796-7ad9-4de8-be7b-689002d7343d	c025e796-7ad9-4de8-be7b-689002d7343d	{"actions": ["Set priority to 'high'", "Set category to 'Billing & Refunds'"], "event_type": "ticket_created"}	\N	2026-09-09 17:46:54.925981
c4a14942-df35-4db4-991b-05ea7acefa92	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	7a7110b1-9451-4771-a297-b59378914907	7a7110b1-9451-4771-a297-b59378914907	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-10 10:40:17.590687
ad89f2c1-509c-4366-b347-86f18ccfad7d	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	5142c951-2b60-49b9-8c49-f63d872038f0	5142c951-2b60-49b9-8c49-f63d872038f0	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-10 12:23:31.469128
6cb36ae5-feaa-4c9c-950d-0d772f8ffea1	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-10 13:16:22.75242
9148229b-0100-439b-a4fe-fde15657cfa5	\N	automation.evaluated	ticket	71f00727-caa8-4658-9db7-0c4dbb7d2645	71f00727-caa8-4658-9db7-0c4dbb7d2645	{"actions": ["Set priority to 'high'", "Set category to 'Billing & Refunds'"], "event_type": "ticket_created"}	\N	2026-09-10 15:08:37.115652
69b8de57-4cdd-43e4-918a-5f09ca08461d	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	71f00727-caa8-4658-9db7-0c4dbb7d2645	71f00727-caa8-4658-9db7-0c4dbb7d2645	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-10 15:10:27.777459
5502d1bd-d6f2-4d4c-85bf-58d7f315e36b	\N	automation.evaluated	ticket	9f75302d-8a1a-44a8-8660-4969785ae442	9f75302d-8a1a-44a8-8660-4969785ae442	{"actions": ["Set priority to 'high'", "Set category to 'Billing & Refunds'"], "event_type": "ticket_created"}	\N	2026-09-10 15:24:41.037289
12242e71-37e2-4ade-b86c-b995bf569c66	\N	automation.evaluated	ticket	096a4ed9-b378-49a4-b78b-ea3c45ab64df	096a4ed9-b378-49a4-b78b-ea3c45ab64df	{"actions": ["Set priority to 'high'", "Set category to 'Billing & Refunds'"], "event_type": "ticket_created"}	\N	2026-09-10 18:11:00.407983
bbcbf155-5d2e-4f89-92d8-0d21e3434158	\N	automation.evaluated	ticket	641222a4-43a8-4138-acf9-f2bd23a72544	641222a4-43a8-4138-acf9-f2bd23a72544	{"actions": ["Set priority to 'high'", "Set category to 'Billing & Refunds'"], "event_type": "ticket_created"}	\N	2026-09-10 18:11:00.410422
ea1d2f92-62a9-4e3e-ac85-9f9915bacae8	\N	automation.evaluated	ticket	5713519c-e2f1-4348-b11a-83e01d622160	5713519c-e2f1-4348-b11a-83e01d622160	{"actions": ["Set priority to 'high'", "Set category to 'Billing & Refunds'"], "event_type": "ticket_created"}	\N	2026-09-10 18:11:00.678796
0ca2946d-612a-4b2b-922c-439c5114324a	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	5713519c-e2f1-4348-b11a-83e01d622160	5713519c-e2f1-4348-b11a-83e01d622160	{"old_status": "escalated", "new_status": "TicketStatus.waiting"}	\N	2026-09-10 18:15:37.890836
3456ffe5-85bd-492b-9388-03df0571d717	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	507f5a74-e09d-461c-b387-1372a84094f2	507f5a74-e09d-461c-b387-1372a84094f2	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-14 16:45:55.186502
8adf4d47-f4fc-452d-a977-4c47fd9dde2d	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	aab74641-2a47-4a99-bbcd-a1c7fa2dac72	aab74641-2a47-4a99-bbcd-a1c7fa2dac72	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-14 16:46:22.547287
855d46af-d90a-4d86-be3a-d3506508a4f7	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	641222a4-43a8-4138-acf9-f2bd23a72544	641222a4-43a8-4138-acf9-f2bd23a72544	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-14 16:46:44.079675
5d9767e3-f070-484b-bca6-b718576a4c17	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	096a4ed9-b378-49a4-b78b-ea3c45ab64df	096a4ed9-b378-49a4-b78b-ea3c45ab64df	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-14 16:46:54.251489
7fd53c83-4e25-4dca-b508-97ff2efe9fa6	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	9f75302d-8a1a-44a8-8660-4969785ae442	9f75302d-8a1a-44a8-8660-4969785ae442	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-14 16:47:09.408708
cd2ac4bb-a8d2-4909-80e8-d41acf7161d0	\N	automation.evaluated	ticket	ea6e1612-4f0e-4925-9ced-2aa4693087f2	ea6e1612-4f0e-4925-9ced-2aa4693087f2	{"actions": ["Set priority to 'high'", "Set category to 'Billing & Refunds'"], "event_type": "ticket_created"}	\N	2026-09-14 17:12:42.442626
5fa3a605-a0bc-4f60-a6f7-ee76197b21e7	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	ea6e1612-4f0e-4925-9ced-2aa4693087f2	ea6e1612-4f0e-4925-9ced-2aa4693087f2	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-14 17:13:39.200131
e83728cc-6ed5-4ae3-b890-cdae34442683	4a47565a-2ec1-404a-8f05-07490e1d9384	ticket.auto_resolved	ticket	5713519c-e2f1-4348-b11a-83e01d622160	5713519c-e2f1-4348-b11a-83e01d622160	{"status": "resolved", "ai_resolved": true, "trigger": "customer_intent"}	\N	2026-09-14 17:59:36.9882
04523764-d7d1-4459-84bb-09ec76ebb463	\N	automation.evaluated	ticket	73603b79-147f-428f-845e-dfabe07404e7	73603b79-147f-428f-845e-dfabe07404e7	{"actions": ["Set priority to 'high'", "Set category to 'Billing & Refunds'"], "event_type": "ticket_created"}	\N	2026-09-15 16:16:19.898975
\.


--
-- Data for Name: automations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.automations (id, name, trigger_json, action_json, is_active, priority, created_by, created_at, updated_at) FROM stdin;
400a768c-306d-4d93-acb8-fe9e8015f08b	Negative Customer Sentiment Alert	{"event_type": "any", "conditions": {"sentiments": ["negative", "frustrated", "angry"]}}	{"set_priority": "high", "set_status": "escalated"}	t	40	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-13 18:47:52.305313	2026-08-13 18:47:52.305313
41cb5a80-e71c-4088-bf1a-9850641c4650	After-Hours Automated Acknowledgment	{"event_type": "ticket_created", "conditions": {"channels": ["email", "instagram", "facebook", "web"]}}	{"send_canned_reply": "Thank you for reaching SupportHub! We have received your inquiry and our support team will respond promptly."}	t	50	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-13 18:47:52.305313	2026-08-13 18:47:52.305313
6d11086a-48ff-4045-af71-b02f5f7abc5d	Refund & Billing Auto-Categorization	{"event_type": "ticket_created", "conditions": {"keywords": ["refund", "billing", "invoice", "charge", "charged twice", "subscription cancel"]}}	{"set_category": "Billing & Refunds", "set_priority": "high"}	t	20	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-13 18:47:52.305313	2026-08-13 18:47:52.305313
90c57bf4-013b-4abb-8b60-fec986aaffd4	Urgent Outage & Emergency Escalation	{"event_type": "any", "conditions": {"keywords": ["outage", "server down", "crash", "emergency", "system unavailable", "data loss"]}}	{"set_priority": "urgent", "set_status": "escalated", "set_category": "Emergency Outage", "send_canned_reply": "We have detected an urgent system issue reported in your ticket. Our senior engineering response team has been immediately alerted."}	t	10	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-13 18:47:52.305313	2026-08-13 18:47:52.305313
c307ec20-7a1b-4444-bec2-8ddff9fd0e9e	VIP WhatsApp Support Routing	{"event_type": "ticket_created", "conditions": {"channels": ["whatsapp"]}}	{"set_priority": "high", "set_category": "Mobile Priority"}	t	30	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-13 18:47:52.305313	2026-08-13 18:47:52.305313
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categories (category_id, company_id, name, description, parent_category_id) FROM stdin;
CAT-001	COMP-001	Electronics	Consumer electronics, computers, mobile devices, and audio gear.	\N
CAT-002	COMP-001	Mobiles & Tablets	Smartphones, tablets, and mobile accessories.	CAT-001
CAT-003	COMP-001	Laptops & Computers	Laptops, desktop computers, monitors, and computing accessories.	CAT-001
CAT-004	COMP-001	Audio & Headphones	True wireless earbuds, over-ear headphones, and portable bluetooth speakers.	CAT-001
CAT-005	COMP-001	Home & Kitchen	Modern furniture, cookware, and everyday smart appliances for home.	\N
CAT-006	COMP-001	Kitchen & Dining	Cookware, mixer grinders, air fryers, and dining sets.	CAT-005
CAT-007	COMP-001	Home Furniture	Ergonomic chairs, study tables, sofas, and bedframes.	CAT-005
CAT-008	COMP-001	Home Appliances	Smart televisions, vacuum cleaners, and air purifiers.	CAT-005
CAT-009	COMP-001	Fashion & Lifestyle	Trendy apparel, premium footwear, and lifestyle accessories.	\N
CAT-010	COMP-001	Men's Clothing	Shirts, t-shirts, jeans, and formal wear for men.	CAT-009
CAT-011	COMP-001	Women's Clothing	Ethnic wear, dresses, tops, and casual apparel for women.	CAT-009
CAT-012	COMP-001	Footwear	Running sneakers, casual shoes, formal leather shoes, and sandals.	CAT-009
\.


--
-- Data for Name: channel_integrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.channel_integrations (id, channel_type, status, credentials_encrypted, display_name, weekly_volume, last_checked_at, created_at, updated_at, config_json) FROM stdin;
2a623c7b-7c27-41c1-9e8d-b7ab216c5416	facebook	connected	EAAPcPdkgrHwBSQIZBoyAJSkUnAdZBtkEL97O0kBZBFue7Fa6wXcCFrBkD5axsBgio2nw50i5sPZBESjxXdTxZCZBr24g8sqmkOVEvjdfVVHb5USH2pKZBSpMwBoTiGJMZB6wywOXhxpkl5kpwAGLBZBktadfF50A6ojULUNTtEsHC86nlpzwOcNxGZBdTtrs5YhKON7jfcv4uNZCQZDZD	SupportHub Official	9	\N	2026-08-13 15:12:46.983504	2026-09-09 11:19:19.242324	\N
7bc70a80-1e0c-4b95-9b62-751473ae6fd2	email	connected	\N	support@supporthub.com	18	\N	2026-08-05 06:10:41.009055	2026-09-09 11:19:19.242324	\N
afc1f74e-4dbb-49c9-a112-5cc09543499d	whatsapp	connected	EAAPcPdkgrHwBSaOghXeLIjJtxOGzOLpRed1owVPEiW9gHSmBo4wQifqpA6xGZCeaqG0FalZAGkvJk9oIKD1MFxPa1bIubyeTa90nQUG6x02fc79ZBocNYyVZCxW9s19cfH85smWC4KLwN1cZAMrA1OvWtCEyKaokX6ZCA5KkUegCH3bZCX9S3FcYaLlMrGrNDxIKb3UzmZC7chu879ix6Xi6ZBLdYNlaAV1xFdYwPdnSGvbj761S8HFw3RVaGswmf2PPv16MdSrJxFjbvu4ysIOLOtaLRL5cZD	+1 (555) 019-2834	15	\N	2026-08-07 12:31:06.277142	2026-09-09 11:19:19.242324	\N
be2320c0-165e-4d3d-ab90-276adef7846b	instagram	connected	\N	@heets.brainerhub	12	\N	2026-08-12 16:08:07.635908	2026-09-09 11:19:19.242324	\N
c423ee30-5941-467e-ac26-2a74ca61a952	website_chat	connected	\N	chat.supporthub.com	24	\N	2026-08-05 06:10:41.009055	2026-09-09 11:19:19.242324	\N
\.


--
-- Data for Name: company; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.company (company_id, name, description, website, support_email, support_phone, default_currency, country, created_at, updated_at) FROM stdin;
COMP-001	ShopKart	ShopKart is India's leading unified online marketplace for electronics, fashion, and home lifestyle products.	https://www.shopkart.in	support@shopkart.in	+91-1800-200-8888	INR	India	\N	2026-08-21 11:13:12
\.


--
-- Data for Name: csat_ratings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.csat_ratings (id, ticket_id, customer_id, rating, comment, created_at) FROM stdin;
\.


--
-- Data for Name: email_logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.email_logs (id, ticket_id, recipient_email, subject, status, error_detail, created_at) FROM stdin;
\.


--
-- Data for Name: email_templates; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.email_templates (id, name, subject_pattern, body_html, updated_at) FROM stdin;
4e93409a-1038-4e09-aa22-38af75817ef9	ticket_created	[SupportHub] Ticket Received: {{ticket_ref}}	<p>Hi {{customer_name}},</p><p>We received your inquiry regarding <strong>{{ticket_subject}}</strong>. Our support team is working on it.</p>	2026-08-05 14:15:37.556643
b07a2f37-60e3-4dc9-8b24-44f74acc52b5	ticket_resolved	[SupportHub] Resolution & Survey: {{ticket_ref}}	<p>Hi {{customer_name}},</p><p>Your inquiry <strong>{{ticket_ref}}</strong> has been resolved. Please rate your experience below:</p><p><a href='{{survey_link_5}}'>⭐⭐⭐⭐⭐ Excellent</a></p>	2026-08-05 14:15:37.556844
1ac41c1a-8289-4234-b26e-bfecf188efd7	agent_reply	Re: {{ticket_subject}} [{{ticket_ref}}]	<p>Hi {{customer_name}},</p><p>{{agent_message}}</p><p>Best regards,<br>{{agent_name}}<br>SupportHub Team</p>	2026-08-05 14:15:37.556994
\.


--
-- Data for Name: kb_articles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kb_articles (id, title, category, body, views, helpful_count, published, created_by, created_at, updated_at, embedding) FROM stdin;
15b631b3-69ba-4073-a620-f4a347b94d35	How do I reset my account password or enable 2FA?	Account	You can reset your password anytime from the Login page by clicking Forgot Password. To manage Two-Factor Authentication (TOTP), navigate to Customer Profile > Security Settings.	120	54	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-05 16:03:56.67175	2026-08-05 16:03:56.671829	[-0.0040910426,0.020646596,0.008921532,-0.078870334,0.008461029,0.011518771,0.022883529,0.00046681246,-0.0040533305,0.000922458,-0.009672076,-0.024861882,-0.0027466633,-0.00095794816,0.14524922,-0.031849414,0.009835452,-0.009348359,0.0010035958,-0.0044109346,-0.0006735158,0.00547068,-0.0049270988,-0.0047937254,0.0059518516,-0.016263718,7.46428e-05,-0.007897826,0.0040473696,0.009883151,-0.008908212,0.002754254,-0.007186898,0.0019915467,-0.016241776,0.031786777,0.004495145,0.0012529723,-0.0020820764,6.7053756e-05,-0.0078431,-0.011455362,0.0063853757,-0.009290644,-0.0041738246,-0.010398134,0.0023104048,-0.0062951716,-0.021037428,0.021046683,-0.010774445,0.002259506,-0.023419736,-0.23745197,0.003903388,-0.006727884,0.003310642,-0.004262312,0.0007144448,-0.024473187,-0.013555233,0.025827736,-0.02012204,-0.024749113,0.0062166,-0.0056282068,0.040259916,0.021239629,-0.008641006,0.01998625,0.0078691365,-0.00075356464,-0.018253922,-0.0151635595,0.0028743884,-0.002565457,-0.009380956,-0.007435174,0.010864427,-0.0035943696,-0.0042527504,0.014183372,-0.004646519,-0.0052298307,-0.00015162367,-0.024108034,0.0049298,0.013451781,0.013071639,0.0030223841,-0.016703572,-0.013105307,0.018115446,-0.00543844,0.015100396,-0.0060474672,-0.003305248,0.0025482727,-0.0074739,-0.011586009,-0.0164147,-0.005842042,0.0009468851,0.00027106487,-0.0016785813,-0.015993692,0.008291992,-0.007321581,-0.008882177,0.0073707295,0.022190899,0.011481334,-0.004126371,0.009164495,0.024625331,-0.18100566,0.0054381355,0.006069462,0.022889072,0.005655269,-0.042511173,-0.009464482,-0.025434438,-0.0024221013,-0.006271077,-0.014936245,0.030489076,-0.017812954,0.003180644,0.0034470914,-0.016604327,-0.011318833,0.004642452,-0.0051393174,-0.0020792836,0.021051286,-0.0031252555,0.020782026,0.011714291,-0.004863798,0.044405233,0.010573046,-0.0067192297,0.013763523,-0.010335312,0.00078204577,-0.013448578,0.017852133,0.0009130681,-0.01498304,0.010169215,-0.01560082,0.008977653,-0.021761991,0.022675619,-0.025933903,0.022581097,-0.026419258,-0.014988455,-0.000993133,0.021332622,-0.0014707001,-0.008531407,-0.005752785,0.011354187,-0.013125333,0.0140318815,-0.0029834616,0.015125744,-8.53046e-05,-0.02735348,-0.016960649,0.0077215685,0.00663329,-0.022305828,0.0009405056,0.012332444,0.0032173663,0.011779016,-0.030096706,0.0030341882,0.0162758,0.006786779,-0.016083648,-0.007839679,-0.016600413,-0.009507899,0.0047582733,-0.017240245,-0.021931447,0.0008903753,-0.014022948,0.004584624,-0.00069718255,0.010391425,0.009389591,5.6621928e-05,0.00055742037,-0.02678866,0.013459981,0.018566525,-0.038309935,0.007301722,0.0038523537,0.0029120853,-0.0025477496,0.008364631,-0.015965216,0.0026614605,0.021637958,0.008758567,-0.011018199,0.023331864,-0.019563172,-0.0058545317,-0.013074242,-0.004469597,-0.009447033,0.007834479,-0.0105060125,0.0137379,0.008604357,-0.01838574,-0.0057944926,0.0017202601,0.004246051,0.009352092,-0.022334242,0.010301859,0.02107426,0.006170228,0.015977638,0.0022809617,-0.014127573,-0.0017422774,0.0036281748,0.006847413,0.0051768706,-0.0060758274,0.012887315,0.014470925,-0.00922779,0.011198037,-0.005303428,0.0061374367,-0.019151477,0.011380709,-5.3566608e-05,0.0020549018,0.025171798,-0.006066919,0.00920854,0.0051169265,-0.004457822,-0.009544809,-0.0029508832,-0.035967395,-0.0074045537,-0.0102996295,-0.010733806,0.013127697,0.0032138133,-0.009942557,-0.02231445,-0.0103601515,-0.0002448185,0.009420804,0.024724714,-0.007022324,-0.016799062,0.014485411,0.0170484,-0.012963691,-0.006692772,-0.003949747,-0.01338903,-0.07206421,0.0037044904,0.012340002,-0.008749802,0.0013256139,-0.005577656,0.008009132,-0.023935763,-0.01077289,0.025299275,-0.012831265,0.0103987325,-0.023530789,-0.00459681,0.0024313512,0.013672247,0.0009294738,-0.0058481335,0.008018648,-0.031731512,-0.007170124,0.0039834934,-0.015808182,-0.022253847,0.008547822,-0.0030982164,0.009585706,0.03556677,-0.006087842,0.022782544,0.008631532,0.0142356865,-0.010882799,-0.003387754,-0.008515849,-0.016260372,-0.0071087624,-0.01911786,-0.0024119108,-0.0033172446,-0.00594463,-0.01623732,-0.0027251828,0.01930091,0.00018899348,-0.001019593,-0.002869329,-0.009343822,-0.022934148,-0.010894764,-0.016740108,0.0028498268,-0.01449944,-0.011552596,-0.015761325,-0.0060874773,-0.009799696,-0.0013782625,0.0042780084,0.0015978941,0.0105063375,0.013204058,0.0055811806,0.006666302,-0.00025355082,0.019859992,0.0009303996,0.015041783,0.0071594734,-0.01570269,0.03403275,0.0040460383,0.004858409,-0.016406583,-0.0012555617,-0.0048965937,0.012254394,-0.0027113957,-0.014948123,0.01992632,-0.018269653,-0.0068377885,0.0038176775,0.011112265,0.0041036545,0.0022140818,0.002185364,0.0044259666,0.009812616,0.0011944596,0.015802607,0.012469957,0.0072013284,-0.01589724,-0.018471805,0.0018898633,0.0074265897,0.016003141,-0.021115785,-0.005156463,-0.003428357,0.016359784,0.02914841,-0.012962202,-0.00080181495,0.019270277,-0.019865723,-0.009722841,0.005062631,0.0055157933,-0.003458534,0.002969324,-0.029129142,0.0052576982,-0.018333057,0.010159791,-0.019720534,-0.0016336745,-0.010380844,0.035748005,-0.010386463,0.01730187,-0.0037838286,0.026875904,0.0008605996,0.019833263,-0.0081262365,0.0005479344,0.011268608,-0.0019326844,-0.0036175794,-0.024129895,-0.0072185253,-0.0011364246,-0.01284625,-0.01822045,0.011980522,0.004252783,0.00570528,0.025143398,-0.019229408,0.0058200248,-0.0007418492,0.0005704315,-0.00617053,-0.009020819,-0.0055668424,0.0069829193,-0.0051413295,0.013992923,0.00077866967,0.005532203,0.007163375,0.012552771,-0.012356166,0.023549246,-0.021061739,-0.006689473,-0.007806023,-0.005598419,0.0130173275,-0.0071728663,-0.013150067,0.007073478,-0.009579428,0.015810328,-0.0056164265,-0.0043958095,-0.0072591235,0.013023512,0.03627289,-0.0058690934,0.0027039878,0.0072445837,0.029799514,-0.011582604,0.02042693,-0.0070170825,0.022836525,0.0054922695,0.001445711,0.016569812,0.017364405,0.012307162,0.011179433,0.00025703668,-0.0041417903,-0.009941875,0.007915046,0.0056116018,0.024239287,-0.029700667,0.026293788,0.027942771,-0.014641211,0.021897184,-0.009508428,0.0053558745,0.010937558,-0.035649315,0.002310927,0.0132616935,0.0043709404,0.010288409,0.02164992,0.0025556842,-0.015460319,-0.019409655,0.036850166,0.00368776,0.008421925,0.03627806,-0.0065398198,0.00463579,0.014387939,-0.021200009,0.021742027,0.001095882,-0.008297707,0.0030418446,0.019793445,0.009105297,-0.007801212,0.0063883173,0.014933756,0.01664507,-0.030083746,0.012595171,-0.0032039273,0.011972295,0.009188703,0.0011304169,0.019100003,-0.020685097,-0.013831635,0.0033642028,0.006691598,0.019040499,0.020911453,-0.009420536,-0.012657548,0.0030164095,-0.0032869296,-0.01585078,-0.022435788,0.006999716,-0.002043003,0.015557413,0.0023064755,-0.02710329,0.013561125,0.028332671,0.0072344467,0.0331837,0.020207511,0.027451042,-0.0035206466,-0.017928649,0.017499298,0.0126836095,0.006499074,-0.019159738,0.019140191,0.0016935754,-0.0060198926,-0.011526431,-0.013365891,0.017039066,0.0010360378,-0.06272131,0.01131368,-0.009841262,0.00058442284,0.0057191206,-0.004291202,-0.020961916,0.023252297,-0.0063993908,-0.017904509,0.0036511424,0.0009212711,-0.008203587,0.0051681045,-0.016931307,-0.024312211,0.015391587,0.008420453,-0.007314321,-0.014182064,0.0040940624,0.009075061,-0.013975928,-0.0003514744,-0.006470944,-0.0034307498,-0.004522353,0.012241094,0.014082504,-0.008947022,-0.027135188,0.012637159,0.013883606,0.0019585204,0.02154524,-0.0070044347,-0.00994911,-0.02518701,-0.008233974,0.006773905,-0.0046339557,-0.033868823,0.0147044975,0.017813055,-0.003097215,0.010657122,-0.0116573665,-0.0026772562,0.0068718414,0.006071553,-0.02772723,0.011558405,-0.0006324384,-0.026185988,0.010459384,-0.0047859554,-0.01060259,-0.007009828,-0.026013719,-0.012128388,0.0061083883,0.01064089,0.011337735,0.009034461,-0.02377266,0.018606262,0.009944785,0.030958103,0.015950657,-0.021246683,-0.0061012935,0.010045793,-0.026221577,-0.008530474,-0.008486601,0.0027796193,-0.00026321967,0.006999912,-0.0035875114,-0.005832598,0.025249999,-0.027111156,-0.07247187,-0.035926133,0.012728158,-0.020814858,-0.00023822961,-0.0063014217,-0.015543497,-0.03158392,-0.013887697,0.0081864465,0.0018672248,-0.010416183,0.0018650551,-0.0025892858,-0.00092295185,-0.0052586114,0.0016613342,0.010083103,0.0059832465,-0.009056913,0.024166273,0.010272508,-0.008821499,-0.011725206,-0.008634062,0.020953404,-0.0042019114,-0.0028167965,-0.0023526012,0.0012208498,-0.009795539,-0.17794414,0.0015114172,-0.01117444,-0.00023500202,0.0037388876,-0.0005100455,-0.0047466476,-0.0023606021,-0.017147193,-0.0044546938,-0.0056978883,-0.028486282,-0.03504851,-0.002189363,0.0024760372,0.14360698,-0.018115694,0.0011543477,0.008240173,-0.017557448,-0.020010678,0.007590716,0.03165247,0.008258011,-0.006285488,-0.004205369,0.015580055,-0.007912057,0.0013878472,0.01870554,0.018889146,0.007627779,0.0022100564,-0.014502638,0.025266165,-0.015805734,0.022006063,0.007938829,-0.017009914,0.0049982653,0.01150451,0.009557759,-0.0064759795,-0.024086744,0.004160793,0.015162581,-0.016422592,0.0076485826,-0.013023584,-0.009903694,-0.005458254,-0.0973456,0.008315759,-0.008331962,0.013157931,0.011152866,0.0018518044,0.001561593,-0.015489041,-0.0064668492,-0.008997482,-0.023194224,-0.0024754202,0.0040340307,0.023617223,0.009644433,0.022174671,0.008989634,-0.0026605756,0.009547064,0.0079293605,0.0037298608,-0.0009659704,-0.008003306,-0.020942206,-0.018399889,0.0062446515,-0.016565828,0.0014909806,-0.016179148,0.00091802044,0.00883332,-0.013261058,0.0065494548,-0.023591073,-0.034079675,0.023591598,0.011975746,0.00026579053,-0.0011512267,0.011261103,-0.020899158,0.0012862649,0.014596011,0.018831896,0.0063634575,-0.003840788,0.021019991,0.01054823,0.02607767,-0.009645091,0.015704533,0.03030734,-0.012597056,0.013704871,0.020151213,-0.0028001582,0.0055427006,-0.0069240965,0.0118299]
2e7bd3d4-dffd-4d13-9b6a-ecb2c43f0b83	How do I request an updated invoice or receipt?	Billing	To download or request your monthly invoice, go to Dashboard > Billing > Invoice History. You can click any invoice to generate a PDF download or send a copy directly to your account email address.	42	19	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-05 16:03:56.671053	2026-08-05 16:03:56.671168	[0.0014439521,0.016552202,0.013362696,-0.07512311,0.0008402328,-0.008470171,0.005116575,0.012125393,-0.037928816,-0.0031410283,-0.0034474526,-0.010363,-0.0124515155,-0.019460462,0.12257809,-0.013090155,0.009725184,0.017180368,-0.006575061,-0.005160853,0.0009883025,0.008525064,0.0049828463,0.013811092,0.01954137,0.02046334,0.028202929,0.013257306,0.009121958,0.023161303,0.00432254,0.012019283,-0.019308908,-0.0023224703,0.011555112,0.0371671,-0.0010552095,0.013141513,-0.024910355,0.0053385617,-0.015860565,0.014316743,-0.0049471473,-0.024352638,0.011191431,-0.0010760782,0.0010100958,-0.013039516,-0.020456487,0.018846689,0.0022718853,0.002194799,-0.027511176,-0.2338493,0.0015172957,-0.03630869,-0.0030117172,-0.0052219997,0.0130910855,-0.016949465,-0.008998658,0.018593328,-0.0030454397,-0.026024107,-0.0021704396,-0.0053054276,0.026349457,0.010668197,-0.00090807123,0.0024682418,-0.005161871,0.025377514,-0.020342438,0.0020345524,0.013615625,-0.026744787,0.0017746225,-0.008435994,0.009819412,-0.0066867317,-0.024853513,-0.012169771,0.008941561,-0.0045132576,0.009764707,-0.022953589,-0.01548882,0.00066611206,-0.022478966,0.020069836,-0.00970679,0.0049552373,0.0018318078,-0.010599826,0.014175785,-0.015209623,0.016369984,-0.0012890095,-0.015359305,-0.02309413,0.0034471569,-0.013768059,-0.025333704,0.02007292,-0.0023184137,-0.030941881,-0.016475152,-0.0085099805,-0.017919045,-0.0047653075,0.0033790723,0.005491306,-0.007407459,-0.011442717,0.0016859404,-0.19457708,0.0049649603,0.0029135854,0.017991701,-0.014298547,-0.026520051,0.004701547,-0.0192759,-0.010589301,0.0021842613,0.0036471286,-0.0070831417,-0.018736418,0.002059296,0.0055735237,-0.0051841885,-0.02895842,0.011282744,-0.017455807,-0.022313382,0.0051613613,-0.021412004,0.009062674,0.0077726,0.0038712968,0.0077133914,0.035559494,-0.002519984,-0.03633425,0.002255565,0.007278297,0.0022170362,0.023054635,-0.01702091,-0.0016917547,-0.0031352425,0.00012495359,0.038586307,0.0066915248,0.014740815,-0.0025563776,-0.0024345224,-0.0011712542,0.015238911,0.010964187,0.016415123,0.022728609,0.003010764,-0.0026786244,0.008039144,0.02758999,-0.01625946,0.0047048987,-0.006246986,0.018097661,-0.014405286,-0.0022989206,0.016274726,0.0010214372,-0.0073742284,-0.013516077,0.01192397,0.0069701327,0.012014465,-0.036015835,0.0061004437,-0.0035960106,0.0146997105,-0.027852999,-0.012202267,-0.020719066,-0.001827343,0.0057690893,-0.0006353169,-0.026940174,-0.014812657,-0.006391995,0.006698364,-0.018860422,-0.0011722975,-0.0075052227,0.0006512797,-0.0012552196,0.0099600265,0.011873992,0.030200487,-0.020928808,0.0035548478,-6.723303e-05,-0.0019134993,0.01685914,-0.0072310115,-0.005631869,0.02152206,0.022118079,-0.0031731608,0.012685491,0.011129384,0.0006820153,-0.0057568112,-0.0076970137,0.01351822,-0.013690473,-0.0015946307,-0.01754128,-0.0007986498,0.008336176,-0.008765734,-0.01129418,0.004896148,0.0074022375,0.011094291,-0.0054778773,0.007928434,0.018332712,0.0026867045,0.017907623,-0.0019764525,-0.017490726,-0.0014464125,0.009665811,-0.0016620324,0.0012676899,0.0065281056,0.009871795,-0.015083034,-0.009874792,-0.0050940844,0.006671113,0.0003581009,-0.017358828,0.007760253,-0.00370016,0.014187065,0.00757614,0.0068142493,0.014125057,-0.010026549,0.0023617342,-0.0068135005,0.0031953931,-0.014552126,-0.020967565,-0.02346679,-0.016187536,0.032399155,-0.0025185694,-0.01647499,0.0019778763,0.0006789171,0.008334406,0.019573556,0.021735415,-0.011661593,-0.014614267,0.014487339,0.00613964,-0.007940003,0.011109168,0.0070158555,0.005672487,-0.07930229,-0.00023287006,0.0100361835,-0.024089605,-0.019512594,0.02049258,-0.004806002,-0.013579341,-0.014740846,0.0012736694,-0.011717202,0.0139333345,0.002331204,-0.017222239,0.008960499,0.009875534,-0.0014392609,0.0078301225,0.0075518675,-0.02858283,0.010475101,0.012396968,-0.015254248,-0.0004083387,-0.0067229406,-0.003066764,0.006255341,0.02668372,0.0048392233,-0.007769002,0.015577545,0.032122713,0.0022610135,0.0018680652,-0.021097997,-0.008693022,-0.007092122,-0.018506432,0.015883485,0.0069940817,-0.022176016,-0.0029025779,-0.016181562,0.036258142,0.0031892098,0.005887279,-0.0019143928,0.020771937,-0.022235913,-0.005988254,0.0060810945,0.0009067008,0.0054342956,0.0015932851,-0.0097933365,-0.017014308,-0.0068359985,0.005949839,-0.0030731573,0.009002438,-0.01450892,0.018300148,-0.003296283,0.01571035,0.0028033268,0.012920626,-0.017939392,-0.0020111878,-0.007255343,0.0021908358,0.015605396,0.008221285,0.014208125,-0.015685935,-0.0059089195,0.007931532,0.006957698,-0.01421395,-0.014342008,0.028618146,-0.013578959,0.0041639,-0.0026389617,0.006529167,-0.00822275,0.010854623,-0.0036166655,-0.009924429,-0.008523562,0.0020303451,0.015676634,-0.010009651,0.027511388,-0.019092644,-0.015985487,-0.009686858,-0.013555225,0.02016842,-0.0071926797,-0.011465447,0.00030983923,0.011343828,-0.019968413,-0.0026427114,-0.0032358335,0.02224776,0.00963056,-0.02408775,-0.0021193733,-0.01417227,-0.00873618,-0.0004740344,-0.022645406,-0.00011088358,-0.0071905535,0.016420325,-0.022800934,0.007386279,0.00064236124,0.024975631,-0.0074890726,0.0048849066,0.02274596,0.0049160337,0.016628511,0.0108554335,-0.014094453,0.016248522,0.009258221,-0.01361243,-0.010851767,-0.019843226,-0.014073458,-0.010446737,-0.0194682,0.009245535,0.007176095,0.00036284627,0.04284635,0.015045076,-0.020473529,0.012895379,0.025804982,-0.012769626,-0.009301105,-0.009927251,-0.0061790887,0.016752714,-0.024361355,0.004526022,-0.0068832445,-0.003007396,0.01146921,0.011890547,-0.033734612,0.01956622,-0.017941978,-0.0021952586,0.006452948,-0.02488212,0.0010833403,-0.0069048936,-0.004257021,-0.0005311169,0.026367221,-0.009711887,0.013554077,-0.00851403,-0.0013742852,0.007847629,0.0057675694,0.0063472833,0.010048458,0.0049124276,3.522296e-05,-0.018486459,0.02459702,-0.013606017,0.012886411,0.012601271,0.0037233636,0.021441692,-0.0016560497,0.019674886,0.014791024,0.005455869,-0.020248253,-0.012543699,0.0019009174,-0.005325255,-0.0047556986,-0.029576184,-0.0036330794,0.02768172,-0.014166058,0.004586706,0.0042899977,-0.001531546,0.0044863564,-0.013405996,0.011486093,0.009926384,0.007456882,-0.0016893361,0.020905053,-0.008965085,-0.00548318,0.0113473935,0.019200834,0.0050540385,0.010027457,0.029332764,-0.001778377,-0.008291439,0.00059417315,0.005542793,-0.027885428,-0.009334961,-0.0021415579,0.027641293,-0.006707173,0.012703069,-0.009241868,0.013675735,0.023029827,-0.0023901216,-0.013186658,-0.004173621,-0.011075952,0.007953353,0.006507726,0.004272168,-0.009938614,0.014454578,-0.008434652,0.0074227015,-0.0022408662,-0.00075916573,0.026707435,-0.013210426,-0.008572337,0.004712187,-0.01341488,0.010692047,-0.017933024,-0.0072499276,-0.024220373,0.0013995148,0.00561494,-0.029275322,0.001968955,0.009763904,0.0049400204,0.025391333,-0.0073602987,0.0030594186,-0.010844883,-0.018856512,0.012807375,-0.012674458,0.024591003,-0.0084314225,-0.0057694726,-0.008709679,0.0091967955,0.008428098,0.0121877985,0.020631796,-0.000648426,-0.06556526,0.013154016,0.00948547,0.03317404,0.013576534,0.0052386527,0.0019594487,0.0012377526,0.0050762035,-0.015196884,-0.008547544,0.009343008,-0.0064083277,0.010531325,-0.01573262,-0.015789447,0.017376427,-0.0056437734,0.00379996,0.0034412916,0.0009276341,0.020902751,-0.008802303,0.005176595,0.004026687,0.011842042,-0.012982019,0.009509643,-0.0111513855,0.004515089,-0.011155811,-0.0026916345,0.018194735,0.0061954777,0.0061675906,-0.01637088,0.010002601,-0.0038282142,0.00932617,0.022627845,-0.011474782,-0.02556842,0.0070387246,-0.00021073913,-0.0026934491,0.011552352,0.01363056,-0.0008710762,0.0052807666,0.0015519893,-0.020243734,-0.00038447822,0.0030596538,-0.026613917,0.020766221,-0.017537244,-0.018875686,-0.0033881715,-0.025664872,0.0010010032,-0.009255725,-0.0017124289,0.013495746,0.01108137,-0.016135681,-0.009821705,-0.01202912,0.040606227,0.0007525301,-0.017002894,-0.006381005,-0.0036931008,-0.003047118,0.0037328305,0.0075323493,-0.01007176,-0.00567914,-0.025355851,-0.0055530565,0.004939837,-0.009410921,-0.00012824616,-0.054761935,-0.026554124,-0.017005272,-0.012267104,0.0018099734,-0.014240369,-0.016087115,0.0053918306,0.007222707,0.004960634,0.010781943,-0.0044889315,0.028221251,-0.018999951,-0.0037187622,0.017347638,-0.0011741051,-0.0024537316,-0.002441268,-0.0088302465,0.014397109,0.007858015,0.0025352533,-0.0064172978,-0.019222325,0.0048772087,-0.0058148215,0.0006489813,-0.010303377,-0.0050207656,0.00182145,-0.19245192,0.00034320762,-0.0015418835,0.010484756,-0.009189281,-0.0031102959,0.0048332294,0.007970712,-0.01587861,-0.021833582,0.019145101,-0.026798172,-0.041597646,0.010932876,-0.0021902702,0.15440217,-0.023608653,0.006991493,0.0029798972,0.011728522,-0.0026307402,-0.00331633,-0.0042276997,0.013515366,-0.020407662,-0.0031636,0.026822008,-0.007276634,0.017303417,0.011216626,-0.0025185002,0.008310121,0.00867628,-0.006549376,0.0053562885,-0.010575606,0.027254036,0.009177303,-0.0019151221,-0.0033819855,-0.0075588445,-0.0010703639,-0.024444751,-0.010287065,-0.0008033791,0.032997355,-0.021803593,0.0037171887,-0.0049779303,0.0004471219,-0.021794554,-0.08717193,-0.007652562,-0.010393226,0.00762758,-0.013088766,-0.0019396475,-0.01946276,0.0007653794,-0.003642547,0.014661599,0.014548156,0.0019444072,0.021524983,-0.008443468,-0.008150088,0.02211417,0.019454462,-0.004649478,0.019585656,0.0064386935,-0.006717459,-0.014530633,-0.018723905,-0.008483323,-0.0085017355,-0.01056645,-0.01701977,-0.002097638,-0.014716241,-0.0043349313,-0.005929028,0.00777523,0.015937207,-0.0074395235,-0.0041912324,0.011074395,0.00050540076,-0.017639447,-0.000431124,-0.0044638664,0.0151509475,-0.016114702,0.008766266,-0.0024976193,0.0029275636,0.01345762,0.027538916,0.0047915545,-0.0074805156,0.0025558786,0.016402658,0.01687774,-0.04283018,-0.0027593928,0.005761031,-0.02029917,0.004788097,0.005303446,0.016241316]
40ac66cf-a549-41e0-9f4c-ff5f0397bc71	How is Customer Satisfaction (CSAT) calculated?	General	When a support ticket or live chat is resolved, customers can rate their experience on a 1-to-5 star scale and leave feedback comments. The CSAT rating is calculated as the average of all verified customer reviews.	31	14	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-05 16:03:56.672248	2026-08-05 16:03:56.672333	[-0.010593449,0.0075856703,0.010794231,-0.08982716,-0.007473734,0.02421317,0.00907383,0.0016993799,-0.014154907,-0.0013658745,0.00663512,-0.0029941315,0.0043645124,-0.0024682335,0.11801746,0.009331586,0.0096254675,-0.0009043901,0.00041611557,-0.022034694,0.01152074,0.013325862,-0.0014125541,-0.0031116868,0.01013548,-0.0055122497,-0.0019100424,0.019170955,0.0033724098,0.002863505,0.0037979444,0.01599437,0.0067563667,0.004069915,-0.008019593,0.026307242,0.012836285,0.01507324,0.0035847984,0.027265113,-0.0040609282,-0.009528356,-0.00017016518,-0.014884787,0.0066844225,0.00038118832,-0.0056375363,-0.02256104,-0.007683154,0.00017712821,-0.010747035,-0.016487954,-0.0001696036,-0.23891363,-0.029302323,-0.032655057,0.007299544,0.003350576,-0.02166477,-0.011571609,-0.011972652,0.014971725,-0.020824213,-0.017259106,0.023846423,-0.012229637,0.039150305,0.024002764,0.021569772,0.017555518,0.007931299,0.003689535,-0.0105558755,-0.006223533,-0.011900153,0.0014915501,0.0005828541,-0.0053843185,-9.111302e-05,-0.0103622405,0.005969843,-0.013757726,-0.002503582,-0.0052219788,0.015943263,0.011372589,-0.0036252444,0.016147945,-0.010846121,0.01019243,0.0062599564,0.0042829635,-0.024465814,-0.0024651196,0.014964351,-0.0042680735,-0.0037540928,0.0029050924,-0.007741434,-0.014240233,-0.016194075,-0.012605739,-0.010932325,0.0030618699,-0.004045825,-0.006420838,0.018920379,-0.014397308,-0.022611346,0.00984351,0.016280994,-0.0018458138,-0.013550493,-0.0037191205,-0.0009055133,-0.20754911,0.0034540892,0.006464691,0.007942405,-0.0072770435,-0.03650087,0.014850746,0.004849412,0.006089264,-0.010903135,-0.011454926,0.023734465,-0.0077747973,0.024168499,0.018837178,-0.011412872,0.005182083,0.016288064,-0.017307326,-0.009354612,0.018447088,-0.024730591,0.0026299395,0.006556033,-0.0042037186,0.0056918194,-0.0010436572,-0.0020646695,-0.009716498,0.010845889,0.00621041,-0.0067382124,0.024022426,-0.013302193,-0.0058223754,-0.006018141,-0.010068109,0.013644378,0.012831245,0.026677053,-0.00904729,0.006034964,-0.013847628,0.0010508901,0.0055138776,0.030704211,0.021456318,-0.0073937005,0.007888156,-0.0033361653,-0.013878207,0.008025841,0.011725311,0.0005361863,0.026831968,-0.011185487,0.00978572,-0.00677876,-0.0032978351,0.004924351,-0.0036947555,0.03042033,0.016896697,-0.003113098,-0.024673797,0.01971507,-0.0015149963,-0.010074983,-0.020032331,-0.023645923,0.0029136653,0.012732971,-0.00019144351,-0.0052797464,-0.0021298504,-0.002935031,-0.012111001,0.012427504,-0.015711892,0.0069483914,-0.004941148,0.0017076734,0.017619502,0.026380515,0.0012686114,0.022587711,-0.0029030652,0.0053876108,0.007082561,-0.004066137,0.009327165,-0.0027353358,-0.011975849,0.016505752,0.030468682,-0.023247294,-0.0023748993,-0.004437631,0.013546557,0.013383515,0.0032995453,-0.017792279,-0.0155700715,0.01954191,-0.00437842,-0.004678033,0.023666712,0.0064681065,-0.004569055,0.0065802536,0.020436328,0.003589139,-0.01991126,-0.0048868777,0.011216966,-0.00084762357,0.008859219,-0.0033215866,0.0054017855,0.0031315158,-0.00061722734,0.006954876,0.0074443296,0.00501184,-0.002313672,-0.0032391138,-0.007959389,0.014611601,-0.015199713,0.015451936,-0.016817218,0.0071135177,-0.01250333,0.00628232,0.0010267862,-0.006901024,0.018435447,-0.0130424965,-0.010626976,-0.0057596737,0.008602508,-0.023733737,-0.02368739,0.0025258,-0.010492129,0.006503423,0.0008365885,-0.010030616,-0.012721435,-0.033982914,0.0045958827,-0.018394599,-0.014501178,0.00013573459,0.028887179,0.01424355,0.0154221775,-0.018914264,-0.014175499,0.018527528,-0.002223205,-0.080477044,0.0046433113,0.021581842,-0.017126305,0.0033697272,-0.0033219464,-0.008338628,-0.015609419,-0.012137806,0.032783356,-0.010790517,0.0075910133,-0.01854861,-0.024328904,0.0039690495,0.0051696086,-0.0036288502,-0.008986151,-0.016342966,-0.02318029,-0.009567833,0.0059028384,-0.016344013,-0.008426118,-0.0032061029,0.012665292,-0.024561988,0.019234648,-0.004267512,0.0018107063,-0.0029801105,0.0022132667,-0.009764705,-0.009224851,-0.006532707,-0.013720982,0.002493775,-0.01696919,0.0067391563,0.014069237,-0.029419487,-0.014523044,-0.0012371129,0.012401732,0.0046674986,-0.013366486,-0.005143552,0.006573867,-0.018875873,-0.018627068,0.00406502,0.0031803125,0.029485837,-0.010426781,-0.0027994413,-0.0059017176,0.0035684158,-0.0059499536,0.013210358,0.009355104,0.007457105,-0.014008184,0.0028637357,-0.002185601,0.0073126713,0.0021888677,-0.0056763566,-0.002870657,-0.011647958,0.008671305,-0.014145685,-0.0004747526,-0.0033655534,-0.036530774,0.0062198327,-0.013815276,-0.0017104518,0.00021974774,0.0027316292,0.015130137,0.013620406,0.011961974,-0.003519096,0.0061346847,-0.00082702853,0.016897421,0.0024451138,-0.012215389,-0.0069733863,-0.0013811102,0.021133548,-0.00013711509,0.0039963005,-0.004359685,-0.025997762,0.018333564,-0.0072102095,0.010626811,0.0045524486,-0.0074039362,-0.006725191,0.011215852,0.008086279,0.0087348465,-0.016225746,0.007242993,-0.017872408,0.00088945386,0.012854323,-0.014985911,-0.005208448,-0.018483898,-0.023557711,0.001165039,-0.024190832,0.024002615,0.012922588,0.0028283803,0.008538358,-0.0120854555,-0.021803819,0.00977255,0.00845029,0.011754906,-0.0067949775,-0.00576617,-0.010458857,0.014927195,0.0072152456,-0.0022732306,-0.006060024,-0.0081893755,0.007456436,0.024198469,-0.0010470656,-0.011037244,0.0013569477,0.005843146,0.001493763,0.0019578272,-0.0026883734,0.0063421377,0.005884972,-0.023125628,-0.022492075,0.0005599634,0.011410458,0.007956253,0.01554344,0.004785704,-0.023416875,-0.012365487,0.013385179,-0.00406645,0.011742017,0.010246072,-0.023427695,-0.010884423,-0.0068547716,-0.028840499,0.008911266,0.011363127,0.0085583255,-0.0008978073,0.005603091,-0.00694224,-0.012522363,0.011930528,-0.005374153,-0.0044625015,0.0003543255,-0.010390217,-0.0004986065,0.004871444,0.020532122,0.016639797,0.009235503,0.0074286014,-0.012217651,0.014954821,-0.0057327203,0.009091184,-0.0021306511,0.0021612018,-0.006149331,-0.015691243,0.0047092293,-0.015468409,0.01234516,0.0010454425,0.016287647,-0.009980385,-0.013867652,0.03835608,0.00090414385,0.009535882,-0.008121143,0.011423556,-0.010707567,-0.011407207,0.005225819,-0.005896841,-0.013955303,0.015681129,0.0034504486,-0.009741543,-0.008608617,0.014193179,0.010064499,-0.025593594,0.012499621,0.013995363,-0.00059311744,-0.0031667685,-0.0022626324,-0.0053759287,-0.013849651,0.021873841,0.0055237967,0.025627803,-0.003225661,-0.0016959162,-0.012477874,0.013252653,0.016452301,-0.017472927,-0.017939482,0.0037883485,-0.009506488,-0.0051522236,0.009013926,0.0023807604,-0.0011513571,0.008168973,0.00028952566,-0.007730957,0.0014523468,0.0167999,-0.002452769,-0.009742511,-0.013429278,-0.022674195,0.00078644947,-0.010930073,-0.020716742,-0.00869716,0.0071854084,0.004387797,-0.0016577246,0.0037554093,-0.0029886554,-0.0011769114,-0.0012596169,0.011852773,0.0031986951,0.03260482,0.0019492637,-0.012887408,0.010877946,0.0229536,0.007944589,-0.022669202,0.017710293,0.010593279,-0.0006485866,0.016770508,-0.012109506,-0.007223254,0.0119037265,-0.0528949,0.0011196389,-0.008437941,0.0010901256,-0.00023690438,-0.0072228247,-0.0016116535,0.003749609,0.010302785,-0.03149053,0.003024044,0.021655388,-0.009829076,0.03606875,-0.0020024928,-0.009336026,-0.003961926,0.016160848,-0.019458475,0.01738016,0.0062902356,0.018134696,0.013447415,0.009822531,0.009798586,0.005011719,-0.0028295044,-0.03212537,-0.023631783,-0.0041066036,0.0071704807,-0.009909084,-0.00990519,0.019808376,0.014026066,0.0040857913,0.020574326,-0.027604721,-0.0020383678,0.010514066,-0.018359879,-0.006344177,-0.025808256,-0.0016605619,0.013000455,-0.00072398654,0.006245341,-0.013842259,-0.004108059,-0.012321016,-0.02431881,-0.009531562,-0.005754759,-0.031730182,-0.0034454288,0.0071079605,0.004526683,0.012659767,-0.017875263,-0.004442765,-0.016811445,0.0013998675,-0.0061962046,0.005817101,0.0074899215,0.0007391004,0.011502375,0.02936364,0.023146804,-0.00659806,0.015324237,0.0024277647,-0.0074597215,0.002038653,-0.022261724,-0.009067688,0.0045811334,0.009982418,-0.0129527,0.0054877535,0.026914697,-0.008916694,-0.07601973,0.00016791627,0.009064747,-0.0042465567,0.019827235,-0.017203344,-0.0010854482,-0.01678251,0.005917804,0.0014670609,0.0041700243,-0.0021028384,0.01054564,-0.018041123,-0.0064372686,0.008041116,0.016082596,0.0010922197,0.0058439504,0.016535893,-0.020361098,0.007485529,0.022637505,-0.005706538,-0.024357593,0.0030474751,-0.0061844923,0.011142062,0.0108575355,0.021028053,0.01262746,-0.19096048,0.0051008225,-0.006376806,0.0055325525,-0.02734292,0.0068833847,0.007664297,0.016021172,-0.002118742,-0.0050241766,0.0015952372,-0.008572055,-0.032987196,0.009039882,-0.003872052,0.14975746,-0.020947965,0.0020587947,-0.018026382,-0.010505938,-0.0005464701,0.00037969634,0.0049117636,0.015290534,-0.01125812,-0.008445766,0.025226535,0.020965988,0.039441276,0.004892419,0.01922368,0.016476393,-0.006904297,0.0041480325,0.013386883,-0.0037531413,0.0059610195,-0.006596282,-0.0010525797,-0.0052201957,0.023047734,0.0037559732,-0.0069099064,-0.011513391,-0.008081926,0.016128603,-0.0036397032,-0.012502503,0.0041971933,-0.0007099634,-0.022127131,-0.10811689,-0.0047344016,0.024179442,0.014624069,0.022659006,0.003904017,-0.019862393,-0.0049095377,-0.0076793334,0.011505607,-0.0020421003,-0.0001881975,0.018056609,-0.011774005,-0.01354322,0.01429464,0.013719483,0.003910127,0.02510362,0.022076102,-0.0075538647,-0.0058806823,0.0005953678,-0.001191077,-0.013744502,0.00064526626,-0.0027189876,0.0005466094,0.0026820095,0.014694292,0.0003932166,0.00096042803,0.011856316,0.02431807,-0.009257231,0.021452274,0.009628568,-0.0085276505,-0.017479777,-0.0176917,-0.013704553,0.004880386,0.008298808,-0.0078994315,0.010292957,0.003819796,0.0085149035,0.026214572,0.0033170625,-0.010116083,0.0027895735,0.009043179,-0.0019524156,-0.0020955498,-0.0130387675,0.018596495,0.035615336,-0.010332049,0.0024095613]
493dfc50-b8fe-4c36-95a3-fb7fb2e4f874	What are our standard business hours?	General	Our global support team operates across multiple time zones to ensure you always get the help you need!\n\n- Level 1 Support (General Inquiries): Available 24/7, 365 days a year.\n- Level 2 Support (Technical & Billing): Available Monday through Friday, 9:00 AM to 6:00 PM (EST).\n- Dedicated Account Managers: Available during standard local business hours based on your region.\n\nOutside of standard business hours, our AI Agent will automatically answer common questions or route your ticket to the correct team for the next morning.\n	0	0	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-07-28 09:50:40.805378	2026-07-28 09:50:40.805711	[-0.014793894,0.0079884175,0.0070866854,-0.08227813,-0.009498018,0.0066510853,0.0065711164,0.0061772964,-0.013367504,-0.014529577,-0.006916436,-0.023236867,0.0008693723,0.0027586157,0.10631566,0.00037155658,0.032250922,-0.010916513,-0.03659643,-0.005288485,0.0042583016,0.002108373,0.0066355653,0.0070461305,0.0005302462,-0.0021213293,0.0038483068,-0.012560166,0.009558687,0.0051563643,-0.013542782,-0.009173642,0.012665337,-0.0057638814,-0.004597529,0.014309153,-0.0019353211,0.018915193,-0.0052113086,0.023132905,0.015447183,0.019304164,0.004239075,-0.0045126015,0.0004036154,-0.011799942,-0.0025465053,-0.052106455,-0.014518833,0.019840758,-0.029934833,-0.001131883,0.006474576,-0.22817045,-0.0058505107,-0.010558113,0.0024626781,0.0015800754,-0.016534284,-0.037965324,-0.0036252318,0.017180627,-0.009026469,-0.026299648,-0.00049041933,-0.0062993537,0.020081611,0.03153667,0.02802029,0.0083304625,-0.015754933,-0.0033166846,-0.00963519,-0.011785092,-0.01704048,0.008920569,0.0041281376,-0.010616737,-0.01344897,-0.015047112,-0.006757735,-0.0032014265,-0.00085553183,-0.011848016,0.021360066,-0.011451053,0.0069381217,0.0019874102,-0.021048907,-0.0036302705,-0.014553493,0.00021817035,0.009914367,-0.026659856,0.030386396,-0.010031993,-0.005650377,-0.0035913326,-0.008231612,-0.014145653,-0.014930469,-0.0039056535,0.006921384,-0.00036642863,-0.017374141,0.01326491,-0.0068834797,0.00057246594,-0.023733515,0.0037370848,0.0036168117,0.014503023,-0.01514533,-0.002241534,-0.00010390112,-0.20027988,0.031059247,-0.008709665,0.014606087,0.0004308625,-0.0367911,-0.011166358,-0.0189343,0.009855862,0.0036648517,-0.013174896,0.010667675,-0.009675878,0.0083914995,0.024713406,-0.010794209,-0.016739903,0.011645994,-0.01068698,0.0014346384,0.0062342645,-0.028982775,0.022909788,-0.0031929975,-3.5724656e-06,0.017586308,0.018184017,0.01249512,-0.011118304,-0.0039937766,-0.005709807,0.0015497954,0.022916347,-0.0013182446,-0.03659788,0.0026662236,-0.00043870666,0.019204134,-0.011413933,0.020407831,-0.01782481,0.013616464,0.0011130089,0.007643396,0.0026782772,0.002911365,0.001189582,-0.0029021688,0.0060652327,0.015685786,-0.009889422,-0.019089555,0.017719295,-0.015507572,0.022852499,0.0041010235,-0.0042278953,-0.0007718461,0.007862168,-0.010762486,0.015098931,0.0004385657,-0.0033755759,0.016891338,-0.025579257,-0.014176663,0.028953712,-0.032664232,-0.030088551,-0.010203745,0.012717538,0.0035875388,0.0126265865,-0.026360793,-0.026873158,0.010718327,-0.016280835,-0.008208856,-0.011814008,0.011998802,-0.005478062,-0.017177572,0.010545853,0.019069063,0.012987745,0.010439405,-0.013873302,-0.008007217,-0.012562274,0.0029916891,-0.0029002286,0.0053843125,-0.029147701,-0.010795286,0.021641333,0.006409853,-0.005461663,0.014501224,-0.007798384,0.0027332893,-0.023362651,-0.008214677,-0.0048779175,0.013441579,-0.025250895,-0.0005540579,-0.0032842206,-0.008044162,-0.0055208458,0.01380543,0.008747891,0.0029301695,-0.008230099,0.0126645565,0.0019781855,0.0064814645,0.017605312,0.016233956,-0.0046032616,-0.020680413,-0.004927793,-0.017738398,-0.025369516,0.032374024,0.020608712,-0.0143660605,-0.005440981,-0.016708504,-0.0033792974,0.013903301,-0.038923837,0.025293263,-0.013416707,0.00812882,0.0043012854,0.0026543427,0.019787265,-0.003607357,0.0026221084,-0.017865391,-0.008780679,-0.005676165,0.002859318,0.0013545966,0.00805566,-0.00056036335,0.0014656017,-0.014987389,-0.0013156942,-0.0035188026,0.0018486021,0.003809814,0.0085486,0.010389909,-0.0013485327,0.0083940495,-0.003047001,-0.010007865,0.016974201,0.008716421,-0.017115135,-0.060436305,0.022042383,0.0145514,-0.011612448,-0.00056941045,0.007750596,-0.025090614,-0.024399033,-0.025600348,0.015941495,-0.0062566693,0.00668699,-0.012107769,-0.01790162,0.018924154,-0.0027750754,-0.015376092,-0.005514586,0.0077293254,-0.012096482,-0.00813659,0.002665484,-0.009688858,-0.0042116335,0.007007799,-0.005138823,-0.019793069,0.024198093,-0.018518899,0.015167842,0.012985993,0.045215227,-0.0045790668,0.0037492744,0.0017449758,-0.021460515,0.00828162,-0.017916135,-0.012080844,-0.007951345,-0.023087913,-0.01936515,0.010427176,0.003498426,-0.000377063,0.00585007,-0.017147165,0.0059622657,-0.014392581,-0.009416836,0.018028902,0.007897329,0.018184004,-0.0026806954,0.0018358206,-0.018704364,0.009873483,0.00024408,0.003162147,0.016075423,-0.0018020804,0.0023861122,0.005327732,0.010470546,0.0049754255,0.0076822396,-0.0043435246,0.018971343,0.0037207883,0.020003524,0.003204651,-0.0037309658,0.0059465063,-0.038992457,0.004757658,-0.004352592,0.00024942242,-0.010222988,-0.004880391,-0.00051331223,-0.0030197008,-0.0024762833,-0.0026530097,0.027470857,0.009844376,0.012329242,-0.01766513,-0.0077476925,-0.011832241,0.0010963344,0.0011934096,-0.00030633353,-0.012785604,-0.016894368,-0.010275823,-0.02032658,-0.019142626,0.012432612,0.0054903477,0.00044470472,-0.015241397,0.012001237,0.0032422533,0.008498366,-0.01672698,0.043800697,0.02004561,-0.007442349,0.0010763458,-0.003092615,-0.0012390456,0.016256476,-0.007560217,0.00044544795,0.012267895,0.0005566124,0.0077067325,-0.0035926194,-0.025034439,-0.0006411619,-0.014956913,0.011669654,0.024425862,0.007582407,-0.009875312,0.016075958,-0.012499361,0.02204758,-0.0067594126,-0.020703772,0.0034677943,-0.023233853,0.014704123,-0.0045115366,-0.009525309,0.009478555,-0.007866443,0.013315444,0.019066414,0.00972059,-0.0020522757,0.010050401,0.009857481,-0.00946436,-0.010714444,0.005716867,0.014305397,0.008960419,-0.016543582,0.008193665,-0.016731279,0.0042626658,0.0149589805,0.0059344354,-0.0214828,0.01067811,-0.026735349,0.0028394198,0.0024392358,-0.033903595,0.0051929965,-0.0023995475,-0.013582042,0.007160924,0.012228061,0.023165377,-0.010332165,-0.0089759985,-0.010094225,-0.010318963,0.005050543,-0.0038243947,-0.0018651589,-0.005838255,0.010524639,-0.004636356,0.022838295,-0.020578166,0.006272831,0.028657038,-0.018824032,0.0014207609,0.003372122,-0.008184678,-0.005047023,-0.0071520787,-0.0068528894,-0.009745609,0.007185668,-0.0027036718,4.1927367e-05,-0.00844595,0.0132087,0.024924994,0.0023114805,0.0072177234,-0.021408109,-0.013356459,0.006081163,-0.013490728,0.021092266,-0.019569477,0.0070861606,0.018016884,0.02372852,-0.006132122,0.0048901206,-0.0044081025,0.028510846,-0.019752229,0.008577518,-0.00025671764,-0.0037817787,-0.0043375394,0.019916287,0.024444126,-0.008216005,0.012553683,-0.011288201,-0.0021441923,0.007514169,-0.0010573788,-0.0018052364,0.024210615,0.0050868415,0.008460535,-0.038093437,0.014652418,-0.017626995,0.0122171845,0.025896683,-0.0030311334,-0.0024700367,0.00011120214,0.0006048239,0.009731845,0.009816473,0.0068867467,0.0090077175,0.002943975,-0.0015883038,0.008161613,-0.0059644445,0.0049386313,-0.026798986,0.008698915,-0.007850942,0.027840566,-0.0030631102,-0.016849302,0.013909132,0.02000406,0.041303225,0.029522218,-0.004985619,0.036274515,-0.012162359,0.0061334316,0.008562249,-0.000675475,0.0065348223,0.023820965,0.013647615,0.0027255598,0.0065153684,-0.029779904,-0.008289677,0.016622385,0.0022205953,-0.05494319,0.018867975,-0.0048597995,0.0031087543,-0.0034002138,0.0062171337,-0.0019669253,-0.009586384,-0.00339332,-0.02065143,0.003880935,0.015471951,0.00041116396,0.0056523257,-0.015819805,-0.025184982,-0.010875704,0.01663077,-0.00998538,-0.020650018,0.007076853,0.011714251,0.01053321,0.0063831843,0.013035526,0.0012893006,0.008689229,-0.0010973575,-0.002549886,-0.010716036,-0.0059334356,-0.013045711,-0.007996617,-0.0074745193,0.008057726,0.0084564425,-0.0004960627,-0.021687979,-0.0016020584,0.01723391,-0.017240148,-0.008548492,-0.016717086,-0.004925825,0.0059806486,-0.0011026389,0.023257693,-0.018504078,0.01781853,0.005993464,-0.03211216,-0.0038761564,0.009111164,-0.023630561,0.0047496967,0.009598979,0.00458332,0.012460096,-0.00498863,-0.024148192,-0.022346606,-0.0016171747,0.0008144851,0.007587033,-0.0060803466,-0.0072308676,-0.00827067,0.00656454,0.019087533,-0.014010776,-0.006718823,-0.0072790626,-0.030750448,0.00729727,-0.017612167,0.01969663,0.0039682826,0.011150022,0.0066060117,-0.0084666535,0.0048121237,-0.014544825,-0.07140231,-0.02125771,0.024381906,0.00167959,0.012120885,0.01441598,-0.011491937,-0.016575422,0.021462422,0.011694567,-0.0047030062,-0.0027173068,0.0047544,-0.015446604,0.0035204787,0.0034416502,0.006768281,-0.0024676002,0.0184967,-0.006353521,0.0017962186,0.004796953,0.01059752,-0.01076091,-0.0043788487,0.023376403,-0.0043862304,0.009414672,0.0019728558,-0.012747202,-0.00869629,-0.2046519,0.016156595,0.0052859145,0.016721519,-0.023892572,0.008700669,-0.00560608,0.009865224,-0.020880723,4.89799e-06,0.00617535,-0.027437635,-0.029380318,0.010881504,-0.01152909,0.14824192,-0.013178627,0.0014085254,-0.0035596339,0.0035463902,-0.014502542,0.008982002,0.017104486,0.008558227,-0.008621851,0.0044360855,0.008865959,0.0069949,0.026348138,0.01474324,0.007997688,0.010387395,0.009790895,-0.020420436,0.015177408,-0.0032151975,0.010122484,-0.008572475,-0.008824186,-0.018801684,0.025268057,0.0007433373,-0.01675837,0.0059413933,-0.003455896,0.005228697,-0.017374994,-0.011262112,-0.010954701,0.0038637153,-0.03473954,-0.10874599,0.003523336,0.011434762,0.01686351,0.010472656,-0.015545147,-0.019345803,0.003572552,-0.004965534,0.010989061,-0.0019040714,0.0030750153,0.0154623855,-0.006630387,-0.0010066929,0.0012589676,0.013742433,0.017636161,-0.0015735741,0.022851598,0.00875158,0.0027471606,-0.0036252814,0.0044690296,0.0020211358,0.013104551,0.010988133,-0.00208374,-0.004434597,-0.0008491232,0.0022941118,0.006125241,-0.0037784192,0.0074909427,-0.0056154775,0.009895838,0.007761955,0.027236186,-0.0008824806,-0.015619177,-0.009882733,0.021897255,-1.06583775e-05,-0.00094614254,-0.016014744,0.011774501,0.016996197,0.0052825734,-0.010813647,0.014603604,-0.011130204,0.014492088,-0.016457474,-0.005113014,0.01295726,0.0047155553,0.00972008,0.016537093,-0.010713245]
54b5ba3d-c45a-4bee-8f53-ffdcf430bd17	How to reset your password 	Account	If you have forgotten your password or simply want to change it for security reasons, follow these steps:\n\n1. Go to the login page and click on the "Forgot Password?" link located below the login button.\n2. Enter the email address associated with your SupportHub account.\n3. Check your email inbox. You should receive a secure password reset link within 2 minutes. (Be sure to check your spam folder just in case!)\n4. Click the link and enter your new password.\n\nPlease ensure your new password is at least 8 characters long and contains a mix of letters, numbers, and special characters. If you no longer have access to your email address, please contact support for manual verification.\n	0	0	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-07-28 09:49:21.991425	2026-07-28 09:49:21.991746	[-0.010826828,0.022501333,0.008624001,-0.05502112,0.002557018,0.020482296,0.009298424,0.009131366,-0.012143107,-0.0013276254,-0.005468719,-0.00624782,0.0008488981,-0.0025077043,0.12669508,-0.013937205,0.014106397,0.0051430506,-0.0065776026,-0.017919168,-2.9748553e-05,0.0012868886,-0.0052708485,-0.008854015,0.00832962,-0.020342201,0.0021857752,0.016915593,0.0064526196,0.019162368,-0.0007048482,0.024167528,-0.0031801383,0.021914588,-0.006788277,0.010266651,0.009072478,0.011979304,-0.010530623,0.012851089,0.007528626,0.0056933905,0.0011853535,-0.0033281138,0.011185628,-0.0040149884,0.0033016875,-0.026937554,-0.0127592785,0.010221634,-0.020442957,0.0022116392,-0.030028865,-0.25176892,0.0036391623,-0.006451441,0.019301765,-0.006546167,-0.009445565,-0.01738297,-0.015602353,0.017064203,-0.01972555,-0.015135497,0.030256806,-0.0034900375,0.03333609,0.03533003,-0.0045546205,0.020646228,-0.010904108,0.00054201705,-0.0017554789,-0.01883278,-0.01920064,-0.0151985185,-0.0058894237,-0.026965618,0.006384418,-0.00463452,0.0047654626,-0.001295958,0.0031944523,-0.010782038,0.005247693,-0.02625813,-0.010932229,0.015233888,-0.004331672,0.0035252064,-0.01851173,0.013323243,0.0023101727,-0.016844189,0.018765675,-0.00029097105,-0.015121154,0.01255448,0.016828543,-0.015323675,-0.00029511785,-0.024022818,-0.008774331,0.0049044373,0.004759209,-0.0022554484,0.0055727945,-0.008898913,-0.017470704,-0.0014468046,0.03011495,-0.007778148,-0.003929759,0.018752322,0.016208924,-0.2077772,0.008913754,0.00658328,0.011525382,0.0004502209,-0.028284151,0.0016191313,0.0017616331,-0.0068986663,0.0033946247,0.00012362275,-0.00023784477,-0.016523067,0.021951772,-0.001429874,-0.004646108,-0.008933433,0.008746081,-0.014128412,-0.012778387,0.014479656,-0.0067434926,0.0057259407,0.021170475,-0.0154290795,0.027599791,0.0063202917,-0.0037211068,-0.0032308737,-0.013225607,0.012852555,-0.006390164,0.015349376,0.0041968296,-0.013622997,0.014705001,-0.01658141,0.004782314,-0.007622702,0.011629368,-0.029677624,0.0036225521,-0.009774786,-0.02119571,-0.008873317,0.012416986,0.017420225,0.00454151,0.000845185,0.01183564,0.00985814,0.005377808,0.0064244294,-0.017621849,0.009248253,-0.024520544,-0.013782283,0.0036738075,0.002368653,0.005280993,0.01701445,-0.0030117265,0.0015478552,0.022403952,-0.03257583,-0.0009560383,0.005468108,0.020610776,-0.011361629,-0.0004176376,0.012367175,-0.0030910126,-0.007914854,-0.017572971,0.0023085207,-0.008805211,-0.010884835,0.00709991,-0.00025587657,0.00967631,0.020356327,-0.011896551,0.0022138758,0.0053955032,0.0096245315,0.020651069,-0.021351697,0.019315917,0.0109131755,-0.004429803,0.0032606907,0.0028829558,-0.008153532,0.0043626856,0.007934815,0.003130112,-0.014870787,-0.0009801965,-0.019777285,0.0071487753,0.003551026,-0.0047570663,-0.009854307,-0.0024741206,-0.020963753,-0.016368318,0.02078445,-0.009013192,0.0018023839,0.015101771,0.008314121,0.025456706,-0.021835644,0.023875954,-0.00035058384,0.006163506,0.008848492,0.020050753,0.0021849612,0.0024226217,-0.010235869,-0.011324344,0.018063866,0.021929987,-0.010506268,0.012203332,-0.01299327,0.0034406842,0.0015244358,0.02210411,-0.011630926,-0.01579756,-0.011319826,0.007941167,0.010073746,0.011016902,-0.007012582,-0.0023206177,0.0011607691,-0.016949564,0.0035650963,-0.03904653,-0.021247115,-0.0049744532,-0.007840035,-0.007648199,-0.002513236,-0.011536766,-0.0061122235,-0.011630113,-0.0034624701,0.018499775,0.025686814,-0.00715381,-0.004797831,0.02074966,0.015945608,-0.012643408,0.015253428,-0.018790344,-0.015315354,-0.07521108,0.012701873,0.008572518,-0.031131478,-0.014103711,0.014000693,-0.00015179024,-0.019535305,-0.020435298,0.020129614,-0.0034757582,0.002496192,-0.020008866,-0.020798035,-0.0102292085,-0.003144541,0.010884979,0.0080474485,-0.019682804,-0.021567272,-0.0116117075,-0.000775013,-0.006312633,-0.03135325,-0.0009873919,-0.0036962545,-0.002116187,0.0026437105,0.0060635423,0.01446354,0.01487036,0.006432246,-0.0048339665,-0.01949567,0.009537953,-0.007919472,-0.004754133,-0.0034777008,0.02178192,-0.0059764516,0.0039904574,-0.0056281216,0.007009139,0.015905946,-0.0025287245,0.0040968624,-0.014937033,-0.001663192,-0.022051375,0.00026443167,0.0063447766,0.0022055681,-0.0050555496,-0.035076104,0.0037635274,0.0024533204,0.007932647,0.002749262,0.00349227,-0.0015638623,0.01151894,-0.0018071932,0.010252213,0.013509072,0.0021753293,0.0050129206,-0.021362208,0.017355293,0.015632907,-0.0083116405,0.012979796,-0.0129102925,0.012627994,0.0003987579,0.0026219338,-0.0040874286,0.012763598,-0.010004054,-0.0062711984,0.021564998,-0.02667701,-0.0014927969,0.0026005819,0.010965411,-0.0071680695,-0.013719284,0.010796136,-0.01853026,7.386092e-05,-0.008209248,0.015037664,0.00032231686,0.007527083,0.0011776265,0.0062868227,0.0042221746,-0.0054849847,-0.0019572794,-0.011303449,-0.009267485,-0.018173387,0.014635311,0.015563944,-0.010539304,-0.0055615674,0.020843951,-0.0046695382,-0.0003494009,-0.008234791,-0.0051055625,0.014382214,0.037338827,-0.016943151,0.002519461,-0.011439876,-0.008798836,-0.016218815,-0.0071968464,-0.031410247,0.030204864,-0.006168425,-0.00133393,-0.004889583,0.03122013,0.012812848,0.007824382,0.004659181,0.01359438,0.0075505436,-0.0037090788,-0.019471077,0.009360634,0.0035019394,-0.00624262,-4.353879e-05,-0.0040442473,-0.0111334855,0.001259885,-0.005108384,0.013969654,-0.023146177,-0.0020510599,0.012866592,0.0057577477,0.0047480534,-0.011473501,-0.029274618,0.03114404,-0.0076787286,0.010654567,-0.00031074206,-0.02227134,0.008725353,0.026850885,0.0035809767,0.003041838,-0.017924638,0.020919237,-0.00026023688,-0.013474056,0.0016782535,0.0010007591,0.0026747806,-0.0042202575,-0.0041469666,0.004882788,0.012564691,0.010741282,0.010576194,0.012111428,0.031799406,-0.014469802,-0.014554778,0.00027333555,0.016226768,-0.021274414,0.01903511,-0.021246925,0.011908734,0.0015386447,-0.003369289,0.013261396,0.0037517631,0.014785184,-0.0008456469,0.010142699,0.007556062,-0.01860925,0.005324239,-0.014954412,0.012548847,-0.022950009,0.0076180347,0.032084096,-0.0076316795,0.00014787039,-0.003774415,0.015144118,0.008160501,-0.01704606,-0.026282793,0.019081138,0.0051232683,0.021145798,0.01307505,-0.012570864,-0.016150154,-0.019606711,0.019367952,0.0049956264,0.003099645,0.03133656,-0.0017685218,0.0030408672,0.0102430945,-0.015871754,0.0037176497,0.014019186,0.004026966,0.00047841866,0.010739133,0.018773997,-0.023517923,0.00042798437,0.024400426,0.016632564,-0.025874907,0.014713994,-0.002877488,0.0037759372,0.017489059,-0.007763704,0.0089837,-0.0041149775,-0.022262687,0.015012564,0.011409085,0.014468653,0.00797699,-0.0011247019,-0.012454238,-0.0038250776,0.006791632,-0.009185008,-0.022627389,-0.0014982149,-0.012526341,0.014495243,0.012442367,-0.034859292,0.00782809,0.02007584,0.011978761,0.013807154,0.009805168,0.01501408,-0.013297142,-0.018528631,0.0249573,0.0051611327,0.011342524,-0.02337974,0.023773605,0.01044543,-0.013936853,-0.008480854,-0.011343351,0.008350817,0.0019397977,-0.062323503,-0.0008956753,-0.00030164854,0.0053221094,-0.0011033834,0.005366008,-0.018178958,-0.004562803,0.00062012026,-0.0059104036,-0.010153885,0.006772785,-0.01633485,0.0065565477,-0.016798666,-0.01186392,0.008349328,0.0076815076,-0.016320085,-0.0027065608,-0.0019621607,0.024461893,-0.008888805,0.002763623,-0.012768249,-0.0011993627,-0.006486845,-0.017579991,0.001795009,-0.0043466864,-0.0090319915,-0.0024930302,0.0011082841,0.007373043,0.015457572,-0.0049112043,0.014615008,-0.036329646,-0.0006805555,-0.0052569336,-0.025727054,-0.022525193,0.011951017,0.023204139,-0.0018620105,0.0058053266,0.007902264,-0.014825245,-0.010932629,0.0048587997,-0.04379434,0.009990512,-0.0026086136,-0.024617082,0.009129436,0.0038481131,-0.007818805,-0.012269288,-0.019999458,-0.026784856,0.0027107287,0.0070290547,0.0032013028,-0.0051031914,-0.0151661355,-0.0011055719,0.01056437,0.010041,0.01042198,-0.031060405,0.00066068146,0.0012530251,-0.029960347,0.008744651,-0.036868237,0.007317857,0.005687888,0.007846047,-0.0028379355,0.0030065724,0.033652112,0.0053405054,-0.059218396,-0.028825346,0.008569683,-0.0057972716,-0.017227715,0.015471321,0.003486656,-0.020125307,0.0036073914,-0.002067481,0.0053242655,-0.008361253,-0.00828519,-0.013487795,0.015829474,0.0021315117,0.014196143,-0.0008773884,0.00018675742,-0.01234765,0.012975343,0.013834153,0.009127664,0.021530267,-0.009209072,0.013257906,0.002536186,0.0058500725,0.0065337145,-0.007908907,0.0050320234,-0.18620233,0.013603228,-0.013460518,0.005170651,-0.0059086233,0.0005173303,0.0066610095,0.02325336,-0.01154172,0.0034616387,0.018239055,-0.018661987,-0.031822294,0.004707038,-0.015637929,0.13938574,-0.019590355,-0.0019187683,0.008597749,-0.008500971,-0.010929673,-0.0078385705,0.028855056,0.019526288,0.0027901805,-0.01788731,0.019889422,-0.016383288,0.0052568815,0.021951523,0.034156796,-0.0056300177,-0.006462154,-0.008618105,0.016093567,-0.0022298945,0.01858974,0.000664339,-0.01546315,0.004188056,0.0057215076,0.0014511507,-0.018221412,-0.012624914,-0.009405446,0.0005225038,0.004091431,0.0025968226,-0.03143127,0.017539853,-0.004345044,-0.09731942,0.017683107,0.0055253785,0.0018511197,0.0052353046,0.002570495,-0.008643117,-0.0033930915,-0.003071822,-0.0006532877,-0.0009597993,-0.010387558,0.027286863,0.009840339,-0.0028057809,0.030531527,0.0026528707,0.004786699,0.006417579,0.0105701545,0.011935398,-0.009099455,-0.01085233,-0.002554702,-0.017499167,-0.006915023,-0.020701094,0.0031570636,-0.006800444,8.41493e-05,0.003958932,0.0051719435,0.001742282,-0.02344057,-0.015438513,0.010504992,0.023410065,-0.010307681,-0.0038467473,0.0066627506,-0.027767858,0.001551904,0.006152813,0.0014851572,0.015563855,0.0043118596,0.0077069355,0.0060363496,0.025216097,-0.010921673,-0.008574591,0.0148589425,-0.018971916,0.032443423,0.016091635,0.007442907,0.0036838895,-0.0033480108,0.0058296877]
b6977faa-2b77-4b04-a375-bb67505b6015	What file formats and attachments are supported in live chat?	Technical	SupportHub live chat supports images (.jpg, .png, .gif, .webp), PDF documents, text files, and logs up to 10MB in size. Click the Paperclip (📎) icon next to the chat composer to upload attachments.	89	35	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-05 16:03:56.671441	2026-08-05 16:03:56.671548	[-0.0037824153,0.02456233,-0.007951194,-0.07206036,0.0029288463,0.02243484,0.013088712,-0.0018413769,-0.00012683809,-0.0053872014,-0.0075952173,-0.0026090008,-0.0024206275,-1.2035845e-05,0.10607108,-0.005072717,0.013588567,-0.004098024,0.009967266,-0.03303872,0.0019076499,-0.0033961928,-0.0146954525,0.0076827314,-0.011028246,-0.019305423,0.032913126,0.00890318,0.0031360285,0.024325555,-0.0001380228,-0.0073966845,0.004315728,0.001128235,0.0032993725,0.019267764,0.016719084,0.006241495,-0.0056848763,0.013676523,-0.013260061,0.02344116,0.016739566,0.0049325046,0.0019260851,0.020600965,-0.007855369,-0.035733365,-0.018403916,0.02422293,-0.017990576,-0.0027280191,-0.009811821,-0.2114331,-0.0014843313,-0.018430304,0.011957118,-0.0016371022,0.0067509552,-0.004508317,-0.00424999,0.023163527,0.008823041,-0.02443952,-0.001177662,-0.007943868,0.011279842,0.032087497,-0.0024187658,-0.0051733637,-0.0010001046,-0.0038893723,-0.012555777,0.0016628257,-0.007840044,-0.026464505,-0.008815913,-0.0008342377,-0.0012327873,0.023714637,-0.019274266,-0.02932573,0.0070566186,-0.015289304,0.009270654,0.023872783,-0.008402707,0.013933509,-0.041043673,-0.0012061399,-0.000795521,-0.004880398,0.019360324,-0.007904734,0.01614319,-0.018989865,0.014901982,0.006656335,-0.0055419155,-0.015831413,0.015124788,-0.021149198,-0.02631401,0.022180272,-0.0043022647,-0.0018798737,0.0046331463,0.001294712,-0.024498148,0.021579577,0.009231458,0.0054777106,-0.008512162,0.02465746,0.00926624,-0.19867004,0.01949648,0.017996758,0.014136901,0.023218332,-0.02881993,0.0075805667,0.029780548,0.0001075283,0.011833277,0.0057996213,0.019585101,0.0049716895,0.015910814,-0.005505888,0.002095429,-0.006632087,-0.014746226,-0.01567229,-0.008304923,0.016159726,-0.012172053,0.024931334,-0.00020117404,-0.0073245736,0.017761825,-0.009803859,0.018002989,-0.010041052,0.0028778152,-0.008480102,0.006426218,0.022999903,-0.006977585,-0.011827265,-0.011153692,-0.021695351,0.0065335995,0.022435816,0.012214413,-0.028330058,0.030861638,0.0153259775,0.008585313,-0.0007479509,-0.004176235,0.0065729916,-0.009553313,0.0002559277,-0.0043610786,0.02281079,-0.008442475,0.020684829,-0.03252164,0.02142117,-0.0099331895,-0.010234635,0.016952774,-0.0010860848,-0.0064015826,0.00038408607,0.0045046555,0.0050601377,0.0109387925,-0.025368486,-0.012609718,0.031609323,-0.013614015,-0.013246056,-0.032588903,0.00037309647,0.0021605003,-0.016125124,0.0052884095,0.0006413582,-0.009478531,-0.014814582,0.00914979,-0.0061332886,0.009143392,-0.0043672924,-0.029454965,0.0027524715,0.024942173,0.010775723,0.006054355,0.002811245,0.006792202,0.020133866,0.0031173895,0.018436227,-0.0036171863,-0.02020217,0.011960772,-0.017881272,0.00803892,-0.016042937,0.0016122962,-0.0070662703,0.008425516,-0.002161435,0.0007048517,-0.021253156,-0.012115327,-0.027439635,0.0028256262,-0.020377317,-0.008400205,-3.791535e-07,0.008277483,0.011422723,-0.0076026097,-0.014341143,0.024273908,-0.00020032733,-0.0048547685,0.025481207,0.00084157375,-0.005447545,-0.005936019,0.0052116057,-0.006871834,0.002980457,0.008260215,-0.010957062,0.0028118019,0.005039501,-0.0074861282,0.024336223,0.025940536,-0.029787911,0.02364626,-0.017990842,-0.0013565149,0.01862266,0.00033372556,0.011191082,-0.018499514,-0.003777386,-0.020053899,0.023541806,-0.023904786,-0.013565151,-0.0046068635,-0.008291342,0.015992608,0.008962448,-0.018041769,-0.021213537,-0.0025353509,0.011131624,-0.008054543,0.00018892568,-0.02782611,-0.0016495021,0.01357164,-0.0041593267,0.0026039556,0.00903273,-0.006313326,-0.00014453162,-0.078649096,0.0014300285,0.025936699,-0.035795886,-0.0017820908,-0.003637672,-0.04902403,-0.027695552,-0.003739279,0.02929492,-0.0035627955,-0.0056244787,0.0086924145,-0.003756332,0.026531488,0.008070431,-0.018119328,0.03071864,-0.025937617,-0.03087061,0.015940173,0.008848348,0.00047329126,-0.05225482,-0.024067469,-0.017871374,-0.01970048,0.014599301,0.01445047,0.019280257,0.010058265,0.0010103505,0.0042241393,-0.0105331745,0.00954514,-0.029630003,-0.008049699,-0.01557102,0.0049976027,0.016884746,0.0051019047,0.026434956,0.003939847,-0.00059588894,-0.006161492,-0.018900502,-0.011629062,0.010277107,-0.029808026,-0.02122966,0.01152107,0.004577235,0.028926391,-0.013685774,-0.0062229745,-0.031177435,0.00810291,-0.008153867,0.0050416146,0.017830158,0.01678686,-0.004931957,0.017094519,0.013941494,-0.005380295,0.011579794,-0.005987085,0.0032281193,0.0041549364,0.020625528,-0.012042566,-0.017243963,-0.0025392312,-0.034079026,-0.016343512,-0.014328657,-0.01592895,-0.016167494,-0.016361892,0.0071313176,-0.017036064,0.006748799,0.005833938,0.02915214,-0.029962275,0.018615933,-0.017060451,-0.0017887305,-0.004125636,-0.008975507,-0.0069471016,0.009270654,0.008096676,-0.008565782,0.008645187,-0.0014080929,-0.01766451,0.014778205,0.011414173,-0.022352386,-0.0059416476,-0.004099616,0.0029472641,0.009026113,-0.008016348,0.007375481,-0.0060142446,-0.008801788,-0.018823225,-0.010047397,0.005711229,0.016572969,-0.0068008592,0.021142704,0.004948889,0.03603464,0.006423242,-0.0052103736,-0.007124578,-0.0031396851,-0.011158971,0.02429338,0.029358113,0.009927434,-0.0029516155,0.021225562,-0.010135847,0.02917593,0.01629919,-0.02117499,0.0015118521,0.00080831425,0.018300358,0.02194475,-0.0011513786,-0.012985982,0.017952507,0.017462699,0.010068403,0.005195148,-0.009824831,0.018667169,0.017978298,-0.030286096,-0.024861872,-0.013377211,0.020562643,0.0161503,-0.0045344755,0.009484813,0.010962353,-0.016443701,0.02055834,0.0042144703,0.011614205,-0.031492762,-0.0022098876,-0.0003097353,0.013503623,-0.033051893,-0.00045408492,-0.008248769,0.00016225492,-0.022822436,-0.0025420578,0.02042813,0.0120398095,-0.0016003931,-0.020783275,-0.0044567664,0.016152862,-0.012119919,-0.010792794,0.020374369,0.01393406,-0.008480711,0.02247447,0.002560407,-0.015331662,-0.0077651693,-0.02684923,0.017353302,-0.024971338,-0.0034973095,0.00057031953,0.013524768,-0.006540511,0.015377581,0.016009614,-0.02229669,0.002479462,-0.0021688184,0.016737401,0.057297327,-0.00740087,-0.0023623086,-0.0036997416,-0.01539495,-0.011017165,-0.015178521,-0.015660757,0.011998341,-0.0029167202,0.017408201,0.013137939,-0.00867871,0.013524937,0.0033872796,0.017413747,-0.0013709294,0.011611634,-0.008940696,0.0036816741,-0.010523842,0.012404806,-0.0024431946,-0.003592641,-0.00070750376,0.003936941,0.0066618873,-0.009707836,0.012056421,-0.0090372255,0.028762674,0.016376318,0.013546112,-0.050212014,0.018630791,-0.015471237,-0.00926071,0.014974492,0.00946063,-0.01191952,0.023861539,-0.005509866,0.013305036,0.0024215702,0.024487637,0.009140902,-0.021190507,-0.025348598,0.0057178694,0.015498953,0.004932174,-0.03697253,0.010677654,0.013904223,-0.00072917476,0.005074655,0.0021930858,0.005553578,0.0039908905,0.0151466625,0.015538845,-0.016734304,0.015458092,0.021525139,-0.014945433,-0.002392882,-0.0044504125,0.0010572444,-0.0074961544,0.023538841,-0.0050390936,-0.0031973706,0.0055058394,0.018824847,0.021286871,-0.009396422,-0.09260446,0.0029073062,0.013600383,-0.01371277,-0.01951446,0.01061978,-0.01248572,-0.029404962,0.0029898144,-0.0036200273,0.011812764,0.018095946,0.018563218,0.012430441,0.013644802,-0.015395968,0.022985931,0.010223053,-0.020426648,0.0021937245,0.010742731,0.017138835,0.0066384277,-0.002594852,-0.004336164,0.004716578,-0.008247312,-0.013187729,-0.010893979,0.013681999,0.012955897,0.006219436,0.0053194985,0.0036311843,0.012708417,-0.0013394867,0.008543491,-0.028764691,-0.0016397199,0.0011474123,-0.03198094,-0.021709904,-0.0021592006,0.012205109,-0.019568214,0.011627836,0.011604435,-0.0127397785,-0.00417419,0.008100471,-0.042322148,-0.009609294,-0.0027517048,-0.012433526,0.01159105,0.002854478,-0.00015033557,-0.012083078,-0.030285513,0.007900413,-0.008726926,0.024180131,0.00205587,0.024154842,-0.014199914,-0.0033629136,0.01263076,0.0313531,0.00999442,-0.008072562,0.0022642948,-0.002577147,-0.013097136,0.010341952,-0.046208072,-0.01794968,-0.0019682357,0.007418363,0.013101095,0.0070964773,0.014510851,-0.008407985,-0.057134666,-0.013935571,0.0071598776,-0.010843247,-0.011228823,-0.00021936522,-0.016201556,-0.017038913,0.009457941,0.008229912,-0.0075898855,-0.0025597755,-0.0235862,-0.013720819,0.0100968145,-0.005649444,0.04194687,-0.023669897,0.005849413,-0.021303501,0.018621206,0.0011458335,0.027141258,0.019777136,-0.019436875,0.00950152,0.018220553,0.019301279,0.018407106,-0.026355613,-0.009221092,-0.14453614,-0.011073638,0.005169538,0.018853767,0.007240025,0.012077291,0.0058393874,0.02277614,-0.016757606,-0.020300783,0.009330583,-0.0032196657,-0.03093386,0.014426438,-0.008663818,0.1378789,-0.011816698,-0.0007604033,-0.011323516,0.0015861517,-0.017902758,-0.0068632774,0.006965071,0.024794387,-0.014362492,-0.012152823,-0.0041276896,-0.0074253688,0.008125695,0.00018811725,-0.0076653925,-0.0069179945,-0.008433942,0.008135424,-0.011296726,-0.013748631,0.019158276,-0.0028004837,-0.0022142164,-0.00857353,0.024652956,-0.01522889,-0.014376456,-0.022425113,0.0022144823,-0.009667694,0.013017183,0.012013181,-0.00087527634,-0.0044271657,-0.0044784923,-0.08081142,0.00082065223,0.004921501,0.035988305,-0.014331603,-0.0058191614,-0.0011998446,0.020897686,-0.012185313,0.02744753,0.00774132,-0.014465857,0.02044911,-0.016972391,-0.005731389,0.0124817835,-0.0022838404,-0.025098104,0.00029076426,0.013090002,0.011826626,-0.002997204,-0.01642118,-0.009376528,-0.012521205,-0.018903047,-0.02063838,0.028439874,-0.0131836375,9.987474e-05,-0.013489127,0.016783372,-0.0030992997,-0.023815606,-0.017592387,-0.008602804,0.021720748,-0.009071703,-0.01179037,0.004279997,-0.0011461644,0.02458596,0.006494146,-0.026940096,-0.0060684774,0.017785022,0.016074268,0.022191193,0.010479798,-0.0077628344,0.0058061457,-0.0011835181,-0.010059742,0.00054854824,0.0033378238,0.015943807,0.0071609,0.0038195592,-0.0043771304]
681cebde-fa36-423e-a229-18986847c409	Troubleshooting WebSocket connection issues	Technical	Real-time chat requires an active WebSocket connection to function properly. If you are seeing messages fail to send or the chat window is delayed, please check the following:\n\n1. Corporate Firewalls: Some enterprise networks block WebSocket (WSS) traffic by default. Ask your IT department to whitelist traffic on port 8001 and 443 for our domain.\n2. Browser Extensions: Strict ad-blockers or privacy extensions (like uBlock Origin or Privacy Badger) can occasionally intercept WebSocket handshakes. Try disabling them temporarily.\n3. Network Drops: If you switch from Wi-Fi to a Cellular network, the connection may drop. Refresh the page to force a manual reconnection.\n\nIf the issue persists, please open a High Priority ticket with the Technical support team.\n	0	0	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-07-28 09:50:15.270651	2026-07-28 09:50:15.270845	[-0.008626447,0.023313673,-0.009349938,-0.081194825,-0.009446735,0.016887048,0.015814468,-0.004517853,-0.001371639,0.0006113882,0.005930196,0.010617044,0.008047496,-0.005111503,0.101640284,-0.009766239,0.017573709,0.008662573,-0.004043812,-0.0032863403,0.0029463929,-0.0019118172,-0.006387025,0.025854882,0.0061366903,-0.018659757,0.024415288,0.0045771366,0.036397904,-0.015225837,-0.011395304,0.009446823,-0.0017326133,0.013870273,-0.0014812793,0.013259997,0.00025292212,0.005671273,-0.0046276753,0.0040718573,0.0023054853,0.013712502,0.022442149,0.0014476895,-0.0091783665,0.021313205,0.020652998,-0.017418519,-0.010868275,0.025906745,-0.026100567,-0.0029341383,-0.0026514437,-0.21062551,-0.018687233,-0.009951913,0.020961242,0.010838286,0.0026896093,-0.032273397,-0.015378263,0.031436224,-0.001017342,-0.02945998,0.019466544,0.016908497,0.018651418,0.034654856,-0.00509314,0.0071024364,0.0029522427,-0.0023067293,-0.022336455,-0.017785449,-0.016793074,-0.032396037,-0.004640687,-0.017228309,0.010976443,0.015542382,-0.024344444,-0.035227716,0.019732252,-0.012521806,0.018351685,0.00062757835,0.006172218,-0.002388704,-0.02508389,-0.0021278593,-0.009722321,0.021967646,-0.006499579,-0.005281047,0.018575208,0.013000955,0.012437643,0.0039908383,0.0050711967,-0.0041211937,-0.009547606,0.0008184227,0.007824355,0.0041984534,0.012227893,-0.010272583,0.019897927,0.009062538,-0.019381182,0.017841946,0.025215954,0.0031419664,-0.020917004,0.0030888636,0.013709871,-0.2169234,0.012253373,-0.0032366645,0.0030960469,0.0022198404,-0.026336553,0.013476084,0.023559436,-0.004824868,0.0066867983,-0.0029895632,0.023834331,-0.0060472456,0.011560169,0.0070273485,-0.0077212662,-0.019026738,0.00058826123,0.0046385764,-0.007702276,-0.0023661149,-0.01915128,0.0099222,0.0015708858,-0.006275575,0.011742885,-0.0007344337,0.0036202283,0.00980484,-0.008040973,-0.0136827305,-0.023717763,0.029901037,-0.0074608475,-0.02183711,-0.015257982,-0.023642182,0.013556752,0.014036229,0.018048799,-0.0152489375,0.025667062,0.018264925,0.0015137851,-0.019633807,-0.00067585456,-0.00659017,0.004200779,-0.0098624,0.00891509,-0.03174107,-0.008484241,0.02209333,-0.008826289,0.013150469,0.004117224,-0.011360187,-0.0027435143,0.0073624304,-0.010550766,0.0072530936,0.0010223617,0.0032547202,-0.00012877745,-0.029277328,-0.0020239088,0.020045891,-0.0018615002,-0.0036869112,-0.022309646,0.011866824,-0.0092620235,-0.013293538,-0.025502983,-0.009640442,-0.01604842,-0.01022746,0.005173509,-0.0023227802,0.0048568877,0.004367669,0.0014524419,0.000102695056,-0.007637328,0.0039437376,0.0064772675,-0.0024103965,0.0009221134,0.012469361,-0.008679666,-0.0053243525,0.014444369,-0.006411001,0.013093898,0.0043108864,-0.011080346,-0.02275139,0.028854622,-0.011699711,0.02001189,-0.003420904,-0.011996235,0.005787816,0.021169053,-0.020772262,0.00023596994,0.0012510758,-0.008810307,0.019083027,0.008461022,0.0152433,0.02308986,-0.022389539,0.016484043,-0.0047835913,-0.0027351228,0.021170877,-0.003070095,-0.01661256,0.005470151,-0.014639353,-0.0036205023,-0.0067693857,0.034288198,0.0038972988,-0.0068136756,0.0011923418,-0.016158676,0.01066758,0.018615013,-0.008323679,0.030166335,0.006378939,-0.013410449,-0.0007761482,0.030442832,0.013606742,-0.028833399,-0.0040082606,0.006764427,0.0061040716,-0.010516454,-0.0072186408,-0.016009316,0.00879105,-0.00020962254,0.005041519,-0.005595854,0.012797213,-0.013007365,0.014646072,-0.0004609846,-0.0019616452,-0.03194042,0.018186616,0.000510904,-0.005727828,-0.029154627,-0.010041839,-0.011381401,-0.01290298,-0.076873004,0.006363351,0.0026592782,-0.024736267,-0.006854105,0.015340362,0.014549852,-0.025264995,-0.0057358253,-0.0029895608,-0.003717953,-0.010854608,0.00047210144,-0.020006001,0.014788959,0.0105302585,-0.013599196,0.0035898187,0.0036969283,-0.0055255312,0.0012747535,0.0058332365,-0.00848936,-0.031847145,-0.019041391,-0.0015601108,-0.0046800724,0.044810962,-0.0018737102,0.012260598,0.0383366,0.028508238,0.0077511873,-0.00055073615,-0.007819907,-0.016057543,0.00714909,-0.016335236,0.009137025,-0.020096341,0.019251656,-0.004007588,-0.01898507,0.009606776,0.013359795,-0.018300856,-0.007441415,0.0018613823,-0.019820629,-0.0200215,0.006961039,0.015798219,-1.1661867e-05,-0.008991231,0.022917693,-0.01957031,0.01126517,0.0020650427,0.024840133,0.024592187,0.021934092,0.0056828195,0.017228479,-0.00034971407,-0.0025471004,-0.0035040313,-2.742203e-05,0.006464077,-0.000839291,0.042105306,0.002786876,-0.0031860038,0.014966004,-0.02965092,-0.0079799425,-0.0002484418,-0.008233465,-0.004652714,-0.011086852,0.008456393,0.0025925485,-0.0028025801,0.0011995346,0.016500028,0.024051288,0.0069878693,-0.013503084,-0.014032649,-0.016559515,-0.015354207,0.016809942,0.009964824,-0.001971143,-0.0057299966,-0.0070889113,0.00016791603,-0.012612729,0.00030226528,0.029863713,-0.012628456,0.010648001,0.03115083,0.011514704,-0.005977409,-0.0039672796,0.023229571,0.0027259127,0.011693848,-0.019794723,0.005280405,0.008286064,0.0029478602,-0.017541748,-0.0054878583,-0.009974545,0.026631065,-0.0013280353,0.013208861,-0.014381591,0.0053028795,-0.008158721,0.018712651,0.02735383,0.0013979656,-0.01952021,0.012318327,-0.022829587,0.027497245,0.017228212,0.00021978829,-0.008477042,0.013576847,0.030839222,-0.00066058943,-0.0074567804,0.0038702313,0.0036789768,0.02362856,0.01418396,0.022603836,-0.02194349,0.012354706,0.009466616,-0.010566705,-0.008284462,2.5189167e-05,-0.0071978434,0.009590981,0.01966765,-0.0022929905,-0.014294434,-0.022003599,-0.0084231,0.001137976,0.0024789232,0.018458229,-0.020886863,0.0055268337,0.0014861341,-0.031671256,-0.002763622,-0.018894253,-0.014204095,-0.010014636,0.003768366,0.0066692196,0.00861134,-0.005827754,-0.007799579,0.011345188,0.01890525,-0.030059095,0.00010589627,0.006048383,0.025142163,-0.02806389,0.02409542,-0.0018070141,0.013544744,-0.0063694944,-0.022396848,0.018222267,-0.022926012,-0.002642071,0.0030620373,-0.008379891,-0.005199873,0.011720466,-0.0010867387,0.013660746,0.007253494,0.0014353578,0.021404378,0.054168712,0.010082983,-4.837869e-05,-0.0073790136,-0.004581355,-0.016019393,-0.0067258687,-0.0012775685,0.011245181,0.0018684071,0.008562629,0.02725629,0.015971135,-0.0012765987,0.008139108,0.013605083,-0.014672354,-0.00035536068,-0.018044092,-0.0045505026,-0.0026425356,0.011893008,-0.0033752802,-0.024165481,-0.010830735,-0.015075145,0.0042979545,0.0046658614,-0.0018212385,-0.010588838,-0.007796668,0.014933257,0.005618224,-0.051194075,0.0022363784,-0.002787495,-0.016403219,0.009196894,0.0064409957,0.0006002141,-0.009220582,-0.008265852,0.01014598,-0.007964314,0.010409472,0.0012134066,-0.0066601904,-0.007507158,0.006569096,0.010195731,-0.020225517,-0.0040834807,0.005006107,-0.0042522894,0.0125261955,0.011429435,-0.00088423054,0.012963757,0.012333543,0.003107341,0.009254398,-0.009171186,0.039459515,0.0038739627,0.0024634106,0.0021672873,-0.0047139707,0.0026249855,-0.0103764245,0.0083606,0.010928077,0.013792662,0.014186288,0.03126814,0.015571392,0.010326801,-0.091453165,-0.002385096,0.014668087,-0.0073715174,-0.0040122806,0.007998443,0.019790158,-0.004401065,-0.0022304517,0.0020022625,0.0092693735,9.743864e-05,0.013353227,0.006836913,-0.015522177,0.0056013465,-0.015830453,0.025802406,-0.011052861,-0.0076953582,-0.011635182,-0.002504786,-0.007970736,0.014698224,0.00997656,0.0015375145,-0.011935308,-0.015884457,-0.004026131,0.0077283923,-0.010328569,0.010732261,-0.0101714665,0.005004409,0.01808379,0.0072785197,0.01897527,-0.025013492,-0.008219039,0.013306817,-0.0068031154,-0.012235712,0.008081433,0.011268812,-0.0071022264,-0.004153901,0.012891515,-0.020947453,0.0059639355,-0.011673742,-0.039362904,-0.007891933,-0.0056213834,-0.030282592,0.00819712,0.021491755,-0.006769119,-0.00059780775,-0.03644305,0.015779775,-0.02640852,0.011498049,-0.0013729822,0.011099162,-0.018512249,-0.008919485,-0.008434331,0.026873438,0.0044563236,-0.004521947,-0.02605456,-0.009573193,-0.03643049,0.01800645,-0.028561361,0.0182857,0.0046653035,0.006742226,-0.019731106,0.022662127,0.023293495,-0.0076576723,-0.077642575,0.004263265,0.0020986325,-0.020607881,-0.004287273,-0.018733216,-0.007183501,-0.022002462,0.0030144171,-0.0016128097,-0.023184394,-0.012182398,-0.002725302,0.014169725,0.00468063,-0.0033814919,0.012246411,-3.1243104e-05,0.0057604723,-0.011059029,-0.0093833,0.007585398,0.003325155,0.011131952,0.002178258,0.004699447,-0.010744068,-0.0066733807,0.025360016,-0.013481913,-0.018548347,-0.15152699,-0.009494185,-0.003591114,0.004146178,0.0030838158,0.008317901,-0.009123499,-0.010103065,-0.038258426,-0.023476042,0.014803413,-0.023887042,0.0010016422,0.020341227,-0.013110554,0.15335827,-0.016884942,0.010190149,-0.019787384,-0.0101082865,-0.02145497,-0.01677,0.012287334,0.004189118,-0.008094527,0.0006045029,0.0051798443,0.0023584587,0.015697606,-0.0025818278,0.008520858,-0.010452824,0.010788245,0.0044304808,0.023323577,-0.0062110005,0.014601566,-0.011932772,0.019383267,0.012277158,0.007925394,0.014284914,-0.003802301,-0.016680129,0.0076625654,0.0012590594,-0.0013276509,-0.0061975885,-0.0072759297,-0.023758555,-0.016171403,-0.09305305,0.0031218457,-0.0051618917,0.028257487,-0.008314076,-0.010601909,0.0094542075,-0.0110549275,-0.0061790333,-0.0043481523,-0.0025458029,-0.009526662,0.030906139,-0.0025955501,-0.010901301,0.013032273,0.030405317,-0.017143244,0.005991214,0.013541146,-0.0077278274,-0.02362555,-0.027098205,-0.0015770072,-0.002182173,-0.02324791,-0.01031169,0.0122771105,-0.015451266,-0.020697018,0.002288511,0.006824854,-0.009363495,-0.016562134,-0.027608037,-0.0004562077,0.01712129,-0.0064819823,0.01566969,-0.02446979,0.0057101925,0.03285989,0.015040117,0.0030987763,-0.003789919,-0.0022841434,0.027443524,0.011373817,-0.0019097349,-0.004385875,-0.0060847807,0.010866648,-0.01342374,0.0047962475,0.017963246,-0.0018060966,-0.0037916065,0.022193205,0.0047674035]
83efcf29-d88c-4208-bef5-286fde78de72	Understanding your monthly subscription invoice	Billing	Your monthly subscription invoice contains a detailed breakdown of all charges incurred during the billing cycle. Here is how to read it:\n\n- Base Plan: This is the flat recurring fee for your chosen tier (Basic, Pro, or Enterprise).\n- Additional Seats: If you have added more agent seats beyond your plan's allowance, they will be billed here at a prorated daily rate.\n- Overages: Any usage that exceeds your plan limits (e.g., extra AI chatbot tokens or SMS messages) will be listed as overages.\n\nInvoices are generated on the 1st of every month. You can download PDF copies of all past invoices by navigating to Dashboard > Settings > Billing > Invoice History. \n	0	0	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-07-28 09:49:45.66964	2026-07-28 09:49:45.669841	[0.00052523316,0.022155805,0.006472724,-0.061679408,-0.0030252272,0.021770585,0.01862067,0.01771426,-0.038503245,-0.0008869416,-0.0023947912,0.008710735,-0.009412061,0.0005771432,0.108385436,0.013368492,0.037659924,0.014759503,-0.014375897,-0.025384592,-0.002391977,0.015838483,-0.009667677,0.008452679,0.002306428,0.024337467,0.017148083,0.019074978,0.037564013,0.017749216,0.004671062,0.00073839404,-0.013556696,0.0013379772,0.0105467,0.024877205,0.02489547,0.01762516,-0.011941724,0.019562043,-0.0057818773,0.01916724,0.00040409697,-0.018359497,-0.0036154713,-0.000656884,0.007310105,-0.03199696,-0.013916679,0.003473066,-0.0088531235,0.014500571,-0.014300563,-0.18247254,-0.0013504982,-0.03238967,-0.021678695,-0.011643191,0.013194893,-0.02725151,-0.015200012,0.025202872,-0.016070863,-0.013195683,0.011604774,0.015844397,0.02621449,0.018766308,0.007130406,-0.0121306125,-0.0023688625,0.01597391,0.0039959876,0.0015993404,-0.0071330555,-0.008971285,-0.009609889,-0.011369168,0.0046296846,0.011152743,-0.015117593,-0.008282711,0.014268755,-0.010019015,0.020688456,-0.025078606,0.0043277666,0.014726957,-0.010602295,0.0059142155,0.0095114745,-0.0042086127,-0.0036958936,-0.029213093,0.018389432,-0.0072583407,0.018090807,0.0042191767,-0.01138718,-0.020926312,-0.018130697,-0.03914669,-0.027283138,0.009595588,0.009059857,-0.02986408,0.0031144198,0.00012689337,-0.029016556,0.015880423,0.013707814,-0.008429882,-0.013154163,-0.0047491626,-0.013934983,-0.20724234,0.02159501,-0.0093466705,-0.008925528,-0.0018818479,-0.0372736,0.014691582,-0.008972529,-0.00294169,0.007841553,0.0018439819,0.019024815,0.001861917,0.013888049,0.017917454,-0.008027572,-0.016405052,0.00032892195,-0.032771062,-0.0065115457,0.025512256,-0.015650645,0.00168753,-0.0023878005,-0.009706905,-0.009800732,0.02697354,-0.0015127102,-0.04161678,-0.011620607,0.0146113625,-0.009942377,0.026663166,-0.015563559,0.0074391454,0.016709697,-0.007239212,0.014122185,0.022075817,0.030117026,-0.02578061,-0.0050478973,0.0058711,-0.0026388476,-0.00268064,0.009325989,0.010440789,-0.016686121,0.020966198,0.0041941814,0.01422925,0.002242898,0.0032944393,-0.020791091,0.025417313,0.017624272,-0.0006373759,0.0098712165,-0.013025769,0.009285239,0.021584019,0.014408981,0.0028463567,0.03602532,-0.026843771,0.0025115372,0.010646165,0.0011751499,-0.035509784,-0.010795548,0.0030159878,0.008770886,7.383496e-05,0.0027807483,-0.02716834,0.0065060584,-0.03144756,0.0077423314,-0.0025064645,0.009482171,0.0039767977,0.0027814005,0.016501421,-0.007346416,0.01738704,0.049593158,-0.022803014,-0.015275913,-0.007944659,-0.013062181,0.016845163,-0.026026221,-0.011181526,0.012058873,0.00023146418,-0.0080311755,0.0029597061,0.0218291,0.0037072957,0.015009156,0.0019479237,-0.010141882,-0.010319066,0.005242262,-0.025803866,-0.016619677,0.0070393737,0.005319193,0.0045816014,0.017903501,0.022832459,-0.0056115193,-0.026739905,0.009772136,-0.0041416097,0.010873729,0.0096568735,0.0066480585,0.0066598803,-0.006441461,-0.0037594861,0.0041373884,-0.002202206,0.0010413923,0.023700701,-0.024621619,0.010861183,-0.0022114683,0.012135044,0.025929056,-0.0026869741,-0.0083985925,-0.0108065605,-0.005763741,-0.003427752,0.008507552,0.00859054,0.0040091565,-0.007154056,-0.02174111,0.0051683295,-0.041360054,-0.011823153,-0.009813122,0.00026021883,0.02421457,0.0029321997,-0.013921692,-0.002983162,-0.01026418,0.0064239237,0.013502111,0.0091062775,-0.03429777,-0.019254263,0.011477898,0.0032699497,-0.015800312,0.0058002807,-0.0044493973,0.0037074643,-0.09278146,0.009898364,0.012064769,-0.029218974,-0.0077561466,0.011135813,-0.0075916247,-0.014424892,-0.010402604,0.017041793,0.0014584493,0.00074157136,0.0106737055,-0.019518632,0.0076461174,-0.0047900476,-0.0029632482,0.010822605,-0.0023862754,-0.023292597,0.0062423185,0.020580081,-0.0012943193,-0.0023563646,-0.0072986186,-0.0052568344,-0.014554287,0.03884445,-0.0055396305,0.0016389559,0.012816067,0.02183553,0.0059697963,0.0042864922,-0.0045072325,-0.0055514085,0.030788759,-0.009045471,0.009735315,-0.006308328,-0.003536672,-0.03311717,0.008327042,0.02399939,-0.0070337444,-0.01159805,-0.00061453244,0.028496096,-0.020717524,-0.006201257,0.0021163775,0.0010160486,0.00538168,-0.0081827985,-0.010696019,-0.023513546,-0.00060170953,-0.0023993754,0.009026919,0.0056506363,-0.008091074,-0.0032876607,0.0099726105,0.01938205,-0.0036489223,-0.0042213057,-0.015737806,-0.0060271476,0.00038624945,0.00844487,0.01587456,0.00736498,-0.0062721386,-0.006002891,0.017300438,0.010010692,-0.0012437743,-0.03072589,-0.019944819,0.018547395,-0.007569872,0.0058836737,0.0014583681,0.0134273805,-0.0148413945,0.016748086,-0.007541133,-0.02756789,-6.8607966e-05,-0.0059008123,0.026045099,-0.0047589387,-0.005388154,0.002273786,-0.013369261,-0.008516866,0.0004941173,-0.0036370684,-0.005265893,0.0015193576,-0.01917342,0.015247544,-0.01578307,-0.0027066376,-0.0056661023,0.03747052,0.012389137,-0.016778717,0.00349608,-0.021404915,0.013561774,0.01419421,-0.007128003,-0.011992722,-0.011390686,0.011037384,-0.013695739,0.0027676288,-0.010726077,0.023332482,-0.016669689,0.007079399,0.010527734,0.014029883,0.0049737534,0.015916318,-0.015766481,0.007812526,-0.00048087505,-0.015451203,-0.018088473,-0.0013096915,-0.008792008,-0.0118344175,-0.010349761,0.007328559,-0.0022927835,0.0076298798,0.032340053,0.011102308,-0.013097609,-0.009484813,0.022764388,-0.021576282,-0.019361218,0.0012039506,-0.017474223,0.021008246,0.002354828,0.007998656,-0.0062772757,-0.017602557,-0.0033907478,0.009923963,-0.023692831,0.008010339,-0.008432941,0.0058762953,-0.006754287,-0.027122471,-0.010106665,-0.0019196414,-0.0019587222,0.0055749523,0.027476387,0.009307274,0.010051739,0.004189932,-0.00712695,0.0039232615,0.00075267296,-0.012924731,-0.0034581376,0.012488401,0.01533382,-0.0180223,0.02109181,0.00063431344,0.0016095879,0.022294788,0.022386748,0.016963085,0.007846629,0.00362517,0.02897298,0.011426097,-0.013565979,-0.010613507,-0.012720226,-0.021811323,0.004083972,-0.015388981,-0.012732489,0.024803694,-0.016952416,-0.0010180427,0.0048374534,-0.0066108294,-0.011001721,-0.019124877,0.011226083,-0.009242842,0.012556198,0.008544832,0.021449331,-0.009885195,0.0062864,0.0059932815,0.019955365,-0.0032861016,0.008198879,0.015860215,-0.013228102,-0.0134522,-0.00085147657,0.00427627,-0.031581532,0.00028137135,-0.0045759375,-0.010499973,0.01233633,0.014987293,-0.010448811,0.024689542,0.017052839,0.0112366015,-0.023855751,-0.0073659476,-0.0005101176,-0.008443846,0.003782125,0.024279028,0.007991017,0.014878773,-0.024349645,0.005584481,-0.0025514716,-0.0053388914,0.011754398,-0.016863449,-0.00810605,0.006364591,-0.020609641,0.0072473697,-0.0070543927,-0.01332857,-0.007043931,0.007924171,0.0099461675,0.0043850327,0.010244379,0.009430296,0.011558294,0.02093251,-0.017443335,0.022396188,0.0027710388,-0.013062016,0.009408615,-0.011796058,0.01612971,-0.0033449293,0.0021006984,-0.0062084273,-0.008163199,-0.014520042,0.017033864,0.009302398,0.0032614777,-0.09050005,0.022691283,0.018534662,0.036250655,-0.004078651,0.0018028914,-0.012903797,-0.018384878,0.008154099,-0.01629489,0.01703888,0.0027720807,-0.009239362,0.009083236,-0.018084966,0.006217536,-0.00056492334,-0.014492369,-0.034200832,-0.0011962181,-0.004833482,-0.00021588053,-0.003999146,0.0013112423,-0.0009006488,0.015146599,-0.0136149,-0.009576858,0.007988733,-0.016782133,-0.012711356,0.0033395851,0.0106744245,0.0051217964,0.020211777,-0.024477424,-0.0069083846,-0.004815205,0.0038889714,0.0076695,-0.008498748,-0.016857004,0.008242588,-0.008246632,-0.017444713,0.021405147,0.030994808,-0.016450282,0.013513971,0.017322438,-0.03602035,-0.009204962,-0.0069743446,-0.02304334,0.01196347,-0.016816948,-0.0068162396,-0.0057142745,-0.022329262,-0.012383641,-0.012787279,-0.0057627973,0.015871491,0.030078731,-0.016141389,-0.0021648996,-0.025449384,0.03105379,0.0018224855,-0.013209055,-0.008626959,-0.01565368,0.0016133861,0.033620115,-0.007619279,0.008357891,0.0009216389,0.0018837858,0.007355319,0.010686619,-0.003163263,0.0047026584,-0.05008881,-0.028628837,-0.013070477,-0.014749027,0.0014810212,0.005493346,-0.011596377,-0.010969166,-0.0029890246,-0.016671421,0.016097909,-0.018469092,0.0098018125,-0.023301043,0.00496417,-0.0013319006,-0.019299299,0.0022270784,0.010146975,-0.016453043,0.018501403,-0.004059258,0.010513243,-0.0059398385,-0.008893582,0.0076733707,-0.014860981,0.0024745963,0.017025452,0.0036856476,-0.008102773,-0.1759911,0.0140863545,-0.0047860458,0.022549152,0.004938125,-0.01050064,0.009524757,0.019151049,-0.013002493,-0.024948435,0.013277502,-0.021772295,-0.035205312,0.014217796,0.0026019886,0.16270179,-0.013239695,-0.0031133287,-0.0077992114,0.008094892,-0.0016342278,0.0056070457,-0.008318242,-0.004735476,-0.03207154,-0.017175324,0.025100928,0.0052768462,0.027858857,0.0059304577,0.024607167,0.012156995,-0.00058596843,-0.020239985,0.022031693,-0.008303885,0.026313413,0.0011192522,0.007917249,-0.0095951585,0.015400987,0.019185444,-0.023437217,-0.006955351,0.010145361,0.010605437,-0.016371533,-0.011788782,-0.0018772337,0.011883704,-0.014769889,-0.08368217,0.012724517,0.0055132452,0.009610206,-0.008059259,-0.015702613,-0.018642373,-0.0016008253,-0.004041257,0.014044281,0.009391828,-0.005497609,0.025219455,-0.023332145,0.0040188245,0.017004455,0.016915254,0.011616193,0.0077710403,0.0068615815,-0.009985145,0.002451657,0.0021890355,-0.008735268,-0.016447343,-0.020514946,0.008688296,0.013028179,-0.003482049,-0.0032062612,-0.0073998165,0.010915423,0.0051732007,0.005593604,0.0016078133,0.007954253,0.014607807,-0.017789433,-0.004809136,-0.014765701,0.0052176877,0.0032927445,0.022003537,-0.015149043,0.01087044,0.023905685,0.02179796,0.0022850663,-0.013012661,0.0031053498,0.006251718,0.03190423,-0.042482503,-0.00671845,0.0053557223,-0.019260583,0.018204752,0.004038632,0.013172932]
e4634581-a28f-4305-958e-81fa34d0d3cd	What are your support operating hours and AI response times?	General	SupportHub AI Assistant operates 24/7 with instant responses (<1 minute). Human support agents are available Monday through Friday from 9 AM to 6 PM EST with average response times under 15 minutes.	64	28	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-05 16:03:56.671984	2026-08-05 16:03:56.672054	[-0.010482517,0.0091576865,-0.00023541904,-0.075867325,-0.006165802,0.021525681,0.0051850467,0.0075358613,-0.003407351,-0.005233116,0.0027712511,-0.009863068,-0.003986975,-0.008333804,0.12601872,0.007058517,0.016489163,-0.006054232,-0.008980911,-0.0133399945,0.014975001,0.0092197,0.0034957777,-0.0071574226,-0.009328991,-0.010055349,0.018018832,-0.004165978,-0.0020908697,0.035463076,-0.0046432707,-0.0013401586,0.009327386,0.015777629,0.010081832,0.011399569,0.008225125,0.0065824836,-0.0040686154,0.025917003,0.019986393,0.014186313,0.0025166697,0.0039397003,-0.008185508,0.006415069,-0.013489745,-0.036811728,-0.023661809,0.029318918,-0.009559295,-0.0045419955,0.005976292,-0.23623407,0.013866171,0.0052838805,-0.00037225953,0.005797736,-0.012048246,-0.031202061,-0.011907351,0.010497534,-0.005032427,-0.023457333,0.0030269204,-0.009832754,0.013444033,0.03439851,0.033309154,0.02782077,-0.012235288,-0.0008762421,-0.00215514,-0.0068323775,-0.019451313,-0.01141245,0.0010905862,0.009378707,-0.013056334,-0.015030347,0.013639785,0.00031223212,-0.00067892106,-0.008392698,0.013093152,-0.014516949,-0.0032814208,0.013765962,-0.0100537995,-0.016652929,-0.0034372155,0.011651933,-0.00468414,-0.017264115,0.0153130675,-0.01611101,-0.009757954,0.01802323,-0.0050418866,-0.010951318,0.010985945,-0.014027279,0.003609277,0.015387559,-0.00096473505,0.008154361,0.0031353775,-0.012273728,-0.009272073,0.0013566848,0.019860897,0.019086836,-0.0028420018,0.0012561585,0.0014345613,-0.17927128,0.014720601,-0.0011898255,0.020599307,-0.0013460409,-0.03343499,0.009166387,-0.0027022753,0.021867638,0.0094808135,-0.017852604,0.011504689,-0.0024635224,0.0047833067,0.024008494,-0.0050462154,-0.0071949707,0.0025219857,-0.01123677,0.008423554,0.006653554,-0.028611174,0.032810945,0.023645926,-0.01612555,0.011894961,0.016932372,0.024254289,-0.007909652,-0.010854139,0.009843709,0.014273892,0.021249037,0.013771667,-0.022797748,-0.010080101,-0.005217874,0.007320663,-0.012515798,0.008267959,-0.018265389,0.010308779,0.003380636,-0.0042806584,0.005724389,-0.00052146224,-0.008292559,-0.014061807,-0.0008454992,0.0048085926,0.01731819,-0.010745083,0.02944579,-0.012006426,0.007389283,-0.0037230537,-0.005648973,-0.00062464154,-0.0042717555,-0.011671474,0.00952432,0.006725221,-0.013822062,0.014805083,-0.027523156,-0.0075587113,0.028562304,-0.021033019,-0.0170107,-0.0029515964,0.01523861,0.013834568,-0.0016181672,-0.018397655,-0.013641138,0.014884099,-0.010596011,0.007746699,-0.010683186,0.009070884,-0.008727376,-0.013434269,0.024094503,0.011836906,0.015485566,0.020739175,-0.011559951,0.023915172,-0.005465663,-0.0046268664,0.009384225,-0.001010367,-0.011366343,0.0038733499,-0.010688979,-0.0013423971,-0.011163065,-0.007948551,-0.0008681069,0.006880659,-0.017907368,0.011527968,-0.0031350362,0.014935951,-0.023801045,-0.0034912701,-0.005489718,-0.0013393689,-0.003913197,0.022658622,-0.0015091511,-0.014529803,-0.0101990765,0.012402232,0.015304939,0.009432833,0.0143031115,0.0074761338,-0.0011473986,-0.020882217,-0.00930313,-0.01061229,0.0035059177,0.029405374,0.0093825525,-0.021085335,-0.004821619,-0.005855868,0.0067756115,0.02049941,-0.030098943,0.02306717,-0.034150347,0.008769663,-0.0033341881,0.015389423,0.025742702,-0.0006236761,0.001780567,-0.025012089,0.01022314,-0.0210114,0.0058152,-0.0053646695,-0.0023315027,-0.010598183,-0.01132204,-0.02191328,-0.009682374,0.0021584784,0.00045121176,-0.0046041855,0.0023398828,0.004484721,-0.00032872544,-0.003495425,-0.0017988933,-0.004961879,0.004518802,0.002925405,-0.008902351,-0.055460252,0.013400023,0.01435528,-0.022518516,0.00060701126,0.00096328784,-0.02618334,-0.022603435,-0.02771398,0.019643571,-0.028360248,-0.006717503,-0.0054349317,-0.019019475,0.026447535,0.00429491,-0.0051656696,0.009960297,-0.007466572,-0.0069896793,-0.0067626564,-0.003168123,0.009934241,-0.025438568,0.0036748245,-0.009503757,-0.017035745,0.01947921,-0.018401373,0.022995992,0.0085591255,0.019855296,0.009561165,0.0019229649,0.00092785875,-0.015388844,-0.003734961,-0.012689921,0.00032488795,-0.008204412,-0.0036470855,-0.00060930237,0.009178289,-0.0071295747,-0.002621021,-0.010882403,-0.017804924,0.014089008,-0.021335434,-0.02567064,0.021685181,0.016246695,0.015053874,-0.020398991,-0.00021119179,-0.019584041,0.025738785,-0.005884294,-0.0019719787,0.02253,0.017258387,-0.0032712626,-0.006247493,0.007907313,0.01702603,0.005284302,-0.0062450976,0.01626017,0.0023409654,0.019167392,-0.00466767,0.0013090749,-0.0020482761,-0.039900444,-0.004913527,0.0055212155,0.010145484,-0.010761047,-1.1547143e-05,0.0018168382,-0.013133925,0.0068566934,-0.013772985,0.018944927,-0.0025898232,0.01488341,-0.0010539017,-0.024298742,-0.0046651466,-0.004449642,-0.0027155248,-0.0028658593,0.007911413,-0.016784355,0.012716249,-0.009759907,-0.009209694,0.006723875,-0.009469704,-0.0023813513,-0.008543076,-0.004075231,-0.005683089,0.004299353,-0.008874551,0.039234787,0.024369491,-0.013835286,-0.018821621,6.4398984e-05,0.009537632,0.02453016,-0.0031797364,0.009650358,0.020082988,0.0069639296,-0.006875778,-0.005194901,-0.027737947,-0.002099197,-0.011033603,0.0012738233,0.003952803,0.010185354,-0.00090296025,0.013320902,-0.01409752,0.026570585,0.023350606,-0.023907837,0.0032476878,0.0029521557,0.023439694,-0.0045652487,0.0031493106,0.0077563943,-0.0052732225,0.010781029,0.0026398958,-0.0052842596,-0.008920943,0.003501949,-0.0031594916,-0.003743432,-0.020278694,0.009562615,0.0074593723,0.032995388,-0.026359158,0.0029839852,-0.010467661,-0.013974674,0.020710813,0.01848274,-0.01191144,0.0004622873,-0.032695763,0.0062856223,-0.0014250457,-0.036594037,0.012005668,0.0011709314,-0.003813521,0.008610722,-0.001849009,0.019307358,0.0035648823,0.007050373,-0.0078921,-0.005041687,0.013158448,-0.012728606,-0.0013191035,-0.0087685725,0.024652475,0.004560852,0.027185928,-0.01548983,-0.0023051298,0.012592068,-0.02314427,-0.0028120878,0.0052065765,0.011463123,-0.023940811,-0.009252169,-0.004037283,-0.0027454272,0.008816736,0.005527276,0.00020221365,-0.015650967,0.019575015,0.03594404,-0.014579638,0.0032179812,-0.013721181,0.0067821327,-0.017603971,-0.017497174,0.0018264818,-0.0020098968,0.01082489,0.013376189,0.022835258,-0.0031726668,-0.008282524,0.0064262627,0.015387698,0.0024973415,-0.0010973685,-0.0019506665,0.0061955955,-0.011289878,0.016247068,0.0072540133,-0.00064725603,0.0008268567,-0.013437472,-0.006605451,0.009626296,-0.0017012988,-0.028265372,0.014312557,0.014670537,0.0063392255,-0.049209006,0.022150412,-0.007223341,0.004991295,0.0028475518,-0.012308047,0.00716614,0.016097503,-0.009557623,0.010651112,0.017794,0.0077032484,0.0046323165,0.0031017293,-0.0055767572,-0.012206241,0.019850165,0.009887382,-0.02167235,0.0031675214,-0.014681923,0.03165249,0.0030066539,-0.018469539,0.0017995154,-0.0028423502,0.01590191,0.027742552,-0.017976917,0.022581419,-0.022044934,-0.0074114176,-0.00095042016,-0.0021090878,-0.003858433,0.022454057,0.0065897373,0.0019021428,-0.013230383,-0.026306137,-0.008118932,0.028806224,-0.0059532276,-0.059927892,0.020249117,0.0073723593,-0.0016767137,-0.012064355,0.02216674,-0.0022949423,-0.010976118,0.0074586435,-0.013513809,-0.0041512325,0.010333794,0.0016246402,4.7143612e-06,-0.0021151863,-0.009405717,0.0034768672,0.013325449,-0.02911188,0.002320212,0.021585977,-0.0013428123,0.012938658,-0.0061288606,0.0050824336,-0.0010528632,0.009737214,0.0024567568,-0.0018224295,-0.0054136547,0.005462144,-0.010078306,-0.00038296607,0.0025428724,0.0116461,-0.004529187,0.006565354,-0.03592071,-0.009709008,0.030735642,-0.026348682,-0.0071732374,-0.014135801,-0.017636294,-0.007215021,0.003287897,0.028447963,-0.027188718,0.0039560753,0.0047632563,-0.048483286,0.0039027412,-0.002853639,-0.024503903,0.0019316833,0.011496258,-0.00067076983,0.00024040206,-0.0010594004,-0.014370603,-0.01787323,0.006152263,0.0030005272,0.027136208,-0.013834418,-0.002009839,-0.006963933,-0.0004557337,0.011601393,-0.0038549781,-0.011312105,-0.009170065,-0.031189969,0.009124654,-0.005581142,0.017602062,-0.011145728,0.007825041,0.003113237,-0.005457029,0.009583369,-0.029061466,-0.060857214,-0.016202534,0.019479077,0.0060501345,-0.0012899315,0.006740665,0.00027871292,-0.012466883,0.006240905,0.0146556655,-0.0024530517,0.00021212394,0.009294798,-0.004916907,-0.0068953643,0.007479747,0.024399439,-0.015416551,0.018072924,-0.021912258,0.00324251,-0.0031928022,0.017466204,-0.00910092,-0.002715536,0.021855034,0.009365322,0.008247039,0.004851575,-0.012159246,-0.0047116308,-0.20763311,0.008641231,0.013227214,0.0082269125,0.0029326174,0.0083463695,-0.017058799,0.022577638,-0.023778073,-0.003323071,0.00071033224,-0.016955532,-0.032628193,0.0023055635,0.0013490247,0.1505719,-0.01316507,0.0037517215,-0.029377488,0.0059420196,-0.0042388053,0.001111239,0.014801234,0.012249381,-0.011589658,0.0071505103,0.021574931,0.0029289396,0.0089357,0.020781983,0.005655124,0.01142186,0.004503028,-0.012020092,0.008566887,-0.0039568204,0.0062488182,-0.009720824,-0.0026415798,-0.016960798,0.026175762,-0.011275199,-0.019919164,0.0020298269,-0.008517387,-0.009240693,-0.007137999,0.0019709428,-0.025395561,0.008894897,-0.020608764,-0.08618104,-0.0012389993,-0.008245642,0.015317934,0.00568484,-0.008260904,-0.013329652,0.014049164,-0.017887129,0.01407209,-0.0026765915,-0.010891801,0.01914919,-0.015384887,-0.0073001054,0.011401823,0.006844826,0.022781657,0.005362674,0.029373856,0.016743042,-0.0036677138,0.002644613,0.008181747,-0.009480764,0.016179206,-0.00026799072,0.007863353,-0.011912098,0.00087291456,-0.0003226999,0.0058388957,0.004139103,-0.012120744,-0.0067658033,-0.010488096,0.02441958,0.021112602,-0.009711023,-0.012383434,-0.006145392,0.03406011,0.0062872646,-0.013010606,-0.0040322067,0.00897383,0.011700082,0.013027994,0.018341996,0.00979739,-0.014667347,0.02518783,0.0056716087,0.0018058078,0.017202592,0.021166611,0.0048387498,0.0122707095,-0.0046868008]
e0c6bad0-d11b-414a-b773-35cdb5434a76	Test Policy on Hardware Returns	Returns & Refunds	Customers can return hardware products within 14 days of receipt with all original accessories intact.	0	0	t	c64e3806-b382-4689-9f1a-94114205ce5f	2026-09-09 15:12:54.976203	2026-09-09 15:12:54.97662	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0.16903085,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0.16903085,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0.3380617,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16903085,0,0,0,0,0,0.16903085,0,0,0,0,0,0,0,0,0,0,0,0]
\.


--
-- Data for Name: kb_chunk_embeddings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kb_chunk_embeddings (id, chunk_id, source_id, source_type, title, category, content, embedding, created_at) FROM stdin;
6a7ceaf5-3d2e-4219-acdf-1d412cbd1fee	POL-001_chunk_0	POL-001	policy	ShopKart Return Policy	Return	# ShopKart Return Policy\n\n### 1. General Return Window\nShopKart offers a return window on eligible items delivered to customers in India:\n- **Electronics & Mobiles:** 7 calendar days from delivery date.\n- **Home & Kitchen Appliances:** 7 to 10 calendar days from delivery date.\n- **Fashion & Footwear:** 15 calendar days from delivery date.\n- **Large Furniture:** 10 calendar days from delivery date.	[0,0,0.14547859,0,0,0,0,0,0,0,0,0,0,0,0,0,0.29095718,0,0,0,0,0,0,0,0,0,0,0,0,0,0.29095718,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0.29095718,0,0.072739296,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0.072739296,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0.072739296,0,0,0,0.072739296,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0.14547859,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2182179,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0.072739296,0,0,0.072739296,0,0,0,0,0,0.072739296,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0.072739296,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0.29095718,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14547859,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2182179,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0.072739296,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14547859,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0.072739296,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0.29095718,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0.29095718,0,0,0,0.072739296,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.29095718,0,0,0,0,0,0,0,0,0,0,0,0.072739296,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.056643
08db7538-86b7-4f21-ac8c-a518de0f79c5	POL-001_chunk_1	POL-001	policy	ShopKart Return Policy	Return	### 2. Return Eligibility & Conditions\nTo qualify for a full return:\n- Products must be in original condition with all manufacturer tags, serial numbers, barcodes, warranty cards, and accessories intact.\n- Items must not show signs of physical abuse, unauthorized modification, or water damage.\n- Original packaging box and user manuals must be returned with the product.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0.1933473,0,0.1933473,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1933473,0,0,0,0,0,0.09667365,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.29002094,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0.09667365,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0.09667365,0,0,0,0.1933473,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.29002094,0,0,0.1933473,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0.09667365,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0.09667365,0,0.09667365,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0.1933473,0,0,0,0.09667365,0,0,0,0.09667365,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0.09667365,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0.09667365,0,0,0.09667365,0,0,0,0.09667365,0,0,0,0,0,0.09667365,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0.09667365,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0.09667365,0,0,0,0.09667365,0.09667365,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0]	2026-09-09 15:50:11.057776
6d3f8c7f-195e-4fef-8626-c5b20c8a3b0d	POL-001_chunk_2	POL-001	policy	ShopKart Return Policy	Return	### 3. Non-Returnable Items\nFor health, safety, and hygiene regulations, the following items are strictly non-returnable:\n- Personal hygiene items, innerwear, socks, and lingerie.\n- Oral care products (e.g. electric toothbrushes, replacement brush heads).\n- Cosmetics, skincare serums, perfumes, and opened beauty formulations.\n- Clearance or discontinued products explicitly flagged as 'Final Sale / Non-Returnable'.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0.09853293,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0.19706586,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0.09853293,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0.29559878,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0.19706586,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0.19706586,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0.19706586,0.09853293,0,0,0,0,0.09853293,0,0,0,0.09853293,0,0.09853293,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0.09853293,0,0,0.09853293,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0.19706586,0.09853293,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0.09853293,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0.29559878,0,0,0,0,0,0,0,0,0,0,0,0,0.19706586,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0.09853293,0,0,0.09853293,0,0,0,0,0,0,0,0,0.09853293,0,0.09853293,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.058171
73e0927a-b1aa-48a5-9e23-76238d9661ed	POL-001_chunk_3	POL-001	policy	ShopKart Return Policy	Return	### 4. Return Pickup & Inspection Process\n- Once a return request is submitted in the ShopKart app/website, a logistics agent will be assigned for doorstep pickup within 24–48 business hours.\n- A physical verification checklist will be performed by the field agent prior to accepting the package.\n- If verified successfully, the return status moves to 'PICKED_UP' and the corresponding refund is automatically initiated.	[0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0.19900744,0,0,0.19900744,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0,0,0,0,0.29851115,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.19900744,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0.19900744,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0.19900744,0,0,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0]	2026-09-09 15:50:11.058435
0fd4f12e-5097-4e64-84e1-b376d5e538c9	POL-002_chunk_0	POL-002	policy	ShopKart Refund Policy	Refund	# ShopKart Refund Policy\n\n### 1. Initiation Timelines\n- **Pre-dispatch Order Cancellations:** Refund initiated immediately upon cancellation approval.\n- **Doorstep Returns:** Refund initiated within 2 to 4 hours of the courier partner completing physical pickup.\n- **Warehouse Returned Items:** Refund initiated within 24 hours of warehouse quality check clearance.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0.09667365,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0.09667365,0,0,0.09667365,0.09667365,0,0,0,0,0,0.1933473,0.09667365,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0.1933473,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0.09667365,0,0.09667365,0,0,0.09667365,0.09667365,0,0,0,0.09667365,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0.09667365,0,0,0,0,0,0,0.1933473,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0.09667365,0,0,0.09667365,0,0,0,0,0,0.09667365,0,0.09667365,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0.09667365,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0.29002094,0.09667365,0,0,0,0,0,0,0,0,0,0,0.3866946,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1933473,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.29002094,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09667365,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1933473,0,0,0]	2026-09-09 15:50:11.058669
d913b11f-bd66-44e5-a166-3f71d14db74b	POL-002_chunk_1	POL-002	policy	ShopKart Refund Policy	Refund	### 2. Refund Settlement Timelines by Payment Method\n- **UPI (Google Pay, PhonePe, Paytm, BHIM):** 2 to 24 hours (usually instantaneous).\n- **ShopKart Wallet / Instant Store Credit:** Instantaneous (0 to 15 minutes).\n- **Credit Cards & Debit Cards (Visa, Mastercard, RuPay):** 3 to 5 business banking days.\n- **Net Banking (All major Indian banks):** 3 to 7 business banking days.\n- **Cash on Delivery (COD) Orders:** Processed via customer-provided UPI VPA or NEFT/IMPS bank account within 24 to 48 hours after return pickup.	[0,0,0,0,0,0,0,0,0,0.14948702,0,0,0,0,0,0,0.22423053,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0.22423053,0,0,0.07474351,0,0,0.14948702,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0.07474351,0,0,0.07474351,0,0,0,0,0,0.14948702,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0.07474351,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14948702,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0.14948702,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0.07474351,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0.14948702,0,0,0,0,0,0,0.07474351,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0.07474351,0,0,0,0,0.07474351,0,0.07474351,0.07474351,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14948702,0,0.07474351,0,0,0,0,0,0,0,0.07474351,0,0,0,0.07474351,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14948702,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0.07474351,0,0,0,0,0,0.14948702,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0.07474351,0,0.07474351,0,0,0,0.07474351,0,0,0,0.07474351,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0.07474351,0.14948702,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0.14948702,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0.07474351,0,0,0.14948702,0,0,0,0,0,0,0,0,0,0,0.22423053,0.14948702,0,0,0,0,0,0.07474351,0,0,0.07474351,0,0,0,0,0,0.07474351,0,0.07474351,0.07474351,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0.07474351,0,0,0,0.07474351,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14948702,0,0.07474351,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14948702,0,0.07474351,0,0,0,0,0.07474351,0,0.07474351,0,0,0.07474351,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0.07474351,0,0.14948702,0,0,0,0,0,0,0,0,0,0,0,0,0.14948702,0,0,0,0,0.07474351,0,0,0,0.07474351,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0.07474351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14948702,0,0,0,0,0.07474351]	2026-09-09 15:50:11.058863
31d185ce-f007-4a27-b233-88df3f7ed13e	POL-002_chunk_2	POL-002	policy	ShopKart Refund Policy	Refund	### 3. Failed Refund Handling\nIf a refund fails due to an invalid UPI handle, closed bank account, or payment gateway timeout:\n- SupportHub will notify the customer via SMS/Email to update their bank/UPI details in the Account section.\n- The automated payment retry engine re-attempts the transaction within 24 hours of updated beneficiary details.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0.09407209,0,0,0,0,0,0,0.09407209,0,0,0,0.09407209,0,0.09407209,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18814418,0.09407209,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0.18814418,0,0,0.18814418,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18814418,0,0,0,0,0.09407209,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0.28221625,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18814418,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0.09407209,0,0,0.09407209,0,0,0,0,0,0,0.09407209,0,0.09407209,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18814418,0,0,0,0,0,0,0,0,0.18814418,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0.09407209,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0.09407209,0,0,0.18814418,0.18814418,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0.09407209,0.09407209,0,0.18814418,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0.18814418,0.09407209,0,0,0,0,0.09407209,0,0,0,0.09407209,0.09407209,0,0,0.09407209,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09407209,0,0.09407209,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.059056
fd775add-3e8d-46c9-b6f1-2dafcc70c3b6	POL-003_chunk_0	POL-003	policy	ShopKart Order Cancellation Policy	Cancellation	# ShopKart Order Cancellation Policy\n\n### 1. When Cancellation is Allowed\n- Customers may cancel an order free of charge at any time while the order status remains **PLACED** or **CONFIRMED**.\n- Self-service one-click cancellation is accessible directly from 'My Orders'.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0.120385855,0,0,0,0,0,0.120385855,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0.24077171,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.36115757,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.36115757,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0.120385855,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0.120385855,0,0,0,0.120385855,0,0,0.120385855,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0.120385855,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0.120385855,0,0,0.120385855,0,0,0.120385855,0,0,0,0,0.120385855,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.059237
4afdbc72-7612-4d3a-970a-c8af35bd4931	POL-003_chunk_1	POL-003	policy	ShopKart Order Cancellation Policy	Cancellation	### 2. When Cancellation is Blocked\n- Once an order reaches **PACKED**, **SHIPPED**, or **IN_TRANSIT**, self-service online cancellation is automatically locked because warehouse logistics and courier manifests have been generated.\n- In such cases, customers should refuse delivery at their doorstep when the courier agent arrives, or initiate a standard return post-delivery.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20965697,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0.104828484,0,0.104828484,0,0,0,0,0,0,0,0,0.104828484,0,0,0.104828484,0,0,0,0.20965697,0,0,0,0,0,0.104828484,0,0.104828484,0,0,0,0,0.104828484,0,0,0,0,0.104828484,0,0,0,0,0.20965697,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0.20965697,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0.104828484,0,0,0,0,0,0,0.104828484,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0.104828484,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0.104828484,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20965697,0,0,0,0,0,0,0,0,0,0,0.20965697,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0.104828484,0,0,0,0,0,0,0,0,0.20965697,0.104828484,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0.104828484,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20965697,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0.104828484,0.104828484,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0.104828484,0,0,0.104828484]	2026-09-09 15:50:11.059421
c2b50e1b-b0a4-42ea-a0fd-a66cfbd56304	POL-003_chunk_2	POL-003	policy	ShopKart Order Cancellation Policy	Cancellation	### 3. Merchant / Platform Cancellations\nShopKart reserves the right to cancel orders in rare situations such as:\n- Item discovered to be damaged or out of stock during pre-dispatch warehouse quality inspection.\n- Incomplete or unserviceable delivery address pincode.\n- Flagged security alerts or suspected unauthorized payment transactions.	[0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0.10846523,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.21693046,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0.10846523,0.10846523,0,0,0,0,0,0,0.21693046,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0.10846523,0,0.21693046,0,0,0,0.10846523,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0.10846523,0.10846523,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0.21693046,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0.32539567,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0.10846523,0,0,0.10846523,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0,0,0]	2026-09-09 15:50:11.059595
2884767b-263d-47be-8d4e-89844f2a2765	POL-004_chunk_0	POL-004	policy	ShopKart Shipping and Delivery Policy	Shipping	# ShopKart Shipping and Delivery Policy\n\n### 1. Standard Delivery Timelines\n- **Metro & Tier-1 Cities (Bengaluru, Mumbai, Delhi NCR, Hyderabad, Chennai, Kolkata, Pune):** 2 to 4 calendar days.\n- **Tier-2 & Tier-3 Cities:** 4 to 7 calendar days.\n- **Special / Remote Regions (Northeast, J&K, Island territories):** 7 to 10 calendar days.	[0,0,0,0,0,0,0,0,0,0,0,0,0.20739034,0,0,0,0.20739034,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0.31108552,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0.10369517,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0.20739034,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0.10369517,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0.10369517,0.10369517,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0.10369517,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0.31108552,0,0,0,0,0.20739034,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0.10369517,0.10369517,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0,0,0.10369517,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0.10369517,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.31108552,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0.10369517,0.10369517,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.059763
e04b1419-6ee0-4e7e-80d1-62ef915f1648	POL-004_chunk_1	POL-004	policy	ShopKart Shipping and Delivery Policy	Shipping	### 2. Logistics & Courier Partners\nOrders are fulfilled via verified tier-1 logistics networks including Delhivery, BlueDart, Ecom Express, Shadowfax, and XpressBees. Live real-time tracking links are provided via SMS and order details.	[0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.26967993,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0.26967993,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.060662
f452a4ae-f5ac-4499-9e37-39dd355f8736	POL-004_chunk_2	POL-004	policy	ShopKart Shipping and Delivery Policy	Shipping	### 3. Delivery Delays & Exceptions\nUnforeseen delays may occur due to severe weather conditions (monsoons, floods), transit hub congestion, regional holidays, or transportation strikes. Customers receive automated tracking alerts whenever transit status updates to 'DELAYED'.	[0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0.2309401,0,0,0.2309401,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0.11547005,0,0.11547005,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2309401,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0.11547005,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0.2309401,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2309401,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0.11547005,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0.2309401,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0.11547005,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0.2309401,0,0,0,0,0,0,0,0,0.11547005,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0.11547005,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.06085
701255b7-ee77-402a-99eb-88af373660b7	POL-004_chunk_3	POL-004	policy	ShopKart Shipping and Delivery Policy	Shipping	### 4. Delivery Address Changes\n- Delivery addresses may be modified only while the order is in **PLACED** or **CONFIRMED** status.\n- Once dispatched, address changes cannot be accommodated due to courier waybill locking.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0.13483997,0,0]	2026-09-09 15:50:11.061034
6e714ca7-90ba-4ff8-84c8-dccae0f70c64	POL-005_chunk_0	POL-005	policy	ShopKart Warranty Policy	Warranty	# ShopKart Warranty Policy\n\n### 1. Manufacturer Warranty\n- All branded electronics, home appliances, IT peripherals, and audio equipment sold on ShopKart carry official manufacturer brand warranty (typically 1 to 3 years as specified on the product page).\n- The official tax invoice downloaded from the ShopKart order page serves as the valid proof of purchase.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0.19706586,0,0.19706586,0,0,0,0,0,0,0.09853293,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0.19706586,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0.09853293,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0.09853293,0.09853293,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0.19706586,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0.09853293,0,0,0.29559878,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0.09853293,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.19706586,0.09853293,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0.39413172,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.19706586,0,0.09853293,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0.19706586,0,0,0,0,0,0,0.09853293,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0.09853293,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09853293]	2026-09-09 15:50:11.061201
90d83f78-df4d-4539-9b50-928ffefcbe21	POL-005_chunk_1	POL-005	policy	ShopKart Warranty Policy	Warranty	### 2. Scope of Warranty Coverage\n- **Covered:** Inherent manufacturing defects, internal component failure, electrical circuit malfunction under normal usage.\n- **Excluded:** Accidental damage, liquid spills, cracked screens, physical abuse, unauthorized third-party repairs, normal cosmetic wear and tear.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.24433888,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0.12216944,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.24433888,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0.12216944,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0.12216944,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0.12216944,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0.12216944,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0.12216944,0,0,0,0,0.12216944,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0.12216944,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0.12216944,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12216944,0,0,0,0,0.12216944,0,0.12216944,0,0,0.12216944,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.06136
46f8f1c3-f518-4e54-bbbd-49a9bdac5957	POL-005_chunk_2	POL-005	policy	ShopKart Warranty Policy	Warranty	### 3. Onsite vs. Carry-in Service\n- **Large Appliances & Televisions:** Supported by authorized brand technician onsite home visits.\n- **Mobiles, Audio & Peripherals:** Supported via authorized brand service centers across India.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.25607377,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0.25607377,0,0,0,0,0.25607377,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0.25607377,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.25607377,0,0,0,0,0,0,0,0,0,0,0,0.25607377,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.061519
7319760d-abab-4fc2-a89e-8cc47985cd1a	POL-006_chunk_0	POL-006	policy	ShopKart Replacement Policy	Replacement	# ShopKart Replacement Policy\n\n### 1. Replacement Eligibility\nIf a delivered product is damaged in transit, defective, or missing accessories, customers may opt for a free replacement instead of a refund within the designated return window.	[0,0,0.25607377,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0.12803689,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.38411063,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.25607377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0.12803689,0,0,0,0.12803689,0.12803689,0,0,0.12803689,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0.12803689,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0.12803689,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0.25607377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.06168
da30cd51-01a6-4465-bc1b-7a5445cc14f0	POL-006_chunk_1	POL-006	policy	ShopKart Replacement Policy	Replacement	### 2. Conditions for Replacement\n- Replacement is subject to seller inventory availability.\n- The replacement unit will be dispatched as soon as the original unit is picked up and verified by the logistics agent.\n- If the required replacement SKU is out of stock, an automatic full refund will be processed.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.21952853,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0.10976426,0,0,0,0,0,0.10976426,0,0,0,0.10976426,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0.10976426,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.43905705,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0.10976426,0.10976426,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.21952853,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.21952853,0,0,0,0,0.32929277,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0.10976426,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0,0,0,0,0,0,0,0,0,0.10976426,0,0,0,0.10976426,0.10976426,0,0]	2026-09-09 15:50:11.06183
cef9b66b-4d1a-44a8-b9de-274eb433663e	POL-007_chunk_0	POL-007	policy	ShopKart Exchange Policy	Exchange	# ShopKart Exchange Policy\n\n### 1. Fashion & Footwear Size Exchanges\n- Customers purchasing apparel or footwear may request a free size exchange (e.g. Size M to Size L, or UK 8 to UK 9) within 15 days of delivery.\n- Size exchanges do not incur additional shipping or handling fees.\n\n### 2. Exchange Fulfillment\n- The courier agent delivers the new size and picks up the existing size during the same delivery attempt (Doorstep Exchange).	[0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14865883,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0.07432941,0,0,0,0,0.07432941,0.07432941,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0.07432941,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0.07432941,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0.14865883,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0.07432941,0.07432941,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14865883,0,0,0,0.52030593,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0.22298825,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0.14865883,0,0.07432941,0,0,0,0,0.07432941,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0.07432941,0,0,0,0,0.07432941,0,0.07432941,0,0,0,0,0.07432941,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0.07432941,0,0,0,0,0,0,0.07432941,0.07432941,0,0,0,0.14865883,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0.07432941,0,0,0,0,0.07432941,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0.14865883,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0.07432941,0,0,0,0,0,0,0.07432941,0,0,0,0.29731765,0.07432941,0,0.07432941,0,0,0,0,0,0,0,0,0.07432941,0,0.22298825,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0.07432941,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07432941,0,0.07432941,0,0,0,0,0,0,0,0,0,0.07432941,0,0,0,0,0,0.07432941,0,0,0,0,0,0,0.07432941]	2026-09-09 15:50:11.062007
c6dad1c6-d903-4cda-b5a5-f17cf95dce5c	POL-008_chunk_0	POL-008	policy	ShopKart Payment Policy	Payment	# ShopKart Payment Policy\n\n### 1. Accepted Payment Modes\n- Unified Payments Interface (UPI) — Google Pay, PhonePe, Paytm, CRED, Amazon Pay, BHIM.\n- Credit Cards & Debit Cards — Visa, MasterCard, RuPay, American Express, Diners Club.\n- Net Banking — 50+ Indian commercial and public sector banks.\n- Digital Wallets — ShopKart Wallet, Paytm, Mobikwik.\n- Cash on Delivery (COD) — Available on orders up to ₹25,000 for serviceable pin codes.	[0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0.08944272,0,0,0,0,0,0.17888544,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0.08944272,0,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0.17888544,0,0.08944272,0,0,0,0.08944272,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0.08944272,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0,0.17888544,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0.08944272,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0.08944272,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0.08944272,0,0,0,0.17888544,0,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0.08944272,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0.17888544,0.08944272,0,0,0,0,0,0,0.08944272,0.08944272,0.08944272,0,0,0,0,0,0.17888544,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.17888544,0,0,0,0,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0.08944272,0.08944272,0,0.08944272,0,0,0,0.08944272,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0.17888544,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0.08944272,0,0,0,0.17888544,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0.08944272,0,0,0,0.08944272,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0.08944272,0.08944272,0,0,0,0,0,0.08944272,0.08944272,0,0,0,0,0.08944272]	2026-09-09 15:50:11.062163
604bcd87-220a-436c-9d2f-b1fbaa79bd55	POL-008_chunk_1	POL-008	policy	ShopKart Payment Policy	Payment	### 2. Payment Security & Encryption\nAll online transactions are encrypted via 256-bit SSL protocols and processed through RBI-compliant PCI-DSS Level 1 certified payment gateways. Two-Factor Authentication (OTP / UPI PIN) is mandatory.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0.12803689,0,0.12803689,0,0,0.12803689,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.25607377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0.25607377,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.25607377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.38411063,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0.12803689,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.12803689,0,0,0,0,0,0,0.12803689,0,0.12803689,0,0,0,0.12803689,0,0,0,0,0,0.12803689,0,0]	2026-09-09 15:50:11.062308
0598e5e8-2f18-458b-a8ae-849f5ad36512	POL-008_chunk_2	POL-008	policy	ShopKart Payment Policy	Payment	### 3. Duplicate Deductions & Gateway Timeouts\nIf money is deducted from your bank account but your order is not confirmed due to a network interruption, the payment gateway auto-reverses the transaction within 24 to 48 banking hours.	[0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0.26967993,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0]	2026-09-09 15:50:11.06247
ca2cc780-4799-425d-a609-1c60e0ba0593	POL-009_chunk_0	POL-009	policy	ShopKart Account Management Policy	Account	# ShopKart Account Management Policy\n\n### 1. Profile & Information Updates\nCustomers can manage saved shipping addresses, primary email IDs, and phone numbers via the Account Settings portal.	[0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2981424,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0.1490712,0,0.1490712,0,0,0,0,0.1490712,0,0,0.2981424,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0,0.1490712,0,0,0,0,0,0,0,0,0.1490712,0,0,0,0.1490712,0,0]	2026-09-09 15:50:11.062622
465ce7f2-1624-4283-93c4-4dc015868146	POL-009_chunk_1	POL-009	policy	ShopKart Account Management Policy	Account	### 2. Account Security & Verification\n- Changing login mobile numbers or registered email addresses requires OTP verification sent to both previous and new credentials.\n- Multi-factor authentication is recommended for enhanced account safety.	[0,0.13483997,0,0,0,0,0,0,0,0,0,0.26967993,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0.13483997,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0]	2026-09-09 15:50:11.062793
f58e633c-168f-4331-887e-3f630572c9cf	POL-009_chunk_2	POL-009	policy	ShopKart Account Management Policy	Account	### 3. Suspended & Locked Accounts\n- Accounts with repeated fraudulent return claims or policy abuse may be temporarily suspended.\n- In case of suspicious unauthorized logins from unfamiliar devices, accounts are placed in **LOCKED** status to safeguard customer payment data until identity is verified.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0.11250879,0,0.11250879,0,0,0,0,0.11250879,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0.11250879,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0.11250879,0,0.11250879,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0.11250879,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0.11250879,0.11250879,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0.22501758,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0.22501758,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0.11250879,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.22501758,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0.11250879,0,0.22501758,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0.33752638,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0.22501758,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.062989
68c120c0-d50c-4145-99e4-c53855141772	POL-010_chunk_0	POL-010	policy	ShopKart Privacy & Security Policy	Security	# ShopKart Privacy & Security Policy\n\n### 1. Customer Privacy Safeguards\nShopKart strictly protects user privacy. Support agents and automated AI assistants are prohibited from disclosing:\n- Phone numbers, home addresses, or email addresses belonging to other customers.\n- Order details, payment records, or shipment manifests belonging to unrelated accounts.\n- One-Time Passwords (OTPs), CVVs, passwords, or banking credentials under any circumstances.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0.16495723,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0.08247861,0,0,0,0,0,0,0,0,0.08247861,0.08247861,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0.08247861,0,0,0,0,0,0,0,0.08247861,0,0.16495723,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0.24743582,0.08247861,0,0,0,0.08247861,0.08247861,0,0,0,0,0,0,0,0.32991445,0,0,0,0,0,0,0,0,0,0.08247861,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0.08247861,0,0,0,0,0.08247861,0,0,0,0,0.08247861,0,0,0,0,0.08247861,0,0.08247861,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0.08247861,0,0,0,0.16495723,0,0,0,0,0,0,0,0,0.16495723,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0.08247861,0,0.08247861,0,0.08247861,0,0.08247861,0.08247861,0.08247861,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0.16495723,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0.08247861,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0.16495723,0,0,0,0,0,0.08247861,0,0,0.08247861,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0.08247861,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0.24743582,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0.08247861,0,0,0,0,0,0,0,0.24743582,0,0,0,0,0,0.24743582,0,0,0,0,0,0,0,0.08247861,0.08247861,0,0,0,0,0,0,0,0,0,0.08247861,0,0.08247861,0,0,0.08247861,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0,0,0,0,0,0,0,0,0.08247861,0,0,0,0.08247861,0,0.08247861,0,0,0.08247861,0,0,0]	2026-09-09 15:50:11.063157
583447c1-83d9-4fb6-8e22-ace60cc754f9	POL-010_chunk_1	POL-010	policy	ShopKart Privacy & Security Policy	Security	### 2. Reporting Unauthorized Access\nIf you detect unfamiliar order placements, unexpected address changes, or suspect account compromise, contact ShopKart Trust & Safety immediately to freeze account activity and initiate audit logs.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997]	2026-09-09 15:50:11.063314
e38a71b1-677d-47f8-af88-c5139eaf7d19	KA-001_chunk_0	KA-001	knowledge_article	How to Track Your ShopKart Order	Orders	# How to Track Your ShopKart Order\n\nYou can easily check the real-time location and expected delivery schedule of your order:\n\n1. **Via ShopKart App / Website:**\n   - Log in to your ShopKart account and click on **'My Orders'**.\n   - Select the relevant order and click **'Track Shipment'**.\n   - You will see live tracking milestones: *Placed -> Confirmed -> Packed -> Shipped -> In Transit -> Out for Delivery -> Delivered*.	[0,0,0.09325048,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0.37300193,0.09325048,0,0.09325048,0,0,0,0,0.09325048,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18650097,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0.09325048,0,0,0,0,0,0.18650097,0.27975145,0,0,0.09325048,0.27975145,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0.09325048,0.09325048,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0.09325048,0.09325048,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0.18650097,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0.09325048,0,0,0.09325048,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0.18650097,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0.09325048,0,0.09325048,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18650097,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0,0,0,0,0,0,0,0,0,0,0.18650097,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09325048,0.09325048,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.063477
49a80e38-67da-4512-b95d-3f3f5452f119	KA-001_chunk_1	KA-001	knowledge_article	How to Track Your ShopKart Order	Orders	# How to Track Your ShopKart Order\n\n2. **Via Logistics Courier Portal:**\n   - Your shipment details include an Air Waybill (AWB) / Tracking Number and Carrier Name (e.g. Delhivery, BlueDart, Ecom Express).\n   - You can copy the tracking number and visit the courier's official tracking portal for granular checkpoint updates.	[0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0.21693046,0,0,0,0.43386093,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0.10846523,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0.21693046,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.21693046,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0.10846523,0.10846523,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.21693046,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0.10846523,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10846523,0,0,0,0,0,0,0,0,0.21693046,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.063636
6fb9b078-7317-4cbd-a289-4dbe525d9169	KA-001_chunk_2	KA-001	knowledge_article	How to Track Your ShopKart Order	Orders	# How to Track Your ShopKart Order\n\n3. **Status Explanations:**\n   - **In Transit:** Package is on the move between regional fulfillment sorting centers.\n   - **Out for Delivery:** Courier delivery executive has dispatched with your parcel and will attempt delivery today.\n   - **Delayed:** Unforeseen transit delays (weather, high volume). New estimated delivery date will be shown.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0.41039133,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0.10259783,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20519567,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0.10259783,0,0,0,0.10259783,0,0,0,0.10259783,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0.20519567,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0.10259783,0.10259783,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0.10259783,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0.10259783,0,0,0,0,0,0.10259783,0.10259783,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0.20519567,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0.10259783,0.10259783,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0.10259783,0,0.10259783,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0.10259783,0.20519567,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0.10259783,0,0,0,0.10259783,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10259783,0.10259783,0,0,0,0,0,0,0,0,0,0,0.10259783,0,0]	2026-09-09 15:50:11.063792
48dd5b0c-4f0a-4b02-bd3d-a0eacebd1e47	KA-002_chunk_0	KA-002	knowledge_article	How to Cancel an Order Before Dispatch	Orders	# How to Cancel an Order Before Dispatch\n\nIf you changed your mind or placed an order by mistake:	[0,0,0,0,0,0.2,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0.2,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4,0,0,0,0,0]	2026-09-09 15:50:11.063967
2965ee54-3b59-451f-8f2c-23151f0fcbd5	KA-002_chunk_1	KA-002	knowledge_article	How to Cancel an Order Before Dispatch	Orders	### 1. Self-Service Cancellation (Instant)\n- Navigate to **'My Orders'** in your ShopKart profile.\n- If the order status is **PLACED** or **CONFIRMED**, click the **'Cancel Order'** button.\n- Choose your cancellation reason (e.g. *Ordered by mistake, Found cheaper alternative, Expected delivery date too late*) and confirm.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0.11867817,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0.11867817,0,0,0,0,0.11867817,0,0,0.11867817,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.3560345,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0.11867817,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0.11867817,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0.11867817,0,0,0.23735633,0.11867817,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0.11867817,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0.11867817,0,0,0,0.11867817,0,0,0,0.11867817,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0.11867817,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0.11867817,0,0,0,0.11867817,0,0,0.11867817,0,0,0,0,0,0.11867817,0,0,0,0,0,0.11867817,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0.11867817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11867817,0,0,0.11867817,0,0,0,0,0]	2026-09-09 15:50:11.064122
b0d5fffb-6dac-47df-a778-b8d10208a8db	KA-002_chunk_2	KA-002	knowledge_article	How to Cancel an Order Before Dispatch	Orders	### 2. Can I cancel if the order is Shipped?\n- Once an order reaches **PACKED**, **SHIPPED**, or **IN_TRANSIT**, cancellation is locked.\n- Do not worry: Simply refuse the package when the courier executive arrives at your doorstep. The item will automatically return to the seller, and your full refund will be processed.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0.120385855,0,0,0,0,0.120385855,0.120385855,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0.120385855,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0.24077171,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0.120385855,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0.120385855,0,0,0,0.120385855,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0.120385855,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.24077171,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0.24077171,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0.120385855,0.24077171,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0.120385855,0,0,0.120385855,0,0,0,0,0,0,0.120385855,0,0,0,0,0.120385855,0,0,0,0,0,0.120385855,0,0,0,0.120385855,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0.120385855,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.120385855,0,0,0]	2026-09-09 15:50:11.064282
d4b216f1-1930-49c6-bd25-fdab024c9132	KA-003_chunk_0	KA-003	knowledge_article	Step-by-Step Guide to Request a Return	Returns	# Step-by-Step Guide to Request a Return\n\nShopKart offers hassle-free doorstep returns within the eligible product return window:\n\n1. **Initiating the Request:**\n   - Go to **'My Orders'** and select the delivered item.\n   - Click **'Request Return / Replace'**.\n   - Select the accurate reason: *Damaged, Wrong Product, Defective, Size Issue, Quality Issue, or Not as Expected*.\n   - Upload 1–3 clear photos showing the issue, shipping label, and original box.	[0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0.08873565,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0.1774713,0.08873565,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0.08873565,0,0.08873565,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0.08873565,0,0,0.1774713,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0.08873565,0,0.26620695,0.08873565,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0.08873565,0.26620695,0,0,0.08873565,0,0.08873565,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0.08873565,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0.08873565,0.08873565,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0.1774713,0,0,0,0.08873565,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0.08873565,0,0,0.1774713,0,0.08873565,0,0,0.08873565,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0.08873565,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0.1774713,0,0.08873565,0,0,0,0.08873565,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0.08873565,0.08873565,0,0.08873565,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0.08873565,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0.08873565,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26620695,0,0,0,0,0,0.08873565,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1774713,0,0,0.08873565,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0.08873565,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.064455
b51cdf66-e9bb-4313-8a5a-b806255c07ad	KA-003_chunk_1	KA-003	knowledge_article	Step-by-Step Guide to Request a Return	Returns	# Step-by-Step Guide to Request a Return\n\n2. **Doorstep Pickup:**\n   - An authorized courier partner will visit your shipping address within 24 to 48 hours.\n   - Keep the item along with tags, warranty cards, manuals, and original packaging ready for handover.\n\n3. **Refund or Replacement Trigger:**\n   - Once the agent verifies the package condition and marks it 'PICKED_UP', your refund or replacement is initiated automatically.	[0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0.09950372,0.19900744,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0.09950372,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0.09950372,0,0.09950372,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0.09950372,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0.19900744,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0.09950372,0,0,0,0.09950372,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0,0,0,0.19900744,0,0,0,0,0.19900744,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0.09950372,0,0,0,0,0.09950372,0,0.09950372,0.09950372,0,0.19900744,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.19900744,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0.09950372,0]	2026-09-09 15:50:11.06462
9cdf2a5f-501e-4f82-9f5f-9f12dddad0a5	KA-004_chunk_0	KA-004	knowledge_article	Understanding Refund Timelines and Methods	Refunds	# Understanding Refund Timelines and Methods\n\nRefunds are processed automatically as soon as an order is cancelled or a returned product is picked up.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0.18569534,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0.18569534,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.064777
a0276359-157c-410f-ac30-28a4ad988774	KA-004_chunk_1	KA-004	knowledge_article	Understanding Refund Timelines and Methods	Refunds	### Expected Settlement Time by Payment Mode:\n- **UPI (GPay / PhonePe / Paytm / BHIM):** 2 to 24 hours (most credits reflect within 15 minutes).\n- **ShopKart Wallet Balance:** Instant (under 10 minutes).\n- **Credit / Debit Cards:** 3 to 5 business banking days (subject to issuing bank cycle).\n- **Net Banking:** 3 to 7 working days.\n- **Cash on Delivery (COD):** 24 to 48 hours after providing verified bank/UPI details.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.17888544,0,0,0,0,0,0,0.08944272,0,0.08944272,0,0,0,0,0.17888544,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0.17888544,0,0.08944272,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0.08944272,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0.17888544,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.17888544,0,0,0,0.08944272,0,0.08944272,0,0,0,0.08944272,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0.17888544,0,0,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.17888544,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0.08944272,0,0,0,0,0,0,0,0.08944272,0,0,0,0.08944272,0,0,0,0,0,0,0.17888544,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0.08944272,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0.08944272,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0.08944272,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0.08944272,0,0,0,0.08944272,0,0.08944272,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0.17888544,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0.17888544,0,0,0.17888544,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0.08944272,0,0,0,0,0,0,0.17888544,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0.08944272,0,0,0.08944272,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08944272]	2026-09-09 15:50:11.064937
f973462c-f477-4a45-afdd-fc4a63f6cb10	KA-004_chunk_2	KA-004	knowledge_article	Understanding Refund Timelines and Methods	Refunds	### If your refund status shows 'PROCESSING':\nThe transaction has been submitted to the National Payments Corporation of India (NPCI) or Visa/Mastercard network. Please allow the standard bank clearance window.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0.14285715,0.14285715,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0.2857143,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0.2857143,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0.14285715,0,0,0.2857143,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0.14285715,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.14285715,0,0,0,0,0]	2026-09-09 15:50:11.065093
15ce05df-9418-43b0-81f0-1e7c48b5ae2d	KA-005_chunk_0	KA-005	knowledge_article	What to Do When Payment Fails or Money is Deducted	Payments	# What to Do When Payment Fails or Money is Deducted\n\nEncountering an issue during checkout can happen due to bank server timeouts or intermittent network drops:	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0.16439898,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0.16439898,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0.32879797,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16439898,0,0]	2026-09-09 15:50:11.065239
a6b0aa95-f1db-4ddd-b7c5-be190c64ac52	KA-005_chunk_1	KA-005	knowledge_article	What to Do When Payment Fails or Money is Deducted	Payments	### Scenario 1: Money deducted from bank, but order not created (PAY04)\n- This is a temporary gateway drop. The funds are held in the banking clearance pool.\n- The payment gateway automatically detects the orphaned transaction and issues an auto-reversal within **24 to 48 banking hours** back to your original source account.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.22501758,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0.11250879,0,0.22501758,0,0,0.11250879,0.11250879,0,0.11250879,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.22501758,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0.11250879,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0.22501758,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0.11250879,0,0,0,0,0.11250879,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0.11250879,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.22501758,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0.11250879,0,0,0,0,0.11250879,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0.11250879,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11250879,0,0.11250879,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.065394
e281efe5-3f00-4d75-845e-4843341a2647	KA-005_chunk_2	KA-005	knowledge_article	What to Do When Payment Fails or Money is Deducted	Payments	### Scenario 2: Charged twice for a single order (PAY05)\n- If your bank account was debited two times for one order, the secondary transaction is automatically identified as a duplicate and refunded within **3 to 5 banking days**.\n- If not credited after 5 days, provide the 12-digit Bank RRN / Transaction Reference to ShopKart Support for manual settlement acceleration.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0.10050378,0,0,0.10050378,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0,0.10050378,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20100756,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0,0,0,0.10050378,0,0,0.10050378,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20100756,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0.20100756,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0.30151135,0,0,0,0.10050378,0,0,0,0,0,0,0,0.10050378,0.10050378,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20100756,0,0,0,0,0,0,0,0,0.10050378,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0.10050378,0.20100756,0,0,0,0,0.20100756,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0,0,0,0,0.10050378,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20100756,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0]	2026-09-09 15:50:11.065544
3e7ada13-407f-4f8e-b655-1533e4568418	KA-006_chunk_0	KA-006	knowledge_article	What to Do If Your Delivery is Delayed	Shipments	# What to Do If Your Delivery is Delayed\n\nWe aim to deliver every package on or before the estimated delivery date:\n\n1. **Why do delays happen?**\n   - Unforeseen severe weather conditions (monsoons, cyclones, waterlogging).\n   - High volume festival sales causing sorting hub backlogs.\n   - Incomplete customer address or unreachable phone number during delivery attempt.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0.31108552,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0,0.10369517,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0.10369517,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0,0,0.10369517,0.10369517,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0.10369517,0.10369517,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0,0.10369517,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20739034,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0.10369517,0,0,0,0.10369517,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0.10369517,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0.10369517,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0.20739034,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0.10369517,0,0,0,0.10369517,0,0,0,0.20739034,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10369517,0,0,0,0.10369517,0,0,0,0.10369517,0.10369517,0,0,0,0.10369517,0,0,0.10369517,0.10369517,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.065708
b2e8a783-6d60-4af0-9c4e-53ad88f971f8	KA-006_chunk_1	KA-006	knowledge_article	What to Do If Your Delivery is Delayed	Shipments	# What to Do If Your Delivery is Delayed\n\n2. **How to check the revised schedule:**\n   - Open **'Track Shipment'** in the app. The revised estimated delivery date and logistics reason will be updated in real time.\n\n3. **Urgent Delivery Escalation:**\n   - If your shipment has been stuck at a local hub for more than 48 hours with no movement, our AI assistant or support team can raise an automated priority dispatch ticket with the courier partner.	[0,0,0,0,0,0.0860663,0.0860663,0,0,0,0,0,0,0,0.1721326,0,0.2581989,0.0860663,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0.0860663,0,0,0.0860663,0,0,0,0,0,0,0.0860663,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0.0860663,0.2581989,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0.0860663,0,0,0.0860663,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0.0860663,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0.1721326,0,0,0,0,0,0.0860663,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0.0860663,0,0,0,0.0860663,0,0,0,0,0,0.1721326,0.0860663,0,0,0,0,0,0,0,0.1721326,0,0.0860663,0,0,0,0,0,0.0860663,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0.2581989,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0.0860663,0.0860663,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0.0860663,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0.2581989,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0.0860663,0.0860663,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0.1721326,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0.0860663,0,0,0.0860663,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0.0860663,0,0,0,0,0.0860663,0,0,0,0,0,0.0860663,0.0860663,0,0,0,0.0860663,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0,0.0860663,0,0,0,0,0,0,0,0,0.0860663,0,0,0,0,0,0,0,0,0,0,0,0.0860663,0,0.1721326,0,0,0,0,0,0,0,0.0860663]	2026-09-09 15:50:11.065865
aac1f8e2-acbc-47cb-9334-b45274ee1ed4	KA-007_chunk_0	KA-007	knowledge_article	How to Claim Manufacturer Warranty	Warranty	# How to Claim Manufacturer Warranty\n\nAll electronics and brand appliances purchased on ShopKart carry authentic brand manufacturer warranty:\n\n1. **Download Official Proof of Purchase:**\n   - Go to **'My Orders'** -> Select the item -> Click **'Download Tax Invoice'**. The GST invoice serves as the primary warranty certificate.	[0,0,0,0.107211255,0,0,0,0,0,0.107211255,0,0,0,0.107211255,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.32163376,0,0,0,0,0,0,0,0,0,0,0,0.21442251,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0.107211255,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.21442251,0,0,0,0,0.21442251,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0.21442251,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0.107211255,0,0.107211255,0,0.32163376,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0.107211255,0,0.107211255,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0.107211255,0,0,0,0,0.107211255,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0.21442251,0,0,0,0,0,0.107211255,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0.107211255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.066042
ce2e7ad2-06f3-43f1-8102-46654d5f60cc	KA-007_chunk_1	KA-007	knowledge_article	How to Claim Manufacturer Warranty	Warranty	# How to Claim Manufacturer Warranty\n\n2. **Locating Authorized Service Centers:**\n   - Check the product description or warranty card inside the box for the manufacturer's toll-free support helpline or website.\n   - For major brands (Apple, Samsung, Dell, Philips, Boat, Sony), walk into any authorized service center with the device and invoice.	[0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0.104828484,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0.104828484,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0.104828484,0,0,0,0,0.104828484,0,0,0,0,0,0.104828484,0,0.20965697,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0.104828484,0,0,0,0,0,0.104828484,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0.104828484,0,0,0.104828484,0.104828484,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0.104828484,0,0,0,0.104828484,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20965697,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20965697,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0.104828484,0.104828484,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0.104828484,0,0,0.20965697,0,0.104828484,0.104828484,0,0,0,0.104828484,0,0,0,0,0,0.104828484,0,0,0.104828484,0,0,0,0,0,0.104828484,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0.104828484,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0.20965697,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0.104828484,0,0,0,0.20965697,0,0,0,0,0,0,0,0,0,0,0,0.20965697,0.104828484,0,0,0,0,0,0.20965697,0,0,0,0,0,0,0,0,0,0,0,0,0,0.104828484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.066186
d47b5966-e9e5-4a1c-be14-9f990dc528c1	KA-007_chunk_2	KA-007	knowledge_article	How to Claim Manufacturer Warranty	Warranty	# How to Claim Manufacturer Warranty\n\n3. **Onsite Appliance Servicing:**\n   - For TVs, washing machines, and large furniture, call the brand helpline to schedule an authorized technician home visit.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0.31234753,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.31234753,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0.15617377,0,0,0,0,0,0.15617377,0,0,0.15617377,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15617377,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.066336
63008d08-1927-4ec7-9556-065d8380ebc4	KA-008_chunk_0	KA-008	knowledge_article	Product Replacement and Exchange Process	Returns	# Product Replacement and Exchange Process\n\nNeed a different size or received a defective unit? Here is how replacement and exchange work:\n\n1. **Requesting Replacement:**\n   - Select **'Request Return / Replacement'** on your delivered order page.\n   - Select **'Replacement'** if you want the exact same product delivered again due to transit damage or defect.\n   - Select **'Size Exchange'** if you need a different apparel or footwear size.	[0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15762208,0,0,0,0,0,0,0.07881104,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0.23643312,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0.07881104,0,0,0,0,0.07881104,0,0,0,0.07881104,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0.07881104,0,0,0,0.07881104,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15762208,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0.07881104,0,0.07881104,0.07881104,0,0,0,0,0,0,0,0.07881104,0,0,0,0.15762208,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.39405522,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0.15762208,0,0,0,0,0,0,0,0,0,0.23643312,0.07881104,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15762208,0,0,0,0.07881104,0,0,0,0,0,0.07881104,0,0,0,0.07881104,0.07881104,0,0,0,0,0,0,0,0,0.07881104,0.07881104,0.07881104,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.15762208,0,0,0,0.07881104,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0.07881104,0,0,0,0,0.07881104,0,0.15762208,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0.15762208,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0.07881104,0.07881104,0,0,0.07881104,0.07881104,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.23643312,0,0,0,0,0,0,0,0,0,0,0,0,0,0.23643312,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0.07881104,0,0,0.23643312,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0,0,0,0,0,0,0,0,0,0,0,0.07881104,0,0,0.07881104,0,0,0,0,0,0]	2026-09-09 15:50:11.066478
040d4142-66c4-4551-b819-aabce35cf2d0	KA-008_chunk_1	KA-008	knowledge_article	Product Replacement and Exchange Process	Returns	# Product Replacement and Exchange Process\n\n2. **Delivery & Pickup Handover:**\n   - In most metro areas, we support **Doorstep Exchange** — the delivery executive brings your new unit and collects the old one during the same visit.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.066623
c69337c1-fb9e-48f0-995b-0ad0d2711f12	KA-009_chunk_0	KA-009	knowledge_article	Account Recovery and Login Troubleshooting	Account	# Account Recovery and Login Troubleshooting\n\nIf you are experiencing issues accessing your ShopKart account:\n\n1. **Forgot Password:**\n   - Click **'Forgot Password'** on the login screen.\n   - Enter your registered email or mobile number to receive a secure password reset link / OTP.\n\n2. **OTP Not Received:**\n   - Ensure you have cellular network coverage and DND settings do not block transactional SMS.\n   - Click **'Resend OTP via Call / WhatsApp'** after 30 seconds.	[0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0.16609097,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0.08304548,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0.08304548,0,0.08304548,0,0,0.08304548,0,0,0,0.08304548,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0.16609097,0,0,0,0,0,0,0,0.16609097,0,0,0,0,0.08304548,0.08304548,0,0.08304548,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16609097,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0.08304548,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0.08304548,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0.08304548,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0.08304548,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0.08304548,0,0,0.08304548,0,0,0,0,0,0.08304548,0,0.24913643,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0.08304548,0,0,0,0,0,0.16609097,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0.33218193,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0.16609097,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0.08304548,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0.08304548,0.16609097,0,0,0.08304548,0.08304548,0,0.08304548,0,0,0.16609097,0.08304548,0,0,0,0.08304548,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0.08304548,0,0,0,0,0,0,0,0.16609097,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0.08304548,0,0,0.08304548,0.08304548,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.24913643,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.08304548,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.06677
a0064740-300f-44a5-85b7-a975ec529feb	KA-009_chunk_1	KA-009	knowledge_article	Account Recovery and Login Troubleshooting	Account	# Account Recovery and Login Troubleshooting\n\n3. **Account Locked or Suspended:**\n   - If your account was locked due to multiple failed login attempts or security triggers, submit an identity verification request via registered email to `support@shopkart.in`.	[0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0.2309401,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0.11547005,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0.11547005,0,0.11547005,0,0,0,0,0.2309401,0,0,0,0.11547005,0,0,0,0.11547005,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2309401,0,0,0,0,0,0,0.11547005,0.34641016,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0.2309401,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2309401,0,0,0,0,0,0,0,0,0,0.2309401,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0.11547005,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.11547005,0,0.11547005,0,0.11547005,0,0,0,0]	2026-09-09 15:50:11.06694
364a2ad8-ccea-4144-b6ae-87b434483257	KA-010_chunk_0	KA-010	knowledge_article	Reporting Damaged, Broken or Defective Products	Returns	# Reporting Damaged, Broken or Defective Products\n\nIf your package arrives physically broken or damaged:\n\n1. **Report Within 48 Hours:**\n   - Report the damage immediately from **'My Orders'** -> **'Item Damaged on Arrival'**.\n   - Attach clear photographs showing:\n     - The outer cardboard box with the shipping courier label visible.\n     - The damaged part of the product.	[0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.19900744,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0.09950372,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0.09950372,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.39801487,0,0,0.09950372,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0.09950372,0,0,0.09950372,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.19900744,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0.19900744,0,0,0.19900744,0,0,0.09950372,0,0,0.19900744,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0.09950372,0,0,0.09950372,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09950372,0,0,0,0,0,0.09950372,0]	2026-09-09 15:50:11.067107
ed4fb6be-7ca4-43bf-8e07-3d7d2568d172	KA-010_chunk_1	KA-010	knowledge_article	Reporting Damaged, Broken or Defective Products	Returns	# Reporting Damaged, Broken or Defective Products\n\n2. **Priority Resolution:**\n   - For verified transit damages, ShopKart provides expedited zero-cost replacement dispatch or 100% instant refund upon pickup verification.	[0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0.13736056,0.13736056,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.27472112,0,0,0,0.13736056,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0.13736056,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0.13736056,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0.27472112,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.27472112,0,0.13736056,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13736056,0,0,0,0]	2026-09-09 15:50:11.067253
a8b7ab6d-a5c1-40cd-803e-9ef989456e7d	KA-011_chunk_0	KA-011	knowledge_article	What to Do If You Received the Wrong Product	Returns	# What to Do If You Received the Wrong Product\n\nIf you opened your package and discovered an entirely different item, color, or model:	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0.37139067,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18569534,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.067403
dc62f014-3eec-4d42-98da-6cb9766b5df5	KA-011_chunk_1	KA-011	knowledge_article	What to Do If You Received the Wrong Product	Returns	# What to Do If You Received the Wrong Product\n\n1. **Keep Original Packaging Intact:**\n   - Do not discard the box, outer plastic flyer, or courier barcode label.\n2. **Submit a Wrong Item Claim:**\n   - Go to **'My Orders'** -> Select the order -> Choose reason **'WRONG_PRODUCT'**.\n   - Upload photos of the product and barcode tag on the box.\n3. **Expedited Swap:**\n   - Our logistics partner will pick up the incorrect item and dispatch the correct product right away.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0.0873704,0,0,0,0,0,0,0,0,0.1747408,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1747408,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0.0873704,0,0,0,0,0.26211122,0,0,0.0873704,0,0,0,0,0,0.0873704,0.0873704,0.0873704,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0.0873704,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0.0873704,0,0,0.0873704,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0.0873704,0,0,0.0873704,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1747408,0,0,0,0,0,0.1747408,0,0.0873704,0,0.0873704,0,0,0,0,0,0,0.0873704,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0.1747408,0,0,0,0,0,0,0.0873704,0.0873704,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26211122,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0.0873704,0,0,0,0.1747408,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0.0873704,0,0,0,0,0,0,0.0873704,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0.0873704,0,0,0.0873704,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1747408,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0.1747408,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0.0873704,0,0,0,0.1747408,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0.0873704,0.0873704,0,0,0,0.0873704,0,0,0.0873704,0,0,0,0.0873704,0,0.0873704,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0.0873704,0,0.0873704,0,0,0,0,0.0873704,0,0,0.0873704,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0873704,0,0,0,0,0,0.0873704,0,0,0,0,0.0873704,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.067548
024dd69e-431c-4364-8f0b-0fa490231caf	KA-012_chunk_0	KA-012	knowledge_article	What to Do If Order Says Delivered But You Did Not Receive It	Orders	# What to Do If Order Says Delivered But You Did Not Receive It\n\nIf you receive an SMS or notification stating your order was delivered, but you haven't received the package:\n\n1. **Check with Household & Security:**\n   - Often, couriers leave packages with apartment building security guards, reception desks, or neighbors.\n\n2. **Contact Delivery Executive:**\n   - The 'Out for Delivery' SMS contains the delivery agent's direct phone number.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1672484,0,0.2508726,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0.0836242,0,0,0,0.0836242,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0.1672484,0,0,0.0836242,0,0.0836242,0,0,0,0.0836242,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0.0836242,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0.2508726,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1672484,0,0,0,0.0836242,0.1672484,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0.1672484,0,0.0836242,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0.1672484,0,0,0,0,0,0,0,0,0.1672484,0,0,0,0,0,0,0.0836242,0,0.0836242,0.0836242,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1672484,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0.0836242,0,0,0,0,0,0.1672484,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1672484,0,0,0,0,0,0,0.1672484,0,0,0,0,0.0836242,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0.0836242,0,0,0,0.0836242,0,0.0836242,0,0,0,0,0,0.0836242,0,0,0.0836242,0,0,0,0,0,0,0,0,0.0836242,0,0.0836242,0,0,0,0.2508726,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1672484,0.0836242,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0.0836242,0.0836242,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0.1672484,0,0,0,0,0,0,0.0836242,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-09 15:50:11.067693
9e6c7538-8ec1-4df0-91d4-f9e832686fbd	KA-012_chunk_1	KA-012	knowledge_article	What to Do If Order Says Delivered But You Did Not Receive It	Orders	# What to Do If Order Says Delivered But You Did Not Receive It\n\n3. **Raise a Non-Receipt Dispute (Scenario O08):**\n   - If the package is genuinely missing, report the dispute within **24 hours** by clicking **'Didn't Receive Order'** on the order tracking screen.\n   - ShopKart opens an immediate geo-location GPS tag audit with the courier service.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0.10050378,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0.10050378,0,0,0,0,0,0,0,0,0,0.30151135,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20100756,0,0,0.10050378,0,0,0.20100756,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20100756,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.30151135,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0.10050378,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20100756,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.20100756,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0.10050378,0,0,0,0.10050378,0,0,0.10050378,0,0,0.10050378,0,0.10050378,0,0.10050378,0.10050378,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0.10050378,0,0,0,0,0.10050378,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0.10050378,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.10050378,0,0,0]	2026-09-09 15:50:11.06784
1e7361ee-583a-45fd-93cc-9ab1aa51cc48	KA-013_chunk_0	KA-013	knowledge_article	ShopKart Account Security and Anti-Fraud Guidelines	Security	# ShopKart Account Security and Anti-Fraud Guidelines\n\nProtecting your payment methods and private information is our highest priority:\n\n1. **Never Share OTPs or Passwords:**\n   - ShopKart employees and customer support executives will **NEVER** ask for your One-Time Password (OTP), UPI PIN, card CVV, or net banking passwords.\n\n2. **Recognizing Phishing Attempts:**\n   - Official communications originate only from `@shopkart.in` and official verified WhatsApp channels.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0.18033393,0,0,0.18033393,0,0,0,0,0,0,0,0,0.09016696,0.09016696,0,0,0,0.09016696,0,0,0,0,0.09016696,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0.09016696,0,0,0,0,0.09016696,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0.09016696,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0.09016696,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0.09016696,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0.18033393,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18033393,0.09016696,0,0,0.09016696,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0.09016696,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0.09016696,0,0,0,0,0.09016696,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0.09016696,0,0,0.09016696,0.09016696,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0.09016696,0,0.09016696,0,0.09016696,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0.09016696,0,0,0,0,0.09016696,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0.09016696,0,0.2705009,0,0,0,0,0,0,0,0.09016696,0.18033393,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0.18033393,0,0.09016696,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0.09016696,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18033393,0,0.09016696,0,0,0.09016696,0,0,0,0.18033393,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18033393,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.18033393,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0.09016696,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0,0.09016696,0,0,0,0,0,0.09016696,0,0,0,0,0,0,0,0,0,0,0.09016696,0.09016696]	2026-09-09 15:50:11.068037
c3494d35-62df-48ff-9dfd-c84cbf2af147	KA-013_chunk_1	KA-013	knowledge_article	ShopKart Account Security and Anti-Fraud Guidelines	Security	# ShopKart Account Security and Anti-Fraud Guidelines\n\n3. **Reporting Suspicious Activity:**\n   - If you notice unauthorized orders placed or profile modifications, immediately select **'Lock Account'** in Security Settings and contact Trust & Safety.	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0.13483997,0,0.26967993,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.26967993,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0.13483997,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0.13483997,0,0,0.13483997,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.26967993,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0.13483997,0,0.13483997,0.13483997,0,0.13483997,0,0,0,0,0.13483997,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.13483997,0,0,0]	2026-09-09 15:50:11.068196
\.


--
-- Data for Name: macros; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.macros (id, title, body, category, created_by, created_at, updated_at) FROM stdin;
f909067f-511e-4a00-9251-9052c7da7adf	Warm Greeting & Acknowledgment	Hello {{customer.name}}!\n\nThank you for reaching out to SupportHub. I am reviewing your inquiry right now and will assist you step by step.\n\nBest regards,\n{{agent.name}}	General	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-14 12:01:02.126803	2026-08-14 12:01:02.126922
0548ad68-a6ef-4e2d-839d-1a2bbe3380b3	Password Reset Instructions	Hi {{customer.name}},\n\nTo reset your password, please navigate to Settings > Security and click 'Request Password Reset'. A secure verification link will be sent to your registered email address.\n\nLet us know if you need further help!\n{{agent.name}}	Technical	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-14 12:01:02.127131	2026-08-14 12:01:02.127217
5fd9659a-3292-4181-b03e-005a4bcaf964	Invoice & Billing Receipt Dispatched	Hi {{customer.name}},\n\nI have generated and attached the updated tax invoice with your company details. You can also download it at any time from your Billing Dashboard.\n\nBest regards,\nSupportHub Billing Team	Billing	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-14 12:01:02.127379	2026-08-14 12:01:02.127469
a29a11cb-1b46-4e6f-b2d0-dd53bcbd7f5c	Ticket Resolution & Feedback Request	Hello {{customer.name}},\n\nI am glad we were able to resolve your inquiry today. I will mark this ticket as resolved. Please take a quick moment to rate your support experience!\n\nHave a wonderful day,\n{{agent.name}}	General	c64e3806-b382-4689-9f1a-94114205ce5f	2026-08-14 12:01:02.127623	2026-08-14 12:01:02.127701
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messages (id, ticket_id, sender_id, sender_type, body, attachments, created_at, external_message_id, body_html) FROM stdin;
cb3fa11a-06ee-4651-82a3-2e1566b75a87	c025e796-7ad9-4de8-be7b-689002d7343d	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-09 17:46:54.766858	\N	\N
16f1cdf1-2703-41fb-ae43-66cf97a644b1	20b42ccb-bb63-4cde-a8fa-1828ae528f18	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	How long does delivery take?	\N	2026-09-10 10:29:54.001642	\N	\N
1190a945-80ad-418b-9bb4-be3bed64f3e7	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?	\N	2026-09-10 11:42:29.217096	\N	\N
29127375-9b5b-4674-bfc5-49e3e056e8bb	6c307a57-6db6-45cc-8a1a-cb06408ab35c	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Give me info. of my all products!	\N	2026-09-10 13:28:35.171009	\N	\N
41cdaa87-7146-4a31-a6e1-6e6e77e4e457	71f00727-caa8-4658-9db7-0c4dbb7d2645	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info. about Home & Kitchen products!	\N	2026-09-10 15:08:58.691201	\N	\N
0a0cdc08-7a47-4453-81a4-7389082460c1	71f00727-caa8-4658-9db7-0c4dbb7d2645	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?	\N	2026-09-10 15:09:41.888664	\N	\N
1910f113-b52c-428d-849d-0deebf428a34	c6384d2a-e873-4772-af84-73b664bf0b36	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-10 15:32:54.630492	\N	\N
b79d4470-b2d1-44ad-b397-d5b37284e701	c025e796-7ad9-4de8-be7b-689002d7343d	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i want to track my order!	\N	2026-09-09 17:47:25.168139	\N	\N
2e242b47-f801-4333-b7ab-901d7c51fdde	c025e796-7ad9-4de8-be7b-689002d7343d	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\nItems: NovaPhone Pro 5G (Midnight Black, 256 GB) (Qty 1).\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).\n\nOrder ORD-002 status: **DELIVERED** (Total: ₹12,498.00).\nItems: ErgoSilent Wireless Keyboard & Mouse Combo (Qty 1), SoundWave ANC 750 Over-Ear Wireless Headphones (Qty 1).\nShipment SHIP-002 for order ORD-002 is **DELIVERED** via BlueDart (Tracking: TRK-BLUEDART-488302652, Estimated Delivery: 2026-08-07).\n\nOrder ORD-025 status: **CONFIRMED** (Total: ₹2,899.00).\nItems: Smart Touch Instant Induction Cooktop 2100W (Qty 1).\nShipment SHIP-025 for order ORD-025 is **PROCESSING** via XpressBees (Tracking: TRK-XPRESSBEES-819595113, Estimated Delivery: 2026-08-23).	\N	2026-09-09 17:47:58.58312	\N	\N
563c7e9a-5cfc-4d06-b5f5-381c0f746c81	20b42ccb-bb63-4cde-a8fa-1828ae528f18	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?	\N	2026-09-10 10:29:55.016291	\N	\N
482444c1-fe43-45d5-863d-245958a056c9	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?	\N	2026-09-10 11:58:52.685874	\N	\N
efd263b3-8ecc-444a-8e00-dffcf305c1f9	6c307a57-6db6-45cc-8a1a-cb06408ab35c	\N	ai	Here is an overview of popular products currently available in our ShopKart catalog:\n\n### 📱 Mobiles & Tablets\n• **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) — **₹46,999.00** (14.5% off) | Status: *IN_STOCK* (45 in stock)\n• **AeroTab Air 11-inch Wi-Fi Tablet (Space Grey, 128 GB)** (`PROD-002`) — **₹27,499.00** (16.7% off) | Status: *IN_STOCK* (4 in stock)\n• **Pixelite 4G Budget Smartphone (Ocean Blue, 64 GB)** (`PROD-003`) — **₹7,999.00** (20.0% off) | Status: *IN_STOCK* (0 in stock)\n• **ClassicTouch Keypad Phone V1** (`PROD-004`) — **₹1,499.00** (25.0% off) | Status: *IN_STOCK* (0 in stock)\n\n### 💻 Laptops & Computers\n• **ZenBook Ultra 14 Thin & Light Laptop (16GB/512GB SSD/Intel Core i7)** (`PROD-005`) — **₹78,990.00** (12.2% off) | Status: *IN_STOCK* (25 in stock)\n• **GamerX Legion RTX 4060 Gaming Laptop (16GB/1TB SSD)** (`PROD-006`) — **₹109,990.00** (12.0% off) | Status: *IN_STOCK* (12 in stock)\n• **ProView 27-inch 4K UHD IPS Monitor** (`PROD-007`) — **₹23,999.00** (20.0% off) | Status: *IN_STOCK* (30 in stock)\n• **ErgoSilent Wireless Keyboard & Mouse Combo** (`PROD-008`) — **₹2,499.00** (28.6% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🎧 Audio & Headphones\n• **SoundWave ANC 750 Over-Ear Wireless Headphones** (`PROD-009`) — **₹9,999.00** (33.3% off) | Status: *IN_STOCK* (40 in stock)\n• **AirBuds Pro True Wireless Earbuds with Dual Mic** (`PROD-010`) — **₹2,499.00** (50.0% off) | Status: *IN_STOCK* (80 in stock)\n• **BoomBox 20W Portable Bluetooth Speaker** (`PROD-011`) — **₹2,799.00** (30.0% off) | Status: *IN_STOCK* (50 in stock)\n• **StudioPro Vocal Condenser USB Microphone with Arm Stand** (`PROD-039`) — **₹4,499.00** (35.7% off) | Status: *IN_STOCK* (20 in stock)\n\n### 🛍️ Kitchen & Dining\n• **ChefPro 1000W 4-Jar Mixer Grinder** (`PROD-012`) — **₹4,799.00** (31.4% off) | Status: *IN_STOCK* (35 in stock)\n• **CrispAir Digital 4.5L Air Fryer (Rapid Air Tech)** (`PROD-013`) — **₹5,999.00** (29.4% off) | Status: *IN_STOCK* (20 in stock)\n• **Hard Anodized 3-Piece Cookware Set (Kadai, Fry Pan, Tawa)** (`PROD-014`) — **₹2,899.00** (32.6% off) | Status: *IN_STOCK* (40 in stock)\n• **Stainless Steel Thermal Insulated Water Bottle 1000ml** (`PROD-038`) — **₹899.00** (40.0% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🛍️ Home Furniture\n• **ErgoRest High-Back Ergonomic Office Chair** (`PROD-015`) — **₹11,499.00** (32.4% off) | Status: *IN_STOCK* (18 in stock)\n• **Solid Sheesham Wood 4-Seater Dining Table Set** (`PROD-016`) — **₹26,999.00** (30.8% off) | Status: *IN_STOCK* (8 in stock)\n• **Modular Engineered Wood Study Desk (Columbian Walnut)** (`PROD-017`) — **₹5,499.00** (38.9% off) | Status: *IN_STOCK* (3 in stock)\n\n### 🏠 Home Appliances\n• **VisionPlus 55-inch 4K Ultra HD Smart Google TV** (`PROD-018`) — **₹38,990.00** (35.0% off) | Status: *IN_STOCK* (22 in stock)\n• **PureBreeze HEPA Air Purifier for Home (CADR 350 m3/h)** (`PROD-019`) — **₹10,999.00** (31.3% off) | Status: *IN_STOCK* (28 in stock)\n• **RoboClean 2-in-1 Robot Vacuum Cleaner & Mop** (`PROD-020`) — **₹19,999.00** (33.3% off) | Status: *IN_STOCK* (15 in stock)\n• **Smart Touch Instant Induction Cooktop 2100W** (`PROD-040`) — **₹2,899.00** (35.6% off) | Status: *IN_STOCK* (30 in stock)\n\n### 🛍️ Men's Clothing\n• **Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)** (`PROD-021`) — **₹1,299.00** (48.0% off) | Status: *IN_STOCK* (55 in stock)\n• **Slim Fit Stretchable Denim Jeans (Dark Indigo)** (`PROD-022`) — **₹1,899.00** (42.4% off) | Status: *IN_STOCK* (40 in stock)\n• **Heavyweight Cotton Graphic Crewneck T-Shirt (Olive)** (`PROD-023`) — **₹799.00** (46.7% off) | Status: *IN_STOCK* (70 in stock)\n• **Men's 3-Pack Modal Cotton Innerwear Boxer Briefs** (`PROD-024`) — **₹899.00** (30.8% off) | Status: *IN_STOCK* (45 in stock)\n\n### 🛍️ Women's Clothing\n• **Floral Embroidered Chanderi Silk Kurta Set with Dupatta** (`PROD-025`) — **₹3,499.00** (41.7% off) | Status: *IN_STOCK* (30 in stock)\n• **Tiered A-Line Floral Summer Midi Dress (Pastel Sage)** (`PROD-026`) — **₹1,699.00** (43.3% off) | Status: *IN_STOCK* (35 in stock)\n• **High-Waist Cotton Ankle Length Casual Trousers** (`PROD-027`) — **₹1,199.00** (45.5% off) | Status: *IN_STOCK* (25 in stock)\n\n### 👟 Footwear\n• **AirStride Pro Lightweight Road Running Shoes** (`PROD-028`) — **₹4,299.00** (33.9% off) | Status: *IN_STOCK* (50 in stock)\n• **Handcrafted Genuine Leather Formal Derby Shoes (Tan)** (`PROD-029`) — **₹3,699.00** (32.7% off) | Status: *IN_STOCK* (25 in stock)\n• **CloudSlide Ergonomic EVA Comfort Flip-Flop Slides** (`PROD-030`) — **₹699.00** (46.2% off) | Status: *IN_STOCK* (65 in stock)\n\n### 📱 Electronics\n• **BeardMaster Pro Cordless Beard Trimmer (0.5 - 20 mm)** (`PROD-031`) — **₹1,699.00** (32.0% off) | Status: *IN_STOCK* (40 in stock)\n• **HydroSonic Sonic Electric Toothbrush with 4 Brush Heads** (`PROD-032`) — **₹2,299.00** (42.5% off) | Status: *IN_STOCK* (30 in stock)\n• **SilkTouch Salon Hair Dryer 2000W with Ionic Care** (`PROD-033`) — **₹2,199.00** (37.2% off) | Status: *IN_STOCK* (25 in stock)\n• **Vitamin C 10% Brightening Glow Face Serum (30 ml)** (`PROD-034`) — **₹549.00** (31.3% off) | Status: *IN_STOCK* (90 in stock)\n  *...and 3 more items in Electronics*\n\n💡 *Tip: Ask for full specs, pricing, or warranty details on any item by specifying its name or ID (e.g., `Tell me about PROD-001`).*	\N	2026-09-10 13:28:35.977099	\N	\N
bd987962-e011-41b5-9b8e-8d4280069483	71f00727-caa8-4658-9db7-0c4dbb7d2645	\N	ai	Found 2 matching product(s) in our store:\n\n• **PureBreeze HEPA Air Purifier for Home (CADR 350 m3/h)** (`PROD-019`) by *PureBreeze* — **₹10,999.00** (MRP: ₹15,999.00, 31.3% off)\n   Category: Home Appliances | Status: *IN_STOCK* (28 available)\n• **CloudSlide Ergonomic EVA Comfort Flip-Flop Slides** (`PROD-030`) by *AirStride* — **₹699.00** (MRP: ₹1,299.00, 46.2% off)\n   Category: Footwear | Status: *IN_STOCK* (65 available)\n\n💡 *Ask me about any specific Product ID or model for warranty, return policies, and full technical specifications!*	\N	2026-09-10 15:08:58.794378	\N	\N
b1abe85d-1383-41a8-a0e8-62ca9c81928f	71f00727-caa8-4658-9db7-0c4dbb7d2645	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?	\N	2026-09-10 15:10:04.400082	\N	\N
235cf98d-29d9-4db7-a158-9c67729e4293	c6384d2a-e873-4772-af84-73b664bf0b36	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me info  of your all products!	\N	2026-09-10 15:33:25.231853	\N	\N
a409d2f2-0bc6-4b41-a81f-9d2ec6ed9737	c025e796-7ad9-4de8-be7b-689002d7343d	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\n\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).	\N	2026-09-09 17:47:26.044719	\N	\N
d8d851e2-103e-4b84-b00a-276d911aa6ae	6c307a57-6db6-45cc-8a1a-cb06408ab35c	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-10 10:34:59.621802	\N	\N
539a4c4c-b74a-46bd-8f51-ad37a6f4961f	5142c951-2b60-49b9-8c49-f63d872038f0	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-10 11:59:04.326806	\N	\N
5063e3ba-7039-4ea2-91fc-dcc2857e7654	6c307a57-6db6-45cc-8a1a-cb06408ab35c	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Give me info. of my all orders!	\N	2026-09-10 13:29:46.468581	\N	\N
a7033dbc-41a9-487d-ac25-64ba01b2fc02	71f00727-caa8-4658-9db7-0c4dbb7d2645	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks i got info. which i wanted!	\N	2026-09-10 15:09:41.755028	\N	\N
df9f173f-f606-4002-be2c-f520fb310315	c6384d2a-e873-4772-af84-73b664bf0b36	\N	ai	Here is an overview of popular products currently available in our ShopKart catalog:\n\n### 📱 Mobiles & Tablets\n• **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) — **₹46,999.00** (14.5% off) | Status: *IN_STOCK* (45 in stock)\n• **AeroTab Air 11-inch Wi-Fi Tablet (Space Grey, 128 GB)** (`PROD-002`) — **₹27,499.00** (16.7% off) | Status: *IN_STOCK* (4 in stock)\n• **Pixelite 4G Budget Smartphone (Ocean Blue, 64 GB)** (`PROD-003`) — **₹7,999.00** (20.0% off) | Status: *IN_STOCK* (0 in stock)\n• **ClassicTouch Keypad Phone V1** (`PROD-004`) — **₹1,499.00** (25.0% off) | Status: *IN_STOCK* (0 in stock)\n\n### 💻 Laptops & Computers\n• **ZenBook Ultra 14 Thin & Light Laptop (16GB/512GB SSD/Intel Core i7)** (`PROD-005`) — **₹78,990.00** (12.2% off) | Status: *IN_STOCK* (25 in stock)\n• **GamerX Legion RTX 4060 Gaming Laptop (16GB/1TB SSD)** (`PROD-006`) — **₹109,990.00** (12.0% off) | Status: *IN_STOCK* (12 in stock)\n• **ProView 27-inch 4K UHD IPS Monitor** (`PROD-007`) — **₹23,999.00** (20.0% off) | Status: *IN_STOCK* (30 in stock)\n• **ErgoSilent Wireless Keyboard & Mouse Combo** (`PROD-008`) — **₹2,499.00** (28.6% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🎧 Audio & Headphones\n• **SoundWave ANC 750 Over-Ear Wireless Headphones** (`PROD-009`) — **₹9,999.00** (33.3% off) | Status: *IN_STOCK* (40 in stock)\n• **AirBuds Pro True Wireless Earbuds with Dual Mic** (`PROD-010`) — **₹2,499.00** (50.0% off) | Status: *IN_STOCK* (80 in stock)\n• **BoomBox 20W Portable Bluetooth Speaker** (`PROD-011`) — **₹2,799.00** (30.0% off) | Status: *IN_STOCK* (50 in stock)\n• **StudioPro Vocal Condenser USB Microphone with Arm Stand** (`PROD-039`) — **₹4,499.00** (35.7% off) | Status: *IN_STOCK* (20 in stock)\n\n### 🛍️ Kitchen & Dining\n• **ChefPro 1000W 4-Jar Mixer Grinder** (`PROD-012`) — **₹4,799.00** (31.4% off) | Status: *IN_STOCK* (35 in stock)\n• **CrispAir Digital 4.5L Air Fryer (Rapid Air Tech)** (`PROD-013`) — **₹5,999.00** (29.4% off) | Status: *IN_STOCK* (20 in stock)\n• **Hard Anodized 3-Piece Cookware Set (Kadai, Fry Pan, Tawa)** (`PROD-014`) — **₹2,899.00** (32.6% off) | Status: *IN_STOCK* (40 in stock)\n• **Stainless Steel Thermal Insulated Water Bottle 1000ml** (`PROD-038`) — **₹899.00** (40.0% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🛍️ Home Furniture\n• **ErgoRest High-Back Ergonomic Office Chair** (`PROD-015`) — **₹11,499.00** (32.4% off) | Status: *IN_STOCK* (18 in stock)\n• **Solid Sheesham Wood 4-Seater Dining Table Set** (`PROD-016`) — **₹26,999.00** (30.8% off) | Status: *IN_STOCK* (8 in stock)\n• **Modular Engineered Wood Study Desk (Columbian Walnut)** (`PROD-017`) — **₹5,499.00** (38.9% off) | Status: *IN_STOCK* (3 in stock)\n\n### 🏠 Home Appliances\n• **VisionPlus 55-inch 4K Ultra HD Smart Google TV** (`PROD-018`) — **₹38,990.00** (35.0% off) | Status: *IN_STOCK* (22 in stock)\n• **PureBreeze HEPA Air Purifier for Home (CADR 350 m3/h)** (`PROD-019`) — **₹10,999.00** (31.3% off) | Status: *IN_STOCK* (28 in stock)\n• **RoboClean 2-in-1 Robot Vacuum Cleaner & Mop** (`PROD-020`) — **₹19,999.00** (33.3% off) | Status: *IN_STOCK* (15 in stock)\n• **Smart Touch Instant Induction Cooktop 2100W** (`PROD-040`) — **₹2,899.00** (35.6% off) | Status: *IN_STOCK* (30 in stock)\n\n### 🛍️ Men's Clothing\n• **Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)** (`PROD-021`) — **₹1,299.00** (48.0% off) | Status: *IN_STOCK* (55 in stock)\n• **Slim Fit Stretchable Denim Jeans (Dark Indigo)** (`PROD-022`) — **₹1,899.00** (42.4% off) | Status: *IN_STOCK* (40 in stock)\n• **Heavyweight Cotton Graphic Crewneck T-Shirt (Olive)** (`PROD-023`) — **₹799.00** (46.7% off) | Status: *IN_STOCK* (70 in stock)\n• **Men's 3-Pack Modal Cotton Innerwear Boxer Briefs** (`PROD-024`) — **₹899.00** (30.8% off) | Status: *IN_STOCK* (45 in stock)\n\n### 🛍️ Women's Clothing\n• **Floral Embroidered Chanderi Silk Kurta Set with Dupatta** (`PROD-025`) — **₹3,499.00** (41.7% off) | Status: *IN_STOCK* (30 in stock)\n• **Tiered A-Line Floral Summer Midi Dress (Pastel Sage)** (`PROD-026`) — **₹1,699.00** (43.3% off) | Status: *IN_STOCK* (35 in stock)\n• **High-Waist Cotton Ankle Length Casual Trousers** (`PROD-027`) — **₹1,199.00** (45.5% off) | Status: *IN_STOCK* (25 in stock)\n\n### 👟 Footwear\n• **AirStride Pro Lightweight Road Running Shoes** (`PROD-028`) — **₹4,299.00** (33.9% off) | Status: *IN_STOCK* (50 in stock)\n• **Handcrafted Genuine Leather Formal Derby Shoes (Tan)** (`PROD-029`) — **₹3,699.00** (32.7% off) | Status: *IN_STOCK* (25 in stock)\n• **CloudSlide Ergonomic EVA Comfort Flip-Flop Slides** (`PROD-030`) — **₹699.00** (46.2% off) | Status: *IN_STOCK* (65 in stock)\n\n### 📱 Electronics\n• **BeardMaster Pro Cordless Beard Trimmer (0.5 - 20 mm)** (`PROD-031`) — **₹1,699.00** (32.0% off) | Status: *IN_STOCK* (40 in stock)\n• **HydroSonic Sonic Electric Toothbrush with 4 Brush Heads** (`PROD-032`) — **₹2,299.00** (42.5% off) | Status: *IN_STOCK* (30 in stock)\n• **SilkTouch Salon Hair Dryer 2000W with Ionic Care** (`PROD-033`) — **₹2,199.00** (37.2% off) | Status: *IN_STOCK* (25 in stock)\n• **Vitamin C 10% Brightening Glow Face Serum (30 ml)** (`PROD-034`) — **₹549.00** (31.3% off) | Status: *IN_STOCK* (90 in stock)\n  *...and 3 more items in Electronics*\n\n💡 *Tip: Ask for full specs, pricing, or warranty details on any item by specifying its name or ID (e.g., `Tell me about PROD-001`).*	\N	2026-09-10 15:33:26.06631	\N	\N
8a7a1f6c-e48d-4670-ba41-6a1dd5830905	c025e796-7ad9-4de8-be7b-689002d7343d	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info. of my all orders!	\N	2026-09-09 17:47:58.55674	\N	\N
dab9880c-85bb-4dd6-9980-6279f6f2fba3	672f537a-e703-4ec8-8518-b7c2eee623b5	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	How long does delivery take?	\N	2026-09-10 10:35:19.891824	\N	\N
b021e88d-7468-4b8f-9f52-23951841d8d4	5142c951-2b60-49b9-8c49-f63d872038f0	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i want to track my order so which category i need to chose for this query ?  📎 [Attachment: Screenshot From 2026-08-12 11-21-17.png](http://localhost:8000/static/uploads/86a78dd43d034b729c50396d1f483f0a_Screenshot From 2026-08-12 11-21-17.png)	\N	2026-09-10 12:00:10.708673	\N	\N
03721342-fa44-41df-b831-b9f9a76aaac7	6c307a57-6db6-45cc-8a1a-cb06408ab35c	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\nItems: NovaPhone Pro 5G (Midnight Black, 256 GB) (Qty 1).\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).\n\nOrder ORD-002 status: **DELIVERED** (Total: ₹12,498.00).\nItems: ErgoSilent Wireless Keyboard & Mouse Combo (Qty 1), SoundWave ANC 750 Over-Ear Wireless Headphones (Qty 1).\nShipment SHIP-002 for order ORD-002 is **DELIVERED** via BlueDart (Tracking: TRK-BLUEDART-488302652, Estimated Delivery: 2026-08-07).\n\nOrder ORD-025 status: **CONFIRMED** (Total: ₹2,899.00).\nItems: Smart Touch Instant Induction Cooktop 2100W (Qty 1).\nShipment SHIP-025 for order ORD-025 is **PROCESSING** via XpressBees (Tracking: TRK-XPRESSBEES-819595113, Estimated Delivery: 2026-08-23).	\N	2026-09-10 13:29:46.512529	\N	\N
9bdf9dab-b5f5-4e84-b77d-3488c9641007	71f00727-caa8-4658-9db7-0c4dbb7d2645	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks	\N	2026-09-10 15:10:04.372722	\N	\N
59bc7cb0-3527-4a87-9137-525181a1899e	c6384d2a-e873-4772-af84-73b664bf0b36	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	My device is not working.	\N	2026-09-10 15:35:33.344505	\N	\N
8e0446e2-986f-4555-9ccd-a9cd1b0b584f	f84f326f-8fd7-4582-97d0-ac023dc09b08	b93ba828-c127-4801-9059-5444918058e2	customer	PRODUCTION REALTIME FINAL TEST 1835	\N	2026-09-02 09:51:02.661051	m_exact_test_d024dcc6	\N
c2587866-3d2c-46d4-b9a0-deeb6ef2e58f	672f537a-e703-4ec8-8518-b7c2eee623b5	\N	ai	According to ShopKart's How to Track Your ShopKart Order (KA-001):\n\n# How to Track Your ShopKart Order\n\n3. **Status Explanations:**\n   - **In Transit:** Package is on the move between regional fulfillment sorting centers.\n   - **Out for Delivery:** Courier delivery executive has dispatched with your parcel and will attempt delivery today.\n   - **Delayed:** Unforeseen transit delays (weather, high volume). New estimated delivery date will be shown.	\N	2026-09-10 10:35:20.408835	\N	\N
1be01dcc-cfc6-4c6e-b9c8-7e98df0ed204	7a7110b1-9451-4771-a297-b59378914907	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Can I change my delivery address?	\N	2026-09-10 10:36:46.357605	\N	\N
8d3253d7-80b3-4c5a-9194-847e759c9c3b	5142c951-2b60-49b9-8c49-f63d872038f0	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\n\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).	\N	2026-09-10 12:00:11.328227	\N	\N
efe9687b-dd5a-46b8-b017-abb1a493d6f1	62b667d8-b19c-4451-a563-4845b06bbec2	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-10 14:10:29.733013	\N	\N
6ed6b7d1-908e-4914-a5e9-bc74033d21c9	71f00727-caa8-4658-9db7-0c4dbb7d2645	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-10 15:10:27.777697	\N	\N
11941f66-fa1f-48de-bfa5-47de629f6552	71f00727-caa8-4658-9db7-0c4dbb7d2645	\N	ai	Your ticket [TCK-36881] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/71f00727-caa8-4658-9db7-0c4dbb7d2645/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-10 15:10:27.777935	\N	\N
b22ef389-1bed-4de7-92fa-8bdf35ac5e52	c6384d2a-e873-4772-af84-73b664bf0b36	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?	\N	2026-09-10 15:35:33.482226	\N	\N
a2f8b151-084a-4ebb-9598-1d16d7b057ff	7a7110b1-9451-4771-a297-b59378914907	\N	ai	According to ShopKart's ShopKart Shipping and Delivery Policy (POL-004):\n\n### 4. Delivery Address Changes\n- Delivery addresses may be modified only while the order is in **PLACED** or **CONFIRMED** status.\n- Once dispatched, address changes cannot be accommodated due to courier waybill locking.	\N	2026-09-10 10:36:46.469007	\N	\N
d3cf17e8-b55e-47e1-bb39-27cf6969f532	7a7110b1-9451-4771-a297-b59378914907	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks my query is resolved!	\N	2026-09-10 10:40:17.582841	\N	\N
aace017e-c329-4b5e-835f-ccb666677014	5142c951-2b60-49b9-8c49-f63d872038f0	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	this resolved my query ! : Thank you!	\N	2026-09-10 12:23:31.455689	\N	\N
a5e3f7cd-9c2f-4325-9523-7eda4c0fe647	f4ad1c11-6675-4e48-ac1b-5954263b9e27	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-10 14:41:09.468032	\N	\N
21610ad4-3956-469b-ab5d-68fd70a3fd3e	62b667d8-b19c-4451-a563-4845b06bbec2	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i want to track my order-001!	\N	2026-09-10 15:16:08.833171	\N	\N
e76e1cd0-9517-44c3-9888-49848833c4aa	7a7110b1-9451-4771-a297-b59378914907	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-10 10:40:17.591011	\N	\N
811071dc-ab8f-4ae0-a9a1-87d1c259363f	7a7110b1-9451-4771-a297-b59378914907	\N	ai	Your ticket [TCK-37200] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/7a7110b1-9451-4771-a297-b59378914907/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-10 10:40:17.592165	\N	\N
9e8a634b-082d-4a62-901f-47d0422f2aa2	5142c951-2b60-49b9-8c49-f63d872038f0	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-10 12:23:31.469541	\N	\N
d03f6dfb-b4bd-462f-86fe-911d64d3fd74	5142c951-2b60-49b9-8c49-f63d872038f0	\N	ai	Your ticket [TCK-19858] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/5142c951-2b60-49b9-8c49-f63d872038f0/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-10 12:23:31.469914	\N	\N
cf003395-ec85-49ba-a568-caa72b3700bf	f4ad1c11-6675-4e48-ac1b-5954263b9e27	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info. of Home & Kitchen products!	\N	2026-09-10 14:41:34.104788	\N	\N
45683ba1-a3e2-490f-96e0-b3cfc713b78b	62b667d8-b19c-4451-a563-4845b06bbec2	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\n\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).	\N	2026-09-10 15:16:08.857961	\N	\N
85b57af5-c903-4d3b-bbb5-279a1b313b8b	b78e3d69-f0e0-4b36-866f-a1fe0c012eaa	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-09 17:05:05.017089	\N	\N
4b951cd8-7f0f-4c0f-a7de-3d44b087542b	b78e3d69-f0e0-4b36-866f-a1fe0c012eaa	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Hi, what is your return policy?	\N	2026-09-09 17:05:09.586207	\N	\N
310de9ff-f161-49ac-b751-fad531ecf15b	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-10 11:42:17.244568	\N	\N
3f615db6-811b-4fc0-b4f5-5545e0361b82	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	📎 [Attachment: Screenshot From 2026-08-12 11-21-17.png](http://localhost:8000/static/uploads/b67ce2a5f64a4fafb2fb235a20947ec2_Screenshot From 2026-08-12 11-21-17.png)	\N	2026-09-10 11:58:52.446616	\N	\N
9288a5b5-e6a6-4e1e-95bb-84a6eff41daf	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	my query is solved! : Thank you!	\N	2026-09-10 13:16:22.743671	\N	\N
9f15cbb7-f027-4874-bc14-6ae2f8b08a6a	f4ad1c11-6675-4e48-ac1b-5954263b9e27	\N	ai	Found 2 matching product(s) in our store:\n\n• **PureBreeze HEPA Air Purifier for Home (CADR 350 m3/h)** (`PROD-019`) by *PureBreeze* — **₹10,999.00** (MRP: ₹15,999.00, 31.3% off)\n   Category: Home Appliances | Status: *IN_STOCK* (28 available)\n• **CloudSlide Ergonomic EVA Comfort Flip-Flop Slides** (`PROD-030`) by *AirStride* — **₹699.00** (MRP: ₹1,299.00, 46.2% off)\n   Category: Footwear | Status: *IN_STOCK* (65 available)\n\n💡 *Ask me about any specific Product ID or model for warranty, return policies, and full technical specifications!*	\N	2026-09-10 14:41:34.211844	\N	\N
7d256881-0fd4-43c2-ac39-508b8582d307	9f75302d-8a1a-44a8-8660-4969785ae442	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	What is your refund policy?	\N	2026-09-10 15:24:40.861731	\N	\N
ea32f2d6-a902-4ee4-9daa-4962f8d0ddfa	b78e3d69-f0e0-4b36-866f-a1fe0c012eaa	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?\n\nAccording to ShopKart's ShopKart Return Policy (POL-001):\n\n# ShopKart Return Policy\n\n### 1. General Return Window\nShopKart offers a return window on eligible items delivered to customers in India:\n- **Electronics & Mobiles:** 7 calendar days from delivery date.\n- **Home & Kitchen Appliances:** 7 to 10 calendar days from delivery date.\n- **Fashion & Footwear:** 15 calendar days from delivery date.\n- **Large Furniture:** 10 calendar days from delivery date.	\N	2026-09-09 17:05:10.069483	\N	\N
14f5293d-7995-4f6a-a121-5e0d9f1eb995	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	What is the Capital of india?	\N	2026-09-10 11:42:29.035481	\N	\N
acd2cccd-bae5-4883-91b6-38516f6b818f	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-10 13:16:22.752664	\N	\N
43bcc565-7e50-45c2-a13e-8279b68099c7	e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	\N	ai	Your ticket [TCK-84229] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-10 13:16:22.752894	\N	\N
9a8d5ba7-9422-4a89-a347-285512c2e4b0	71f00727-caa8-4658-9db7-0c4dbb7d2645	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-10 15:08:37.11008	\N	\N
f6406f92-8deb-4479-881b-8d662cbf3e52	71f00727-caa8-4658-9db7-0c4dbb7d2645	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks , myquery is resolved!	\N	2026-09-10 15:10:27.770069	\N	\N
5a483dff-167e-4ca7-a21c-c924822c3517	9f75302d-8a1a-44a8-8660-4969785ae442	\N	ai	According to ShopKart's ShopKart Refund Policy (POL-002):\n\n# ShopKart Refund Policy\n\n### 1. Initiation Timelines\n- **Pre-dispatch Order Cancellations:** Refund initiated immediately upon cancellation approval.\n- **Doorstep Returns:** Refund initiated within 2 to 4 hours of the courier partner completing physical pickup.\n- **Warehouse Returned Items:** Refund initiated within 24 hours of warehouse quality check clearance.	\N	2026-09-10 15:24:41.023885	\N	\N
28ca517f-4a58-4d3c-bc5c-029fc1904646	096a4ed9-b378-49a4-b78b-ea3c45ab64df	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	What is your refund policy?	\N	2026-09-10 18:10:57.650289	\N	\N
6125456b-9030-473e-bbd5-15568e29566e	641222a4-43a8-4138-acf9-f2bd23a72544	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	What is your refund policy?	\N	2026-09-10 18:11:00.358278	\N	\N
f36ca38f-9e77-4fe1-ad11-3625eef99338	096a4ed9-b378-49a4-b78b-ea3c45ab64df	\N	ai	According to ShopKart's ShopKart Refund Policy (POL-002):\n\n# ShopKart Refund Policy\n\n### 1. Initiation Timelines\n- **Pre-dispatch Order Cancellations:** Refund initiated immediately upon cancellation approval.\n- **Doorstep Returns:** Refund initiated within 2 to 4 hours of the courier partner completing physical pickup.\n- **Warehouse Returned Items:** Refund initiated within 24 hours of warehouse quality check clearance.	\N	2026-09-10 18:11:00.354768	\N	\N
112dcd22-b1e6-4fd3-bc46-73659890590c	641222a4-43a8-4138-acf9-f2bd23a72544	\N	ai	According to ShopKart's ShopKart Refund Policy (POL-002):\n\n# ShopKart Refund Policy\n\n### 1. Initiation Timelines\n- **Pre-dispatch Order Cancellations:** Refund initiated immediately upon cancellation approval.\n- **Doorstep Returns:** Refund initiated within 2 to 4 hours of the courier partner completing physical pickup.\n- **Warehouse Returned Items:** Refund initiated within 24 hours of warehouse quality check clearance.	\N	2026-09-10 18:11:00.379561	\N	\N
a78ecbb2-48a8-4efa-9e77-3d2dd435afc9	5713519c-e2f1-4348-b11a-83e01d622160	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	What is your refund policy?	\N	2026-09-10 18:11:00.450948	\N	\N
2ed02743-6b56-4311-a3c5-8c4b475a1435	5713519c-e2f1-4348-b11a-83e01d622160	\N	ai	I have transferred your request to our senior support team (HIGH priority: Customer explicitly requested transfer to a human support agent.). A human support representative is reviewing your case details and will assist you shortly.	\N	2026-09-10 18:14:22.978999	\N	\N
149e603f-dae3-4692-a111-6ddca828abbf	5713519c-e2f1-4348-b11a-83e01d622160	\N	ai	According to ShopKart's ShopKart Refund Policy (POL-002):\n\n# ShopKart Refund Policy\n\n### 1. Initiation Timelines\n- **Pre-dispatch Order Cancellations:** Refund initiated immediately upon cancellation approval.\n- **Doorstep Returns:** Refund initiated within 2 to 4 hours of the courier partner completing physical pickup.\n- **Warehouse Returned Items:** Refund initiated within 24 hours of warehouse quality check clearance.	\N	2026-09-10 18:11:00.533284	\N	\N
a2684321-f6bb-4ddc-b27b-801964b18332	5713519c-e2f1-4348-b11a-83e01d622160	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i want to talk with human agent	\N	2026-09-10 18:14:22.940517	\N	\N
1026cfdb-e87a-4936-a26a-02b432348ef0	aab74641-2a47-4a99-bbcd-a1c7fa2dac72	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-14 15:59:27.731348	\N	\N
1259ab90-def9-4486-a553-9bac7fbfc91b	aab74641-2a47-4a99-bbcd-a1c7fa2dac72	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	tell me every products for Electronics	\N	2026-09-14 15:59:55.092789	\N	\N
c8e9bddd-5197-49d1-8601-4e619566fe2b	aab74641-2a47-4a99-bbcd-a1c7fa2dac72	\N	ai	Found 2 matching product(s) in our store:\n\n• **Pixelite 4G Budget Smartphone (Ocean Blue, 64 GB)** (`PROD-003`) by *Pixelite* — **₹7,999.00** (MRP: ₹9,999.00, 20.0% off)\n   Category: Mobiles & Tablets | Status: *IN_STOCK* (0 available)\n• **CloudSlide Ergonomic EVA Comfort Flip-Flop Slides** (`PROD-030`) by *AirStride* — **₹699.00** (MRP: ₹1,299.00, 46.2% off)\n   Category: Footwear | Status: *IN_STOCK* (65 available)\n\n💡 *Ask me about any specific Product ID or model for warranty, return policies, and full technical specifications!*	\N	2026-09-14 15:59:58.829572	\N	\N
52bb12e1-a259-410e-9237-56cbe26ef239	5faee52b-bcd9-442b-9136-148790eba194	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-14 16:18:27.692473	\N	\N
119f6850-f21c-410b-81af-fec4f02509b1	5faee52b-bcd9-442b-9136-148790eba194	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	tell me every products for Electronics	\N	2026-09-14 16:18:34.316441	\N	\N
579635d5-f05d-4747-91cb-9359fe0ad52e	5faee52b-bcd9-442b-9136-148790eba194	\N	ai	Found 19 matching product(s) across 4 categories in our store:\n\n### 📱 Mobiles & Tablets\n• **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) by *NovaPhone* — **₹46,999.00** (MRP: ₹54,999.00, 14.5% off)\n   Status: *IN_STOCK* (45 available)\n• **AeroTab Air 11-inch Wi-Fi Tablet (Space Grey, 128 GB)** (`PROD-002`) by *AeroTab* — **₹27,499.00** (MRP: ₹32,999.00, 16.7% off)\n   Status: *IN_STOCK* (4 available)\n• **Pixelite 4G Budget Smartphone (Ocean Blue, 64 GB)** (`PROD-003`) by *Pixelite* — **₹7,999.00** (MRP: ₹9,999.00, 20.0% off)\n   Status: *OUT_OF_STOCK* (0 available)\n• **ClassicTouch Keypad Phone V1** (`PROD-004`) by *ClassicTouch* — **₹1,499.00** (MRP: ₹1,999.00, 25.0% off)\n   Status: *OUT_OF_STOCK* (0 available)\n\n### 💻 Laptops & Computers\n• **ZenBook Ultra 14 Thin & Light Laptop (16GB/512GB SSD/Intel Core i7)** (`PROD-005`) by *ZenTech* — **₹78,990.00** (MRP: ₹89,990.00, 12.2% off)\n   Status: *IN_STOCK* (25 available)\n• **GamerX Legion RTX 4060 Gaming Laptop (16GB/1TB SSD)** (`PROD-006`) by *GamerX* — **₹109,990.00** (MRP: ₹124,990.00, 12.0% off)\n   Status: *IN_STOCK* (12 available)\n• **ProView 27-inch 4K UHD IPS Monitor** (`PROD-007`) by *ProView* — **₹23,999.00** (MRP: ₹29,999.00, 20.0% off)\n   Status: *IN_STOCK* (30 available)\n• **ErgoSilent Wireless Keyboard & Mouse Combo** (`PROD-008`) by *LogiTechie* — **₹2,499.00** (MRP: ₹3,499.00, 28.6% off)\n   Status: *IN_STOCK* (60 available)\n\n### 🎧 Audio & Headphones\n• **SoundWave ANC 750 Over-Ear Wireless Headphones** (`PROD-009`) by *SoundWave* — **₹9,999.00** (MRP: ₹14,999.00, 33.3% off)\n   Status: *IN_STOCK* (40 available)\n• **AirBuds Pro True Wireless Earbuds with Dual Mic** (`PROD-010`) by *AirPulse* — **₹2,499.00** (MRP: ₹4,999.00, 50.0% off)\n   Status: *IN_STOCK* (80 available)\n• **BoomBox 20W Portable Bluetooth Speaker** (`PROD-011`) by *SonicBlast* — **₹2,799.00** (MRP: ₹3,999.00, 30.0% off)\n   Status: *IN_STOCK* (50 available)\n• **StudioPro Vocal Condenser USB Microphone with Arm Stand** (`PROD-039`) by *SoundWave* — **₹4,499.00** (MRP: ₹6,999.00, 35.7% off)\n   Status: *IN_STOCK* (20 available)\n\n### ⚡ Electronics\n• **BeardMaster Pro Cordless Beard Trimmer (0.5 - 20 mm)** (`PROD-031`) by *GroomCraft* — **₹1,699.00** (MRP: ₹2,499.00, 32.0% off)\n   Status: *IN_STOCK* (40 available)\n• **HydroSonic Sonic Electric Toothbrush with 4 Brush Heads** (`PROD-032`) by *HydroSonic* — **₹2,299.00** (MRP: ₹3,999.00, 42.5% off)\n   Status: *IN_STOCK* (30 available)\n• **SilkTouch Salon Hair Dryer 2000W with Ionic Care** (`PROD-033`) by *GroomCraft* — **₹2,199.00** (MRP: ₹3,499.00, 37.2% off)\n   Status: *IN_STOCK* (25 available)\n• **Vitamin C 10% Brightening Glow Face Serum (30 ml)** (`PROD-034`) by *GlowBotanica* — **₹549.00** (MRP: ₹799.00, 31.3% off)\n   Status: *IN_STOCK* (90 available)\n• **Ultra-Hydrating Ceramide Barrier Face Cream (50 g)** (`PROD-035`) by *GlowBotanica* — **₹499.00** (MRP: ₹699.00, 28.6% off)\n   Status: *IN_STOCK* (60 available)\n• **Anti-Dandruff Tea Tree & Salicylic Acid Shampoo (250 ml)** (`PROD-036`) by *RootCare* — **₹419.00** (MRP: ₹599.00, 30.1% off)\n   Status: *IN_STOCK* (75 available)\n• **Daily Invisible Matte Sunscreen Gel SPF 50 PA++++ (50g)** (`PROD-037`) by *GlowBotanica* — **₹479.00** (MRP: ₹649.00, 26.2% off)\n   Status: *IN_STOCK* (100 available)\n\n💡 *Ask me about any specific Product ID or model for warranty, return policies, and full technical specifications!*	\N	2026-09-14 16:18:43.861694	\N	\N
9bca5bf3-f660-4878-b077-292dbe583ae1	5faee52b-bcd9-442b-9136-148790eba194	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	tell me every products for Home usages	\N	2026-09-14 16:20:07.837615	\N	\N
65a42c31-b206-4d3b-85ac-2f0a9595924c	5faee52b-bcd9-442b-9136-148790eba194	\N	ai	Found 12 matching product(s) across 4 categories in our store:\n\n### 🍳 Kitchen & Dining\n• **ChefPro 1000W 4-Jar Mixer Grinder** (`PROD-012`) by *ChefPro* — **₹4,799.00** (MRP: ₹6,999.00, 31.4% off)\n   Status: *IN_STOCK* (35 available)\n• **CrispAir Digital 4.5L Air Fryer (Rapid Air Tech)** (`PROD-013`) by *CrispAir* — **₹5,999.00** (MRP: ₹8,499.00, 29.4% off)\n   Status: *IN_STOCK* (20 available)\n• **Hard Anodized 3-Piece Cookware Set (Kadai, Fry Pan, Tawa)** (`PROD-014`) by *KitchenCraft* — **₹2,899.00** (MRP: ₹4,299.00, 32.6% off)\n   Status: *IN_STOCK* (40 available)\n• **Stainless Steel Thermal Insulated Water Bottle 1000ml** (`PROD-038`) by *HydroFlasker* — **₹899.00** (MRP: ₹1,499.00, 40.0% off)\n   Status: *IN_STOCK* (60 available)\n\n### 🪑 Home Furniture\n• **ErgoRest High-Back Ergonomic Office Chair** (`PROD-015`) by *ErgoRest* — **₹11,499.00** (MRP: ₹16,999.00, 32.4% off)\n   Status: *IN_STOCK* (18 available)\n• **Solid Sheesham Wood 4-Seater Dining Table Set** (`PROD-016`) by *RoyalTimber* — **₹26,999.00** (MRP: ₹38,999.00, 30.8% off)\n   Status: *IN_STOCK* (8 available)\n• **Modular Engineered Wood Study Desk (Columbian Walnut)** (`PROD-017`) by *UrbanSpace* — **₹5,499.00** (MRP: ₹8,999.00, 38.9% off)\n   Status: *IN_STOCK* (3 available)\n\n### 🏠 Home Appliances\n• **VisionPlus 55-inch 4K Ultra HD Smart Google TV** (`PROD-018`) by *VisionPlus* — **₹38,990.00** (MRP: ₹59,990.00, 35.0% off)\n   Status: *IN_STOCK* (22 available)\n• **PureBreeze HEPA Air Purifier for Home (CADR 350 m3/h)** (`PROD-019`) by *PureBreeze* — **₹10,999.00** (MRP: ₹15,999.00, 31.3% off)\n   Status: *IN_STOCK* (28 available)\n• **RoboClean 2-in-1 Robot Vacuum Cleaner & Mop** (`PROD-020`) by *RoboClean* — **₹19,999.00** (MRP: ₹29,999.00, 33.3% off)\n   Status: *IN_STOCK* (15 available)\n• **Smart Touch Instant Induction Cooktop 2100W** (`PROD-040`) by *ChefPro* — **₹2,899.00** (MRP: ₹4,499.00, 35.6% off)\n   Status: *IN_STOCK* (30 available)\n\n### 👟 Footwear\n• **CloudSlide Ergonomic EVA Comfort Flip-Flop Slides** (`PROD-030`) by *AirStride* — **₹699.00** (MRP: ₹1,299.00, 46.2% off)\n   Status: *IN_STOCK* (65 available)\n\n💡 *Ask me about any specific Product ID or model for warranty, return policies, and full technical specifications!*	\N	2026-09-14 16:20:25.955182	\N	\N
5750603e-0d40-499f-8482-90464d9d6de4	5faee52b-bcd9-442b-9136-148790eba194	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	tell me every products for gifting for men	\N	2026-09-14 16:21:40.57231	\N	\N
1c20ccd0-726f-4820-b21b-5558f2686066	5faee52b-bcd9-442b-9136-148790eba194	\N	ai	I was unable to locate the requested record in our system. Please check the ID or contact support.	\N	2026-09-14 16:21:50.583996	\N	\N
cb5ce6d8-d666-41ce-8a71-128e92e644dc	5faee52b-bcd9-442b-9136-148790eba194	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	tell me every products for gifting for men	\N	2026-09-14 16:22:09.031027	\N	\N
4761b746-1275-4bf2-873a-ca847f08adc1	5faee52b-bcd9-442b-9136-148790eba194	\N	ai	I was unable to locate the requested record in our system. Please check the ID or contact support.	\N	2026-09-14 16:22:19.815231	\N	\N
73f9f6a6-5672-4ea2-8faa-f914eb957fe8	507f5a74-e09d-461c-b387-1372a84094f2	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-14 16:22:27.641788	\N	\N
ca49d240-ca43-44a5-8ab1-b305c59291f5	507f5a74-e09d-461c-b387-1372a84094f2	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	tell me every products for gifting for men	\N	2026-09-14 16:22:31.121227	\N	\N
d7991a7d-8613-4551-8dfc-3d239e0e6dd2	507f5a74-e09d-461c-b387-1372a84094f2	\N	ai	I was unable to locate the requested record in our system. Please check the ID or contact support.	\N	2026-09-14 16:22:41.398032	\N	\N
c2067440-db20-46f1-8538-fa58b9ddd0ec	5faee52b-bcd9-442b-9136-148790eba194	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	tell me every products for gifting for men	\N	2026-09-14 16:33:59.540948	\N	\N
6526d839-7ebc-42cd-8857-5885101bd4db	5faee52b-bcd9-442b-9136-148790eba194	\N	ai	Found 5 matching product(s) across 2 categories in our store:\n\n### 👔 Men's Clothing\n• **Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)** (`PROD-021`) by *UrbanTrend* — **₹1,299.00** (MRP: ₹2,499.00, 48.0% off)\n   Status: *IN_STOCK* (55 available)\n• **Slim Fit Stretchable Denim Jeans (Dark Indigo)** (`PROD-022`) by *DenimCo* — **₹1,899.00** (MRP: ₹3,299.00, 42.4% off)\n   Status: *IN_STOCK* (40 available)\n• **Heavyweight Cotton Graphic Crewneck T-Shirt (Olive)** (`PROD-023`) by *UrbanTrend* — **₹799.00** (MRP: ₹1,499.00, 46.7% off)\n   Status: *IN_STOCK* (70 available)\n• **Men's 3-Pack Modal Cotton Innerwear Boxer Briefs** (`PROD-024`) by *ComfyWear* — **₹899.00** (MRP: ₹1,299.00, 30.8% off)\n   Status: *IN_STOCK* (45 available)\n\n### ⚡ Electronics\n• **BeardMaster Pro Cordless Beard Trimmer (0.5 - 20 mm)** (`PROD-031`) by *GroomCraft* — **₹1,699.00** (MRP: ₹2,499.00, 32.0% off)\n   Status: *IN_STOCK* (40 available)\n\n💡 *Ask me about any specific Product ID or model for warranty, return policies, and full technical specifications!*	\N	2026-09-14 16:34:09.356722	\N	\N
abcf7403-8f47-4fe3-abd3-5223d290d222	5faee52b-bcd9-442b-9136-148790eba194	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	tell me every products for gifting for women	\N	2026-09-14 16:38:08.554213	\N	\N
ca704f4f-f0f8-4a17-ac51-fea25ce8235a	5faee52b-bcd9-442b-9136-148790eba194	\N	ai	Found 3 matching product(s) in our store:\n\n• **Floral Embroidered Chanderi Silk Kurta Set with Dupatta** (`PROD-025`) by *Riwayat Ethnic* — **₹3,499.00** (MRP: ₹5,999.00, 41.7% off)\n   Category: Women's Clothing | Status: *IN_STOCK* (30 available)\n• **Tiered A-Line Floral Summer Midi Dress (Pastel Sage)** (`PROD-026`) by *FloraBella* — **₹1,699.00** (MRP: ₹2,999.00, 43.3% off)\n   Category: Women's Clothing | Status: *IN_STOCK* (35 available)\n• **High-Waist Cotton Ankle Length Casual Trousers** (`PROD-027`) by *FloraBella* — **₹1,199.00** (MRP: ₹2,199.00, 45.5% off)\n   Category: Women's Clothing | Status: *IN_STOCK* (25 available)\n💡 *Ask me about any specific Product ID or model for warranty, return policies, and full technical specifications!*	\N	2026-09-14 16:38:14.359732	\N	\N
efa6a77e-f190-4cdc-a944-a8f1b2375d06	507f5a74-e09d-461c-b387-1372a84094f2	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks , my query is solved	\N	2026-09-14 16:45:55.144755	\N	\N
7ce7747d-5f95-4a84-a964-93e63d40333b	507f5a74-e09d-461c-b387-1372a84094f2	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-14 16:45:55.188356	\N	\N
77b8cec3-1f79-4c66-9e97-c1b79475e693	507f5a74-e09d-461c-b387-1372a84094f2	\N	ai	Your ticket [TCK-26948] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/507f5a74-e09d-461c-b387-1372a84094f2/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-14 16:45:55.208279	\N	\N
360da2f1-0f8a-4bce-97cb-f6aaf2309e61	aab74641-2a47-4a99-bbcd-a1c7fa2dac72	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks , my query is solved	\N	2026-09-14 16:46:22.519105	\N	\N
c142ae9b-dcf2-4f4b-a9a6-291d9fff2548	aab74641-2a47-4a99-bbcd-a1c7fa2dac72	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-14 16:46:22.548135	\N	\N
930e9efa-0472-4640-81a5-21c3c04b3b5f	aab74641-2a47-4a99-bbcd-a1c7fa2dac72	\N	ai	Your ticket [TCK-82682] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/aab74641-2a47-4a99-bbcd-a1c7fa2dac72/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-14 16:46:22.549113	\N	\N
c9d847de-11d2-48ab-bb1c-7207ba63f3cf	641222a4-43a8-4138-acf9-f2bd23a72544	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks , my query is solved	\N	2026-09-14 16:46:44.035127	\N	\N
567057d9-b474-44b9-9d82-260747ede004	641222a4-43a8-4138-acf9-f2bd23a72544	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-14 16:46:44.081822	\N	\N
1c8ce518-4638-41cd-ab38-74820872a18b	641222a4-43a8-4138-acf9-f2bd23a72544	\N	ai	Your ticket [TCK-73337] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/641222a4-43a8-4138-acf9-f2bd23a72544/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-14 16:46:44.084074	\N	\N
ca11eac3-815d-47a8-bb69-03316c15e20a	096a4ed9-b378-49a4-b78b-ea3c45ab64df	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks , my query is solved	\N	2026-09-14 16:46:54.227882	\N	\N
b0733658-c8ad-4b88-a253-4c2034ba7664	096a4ed9-b378-49a4-b78b-ea3c45ab64df	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-14 16:46:54.25258	\N	\N
3c45153e-1872-47ca-94b9-dd46c81000c6	096a4ed9-b378-49a4-b78b-ea3c45ab64df	\N	ai	Your ticket [TCK-57249] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/096a4ed9-b378-49a4-b78b-ea3c45ab64df/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-14 16:46:54.253666	\N	\N
baf3a14f-cfba-4fc1-80b2-6fcd7ec08827	9f75302d-8a1a-44a8-8660-4969785ae442	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks , my query is solved	\N	2026-09-14 16:47:09.358917	\N	\N
27dd1dad-0bb2-4768-a609-bdd86a79c953	9f75302d-8a1a-44a8-8660-4969785ae442	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-14 16:47:09.410771	\N	\N
bbf04ccc-5292-4c6f-a49a-7fd3aad613b4	9f75302d-8a1a-44a8-8660-4969785ae442	\N	ai	Your ticket [TCK-40503] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/9f75302d-8a1a-44a8-8660-4969785ae442/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-14 16:47:09.413063	\N	\N
1c9f6c05-9df4-4b92-b53f-72bddd3fa851	5faee52b-bcd9-442b-9136-148790eba194	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i want to talk with humen agent!	\N	2026-09-14 17:06:49.861161	\N	\N
b1ea06c5-0053-4a01-859e-a79f0ce248e7	5faee52b-bcd9-442b-9136-148790eba194	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?	\N	2026-09-14 17:06:50.372356	\N	\N
55171e57-7305-43f5-a9c9-9ba424b35fa0	ea6e1612-4f0e-4925-9ced-2aa4693087f2	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-14 17:12:42.388421	\N	\N
e62fb259-6203-4a99-a272-24b53ee4e488	ea6e1612-4f0e-4925-9ced-2aa4693087f2	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	tell me aout my product of order-001	\N	2026-09-14 17:13:01.601981	\N	\N
4a60e527-14f3-4173-b1dc-a116db805f7c	ea6e1612-4f0e-4925-9ced-2aa4693087f2	\N	ai	Order **ORD-001** — Product Details\n\n📦 **Items Included:**\n• **NovaPhone Pro 5G (Midnight Black, 256 GB)**\n   SKU: `PROD-001` • Qty: 1 • Price: **₹46,999.00** (Total: **₹46,999.00**)\n\n📌 **Order Summary:**\n• Status: **DELIVERED**\n• Total Amount: **₹46,999.00**	\N	2026-09-14 17:13:01.728923	\N	\N
188b93e5-7ce6-4126-b6ad-372a803f3085	ea6e1612-4f0e-4925-9ced-2aa4693087f2	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thank you my query is solved	\N	2026-09-14 17:13:39.152367	\N	\N
0bd494ec-264b-4f9f-9c7d-37c226d85444	ea6e1612-4f0e-4925-9ced-2aa4693087f2	\N	ai	I'm glad to hear your issue has been resolved! I've marked this ticket as resolved. If you need any further assistance in the future, please feel free to reach out. Have a great day!	\N	2026-09-14 17:13:39.202391	\N	\N
4fba346c-ce37-4be1-b7a3-c737264ee5c0	ea6e1612-4f0e-4925-9ced-2aa4693087f2	\N	ai	Your ticket [TCK-85785] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/ea6e1612-4f0e-4925-9ced-2aa4693087f2/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-14 17:13:39.204846	\N	\N
742b47a5-09b7-446e-9bb6-ea978e411406	5faee52b-bcd9-442b-9136-148790eba194	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i want to talk with human customer agent	\N	2026-09-14 17:36:55.057711	\N	\N
bceed76e-6bf4-460d-9243-366647677c40	5faee52b-bcd9-442b-9136-148790eba194	\N	ai	I have transferred your request to our senior support team (HIGH priority: Customer explicitly requested transfer to a human support agent.). A human support representative is reviewing your case details and will assist you shortly.	\N	2026-09-14 17:36:55.121531	\N	\N
bacdbf88-0250-45f3-b7f0-7bc165bbea62	5713519c-e2f1-4348-b11a-83e01d622160	646b7a11-99f7-4721-b183-f74dbec4bcc5	agent	Reference: Order Cancellation & Refund Timelines (POL-002) - Cancellation rules before dispatch and automatic UPI/Card refund timelines (5-7 business days).	\N	2026-09-14 17:51:24.386273	\N	\N
0ad072af-63d4-4ee4-b643-2ec6eff99ab3	5713519c-e2f1-4348-b11a-83e01d622160	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks , i got my answer	\N	2026-09-14 17:52:34.602461	\N	\N
59b53886-1db3-4c18-96e4-b292295cc1ce	5713519c-e2f1-4348-b11a-83e01d622160	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?	\N	2026-09-14 17:52:35.603205	\N	\N
436adb21-982f-48b0-bbf0-ddafaa7e35f2	7eb9c8b6-fa52-4022-b221-01198ce8d403	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	what is your return policy	\N	2026-09-15 14:45:44.857778	\N	\N
5918bd4a-9216-45d1-81d9-f6aa588dcd05	5713519c-e2f1-4348-b11a-83e01d622160	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	thanks , i got my answer	\N	2026-09-14 17:59:36.273775	\N	\N
1718ad1c-0dde-44de-b93f-208c2e9f6eaa	5713519c-e2f1-4348-b11a-83e01d622160	\N	ai	I'm glad to hear that you got your answer and your issue has been resolved! I have marked this ticket as completed and resolved. If you need any further assistance in the future, please feel free to reach out anytime. Have a wonderful day!	\N	2026-09-14 17:59:36.988618	\N	\N
eaa9d715-254b-4a0e-8e32-44871a50ec84	5713519c-e2f1-4348-b11a-83e01d622160	\N	ai	Your ticket [TCK-66901] has been resolved.\n\nHow would you rate your support experience today?\nPlease click the link below to submit your rating (1-5):\nhttp://localhost:8000/api/v1/tickets/5713519c-e2f1-4348-b11a-83e01d622160/rate-email?rating=5\nWe appreciate your feedback!	\N	2026-09-14 17:59:36.989528	\N	\N
522c1ed3-8f76-4660-a031-9ba1ccf3ead1	1af2296b-f1ed-435f-ab75-e36bc02a47aa	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-15 12:10:53.153514	\N	\N
b3adcb5c-35e2-4a2b-9036-ceaf278444ca	1af2296b-f1ed-435f-ab75-e36bc02a47aa	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me info. of PROD-001	\N	2026-09-15 12:11:07.037002	\N	\N
208feb1e-e11e-40b8-930d-35c4b5a2ef6d	1af2296b-f1ed-435f-ab75-e36bc02a47aa	\N	ai	Product: NovaPhone Pro 5G (Midnight Black, 256 GB) (PROD-001) by NovaPhone.\nPrice: ₹46,999.00 (MRP: ₹54,999.00, Discount: 14.5%).\nAvailability: IN_STOCK (In Stock: 45).	\N	2026-09-15 12:11:12.985961	\N	\N
2c86c946-86c1-4c0e-9c7c-a31bcf1b6296	1af2296b-f1ed-435f-ab75-e36bc02a47aa	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me info. of PROD-001	\N	2026-09-15 12:23:32.057415	\N	\N
eec262ac-1eac-4db4-97bb-421d8a6d4be8	1af2296b-f1ed-435f-ab75-e36bc02a47aa	\N	ai	Product: **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) by **NovaPhone**.\nCategory: Mobiles & Tablets (`CAT-002`)\n\n📝 **Overview:**\nFlagship 5G smartphone with 120Hz AMOLED display, 50MP triple camera, and 5000mAh battery.\n\n💰 **Pricing & Availability:**\n• **Price:** ₹46,999.00 (MRP: ₹54,999.00, Discount: 14.5%)\n• **Availability:** IN_STOCK (In Stock: 45)\n\n⚙️ **Technical Specifications:**\n• **RAM:** 8 GB\n• **Color:** Midnight Black\n• **Battery:** 5000 mAh\n• **Processor:** Snapdragon 8 Gen 2\n• **5G Support:** Yes\n• **Screen Size:** 6.7 inches\n• **Internal Storage:** 256 GB\n\n🛡️ **Policies & Store Details:**\n• **Return Policy:** Eligible for return within 7 days\n• **Warranty:** Standard manufacturer coverage\n• **Reference IDs:** Seller ID: `SELL-001` • Company ID: `COMP-001`	\N	2026-09-15 12:23:46.48707	\N	\N
4db02de5-9859-40d4-91a4-4ee28f00b6d8	d48d3479-0618-4201-8d9a-515a666d1cae	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-15 12:25:28.449805	\N	\N
8e9f331d-0af5-424a-8aa5-bd2d6579414a	d48d3479-0618-4201-8d9a-515a666d1cae	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me info. of NovaPhone Pro 5G	\N	2026-09-15 12:25:42.907921	\N	\N
417bd593-a79b-43be-b03c-2ce15c9f54d3	d48d3479-0618-4201-8d9a-515a666d1cae	\N	ai	Found 1 matching product(s) in our store:\n\n• **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) by *NovaPhone* — **₹46,999.00** (MRP: ₹54,999.00, 14.5% off)\n   Category: Mobiles & Tablets | Status: *IN_STOCK* (45 available)\n💡 *Ask me about any specific Product ID or model for warranty, return policies, and full technical specifications!*	\N	2026-09-15 12:25:54.436948	\N	\N
7951c928-4922-4330-a83a-74a22e17c238	d48d3479-0618-4201-8d9a-515a666d1cae	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me info. of NovaPhone Pro 5G	\N	2026-09-15 13:16:18.612525	\N	\N
00874975-7b21-4ca2-bc28-4deca938dbaa	d48d3479-0618-4201-8d9a-515a666d1cae	\N	ai	Product: **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) by **NovaPhone**.\nCategory: Mobiles & Tablets (`CAT-002`)\n\n📝 **Overview:**\nFlagship 5G smartphone with 120Hz AMOLED display, 50MP triple camera, and 5000mAh battery.\n\n💰 **Pricing & Availability:**\n• **Price:** ₹46,999.00 (MRP: ₹54,999.00, Discount: 14.5%)\n• **Availability:** IN_STOCK (In Stock: 45)\n\n⚙️ **Technical Specifications:**\n• **RAM:** 8 GB\n• **Color:** Midnight Black\n• **Battery:** 5000 mAh\n• **Processor:** Snapdragon 8 Gen 2\n• **5G Support:** Yes\n• **Screen Size:** 6.7 inches\n• **Internal Storage:** 256 GB\n\n🛡️ **Policies & Store Details:**\n• **Return Policy:** Eligible for return within 7 days\n• **Warranty:** Standard manufacturer coverage\n• **Reference IDs:** Seller ID: `SELL-001` • Company ID: `COMP-001`	\N	2026-09-15 13:16:28.419102	\N	\N
264b0188-dad5-4b70-81db-79222567b51b	48136439-fab6-4224-ae17-3fb3ca6a3a97	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-15 13:49:33.840266	\N	\N
14173b51-d274-4cea-a30c-ebf03aa3f27d	48136439-fab6-4224-ae17-3fb3ca6a3a97	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me info. of NovaPhone Pro 5G	\N	2026-09-15 13:49:39.695521	\N	\N
2214d319-3908-495b-bd78-2fc083ddf847	48136439-fab6-4224-ae17-3fb3ca6a3a97	\N	ai	Here is an overview of popular products currently available in our ShopKart catalog:\n\n### 📱 Mobiles & Tablets\n• **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) — **₹46,999.00** (14.5% off) | Status: *IN_STOCK* (45 in stock)\n• **AeroTab Air 11-inch Wi-Fi Tablet (Space Grey, 128 GB)** (`PROD-002`) — **₹27,499.00** (16.7% off) | Status: *IN_STOCK* (4 in stock)\n• **Pixelite 4G Budget Smartphone (Ocean Blue, 64 GB)** (`PROD-003`) — **₹7,999.00** (20.0% off) | Status: *OUT_OF_STOCK* (0 in stock)\n• **ClassicTouch Keypad Phone V1** (`PROD-004`) — **₹1,499.00** (25.0% off) | Status: *OUT_OF_STOCK* (0 in stock)\n\n### 💻 Laptops & Computers\n• **ZenBook Ultra 14 Thin & Light Laptop (16GB/512GB SSD/Intel Core i7)** (`PROD-005`) — **₹78,990.00** (12.2% off) | Status: *IN_STOCK* (25 in stock)\n• **GamerX Legion RTX 4060 Gaming Laptop (16GB/1TB SSD)** (`PROD-006`) — **₹109,990.00** (12.0% off) | Status: *IN_STOCK* (12 in stock)\n• **ProView 27-inch 4K UHD IPS Monitor** (`PROD-007`) — **₹23,999.00** (20.0% off) | Status: *IN_STOCK* (30 in stock)\n• **ErgoSilent Wireless Keyboard & Mouse Combo** (`PROD-008`) — **₹2,499.00** (28.6% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🎧 Audio & Headphones\n• **SoundWave ANC 750 Over-Ear Wireless Headphones** (`PROD-009`) — **₹9,999.00** (33.3% off) | Status: *IN_STOCK* (40 in stock)\n• **AirBuds Pro True Wireless Earbuds with Dual Mic** (`PROD-010`) — **₹2,499.00** (50.0% off) | Status: *IN_STOCK* (80 in stock)\n• **BoomBox 20W Portable Bluetooth Speaker** (`PROD-011`) — **₹2,799.00** (30.0% off) | Status: *IN_STOCK* (50 in stock)\n• **StudioPro Vocal Condenser USB Microphone with Arm Stand** (`PROD-039`) — **₹4,499.00** (35.7% off) | Status: *IN_STOCK* (20 in stock)\n\n### 🍳 Kitchen & Dining\n• **ChefPro 1000W 4-Jar Mixer Grinder** (`PROD-012`) — **₹4,799.00** (31.4% off) | Status: *IN_STOCK* (35 in stock)\n• **CrispAir Digital 4.5L Air Fryer (Rapid Air Tech)** (`PROD-013`) — **₹5,999.00** (29.4% off) | Status: *IN_STOCK* (20 in stock)\n• **Hard Anodized 3-Piece Cookware Set (Kadai, Fry Pan, Tawa)** (`PROD-014`) — **₹2,899.00** (32.6% off) | Status: *IN_STOCK* (40 in stock)\n• **Stainless Steel Thermal Insulated Water Bottle 1000ml** (`PROD-038`) — **₹899.00** (40.0% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🪑 Home Furniture\n• **ErgoRest High-Back Ergonomic Office Chair** (`PROD-015`) — **₹11,499.00** (32.4% off) | Status: *IN_STOCK* (18 in stock)\n• **Solid Sheesham Wood 4-Seater Dining Table Set** (`PROD-016`) — **₹26,999.00** (30.8% off) | Status: *IN_STOCK* (8 in stock)\n• **Modular Engineered Wood Study Desk (Columbian Walnut)** (`PROD-017`) — **₹5,499.00** (38.9% off) | Status: *IN_STOCK* (3 in stock)\n\n### 🏠 Home Appliances\n• **VisionPlus 55-inch 4K Ultra HD Smart Google TV** (`PROD-018`) — **₹38,990.00** (35.0% off) | Status: *IN_STOCK* (22 in stock)\n• **PureBreeze HEPA Air Purifier for Home (CADR 350 m3/h)** (`PROD-019`) — **₹10,999.00** (31.3% off) | Status: *IN_STOCK* (28 in stock)\n• **RoboClean 2-in-1 Robot Vacuum Cleaner & Mop** (`PROD-020`) — **₹19,999.00** (33.3% off) | Status: *IN_STOCK* (15 in stock)\n• **Smart Touch Instant Induction Cooktop 2100W** (`PROD-040`) — **₹2,899.00** (35.6% off) | Status: *IN_STOCK* (30 in stock)\n\n### 👔 Men's Clothing\n• **Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)** (`PROD-021`) — **₹1,299.00** (48.0% off) | Status: *IN_STOCK* (55 in stock)\n• **Slim Fit Stretchable Denim Jeans (Dark Indigo)** (`PROD-022`) — **₹1,899.00** (42.4% off) | Status: *IN_STOCK* (40 in stock)\n• **Heavyweight Cotton Graphic Crewneck T-Shirt (Olive)** (`PROD-023`) — **₹799.00** (46.7% off) | Status: *IN_STOCK* (70 in stock)\n• **Men's 3-Pack Modal Cotton Innerwear Boxer Briefs** (`PROD-024`) — **₹899.00** (30.8% off) | Status: *IN_STOCK* (45 in stock)\n\n### 👔 Women's Clothing\n• **Floral Embroidered Chanderi Silk Kurta Set with Dupatta** (`PROD-025`) — **₹3,499.00** (41.7% off) | Status: *IN_STOCK* (30 in stock)\n• **Tiered A-Line Floral Summer Midi Dress (Pastel Sage)** (`PROD-026`) — **₹1,699.00** (43.3% off) | Status: *IN_STOCK* (35 in stock)\n• **High-Waist Cotton Ankle Length Casual Trousers** (`PROD-027`) — **₹1,199.00** (45.5% off) | Status: *IN_STOCK* (25 in stock)\n\n### 👟 Footwear\n• **AirStride Pro Lightweight Road Running Shoes** (`PROD-028`) — **₹4,299.00** (33.9% off) | Status: *IN_STOCK* (50 in stock)\n• **Handcrafted Genuine Leather Formal Derby Shoes (Tan)** (`PROD-029`) — **₹3,699.00** (32.7% off) | Status: *IN_STOCK* (25 in stock)\n• **CloudSlide Ergonomic EVA Comfort Flip-Flop Slides** (`PROD-030`) — **₹699.00** (46.2% off) | Status: *IN_STOCK* (65 in stock)\n\n### ⚡ Electronics\n• **BeardMaster Pro Cordless Beard Trimmer (0.5 - 20 mm)** (`PROD-031`) — **₹1,699.00** (32.0% off) | Status: *IN_STOCK* (40 in stock)\n• **HydroSonic Sonic Electric Toothbrush with 4 Brush Heads** (`PROD-032`) — **₹2,299.00** (42.5% off) | Status: *IN_STOCK* (30 in stock)\n• **SilkTouch Salon Hair Dryer 2000W with Ionic Care** (`PROD-033`) — **₹2,199.00** (37.2% off) | Status: *IN_STOCK* (25 in stock)\n• **Vitamin C 10% Brightening Glow Face Serum (30 ml)** (`PROD-034`) — **₹549.00** (31.3% off) | Status: *IN_STOCK* (90 in stock)\n• **Ultra-Hydrating Ceramide Barrier Face Cream (50 g)** (`PROD-035`) — **₹499.00** (28.6% off) | Status: *IN_STOCK* (60 in stock)\n• **Anti-Dandruff Tea Tree & Salicylic Acid Shampoo (250 ml)** (`PROD-036`) — **₹419.00** (30.1% off) | Status: *IN_STOCK* (75 in stock)\n• **Daily Invisible Matte Sunscreen Gel SPF 50 PA++++ (50g)** (`PROD-037`) — **₹479.00** (26.2% off) | Status: *IN_STOCK* (100 in stock)\n\n💡 *Tip: Ask for full specs, pricing, or warranty details on any item by specifying its name or ID (e.g., `Tell me about PROD-001`).*	\N	2026-09-15 13:54:08.892755	\N	\N
8a1914c4-d8c7-4d60-a745-57fa2615f57d	7eb9c8b6-fa52-4022-b221-01198ce8d403	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i want to talk with customer agent	\N	2026-09-15 14:46:07.692382	\N	\N
2ca0c642-e727-4932-9f38-1a492dcc8c9a	48136439-fab6-4224-ae17-3fb3ca6a3a97	\N	ai	Product: **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) by **NovaPhone**.\nCategory: Mobiles & Tablets (`CAT-002`)\n\n📝 **Overview:**\nFlagship 5G smartphone with 120Hz AMOLED display, 50MP triple camera, and 5000mAh battery.\n\n💰 **Pricing & Availability:**\n• **Price:** ₹46,999.00 (MRP: ₹54,999.00, Discount: 14.5%)\n• **Availability:** IN_STOCK (In Stock: 45)\n\n⚙️ **Technical Specifications:**\n• **RAM:** 8 GB\n• **Color:** Midnight Black\n• **Battery:** 5000 mAh\n• **Processor:** Snapdragon 8 Gen 2\n• **5G Support:** Yes\n• **Screen Size:** 6.7 inches\n• **Internal Storage:** 256 GB\n\n🛡️ **Policies & Store Details:**\n• **Return Policy:** Eligible for return within 7 days\n• **Warranty:** Standard manufacturer coverage\n• **Reference IDs:** Seller ID: `SELL-001` • Company ID: `COMP-001`	\N	2026-09-15 13:49:46.664059	\N	\N
2618b72a-23be-4a93-83d2-8382ce406d8b	48136439-fab6-4224-ae17-3fb3ca6a3a97	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all products info.	\N	2026-09-15 13:54:05.963117	\N	\N
5ecf19d8-6009-4c6b-945b-a3949c6c5ef2	b7d31821-eb98-43e9-9a03-a18455a7ba98	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-15 13:54:52.590918	\N	\N
8368ce76-a4cd-4d29-9df3-a6619b98b89a	b7d31821-eb98-43e9-9a03-a18455a7ba98	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info. for Classic Fit 100% Pure Cotton Oxford Shirt	\N	2026-09-15 13:55:06.036757	\N	\N
9e970f5c-ee49-4555-8d78-877d850bc949	b7d31821-eb98-43e9-9a03-a18455a7ba98	\N	ai	I am your ShopKart AI Customer Support assistant. I specialize in helping you with orders, deliveries, returns, refunds, product specifications, and shopping policies. How may I assist you with your ShopKart order or account today?	\N	2026-09-15 13:55:06.628613	\N	\N
ef6fa49b-c6c1-45d0-8f4b-eaeff15a6d4d	b7d31821-eb98-43e9-9a03-a18455a7ba98	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info. for Classic Fit 100% Pure Cotton Oxford Shirt	\N	2026-09-15 14:01:54.684185	\N	\N
7e16b189-ba64-4044-80f3-25e7eb7b2bb2	b7d31821-eb98-43e9-9a03-a18455a7ba98	\N	ai	Product: **Men's 3-Pack Modal Cotton Innerwear Boxer Briefs** (`PROD-024`) by **ComfyWear**.\nCategory: Men's Clothing (`CAT-010`)\n\n📝 **Overview:**\nUltra-soft antimicrobial modal fabric boxer briefs with anti-chafing waistband.\n\n💰 **Pricing & Availability:**\n• **Price:** ₹899.00 (MRP: ₹1,299.00, Discount: 30.8%)\n• **Availability:** IN_STOCK (In Stock: 45)\n\n⚙️ **Technical Specifications:**\n• **Material:** 92% MicroModal, 8% Spandex\n• **Pack Size:** 3\n• **Hygiene Policy:** Non-Returnable for hygiene reasons\n\n🛡️ **Policies & Store Details:**\n• **Return Policy:** Eligible for return within 7 days\n• **Warranty:** Standard manufacturer coverage\n• **Reference IDs:** Seller ID: `SELL-004` • Company ID: `COMP-001`	\N	2026-09-15 14:02:03.766596	\N	\N
c11e1dbc-1b34-4c8e-9860-a423bc68bed3	a88fe49f-6444-49c4-bfc2-b465c1e543e2	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-15 14:02:25.044683	\N	\N
4f9913d0-2b88-4e4a-a35a-6e6da3993b93	b7d31821-eb98-43e9-9a03-a18455a7ba98	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me info. of product-021	\N	2026-09-15 14:03:58.497781	\N	\N
658c3af6-ad98-4270-87ed-e224f37f611e	b7d31821-eb98-43e9-9a03-a18455a7ba98	\N	ai	Product: **Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)** (`PROD-021`) by **UrbanTrend**.\nCategory: Men's Clothing (`CAT-010`)\n\n📝 **Overview:**\nBreathable premium combed cotton casual button-down shirt with curved hemline.\n\n💰 **Pricing & Availability:**\n• **Price:** ₹1,299.00 (MRP: ₹2,499.00, Discount: 48.0%)\n• **Availability:** IN_STOCK (In Stock: 55)\n\n⚙️ **Technical Specifications:**\n• **Fit:** Regular Fit\n• **Care:** Machine Wash Warm\n• **Collar:** Button Down\n• **Fabric:** 100% Combed Cotton\n• **Sleeve:** Full Sleeve\n\n🛡️ **Policies & Store Details:**\n• **Return Policy:** Eligible for return within 7 days\n• **Warranty:** Standard manufacturer coverage\n• **Reference IDs:** Seller ID: `SELL-001` • Company ID: `COMP-001`	\N	2026-09-15 14:04:12.770403	\N	\N
cd2ae1aa-32db-4194-b341-ed2a46e0ff5b	b7d31821-eb98-43e9-9a03-a18455a7ba98	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info. for Classic Fit 100% Pure Cotton Oxford Shirt	\N	2026-09-15 14:04:35.315584	\N	\N
a52a9f53-106c-4559-80fb-5e5e20943364	b7d31821-eb98-43e9-9a03-a18455a7ba98	\N	ai	Product: **Men's 3-Pack Modal Cotton Innerwear Boxer Briefs** (`PROD-024`) by **ComfyWear**.\nCategory: Men's Clothing (`CAT-010`)\n\n📝 **Overview:**\nUltra-soft antimicrobial modal fabric boxer briefs with anti-chafing waistband.\n\n💰 **Pricing & Availability:**\n• **Price:** ₹899.00 (MRP: ₹1,299.00, Discount: 30.8%)\n• **Availability:** IN_STOCK (In Stock: 45)\n\n⚙️ **Technical Specifications:**\n• **Material:** 92% MicroModal, 8% Spandex\n• **Pack Size:** 3\n• **Hygiene Policy:** Non-Returnable for hygiene reasons\n\n🛡️ **Policies & Store Details:**\n• **Return Policy:** Eligible for return within 7 days\n• **Warranty:** Standard manufacturer coverage\n• **Reference IDs:** Seller ID: `SELL-004` • Company ID: `COMP-001`	\N	2026-09-15 14:04:41.456345	\N	\N
6c630dcf-0b89-45bf-8ed4-281d44dd843c	b7d31821-eb98-43e9-9a03-a18455a7ba98	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info. for Classic Fit 100% Pure Cotton Oxford Shirt	\N	2026-09-15 14:28:59.751063	\N	\N
49026018-f86a-4671-9fa1-4e1d2b82d7d7	b7d31821-eb98-43e9-9a03-a18455a7ba98	\N	ai	Product: **Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)** (`PROD-021`) by **UrbanTrend**.\nCategory: Men's Clothing (`CAT-010`)\n\n📝 **Overview:**\nBreathable premium combed cotton casual button-down shirt with curved hemline.\n\n💰 **Pricing & Availability:**\n• **Price:** ₹1,299.00 (MRP: ₹2,499.00, Discount: 48.0%)\n• **Availability:** IN_STOCK (In Stock: 55)\n\n⚙️ **Technical Specifications:**\n• **Fit:** Regular Fit\n• **Care:** Machine Wash Warm\n• **Collar:** Button Down\n• **Fabric:** 100% Combed Cotton\n• **Sleeve:** Full Sleeve\n\n🛡️ **Policies & Store Details:**\n• **Return Policy:** Eligible for return within 7 days\n• **Warranty:** Standard manufacturer coverage\n• **Reference IDs:** Seller ID: `SELL-001` • Company ID: `COMP-001`	\N	2026-09-15 14:29:03.334804	\N	\N
cff95161-d026-4921-8c45-847763a6860d	7eb9c8b6-fa52-4022-b221-01198ce8d403	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Where is my order?	\N	2026-09-15 14:43:24.945379	\N	\N
a595489a-d053-416b-87f7-1c95afc0e2a3	7eb9c8b6-fa52-4022-b221-01198ce8d403	\N	ai	Your order ORD-001 is currently **DELIVERED** with Delhivery (Tracking: TRK-DELHIVERY-764130526). Estimated delivery: 2026-08-19.	\N	2026-09-15 14:43:24.970059	\N	\N
1aa27a7c-4ec0-4416-91d2-424ec9a91f4d	7eb9c8b6-fa52-4022-b221-01198ce8d403	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all products info.	\N	2026-09-15 14:43:50.705744	\N	\N
b2f9dbe3-107d-456c-805f-3bdb3dbaca14	7eb9c8b6-fa52-4022-b221-01198ce8d403	\N	ai	Here is an overview of popular products currently available in our ShopKart catalog:\n\n### 📱 Mobiles & Tablets\n• **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) — **₹46,999.00** (14.5% off) | Status: *IN_STOCK* (45 in stock)\n• **AeroTab Air 11-inch Wi-Fi Tablet (Space Grey, 128 GB)** (`PROD-002`) — **₹27,499.00** (16.7% off) | Status: *IN_STOCK* (4 in stock)\n• **Pixelite 4G Budget Smartphone (Ocean Blue, 64 GB)** (`PROD-003`) — **₹7,999.00** (20.0% off) | Status: *OUT_OF_STOCK* (0 in stock)\n• **ClassicTouch Keypad Phone V1** (`PROD-004`) — **₹1,499.00** (25.0% off) | Status: *OUT_OF_STOCK* (0 in stock)\n\n### 💻 Laptops & Computers\n• **ZenBook Ultra 14 Thin & Light Laptop (16GB/512GB SSD/Intel Core i7)** (`PROD-005`) — **₹78,990.00** (12.2% off) | Status: *IN_STOCK* (25 in stock)\n• **GamerX Legion RTX 4060 Gaming Laptop (16GB/1TB SSD)** (`PROD-006`) — **₹109,990.00** (12.0% off) | Status: *IN_STOCK* (12 in stock)\n• **ProView 27-inch 4K UHD IPS Monitor** (`PROD-007`) — **₹23,999.00** (20.0% off) | Status: *IN_STOCK* (30 in stock)\n• **ErgoSilent Wireless Keyboard & Mouse Combo** (`PROD-008`) — **₹2,499.00** (28.6% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🎧 Audio & Headphones\n• **SoundWave ANC 750 Over-Ear Wireless Headphones** (`PROD-009`) — **₹9,999.00** (33.3% off) | Status: *IN_STOCK* (40 in stock)\n• **AirBuds Pro True Wireless Earbuds with Dual Mic** (`PROD-010`) — **₹2,499.00** (50.0% off) | Status: *IN_STOCK* (80 in stock)\n• **BoomBox 20W Portable Bluetooth Speaker** (`PROD-011`) — **₹2,799.00** (30.0% off) | Status: *IN_STOCK* (50 in stock)\n• **StudioPro Vocal Condenser USB Microphone with Arm Stand** (`PROD-039`) — **₹4,499.00** (35.7% off) | Status: *IN_STOCK* (20 in stock)\n\n### 🍳 Kitchen & Dining\n• **ChefPro 1000W 4-Jar Mixer Grinder** (`PROD-012`) — **₹4,799.00** (31.4% off) | Status: *IN_STOCK* (35 in stock)\n• **CrispAir Digital 4.5L Air Fryer (Rapid Air Tech)** (`PROD-013`) — **₹5,999.00** (29.4% off) | Status: *IN_STOCK* (20 in stock)\n• **Hard Anodized 3-Piece Cookware Set (Kadai, Fry Pan, Tawa)** (`PROD-014`) — **₹2,899.00** (32.6% off) | Status: *IN_STOCK* (40 in stock)\n• **Stainless Steel Thermal Insulated Water Bottle 1000ml** (`PROD-038`) — **₹899.00** (40.0% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🪑 Home Furniture\n• **ErgoRest High-Back Ergonomic Office Chair** (`PROD-015`) — **₹11,499.00** (32.4% off) | Status: *IN_STOCK* (18 in stock)\n• **Solid Sheesham Wood 4-Seater Dining Table Set** (`PROD-016`) — **₹26,999.00** (30.8% off) | Status: *IN_STOCK* (8 in stock)\n• **Modular Engineered Wood Study Desk (Columbian Walnut)** (`PROD-017`) — **₹5,499.00** (38.9% off) | Status: *IN_STOCK* (3 in stock)\n\n### 🏠 Home Appliances\n• **VisionPlus 55-inch 4K Ultra HD Smart Google TV** (`PROD-018`) — **₹38,990.00** (35.0% off) | Status: *IN_STOCK* (22 in stock)\n• **PureBreeze HEPA Air Purifier for Home (CADR 350 m3/h)** (`PROD-019`) — **₹10,999.00** (31.3% off) | Status: *IN_STOCK* (28 in stock)\n• **RoboClean 2-in-1 Robot Vacuum Cleaner & Mop** (`PROD-020`) — **₹19,999.00** (33.3% off) | Status: *IN_STOCK* (15 in stock)\n• **Smart Touch Instant Induction Cooktop 2100W** (`PROD-040`) — **₹2,899.00** (35.6% off) | Status: *IN_STOCK* (30 in stock)\n\n### 👔 Men's Clothing\n• **Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)** (`PROD-021`) — **₹1,299.00** (48.0% off) | Status: *IN_STOCK* (55 in stock)\n• **Slim Fit Stretchable Denim Jeans (Dark Indigo)** (`PROD-022`) — **₹1,899.00** (42.4% off) | Status: *IN_STOCK* (40 in stock)\n• **Heavyweight Cotton Graphic Crewneck T-Shirt (Olive)** (`PROD-023`) — **₹799.00** (46.7% off) | Status: *IN_STOCK* (70 in stock)\n• **Men's 3-Pack Modal Cotton Innerwear Boxer Briefs** (`PROD-024`) — **₹899.00** (30.8% off) | Status: *IN_STOCK* (45 in stock)\n\n### 👔 Women's Clothing\n• **Floral Embroidered Chanderi Silk Kurta Set with Dupatta** (`PROD-025`) — **₹3,499.00** (41.7% off) | Status: *IN_STOCK* (30 in stock)\n• **Tiered A-Line Floral Summer Midi Dress (Pastel Sage)** (`PROD-026`) — **₹1,699.00** (43.3% off) | Status: *IN_STOCK* (35 in stock)\n• **High-Waist Cotton Ankle Length Casual Trousers** (`PROD-027`) — **₹1,199.00** (45.5% off) | Status: *IN_STOCK* (25 in stock)\n\n### 👟 Footwear\n• **AirStride Pro Lightweight Road Running Shoes** (`PROD-028`) — **₹4,299.00** (33.9% off) | Status: *IN_STOCK* (50 in stock)\n• **Handcrafted Genuine Leather Formal Derby Shoes (Tan)** (`PROD-029`) — **₹3,699.00** (32.7% off) | Status: *IN_STOCK* (25 in stock)\n• **CloudSlide Ergonomic EVA Comfort Flip-Flop Slides** (`PROD-030`) — **₹699.00** (46.2% off) | Status: *IN_STOCK* (65 in stock)\n\n### ⚡ Electronics\n• **BeardMaster Pro Cordless Beard Trimmer (0.5 - 20 mm)** (`PROD-031`) — **₹1,699.00** (32.0% off) | Status: *IN_STOCK* (40 in stock)\n• **HydroSonic Sonic Electric Toothbrush with 4 Brush Heads** (`PROD-032`) — **₹2,299.00** (42.5% off) | Status: *IN_STOCK* (30 in stock)\n• **SilkTouch Salon Hair Dryer 2000W with Ionic Care** (`PROD-033`) — **₹2,199.00** (37.2% off) | Status: *IN_STOCK* (25 in stock)\n• **Vitamin C 10% Brightening Glow Face Serum (30 ml)** (`PROD-034`) — **₹549.00** (31.3% off) | Status: *IN_STOCK* (90 in stock)\n• **Ultra-Hydrating Ceramide Barrier Face Cream (50 g)** (`PROD-035`) — **₹499.00** (28.6% off) | Status: *IN_STOCK* (60 in stock)\n• **Anti-Dandruff Tea Tree & Salicylic Acid Shampoo (250 ml)** (`PROD-036`) — **₹419.00** (30.1% off) | Status: *IN_STOCK* (75 in stock)\n• **Daily Invisible Matte Sunscreen Gel SPF 50 PA++++ (50g)** (`PROD-037`) — **₹479.00** (26.2% off) | Status: *IN_STOCK* (100 in stock)\n\n💡 *Tip: Ask for full specs, pricing, or warranty details on any item by specifying its name or ID (e.g., `Tell me about PROD-001`).*	\N	2026-09-15 14:43:53.740421	\N	\N
a5346904-0b5a-40bd-8ba7-5117335a3fd0	7eb9c8b6-fa52-4022-b221-01198ce8d403	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info. of my all orders	\N	2026-09-15 14:44:15.344553	\N	\N
02285332-268d-4b8f-98b8-5e24ad6f12e6	7eb9c8b6-fa52-4022-b221-01198ce8d403	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\nItems: NovaPhone Pro 5G (Midnight Black, 256 GB) (Qty 1).\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).\n\nOrder ORD-002 status: **DELIVERED** (Total: ₹12,498.00).\nItems: ErgoSilent Wireless Keyboard & Mouse Combo (Qty 1), SoundWave ANC 750 Over-Ear Wireless Headphones (Qty 1).\nShipment SHIP-002 for order ORD-002 is **DELIVERED** via BlueDart (Tracking: TRK-BLUEDART-488302652, Estimated Delivery: 2026-08-07).\n\nOrder ORD-025 status: **CONFIRMED** (Total: ₹2,899.00).\nItems: Smart Touch Instant Induction Cooktop 2100W (Qty 1).\nShipment SHIP-025 for order ORD-025 is **PROCESSING** via XpressBees (Tracking: TRK-XPRESSBEES-819595113, Estimated Delivery: 2026-08-23).	\N	2026-09-15 14:44:15.412729	\N	\N
34429d55-ea59-4a94-bfb0-7ae048ca72f9	7eb9c8b6-fa52-4022-b221-01198ce8d403	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info. for : NovaPhone Pro 5G	\N	2026-09-15 14:44:43.99699	\N	\N
02437634-abb6-4b46-a32a-8f79de6be7d0	7eb9c8b6-fa52-4022-b221-01198ce8d403	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	how can i return this product	\N	2026-09-15 14:45:12.548867	\N	\N
f0bbafe8-f904-49b3-8f7d-170fc933da0e	7eb9c8b6-fa52-4022-b221-01198ce8d403	\N	ai	Yes, **NovaPhone Pro 5G (Midnight Black, 256 GB)** (PROD-001) is eligible for return within **7 days** of delivery.\n\nItems must be unused, in original packaging with all tags intact. You can initiate a return directly from **My Orders**.	\N	2026-09-15 14:45:13.06695	\N	\N
1470f904-34f8-411d-ab28-e34efe96be82	7eb9c8b6-fa52-4022-b221-01198ce8d403	\N	ai	Product: **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) by **NovaPhone**.\nCategory: Mobiles & Tablets (`CAT-002`)\n\n📝 **Overview:**\nFlagship 5G smartphone with 120Hz AMOLED display, 50MP triple camera, and 5000mAh battery.\n\n💰 **Pricing & Availability:**\n• **Price:** ₹46,999.00 (MRP: ₹54,999.00, Discount: 14.5%)\n• **Availability:** IN_STOCK (In Stock: 45)\n\n⚙️ **Technical Specifications:**\n• **RAM:** 8 GB\n• **Color:** Midnight Black\n• **Battery:** 5000 mAh\n• **Processor:** Snapdragon 8 Gen 2\n• **5G Support:** Yes\n• **Screen Size:** 6.7 inches\n• **Internal Storage:** 256 GB\n\n🛡️ **Policies & Store Details:**\n• **Return Policy:** Eligible for return within 7 days\n• **Warranty:** Standard manufacturer coverage\n• **Reference IDs:** Seller ID: `SELL-001` • Company ID: `COMP-001`	\N	2026-09-15 14:44:44.170044	\N	\N
208a7947-3967-4749-af75-86d631d6d60d	7eb9c8b6-fa52-4022-b221-01198ce8d403	\N	ai	According to ShopKart's ShopKart Return Policy (POL-001):\n\n# ShopKart Return Policy\n\n### 1. General Return Window\nShopKart offers a return window on eligible items delivered to customers in India:\n- **Electronics & Mobiles:** 7 calendar days from delivery date.\n- **Home & Kitchen Appliances:** 7 to 10 calendar days from delivery date.\n- **Fashion & Footwear:** 15 calendar days from delivery date.\n- **Large Furniture:** 10 calendar days from delivery date.	\N	2026-09-15 14:45:45.05095	\N	\N
760f64b3-908a-4d66-848c-c1bcc74af32b	7eb9c8b6-fa52-4022-b221-01198ce8d403	\N	ai	I have transferred your request to our senior support team (HIGH priority: Customer explicitly requested transfer to a human support agent.). A human support representative is reviewing your case details and will assist you shortly.	\N	2026-09-15 14:46:07.848422	\N	\N
92145155-6c19-48fb-8bf2-aa9895697874	73603b79-147f-428f-845e-dfabe07404e7	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-15 16:16:19.881457	\N	\N
d7e122d2-48f4-4174-bd93-fdd75bf4deca	73603b79-147f-428f-845e-dfabe07404e7	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Give me info of my order-001	\N	2026-09-15 16:16:31.410286	\N	\N
082bbd49-c463-4fae-8a00-fe9c9147e9b4	73603b79-147f-428f-845e-dfabe07404e7	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\n\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).	\N	2026-09-15 16:16:31.480143	\N	\N
0b8b454f-6f29-4f48-a227-9b246557ffd3	73603b79-147f-428f-845e-dfabe07404e7	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info of my orders	\N	2026-09-15 16:17:02.401456	\N	\N
adef4c26-cad2-4d08-a13d-352fa917f778	73603b79-147f-428f-845e-dfabe07404e7	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\nItems: NovaPhone Pro 5G (Midnight Black, 256 GB) (Qty 1).\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).\n\nOrder ORD-002 status: **DELIVERED** (Total: ₹12,498.00).\nItems: ErgoSilent Wireless Keyboard & Mouse Combo (Qty 1), SoundWave ANC 750 Over-Ear Wireless Headphones (Qty 1).\nShipment SHIP-002 for order ORD-002 is **DELIVERED** via BlueDart (Tracking: TRK-BLUEDART-488302652, Estimated Delivery: 2026-08-07).\n\nOrder ORD-025 status: **CONFIRMED** (Total: ₹2,899.00).\nItems: Smart Touch Instant Induction Cooktop 2100W (Qty 1).\nShipment SHIP-025 for order ORD-025 is **PROCESSING** via XpressBees (Tracking: TRK-XPRESSBEES-819595113, Estimated Delivery: 2026-08-23).	\N	2026-09-15 16:17:02.432017	\N	\N
af5900ef-d552-4c3c-8323-1fc7ce63792c	4c570e55-16f1-4885-94a3-3a406ea7beb1	\N	ai	Hello Aarav Sharma! How can I assist you with your support request today?	\N	2026-09-15 16:33:56.08771	\N	\N
eb81ebcd-373e-4ba0-84bf-9f05606577a5	4c570e55-16f1-4885-94a3-3a406ea7beb1	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i want to inquiry about my order	\N	2026-09-15 16:34:34.871232	\N	\N
78e962f7-7f65-4243-be30-ea85107934d9	4c570e55-16f1-4885-94a3-3a406ea7beb1	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\n\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).	\N	2026-09-15 16:34:34.914946	\N	\N
d8c4d76c-dfaa-44a3-bdda-6743148d0318	4c570e55-16f1-4885-94a3-3a406ea7beb1	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all products info.	\N	2026-09-16 15:19:41.482822	\N	\N
bfb652b0-5248-4ebe-b197-ddf09a7590e1	4c570e55-16f1-4885-94a3-3a406ea7beb1	\N	ai	Here is an overview of popular products currently available in our ShopKart catalog:\n\n### 📱 Mobiles & Tablets\n• **NovaPhone Pro 5G (Midnight Black, 256 GB)** (`PROD-001`) — **₹46,999.00** (14.5% off) | Status: *IN_STOCK* (45 in stock)\n• **AeroTab Air 11-inch Wi-Fi Tablet (Space Grey, 128 GB)** (`PROD-002`) — **₹27,499.00** (16.7% off) | Status: *IN_STOCK* (4 in stock)\n• **Pixelite 4G Budget Smartphone (Ocean Blue, 64 GB)** (`PROD-003`) — **₹7,999.00** (20.0% off) | Status: *OUT_OF_STOCK* (0 in stock)\n• **ClassicTouch Keypad Phone V1** (`PROD-004`) — **₹1,499.00** (25.0% off) | Status: *OUT_OF_STOCK* (0 in stock)\n\n### 💻 Laptops & Computers\n• **ZenBook Ultra 14 Thin & Light Laptop (16GB/512GB SSD/Intel Core i7)** (`PROD-005`) — **₹78,990.00** (12.2% off) | Status: *IN_STOCK* (25 in stock)\n• **GamerX Legion RTX 4060 Gaming Laptop (16GB/1TB SSD)** (`PROD-006`) — **₹109,990.00** (12.0% off) | Status: *IN_STOCK* (12 in stock)\n• **ProView 27-inch 4K UHD IPS Monitor** (`PROD-007`) — **₹23,999.00** (20.0% off) | Status: *IN_STOCK* (30 in stock)\n• **ErgoSilent Wireless Keyboard & Mouse Combo** (`PROD-008`) — **₹2,499.00** (28.6% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🎧 Audio & Headphones\n• **SoundWave ANC 750 Over-Ear Wireless Headphones** (`PROD-009`) — **₹9,999.00** (33.3% off) | Status: *IN_STOCK* (40 in stock)\n• **AirBuds Pro True Wireless Earbuds with Dual Mic** (`PROD-010`) — **₹2,499.00** (50.0% off) | Status: *IN_STOCK* (80 in stock)\n• **BoomBox 20W Portable Bluetooth Speaker** (`PROD-011`) — **₹2,799.00** (30.0% off) | Status: *IN_STOCK* (50 in stock)\n• **StudioPro Vocal Condenser USB Microphone with Arm Stand** (`PROD-039`) — **₹4,499.00** (35.7% off) | Status: *IN_STOCK* (20 in stock)\n\n### 🍳 Kitchen & Dining\n• **ChefPro 1000W 4-Jar Mixer Grinder** (`PROD-012`) — **₹4,799.00** (31.4% off) | Status: *IN_STOCK* (35 in stock)\n• **CrispAir Digital 4.5L Air Fryer (Rapid Air Tech)** (`PROD-013`) — **₹5,999.00** (29.4% off) | Status: *IN_STOCK* (20 in stock)\n• **Hard Anodized 3-Piece Cookware Set (Kadai, Fry Pan, Tawa)** (`PROD-014`) — **₹2,899.00** (32.6% off) | Status: *IN_STOCK* (40 in stock)\n• **Stainless Steel Thermal Insulated Water Bottle 1000ml** (`PROD-038`) — **₹899.00** (40.0% off) | Status: *IN_STOCK* (60 in stock)\n\n### 🪑 Home Furniture\n• **ErgoRest High-Back Ergonomic Office Chair** (`PROD-015`) — **₹11,499.00** (32.4% off) | Status: *IN_STOCK* (18 in stock)\n• **Solid Sheesham Wood 4-Seater Dining Table Set** (`PROD-016`) — **₹26,999.00** (30.8% off) | Status: *IN_STOCK* (8 in stock)\n• **Modular Engineered Wood Study Desk (Columbian Walnut)** (`PROD-017`) — **₹5,499.00** (38.9% off) | Status: *IN_STOCK* (3 in stock)\n\n### 🏠 Home Appliances\n• **VisionPlus 55-inch 4K Ultra HD Smart Google TV** (`PROD-018`) — **₹38,990.00** (35.0% off) | Status: *IN_STOCK* (22 in stock)\n• **PureBreeze HEPA Air Purifier for Home (CADR 350 m3/h)** (`PROD-019`) — **₹10,999.00** (31.3% off) | Status: *IN_STOCK* (28 in stock)\n• **RoboClean 2-in-1 Robot Vacuum Cleaner & Mop** (`PROD-020`) — **₹19,999.00** (33.3% off) | Status: *IN_STOCK* (15 in stock)\n• **Smart Touch Instant Induction Cooktop 2100W** (`PROD-040`) — **₹2,899.00** (35.6% off) | Status: *IN_STOCK* (30 in stock)\n\n### 👔 Men's Clothing\n• **Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)** (`PROD-021`) — **₹1,299.00** (48.0% off) | Status: *IN_STOCK* (55 in stock)\n• **Slim Fit Stretchable Denim Jeans (Dark Indigo)** (`PROD-022`) — **₹1,899.00** (42.4% off) | Status: *IN_STOCK* (40 in stock)\n• **Heavyweight Cotton Graphic Crewneck T-Shirt (Olive)** (`PROD-023`) — **₹799.00** (46.7% off) | Status: *IN_STOCK* (70 in stock)\n• **Men's 3-Pack Modal Cotton Innerwear Boxer Briefs** (`PROD-024`) — **₹899.00** (30.8% off) | Status: *IN_STOCK* (45 in stock)\n\n### 👔 Women's Clothing\n• **Floral Embroidered Chanderi Silk Kurta Set with Dupatta** (`PROD-025`) — **₹3,499.00** (41.7% off) | Status: *IN_STOCK* (30 in stock)\n• **Tiered A-Line Floral Summer Midi Dress (Pastel Sage)** (`PROD-026`) — **₹1,699.00** (43.3% off) | Status: *IN_STOCK* (35 in stock)\n• **High-Waist Cotton Ankle Length Casual Trousers** (`PROD-027`) — **₹1,199.00** (45.5% off) | Status: *IN_STOCK* (25 in stock)\n\n### 👟 Footwear\n• **AirStride Pro Lightweight Road Running Shoes** (`PROD-028`) — **₹4,299.00** (33.9% off) | Status: *IN_STOCK* (50 in stock)\n• **Handcrafted Genuine Leather Formal Derby Shoes (Tan)** (`PROD-029`) — **₹3,699.00** (32.7% off) | Status: *IN_STOCK* (25 in stock)\n• **CloudSlide Ergonomic EVA Comfort Flip-Flop Slides** (`PROD-030`) — **₹699.00** (46.2% off) | Status: *IN_STOCK* (65 in stock)\n\n### ⚡ Electronics\n• **BeardMaster Pro Cordless Beard Trimmer (0.5 - 20 mm)** (`PROD-031`) — **₹1,699.00** (32.0% off) | Status: *IN_STOCK* (40 in stock)\n• **HydroSonic Sonic Electric Toothbrush with 4 Brush Heads** (`PROD-032`) — **₹2,299.00** (42.5% off) | Status: *IN_STOCK* (30 in stock)\n• **SilkTouch Salon Hair Dryer 2000W with Ionic Care** (`PROD-033`) — **₹2,199.00** (37.2% off) | Status: *IN_STOCK* (25 in stock)\n• **Vitamin C 10% Brightening Glow Face Serum (30 ml)** (`PROD-034`) — **₹549.00** (31.3% off) | Status: *IN_STOCK* (90 in stock)\n• **Ultra-Hydrating Ceramide Barrier Face Cream (50 g)** (`PROD-035`) — **₹499.00** (28.6% off) | Status: *IN_STOCK* (60 in stock)\n• **Anti-Dandruff Tea Tree & Salicylic Acid Shampoo (250 ml)** (`PROD-036`) — **₹419.00** (30.1% off) | Status: *IN_STOCK* (75 in stock)\n• **Daily Invisible Matte Sunscreen Gel SPF 50 PA++++ (50g)** (`PROD-037`) — **₹479.00** (26.2% off) | Status: *IN_STOCK* (100 in stock)\n\n💡 *Tip: Ask for full specs, pricing, or warranty details on any item by specifying its name or ID (e.g., `Tell me about PROD-001`).*	\N	2026-09-16 15:19:44.797894	\N	\N
51a30eb6-8564-441b-a655-c755c22b26fd	4c570e55-16f1-4885-94a3-3a406ea7beb1	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me info. of order-001	\N	2026-09-16 15:23:04.5244	\N	\N
2511b4d5-fc62-4f9c-a60d-3d497bf71927	4c570e55-16f1-4885-94a3-3a406ea7beb1	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\n\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).	\N	2026-09-16 15:23:04.622481	\N	\N
df417c74-d732-42ac-8da7-3e9a20b4bbc7	4c570e55-16f1-4885-94a3-3a406ea7beb1	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	give me all info of the product of order-001	\N	2026-09-16 15:23:31.862035	\N	\N
2bde8a95-c7b9-4167-8cb3-606db25eafb8	4c570e55-16f1-4885-94a3-3a406ea7beb1	\N	ai	Order ORD-001 status: **DELIVERED** (Total: ₹46,999.00).\nItems: NovaPhone Pro 5G (Midnight Black, 256 GB) (Qty 1).\nShipment SHIP-001 for order ORD-001 is **DELIVERED** via Delhivery (Tracking: TRK-DELHIVERY-764130526, Estimated Delivery: 2026-08-19).\n\nOrder ORD-002 status: **DELIVERED** (Total: ₹12,498.00).\nItems: ErgoSilent Wireless Keyboard & Mouse Combo (Qty 1), SoundWave ANC 750 Over-Ear Wireless Headphones (Qty 1).\nShipment SHIP-002 for order ORD-002 is **DELIVERED** via BlueDart (Tracking: TRK-BLUEDART-488302652, Estimated Delivery: 2026-08-07).\n\nOrder ORD-025 status: **CONFIRMED** (Total: ₹2,899.00).\nItems: Smart Touch Instant Induction Cooktop 2100W (Qty 1).\nShipment SHIP-025 for order ORD-025 is **PROCESSING** via XpressBees (Tracking: TRK-XPRESSBEES-819595113, Estimated Delivery: 2026-08-23).	\N	2026-09-16 15:23:31.970159	\N	\N
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.order_items (order_item_id, order_id, product_id, quantity, unit_price, total_price) FROM stdin;
ITEM-001	ORD-001	PROD-001	1	46999.00	46999.00
ITEM-002	ORD-002	PROD-008	1	2499.00	2499.00
ITEM-003	ORD-002	PROD-009	1	9999.00	9999.00
ITEM-005	ORD-004	PROD-005	1	78990.00	78990.00
ITEM-006	ORD-005	PROD-018	1	38990.00	38990.00
ITEM-007	ORD-006	PROD-010	1	2499.00	2499.00
ITEM-008	ORD-007	PROD-013	1	5999.00	5999.00
ITEM-009	ORD-008	PROD-003	1	7999.00	7999.00
ITEM-010	ORD-009	PROD-021	2	1299.00	2598.00
ITEM-011	ORD-010	PROD-028	1	4299.00	4299.00
ITEM-012	ORD-011	PROD-025	1	3499.00	3499.00
ITEM-013	ORD-012	PROD-015	1	11499.00	11499.00
ITEM-014	ORD-013	PROD-031	1	1699.00	1699.00
ITEM-015	ORD-014	PROD-024	1	899.00	899.00
ITEM-016	ORD-015	PROD-022	1	1899.00	1899.00
ITEM-017	ORD-016	PROD-029	1	3699.00	3699.00
ITEM-018	ORD-017	PROD-011	1	2799.00	2799.00
ITEM-019	ORD-018	PROD-006	1	109990.00	109990.00
ITEM-020	ORD-019	PROD-019	1	10999.00	10999.00
ITEM-021	ORD-020	PROD-034	2	549.00	1098.00
ITEM-022	ORD-021	PROD-026	1	1699.00	1699.00
ITEM-023	ORD-021	PROD-030	1	699.00	699.00
ITEM-024	ORD-022	PROD-038	2	899.00	1798.00
ITEM-025	ORD-023	PROD-033	1	2199.00	2199.00
ITEM-026	ORD-024	PROD-039	1	4499.00	4499.00
ITEM-027	ORD-025	PROD-040	1	2899.00	2899.00
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.orders (order_id, company_id, customer_id, status, order_date, total_amount, shipping_address, cancellation_reason, created_at, updated_at) FROM stdin;
ORD-015	COMP-001	b395b112-7158-4b1e-95f1-d240ad28315b	DELIVERED	2026-08-14 08:00:00	1899.00	14, 2nd Cross, 7th Main, Indiranagar, Bengaluru, Karnataka - 560038	\N	2026-08-14 08:00:00	2026-08-21 11:13:12
ORD-016	COMP-001	218f5584-0624-4692-bbdf-c52e3d9b0568	DELIVERED	2026-08-07 08:00:00	3699.00	501, Heritage Horizon, CG Road, Navrangpura, Ahmedabad, Gujarat - 380009	\N	2026-08-07 08:00:00	2026-08-21 11:13:12
ORD-001	COMP-001	4a47565a-2ec1-404a-8f05-07490e1d9384	DELIVERED	2026-08-16 10:00:00	46999.00	Flat 402, Green Glen Layout, Outer Ring Road, Bellandur, Bengaluru, Karnataka - 560103	\N	2026-08-16 10:00:00	2026-08-21 11:13:12
ORD-002	COMP-001	4a47565a-2ec1-404a-8f05-07490e1d9384	DELIVERED	2026-08-04 11:00:00	12498.00	Flat 402, Green Glen Layout, Outer Ring Road, Bellandur, Bengaluru, Karnataka - 560103	\N	2026-08-04 11:00:00	2026-08-21 11:13:12
ORD-004	COMP-001	70bf9179-aa0b-4134-bb43-6572d7eb240a	OUT_FOR_DELIVERY	2026-08-17 08:00:00	78990.00	House No. 42, Block C, Defence Colony, New Delhi, Delhi - 110024	\N	2026-08-17 08:00:00	2026-08-21 11:13:12
ORD-005	COMP-001	f202a0ff-09fd-4bbe-bb82-63dfa022c864	DELAYED	2026-08-14 08:00:00	38990.00	Plot 18, Road No. 12, Banjara Hills, Hyderabad, Telangana - 500034	\N	2026-08-14 08:00:00	2026-08-21 11:13:12
ORD-006	COMP-001	233549a6-737c-4534-8b5c-cea20b12ffad	DELAYED	2026-08-11 09:00:00	2499.00	New No. 15, 4th Main Road, RA Puram, Chennai, Tamil Nadu - 600028	\N	2026-08-11 09:00:00	2026-08-21 11:13:12
ORD-007	COMP-001	de90577d-bf90-4ad1-acd5-af943539b65b	CONFIRMED	2026-08-19 10:00:00	5999.00	Row House 7, Nyati Estate, Mohammadwadi, Pune, Maharashtra - 411060	\N	2026-08-19 10:00:00	2026-08-21 11:13:12
ORD-008	COMP-001	da9ae675-d683-4d64-bbb5-298eaa791672	CANCELLED	2026-08-13 03:00:00	7999.00	Flat 2A, South City Residency, Prince Anwar Shah Road, Kolkata, West Bengal - 700068	Item became out of stock during warehouse fulfillment	2026-08-13 03:00:00	2026-08-21 11:13:12
ORD-009	COMP-001	2adbb717-51da-424e-bdc5-0cc7840a476a	DELIVERED	2026-08-18 10:00:00	2598.00	102, Shanti Heights, Law College Road, Erandwane, Pune, Maharashtra - 411004	\N	2026-08-18 10:00:00	2026-08-21 11:13:12
ORD-010	COMP-001	1f3cac08-90fd-4f14-bbd0-50b8c32d3662	SHIPPED	2026-08-15 02:00:00	4299.00	Villa 12, Skyline Meadows, Kakkanad, Kochi, Kerala - 682030	\N	2026-08-15 02:00:00	2026-08-21 11:13:12
ORD-011	COMP-001	2d2e9163-288b-4994-bfc4-368bb117de95	PLACED	2026-08-19 05:00:00	3499.00	Tower 4, Flat 1102, Nirvana Country, Sector 50, Gurugram, Haryana - 122018	\N	2026-08-19 05:00:00	2026-08-21 11:13:12
ORD-012	COMP-001	639c918b-c490-4a64-8598-7943a3016f0e	FAILED	2026-08-17 11:00:00	11499.00	House 28, Zoo Road Tiniali, RG Baruah Road, Guwahati, Assam - 781024	Order creation failed due to gateway timeout during checkout	2026-08-17 11:00:00	2026-08-21 11:13:12
ORD-013	COMP-001	1666975c-32b8-4a3f-994b-0cadb8c754a5	IN_TRANSIT	2026-08-16 11:00:00	1699.00	45, Malviya Nagar, Near Calgiri Hospital, Jaipur, Rajasthan - 302017	\N	2026-08-16 11:00:00	2026-08-21 11:13:12
ORD-014	COMP-001	a2950fb1-86d1-42e0-acff-82037eb02962	DELIVERED	2026-08-09 10:00:00	899.00	3/120, Vivek Khand, Gomti Nagar, Lucknow, Uttar Pradesh - 226010	\N	2026-08-09 10:00:00	2026-08-21 11:13:12
ORD-017	COMP-001	6f52bb95-3341-4a7b-a33c-9a5e67f9dd6f	DELIVERED	2026-08-01 03:00:00	2799.00	TC 15/1982, Cotton Hill, Vazhuthacaud, Thiruvananthapuram, Kerala - 695014	\N	2026-08-01 03:00:00	2026-08-21 11:13:12
ORD-018	COMP-001	5b6089d7-d2e6-4ba9-b8fd-598db511b129	DELIVERED	2026-08-05 02:00:00	109990.00	A-12, Sector 15A, Noida, Noida, Uttar Pradesh - 201301	\N	2026-08-05 02:00:00	2026-08-21 11:13:12
ORD-019	COMP-001	0f97f36b-0935-49a2-8de9-84bb3344ba5d	PACKED	2026-08-18 11:00:00	10999.00	8B, Alipore Park Road, Alipore, Kolkata, West Bengal - 700027	\N	2026-08-18 11:00:00	2026-08-21 11:13:12
ORD-020	COMP-001	2715e45f-a024-4eb6-9e71-7a3b5be57bf7	DELIVERED	2026-08-12 03:00:00	1098.00	12, Manoramaganj, Near Geeta Bhawan, Indore, Madhya Pradesh - 452001	\N	2026-08-12 03:00:00	2026-08-21 11:13:12
ORD-021	COMP-001	b95c612a-3514-4d63-8b62-1b9f2bd3c24f	DELIVERED	2026-08-10 08:00:00	2398.00	House 512, Sector 8B, Chandigarh, Chandigarh - 160009	\N	2026-08-10 08:00:00	2026-08-21 11:13:12
ORD-022	COMP-001	918d530e-ba04-41a7-a0a9-8dbc477f51e9	IN_TRANSIT	2026-08-17 03:00:00	1798.00	33, 11th Main Road, Malleshwaram, Bengaluru, Karnataka - 560003	\N	2026-08-17 03:00:00	2026-08-21 11:13:12
ORD-023	COMP-001	a6191a36-88ed-4559-ae61-a985777583e4	DELIVERED	2026-08-08 05:00:00	2199.00	B-12, Sector C, Mahanagar, Lucknow, Uttar Pradesh - 226006	\N	2026-08-08 05:00:00	2026-08-21 11:13:12
ORD-024	COMP-001	a8328835-e5dd-4e0d-bbef-9e11ec27aa69	DELIVERED	2026-08-11 08:00:00	4499.00	C-14, Vaishali Nagar, Jaipur, Rajasthan - 302021	\N	2026-08-11 08:00:00	2026-08-21 11:13:12
ORD-025	COMP-001	4a47565a-2ec1-404a-8f05-07490e1d9384	CONFIRMED	2026-08-18 04:00:00	2899.00	Flat 402, Green Glen Layout, Outer Ring Road, Bellandur, Bengaluru, Karnataka - 560103	\N	2026-08-18 04:00:00	2026-08-21 11:13:12
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.payments (payment_id, order_id, customer_id, amount, method, status, transaction_reference, payment_date, failure_reason) FROM stdin;
PAY-010	ORD-009	2adbb717-51da-424e-bdc5-0cc7840a476a	2598.00	DEBIT_CARD	SUCCESS	TXN-DEB-55176955	2026-08-18 10:00:00	\N
PAY-011	ORD-010	1f3cac08-90fd-4f14-bbd0-50b8c32d3662	4299.00	UPI	SUCCESS	TXN-UPI-DUP1-23718431	2026-08-15 02:00:00	\N
PAY-012	ORD-010	1f3cac08-90fd-4f14-bbd0-50b8c32d3662	4299.00	UPI	SUCCESS	TXN-UPI-DUP2-22448136	2026-08-15 02:01:00	\N
PAY-001	ORD-001	4a47565a-2ec1-404a-8f05-07490e1d9384	46999.00	CREDIT_CARD	FAILED	TXN-CC-FAIL-89089901	2026-08-16 10:00:00	Bank server timeout during OTP authentication
PAY-002	ORD-001	4a47565a-2ec1-404a-8f05-07490e1d9384	46999.00	UPI	SUCCESS	TXN-UPI-47338124	2026-08-16 10:04:00	\N
PAY-003	ORD-002	4a47565a-2ec1-404a-8f05-07490e1d9384	12498.00	CREDIT_CARD	SUCCESS	TXN-CRE-10872248	2026-08-04 11:00:00	\N
PAY-005	ORD-004	70bf9179-aa0b-4134-bb43-6572d7eb240a	78990.00	NET_BANKING	SUCCESS	TXN-NET-66722344	2026-08-17 08:00:00	\N
PAY-006	ORD-005	f202a0ff-09fd-4bbe-bb82-63dfa022c864	38990.00	WALLET	SUCCESS	TXN-WAL-55667651	2026-08-14 08:00:00	\N
PAY-007	ORD-006	233549a6-737c-4534-8b5c-cea20b12ffad	2499.00	COD	SUCCESS	TXN-COD-47295260	2026-08-11 09:00:00	\N
PAY-008	ORD-007	de90577d-bf90-4ad1-acd5-af943539b65b	5999.00	UPI	SUCCESS	TXN-UPI-30868105	2026-08-19 10:00:00	\N
PAY-009	ORD-008	da9ae675-d683-4d64-bbb5-298eaa791672	7999.00	UPI	REFUNDED	TXN-UPI-CAN-38898923	2026-08-13 03:00:00	\N
PAY-013	ORD-011	2d2e9163-288b-4994-bfc4-368bb117de95	3499.00	NET_BANKING	PENDING	TXN-NETBANK-PEND-60992979	2026-08-19 05:00:00	Awaiting confirmation webhook from issuing bank
PAY-014	ORD-012	639c918b-c490-4a64-8598-7943a3016f0e	11499.00	CREDIT_CARD	SUCCESS	TXN-CC-ORDFALL-22981052	2026-08-17 11:00:00	\N
PAY-015	ORD-013	1666975c-32b8-4a3f-994b-0cadb8c754a5	1699.00	UPI	SUCCESS	TXN-UPI-58181396	2026-08-16 11:00:00	\N
PAY-016	ORD-014	a2950fb1-86d1-42e0-acff-82037eb02962	899.00	CREDIT_CARD	SUCCESS	TXN-CRE-56164955	2026-08-09 10:00:00	\N
PAY-017	ORD-015	b395b112-7158-4b1e-95f1-d240ad28315b	1899.00	DEBIT_CARD	SUCCESS	TXN-DEB-91030736	2026-08-14 08:00:00	\N
PAY-018	ORD-016	218f5584-0624-4692-bbdf-c52e3d9b0568	3699.00	NET_BANKING	SUCCESS	TXN-NET-45503389	2026-08-07 08:00:00	\N
PAY-019	ORD-017	6f52bb95-3341-4a7b-a33c-9a5e67f9dd6f	2799.00	WALLET	SUCCESS	TXN-WAL-15831819	2026-08-01 03:00:00	\N
PAY-020	ORD-018	5b6089d7-d2e6-4ba9-b8fd-598db511b129	109990.00	COD	SUCCESS	TXN-COD-71662963	2026-08-05 02:00:00	\N
PAY-021	ORD-019	0f97f36b-0935-49a2-8de9-84bb3344ba5d	10999.00	UPI	SUCCESS	TXN-UPI-81971316	2026-08-18 11:00:00	\N
PAY-022	ORD-020	2715e45f-a024-4eb6-9e71-7a3b5be57bf7	1098.00	CREDIT_CARD	SUCCESS	TXN-CRE-26753883	2026-08-12 03:00:00	\N
PAY-023	ORD-021	b95c612a-3514-4d63-8b62-1b9f2bd3c24f	2398.00	DEBIT_CARD	SUCCESS	TXN-DEB-60806024	2026-08-10 08:00:00	\N
PAY-024	ORD-022	918d530e-ba04-41a7-a0a9-8dbc477f51e9	1798.00	NET_BANKING	SUCCESS	TXN-NET-20576383	2026-08-17 03:00:00	\N
PAY-025	ORD-023	a6191a36-88ed-4559-ae61-a985777583e4	2199.00	WALLET	SUCCESS	TXN-WAL-84093639	2026-08-08 05:00:00	\N
PAY-026	ORD-024	a8328835-e5dd-4e0d-bbef-9e11ec27aa69	4499.00	COD	SUCCESS	TXN-COD-49349722	2026-08-11 08:00:00	\N
PAY-027	ORD-025	4a47565a-2ec1-404a-8f05-07490e1d9384	2899.00	UPI	SUCCESS	TXN-UPI-94374605	2026-08-18 04:00:00	\N
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.products (product_id, company_id, seller_id, category_id, name, brand, description, price, mrp, stock_quantity, specifications, created_at) FROM stdin;
PROD-001	COMP-001	SELL-001	CAT-002	NovaPhone Pro 5G (Midnight Black, 256 GB)	NovaPhone	Flagship 5G smartphone with 120Hz AMOLED display, 50MP triple camera, and 5000mAh battery.	46999.00	54999.00	45	{"RAM": "8 GB", "Color": "Midnight Black", "Battery": "5000 mAh", "Processor": "Snapdragon 8 Gen 2", "5G Support": "Yes", "Screen Size": "6.7 inches", "Internal Storage": "256 GB"}	\N
PROD-002	COMP-001	SELL-002	CAT-002	AeroTab Air 11-inch Wi-Fi Tablet (Space Grey, 128 GB)	AeroTab	Ultra-slim 11-inch tablet with 2K resolution, stylus support, and quad stereo speakers.	27499.00	32999.00	4	{"Weight": "480 g", "Display": "11 inch 2K IPS", "Storage": "128 GB", "Battery Life": "Up to 12 hours", "Stylus Compatible": "Yes"}	\N
PROD-003	COMP-001	SELL-003	CAT-002	Pixelite 4G Budget Smartphone (Ocean Blue, 64 GB)	Pixelite	Reliable everyday smartphone with large HD+ display and 5000mAh battery.	7999.00	9999.00	0	{"RAM": "4 GB", "Color": "Ocean Blue", "Display": "6.5 inch HD+", "Internal Storage": "64 GB"}	\N
PROD-004	COMP-001	SELL-004	CAT-002	ClassicTouch Keypad Phone V1	ClassicTouch	Rugged feature phone with FM radio, LED torch, and 7-day standby battery.	1499.00	1999.00	0	{"Torch": "Yes", "Battery": "1800 mAh", "Dual SIM": "Yes", "Form Factor": "Keypad"}	\N
PROD-005	COMP-001	SELL-005	CAT-003	ZenBook Ultra 14 Thin & Light Laptop (16GB/512GB SSD/Intel Core i7)	ZenTech	Sleek metallic chassis laptop with OLED display and all-day battery life.	78990.00	89990.00	25	{"OS": "Windows 11 Home", "RAM": "16 GB LPDDR5", "Screen": "14 inch 2.8K OLED", "Weight": "1.28 kg", "Storage": "512 GB NVMe SSD", "Processor": "Intel Core i7 13th Gen"}	\N
PROD-006	COMP-001	SELL-006	CAT-003	GamerX Legion RTX 4060 Gaming Laptop (16GB/1TB SSD)	GamerX	High-performance gaming machine with 165Hz QHD display and RGB backlit keyboard.	109990.00	124990.00	12	{"GPU": "NVIDIA GeForce RTX 4060 8GB", "RAM": "16 GB DDR5", "Display": "15.6 inch 165Hz", "Storage": "1 TB SSD", "Processor": "AMD Ryzen 7 7840HS"}	\N
PROD-007	COMP-001	SELL-007	CAT-003	ProView 27-inch 4K UHD IPS Monitor	ProView	Color-accurate 4K monitor with 99% sRGB, HDR400, and USB-C 65W charging port.	23999.00	29999.00	30	{"Ports": "HDMI 2.0, DP 1.4, USB Type-C", "Panel Type": "IPS", "Resolution": "3840 x 2160 Pixels (4K)", "Refresh Rate": "60 Hz"}	\N
PROD-008	COMP-001	SELL-008	CAT-003	ErgoSilent Wireless Keyboard & Mouse Combo	LogiTechie	Comfortable silent-click keyboard and ergonomic precision optical mouse.	2499.00	3499.00	60	{"Battery": "AA / AAA Batteries included", "Connectivity": "2.4GHz USB Dongle & Bluetooth", "Compatibility": "Windows, macOS, Linux"}	\N
PROD-009	COMP-001	SELL-009	CAT-004	SoundWave ANC 750 Over-Ear Wireless Headphones	SoundWave	Premium active noise cancelling headphones with 40-hour playtime and spatial audio.	9999.00	14999.00	40	{"Type": "Over-Ear", "Color": "Matte Black", "Charging": "Fast USB-C", "Battery Life": "40 Hours", "Noise Cancellation": "Hybrid Active Noise Cancellation (ANC)"}	\N
PROD-010	COMP-001	SELL-010	CAT-004	AirBuds Pro True Wireless Earbuds with Dual Mic	AirPulse	Compact TWS earbuds with deep bass boost, IPX5 water resistance, and environmental noise cancellation.	2499.00	4999.00	80	{"Driver Size": "13 mm", "Total Playback": "32 Hours with Case", "Water Resistance": "IPX5", "Bluetooth Version": "5.3"}	\N
PROD-011	COMP-001	SELL-001	CAT-004	BoomBox 20W Portable Bluetooth Speaker	SonicBlast	Rugged outdoor waterproof bluetooth speaker with punchy bass and party lights.	2799.00	3999.00	50	{"Output": "20 Watts RMS", "Battery": "12 Hours playback", "Waterproof": "IP67"}	\N
PROD-012	COMP-001	SELL-002	CAT-006	ChefPro 1000W 4-Jar Mixer Grinder	ChefPro	Heavy-duty commercial motor mixer grinder with stainless steel jars and pulse control.	4799.00	6999.00	35	{"Wattage": "1000 W", "Blade Material": "304 Stainless Steel", "Number of Jars": "4 Jars (Wet, Dry, Chutney, Juicer)", "Speed Settings": "3 Speed with Incher"}	\N
PROD-013	COMP-001	SELL-003	CAT-006	CrispAir Digital 4.5L Air Fryer (Rapid Air Tech)	CrispAir	Oil-free cooking with 8 one-touch cooking presets and digital touch LED screen.	5999.00	8499.00	20	{"Power": "1400 W", "Capacity": "4.5 Litres", "Non-Stick Basket": "Yes, Dishwasher safe", "Temperature Range": "80°C - 200°C"}	\N
PROD-014	COMP-001	SELL-004	CAT-006	Hard Anodized 3-Piece Cookware Set (Kadai, Fry Pan, Tawa)	KitchenCraft	Durable non-toxic hard anodized induction base cookware set with stay-cool handles.	2899.00	4299.00	40	{"Pieces": "3", "Material": "Hard Anodized Aluminum", "Lid Included": "Tempered Glass Lid", "Induction Compatible": "Yes"}	\N
PROD-015	COMP-001	SELL-005	CAT-007	ErgoRest High-Back Ergonomic Office Chair	ErgoRest	Breathable mesh chair with adjustable lumbar support, 3D armrests, and synchro-tilt mechanism.	11499.00	16999.00	18	{"Recline": "Up to 135 degrees", "Assembly": "DIY with tool kit", "Material": "Breathable Nylon Mesh & Alloy Base", "Max Weight Capacity": "140 kg"}	\N
PROD-016	COMP-001	SELL-006	CAT-007	Solid Sheesham Wood 4-Seater Dining Table Set	RoyalTimber	Handcrafted Indian Sheesham wood dining set with rich walnut finish and 4 cushioned chairs.	26999.00	38999.00	8	{"Finish": "Walnut Finish", "Wood Type": "Solid Sheesham (Rosewood)", "Seating Capacity": "4 Persons", "Table Dimensions": "115 x 75 x 76 cm"}	\N
PROD-017	COMP-001	SELL-007	CAT-007	Modular Engineered Wood Study Desk (Columbian Walnut)	UrbanSpace	Minimalist study table with integrated cable management and 2 storage drawers.	5499.00	8999.00	3	{"Drawers": "2 Smooth Slide Drawers", "Material": "Engineered Particle Wood", "Dimensions": "100 x 60 x 75 cm"}	\N
PROD-018	COMP-001	SELL-008	CAT-008	VisionPlus 55-inch 4K Ultra HD Smart Google TV	VisionPlus	Frameless 4K HDR10+ Smart TV with Dolby Atmos sound and built-in Chromecast.	38990.00	59990.00	22	{"USB Ports": "2", "HDMI Ports": "3", "Resolution": "4K Ultra HD (3840x2160)", "Sound Output": "30 Watts Dolby Audio", "Operating System": "Google TV"}	\N
PROD-019	COMP-001	SELL-009	CAT-008	PureBreeze HEPA Air Purifier for Home (CADR 350 m3/h)	PureBreeze	True HEPA H13 air purifier with real-time AQI digital display and smart Wi-Fi app control.	10999.00	15999.00	28	{"Filter Type": "H13 True HEPA + Activated Carbon", "Noise Level": "24 dB (Sleep Mode)", "Coverage Area": "Up to 450 sq. ft."}	\N
PROD-020	COMP-001	SELL-010	CAT-008	RoboClean 2-in-1 Robot Vacuum Cleaner & Mop	RoboClean	LiDAR navigation robotic cleaner with 4000Pa suction power and multi-floor mapping.	19999.00	29999.00	15	{"Navigation": "LiDAR LDS 360", "Suction Power": "4000 Pa", "Battery Capacity": "5200 mAh", "Dustbin Capacity": "450 ml"}	\N
PROD-021	COMP-001	SELL-001	CAT-010	Classic Fit 100% Pure Cotton Oxford Shirt (Navy Blue)	UrbanTrend	Breathable premium combed cotton casual button-down shirt with curved hemline.	1299.00	2499.00	55	{"Fit": "Regular Fit", "Care": "Machine Wash Warm", "Collar": "Button Down", "Fabric": "100% Combed Cotton", "Sleeve": "Full Sleeve"}	\N
PROD-022	COMP-001	SELL-002	CAT-010	Slim Fit Stretchable Denim Jeans (Dark Indigo)	DenimCo	Comfortable 5-pocket stretch denim with antique brass rivets and zip fly.	1899.00	3299.00	40	{"Fit": "Slim Fit", "Rise": "Mid Rise", "Fabric": "98% Cotton, 2% Elastane", "Length": "Regular 32 inches"}	\N
PROD-023	COMP-001	SELL-003	CAT-010	Heavyweight Cotton Graphic Crewneck T-Shirt (Olive)	UrbanTrend	240 GSM bio-washed oversized streetwear t-shirt with screen-printed graphic.	799.00	1499.00	70	{"Fit": "Oversized Fit", "GSM": "240 GSM", "Fabric": "100% Bio-Washed Cotton"}	\N
PROD-024	COMP-001	SELL-004	CAT-010	Men's 3-Pack Modal Cotton Innerwear Boxer Briefs	ComfyWear	Ultra-soft antimicrobial modal fabric boxer briefs with anti-chafing waistband.	899.00	1299.00	45	{"Material": "92% MicroModal, 8% Spandex", "Pack Size": "3", "Hygiene Policy": "Non-Returnable for hygiene reasons"}	\N
PROD-025	COMP-001	SELL-005	CAT-011	Floral Embroidered Chanderi Silk Kurta Set with Dupatta	Riwayat Ethnic	Elegant festive 3-piece kurta set featuring intricate zari embroidery and scalloped organza dupatta.	3499.00	5999.00	30	{"Work": "Zari & Thread Hand Embroidery", "Fabric": "Chanderi Silk Blend", "Includes": "Kurta, Trousers, Organza Dupatta", "Dry Clean": "Dry Clean Recommended"}	\N
PROD-026	COMP-001	SELL-006	CAT-011	Tiered A-Line Floral Summer Midi Dress (Pastel Sage)	FloraBella	Breezy lightweight rayon midi dress with puff sleeves and sweetheart neckline.	1699.00	2999.00	35	{"Fabric": "100% Viscose Rayon", "Length": "Midi", "Pattern": "Botanical Floral Print", "Sleeve Length": "Short Puff Sleeve"}	\N
PROD-027	COMP-001	SELL-007	CAT-011	High-Waist Cotton Ankle Length Casual Trousers	FloraBella	Smart tailored trousers with elasticated back waist and deep side pockets.	1199.00	2199.00	25	{"Waist": "High Rise Elasticated", "Fabric": "Cotton Twill with Spandex", "Closure": "Button & Zip Fly"}	\N
PROD-028	COMP-001	SELL-008	CAT-012	AirStride Pro Lightweight Road Running Shoes	AirStride	Engineered mesh running shoes with responsive nitrogen-infused foam midsole and rubber outsole.	4299.00	6499.00	50	{"Sole": "High-Abrasion Rubber", "Weight": "245 g (UK 8)", "Cushioning": "Nitrogen-Infused EVA Foam", "Upper Material": "Breathable Engineered Jacquard Mesh"}	\N
PROD-029	COMP-001	SELL-009	CAT-012	Handcrafted Genuine Leather Formal Derby Shoes (Tan)	OxfordHeritage	Classic full-grain Argentine leather formal lace-ups with cushioned memory foam footbed.	3699.00	5499.00	25	{"Sole": "TPR Durable Sole", "Color": "Rich Tan", "Insole": "Orthopedic Memory Foam", "Material": "100% Genuine Full Grain Leather"}	\N
PROD-030	COMP-001	SELL-010	CAT-012	CloudSlide Ergonomic EVA Comfort Flip-Flop Slides	AirStride	Waterproof quick-drying rebound foam slides for everyday home and casual outdoor wear.	699.00	1299.00	65	{"Material": "Ultra-light EVA", "Waterproof": "100% Waterproof", "Arch Support": "Anatomical Arch Support"}	\N
PROD-031	COMP-001	SELL-001	CAT-001	BeardMaster Pro Cordless Beard Trimmer (0.5 - 20 mm)	GroomCraft	Titanium coated self-sharpening blades with 40 length settings and 90-minute runtime.	1699.00	2499.00	40	{"Run Time": "90 Minutes on 1 Hour Charge", "Blade Material": "Titanium Coated Stainless Steel", "Water Resistance": "IPX7 Washable Head", "Precision Settings": "40 Lock-in Lengths (0.5mm to 20mm)"}	\N
PROD-032	COMP-001	SELL-002	CAT-001	HydroSonic Sonic Electric Toothbrush with 4 Brush Heads	HydroSonic	40000 VPM ultrasonic smart toothbrush with 5 brushing modes and 2-minute smart timer.	2299.00	3999.00	30	{"Vibrations": "40,000 Strokes / Min", "Waterproof": "IPX8", "Battery Life": "30 Days on Full Charge", "Heads Included": "4 DuPont Bristle Heads"}	\N
PROD-033	COMP-001	SELL-003	CAT-001	SilkTouch Salon Hair Dryer 2000W with Ionic Care	GroomCraft	Professional 2000W AC motor blow dryer with ionic conditioning nozzle and cool shot button.	2199.00	3499.00	25	{"Power": "2000 Watts AC Motor", "Attachments": "Diffuser & Concentrator Nozzle", "Heat Settings": "3 Heat / 2 Speed Modes"}	\N
PROD-034	COMP-001	SELL-004	CAT-001	Vitamin C 10% Brightening Glow Face Serum (30 ml)	GlowBotanica	Potent antioxidant serum with Vitamin C, Ferulic Acid, and Hyaluronic Acid for radiant skin.	549.00	799.00	90	{"Volume": "30 ml", "Skin Type": "All Skin Types", "Cruelty Free": "Yes, 100% Vegan", "Active Ingredients": "10% Ethyl Ascorbic Acid, 0.5% Ferulic Acid"}	\N
PROD-035	COMP-001	SELL-005	CAT-001	Ultra-Hydrating Ceramide Barrier Face Cream (50 g)	GlowBotanica	Deep moisturizing restorative cream with 5 essential ceramides and Centella Asiatica.	499.00	699.00	60	{"Net Quantity": "50 grams", "Fragrance Free": "Yes", "Dermatologically Tested": "Yes"}	\N
PROD-036	COMP-001	SELL-006	CAT-001	Anti-Dandruff Tea Tree & Salicylic Acid Shampoo (250 ml)	RootCare	Sulphate-free scalp clarifying shampoo to reduce flakes and soothe itchy scalp.	419.00	599.00	75	{"Volume": "250 ml", "Key Actives": "Australian Tea Tree Oil, 1% Salicylic Acid", "Sulphate & Paraben Free": "Yes"}	\N
PROD-037	COMP-001	SELL-007	CAT-001	Daily Invisible Matte Sunscreen Gel SPF 50 PA++++ (50g)	GlowBotanica	Broad spectrum hybrid sunscreen leaving zero white cast with non-greasy velvet finish.	479.00	649.00	100	{"SPF": "SPF 50 PA++++", "Net Weight": "50 g", "White Cast": "Zero White Cast", "Water Resistant": "Up to 80 mins"}	\N
PROD-038	COMP-001	SELL-008	CAT-006	Stainless Steel Thermal Insulated Water Bottle 1000ml	HydroFlasker	Double-wall vacuum insulated stainless steel flask keeping beverages cold for 24h or hot for 12h.	899.00	1499.00	60	{"BPA Free": "Yes", "Capacity": "1000 ml (1 Litre)", "Material": "18/8 Food Grade Stainless Steel"}	\N
PROD-039	COMP-001	SELL-009	CAT-004	StudioPro Vocal Condenser USB Microphone with Arm Stand	SoundWave	Cardioid studio-quality USB microphone for podcasting, streaming, and voiceover recording.	4499.00	6999.00	20	{"Connection": "USB Type-C to Type-A Plug & Play", "Polar Pattern": "Cardioid", "Sampling Rate": "192kHz / 24-bit"}	\N
PROD-040	COMP-001	SELL-010	CAT-008	Smart Touch Instant Induction Cooktop 2100W	ChefPro	Energy efficient induction cooktop with feather touch buttons and preset Indian cooking menus.	2899.00	4499.00	30	{"Power": "2100 W", "Timer": "Up to 3 Hours", "Surface": "Micro Crystal Glass Plate"}	\N
\.


--
-- Data for Name: quick_replies; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.quick_replies (id, tenant_id, category, keyword_pattern, response_text, priority, is_active, created_at, updated_at) FROM stdin;
7041813b-63e1-49e5-8e93-7f616723df7d	shopkart	Billing	refund, money back, credit	Your refund has been processed and should appear in 5-7 business days.	1	t	2026-09-09 16:49:19.23583	2026-09-09 16:49:19.236
e3c9dba9-9c8c-46a4-aa93-8e55a7b02bef	shopkart	Orders	track, order status, where is my order	I checked your order status — it is currently in transit. You can track your shipment live under the Orders tab in your dashboard.	2	t	2026-09-09 16:49:19.236282	2026-09-09 16:49:19.236401
07a1ce70-4928-458b-90cc-bce93b063aca	shopkart	Returns	return, replace, exchange	To initiate a return, visit your Orders page, select your order, and click Request Return. Items can be returned within 30 days of delivery.	3	t	2026-09-09 16:49:19.236624	2026-09-09 16:49:19.23674
2702b52d-c9ef-4474-8196-27dfb792c941	shopkart	Shipping	delivery, shipping, courier	Standard delivery takes 3–5 business days for metro areas and 5–7 business days for non-metro locations.	4	t	2026-09-09 16:49:19.236924	2026-09-09 16:49:19.236999
ed813dfd-82bc-4b6e-848c-0c49a1a65a3e	shopkart	Billing	refund policy, cancel refund	Refunds are initiated within 2 to 4 hours of courier pickup for damaged items, and credited to your original payment method.	5	t	2026-09-09 16:49:19.237153	2026-09-09 16:49:19.237228
\.


--
-- Data for Name: refunds; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.refunds (refund_id, return_id, order_id, customer_id, refund_amount, status, initiated_at, expected_date, completed_at) FROM stdin;
REF-002	RET-004	ORD-016	218f5584-0624-4692-bbdf-c52e3d9b0568	3699.00	PROCESSING	2026-08-12 08:00:00	2026-08-17	\N
REF-003	RET-005	ORD-017	6f52bb95-3341-4a7b-a33c-9a5e67f9dd6f	2799.00	FAILED	2026-08-07 03:00:00	2026-08-10	\N
REF-004	RET-006	ORD-018	5b6089d7-d2e6-4ba9-b8fd-598db511b129	89990.00	COMPLETED	2026-08-09 02:00:00	2026-08-12	2026-08-11 02:00:00
\.


--
-- Data for Name: returns; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.returns (return_id, order_id, order_item_id, customer_id, reason, status, requested_at, pickup_date, completed_at) FROM stdin;
RET-002	ORD-014	ITEM-015	a2950fb1-86d1-42e0-acff-82037eb02962	SIZE_ISSUE	REJECTED	2026-08-10 10:00:00	\N	\N
RET-003	ORD-015	ITEM-016	b395b112-7158-4b1e-95f1-d240ad28315b	SIZE_ISSUE	PICKUP_SCHEDULED	2026-08-16 08:00:00	2026-08-17	\N
RET-004	ORD-016	ITEM-017	218f5584-0624-4692-bbdf-c52e3d9b0568	NOT_AS_EXPECTED	PICKED_UP	2026-08-10 08:00:00	2026-08-12	\N
RET-005	ORD-017	ITEM-018	6f52bb95-3341-4a7b-a33c-9a5e67f9dd6f	QUALITY_ISSUE	COMPLETED	2026-08-05 03:00:00	2026-08-07	2026-08-10 03:00:00
RET-006	ORD-018	ITEM-019	5b6089d7-d2e6-4ba9-b8fd-598db511b129	WRONG_PRODUCT	COMPLETED	2026-08-07 02:00:00	2026-08-09	2026-08-11 02:00:00
\.


--
-- Data for Name: sellers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sellers (seller_id, company_id, seller_name, email, phone, city, state, rating, joined_date, status) FROM stdin;
SELL-001	COMP-001	TechWorld Retail	contact@techworldretail.in	+91-9845012345	Bengaluru	Karnataka	4.80	\N	ACTIVE
SELL-002	COMP-001	PrimeAudio India	support@primeaudio.in	+91-9820011223	Mumbai	Maharashtra	4.70	\N	ACTIVE
SELL-003	COMP-001	UrbanStyle Apparels	sales@urbanstyle.co.in	+91-9811098765	New Delhi	Delhi	4.50	\N	ACTIVE
SELL-004	COMP-001	HomeNest Living	care@homenestliving.in	+91-9440056789	Hyderabad	Telangana	4.60	\N	ACTIVE
SELL-005	COMP-001	GizmoHub Online	orders@gizmohub.in	+91-9764023456	Pune	Maharashtra	4.40	\N	ACTIVE
SELL-006	COMP-001	Apex Smart Electronics	service@apexsmart.in	+91-9840034567	Chennai	Tamil Nadu	4.60	\N	ACTIVE
SELL-007	COMP-001	Bharat Footwear Co	help@bharatfootwear.in	+91-9568012345	Agra	Uttar Pradesh	4.30	\N	ACTIVE
SELL-008	COMP-001	LuxeKitchen Appliances	info@luxekitchen.in	+91-9879023456	Ahmedabad	Gujarat	4.50	\N	ACTIVE
SELL-009	COMP-001	Aura Grooming Products	care@auragrooming.in	+91-9414012345	Jaipur	Rajasthan	3.90	\N	INACTIVE
SELL-010	COMP-001	Nova Collections	support@novacollections.in	+91-9830056789	Kolkata	West Bengal	3.40	\N	SUSPENDED
\.


--
-- Data for Name: shipments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.shipments (shipment_id, order_id, tracking_number, carrier, status, estimated_delivery_date, actual_delivery_date, shipped_at, delivered_at) FROM stdin;
SHIP-019	ORD-019	TRK-SHADOWFAX-995619255	Shadowfax	PROCESSING	2026-08-23	\N	\N	\N
SHIP-020	ORD-020	TRK-XPRESSBEES-491735568	XpressBees	DELIVERED	2026-08-15	2026-08-14	2026-08-12 17:00:00	\N
SHIP-001	ORD-001	TRK-DELHIVERY-764130526	Delhivery	DELIVERED	2026-08-19	2026-08-19	2026-08-17 00:00:00	\N
SHIP-002	ORD-002	TRK-BLUEDART-488302652	BlueDart	DELIVERED	2026-08-07	2026-08-07	2026-08-05 01:00:00	\N
SHIP-004	ORD-004	TRK-SHADOWFAX-306468299	Shadowfax	OUT_FOR_DELIVERY	2026-08-17	\N	2026-08-17 20:00:00	\N
SHIP-005	ORD-005	TRK-XPRESSBEES-856528252	XpressBees	DELAYED	2026-08-16	\N	2026-08-14 23:00:00	\N
SHIP-006	ORD-006	TRK-DELHIVERY-174684276	Delhivery	LOST	2026-08-13	\N	2026-08-11 21:00:00	\N
SHIP-007	ORD-007	TRK-BLUEDART-149203558	BlueDart	PROCESSING	2026-08-24	\N	\N	\N
SHIP-008	ORD-008	TRK-ECOMEXPRESS-810026086	Ecom Express	PROCESSING	\N	\N	\N	\N
SHIP-009	ORD-009	TRK-SHADOWFAX-344703907	Shadowfax	DELIVERED	2026-08-21	2026-08-21	2026-08-19 00:00:00	\N
SHIP-010	ORD-010	TRK-XPRESSBEES-930075810	XpressBees	SHIPPED	2026-08-19	\N	2026-08-15 12:00:00	\N
SHIP-011	ORD-011	TRK-DELHIVERY-410727955	Delhivery	PROCESSING	2026-08-24	\N	\N	\N
SHIP-012	ORD-012	TRK-BLUEDART-185675980	BlueDart	PROCESSING	\N	\N	\N	\N
SHIP-013	ORD-013	TRK-ECOMEXPRESS-349957310	Ecom Express	IN_TRANSIT	2026-08-19	\N	2026-08-17 05:00:00	\N
SHIP-014	ORD-014	TRK-SHADOWFAX-208449460	Shadowfax	DELIVERED	2026-08-12	2026-08-12	2026-08-10 00:00:00	\N
SHIP-015	ORD-015	TRK-XPRESSBEES-508157429	XpressBees	DELIVERED	2026-08-17	2026-08-17	2026-08-14 22:00:00	\N
SHIP-016	ORD-016	TRK-DELHIVERY-398471886	Delhivery	DELIVERED	2026-08-10	2026-08-10	2026-08-07 22:00:00	\N
SHIP-017	ORD-017	TRK-BLUEDART-586845604	BlueDart	DELIVERED	2026-08-04	2026-08-03	2026-08-01 17:00:00	\N
SHIP-018	ORD-018	TRK-ECOMEXPRESS-782560971	Ecom Express	DELIVERED	2026-08-08	2026-08-07	2026-08-05 16:00:00	\N
SHIP-021	ORD-021	TRK-DELHIVERY-274648506	Delhivery	DELIVERED	2026-08-13	2026-08-13	2026-08-10 22:00:00	\N
SHIP-022	ORD-022	TRK-BLUEDART-497478786	BlueDart	IN_TRANSIT	2026-08-20	\N	2026-08-17 21:00:00	\N
SHIP-023	ORD-023	TRK-ECOMEXPRESS-481469012	Ecom Express	DELIVERED	2026-08-11	2026-08-10	2026-08-08 19:00:00	\N
SHIP-024	ORD-024	TRK-SHADOWFAX-324956459	Shadowfax	DELIVERED	2026-08-14	2026-08-14	2026-08-11 22:00:00	\N
SHIP-025	ORD-025	TRK-XPRESSBEES-819595113	XpressBees	PROCESSING	2026-08-23	\N	\N	\N
\.


--
-- Data for Name: ticket_embeddings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ticket_embeddings (id, ticket_id, embedding, created_at) FROM stdin;
415ad0b2-0ab8-4cbc-b1b7-ff34a7df35ca	5713519c-e2f1-4348-b11a-83e01d622160	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4472136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4472136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4472136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4472136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.4472136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	2026-09-10 18:18:40.704534
\.


--
-- Data for Name: tickets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets (id, ref, customer_id, agent_id, subject, category, channel, status, priority, sla_due_at, sla_breached, sentiment, ai_confidence, ai_resolved, ai_summary, deleted_at, created_at, updated_at) FROM stdin;
b78e3d69-f0e0-4b36-866f-a1fe0c012eaa	TCK-97818	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Return & Replacement Request	Billing & Refunds	website_chat	new	high	2026-09-10 01:05:05.006884	f	\N	\N	f	\N	\N	2026-09-09 17:05:05.007472	2026-09-09 17:05:10.069133
c025e796-7ad9-4de8-be7b-689002d7343d	TCK-10324	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Order Status & Tracking	Billing & Refunds	website_chat	new	high	2026-09-10 01:46:54.75347	f	\N	\N	f	\N	\N	2026-09-09 17:46:54.753995	2026-09-09 17:47:58.582756
20b42ccb-bb63-4cde-a8fa-1828ae528f18	TCK-95221	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	How long does delivery take?	Shipping & Delivery	website_chat	new	medium	2026-09-10 18:29:53.990999	f	\N	\N	f	\N	\N	2026-09-10 10:29:53.991306	2026-09-10 10:29:55.015919
e13c2b3f-1c7d-44d3-abd0-c9ea5a60088b	TCK-84229	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Capital of India	general	website_chat	resolved	medium	2026-09-10 19:42:17.235339	f	\N	\N	t	\N	\N	2026-09-10 11:42:17.235822	2026-09-10 13:16:22.752713
71f00727-caa8-4658-9db7-0c4dbb7d2645	TCK-36881	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	All Info. About Home & Kitchen PRODUCTS	Billing & Refunds	website_chat	resolved	high	2026-09-10 23:08:37.102331	f	\N	\N	t	\N	\N	2026-09-10 15:08:37.102728	2026-09-10 15:10:27.777753
62b667d8-b19c-4451-a563-4845b06bbec2	TCK-83778	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Order Status & Tracking	general	website_chat	new	medium	2026-09-10 22:10:29.719212	f	\N	\N	f	\N	\N	2026-09-10 14:10:29.719548	2026-09-10 15:16:08.857653
c6384d2a-e873-4772-af84-73b664bf0b36	TCK-53935	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Product Catalog Overview	general	website_chat	new	medium	2026-09-10 23:32:54.61892	f	\N	\N	f	\N	\N	2026-09-10 15:32:54.619791	2026-09-10 15:35:33.481919
672f537a-e703-4ec8-8518-b7c2eee623b5	TCK-96716	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	How long does delivery take?	Shipping & Delivery	website_chat	new	medium	2026-09-10 18:35:19.885849	f	\N	\N	f	\N	\N	2026-09-10 10:35:19.886202	2026-09-10 10:35:20.408422
7a7110b1-9451-4771-a297-b59378914907	TCK-37200	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Can I change my delivery address?	Shipping & Delivery	website_chat	resolved	medium	2026-09-10 18:36:46.350266	f	\N	\N	t	\N	\N	2026-09-10 10:36:46.351075	2026-09-10 10:40:17.591064
5142c951-2b60-49b9-8c49-f63d872038f0	TCK-19858	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Order Status & Tracking	general	website_chat	resolved	medium	2026-09-10 19:59:04.312333	f	\N	\N	t	\N	\N	2026-09-10 11:59:04.313866	2026-09-10 12:23:31.469636
6c307a57-6db6-45cc-8a1a-cb06408ab35c	TCK-18324	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Product Catalog Overview	general	website_chat	new	medium	2026-09-10 18:34:59.610437	f	\N	\N	f	\N	\N	2026-09-10 10:34:59.610948	2026-09-10 13:29:46.512213
f4ad1c11-6675-4e48-ac1b-5954263b9e27	TCK-64883	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	All Info. of Home & Kitchen PRODUCTS	general	website_chat	new	medium	2026-09-10 22:41:09.458183	f	\N	\N	f	\N	\N	2026-09-10 14:41:09.458481	2026-09-10 14:41:34.211483
f84f326f-8fd7-4582-97d0-ac023dc09b08	TCK-40555	b93ba828-c127-4801-9059-5444918058e2	\N	Instagram DM from Heet Sanghani	instagram	instagram	escalated	medium	\N	f	\N	\N	f	\N	\N	2026-09-02 09:51:01.64548	2026-09-02 09:51:02.639499
9f75302d-8a1a-44a8-8660-4969785ae442	TCK-40503	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	What is your refund policy?	Billing & Refunds	website_chat	resolved	high	2026-09-10 23:24:40.856529	f	\N	\N	t	\N	\N	2026-09-10 15:24:40.85681	2026-09-14 16:47:09.411253
ea6e1612-4f0e-4925-9ced-2aa4693087f2	TCK-85785	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Aout My PRODUCT of ORDER-001	Billing & Refunds	website_chat	resolved	high	2026-09-15 01:12:42.347086	f	\N	\N	t	\N	\N	2026-09-14 17:12:42.350354	2026-09-14 17:13:39.202919
507f5a74-e09d-461c-b387-1372a84094f2	TCK-26948	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Every PRODUCTS for Gifting for Men	general	website_chat	resolved	medium	2026-09-15 00:22:27.628032	f	\N	\N	t	\N	\N	2026-09-14 16:22:27.628917	2026-09-14 16:45:55.188781
5faee52b-bcd9-442b-9136-148790eba194	TCK-94149	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Electronics Products	Escalation	website_chat	escalated	high	2026-09-15 00:18:27.667498	f	\N	\N	f	\N	\N	2026-09-14 16:18:27.668703	2026-09-14 17:36:55.12072
aab74641-2a47-4a99-bbcd-a1c7fa2dac72	TCK-82682	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Every PRODUCTS for Electronics	general	website_chat	resolved	medium	2026-09-14 23:59:27.679151	f	\N	\N	t	\N	\N	2026-09-14 15:59:27.681416	2026-09-14 16:46:22.548305
641222a4-43a8-4138-acf9-f2bd23a72544	TCK-73337	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	What is your refund policy?	Billing & Refunds	website_chat	resolved	high	2026-09-11 02:10:59.990044	f	\N	\N	t	\N	\N	2026-09-10 18:10:59.990416	2026-09-14 16:46:44.082245
096a4ed9-b378-49a4-b78b-ea3c45ab64df	TCK-57249	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	What is your refund policy?	Billing & Refunds	website_chat	resolved	high	2026-09-11 02:10:57.625307	f	\N	\N	t	\N	\N	2026-09-10 18:10:57.625697	2026-09-14 16:46:54.252825
5713519c-e2f1-4348-b11a-83e01d622160	TCK-66901	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	What is your refund policy?	Escalation	website_chat	resolved	high	2026-09-11 02:11:00.436439	f	\N	\N	t	Ticket 'What is your refund policy?' is currently waiting with 4 messages exchanged.	\N	2026-09-10 18:11:00.436961	2026-09-14 17:59:36.988706
7eb9c8b6-fa52-4022-b221-01198ce8d403	TCK-48313	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Where is my order?	Escalation	website_chat	escalated	high	2026-09-15 22:43:24.749269	f	\N	\N	f	\N	\N	2026-09-15 14:43:24.750943	2026-09-15 14:46:07.847381
1af2296b-f1ed-435f-ab75-e36bc02a47aa	TCK-15115	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Product Inquiry (PROD-001)	general	website_chat	new	medium	2026-09-15 20:10:53.130214	f	\N	\N	f	\N	\N	2026-09-15 12:10:53.132528	2026-09-15 12:23:46.486366
d48d3479-0618-4201-8d9a-515a666d1cae	TCK-44088	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Info. of Novaphone Pro 5g	general	website_chat	new	medium	2026-09-15 20:25:28.407991	f	\N	\N	f	\N	\N	2026-09-15 12:25:28.410026	2026-09-15 13:16:28.418188
73603b79-147f-428f-845e-dfabe07404e7	TCK-97364	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	My ORDER-001	Billing & Refunds	website_chat	new	high	2026-09-16 00:16:19.864055	f	\N	\N	f	\N	\N	2026-09-15 16:16:19.865822	2026-09-15 16:17:02.43138
48136439-fab6-4224-ae17-3fb3ca6a3a97	TCK-42794	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Info. of Novaphone Pro 5g	general	website_chat	new	medium	2026-09-15 21:49:33.523494	f	\N	\N	f	\N	\N	2026-09-15 13:49:33.717903	2026-09-15 13:54:08.891828
a88fe49f-6444-49c4-bfc2-b465c1e543e2	TCK-53499	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	General Support Query	general	website_chat	new	medium	2026-09-15 22:02:25.006253	f	\N	\N	f	\N	\N	2026-09-15 14:02:25.008759	2026-09-15 14:02:25.009763
b7d31821-eb98-43e9-9a03-a18455a7ba98	TCK-41972	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	All Info. for Classic Fit 100% Pure Cotton...	general	website_chat	new	medium	2026-09-15 21:54:52.548657	f	\N	\N	f	\N	\N	2026-09-15 13:54:52.551192	2026-09-15 14:29:03.334118
4c570e55-16f1-4885-94a3-3a406ea7beb1	TCK-56824	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Inquiry About My ORDER	general	website_chat	new	medium	2026-09-16 00:33:56.010142	f	\N	\N	f	\N	\N	2026-09-15 16:33:56.010878	2026-09-16 15:23:31.969568
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, email, name, password_hash, role, status, avatar_url, totp_secret, totp_enabled, created_at, updated_at, email_signature, channel, channel_customer_id, phone, customer_id, address, city, state, postal_code, country, company_id) FROM stdin;
b58c1521-0efc-4bae-a8a4-2ef5e70810eb	whatsapp_9106913089@channel.supporthub.internal	Heet Patel	__channel_customer__	customer	active	\N	\N	f	2026-09-02 09:49:15.448898	2026-09-02 09:49:15.449314	\N	whatsapp	9106913089	9106913089	\N	\N	\N	\N	\N	\N	\N
444d7140-ae08-44b0-b9e4-4734d87bd961	whatsapp_9104282872@channel.supporthub.internal	Heet Patel	__channel_customer__	customer	active	\N	\N	f	2026-09-02 09:49:15.273413	2026-09-02 09:49:15.273915	\N	whatsapp	9104282872	9104282872	\N	\N	\N	\N	\N	\N	\N
f399608c-b111-4148-a069-444a31b1ce0c	mihirk.brainerhub@gmail.com	Mihir	$2b$12$TfTPBR0V5QW2aqUCkI4LTelKgSnJmPsoUAw6s6lGpgLWPrrivh9cG	customer	active	\N	\N	f	2026-08-24 17:00:47.906145	2026-08-24 17:00:47.906259	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
4b64d0f2-7370-4f17-b00e-46618025e266	instagram_1038307988929264@supporthub.local	Akash Soni	external_instagram_1038307988929264	customer	active	https://instagram.famd5-4.fna.fbcdn.net/v/t51.82787-19/670297074_18167938135409626_4699725992919576518_n.jpg?stp=dst-jpg_s206x206_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ccb=7-5&_nc_sid=bf7eb4&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=sGX0x7UfK8MQ7kNvwH8rGBR&_nc_oc=Adp65vsmzC6WwrKF6qjDCv0zT4Ikc08k_JaLmWeDOKpRB-1p8hdbWhd_qkCQkHJY8Pc&_nc_zt=24&_nc_ht=instagram.famd5-4.fna&edm=ALmAK4EEAAAA&_nc_gid=8-qJslePuvP6nmsGR7wIxQ&oh=00_AQGs2J3KFLyeRET0CJubUVlGXJeSzVemPvIm1-AT0Z-TQw&oe=6A80CB53	\N	f	2026-08-11 16:58:10.098217	2026-08-11 16:58:10.098322	\N	instagram	1038307988929264	\N	\N	\N	\N	\N	\N	\N	\N
9cac773a-b11d-4fb2-a064-4932f5b94202	instagram_3186178738258152@supporthub.local	Mihir Kanzariya	external_instagram_3186178738258152	customer	active	https://instagram.famd5-5.fna.fbcdn.net/v/t51.82787-19/708754519_18129960619606059_2493243118152018562_n.jpg?stp=dst-jpg_s206x206_tt6&_nc_cat=101&_nc_map=urlgen_bucketless&ccb=7-5&_nc_sid=bf7eb4&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=xkTwRH6M95QQ7kNvwHudKPX&_nc_oc=AdrqPKPbLfMaZhBv64ttDuf5lG5H0y27ArjP8lbOjkPrKuMFERxsW7CLukDqCvmy6dA&_nc_zt=24&_nc_ht=instagram.famd5-5.fna&edm=ALmAK4EEAAAA&_nc_gid=Vfdm6G4pV_AeetJu1EuAkw&oh=00_AQHJ6iRrMuCtA984k3WGqdp98Yyy7hdV09nGOxTrwRameA&oe=6A80CE96	\N	f	2026-08-11 17:05:13.090814	2026-08-11 17:05:13.091397	\N	instagram	3186178738258152	\N	\N	\N	\N	\N	\N	\N	\N
c64e3806-b382-4689-9f1a-94114205ce5f	admin@supporthub.com	Admin User	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	admin	active	\N	\N	f	2026-07-28 08:00:25.178256	2026-07-28 08:00:25.178446	\N	\N	\N	+1 (555) 010-0001	\N	\N	\N	\N	\N	\N	\N
98d7e49a-2551-4bb8-b425-3b3226046c7e	heets.brainerhub@gmail.com	Heet Patel	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	admin	active	\N	\N	f	2026-07-28 07:00:30.539021	2026-07-28 07:00:30.539253	\N	\N	\N	+1 (555) 010-0002	\N	\N	\N	\N	\N	\N	\N
6f1218cf-07fd-41a5-97c4-185c7e2559b6	messenger_38499898592930667@supporthub.local	Heet Sanghani	external_messenger_user	customer	active	https://ui-avatars.com/api/?name=Heet+Sanghani&background=1877F2&color=fff&size=128&rounded=true	\N	f	2026-08-13 12:17:00.178029	2026-08-13 12:17:00.178154	\N	facebook	38499898592930667	\N	\N	\N	\N	\N	\N	\N	\N
b7e52df6-21dd-4fa2-bb0d-11961f360cd1	manager@supporthub.com	Manager User	$2b$12$qXY/VWSdzUx0W7UZIPkO4eRBf7vI5LMpXzWwM2Pu3QNGwhkRpB5ua	manager	active	\N	\N	f	2026-07-28 08:00:25.605791	2026-07-28 08:00:25.605974	\N	\N	\N	+1 (555) 010-0003	\N	\N	\N	\N	\N	\N	\N
646b7a11-99f7-4721-b183-f74dbec4bcc5	agent@supporthub.com	Agent User	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	agent	active	\N	\N	f	2026-07-28 08:00:26.026051	2026-07-28 08:00:26.026223	\N	\N	\N	+1 (555) 010-0005	\N	\N	\N	\N	\N	\N	\N
92afcf18-b36b-4c7a-a242-83689baff0dc	whatsapp_9103100185@channel.supporthub.internal	Heet Patel	__channel_customer__	customer	active	\N	\N	f	2026-09-02 09:49:15.11007	2026-09-02 09:49:15.11062	\N	whatsapp	9103100185	9103100185	\N	\N	\N	\N	\N	\N	\N
3f6a0843-51d6-4568-b5f6-b1c377ac3383	whatsapp_9102971500@channel.supporthub.internal	New Name	__channel_customer__	customer	active	\N	\N	f	2026-09-02 09:49:14.773924	2026-09-02 04:19:14.890117	\N	whatsapp	9102971500	9102971500	\N	\N	\N	\N	\N	\N	\N
906786ea-2932-40d9-b23e-d7c2e0963410	instagram_26806233522386775@supporthub.local	Zaru Patel	external_instagram_26806233522386775	customer	active	\N	\N	f	2026-08-11 15:36:02.044755	2026-08-11 15:36:02.045269	\N	instagram	26806233522386775	\N	\N	\N	\N	\N	\N	\N	\N
0a782dfe-8a13-4656-92e4-5689e49833a1	sarah.j@example.com	Sarah Johnson	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.067794	2026-09-09 09:28:20.872857	\N	\N	\N	+1 (555) 234-5678	CUST-002	\N	\N	\N	\N	India	COMP-001
70bf9179-aa0b-4134-bb43-6572d7eb240a	rohan.verma@example.com	Rohan Verma	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.072821	2026-09-09 09:28:20.875068	\N	\N	\N	+91-9811234567	CUST-003	House No. 42, Block C, Defence Colony	New Delhi	Delhi	110024	India	COMP-001
f202a0ff-09fd-4bbe-bb82-63dfa022c864	ananya.reddy@example.com	Ananya Reddy	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.076976	2026-09-09 09:28:20.877274	\N	\N	\N	+91-9440123456	CUST-004	Plot 18, Road No. 12, Banjara Hills	Hyderabad	Telangana	500034	India	COMP-001
233549a6-737c-4534-8b5c-cea20b12ffad	vikram.iyer@example.com	Vikram Iyer	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.081429	2026-09-09 09:28:20.879154	\N	\N	\N	+91-9840123456	CUST-005	New No. 15, 4th Main Road, RA Puram	Chennai	Tamil Nadu	600028	India	COMP-001
de90577d-bf90-4ad1-acd5-af943539b65b	sneha.kulkarni@example.com	Sneha Kulkarni	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.085896	2026-09-09 09:28:20.881111	\N	\N	\N	+91-9764123456	CUST-006	Row House 7, Nyati Estate, Mohammadwadi	Pune	Maharashtra	411060	India	COMP-001
da9ae675-d683-4d64-bbb5-298eaa791672	rajesh.banerjee@example.com	Rajesh Banerjee	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.090658	2026-09-09 09:28:20.88279	\N	\N	\N	+91-9830123456	CUST-007	Flat 2A, South City Residency, Prince Anwar Shah Road	Kolkata	West Bengal	700068	India	COMP-001
2adbb717-51da-424e-bdc5-0cc7840a476a	kavita.deshmukh@example.com	Kavita Deshmukh	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.09431	2026-09-09 09:28:20.885122	\N	\N	\N	+91-9822123456	CUST-008	102, Shanti Heights, Law College Road, Erandwane	Pune	Maharashtra	411004	India	COMP-001
1f3cac08-90fd-4f14-bbd0-50b8c32d3662	aditya.nair@example.com	Aditya Nair	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.098412	2026-09-09 09:28:20.887142	\N	\N	\N	+91-9847123456	CUST-009	Villa 12, Skyline Meadows, Kakkanad	Kochi	Kerala	682030	India	COMP-001
2d2e9163-288b-4994-bfc4-368bb117de95	neha.gupta@example.com	Neha Gupta	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.102578	2026-09-09 09:28:20.889099	\N	\N	\N	+91-9810123456	CUST-010	Tower 4, Flat 1102, Nirvana Country, Sector 50	Gurugram	Haryana	122018	India	COMP-001
639c918b-c490-4a64-8598-7943a3016f0e	siddharth.c@example.com	Siddharth Choudhury	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.107264	2026-09-09 09:28:20.891118	\N	\N	\N	+91-9435123456	CUST-011	House 28, Zoo Road Tiniali, RG Baruah Road	Guwahati	Assam	781024	India	COMP-001
1666975c-32b8-4a3f-994b-0cadb8c754a5	pooja.joshi@example.com	Pooja Joshi	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.111152	2026-09-09 09:28:20.893269	\N	\N	\N	+91-9414123456	CUST-012	45, Malviya Nagar, Near Calgiri Hospital	Jaipur	Rajasthan	302017	India	COMP-001
a2950fb1-86d1-42e0-acff-82037eb02962	manish.tiwari@example.com	Manish Tiwari	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.115431	2026-09-09 09:28:20.894996	\N	\N	\N	+91-9450123456	CUST-013	3/120, Vivek Khand, Gomti Nagar	Lucknow	Uttar Pradesh	226010	India	COMP-001
b395b112-7158-4b1e-95f1-d240ad28315b	deepika.rao@example.com	Deepika Rao	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.119573	2026-09-09 09:28:20.896829	\N	\N	\N	+91-9844123456	CUST-014	14, 2nd Cross, 7th Main, Indiranagar	Bengaluru	Karnataka	560038	India	COMP-001
218f5584-0624-4692-bbdf-c52e3d9b0568	karan.mehta@example.com	Karan Mehta	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.12435	2026-09-09 09:28:20.898457	\N	\N	\N	+91-9879123456	CUST-015	501, Heritage Horizon, CG Road, Navrangpura	Ahmedabad	Gujarat	380009	India	COMP-001
6f52bb95-3341-4a7b-a33c-9a5e67f9dd6f	meera.menon@example.com	Meera Menon	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.12809	2026-09-09 09:28:20.900629	\N	\N	\N	+91-9846123456	CUST-016	TC 15/1982, Cotton Hill, Vazhuthacaud	Thiruvananthapuram	Kerala	695014	India	COMP-001
5b6089d7-d2e6-4ba9-b8fd-598db511b129	arjun.kapoor@example.com	Arjun Kapoor	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.132244	2026-09-09 09:28:20.902373	\N	\N	\N	+91-9818123456	CUST-017	A-12, Sector 15A, Noida	Noida	Uttar Pradesh	201301	India	COMP-001
0f97f36b-0935-49a2-8de9-84bb3344ba5d	ritu.agarwal@example.com	Ritu Agarwal	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.136082	2026-09-09 09:28:20.904187	\N	\N	\N	+91-9331123456	CUST-018	8B, Alipore Park Road, Alipore	Kolkata	West Bengal	700027	India	COMP-001
2715e45f-a024-4eb6-9e71-7a3b5be57bf7	amit.singhania@example.com	Amit Singhania	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.14088	2026-09-09 09:28:20.905749	\N	\N	\N	+91-9826123456	CUST-019	12, Manoramaganj, Near Geeta Bhawan	Indore	Madhya Pradesh	452001	India	COMP-001
b95c612a-3514-4d63-8b62-1b9f2bd3c24f	shweta.bhatia@example.com	Shweta Bhatia	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.144961	2026-09-09 09:28:20.90778	\N	\N	\N	+91-9814123456	CUST-020	House 512, Sector 8B	Chandigarh	Chandigarh	160009	India	COMP-001
918d530e-ba04-41a7-a0a9-8dbc477f51e9	rahul.d@example.com	Rahul Dravid	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.149195	2026-09-09 09:28:20.909599	\N	\N	\N	+91-9880123456	CUST-021	33, 11th Main Road, Malleshwaram	Bengaluru	Karnataka	560003	India	COMP-001
a6191a36-88ed-4559-ae61-a985777583e4	divya.sri@example.com	Divya Srivastava	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.153197	2026-09-09 09:28:20.911612	\N	\N	\N	+91-9415123456	CUST-022	B-12, Sector C, Mahanagar	Lucknow	Uttar Pradesh	226006	India	COMP-001
a8328835-e5dd-4e0d-bbef-9e11ec27aa69	gaurav.saxena@example.com	Gaurav Saxena	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.157565	2026-09-09 09:28:20.913294	\N	\N	\N	+91-9829123456	CUST-023	C-14, Vaishali Nagar	Jaipur	Rajasthan	302021	India	COMP-001
1faf7b89-ee0d-4426-8ad0-1d890e4e92f2	suresh.pandey@example.com	Suresh Pandey	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.16186	2026-09-09 09:28:20.915398	\N	\N	\N	+91-9871123456	CUST-024	Flat 104, Golf Course Extension Road, Sector 65	Gurugram	Haryana	122101	India	COMP-001
47a50f4d-2bf9-42e7-b7d9-7a4251b7e115	tanya.malhotra@example.com	Tanya Malhotra	$2b$12$LJigtp.7FE4lMGH8f5UCu.A0hYjvELDgFGvYpcOYqQdkE.h8JgGXm	customer	active	\N	\N	f	2026-09-08 10:41:52.166125	2026-09-09 09:28:20.917231	\N	\N	\N	+91-9811987654	CUST-025	D-70, Greater Kailash 1	New Delhi	Delhi	110048	India	COMP-001
ac6d17a1-b2cc-40f9-ac52-925c912ebb69	priya.p@example.com	Priya Patel	$2b$12$DEWYPzmis.5GBep.pZd4Z.ft5YitdNVX4VTQp5m6tQgPob7DwEjee	manager	active	\N	\N	f	2026-09-09 16:49:17.593065	2026-09-09 16:49:17.593172	\N	\N	\N	+1 (555) 010-0004	\N	\N	\N	\N	\N	\N	\N
cb0abb46-6d76-4539-93e6-88317185329b	alex.t@example.com	Alex Turner	$2b$12$AVlrZunShNE4Y2OTwKHP9.9QIdbre4oIEIYCFtKkGASjJYIa.JeDO	customer	active	\N	\N	f	2026-09-09 16:49:18.109563	2026-09-09 16:49:18.109671	\N	\N	\N	+1 (555) 345-6789	CUST-026	\N	\N	\N	\N	\N	\N
af7fd2f5-f9b6-4a59-aa9a-6d72d2a128fe	michael.c@example.com	Michael Chen	$2b$12$0tJgRe5Epou7aX1cOcLlLecASlQv0Gp7tZEEp6pyN5IP6NPOfDdku	customer	active	\N	\N	f	2026-09-09 16:49:18.331963	2026-09-09 16:49:18.33214	\N	\N	\N	+1 (555) 456-7890	CUST-027	\N	\N	\N	\N	\N	\N
ae7e0c16-0c4d-4b61-b881-947260041824	rahul.s@example.com	Rahul Sharma	$2b$12$bGySLNMuUa8pVcQo/4f3AuSQGTEcCKis1tVkyahhoWkynnaFSm6da	customer	active	\N	\N	f	2026-09-09 16:49:18.562577	2026-09-09 16:49:18.56269	\N	\N	\N	+91-9899123456	CUST-028	\N	\N	\N	\N	\N	\N
4bad7cdc-e978-485c-a8b7-9dde0f9a3d20	david.b@example.com	David Brown	$2b$12$UUnxJ1IBcbwyWWfJZp6lxOGTrUT18uDvryM8eDg63fvPn0dTC9hPO	customer	active	\N	\N	f	2026-09-09 16:49:18.779027	2026-09-09 16:49:18.779125	\N	\N	\N	+1 (555) 567-8901	CUST-029	\N	\N	\N	\N	\N	\N
a0ff970f-028a-4d09-9b45-06281543f07a	elena.r@example.com	Elena Rostova	$2b$12$KEor09uXiAgw2p6YAPB9yOcopGVcm9XC9Po8DObTbopjv4Av/p1pO	customer	active	\N	\N	f	2026-09-09 16:49:18.995967	2026-09-09 16:49:18.996081	\N	\N	\N	+1 (555) 678-9012	CUST-030	\N	\N	\N	\N	\N	\N
414c5476-f89e-4c74-8a64-832e77789e7d	whatsapp_919824052103@channel.supporthub.internal	👑 Heet Sanghani 👑	$2b$12$ZqjyISQ9K63yo8/RQatMY.dXtAzlmF0pIQh9kaDOtoz7TmaKdvpse	customer	active	\N	\N	f	2026-09-09 16:49:19.216996	2026-09-09 16:49:19.217101	\N	whatsapp	919824052103	+91 98240 52103	\N	\N	\N	\N	\N	\N	\N
4a47565a-2ec1-404a-8f05-07490e1d9384	customer@supporthub.com	Aarav Sharma	$2b$12$5uFDBnkyAo2NLLOpKOQ1luekuAUmGTZNJh5oq6HoTxFm5757pUZWG	customer	active	\N	\N	f	2026-07-28 08:00:26.475598	2026-09-09 09:28:20.869209	\N	\N	+919123456789	+91-9876543210	CUST-001	Flat 402, Green Glen Layout, Outer Ring Road, Bellandur	Bengaluru	Karnataka	560103	India	COMP-001
b93ba828-c127-4801-9059-5444918058e2	instagram_2308674163238603@supporthub.local	Heet Sanghani	external_instagram_2308674163238603	customer	active	https://instagram.famd5-4.fna.fbcdn.net/v/t51.2885-19/485182575_1169046478270639_4343296096011791040_n.jpg?stp=dst-jpg_s206x206_tt6&_nc_cat=103&_nc_map=urlgen_bucketless&ccb=7-5&_nc_sid=bf7eb4&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=qcgq4TFjC-oQ7kNvwHRlyKF&_nc_oc=AdpNL7GyU68jMzJZSnXmOh0r45auCRHy33jXou9Kg8SroJbbV1O-x6QEKvw5ax8OT9Y&_nc_zt=24&_nc_ht=instagram.famd5-4.fna&edm=ALmAK4EEAAAA&oh=00_AQLWCj-E-Sxyr1-pAhcKGgQd-kC1iGSvmR6w5PD4nNYrfw&oe=6AA70CEE	\N	f	2026-08-10 17:42:41.824955	2026-08-10 17:42:41.825059	\N	instagram	2308674163238603	+91 91234 56789	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: webhook_events; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.webhook_events (id, event_id, channel, processed, error, processing_ms, raw_payload, received_at, processed_at) FROM stdin;
77c30338-e3aa-4f1b-bb83-330d31925e4c	wamid.TEST_04af468d	whatsapp	t	\N	49	\N	2026-08-19 11:41:40.005123	2026-08-19 11:41:40.029812
9be7f045-de7a-4f7b-aedf-e037ed49331b	wamid.LIVE_TEST_102	whatsapp	t	\N	61	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "+15550253483", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "Live Test Customer"}, "wa_id": "919876543210"}], "messages": [{"from": "919876543210", "id": "wamid.LIVE_TEST_102", "timestamp": "1700000000", "text": {"body": "Hi Support! What are your business hours?"}, "type": "text"}]}	2026-08-06 06:30:39.546066	2026-08-06 06:30:39.581901
d89bfc10-184f-46e8-bf49-7e9350b817c0	wamid.TEST_697a7da0	whatsapp	t	\N	78	\N	2026-08-06 05:29:24.831542	2026-08-06 05:29:24.867073
d175a3c7-48bb-4441-964a-d80ad7fe6c2f	wamid.TEST_35577247	whatsapp	t	\N	8	\N	2026-08-06 05:29:24.872705	2026-08-06 05:29:24.880059
fc28fc81-e9eb-4639-8f12-7cc8709d9c42	wamid.TEST_56788711	whatsapp	t	\N	6	\N	2026-08-06 05:29:24.882998	2026-08-06 05:29:24.888624
e16b71c7-6521-4aa4-8e95-ea4266effb15	wamid.TEST_9a9db653	whatsapp	t	\N	51	\N	2026-08-19 13:22:16.652784	2026-08-19 13:22:16.678914
4ad72010-6e6f-4881-81cb-d15a5a08ef57	wamid.TEST_3314a229	whatsapp	t	\N	7	\N	2026-08-06 05:29:24.892768	2026-08-06 05:29:24.899817
2fb9d047-2e94-4a01-b1db-74f3d424fbfb	wamid.TEST_e6cdcc1d	whatsapp	t	\N	7	\N	2026-08-06 05:29:24.902837	2026-08-06 05:29:24.909138
5f5864ac-07d1-4f74-a7f2-9fab36f89edf	wamid.TEST_70d6adcb	whatsapp	t	\N	9	\N	2026-08-19 13:22:16.68273	2026-08-19 13:22:16.690862
94d6f0b2-8eda-48ac-a5c6-020f77b6c899	wamid.TEST_6e38fd29	whatsapp	t	\N	7	\N	2026-08-06 05:29:24.913421	2026-08-06 05:29:24.920529
96d30158-98eb-4a29-977c-e9c4d174d7d3	wamid.TEST_03147c52	whatsapp	t	\N	7	\N	2026-08-06 05:29:24.923532	2026-08-06 05:29:24.93055
b3182659-2a07-4065-9b77-742f345ee1af	wamid.TEST_a885ff82	whatsapp	t	\N	41	\N	2026-08-19 13:22:58.847826	2026-08-19 13:22:58.865932
60d28ddf-b9e1-41b5-ab21-c3ce1b9fd93c	wamid.TEST_062fbfbc	whatsapp	t	\N	6	\N	2026-08-06 05:29:24.933677	2026-08-06 05:29:24.939188
8f4b8736-039d-4668-944d-c30f5da5d355	wamid.TEST_65b4bbc4	whatsapp	t	\N	7	\N	2026-08-06 05:29:24.942056	2026-08-06 05:29:24.948681
6732cce3-93af-422d-a2a5-fa218bf1f3f3	wamid.DEDUP_319d4c32	whatsapp	t	\N	7	\N	2026-08-06 05:29:24.953607	2026-08-06 05:29:24.960447
eee8e526-ccea-4415-a08b-6002c99abebc	wamid.DEDUP2_76af6b2d	whatsapp	t	\N	7	\N	2026-08-06 05:29:24.964376	2026-08-06 05:29:24.971327
548e2894-b843-46d3-b9ed-575b453c62e9	wamid.TEST_0ca0242d	whatsapp	t	\N	8	\N	2026-08-06 05:29:24.976325	2026-08-06 05:29:24.983728
8266ecea-7ff3-4226-b6e8-43059eb2c378	wamid.TEST_f2f36cba	whatsapp	t	\N	8	\N	2026-08-06 05:29:24.987134	2026-08-06 05:29:24.994235
f09421d9-86dd-4495-b6e5-b8943293407e	wamid.TEST_1c3740eb	whatsapp	t	\N	6	\N	2026-08-06 05:29:24.997362	2026-08-06 05:29:25.002718
2a48ac16-0f80-4561-83d6-1b0e19845aff	wamid.TEST_1899e700	whatsapp	t	\N	67	\N	2026-08-06 05:29:34.186846	2026-08-06 05:29:34.211558
5a48af0e-b534-4125-ae59-f09295a5ace2	wamid.TEST_f41718a2	whatsapp	t	\N	9	\N	2026-08-06 05:29:34.216906	2026-08-06 05:29:34.225205
c305d7bc-7cc6-4705-a9c2-a3581f9a795c	wamid.TEST_d811592f	whatsapp	t	\N	6	\N	2026-08-06 05:29:34.228003	2026-08-06 05:29:34.233559
3691ac67-20bb-48bd-b452-385915399a16	wamid.TEST_2c7aa7ae	whatsapp	t	\N	8	\N	2026-08-06 05:29:34.237911	2026-08-06 05:29:34.245241
6e5e6ef9-3fef-4858-8271-1f4e125655d2	wamid.TEST_66890cea	whatsapp	t	\N	7	\N	2026-08-06 05:29:34.24806	2026-08-06 05:29:34.255004
bec8577a-9c1d-4faf-8d88-2b30f62a8114	wamid.TEST_58b9c533	whatsapp	t	\N	7	\N	2026-08-06 05:29:34.259154	2026-08-06 05:29:34.266386
02018eb7-6a20-488e-8a47-4c2e7e10ae2f	wamid.TEST_4514dc80	whatsapp	t	\N	7	\N	2026-08-06 05:29:34.269482	2026-08-06 05:29:34.276387
d48e4e7e-d4bb-42e9-9889-3cedbfaf42f8	wamid.TEST_3bf50111	whatsapp	t	\N	6	\N	2026-08-06 05:29:34.279268	2026-08-06 05:29:34.28469
fbae49d8-da50-44b5-8b67-818ead83796e	wamid.TEST_31bc5eef	whatsapp	t	\N	7	\N	2026-08-06 05:29:34.287751	2026-08-06 05:29:34.294526
dfbe3abe-bb2e-437c-907f-8d9f841fc12c	wamid.DEDUP_f40a24a9	whatsapp	t	\N	8	\N	2026-08-06 05:29:34.299358	2026-08-06 05:29:34.306823
c0b2a11a-b0eb-4808-9ce9-bdd66755a2cb	wamid.DEDUP2_7920a1fb	whatsapp	t	\N	7	\N	2026-08-06 05:29:34.310527	2026-08-06 05:29:34.317297
63c4d1f9-5810-4f7c-be9d-03f25817b711	wamid.TEST_e0ae66a9	whatsapp	t	\N	7	\N	2026-08-06 05:29:34.322063	2026-08-06 05:29:34.329088
b1169604-5b2e-46e4-b08e-1839037401dc	wamid.TEST_31eda77f	whatsapp	t	\N	8	\N	2026-08-06 05:29:34.331966	2026-08-06 05:29:34.339633
9ce1a4e8-ae4b-45fe-b837-3a2091915dbc	wamid.TEST_7ec21716	whatsapp	t	\N	6	\N	2026-08-06 05:29:34.342567	2026-08-06 05:29:34.347956
b0852b74-6872-4449-8dfb-18e360b5c39b	wamid.TEST_e5a77793	whatsapp	t	\N	7	\N	2026-08-06 05:29:34.350866	2026-08-06 05:29:34.357965
7381d146-1646-4b76-a8e0-981efaaa1c33	wamid.TEST_d770c798	whatsapp	t	\N	6	\N	2026-08-06 05:29:34.36407	2026-08-06 05:29:34.370242
8dd143be-fb47-4a5c-aa5e-cd80db413b86	wamid.TEST_c3532770	whatsapp	t	\N	7	\N	2026-08-06 05:29:34.373394	2026-08-06 05:29:34.380139
901ae291-4b7e-46c5-a283-0f3ff65c52fc	wamid.TEST_6df3ce1d	whatsapp	t	\N	7	\N	2026-08-06 05:29:34.384445	2026-08-06 05:29:34.391483
852497fa-7c55-469d-90ef-c6e5b8b322e4	wamid.TEST_e43339ce	whatsapp	t	\N	68	\N	2026-08-06 05:43:08.179631	2026-08-06 05:43:08.205267
e5da91c3-0c58-4eba-b9d6-2c857529d2ee	wamid.TEST_2896ce8f	whatsapp	t	\N	9	\N	2026-08-06 05:43:08.210596	2026-08-06 05:43:08.219253
79ff3045-c2fa-4cda-9fdd-1202e7469464	wamid.TEST_389ff033	whatsapp	t	\N	6	\N	2026-08-06 05:43:08.222416	2026-08-06 05:43:08.228377
f5ce1da0-47d6-4418-ab32-d5285bad4109	wamid.TEST_b7578ec6	whatsapp	t	\N	8	\N	2026-08-06 05:43:08.23274	2026-08-06 05:43:08.240269
2ab40fa4-49b4-407d-9a27-f1c234333656	wamid.TEST_e087d8f1	whatsapp	t	\N	7	\N	2026-08-06 05:43:08.24308	2026-08-06 05:43:08.249774
2a87b80f-09ff-4353-a220-c66b30667785	wamid.TEST_43ca591f	whatsapp	t	\N	8	\N	2026-08-06 05:43:08.253926	2026-08-06 05:43:08.261322
ff82f5cb-775f-4dc1-b3bd-384986fdf578	wamid.TEST_4c4104ba	whatsapp	t	\N	7	\N	2026-08-06 05:43:08.264284	2026-08-06 05:43:08.271375
af3321fa-f7f5-466b-a475-df391b3b22b5	wamid.TEST_82128f88	whatsapp	t	\N	6	\N	2026-08-06 05:43:08.274314	2026-08-06 05:43:08.279758
46fba533-576b-4505-9088-c7111a75cd54	wamid.TEST_baacb635	whatsapp	t	\N	7	\N	2026-08-06 05:43:08.282823	2026-08-06 05:43:08.289845
23fb577b-142b-4503-826b-4eedf6fad50f	wamid.DEDUP_08895ce8	whatsapp	t	\N	7	\N	2026-08-06 05:43:08.294387	2026-08-06 05:43:08.301616
4cdfd6e2-dba3-4093-bf84-f60199df50f5	wamid.DEDUP2_344e7b15	whatsapp	t	\N	7	\N	2026-08-06 05:43:08.305501	2026-08-06 05:43:08.312256
d002e18c-5c4b-4ee0-b5be-5c1cea3ada37	wamid.TEST_0fd4d0f6	whatsapp	t	\N	7	\N	2026-08-06 05:43:08.317117	2026-08-06 05:43:08.324122
5509727b-188f-49c4-8a1e-1117e13fddfd	wamid.TEST_c52b5269	whatsapp	t	\N	8	\N	2026-08-06 05:43:08.327323	2026-08-06 05:43:08.335191
534eb63a-4f28-416a-8020-04a929dc117a	wamid.TEST_d766e99a	whatsapp	t	\N	6	\N	2026-08-06 05:43:08.338191	2026-08-06 05:43:08.343602
57e4af35-d2e2-4f4b-bb7b-247b0053d311	wamid.TEST_4e95556d	whatsapp	t	\N	7	\N	2026-08-06 05:43:08.346613	2026-08-06 05:43:08.353532
117f78f8-3b4d-4508-9587-8cad5991d5b4	wamid.TEST_eb02e2f0	whatsapp	t	\N	6	\N	2026-08-06 05:43:08.359556	2026-08-06 05:43:08.365721
c137120e-c714-43fa-86e3-7727f885dc54	wamid.TEST_ddce11bd	whatsapp	t	\N	7	\N	2026-08-06 05:43:08.369052	2026-08-06 05:43:08.375891
f7bd97ab-be67-4e7c-8d55-0c0b9466764b	wamid.TEST_4aea30f7	whatsapp	t	\N	7	\N	2026-08-06 05:43:08.380067	2026-08-06 05:43:08.387147
9ecb7868-decb-4d15-8256-1cd3f0fc6a17	wamid.TEST_fe89f2f2	whatsapp	t	\N	74	\N	2026-08-06 05:53:42.645202	2026-08-06 05:53:42.674194
df1fa1cb-2d12-486d-8e83-85e5f217f6ea	wamid.TEST_237b63dd	whatsapp	t	\N	9	\N	2026-08-06 05:53:42.680778	2026-08-06 05:53:42.689509
cc45aa0f-e651-4e02-a74a-173b1353c4aa	wamid.TEST_145f3cd4	whatsapp	t	\N	7	\N	2026-08-06 05:53:42.69271	2026-08-06 05:53:42.698859
f0e2e3d5-6cf7-4495-9c8b-6548ece34e54	wamid.TEST_0c23fae6	whatsapp	t	\N	8	\N	2026-08-06 05:53:42.70296	2026-08-06 05:53:42.710497
d9d58502-ca4a-4e7d-b2e3-194fcde10d7e	wamid.TEST_6f2458e1	whatsapp	t	\N	7	\N	2026-08-06 05:53:42.713378	2026-08-06 05:53:42.720336
f69bb14f-10d4-47de-99fd-a6b320fe1fe1	wamid.TEST_02655eb8	whatsapp	t	\N	8	\N	2026-08-06 05:53:42.724113	2026-08-06 05:53:42.731801
0b3c4b5b-e3be-4b65-8557-fbbe4bd2862f	wamid.TEST_41714019	whatsapp	t	\N	8	\N	2026-08-06 05:53:42.734622	2026-08-06 05:53:42.74201
9bd116f3-f7dd-4d17-897c-768eee3011db	wamid.TEST_2544d1b8	whatsapp	t	\N	6	\N	2026-08-06 05:53:42.744829	2026-08-06 05:53:42.750261
1d0a175a-a7ec-4992-b85d-945f53c63e07	wamid.TEST_30c45fa0	whatsapp	t	\N	7	\N	2026-08-06 05:53:42.753226	2026-08-06 05:53:42.760346
bb79e05f-eb60-4078-ac59-e05374d7743b	wamid.DEDUP_adcc9fce	whatsapp	t	\N	7	\N	2026-08-06 05:53:42.764935	2026-08-06 05:53:42.772055
93eb9dc4-c32b-4f99-bdfe-b9ae25cda473	wamid.DEDUP2_56b4d3bd	whatsapp	t	\N	7	\N	2026-08-06 05:53:42.775925	2026-08-06 05:53:42.783198
9263df4a-0c89-4641-8dcc-3d23590f0139	wamid.TEST_7764597b	whatsapp	t	\N	7	\N	2026-08-06 05:53:42.787382	2026-08-06 05:53:42.794467
964e4e09-6553-44c4-8e14-3d9469f6341a	wamid.TEST_f9869899	whatsapp	t	\N	8	\N	2026-08-06 05:53:42.797365	2026-08-06 05:53:42.804747
9685b670-d95a-4b00-9351-dcbe00a2ba75	wamid.TEST_01ac693a	whatsapp	t	\N	6	\N	2026-08-06 05:53:42.807486	2026-08-06 05:53:42.813258
e36dd432-504a-4f39-b573-397d97f5970e	wamid.TEST_6173de13	whatsapp	t	\N	7	\N	2026-08-06 05:53:42.816098	2026-08-06 05:53:42.822984
f63fe6e9-7895-4b04-892a-ab3b6736bb62	wamid.TEST_20f87b54	whatsapp	t	\N	8	\N	2026-08-06 05:53:42.828661	2026-08-06 05:53:42.836625
cbd3da3e-44e6-44d1-8501-e14a3b060dd4	wamid.TEST_e65d270e	whatsapp	t	\N	7	\N	2026-08-06 05:53:42.83949	2026-08-06 05:53:42.846654
61cfd1a9-57ab-436c-8519-251ad43244d1	wamid.TEST_44a7281f	whatsapp	t	\N	7	\N	2026-08-06 05:53:42.850256	2026-08-06 05:53:42.857088
50138ac5-ffc4-41dd-85e1-8694d73de802	m_ws_broadcast_test_658d7cf6	instagram	t	\N	\N	{"sender": {"id": "23086741_aba4"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_658d7cf6", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-14 06:49:05.052133	\N
dd5a898a-72da-4b37-bf36-5409ef1d5a22	wamid.HBgLOTE5ODc2NTQzMjEwFQIAERgSQURBMDM3ODU2RTA1MzA3QzUA	whatsapp	t	\N	81	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15550253483", "phone_number_id": "123456"}, "contacts": [{"profile": {"name": "Test Customer"}, "wa_id": "919876543210"}], "messages": [{"from": "919876543210", "id": "wamid.HBgLOTE5ODc2NTQzMjEwFQIAERgSQURBMDM3ODU2RTA1MzA3QzUA", "timestamp": "1700000000", "text": {"body": "Test message signature check"}, "type": "text"}]}	2026-08-06 06:27:06.150559	2026-08-06 06:27:06.179426
a5d24949-9936-444f-a958-0a3c2e0d7494	m_auto_342395b4	instagram	t	\N	\N	{"sender": {"id": "auto_ai_886fea"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_342395b4", "text": "Do you ship internationally?"}}	2026-08-13 13:09:42.637391	\N
d59a4fef-21e7-4756-b48d-092e2e5f1c74	wamid.TEST_PARSE_001	whatsapp	t	\N	9	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "+15550253483", "phone_number_id": "PN_123456789"}, "contacts": [{"profile": {"name": "Alice Smith"}, "wa_id": "919876543210"}], "messages": [{"from": "919876543210", "id": "wamid.TEST_PARSE_001", "timestamp": "1700000000", "text": {"body": "Hello, I need help with my account!"}, "type": "text"}]}	2026-08-06 06:27:26.28933	2026-08-06 06:27:26.297568
a1c8b7fd-fd86-4c1f-b9ab-b42083db6bf6	ABGGFlA5Fpa	whatsapp	t	\N	82	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "16505551111", "phone_number_id": "123456123"}, "contacts": [{"profile": {"name": "test user name"}, "wa_id": "16315551181", "user_id": "US.13491208655302741918"}], "messages": [{"id": "ABGGFlA5Fpa", "timestamp": "1504902988", "from": "16315551181", "from_user_id": "US.13491208655302741918", "type": "text", "text": {"body": "this is a text message"}}]}	2026-08-06 08:34:47.290556	2026-08-06 08:34:47.328035
9f360c0d-b60a-4675-873e-722aeb707802	m_auto_0c02b5e0	instagram	t	\N	\N	{"sender": {"id": "auto_ai_8bfcf3"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_0c02b5e0", "text": "Do you ship internationally?"}}	2026-08-13 05:36:54.635153	\N
bce14d56-c330-4260-9c02-8f0de6f7f887	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDNGRDk2MzAzRDhDQkFFQjAzRAA=	whatsapp	t	\N	62	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDNGRDk2MzAzRDhDQkFFQjAzRAA=", "timestamp": "1786006952", "text": {"body": "Hello"}, "type": "text"}]}	2026-08-06 09:02:34.662583	2026-08-06 09:02:34.688193
4fee78f1-5a61-4fb4-83bb-39c1e9200a7a	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDNBOUYwOEY3NENGMkMwNjREMgA=	whatsapp	t	\N	47	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDNBOUYwOEY3NENGMkMwNjREMgA=", "timestamp": "1786008058", "text": {"body": "Hello AI"}, "type": "text"}]}	2026-08-06 09:20:59.496944	2026-08-06 09:20:59.518811
ac8b8803-71d4-44e5-9ec5-55ef85b70085	m_exact_test_3570bdfa	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_3570bdfa", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-13 05:36:57.060945	\N
ea338d40-fd1c-4d8d-b10c-6f1d005237a7	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEE0MjhBNUVBMDM0ODI1MTE2RgA=	whatsapp	t	\N	64	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEE0MjhBNUVBMDM0ODI1MTE2RgA=", "timestamp": "1786008475", "text": {"body": "Hello"}, "type": "text"}]}	2026-08-06 09:27:56.840773	2026-08-06 09:27:56.86769
24232454-be62-413e-803d-6f76154148b9	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDk4M0U5MEUyMDJFQTQ4Q0RFRgA=	whatsapp	t	\N	47	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDk4M0U5MEUyMDJFQTQ4Q0RFRgA=", "timestamp": "1786008413", "text": {"body": "Hello"}, "type": "text"}]}	2026-08-06 09:30:56.857572	2026-08-06 09:30:56.880413
4d4d728e-8fe2-47bb-8216-c9cf48d61388	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDUwNDVCOUE1MDg1OTYyMjM0MQA=	whatsapp	t	\N	45	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDUwNDVCOUE1MDg1OTYyMjM0MQA=", "timestamp": "1786009080", "text": {"body": "I forgot my password. Can you help me reset it?"}, "type": "text"}]}	2026-08-06 09:38:01.57761	2026-08-06 09:38:01.593713
f356b1c4-4715-422e-bb76-7bfb2910db6e	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEMwOTE4NkUzRDVCOTM2RTRFRQA=	whatsapp	t	\N	20	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEMwOTE4NkUzRDVCOTM2RTRFRQA=", "timestamp": "1786012052", "text": {"body": "Thanks, that fixed it!"}, "type": "text"}]}	2026-08-06 10:27:34.150478	2026-08-06 10:27:34.167972
8fcd73a6-f58d-44c5-81e1-d49d103b4434	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDJBNzc2NTJBRTVFNzdBOUIwRgA=	whatsapp	t	\N	15	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDJBNzc2NTJBRTVFNzdBOUIwRgA=", "timestamp": "1786012432", "text": {"body": "Thanks, that fixed it!"}, "type": "text"}]}	2026-08-06 10:33:53.76987	2026-08-06 10:33:53.782704
f4463f32-2aef-4405-b27d-9055d1cddb9f	wamid.TEST_REAL_TIME_SEND_101	whatsapp	t	\N	70	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "+15550253483", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103"}], "messages": [{"from": "919824052103", "id": "wamid.TEST_REAL_TIME_SEND_101", "timestamp": "1700000000", "text": {"body": "Hello SupportHub! Testing live outbound WhatsApp AI auto-reply."}, "type": "text"}]}	2026-08-06 10:47:48.152512	2026-08-06 10:47:48.177684
531d0d1e-333f-4e75-a886-891e7c7f113a	wamid.TEST_REAL_TIME_SEND_102	whatsapp	t	\N	67	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "+15550253483", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103"}], "messages": [{"from": "919824052103", "id": "wamid.TEST_REAL_TIME_SEND_102", "timestamp": "1700000000", "text": {"body": "Hello SupportHub! Testing live outbound WhatsApp AI auto-reply."}, "type": "text"}]}	2026-08-06 10:48:24.794339	2026-08-06 10:48:24.819673
95ec6492-5a62-4fc6-939c-71b1d8eccef5	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDE3QTdDNDY0RDMxNUU4OTU2RAA=	whatsapp	t	\N	51	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDE3QTdDNDY0RDMxNUU4OTU2RAA=", "timestamp": "1786013346", "text": {"body": "Thanks, that fixed it!"}, "type": "text"}]}	2026-08-06 10:49:07.594352	2026-08-06 10:49:07.617647
b689460f-a977-46d9-9bcc-d5a9b5940fc5	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1Mzc4OTY4NTc0NDU5NjUyNTUxMDMxMjA3NzU1Nzc2MAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786428518445, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1Mzc4OTY4NTc0NDU5NjUyNTUxMDMxMjA3NzU1Nzc2MAZDZD", "text": "REAL FINAL E2E INSTAGRAM TEST 2026-08-11-1135"}}	2026-08-11 06:08:39.603104	\N
bcefea67-22f1-4822-bab0-3a4faca6e2d4	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEQ2N0UzQzcwMTE0NjIyNDM1NQA=	whatsapp	t	\N	10	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEQ2N0UzQzcwMTE0NjIyNDM1NQA=", "timestamp": "1786013371", "text": {"body": "close this chat"}, "type": "text"}]}	2026-08-06 10:49:31.965309	2026-08-06 10:49:31.9742
eb1f5f6b-a27c-43c0-b901-c2bb966f7d12	wamid.TEST_c34f9624	whatsapp	t	\N	51	\N	2026-08-19 13:32:54.418307	2026-08-19 13:32:54.44544
6e4cfc4a-677a-4804-a157-914df8d54ca4	wamid.TEST_CLOSE_CHAT_INTENT_103	whatsapp	t	\N	70	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "+15550253483", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103"}], "messages": [{"from": "919824052103", "id": "wamid.TEST_CLOSE_CHAT_INTENT_103", "timestamp": "1700000000", "text": {"body": "close this chat"}, "type": "text"}]}	2026-08-06 10:56:02.804669	2026-08-06 10:56:02.832001
ca93fb65-b3bf-4e56-b023-47802dbde45f	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDEyNTY3NjczMDg1Nzc4MDU2MTkwNTU1Nzk2Mjc1MgZDZD	instagram	t	\N	\N	{"sender": {"id": "26806233522386775"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786446732553, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDEyNTY3NjczMDg1Nzc4MDU2MTkwNTU1Nzk2Mjc1MgZDZD", "text": "Hii"}}	2026-08-11 11:12:13.577596	\N
087f5be6-459f-4e1e-a779-0a842dce169c	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDk5RkYzQjM3RDkwMTYzRTI1RAA=	whatsapp	t	\N	24	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDk5RkYzQjM3RDkwMTYzRTI1RAA=", "timestamp": "1786021118", "text": {"body": "hi"}, "type": "text"}]}	2026-08-06 12:58:40.661846	2026-08-06 12:58:40.683016
1ae5cf24-cf9e-4c14-a34d-94db3b35a16b	m_auto_89979e50	instagram	t	\N	\N	{"sender": {"id": "auto_ai_8d35f5"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_89979e50", "text": "Do you ship internationally?"}}	2026-08-13 13:09:48.304484	\N
de70fe1b-3e09-4af4-9f79-011ec5edf7ae	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDEzMzdDQUZCMUY1MkY3RTMzNAA=	whatsapp	t	\N	13	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDEzMzdDQUZCMUY1MkY3RTMzNAA=", "timestamp": "1786021173", "text": {"body": "hi"}, "type": "text"}]}	2026-08-06 12:59:34.735725	2026-08-06 12:59:34.747085
425bbff1-6b39-40c6-a243-5d598730dd96	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDdEQTMzMENDODNDRkFGNUZGRgA=	whatsapp	t	\N	20	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDdEQTMzMENDODNDRkFGNUZGRgA=", "timestamp": "1786021434", "text": {"body": "hi"}, "type": "text"}]}	2026-08-06 13:03:55.585255	2026-08-06 13:03:55.602093
a1da3819-1e50-4886-bf76-b1be245dddd0	wamid.TEST_c0007986	whatsapp	t	\N	80	\N	2026-08-19 11:35:39.95291	2026-08-19 11:35:39.982071
cedb5649-4ac2-4d46-b511-4af359d70d04	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEJERTY2NDJFMUZENkMyRUExRQA=	whatsapp	t	\N	28	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEJERTY2NDJFMUZENkMyRUExRQA=", "timestamp": "1786083209", "text": {"body": "How do I request an updated invoice or receipt?"}, "type": "text"}]}	2026-08-07 06:13:31.388799	2026-08-07 06:13:31.412058
f1fd2e8b-284d-494b-8b98-12cca3014881	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQxOTc4NDA1Nzc0NDUwOTE2OTg1NjUxMjI2MjE0NAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786516886252, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQxOTc4NDA1Nzc0NDUwOTE2OTg1NjUxMjI2MjE0NAZDZD", "attachments": [{"type": "image", "payload": {"url": "https://lookaside.fbsbx.com/ig_messaging_cdn/?asset_id=1805902864109822&signature=Ab1zhKp3xrbQ_mNQ4eGOi7aSLQQQtnv8X6zurUfHRMU9aKfRHM6tXNioES6rFjM7saI6rUJ0Dqk_X4tsGfW_iXsj0f6NLU1AjGSteGasSu_r-NCgQUmrT9hz9bzlpqvXpYrluXek6YT2A5wLiagF75vVQO5tOZ2art2pn7rMfNzEaeFdlwaFcqF_bnJkhlFKbKRRDXFVVS49rLb7dGkBxEG1eXMfWOM"}}]}}	2026-08-12 06:41:29.154814	\N
b439dcce-699c-4fd6-a4a5-fd7041ce3f0a	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDEzODMzMTY3MjEyOTk4NDUxNTY3MTcwMjExMDIwOAZDZD	instagram	t	\N	\N	{"sender": {"id": "26806233522386775"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786447418579, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDEzODMzMTY3MjEyOTk4NDUxNTY3MTcwMjExMDIwOAZDZD", "text": "I forget my password,   can you help me reset it?"}}	2026-08-11 11:23:39.473856	\N
6f86b0e5-4baa-4f8a-a19e-ebc5f2e7b691	wamid.TEST_31247e0f	whatsapp	t	\N	9	\N	2026-08-19 11:35:39.987347	2026-08-19 11:35:39.995911
a5054ee2-1e86-4441-84af-db6d7fcd83e8	wamid.TEST_779b0b7b	whatsapp	t	\N	7	\N	2026-08-19 11:35:39.99916	2026-08-19 11:35:40.005397
81287bae-6766-481f-b862-87021a38a080	m_ws_broadcast_test_cb5c078f	instagram	t	\N	\N	{"sender": {"id": "23086741_7148"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_cb5c078f", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-13 13:18:15.915838	\N
f48c8ef6-7e03-4a93-b837-2ee8ece2ccfc	wamid.TEST_634efe62	whatsapp	t	\N	49	\N	2026-08-19 11:41:40.062436	2026-08-19 11:41:40.087796
11ebc147-807d-4589-8d04-09b8d3558c2c	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDEyNzQ5ODMxMDYyNDEwMDc2MzQzNTc4ODE0MDU0NAZDZD	instagram	t	\N	\N	{"sender": {"id": "26806233522386775"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786446831301, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDEyNzQ5ODMxMDYyNDEwMDc2MzQzNTc4ODE0MDU0NAZDZD", "text": "I forget my password,   can you help me reset it?"}}	2026-08-11 11:13:52.140409	\N
cf0304ba-29c5-4865-b52c-c923da355a90	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDQ5ODNCQjUwN0YwMzA3NDFGMAA=	whatsapp	t	\N	22	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDQ5ODNCQjUwN0YwMzA3NDFGMAA=", "timestamp": "1786354522", "text": {"body": "hi"}, "type": "text"}]}	2026-08-10 09:35:24.620815	2026-08-10 09:35:24.640294
38c0b8b9-0afe-4675-92b1-802f9b99b34e	wamid.TEST_f234a03a	whatsapp	t	\N	47	\N	2026-08-20 05:35:29.252253	2026-08-20 05:35:29.275257
95cd0463-eed8-447d-9e15-f26a2723f0fd	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMERDQTJFMDFCQzk3Qjk0OUEzNQA=	whatsapp	t	\N	14	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMERDQTJFMDFCQzk3Qjk0OUEzNQA=", "timestamp": "1786354598", "text": {"body": "hi"}, "type": "text"}]}	2026-08-10 09:36:39.809651	2026-08-10 09:36:39.820566
ee958d38-1128-4546-b127-50a9a036b345	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDgzNzJGODdGMUEyQzdEMzAxMgA=	whatsapp	t	\N	23	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDgzNzJGODdGMUEyQzdEMzAxMgA=", "timestamp": "1786513962", "type": "image", "image": {"caption": "what i need to select for the query : forgot my password. Can you help me reset it?", "mime_type": "image/jpeg", "sha256": "MATtC7xPBOcJ3aeplVdQEmYXuK8UGltWZHsHLtQn0AQ=", "id": "1030733666623164", "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=1030733666623164&source=webhook&ext=1786514265&hash=ATyO7GntBbzPpJ5R7ArKsCvn2rFhjDtiR-W8GoNbrBzSuA"}}]}	2026-08-12 05:52:47.186054	2026-08-12 05:52:47.203426
2dcf67e6-138d-46bb-af8a-a96449748925	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEFGRDk4MDI1Q0ZFNDAzNDNFRAA=	whatsapp	t	\N	9	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMEFGRDk4MDI1Q0ZFNDAzNDNFRAA=", "timestamp": "1786354659", "text": {"body": "hi"}, "type": "text"}]}	2026-08-10 09:37:40.069021	2026-08-10 09:37:40.0768
21ab84f9-3b72-4d2e-b7e8-c2e4a4bd002d	wamid.TEST_3ab0ecf2	whatsapp	t	\N	9	\N	2026-08-19 11:41:40.09105	2026-08-19 11:41:40.100027
d45d80d0-9f93-4e3e-ad94-5973a11c7f04	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQzMjYwMzkxOTM0NjY0NTc2ODczODczNjk2MzU4NAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786517581218, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQzMjYwMzkxOTM0NjY0NTc2ODczODczNjk2MzU4NAZDZD", "text": "what i need to select for the query : forgot my password. Can you help me reset it?"}}	2026-08-12 06:53:02.158362	\N
413e479f-36b1-4707-8eb9-856ab444a8d0	mid.1234567890	facebook	t	\N	\N	{"sender": {"id": "test_fb_54f799ca"}, "recipient": {"id": "mock_page_id"}, "message": {"mid": "mid.1234567890", "text": "Hello SupportHub from Messenger!"}}	2026-08-13 13:10:20.339011	\N
5fb40571-8ee0-44d0-b75a-c80b3c1e8428	m_real_dm_test_380d87db	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_real_dm_test_380d87db", "text": "REAL DM AFTER PUBLISH 1735"}}	2026-08-10 12:12:41.81308	\N
8cfbdcdb-ea7a-4ae0-a412-fb38d62f4234	m_auto_810056e4	instagram	t	\N	\N	{"sender": {"id": "auto_ai_ec05d1"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_810056e4", "text": "Do you ship internationally?"}}	2026-08-13 05:37:10.15085	\N
401e4a17-6f4c-4d28-966d-cea672f31074	m_auto_43a392c5	instagram	t	\N	\N	{"sender": {"id": "auto_ai_90f7da"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_43a392c5", "text": "Do you ship internationally?"}}	2026-08-13 05:41:22.29384	\N
911886b0-9ab3-4500-af16-9f1e7f68ed60	m_CeJMrbcGmw5JcwzfJou25KBR9GLU8WS3E1hs56gsQqcaIVJRtizJqmfkNe0hk9zXCfPfb6qxssWeoYDUhw872A	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786617984126, "message": {"mid": "m_CeJMrbcGmw5JcwzfJou25KBR9GLU8WS3E1hs56gsQqcaIVJRtizJqmfkNe0hk9zXCfPfb6qxssWeoYDUhw872A", "text": "what i need to select for the query : forgot my password. Can you help me reset it?"}}	2026-08-13 10:46:25.033493	\N
033ff311-3a7c-447d-92dc-d0883f336899	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjYwMTQ3MDY2MTcxNTE3ODYyNzQyOTYzNTcxOTE2OAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786364105177, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjYwMTQ3MDY2MTcxNTE3ODYyNzQyOTYzNTcxOTE2OAZDZD", "text": "INSTAGRAM E2E TEST 2026-NEW-001"}}	2026-08-10 12:15:06.051608	\N
29664b49-a266-4821-9881-9b044ef639de	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjYwMzY3ODM0MDgwMDA3OTE4OTY5ODAzMDg2MjMzNgZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786364224855, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjYwMzY3ODM0MDgwMDA3OTE4OTY5ODAzMDg2MjMzNgZDZD", "text": "REALTIME TEST 2026-08-10"}}	2026-08-10 12:17:05.628093	\N
ec491d23-3180-4a41-827d-e47a51694dc7	m_ws_broadcast_test_28a1086d	instagram	t	\N	\N	{"sender": {"id": "23086741_487b"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_28a1086d", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-13 13:11:14.795883	\N
eb2a07a8-0ced-41f6-8a25-fd5a2f40bc33	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjYxMDM5OTgzNDgwMjcwOTQzNDI1MjI0MzUwMTA1NgZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786364589228, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjYxMDM5OTgzNDgwMjcwOTQzNDI1MjI0MzUwMTA1NgZDZD", "text": "REALTIME TEST 2026-08-10-FINAL"}}	2026-08-10 12:23:10.211759	\N
ef8cc68f-c4c7-4872-8f32-c6491f1e48bb	wamid.TEST_4a09413d	whatsapp	t	\N	46	\N	2026-08-19 13:32:54.480975	2026-08-19 13:32:54.50233
16b551a6-9328-4b75-86f0-795cdc38d975	wamid.TEST_6002cb11	whatsapp	t	\N	46	\N	2026-08-19 11:41:40.133972	2026-08-19 11:41:40.153778
954637c2-d959-4b96-b484-7fce3c42900a	m_test_realtime_001_final	instagram	t	\N	\N	{"sender": {"id": "23086741"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786365300000, "message": {"mid": "m_test_realtime_001_final", "text": "FINAL REALTIME INSTAGRAM TEST 001"}}	2026-08-10 12:35:00.153243	\N
be2b2f3d-4d7c-469c-9ae1-f5c09049f1d9	m_test_realtime_002_latest	instagram	t	\N	\N	{"sender": {"id": "23086741"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786365400000, "message": {"mid": "m_test_realtime_002_latest", "text": "FINAL REALTIME INSTAGRAM TEST 002 LATEST TICKET"}}	2026-08-10 12:36:40.806924	\N
2b121e28-3c82-46eb-a3c8-54cfc80015a8	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDA5RkM0Q0ZERDgzQTQ4NDlEOQA=	whatsapp	t	\N	21	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDA5RkM0Q0ZERDgzQTQ4NDlEOQA=", "timestamp": "1786514819", "text": {"body": "hi"}, "type": "text"}]}	2026-08-12 06:07:00.326767	2026-08-12 06:07:00.345133
ec5bdd9c-1fd9-4736-ace3-983c1f375a1f	m_ws_broadcast_test_e8d37e57	instagram	t	\N	\N	{"sender": {"id": "23086741_5ec8"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_e8d37e57", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-13 13:10:22.423357	\N
e795d607-de1d-4ce0-966d-096525b67ca4	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQzMjYwNDA2NDc2MjMyOTMwMTc5MTEzMjM1MjUxMgZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786517581226, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQzMjYwNDA2NDc2MjMyOTMwMTc5MTEzMjM1MjUxMgZDZD", "attachments": [{"type": "image", "payload": {"url": "https://lookaside.fbsbx.com/ig_messaging_cdn/?asset_id=2320801635122995&signature=Ab06gGpYmHaLYXh9Z2RRPT34BkDdr0q1IDa5GEOFWlYKZbg-YVPXCXYPoOThBNM9qLCa1oqFH661G0AnF-WdbYhnHnRhaL7QbVwR_sdqCnt90a4dRpq8rigVYpFWTqpIW3MYTsHmfFh8BGuBM1ye4CTPzvLRtb6gcR_lp5vh6EQUs_LZfCU-DADpguW3j9rNfAYxpsHRxd68BVI1RNv8BhBSc-Z3F2s"}}]}}	2026-08-12 06:53:03.490463	\N
f0819ba8-1420-4fa3-b69a-9701b503ea0e	wamid.TEST_c1a6fe2c	whatsapp	t	\N	9	\N	2026-08-19 11:41:40.157122	2026-08-19 11:41:40.165363
8fd74c20-89ce-43a5-aee4-f6fa40f04a2b	m_auto_0a050639	instagram	t	\N	\N	{"sender": {"id": "auto_ai_30f4f9"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_0a050639", "text": "Do you ship internationally?"}}	2026-08-13 05:37:25.518687	\N
6beb1a06-7ff9-4828-a981-e43dd86bf50a	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjYyOTc4MDEzNzk5MDg0MTAwNzk5MTM4MzEzMDExMgZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786365639836, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjYyOTc4MDEzNzk5MDg0MTAwNzk5MTM4MzEzMDExMgZDZD", "text": "REAL INSTAGRAM WEBSOCKET E2E TEST 001"}}	2026-08-10 12:40:40.660552	\N
8a97ed22-918f-43e2-8acc-6ffbdb2e62b4	m_auto_af33ce6a	instagram	t	\N	\N	{"sender": {"id": "auto_ai_b096a6"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_af33ce6a", "text": "Do you ship internationally?"}}	2026-08-13 05:42:34.154493	\N
2ac826f7-854b-4a83-b483-30f6761ef1ac	m_LuuQ_MxOymyPbea2VTO1VaBR9GLU8WS3E1hs56gsQqdpBgzQpK1ZFM4zzaaHP3hN1pT2s556AhUBUsZ5ZtAhgw	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786617984974, "message": {"mid": "m_LuuQ_MxOymyPbea2VTO1VaBR9GLU8WS3E1hs56gsQqdpBgzQpK1ZFM4zzaaHP3hN1pT2s556AhUBUsZ5ZtAhgw", "attachments": [{"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t1.15752-9/770822884_1805902870776488_5657872292450003774_n.png?_nc_cat=110&ccb=1-7&_nc_sid=eb2e90&_nc_ohc=KYUZlk4ru-AQ7kNvwGJaHuQ&_nc_oc=AdoK9AlUaUqnHn01f2-NcUGiXQ6dlP8XXtAjnxNDcBcrkYpgB52z2-g9a-AmLV3pc1-8svULxPwUzKIOSr_PPC_9&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.xx&oh=03_Q7cD6AEWJhHFod_i5fjQ8NOVwzKamFkLFFmAGJpccBDWgLcX2A&oe=6AA52C7A"}}]}}	2026-08-13 10:46:26.171756	\N
cfe3dd62-e5f2-4cc3-8b13-80761deba174	m_auto_3906c4b5	instagram	t	\N	\N	{"sender": {"id": "auto_ai_b83d16"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_3906c4b5", "text": "Do you ship internationally?"}}	2026-08-13 13:08:12.324824	\N
9cf396f9-5e0d-4c79-a653-6b16f4ce7a60	m_test_e2e_final_1811_abc	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786366000000, "message": {"mid": "m_test_e2e_final_1811_abc", "text": "REAL E2E FINAL TEST 1811"}}	2026-08-10 12:47:28.33287	\N
8913c790-045a-46f9-828a-9698e8dafb99	m_exact_test_fe963acb	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_fe963acb", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-13 13:11:15.194012	\N
af343f1d-69a9-49f9-8a31-e5a7a3f4987f	m_live_e2e_1786366168	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786366168863, "message": {"mid": "m_live_e2e_1786366168", "text": "LIVE REALTIME DELIVERY TEST 6168"}}	2026-08-10 12:49:28.916925	\N
80b12860-62f5-4383-ad02-255b9be5560d	m_ws_broadcast_test_e059aaa4	instagram	t	\N	\N	{"sender": {"id": "23086741_7f4c"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_e059aaa4", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-13 13:08:49.377977	\N
44970bb5-d0f4-4c74-91ca-dff63666ace5	m_exact_test_7804c3b8	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_7804c3b8", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-13 13:18:16.294691	\N
e5a92f84-74d1-4dd4-b4db-9c8c1e663c19	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjY0MjI3MDE2MDM1MzUxMTYxMDMxNzA4MjE5ODAxNgZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786366316922, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjY0MjI3MDE2MDM1MzUxMTYxMDMxNzA4MjE5ODAxNgZDZD", "text": "FINAL REAL INSTAGRAM LIVE TEST 1811"}}	2026-08-10 12:51:57.663401	\N
2039fe61-df19-4cdc-b959-4039eec78ce5	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjY0MzU0MDc1NDAwNzQ5OTUzMTk5NzAzMTY5NDMzNgZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786366385801, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjY0MzU0MDc1NDAwNzQ5OTUzMTk5NzAzMTY5NDMzNgZDZD", "text": "PRODUCTION E2E INSTAGRAM TEST 2026-08-10-001"}}	2026-08-10 12:53:06.585683	\N
7cc1ac06-52e1-4aa3-b9fa-28b1363d3ac4	m_ws_live_verify_eab22911	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_live_verify_eab22911", "text": "LIVE VERIFICATION SOCKET TEST 2026"}}	2026-08-10 13:03:58.208663	\N
4eb36792-568b-4532-811b-4258e8ab6f94	wamid.TEST_5b398c19	whatsapp	t	\N	43	\N	2026-08-20 06:11:22.728195	2026-08-20 06:11:22.747056
e47ed183-85ff-411a-a9e7-30f9c5e0be6f	wamid.TEST_f096ce39	whatsapp	t	\N	11	\N	2026-08-19 11:35:40.009966	2026-08-19 11:35:40.020555
09b618e9-d44d-4b08-ab7e-489a70b20fef	m_exact_test_5fd98c80	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_5fd98c80", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-13 13:10:22.805124	\N
0591453d-ed1c-4522-9c7a-d7ca8c9c54a5	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjY1NzE4ODU3NjEzNDY5NDAxNzg2MzM2NTE2NTA1NgZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786367125651, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjY1NzE4ODU3NjEzNDY5NDAxNzg2MzM2NTE2NTA1NgZDZD", "text": "PRODUCTION E2E INSTAGRAM TEST 2026-08-10-01"}}	2026-08-10 13:05:26.456464	\N
86b60dd4-2d3e-4a59-8569-48af7736af13	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NDEzNDEzMjc0NTc3MTQ3NzQ1Nzk3MjQzNTYxNTc0NAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786447190955, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NDEzNDEzMjc0NTc3MTQ3NzQ1Nzk3MjQzNTYxNTc0NAZDZD", "text": "Hello SupportHub team, my Order #88213 is stuck in Processing status for 3 days. Could you please check?"}}	2026-08-11 11:19:51.709063	\N
5dc96755-1009-4f67-9f1e-84250ecfd9d6	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjY1NzY1MDgyNjM0MjkyODc3NDUzOTYxNDYxNzYwMAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786367150709, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1MjY1NzY1MDgyNjM0MjkyODc3NDUzOTYxNDYxNzYwMAZDZD", "text": "PRODUCTION E2E INSTAGRAM TEST 2026-08-10-01"}}	2026-08-10 13:05:51.526968	\N
8a896387-1afb-4359-a8c5-55b4eaad24eb	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDZBODMyQzc5QUZBMENFMTUyMgA=	whatsapp	t	\N	19	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDZBODMyQzc5QUZBMENFMTUyMgA=", "timestamp": "1786515243", "type": "image", "image": {"caption": "what i need to select for the query : forgot my password. Can you help me reset it?", "mime_type": "image/jpeg", "sha256": "MATtC7xPBOcJ3aeplVdQEmYXuK8UGltWZHsHLtQn0AQ=", "id": "1126597309692442", "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=1126597309692442&source=webhook&ext=1786515546&hash=ATyUUUJbU1tmxpcD5Frc4xcAL5djLG1Z2Rwy8jvoxQPL2w"}}]}	2026-08-12 06:14:08.468127	2026-08-12 06:14:08.483787
b0bb8ef9-2bbd-4bb4-9b10-39443ee66c80	mid_08aa86c9467c	facebook	t	\N	\N	{"sender": {"id": "test_fb_5373a66b"}, "recipient": {"id": "mock_page_id"}, "message": {"mid": "mid_08aa86c9467c", "text": "Hello SupportHub from Messenger!"}}	2026-08-13 13:10:53.867334	\N
df6c7c2d-d6c5-4c3e-9151-d99398d5724e	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQzOTI2NDY2MzAxOTA1OTQ1ODk1MzM4NDU1ODU5MgZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786517942298, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQzOTI2NDY2MzAxOTA1OTQ1ODk1MzM4NDU1ODU5MgZDZD", "text": "what i need to select for the query : forgot my password. Can you help me reset it?"}}	2026-08-12 06:59:03.227616	\N
500a64f7-71f8-42ba-9b98-e9bd1b37cfd1	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1MzI5OTU2MTM0NzY1ODozMjk1NDE0NDQwNDYxMzA2OTUwMTA2MjA4MDUzODYwNzYxNgZDZD	instagram	t	\N	\N	{"sender": {"id": "1038307988929264"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786447747794, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1MzI5OTU2MTM0NzY1ODozMjk1NDE0NDQwNDYxMzA2OTUwMTA2MjA4MDUzODYwNzYxNgZDZD", "text": "775847"}}	2026-08-11 11:29:08.536312	\N
4b4963a3-1072-49a2-9052-f791a3387363	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQzOTI2NjM0OTg4MTU3MTI3OTMyMzMzMjA4MzcxMgZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786517942389, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQzOTI2NjM0OTg4MTU3MTI3OTMyMzMzMjA4MzcxMgZDZD", "attachments": [{"type": "image", "payload": {"url": "https://lookaside.fbsbx.com/ig_messaging_cdn/?asset_id=1046255631642082&signature=Ab25wHhL-7q3a_Lxr5QbHmQkkRVhdQhCI2hxO6RzSluPnnPE2M_12z8VBGt8I5Ylak46N6Y6aBkuGEcqooaoKrzS8ciuPe3lsdMR6zrtmqUu-lGzYSX4CDeTdyvQ_FX3p7Y1tFvhcjdKQq1jAPFwanfxsjOkmDmWAhMOoejNU_07x4FV0JTD0fCnQ5j4OlnZpk6p__2Adejb96jBHbMDOItCJjlUq24"}}]}}	2026-08-12 06:59:04.355895	\N
c730fd22-fb50-444c-bd85-5941eb61c926	m_auto_15da5a62	instagram	t	\N	\N	{"sender": {"id": "auto_ai_87d3ca"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_15da5a62", "text": "Do you ship internationally?"}}	2026-08-13 05:37:45.133773	\N
1f9b52fa-0b24-4cfe-b0bb-6fb855c5898e	m_lwj5jUdebWPZzu0XVvICjaBR9GLU8WS3E1hs56gsQqfq7uDPG9U800tw6Lvst3rsT7lUs1GIsum0oOmmIgyjWA	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786616658118, "message": {"mid": "m_lwj5jUdebWPZzu0XVvICjaBR9GLU8WS3E1hs56gsQqfq7uDPG9U800tw6Lvst3rsT7lUs1GIsum0oOmmIgyjWA", "text": "what i need to select for the query : forgot my password. Can you help me reset it?"}}	2026-08-13 10:28:09.431146	\N
3b6a3e93-09f7-4fa9-9d5f-4871287aafdb	m_tsISdcOVudd5kN-_ldf8JKBR9GLU8WS3E1hs56gsQqfArr_FvBAtnTWAWrPdRXm-3Q4CGKP1RjojcJPxYey88A	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786616899081, "message": {"mid": "m_tsISdcOVudd5kN-_ldf8JKBR9GLU8WS3E1hs56gsQqfArr_FvBAtnTWAWrPdRXm-3Q4CGKP1RjojcJPxYey88A", "text": "what i need to select for the query : forgot my password. Can you help me reset it?"}}	2026-08-13 10:28:19.866935	\N
0ea505e9-8afd-4607-8fbe-4d44d3cf57fa	m_r1H1ZT3sAkS1glUwWWPe2aBR9GLU8WS3E1hs56gsQqeiELXn0L9ukjO4pxOUZESHQAKCS6UfL2404koQK19YuQ	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786618314603, "message": {"mid": "m_r1H1ZT3sAkS1glUwWWPe2aBR9GLU8WS3E1hs56gsQqeiELXn0L9ukjO4pxOUZESHQAKCS6UfL2404koQK19YuQ", "text": "what i need to select for the query : forgot my password. Can you help me reset it?"}}	2026-08-13 10:51:55.397725	\N
bcf01ef7-04e1-4779-930c-4cfd67fcd73b	m_ws_broadcast_test_f523f923	instagram	t	\N	\N	{"sender": {"id": "23086741_53c9"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f523f923", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-13 13:08:16.203416	\N
13659982-dcdc-43a4-a66b-4103210eb841	m_exact_test_586f5748	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_586f5748", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-13 13:08:49.77731	\N
1385a9a3-69e3-4178-9f49-ae09d35bc9f7	wamid.TEST_c497cf9c	whatsapp	t	\N	42	\N	2026-08-19 11:41:40.195895	2026-08-19 11:41:40.215264
d013004c-ce12-4d00-82c5-ba489c6bc734	wamid.TEST_0d1b096e	whatsapp	t	\N	136	\N	2026-08-26 10:09:11.189867	2026-08-26 10:09:11.267651
55a8bae0-9300-44a1-917a-d693f74e1031	m_ws_broadcast_test_4653abe7	instagram	t	\N	\N	{"sender": {"id": "23086741_5ea4"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_4653abe7", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-11 12:32:57.745746	\N
3cc9d747-ff63-4bb5-9508-e883bc27be42	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDEwOTc5MTExMjEyNjI1MTcxNDEwMjM1NDI0NzY4MAZDZD	instagram	t	\N	\N	{"sender": {"id": "26806233522386775"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786445871392, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDEwOTc5MTExMjEyNjI1MTcxNDEwMjM1NDI0NzY4MAZDZD", "text": "Hii"}}	2026-08-11 10:57:52.392943	\N
49559150-cb54-41e7-aa30-f846ccfbfcc5	wamid.TEST_44cbb3ed	whatsapp	t	\N	7	\N	2026-08-19 13:32:54.505735	2026-08-19 13:32:54.512539
a6d1b483-7ca3-456e-976b-037b0d15ad41	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDNEN0I4MTlEQzM1Mzc1QThFMwA=	whatsapp	t	\N	14	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDNEN0I4MTlEQzM1Mzc1QThFMwA=", "timestamp": "1786515692", "type": "video", "video": {"caption": "how can i change my profile info. like : name and all", "mime_type": "video/mp4", "sha256": "7mol+jn5RwJpZB9PmgI6tK3iUZWlq+Xrc1WJW2D5xJc=", "id": "1857684608974482", "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=1857684608974482&source=webhook&ext=1786515995&hash=ATzguQVeJPnZ9GJPJrurWX02-Lcqjw4T_vwl2v5DRzhg_Q"}}]}	2026-08-12 06:21:37.933549	2026-08-12 06:21:37.946837
b01daf6f-a2de-433c-8204-63ada3eb85fd	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTU1ODA4NDQ1NzkxNDU3NTAwMDA2MjYwNDA4MzIwMAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786524383532, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTU1ODA4NDQ1NzkxNDU3NTAwMDA2MjYwNDA4MzIwMAZDZD", "text": "what i need to select for the query : forgot my password. Can you help me reset it?"}}	2026-08-12 08:46:24.502007	\N
a42440a3-b1ff-401d-9931-387dde16b8c4	wamid.TEST_184a6e2b	whatsapp	t	\N	42	\N	2026-08-19 13:32:54.608612	2026-08-19 13:32:54.627992
a743b446-01ae-4d07-9f04-027f62269745	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTU1ODA4NTQxNDE1Njg5NDI5MzAxODM0MDc1MzQwOAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786524383583, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTU1ODA4NTQxNDE1Njg5NDI5MzAxODM0MDc1MzQwOAZDZD", "attachments": [{"type": "image", "payload": {"url": "https://lookaside.fbsbx.com/ig_messaging_cdn/?asset_id=1105462715137224&signature=Ab3ydGOfdjIQGhBEWOZ0nz_0hRpxhCs4zy0r9KNSs06sFpzDLX8HmWr5lkrJCDlKD8Xjos4uvRzAzGm5YGM7riDtyD2kvZtec7sp9hQRXQMiSWgXufGgR3Gz_IBBXfuPCmstYr_O1tDBf5cKNlUcD8naV3RLu7n3WmWWx1wkeg7uykn9Xl_yZpEvoGd0UKvtPWzHa9k83PHk-pZBHGO_KSR2N0qba7k"}}]}}	2026-08-12 08:46:25.871418	\N
57406bd6-cf13-45d0-adb0-57746dcdc7fa	m_ws_broadcast_test_9e877aba	instagram	t	\N	\N	{"sender": {"id": "23086741_94c5"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_9e877aba", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-13 13:10:56.259262	\N
2ca8d272-7453-4b0c-9fc2-3a2213ed153b	wamid.TEST_3918ac83	whatsapp	t	\N	43	\N	2026-08-19 13:22:16.723935	2026-08-19 13:22:16.743044
1b4445cb-fb22-4ec6-ae6f-06b9c12359bf	wamid.DEDUP_f0c2dbe5	whatsapp	t	\N	44	\N	2026-08-19 13:32:54.726661	2026-08-19 13:32:54.746506
da9a01df-9b73-4cb3-8416-7de70fe484b9	wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDQ5QkJDNjc2REY0RERDRjE1NAA=	whatsapp	t	\N	22	{"messaging_product": "whatsapp", "metadata": {"display_phone_number": "15552041051", "phone_number_id": "1296854793505632"}, "contacts": [{"profile": {"name": "\\ud83d\\udc51 Heet Sanghani \\ud83d\\udc51"}, "wa_id": "919824052103", "user_id": "IN.1404279701556294"}], "messages": [{"from": "919824052103", "from_user_id": "IN.1404279701556294", "id": "wamid.HBgMOTE5ODI0MDUyMTAzFQIAEhgWM0VCMDQ5QkJDNjc2REY0RERDRjE1NAA=", "timestamp": "1786436730", "text": {"body": "forgot my password. Can you help me reset it?"}, "type": "text"}]}	2026-08-11 08:25:32.653476	2026-08-11 08:25:32.672795
f0fdf897-dffa-4147-9183-798593620747	wamid.TEST_18e86470	whatsapp	t	\N	9	\N	2026-08-19 13:22:16.746209	2026-08-19 13:22:16.754566
10c95ee4-ac38-4a01-89bb-cb395e84e020	m_auto_ded6f292	instagram	t	\N	\N	{"sender": {"id": "auto_ai_82364d"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_ded6f292", "text": "Do you ship internationally?"}}	2026-08-13 05:39:28.709771	\N
9140908b-681d-4ee6-a302-91ddc6efaea5	m_ws_broadcast_test_da99f0bb	instagram	t	\N	\N	{"sender": {"id": "23086741_a8fc"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_da99f0bb", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-14 08:00:53.672417	\N
43493097-adb4-4bd8-98fb-53d54cad64be	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDA1MjM4ODExMDA2Njg0Mzc0OTc1OTMxNzk2Njg0OAZDZD	instagram	t	\N	\N	{"sender": {"id": "26806233522386775"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786442759569, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI4NTgzMTE4ODI5MTE3MTQ0MjozMjk1NDA1MjM4ODExMDA2Njg0Mzc0OTc1OTMxNzk2Njg0OAZDZD", "text": "Hi"}}	2026-08-11 10:06:01.520918	\N
9fbfcb97-0825-45b5-bce5-339bc7ca57ed	m_72gbFXf-1w1L7N2JZv1C76BR9GLU8WS3E1hs56gsQqdUpU65TsqAOpOHex9QnUWzjYnHEAhTn7gED1dLAvH_VQ	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786616658903, "message": {"mid": "m_72gbFXf-1w1L7N2JZv1C76BR9GLU8WS3E1hs56gsQqdUpU65TsqAOpOHex9QnUWzjYnHEAhTn7gED1dLAvH_VQ", "attachments": [{"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t1.15752-9/770822884_1805902870776488_5657872292450003774_n.png?_nc_cat=110&ccb=1-7&_nc_sid=eb2e90&_nc_ohc=KYUZlk4ru-AQ7kNvwEWH3Uv&_nc_oc=AdqpIceAoPNlJI8yLoiDr3l9DxNkRxySwEIyitogo2ibZiRenx701BWb9PwQR7LanRf-GbQVmwSb7qnjvNaYchdm&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.xx&oh=03_Q7cD6AEnTIn_2L73KW6hKMcJCh-t9GxQilQCA8Li2w82R8ZWVQ&oe=6AA4F43A"}}]}}	2026-08-13 10:28:10.56329	\N
e6fdfd58-6e94-4de2-a876-9b76ccaa5351	m_exact_test_eec10560	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_eec10560", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-13 13:08:16.591493	\N
5d2aaac1-ab31-43e0-b508-ca02c46fbad0	m_auto_ffe5261f	instagram	t	\N	\N	{"sender": {"id": "auto_ai_e5a909"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_ffe5261f", "text": "Do you ship internationally?"}}	2026-08-13 13:09:12.69233	\N
97217d45-6341-49b4-a384-d896c1216e4a	wamid.TEST_0015db7d	whatsapp	t	\N	47	\N	2026-08-19 13:22:58.896534	2026-08-19 13:22:58.918615
2859de2b-aec9-413a-ba5d-6edfc918df23	m_exact_test_77ccdd42	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_77ccdd42", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-14 06:31:43.543282	\N
d22a0926-ab04-45d4-bf2b-14de2d1248a2	wamid.TEST_cf38dbb2	whatsapp	t	\N	9	\N	2026-08-19 13:22:58.922462	2026-08-19 13:22:58.930755
42d3f290-c7d5-4091-851b-2114272e4390	wamid.TEST_c067c6a9	whatsapp	t	\N	136	\N	2026-08-26 12:30:36.94858	2026-08-26 12:30:37.011533
c054497d-a994-4c19-ae8f-f03cc19106b0	wamid.TEST_41b3ed58	whatsapp	t	\N	146	\N	2026-08-26 10:09:11.384865	2026-08-26 10:09:11.437439
398fbe2f-6d3e-4077-9ad9-39cfcac75a4e	m_exact_test_99061757	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_99061757", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-11 12:32:59.463128	\N
43d122cd-91e0-4724-8da4-1b41c76c24e5	wamid.TEST_5ce1fcd8	whatsapp	t	\N	43	\N	2026-08-19 11:41:40.245175	2026-08-19 11:41:40.26456
531bd738-b892-4b64-8eef-a5dfe0ca6fda	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQxOTc4Mzg4MDU2MzUzMjM0MTg3NjI2ODk5MDQ2NAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786516886242, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1NTQxOTc4Mzg4MDU2MzUzMjM0MTg3NjI2ODk5MDQ2NAZDZD", "text": "what i need to select for the query : forgot my password. Can you help me reset it?"}}	2026-08-12 06:41:27.237135	\N
83dde352-cd21-4f49-be6b-eff3d7f10329	m_ws_broadcast_test_9fdf7fda	instagram	t	\N	\N	{"sender": {"id": "23086741_4a27"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_9fdf7fda", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-13 05:36:56.713071	\N
266ddd25-dd44-4836-836e-425871356eed	m_ws_broadcast_test_3cb3dd4d	instagram	t	\N	\N	{"sender": {"id": "23086741_6c51"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_3cb3dd4d", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-14 07:09:12.370891	\N
f390d184-2a40-4be8-ad46-98861064138a	m_auto_d9e928ff	instagram	t	\N	\N	{"sender": {"id": "auto_ai_70d81d"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_d9e928ff", "text": "Do you ship internationally?"}}	2026-08-13 05:39:48.004145	\N
6877be8c-a1e6-47cb-8665-84dddaafbf4d	m_uwLkPIDgHfx3uqRT6xOnS6BR9GLU8WS3E1hs56gsQqfIiQXIPuE0STGv4vkg61adRNJgj4c47RgJaqVRkgV-RQ	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786616899899, "message": {"mid": "m_uwLkPIDgHfx3uqRT6xOnS6BR9GLU8WS3E1hs56gsQqfIiQXIPuE0STGv4vkg61adRNJgj4c47RgJaqVRkgV-RQ", "attachments": [{"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t1.15752-9/770822884_1805902870776488_5657872292450003774_n.png?_nc_cat=110&ccb=1-7&_nc_sid=eb2e90&_nc_ohc=KYUZlk4ru-AQ7kNvwGJaHuQ&_nc_oc=AdoK9AlUaUqnHn01f2-NcUGiXQ6dlP8XXtAjnxNDcBcrkYpgB52z2-g9a-AmLV3pc1-8svULxPwUzKIOSr_PPC_9&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.xx&oh=03_Q7cD6AESIbsrC0KymjkEcPlzFKMMF11O4NSh9WC18s89OitNeg&oe=6AA4F43A"}}]}}	2026-08-13 10:28:21.992751	\N
498a7591-1235-4c2c-a4ea-a2b16efb299a	wamid.TEST_0a6f84d2	whatsapp	t	\N	8	\N	2026-08-19 11:41:40.268479	2026-08-19 11:41:40.275931
089d9a2e-fc3c-4543-aca3-90ab0c26aec9	m_IwtgAi5aoS3Y1N1pNpcZVqBR9GLU8WS3E1hs56gsQqeJL7r3-0ICCcMKU3lvCOiJchRU4wvvGe_wMtBGjp0fpQ	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786618315368, "message": {"mid": "m_IwtgAi5aoS3Y1N1pNpcZVqBR9GLU8WS3E1hs56gsQqeJL7r3-0ICCcMKU3lvCOiJchRU4wvvGe_wMtBGjp0fpQ", "attachments": [{"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t1.15752-9/770822884_1805902870776488_5657872292450003774_n.png?_nc_cat=110&ccb=1-7&_nc_sid=eb2e90&_nc_ohc=KYUZlk4ru-AQ7kNvwGJaHuQ&_nc_oc=AdoK9AlUaUqnHn01f2-NcUGiXQ6dlP8XXtAjnxNDcBcrkYpgB52z2-g9a-AmLV3pc1-8svULxPwUzKIOSr_PPC_9&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.xx&oh=03_Q7cD6AEWJhHFod_i5fjQ8NOVwzKamFkLFFmAGJpccBDWgLcX2A&oe=6AA52C7A"}}]}}	2026-08-13 10:51:56.655319	\N
32ce31e8-bf72-4a09-ac6e-6b85b3206cb5	m_exact_test_68350de1	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_68350de1", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-13 13:10:56.663117	\N
cfc6941f-fa4d-4a10-93e8-2014deb85451	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTQ3MDQ5MTE1MjkwNjU0ODozMjk1NDE1MTExMTU2ODg2MTA4NTQyMjgxMDM1MDc0NzY0OAZDZD	instagram	t	\N	\N	{"sender": {"id": "3186178738258152"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786448111378, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTQ3MDQ5MTE1MjkwNjU0ODozMjk1NDE1MTExMTU2ODg2MTA4NTQyMjgxMDM1MDc0NzY0OAZDZD", "text": "Hii"}}	2026-08-11 11:35:12.700581	\N
349ac123-2dc1-4f3e-b1fa-dc2e79f8f479	m_auto_4ce8b29c	instagram	t	\N	\N	{"sender": {"id": "auto_ai_9c06be"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_4ce8b29c", "text": "Do you ship internationally?"}}	2026-08-13 13:08:47.112836	\N
36dc8492-82ab-4944-8acf-fb4f9fccd7fc	m_ws_broadcast_test_2ac2b600	instagram	t	\N	\N	{"sender": {"id": "23086741_ad2f"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_2ac2b600", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-19 11:41:44.847782	\N
73d0b21c-7fb9-4be1-8c75-1186256e7526	wamid.TEST_3d38597a	whatsapp	t	\N	55	\N	2026-08-19 13:22:16.789492	2026-08-19 13:22:16.816903
4fca1257-b0a5-4280-9243-31feea101538	m_exact_test_603be7ca	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_603be7ca", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-14 08:00:54.071198	\N
8a4ec680-e498-4028-98dc-d3582e80a3d1	m_auto_29188be8	instagram	t	\N	\N	{"sender": {"id": "auto_ai_e004f4"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_auto_29188be8", "text": "Do you ship internationally?"}}	2026-08-13 13:09:21.959985	\N
df035df4-4aa0-4ecf-a0a4-71c5051239c1	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1ODcyNzE0MTk3NTk2MzM0NzY2MzI1MDYxNjQ4Mzg0MAZDZD	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786696178484, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI2MDUxNTEyMDgyMDU1MzcyMzozMjk1ODcyNzE0MTk3NTk2MzM0NzY2MzI1MDYxNjQ4Mzg0MAZDZD", "text": "Hi"}}	2026-08-14 08:29:39.924505	\N
00f1759c-ae05-4d5a-9443-8f6fb1484cee	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5NzMwMDUxOTY5NzcyMzk1MTYwNTczNDE3ODgxNgZDZD	instagram	t	\N	\N	{"sender": {"id": "1755928588776159"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786943927275, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5NzMwMDUxOTY5NzcyMzk1MTYwNTczNDE3ODgxNgZDZD", "text": "Hyy"}}	2026-08-17 05:18:49.620619	\N
715afa73-45b7-420d-8d78-cb6741d28c61	wamid.TEST_b4f7d05a	whatsapp	t	\N	52	\N	2026-08-19 13:22:58.660771	2026-08-19 13:22:58.687563
ada7b63a-3e73-4803-8bf5-086f3896bf2f	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5OTQ3NTM2ODU3NzI0MDk1NDg0NzU0MTMyOTkyMAZDZD	instagram	t	\N	\N	{"sender": {"id": "1755928588776159"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786944045174, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5OTQ3NTM2ODU3NzI0MDk1NDg0NzU0MTMyOTkyMAZDZD", "text": "I have purchased a tshirt at 15 aug"}}	2026-08-17 05:20:47.513347	\N
7dfe813b-dea5-44c8-80dc-4e56c5de506d	wamid.DEDUP_6ce2919f	whatsapp	t	\N	44	\N	2026-08-19 13:22:58.961021	2026-08-19 13:22:58.981897
0493d997-cb7e-4b88-a916-67f0215c5c33	wamid.TEST_fc83d87f	whatsapp	t	\N	52	\N	2026-08-19 13:27:18.92119	2026-08-19 13:27:18.948346
ff653b42-007d-4fb2-aeef-94b09c076fd0	m_ws_broadcast_test_078260e3	instagram	t	\N	\N	{"sender": {"id": "23086741_5188"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_078260e3", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-14 06:31:43.19337	\N
9060a1ed-952c-40fd-842e-a6d413608ae7	m_exact_test_0aafe712	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_0aafe712", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-14 06:49:06.134596	\N
3b1af47b-2b16-4cbb-9f6b-3baa6ac1f35f	wamid.DEDUP_ea9685e4	whatsapp	t	\N	42	\N	2026-08-19 11:41:40.305368	2026-08-19 11:41:40.32438
d99e1a4b-370f-4735-a9c0-f3bf79425f18	m_exact_test_e465a41c	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_e465a41c", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-14 07:09:13.340022	\N
f954b0a4-8d95-4459-b2e1-85ef737195d7	m_exact_test_685880d6	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_685880d6", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-19 11:41:45.217572	\N
209ec955-8a49-49b8-99df-c847e38df6ab	wamid.TEST_9bf65004	whatsapp	t	\N	45	\N	2026-08-19 13:22:16.848464	2026-08-19 13:22:16.869156
5ffdcc06-fd70-4183-87b4-7e6d3a0debb3	wamid.TEST_b64f695f	whatsapp	t	\N	9	\N	2026-08-19 13:22:16.873682	2026-08-19 13:22:16.882078
884c9f7a-544a-4039-b2cd-7364e6ee7f95	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTYwMTg0Nzk2MzAxNjAzOTozMjk1ODcyNDYyMTQ3MTg2NDI1MDI4MTkxNDY2MTg2MzQyNAZDZD	instagram	t	\N	\N	{"sender": {"id": "1393311096269047"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786696041847, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTYwMTg0Nzk2MzAxNjAzOTozMjk1ODcyNDYyMTQ3MTg2NDI1MDI4MTkxNDY2MTg2MzQyNAZDZD", "text": "Hii"}}	2026-08-14 08:27:23.927308	\N
9db4dfae-21ec-4988-bdbe-b5dd86c06f76	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5NzgwMTI2NzExNzE0MjQwNzU0NjIxNDAyMzE2OAZDZD	instagram	t	\N	\N	{"sender": {"id": "1755928588776159"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786943954421, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5NzgwMTI2NzExNzE0MjQwNzU0NjIxNDAyMzE2OAZDZD", "text": "I want know about my status of order"}}	2026-08-17 05:19:15.349826	\N
3e6e8b09-5cef-4529-be2b-5c84f0649403	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5ODI4MzcyNTE2MTY2MDg0Njc1MTI2MjcwMzYxNgZDZD	instagram	t	\N	\N	{"sender": {"id": "1755928588776159"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786943980575, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5ODI4MzcyNTE2MTY2MDg0Njc1MTI2MjcwMzYxNgZDZD", "text": "kartiksangada01@gmail.com"}}	2026-08-17 05:19:41.348043	\N
987c024e-584b-4014-a25a-dff63a636590	m_real_test_f25df5d4	instagram	f	(sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "ix_tickets_ref"\nDETAIL:  Key (ref)=(TCK-25989) already exists.\n[SQL: INSERT INTO tickets (id, ref, customer_id, agent_id, subject, category, channel, status, priority, sla_due_at, sla_breached, sentiment, ai_confidence, ai_resolved, ai_summary, deleted_at, created_at, updated_at) VALUES ($1::UUID, $2::VARCHAR, $3::UUID, $4::UUID, $5::VARCHAR, 	\N	{"sender": {"id": "23086741_fa58"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_real_test_f25df5d4", "text": "INSTAGRAM E2E TEST 2026-NEW-001"}}	2026-08-19 13:22:19.119981	\N
c58d572b-006f-4899-b404-47fec239b2d8	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5ODcyNTY0MjUwMTU4MDU4OTI5NTM3MjA3NTAwOAZDZD	instagram	t	\N	\N	{"sender": {"id": "1755928588776159"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786944004531, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzI5ODcyNTY0MjUwMTU4MDU4OTI5NTM3MjA3NTAwOAZDZD", "text": "123456"}}	2026-08-17 05:20:05.390327	\N
ff8ba4ed-21fb-425a-8884-cbd6050edbed	m_ws_broadcast_test_228b370f	instagram	t	\N	\N	{"sender": {"id": "23086741_45ec"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_228b370f", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-19 13:22:21.367955	\N
ae224525-33f5-4e6a-a96a-e4165e29e574	wamid.TEST_6e47dc8c	whatsapp	t	\N	46	\N	2026-08-19 13:22:58.72231	2026-08-19 13:22:58.742949
9c3cd2a0-d88c-4866-b4a0-54414e0eb852	wamid.TEST_f12e202d	whatsapp	t	\N	8	\N	2026-08-19 13:22:58.746186	2026-08-19 13:22:58.753822
3d7b8236-e0e1-4b3e-9893-229ee2f44efa	wamid.TEST_f532b759	whatsapp	t	\N	48	\N	2026-08-19 13:27:18.983528	2026-08-19 13:27:19.005494
b0f450fe-d82b-444b-929b-651b4c084188	wamid.TEST_893a5a74	whatsapp	t	\N	11	\N	2026-08-19 13:27:19.00916	2026-08-19 13:27:19.019374
8df56ee7-4862-44de-889f-bb6f9b840430	wamid.TEST_597e766a	whatsapp	t	\N	45	\N	2026-08-19 13:27:19.130834	2026-08-19 13:27:19.151692
3167f02a-da59-481a-ad4f-9957007f0796	wamid.DEDUP_2f7b10f9	whatsapp	t	\N	47	\N	2026-08-19 13:27:19.269117	2026-08-19 13:27:19.290526
a070d9bb-245c-4ed2-8f84-d51d72f581c3	wamid.TEST_e294cf46	whatsapp	t	\N	8	\N	2026-08-19 11:35:40.023462	2026-08-19 11:35:40.031288
8ad5154b-c0be-4ff9-9d82-0b0b4d6492d0	wamid.TEST_b7c123ab	whatsapp	t	\N	8	\N	2026-08-19 11:35:40.035531	2026-08-19 11:35:40.043672
7b1c5961-cafd-43a4-b53d-d893f0af6b95	wamid.TEST_a64a2f10	whatsapp	t	\N	8	\N	2026-08-19 11:35:40.046683	2026-08-19 11:35:40.054429
a6371f74-4023-4ada-91bb-79ed3a0381c8	wamid.TEST_76b5f804	whatsapp	t	\N	7	\N	2026-08-19 11:35:40.057499	2026-08-19 11:35:40.064366
aeb9a047-ccc7-4ffa-a78c-f54a87b05b71	wamid.TEST_a68fd2b5	whatsapp	t	\N	10	\N	2026-08-19 11:35:40.06856	2026-08-19 11:35:40.077553
caef50b3-4066-4c84-a54a-09c2208422e7	wamid.DEDUP_96b54e8d	whatsapp	t	\N	8	\N	2026-08-19 11:35:40.082303	2026-08-19 11:35:40.089761
f46becc0-b77c-4bb1-b20f-8fcd1737f1d6	wamid.DEDUP2_ba939b06	whatsapp	t	\N	8	\N	2026-08-19 11:35:40.093919	2026-08-19 11:35:40.101551
558b1097-4e6f-4842-ac1a-134d6b81ef92	wamid.TEST_98ff1947	whatsapp	t	\N	10	\N	2026-08-19 11:35:40.106209	2026-08-19 11:35:40.115766
21f326b1-fd65-49a4-8c83-5dec78090f3c	wamid.TEST_d630e6a2	whatsapp	t	\N	8	\N	2026-08-19 11:35:40.119516	2026-08-19 11:35:40.127202
820f7968-0914-4703-9d70-a37a3642371a	wamid.TEST_cfb972c6	whatsapp	t	\N	7	\N	2026-08-19 11:35:40.130345	2026-08-19 11:35:40.136642
bca030f0-a07c-4c19-bbca-7b1f28c49a52	wamid.TEST_a03e8538	whatsapp	t	\N	8	\N	2026-08-19 11:35:40.139533	2026-08-19 11:35:40.147635
aec98974-1282-4c33-9a2a-d2befc6d3c5a	wamid.TEST_ae1217d0	whatsapp	t	\N	7	\N	2026-08-19 11:35:40.154141	2026-08-19 11:35:40.161125
dabf98e4-b6cb-4544-9540-19ef9455bd53	wamid.TEST_65726fd9	whatsapp	t	\N	12	\N	2026-08-19 11:35:40.165502	2026-08-19 11:35:40.17639
9d9df1ed-8de5-4d26-a21f-8626046af9e2	wamid.TEST_caa3e830	whatsapp	t	\N	8	\N	2026-08-19 11:35:40.181164	2026-08-19 11:35:40.189041
639e5adb-5d70-4b33-abf7-994065ec5df3	wamid.TEST_75b3772f	whatsapp	t	\N	47	\N	2026-08-19 11:39:32.439461	2026-08-19 11:39:32.462374
d6577ec2-9cc1-4dfc-bf39-06a7751a0d5e	wamid.TEST_19added5	whatsapp	t	\N	48	\N	2026-08-19 11:39:32.495179	2026-08-19 11:39:32.519894
a78bf062-0638-4ef0-baf1-fd194aaaee15	wamid.TEST_4f4506f4	whatsapp	t	\N	10	\N	2026-08-19 11:39:32.523801	2026-08-19 11:39:32.53326
eccfc1a9-4868-4a4e-b2b7-55d33c38e726	wamid.TEST_f088ae06	whatsapp	t	\N	69	\N	2026-08-19 11:39:32.576427	2026-08-19 11:39:32.610726
c8351793-fdb7-407f-a875-983adebce0d2	wamid.TEST_092c38f8	whatsapp	t	\N	11	\N	2026-08-19 11:39:32.615835	2026-08-19 11:39:32.625645
ed08e490-f51d-40f3-bc6c-6ca6931df682	wamid.TEST_f02dda7e	whatsapp	t	\N	57	\N	2026-08-19 11:39:32.668828	2026-08-19 11:39:32.694289
9d316ec0-1c26-48e2-98bf-20a6cb0cd98a	wamid.TEST_8a150ac7	whatsapp	t	\N	47	\N	2026-08-19 11:39:32.726772	2026-08-19 11:39:32.748717
5ca0f0b4-f4d5-43d9-a308-0188e3e01710	wamid.TEST_0890b6e1	whatsapp	t	\N	7	\N	2026-08-19 11:39:32.75236	2026-08-19 11:39:32.759393
87b5f610-d960-48f9-9cee-6b5ad5c859ed	wamid.DEDUP_2192beea	whatsapp	t	\N	46	\N	2026-08-19 11:39:32.790997	2026-08-19 11:39:32.811747
50219921-b0b7-4626-a6a3-e4b9175988f2	wamid.TEST_3c900a37	whatsapp	t	\N	44	\N	2026-08-20 05:35:29.308361	2026-08-20 05:35:29.329173
8501d63b-ce31-47aa-ac16-ea2aa3b206e4	m_exact_test_84bbc7f8	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_84bbc7f8", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 06:17:08.415513	\N
7f0c9914-cfc3-4079-affe-eef7119e39de	wamid.TEST_e241b391	whatsapp	t	\N	42	\N	2026-08-21 06:41:22.025943	2026-08-21 06:41:22.045126
f1c1e5da-2c84-4f3d-9f09-70288a1c6da7	wamid.TEST_ef1aadea	whatsapp	t	\N	52	\N	2026-08-21 04:35:27.714302	2026-08-21 04:35:27.739962
b7708326-4cc0-44a9-bd65-5f5ae0dcd35d	aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzMwMDA5OTUxNDI3MzY1NTM4MTk2ODcyNTk5OTYxNgZDZD	instagram	t	\N	\N	{"sender": {"id": "1755928588776159"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786944079009, "message": {"mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDM1NDc4OTkxODgzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1ODU4MDAxMDk5MjMwNTozMjk2MzMwMDA5OTUxNDI3MzY1NTM4MTk2ODcyNTk5OTYxNgZDZD", "text": "No thanks"}}	2026-08-17 05:21:19.858169	\N
b2fd74b4-4398-4a14-bfd2-4577e5d40db0	wamid.TEST_72ed7932	whatsapp	t	\N	45	\N	2026-08-19 13:32:54.543932	2026-08-19 13:32:54.565351
31309394-06e1-476c-b36d-8c1d1072fc45	m_ws_broadcast_test_af3b2ceb	instagram	t	\N	\N	{"sender": {"id": "23086741_5aee"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_af3b2ceb", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-17 06:22:07.608459	\N
fb14d588-fe06-4e6f-b676-e6219bfe3bdc	wamid.TEST_e10d63e4	whatsapp	t	\N	48	\N	2026-08-20 09:45:18.074131	2026-08-20 09:45:18.097812
d430e49d-1d40-4e9a-a034-776e1a71aad6	m_exact_test_51d8b8f3	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_51d8b8f3", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-17 06:22:07.950516	\N
3ae1189f-cd09-4af9-ab58-8d1a06caf524	wamid.TEST_ecd6f944	whatsapp	t	\N	9	\N	2026-08-19 13:32:54.569086	2026-08-19 13:32:54.577798
87d7226d-cbf9-44ed-bbd0-a0b544bc2202	m_ws_broadcast_test_10d01f68	instagram	t	\N	\N	{"sender": {"id": "23086741_82fc"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_10d01f68", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-17 06:29:21.778334	\N
2ccb592d-feb4-49d0-b572-4496bb973f3d	wamid.TEST_d78830d8	whatsapp	t	\N	10	\N	2026-08-20 05:35:29.333013	2026-08-20 05:35:29.3423
41164e6f-f15c-44b2-855d-d434f6e54d7e	m_exact_test_b309d9d6	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_b309d9d6", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-17 06:29:22.130406	\N
090aa73b-0757-40be-9fc2-00cf922e55b0	wamid.TEST_fe34dac9	whatsapp	t	\N	47	\N	2026-08-19 13:32:54.659602	2026-08-19 13:32:54.682185
26e54d45-1c89-40b6-9fe3-21d98d5bbafd	m_BPoVzp9-KLE5HvIyIJzJN6BR9GLU8WS3E1hs56gsQqczku7YUVDNR7dwfVEm4zOacAjvyc4qBeyvMRsSZvoEOA	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786951742795, "message": {"mid": "m_BPoVzp9-KLE5HvIyIJzJN6BR9GLU8WS3E1hs56gsQqczku7YUVDNR7dwfVEm4zOacAjvyc4qBeyvMRsSZvoEOA", "text": "what i need to select for the query : forgot my password. Can you help me reset it?"}}	2026-08-17 07:29:03.952671	\N
58d7b6fb-91aa-4d30-ac65-a378950a75bc	m_fxOg6VKRHTMCJROKyRuFyKBR9GLU8WS3E1hs56gsQqe7clfTXF2mJ0qW_qtpTGmqHGINECiTueaSJdKbDBxafw	facebook	t	\N	\N	{"sender": {"id": "38499898592930667"}, "recipient": {"id": "1281820968343824"}, "timestamp": 1786951744002, "message": {"mid": "m_fxOg6VKRHTMCJROKyRuFyKBR9GLU8WS3E1hs56gsQqe7clfTXF2mJ0qW_qtpTGmqHGINECiTueaSJdKbDBxafw", "attachments": [{"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t1.15752-9/770822884_1805902870776488_5657872292450003774_n.png?_nc_cat=110&ccb=1-7&_nc_sid=eb2e90&_nc_ohc=gkPrWo8otxoQ7kNvwF5ni4q&_nc_oc=AdrOph2RQIYyH3aGopH8UcM0cwXLaBJW6sbmW6arVI3W53iXtTZs5LCW8ngMDUwM2Z1rqiZ0_ZnZITZYWLi0Zw1d&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.xx&oh=03_Q7cD6AEqphlNuV_wHBotZjpT5O6SposyboJei4LmpcbPjnA_7g&oe=6AAA3A3A"}}]}}	2026-08-17 07:29:05.479309	\N
fd7e7e9c-c4e0-4b3b-95c3-faf0ff5f8da9	wamid.TEST_cdf960f0	whatsapp	t	\N	44	\N	2026-08-19 13:22:16.598159	2026-08-19 13:22:16.619002
9f54da74-1e45-4a00-916e-5f0a1b5500f3	m_ws_broadcast_test_7c61773e	instagram	t	\N	\N	{"sender": {"id": "23086741_fb65"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_7c61773e", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-19 11:31:29.053143	\N
762585ca-da67-479c-a110-d76b8a3032e1	wamid.TEST_c1b65a45	whatsapp	t	\N	9	\N	2026-08-19 13:32:54.68686	2026-08-19 13:32:54.695137
c5b81857-12e3-4b81-a48b-36a4ad55e6f5	m_exact_test_04bf59d5	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_04bf59d5", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-19 11:31:29.403209	\N
d8c01db5-9575-400a-b0ac-5a5287d8e7c6	wamid.DEDUP_78022835	whatsapp	t	\N	46	\N	2026-08-19 13:22:16.911539	2026-08-19 13:22:16.934282
f218b54d-495e-4b38-b2d5-e21fd21da929	m_ws_broadcast_test_223b819b	instagram	t	\N	\N	{"sender": {"id": "23086741_6296"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_223b819b", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-19 11:39:37.250607	\N
2d3d70df-7767-4373-b6d5-c5f9776db0ba	m_exact_test_fbfd0b52	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_fbfd0b52", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-19 11:39:37.630923	\N
cf0b3e6b-d377-4324-b37a-5a0a44466ded	m_exact_test_67fe1dec	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_67fe1dec", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-19 13:22:21.735287	\N
a7a6ab58-df00-4490-84ee-8433d7970998	wamid.TEST_11c67adf	whatsapp	t	\N	44	\N	2026-08-19 13:22:58.785159	2026-08-19 13:22:58.805721
6f07c5d5-e36b-465d-9952-a60e9670ef8e	wamid.TEST_36b25b75	whatsapp	t	\N	8	\N	2026-08-19 13:22:58.809129	2026-08-19 13:22:58.817224
2ff4f492-fabb-4e7a-b777-551db9abd5e2	m_ws_broadcast_test_a71f86f6	instagram	t	\N	\N	{"sender": {"id": "23086741_e54a"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a71f86f6", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-19 13:32:59.142577	\N
1ae96649-ff9c-4037-ad50-8761a191698d	m_exact_test_d02025db	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_d02025db", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-19 13:32:59.516363	\N
646e1be6-46ac-4611-856c-b1016538d44f	m_ws_broadcast_test_d639add7	instagram	t	\N	\N	{"sender": {"id": "23086741_c288"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_d639add7", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-19 13:23:03.328461	\N
18c0c462-2a8c-480c-8c03-7e0e724ad8a1	m_exact_test_7cb04cfd	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_7cb04cfd", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-19 13:23:03.702345	\N
0cd25139-a38e-45c3-9fd4-0dc4e035ed1b	wamid.TEST_9b430bce	whatsapp	t	\N	54	\N	2026-08-19 13:27:19.055098	2026-08-19 13:27:19.08188
e2911440-e1ea-4bc6-83f6-821b9f1fdd4d	wamid.TEST_1107d55a	whatsapp	t	\N	11	\N	2026-08-19 13:27:19.087419	2026-08-19 13:27:19.097654
aed47f25-3f47-45a4-9966-d318d309bf69	wamid.TEST_6abfacd6	whatsapp	t	\N	65	\N	2026-08-19 13:27:19.18617	2026-08-19 13:27:19.222746
9f9fc531-b9f3-4459-bf8a-06308bd1fd8c	wamid.TEST_f0fa60c9	whatsapp	t	\N	10	\N	2026-08-19 13:27:19.228964	2026-08-19 13:27:19.23753
4e399c2f-6201-42d4-b1db-d86b663b0b85	m_ws_broadcast_test_6698ff62	instagram	t	\N	\N	{"sender": {"id": "23086741_d3cd"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_6698ff62", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-19 13:27:23.674226	\N
e5216d73-4983-425d-bbb7-8021c59e8343	m_exact_test_ad46f350	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_ad46f350", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-19 13:27:24.058568	\N
ef4b9141-2fa8-43b6-9e49-c0dd5ac8b36c	wamid.TEST_496b36fa	whatsapp	t	\N	9	\N	2026-08-20 06:11:22.75044	2026-08-20 06:11:22.758945
9ceec41d-7786-4241-ba56-5d54b66ddf05	wamid.TEST_79ae7946	whatsapp	t	\N	55	\N	2026-08-19 13:34:54.313102	2026-08-19 13:34:54.340657
3e392ed2-415b-4fcf-9e45-cee4c99772a7	wamid.TEST_124a78a4	whatsapp	t	\N	44	\N	2026-08-20 05:35:29.376459	2026-08-20 05:35:29.397078
6b9f36c5-069c-41a8-9038-e99e34a22a2f	wamid.TEST_90922717	whatsapp	t	\N	46	\N	2026-08-19 13:34:54.37466	2026-08-19 13:34:54.396444
545e26c1-5655-46e9-b394-8c5ef9f981e4	wamid.TEST_dfffd5ca	whatsapp	t	\N	7	\N	2026-08-19 13:34:54.40035	2026-08-19 13:34:54.407241
bac5fc92-6c03-4666-8f5b-fd9e788552f8	wamid.TEST_35a1b0f2	whatsapp	t	\N	9	\N	2026-08-20 05:35:29.400592	2026-08-20 05:35:29.409162
a1e3e459-b115-4129-8f68-2ca7dc0a1397	wamid.TEST_2356085d	whatsapp	t	\N	55	\N	2026-08-19 13:34:54.446345	2026-08-19 13:34:54.469583
dd66d10d-a4b2-4577-90da-1651c2369822	wamid.TEST_1d48a83d	whatsapp	t	\N	10	\N	2026-08-19 13:34:54.473126	2026-08-19 13:34:54.482991
a7271363-b466-4b93-a7c9-b05b97019e7f	wamid.TEST_d5c63016	whatsapp	t	\N	44	\N	2026-08-20 05:35:29.441397	2026-08-20 05:35:29.461635
93a139cb-d511-461d-8709-3968326e2390	wamid.TEST_2e4ec8a2	whatsapp	t	\N	44	\N	2026-08-19 13:34:54.51493	2026-08-19 13:34:54.534993
da194e78-7d30-43ff-8dbf-2cf4c21f537a	wamid.TEST_b71936e4	whatsapp	t	\N	47	\N	2026-08-19 13:34:54.564906	2026-08-19 13:34:54.588168
1db7066e-4136-433a-b424-cfcc9ebe803b	wamid.TEST_645cb557	whatsapp	t	\N	47	\N	2026-08-20 05:35:29.491796	2026-08-20 05:35:29.515182
ce2b8da9-afd8-4da6-9cea-de8e70860aa2	wamid.TEST_4ba0f1c6	whatsapp	t	\N	8	\N	2026-08-19 13:34:54.591591	2026-08-19 13:34:54.598694
90901040-caa4-4a2f-8324-46c414e1ce81	wamid.DEDUP_ca9677e6	whatsapp	t	\N	46	\N	2026-08-19 13:34:54.628311	2026-08-19 13:34:54.651387
0a6a33b3-da20-4d43-b0a9-a0ed0e008e1c	wamid.TEST_97227f33	whatsapp	t	\N	8	\N	2026-08-20 05:35:29.519166	2026-08-20 05:35:29.526801
205f855b-44cb-42ed-9185-61ad576278b1	wamid.DEDUP_6ee35b68	whatsapp	t	\N	44	\N	2026-08-20 05:35:29.557078	2026-08-20 05:35:29.577102
62c9b4eb-346a-4905-8519-37e9bee80489	m_unmatched_test_58b12b6c	instagram	t	\N	\N	{"sender": {"id": "123456"}, "recipient": {"id": "99999999999999999"}, "message": {"mid": "m_unmatched_test_58b12b6c", "text": "Unmatched account text"}}	2026-08-20 05:35:30.92237	\N
5bbd1bd0-77ad-4e57-a34d-8d9c6390e91f	m_ws_broadcast_test_780fa223	instagram	t	\N	\N	{"sender": {"id": "23086741_a260"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_780fa223", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-19 13:35:00.188358	\N
7ef3622e-2c70-413e-a0a9-c1f03843ac13	m_exact_test_40abd693	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_40abd693", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-19 13:35:00.561015	\N
06c58c6c-8977-4466-b144-c631be30eae5	wamid.TEST_3bb1d9f2	whatsapp	t	\N	51	\N	2026-08-20 04:36:05.746226	2026-08-20 04:36:05.771406
0acecf90-584c-4760-bc97-7d95abf183f1	wamid.TEST_62f6ea11	whatsapp	t	\N	44	\N	2026-08-20 04:36:05.804207	2026-08-20 04:36:05.825601
a1e46025-4a3f-4a46-94c0-cfddfc4ce3e5	wamid.TEST_06d517f5	whatsapp	t	\N	7	\N	2026-08-20 04:36:05.82911	2026-08-20 04:36:05.835922
f61cdfa3-0a71-406b-b5ac-7eea239cee64	wamid.TEST_caf5391e	whatsapp	t	\N	45	\N	2026-08-20 04:36:05.868051	2026-08-20 04:36:05.888631
23197211-3ab3-421e-8558-35c1009d43f0	m_ws_broadcast_test_386db347	instagram	t	\N	\N	{"sender": {"id": "23086741_69c9"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_386db347", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 05:35:32.650597	\N
605e92d6-350d-46ac-810a-65ea33b4d1d0	wamid.TEST_60955c7e	whatsapp	t	\N	10	\N	2026-08-20 04:36:05.892729	2026-08-20 04:36:05.901954
b1d50221-fedd-4f4f-8a0c-19c3d06d8907	wamid.TEST_d04e9065	whatsapp	t	\N	51	\N	2026-08-20 04:36:05.935761	2026-08-20 04:36:05.961295
427b0bb8-dfb8-42da-9ae8-9129674dab06	wamid.TEST_3ed77244	whatsapp	t	\N	49	\N	2026-08-20 05:35:47.378027	2026-08-20 05:35:47.403027
4cd818fd-b0c4-40f8-9682-545e4abdb688	wamid.TEST_81d818df	whatsapp	t	\N	47	\N	2026-08-20 04:36:05.992628	2026-08-20 04:36:06.015299
712606e3-d0d7-4f5c-a79a-bb8c8a322207	wamid.TEST_4b61ccb2	whatsapp	t	\N	8	\N	2026-08-20 04:36:06.019445	2026-08-20 04:36:06.027002
bf23fd21-ec59-4844-8f78-b6dca0bc337c	wamid.TEST_0309ec10	whatsapp	t	\N	44	\N	2026-08-20 05:35:47.435991	2026-08-20 05:35:47.456578
762ffa36-8b0f-44d3-aacc-f848d096ff02	wamid.DEDUP_4afbc384	whatsapp	t	\N	43	\N	2026-08-20 04:36:06.056528	2026-08-20 04:36:06.076419
d1f1c4c0-ce40-450f-a622-e8bcacfae242	wamid.TEST_aa929e97	whatsapp	t	\N	8	\N	2026-08-20 05:35:47.459866	2026-08-20 05:35:47.46706
432c2bfc-5ab4-42bc-bbd1-66f50bdc7f31	wamid.TEST_a7a0165e	whatsapp	t	\N	51	\N	2026-08-20 05:35:47.502469	2026-08-20 05:35:47.527036
c5de4595-b352-448e-9c17-7d9cd9a85970	m_ws_broadcast_test_5d75c37b	instagram	t	\N	\N	{"sender": {"id": "23086741_3e12"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_5d75c37b", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 04:36:12.012588	\N
ee81a8ad-3c0f-4de7-8d25-6c8c77627b58	m_exact_test_71ab6e7c	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_71ab6e7c", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 04:36:12.357238	\N
5762f287-1efa-4295-bf3a-5874cc4dfd17	wamid.TEST_4f8134f4	whatsapp	t	\N	49	\N	2026-08-20 04:43:09.244085	2026-08-20 04:43:09.269825
0ae94ce0-060b-4a5c-9e1b-0a06d4fe446f	wamid.TEST_9837351f	whatsapp	t	\N	43	\N	2026-08-20 04:43:09.3015	2026-08-20 04:43:09.321307
fc6b32a1-18b7-4a9b-9025-8afb36fa29e3	wamid.TEST_1c01932e	whatsapp	t	\N	8	\N	2026-08-20 04:43:09.324772	2026-08-20 04:43:09.331983
3e775fb4-9bab-4498-8bf0-d1fed5a0e87c	wamid.TEST_ded8c8d0	whatsapp	t	\N	43	\N	2026-08-20 04:43:09.364136	2026-08-20 04:43:09.383484
8da4101d-00de-480e-b579-5acbf7a1149c	wamid.TEST_fd5ad1ee	whatsapp	t	\N	9	\N	2026-08-20 04:43:09.386887	2026-08-20 04:43:09.395
b7de2393-a175-40c4-8871-c02a1c4d7b16	wamid.TEST_61b5d2f6	whatsapp	t	\N	43	\N	2026-08-20 04:43:09.427222	2026-08-20 04:43:09.445795
8ea5271f-ed43-4236-9120-2f59765ed1b5	wamid.TEST_f3c4a20d	whatsapp	t	\N	44	\N	2026-08-20 04:43:09.475751	2026-08-20 04:43:09.49551
468414bd-c007-4690-bca6-1d5b476201fb	wamid.TEST_ac820890	whatsapp	t	\N	7	\N	2026-08-20 04:43:09.499001	2026-08-20 04:43:09.505688
c78c7018-6bdd-4be3-9cdd-2e7d93c318ce	wamid.DEDUP_7005786c	whatsapp	t	\N	50	\N	2026-08-20 04:43:09.534753	2026-08-20 04:43:09.562148
f7e28770-2aaa-408b-9b6a-982e24224f61	m_ws_broadcast_test_98cbfe63	instagram	t	\N	\N	{"sender": {"id": "23086741_547f"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_98cbfe63", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 04:43:15.220164	\N
3313e194-ad76-43de-918e-f82529772a6a	m_exact_test_241b9f5f	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_241b9f5f", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 04:43:15.581507	\N
23f966b9-99d7-4b94-b175-bb74e35c2322	wamid.TEST_312b75a2	whatsapp	t	\N	49	\N	2026-08-20 05:04:47.595325	2026-08-20 05:04:47.620529
af495cf5-dac2-4118-aceb-67ae2a949454	wamid.TEST_9f02d907	whatsapp	t	\N	44	\N	2026-08-20 05:04:47.652403	2026-08-20 05:04:47.672841
ae9d57ed-9230-46fa-ab6e-e3a6ce0d3a9c	wamid.TEST_664b00d1	whatsapp	t	\N	8	\N	2026-08-20 05:04:47.677486	2026-08-20 05:04:47.684968
0aba8227-64e7-4ce4-893e-352a56a488d6	wamid.TEST_95cd9d3d	whatsapp	t	\N	43	\N	2026-08-20 05:04:47.715618	2026-08-20 05:04:47.735414
c4188868-4761-452c-98ca-9a519a0e506a	wamid.TEST_beea87e6	whatsapp	t	\N	8	\N	2026-08-20 05:04:47.738943	2026-08-20 05:04:47.746774
47fc529f-4433-45b6-8b3c-1558d4e05bb3	wamid.TEST_55ad12ea	whatsapp	t	\N	41	\N	2026-08-20 05:04:47.777231	2026-08-20 05:04:47.795976
33cc71d6-6cc3-4730-9fd4-6db5485660cd	wamid.TEST_9f916359	whatsapp	t	\N	44	\N	2026-08-20 05:04:47.825798	2026-08-20 05:04:47.846246
d38a2a05-28a3-464c-8257-21755839e0aa	wamid.TEST_f265afcf	whatsapp	t	\N	8	\N	2026-08-20 05:04:47.8501	2026-08-20 05:04:47.857529
1d75e2ca-d044-4922-bd06-ff228a0132dd	wamid.DEDUP_9feeb1d7	whatsapp	t	\N	44	\N	2026-08-20 05:04:47.888198	2026-08-20 05:04:47.907903
445b6775-7367-4dd4-83cb-fe762f32f5a2	m_ws_broadcast_test_e3267e9b	instagram	t	\N	\N	{"sender": {"id": "23086741_b897"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_e3267e9b", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 05:04:54.157647	\N
7550c9f7-c0d2-426a-90f8-b5018f65cd92	m_exact_test_766a87c8	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_766a87c8", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 05:04:54.525384	\N
71fbc74c-8c8d-4879-a867-71676f414191	wamid.TEST_676c4477	whatsapp	t	\N	55	\N	2026-08-20 13:34:20.78236	2026-08-20 13:34:20.811733
cd3ffdd1-fc01-41f6-8f7f-bcd94302712f	m_exact_test_e8f377f9	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_e8f377f9", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 05:35:32.722265	\N
7d4a1e9a-d2bf-4e27-8a50-2a913f241102	wamid.TEST_0e069b97	whatsapp	t	\N	58	\N	2026-08-20 09:45:18.13446	2026-08-20 09:45:18.166129
a177305c-db7b-4375-a6f6-a8b06d943fdb	wamid.TEST_757c72d4	whatsapp	t	\N	49	\N	2026-08-21 06:16:10.851763	2026-08-21 06:16:10.876625
59514437-125c-467b-bff0-90dcc2cd9c3f	wamid.TEST_1c144fda	whatsapp	t	\N	44	\N	2026-08-21 04:35:27.955619	2026-08-21 04:35:27.975784
06f7e1cf-48fc-4dde-ab2c-1186ee6a4977	m_exact_test_c944e574	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_c944e574", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 05:38:48.009594	\N
9a216e48-8e5a-463f-984d-b0c7d1094d54	wamid.TEST_ed2a2d49	whatsapp	t	\N	10	\N	2026-08-20 09:45:18.170504	2026-08-20 09:45:18.17966
2d4caf29-9d02-4a51-90d8-de2a69f40cfe	wamid.TEST_2f454407	whatsapp	t	\N	43	\N	2026-08-20 06:11:22.790922	2026-08-20 06:11:22.810178
f35bb43f-1813-4d6d-9d4c-dc0c0493a110	wamid.DEDUP_977c07b8	whatsapp	t	\N	49	\N	2026-08-20 13:34:21.141849	2026-08-20 13:34:21.165868
95e5a851-5ca2-4de8-b1d7-b7a53a19107c	wamid.TEST_787f33fa	whatsapp	t	\N	9	\N	2026-08-20 06:11:22.813628	2026-08-20 06:11:22.82217
8b3e74da-fb4f-48f1-b339-8161a313d974	m_unmatched_test_7e5b45d3	instagram	t	\N	\N	{"sender": {"id": "123456"}, "recipient": {"id": "99999999999999999"}, "message": {"mid": "m_unmatched_test_7e5b45d3", "text": "Unmatched account text"}}	2026-08-20 05:35:37.887523	\N
555fe176-d280-43df-9334-8dee51b9c3ea	wamid.TEST_fbab06d9	whatsapp	t	\N	44	\N	2026-08-20 09:45:18.277301	2026-08-20 09:45:18.298566
a6af18ed-dec7-40dd-9744-39b4d3579b3c	wamid.TEST_d3961f2a	whatsapp	t	\N	43	\N	2026-08-20 06:11:22.901764	2026-08-20 06:11:22.922132
a8afd414-a8a7-46b2-895b-556ea107a634	wamid.TEST_7caf4782	whatsapp	t	\N	7	\N	2026-08-20 06:11:22.925845	2026-08-20 06:11:22.932538
dffdc97e-c0b5-49f2-94ce-884e61f7c780	wamid.DEDUP_56e4b8ef	whatsapp	t	\N	42	\N	2026-08-20 09:45:18.390024	2026-08-20 09:45:18.409357
0046033a-2b8b-45a3-ab54-2fc6ac96acfa	m_exact_test_a3e7fbdd	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_a3e7fbdd", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 09:45:24.699854	\N
d73382b2-2e27-45fe-aee7-83f74ac0b0c4	m_ws_broadcast_test_4e6f806b	instagram	t	\N	\N	{"sender": {"id": "23086741_497a"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_4e6f806b", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 06:11:26.408605	\N
d0e212bf-7f0c-48a6-a4af-a243ca82475f	wamid.TEST_c7e34c89	whatsapp	t	\N	46	\N	2026-08-20 06:22:41.581815	2026-08-20 06:22:41.604297
ef466204-479d-41b0-b5ba-9e1fd1c06915	wamid.TEST_8c99accc	whatsapp	t	\N	44	\N	2026-08-20 10:05:49.362243	2026-08-20 10:05:49.382896
d96757a4-d617-443c-8108-e74d3cbba13e	wamid.TEST_e9e7cc19	whatsapp	t	\N	47	\N	2026-08-20 06:22:41.718683	2026-08-20 06:22:41.739525
f94551b2-d94d-4d45-8f8c-3f5f10c3d82b	wamid.TEST_35377e6e	whatsapp	t	\N	8	\N	2026-08-20 06:22:41.743088	2026-08-20 06:22:41.750631
ead8f5d3-7710-4122-ac2a-0d4d225c5d72	wamid.TEST_be882835	whatsapp	t	\N	8	\N	2026-08-20 10:05:49.387006	2026-08-20 10:05:49.394885
9961f25c-59e8-4bf2-a902-40d108416488	wamid.TEST_40f62d65	whatsapp	t	\N	64	\N	2026-08-20 06:22:41.847021	2026-08-20 06:22:41.88354
43091108-764f-4b64-9ac6-dc697b939282	wamid.TEST_c282bd86	whatsapp	t	\N	14	\N	2026-08-20 06:22:41.889749	2026-08-20 06:22:41.902044
9a671bab-21d3-4c01-91d5-770f6300c2b6	wamid.TEST_52ad3a67	whatsapp	t	\N	44	\N	2026-08-20 10:05:49.490829	2026-08-20 10:05:49.511932
74757f03-58e2-4086-9b5c-072784737df3	wamid.DEDUP_56738259	whatsapp	t	\N	50	\N	2026-08-20 10:05:49.603451	2026-08-20 10:05:49.628217
f7fb2c8e-5db4-4b61-8089-dbf86a5e1e0b	m_exact_test_02df4485	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_02df4485", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 10:06:22.97884	\N
f73551bb-cbf9-4ecf-a5a1-1712d17f5438	wamid.TEST_eb187a12	whatsapp	t	\N	42	\N	2026-08-20 10:23:36.77988	2026-08-20 10:23:36.799158
e908a6dc-7c93-46a2-90aa-ec196ce7bb45	m_ws_broadcast_test_2cea50fc	instagram	t	\N	\N	{"sender": {"id": "23086741_33b5"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_2cea50fc", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 06:22:50.014596	\N
691347a5-340d-4937-b97c-094794250b50	wamid.TEST_77effb9b	whatsapp	t	\N	7	\N	2026-08-20 10:23:36.802461	2026-08-20 10:23:36.809554
8a56dce2-23df-4b29-881a-339cf4608ac1	m_exact_test_f73395ad	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_f73395ad", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 06:22:50.099578	\N
17e5e55b-a233-4512-afc9-b38329a47f16	wamid.TEST_e442cc04	whatsapp	t	\N	42	\N	2026-08-20 06:35:43.430485	2026-08-20 06:35:43.449318
51bc5220-f7e0-400e-8b85-627b76c06ed3	wamid.TEST_e9ad9dc8	whatsapp	t	\N	42	\N	2026-08-20 10:23:36.901668	2026-08-20 10:23:36.920928
619c1516-a9ef-4a9e-b7fb-81316a8598c8	wamid.TEST_0e65d5c5	whatsapp	t	\N	8	\N	2026-08-20 06:35:43.452947	2026-08-20 06:35:43.460163
664c19b6-4718-4034-82ea-b7411a09bc0e	wamid.TEST_4ded9024	whatsapp	t	\N	43	\N	2026-08-20 06:35:43.554996	2026-08-20 06:35:43.573858
d4f4e50b-76c4-424b-b51f-05288d4c9835	wamid.DEDUP_57af828d	whatsapp	t	\N	47	\N	2026-08-20 10:23:37.020512	2026-08-20 10:23:37.042011
6ab685ae-864e-4896-9ba6-5bcc29452b9d	wamid.TEST_47121227	whatsapp	t	\N	46	\N	2026-08-20 06:35:43.607044	2026-08-20 06:35:43.626259
06de3281-d8ef-4357-9376-52ab0088d6bd	wamid.TEST_0da1afed	whatsapp	t	\N	9	\N	2026-08-20 06:35:43.629852	2026-08-20 06:35:43.638822
fef5bf27-6547-4305-87d5-5f6b66bd0d14	wamid.DEDUP_e09adb15	whatsapp	t	\N	43	\N	2026-08-20 06:35:43.668044	2026-08-20 06:35:43.68859
e68274f5-7c4d-495a-a3a9-6abd38749f6b	m_exact_test_c0349f1a	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_c0349f1a", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 10:23:58.41836	\N
2fd32c67-b625-443f-88d9-e5c4a0be5df2	wamid.TEST_3862e71b	whatsapp	t	\N	45	\N	2026-08-20 11:15:17.121002	2026-08-20 11:15:17.143596
6580b0aa-c09b-40ec-8c92-be5505881b89	wamid.TEST_a2814ae3	whatsapp	t	\N	10	\N	2026-08-20 11:15:17.14813	2026-08-20 11:15:17.157741
64a300f7-38c4-4fc9-8d5f-2175711b6961	wamid.TEST_47248a1e	whatsapp	t	\N	44	\N	2026-08-20 11:15:17.262305	2026-08-20 11:15:17.283054
93fd722a-8fa6-4537-bbc7-37ff6aa0adfa	wamid.DEDUP_583b0bc3	whatsapp	t	\N	42	\N	2026-08-20 11:15:17.376447	2026-08-20 11:15:17.395431
bf8ff2a2-3ae1-4f6e-9af9-899b1faf010c	m_ws_broadcast_test_437037af	instagram	t	\N	\N	{"sender": {"id": "23086741_ee5b"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_437037af", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 06:35:48.68363	\N
9093b833-dd06-4efa-b123-aec84ac73c79	m_exact_test_0f703ea3	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_0f703ea3", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 06:35:48.761132	\N
c39c3733-0a8e-4480-9a82-9b97384e9407	wamid.TEST_3ce3ca69	whatsapp	t	\N	51	\N	2026-08-20 08:03:27.067412	2026-08-20 08:03:27.09278
be83b6a0-8137-46b3-bea8-db5c74da3111	wamid.TEST_f8774678	whatsapp	t	\N	80	\N	2026-08-20 08:03:27.130491	2026-08-20 08:03:27.183525
96b0fdff-15e9-4a6d-8e50-3add3f597d99	wamid.TEST_a54a5d03	whatsapp	t	\N	12	\N	2026-08-20 08:03:27.189367	2026-08-20 08:03:27.199702
3ce4ddd6-3b45-4627-8ecb-5dd81e2eaa58	wamid.TEST_59605cfa	whatsapp	t	\N	49	\N	2026-08-20 08:03:27.235972	2026-08-20 08:03:27.258929
b79d52f8-8dcd-475a-aeaf-f90b5a461649	wamid.TEST_8aba5f8b	whatsapp	t	\N	10	\N	2026-08-20 08:03:27.26242	2026-08-20 08:03:27.272363
7ef975ec-e238-450a-8ce7-92419d445099	m_exact_test_ac674371	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_ac674371", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 11:15:29.332262	\N
df059aca-6a1d-425d-ae30-8e4c7bbdab09	wamid.TEST_b90bf670	whatsapp	t	\N	47	\N	2026-08-20 08:03:27.305194	2026-08-20 08:03:27.327534
73a00e7b-c981-41b6-a146-ec7c73ef7c7d	wamid.TEST_4f21a617	whatsapp	t	\N	48	\N	2026-08-20 08:03:27.359544	2026-08-20 08:03:27.382969
a84a45fe-9747-46ed-acd9-fe98c5cf6083	wamid.TEST_79c7ed75	whatsapp	t	\N	8	\N	2026-08-20 08:03:27.387261	2026-08-20 08:03:27.394487
71447f69-6718-4b67-a0de-aeba53210c05	wamid.DEDUP_a4e82815	whatsapp	t	\N	96	\N	2026-08-20 08:03:27.444813	2026-08-20 08:03:27.500361
7251639d-141e-414a-8d9c-b444a33563a5	wamid.TEST_afa05421	whatsapp	t	\N	54	\N	2026-08-20 12:14:57.836681	2026-08-20 12:14:57.864403
a2c4855e-ecd0-41af-9445-b11c247fb607	wamid.TEST_9d74569f	whatsapp	t	\N	10	\N	2026-08-20 05:35:47.530895	2026-08-20 05:35:47.540272
f7d8d8f4-42ee-405e-bac8-571f8c6233c2	m_ws_broadcast_test_50c812d6	instagram	t	\N	\N	{"sender": {"id": "23086741_239b"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_50c812d6", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 05:38:47.943011	\N
bf3e0e5b-b06a-4759-a682-4fdcffd4a60c	wamid.TEST_2b975104	whatsapp	t	\N	46	\N	2026-08-20 05:35:47.573522	2026-08-20 05:35:47.596019
ab0f3977-099f-462a-952d-e0b617d66e37	wamid.TEST_3059a236	whatsapp	t	\N	48	\N	2026-08-20 05:35:47.627961	2026-08-20 05:35:47.651788
5b71759b-db88-4729-b9ed-458051306554	wamid.TEST_8698298b	whatsapp	t	\N	56	\N	2026-08-20 06:11:22.667022	2026-08-20 06:11:22.694919
40cfef85-1a55-44f8-a808-29b943c75f34	wamid.TEST_672d36ab	whatsapp	t	\N	9	\N	2026-08-20 05:35:47.655973	2026-08-20 05:35:47.663764
4a107e3f-8f47-4907-a5bd-83fdfc4ba552	wamid.DEDUP_fe36ffae	whatsapp	t	\N	48	\N	2026-08-20 05:35:47.694987	2026-08-20 05:35:47.718803
ba4fb286-7d4f-479c-a9ce-762f5e7a911a	wamid.TEST_aa8bba02	whatsapp	t	\N	42	\N	2026-08-20 06:11:22.853184	2026-08-20 06:11:22.872341
0e384663-e6e8-4182-9cf8-99ab8e6b335f	wamid.DEDUP_635c24dc	whatsapp	t	\N	43	\N	2026-08-20 06:11:22.96168	2026-08-20 06:11:22.982066
d647c6b7-2e76-4f88-8c31-3d5ea6436a06	m_unmatched_test_bd31a9c9	instagram	t	\N	\N	{"sender": {"id": "123456"}, "recipient": {"id": "99999999999999999"}, "message": {"mid": "m_unmatched_test_bd31a9c9", "text": "Unmatched account text"}}	2026-08-20 05:35:49.078068	\N
7312acc3-bae0-428f-b6d4-502a47c635c3	m_exact_test_57a6e3b4	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_57a6e3b4", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 06:11:26.471385	\N
37b0c0a4-13b0-4494-b1dc-2b6566abc5da	wamid.TEST_c27bc57f	whatsapp	t	\N	56	\N	2026-08-20 06:22:41.642792	2026-08-20 06:22:41.668951
b9587e60-979c-48e4-81ae-53b9b2089c6c	wamid.TEST_d5eb16b7	whatsapp	t	\N	10	\N	2026-08-20 06:22:41.673663	2026-08-20 06:22:41.682976
3afba04f-2cd0-4eef-8994-1cb9949c1e6d	m_ws_broadcast_test_fdfd890f	instagram	t	\N	\N	{"sender": {"id": "23086741_db1f"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_fdfd890f", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 05:35:50.67136	\N
572887f5-f1d8-484d-bebd-c896f1fe9c5b	wamid.TEST_132be9e7	whatsapp	t	\N	53	\N	2026-08-20 06:22:41.782648	2026-08-20 06:22:41.812092
1d188a04-1b9a-48c3-9983-5e00f505ca1e	m_exact_test_cec6c034	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_cec6c034", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 05:35:50.736494	\N
4a892dd3-7af0-449f-917f-c733c441aa14	wamid.TEST_0bf0c975	whatsapp	t	\N	47	\N	2026-08-20 05:36:29.749243	2026-08-20 05:36:29.772488
90387112-7271-4c0f-a1ed-6e668d1a5687	wamid.DEDUP_9b44dafe	whatsapp	t	\N	64	\N	2026-08-20 06:22:41.948292	2026-08-20 06:22:41.975119
a3eaba1c-2e93-4cdb-955f-696c8820cf4b	wamid.TEST_e33b3de6	whatsapp	t	\N	45	\N	2026-08-20 05:36:29.806373	2026-08-20 05:36:29.826615
a6c77059-e1da-43bc-b369-3c8fca5e35d9	wamid.TEST_62fb27df	whatsapp	t	\N	9	\N	2026-08-20 05:36:29.830399	2026-08-20 05:36:29.838328
8c09fd45-b899-4ccf-9597-c33475438a93	wamid.TEST_988095f1	whatsapp	t	\N	44	\N	2026-08-20 05:36:29.869609	2026-08-20 05:36:29.890195
a7d8868c-7950-4eb6-85fa-1e4c48e35721	wamid.TEST_53e72acb	whatsapp	t	\N	54	\N	2026-08-20 06:35:43.373684	2026-08-20 06:35:43.397681
320957c1-6012-4736-96a7-32d61ec7d274	wamid.TEST_a054b1de	whatsapp	t	\N	9	\N	2026-08-20 05:36:29.893616	2026-08-20 05:36:29.902581
86ba4104-f4c7-4e30-996d-2464565e5cba	wamid.TEST_70c5c507	whatsapp	t	\N	44	\N	2026-08-20 05:36:29.935068	2026-08-20 05:36:29.954786
7da600a7-9dea-4a17-a999-45c44b0c8ee6	wamid.TEST_72c7b733	whatsapp	t	\N	44	\N	2026-08-20 06:35:43.491774	2026-08-20 06:35:43.511828
056ba78c-76d1-4755-b260-9338870c837c	wamid.TEST_5f942edd	whatsapp	t	\N	51	\N	2026-08-20 05:36:29.987803	2026-08-20 05:36:30.012102
c34b052a-0db0-44de-a037-ae441567c38e	wamid.TEST_0b3ce854	whatsapp	t	\N	8	\N	2026-08-20 05:36:30.01594	2026-08-20 05:36:30.023889
2a4d3396-e7f4-4c6f-a712-475d2e64045a	wamid.TEST_17b9b5fd	whatsapp	t	\N	8	\N	2026-08-20 06:35:43.515292	2026-08-20 06:35:43.523348
18fa64d2-c275-4cba-8057-223f555bcac2	wamid.DEDUP_6bf8d89a	whatsapp	t	\N	43	\N	2026-08-20 05:36:30.054362	2026-08-20 05:36:30.074477
4813285b-4112-4ec7-9855-a5a24c5cb0ac	m_unmatched_test_bc248103	instagram	t	\N	\N	{"sender": {"id": "123456"}, "recipient": {"id": "99999999999999999"}, "message": {"mid": "m_unmatched_test_bc248103", "text": "Unmatched account text"}}	2026-08-20 05:36:31.454713	\N
62a2de2c-44b8-486d-830c-8009229abde8	m_ws_broadcast_test_1cc3f26b	instagram	t	\N	\N	{"sender": {"id": "23086741_9fd0"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_1cc3f26b", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 05:36:33.369267	\N
0a50b90b-0126-4179-817a-2beb3cc205c5	m_exact_test_2b520d20	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_2b520d20", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 05:36:33.436861	\N
b710c421-8751-4147-8d9a-ca7890de2f87	wamid.TEST_61aa8704	whatsapp	t	\N	47	\N	2026-08-20 05:38:22.344065	2026-08-20 05:38:22.367821
162d0312-5c9f-47ab-bb69-35c1b3c6f80b	wamid.TEST_77b6851e	whatsapp	t	\N	51	\N	2026-08-20 05:38:22.405204	2026-08-20 05:38:22.429438
78a2f51e-fefa-46a9-855a-a8ecb3bbb882	wamid.TEST_03b3b4c6	whatsapp	t	\N	9	\N	2026-08-20 05:38:22.434039	2026-08-20 05:38:22.442098
b567c259-50e6-4253-8614-997a4fe39ef2	wamid.TEST_b69b9ae1	whatsapp	t	\N	46	\N	2026-08-20 05:38:22.475536	2026-08-20 05:38:22.497505
35ce1c13-a043-4d50-8c87-5e789e2095e6	wamid.TEST_1d48b3b3	whatsapp	t	\N	9	\N	2026-08-20 05:38:22.501429	2026-08-20 05:38:22.509682
efb9efcc-7fba-494e-a22d-8ff30a8fcdb9	wamid.TEST_8f901f5c	whatsapp	t	\N	42	\N	2026-08-20 05:38:22.540306	2026-08-20 05:38:22.559706
b3dc2540-73ad-4a7a-8e22-f997b5997429	wamid.TEST_9cdfb8c8	whatsapp	t	\N	60	\N	2026-08-20 05:38:22.601894	2026-08-20 05:38:22.627516
17b33443-8dce-4adf-87a2-f29829075184	wamid.TEST_c25a9961	whatsapp	t	\N	9	\N	2026-08-20 05:38:22.631075	2026-08-20 05:38:22.639455
783c66ae-48c9-4f9d-9e70-f0fad4b7b365	wamid.DEDUP_dd27b468	whatsapp	t	\N	43	\N	2026-08-20 05:38:22.669955	2026-08-20 05:38:22.689526
30a9ba4b-85f7-44b3-abf6-5bce38049ab3	m_unmatched_test_c4284eed	instagram	t	\N	\N	{"sender": {"id": "123456"}, "recipient": {"id": "99999999999999999"}, "message": {"mid": "m_unmatched_test_c4284eed", "text": "Unmatched account text"}}	2026-08-20 05:38:24.024592	\N
526a517c-8694-4c6b-b436-8721407f388a	m_ws_broadcast_test_8c82cab4	instagram	t	\N	\N	{"sender": {"id": "23086741_f47c"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_8c82cab4", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 05:38:25.904439	\N
b3c79fe1-bcc2-4aec-ac5e-cdb83f066af8	m_exact_test_777f9cea	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_777f9cea", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 05:38:25.977129	\N
11fbed16-4732-4268-91a7-53369244b1ff	m_unmatched_test_16583632	instagram	t	\N	\N	{"sender": {"id": "123456"}, "recipient": {"id": "99999999999999999"}, "message": {"mid": "m_unmatched_test_16583632", "text": "Unmatched account text"}}	2026-08-20 05:38:30.567046	\N
5ec1666b-9c87-4a06-8ca3-e6e44ba85afd	wamid.TEST_c08ef0c9	whatsapp	t	\N	52	\N	2026-08-20 05:38:44.501627	2026-08-20 05:38:44.52982
9dacbce3-8843-4643-87cd-1b52b3c46255	wamid.TEST_6bc40ca3	whatsapp	t	\N	48	\N	2026-08-20 05:38:44.564965	2026-08-20 05:38:44.587655
d1c8addb-19bf-4135-9877-14b737044136	wamid.TEST_322d60d7	whatsapp	t	\N	9	\N	2026-08-20 05:38:44.592125	2026-08-20 05:38:44.600075
1c7524d0-09bd-41e6-86e9-eb3ce9012ec9	wamid.TEST_4856d9f8	whatsapp	t	\N	43	\N	2026-08-20 05:38:44.631645	2026-08-20 05:38:44.651348
75399270-8d3f-4209-be1d-aa2c7bb2a2ff	wamid.TEST_cf8e7caf	whatsapp	t	\N	8	\N	2026-08-20 05:38:44.655425	2026-08-20 05:38:44.663139
f25b88e5-f5ba-4c0b-ae7d-9164e79f686d	wamid.TEST_9bfed9a0	whatsapp	t	\N	47	\N	2026-08-20 05:38:44.694756	2026-08-20 05:38:44.718643
4b3ed835-1696-4c11-9809-fbf726651aac	wamid.TEST_213c3344	whatsapp	t	\N	45	\N	2026-08-20 05:38:44.74988	2026-08-20 05:38:44.770722
417db334-0c13-4c50-aca6-82788d9dc83f	wamid.TEST_bf098603	whatsapp	t	\N	8	\N	2026-08-20 05:38:44.774507	2026-08-20 05:38:44.781582
4fe87d9e-97c1-434b-97dc-8daf1a921715	wamid.DEDUP_3ddf2199	whatsapp	t	\N	43	\N	2026-08-20 05:38:44.811982	2026-08-20 05:38:44.831838
3f0aff40-8839-42da-ab11-40f9f0c7e90c	wamid.TEST_b6c09cc5	whatsapp	t	\N	45	\N	2026-08-20 09:45:18.215073	2026-08-20 09:45:18.234332
9cc7ac45-f1be-4fe1-b70e-1f9dc6d8ab3c	wamid.TEST_15b0464a	whatsapp	t	\N	46	\N	2026-08-21 13:22:23.97571	2026-08-21 13:22:23.998245
77cc2762-c777-49c9-9fac-d8a436469a38	wamid.TEST_df713577	whatsapp	t	\N	9	\N	2026-08-20 09:45:18.238029	2026-08-20 09:45:18.246335
6b674588-8714-4f4c-8cf5-54536472350e	wamid.TEST_bb905571	whatsapp	t	\N	44	\N	2026-08-20 09:45:18.329062	2026-08-20 09:45:18.349645
360a0123-eaa6-44a4-ba12-3348145c55ef	wamid.TEST_68419026	whatsapp	t	\N	8	\N	2026-08-20 09:45:18.353293	2026-08-20 09:45:18.360484
c50975bf-24c1-4d72-b49e-0a93ac02f960	m_ws_broadcast_test_a48bc487	instagram	t	\N	\N	{"sender": {"id": "23086741_5a17"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a48bc487", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 08:03:32.389991	\N
d78eaf88-b581-460b-a2ab-e38b20a3b4f8	m_exact_test_328e5622	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_328e5622", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 08:03:32.45947	\N
a366f750-2527-46cb-adc3-7f31c4fc8eba	wamid.TEST_9e34dc96	whatsapp	t	\N	51	\N	2026-08-20 08:15:15.763111	2026-08-20 08:15:15.788707
e74ac101-6e9a-4447-9f2e-3e9853f42641	wamid.TEST_3d78e223	whatsapp	t	\N	49	\N	2026-08-20 08:15:15.826861	2026-08-20 08:15:15.848235
05e20668-c9fc-4759-8f0d-8155acd41ad9	wamid.TEST_bfb24a73	whatsapp	t	\N	7	\N	2026-08-20 08:15:15.851729	2026-08-20 08:15:15.858415
9e746b57-1738-4072-af82-27251e7a2805	wamid.TEST_144a61e5	whatsapp	t	\N	42	\N	2026-08-20 08:15:15.888927	2026-08-20 08:15:15.908155
cf2a6b7c-9af5-4cb2-87a0-4655d4a8f11a	wamid.TEST_1c6bbf60	whatsapp	t	\N	8	\N	2026-08-20 08:15:15.91137	2026-08-20 08:15:15.919286
1660604e-86f7-4b7b-8415-765df818d06a	wamid.TEST_23234b1a	whatsapp	t	\N	44	\N	2026-08-20 08:15:15.950011	2026-08-20 08:15:15.970206
2bfc8fd8-1f82-4076-a4bb-e6322f826cad	wamid.TEST_2755591f	whatsapp	t	\N	44	\N	2026-08-20 08:15:15.999712	2026-08-20 08:15:16.020094
3abb0e18-77ef-4ee2-9255-20187c2b3dde	wamid.TEST_10bf8b58	whatsapp	t	\N	7	\N	2026-08-20 08:15:16.023791	2026-08-20 08:15:16.030239
fab5597f-1be1-4620-9553-2377d69fb8e8	m_ws_broadcast_test_10d2b773	instagram	t	\N	\N	{"sender": {"id": "23086741_bc36"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_10d2b773", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 09:45:24.632031	\N
b2b5c851-9a70-4a7a-b310-0182a391cf87	wamid.DEDUP_1656b0d9	whatsapp	t	\N	41	\N	2026-08-20 08:15:16.058905	2026-08-20 08:15:16.077627
6d90a1a0-4b6e-451d-9f9a-90f70bb1e43a	wamid.TEST_27c61668	whatsapp	t	\N	52	\N	2026-08-20 10:05:49.303462	2026-08-20 10:05:49.329862
ab787e32-be11-474c-bf0b-1362d4486ac3	wamid.TEST_a7e79512	whatsapp	t	\N	44	\N	2026-08-20 10:05:49.428343	2026-08-20 10:05:49.448889
241427d0-a169-4e9d-a691-a979dfc63275	wamid.TEST_c689c35f	whatsapp	t	\N	8	\N	2026-08-20 10:05:49.452362	2026-08-20 10:05:49.459906
a0d21b68-5362-4596-b4fa-59e657bccec5	wamid.TEST_51c686e6	whatsapp	t	\N	42	\N	2026-08-20 10:05:49.541934	2026-08-20 10:05:49.560784
1458a44c-451b-45e2-9004-cad7116fc5f2	wamid.TEST_fdff7c60	whatsapp	t	\N	8	\N	2026-08-20 10:05:49.564775	2026-08-20 10:05:49.572149
211b1218-c6f0-4608-af7f-baa98aa23f9d	m_ws_broadcast_test_2713fde3	instagram	t	\N	\N	{"sender": {"id": "23086741_016c"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_2713fde3", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 08:15:21.033341	\N
748b5136-70dc-4650-b27f-bbcdb0f12360	m_exact_test_d0b40d09	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_d0b40d09", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 08:15:21.095563	\N
6399dcf8-7c87-4931-a2a1-c7dddfc91f9d	wamid.TEST_e4898087	whatsapp	t	\N	49	\N	2026-08-20 08:49:44.1759	2026-08-20 08:49:44.198895
2d460d4d-a0a7-4093-959e-0504e3a76de4	wamid.TEST_ef51576b	whatsapp	t	\N	42	\N	2026-08-20 08:49:44.230845	2026-08-20 08:49:44.250357
54863a26-c5e8-4bc4-a4b8-22cde7beb18b	wamid.TEST_f7738f89	whatsapp	t	\N	8	\N	2026-08-20 08:49:44.253872	2026-08-20 08:49:44.260942
7452737b-eecd-4c82-b4dc-01dbef180ac7	m_ws_broadcast_test_60d4c006	instagram	t	\N	\N	{"sender": {"id": "23086741_53e0"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_60d4c006", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 10:06:17.235284	\N
41abf87c-b34b-47a2-b6df-8482543e4935	wamid.TEST_cf71c2bf	whatsapp	t	\N	43	\N	2026-08-20 08:49:44.291663	2026-08-20 08:49:44.311768
7944b03b-36bf-4448-9b19-5ae0b7477b45	wamid.TEST_116fb5cc	whatsapp	t	\N	8	\N	2026-08-20 08:49:44.315001	2026-08-20 08:49:44.323052
c1441025-4743-4e81-bbe8-bc6ba91daac3	wamid.TEST_0f2f5738	whatsapp	t	\N	46	\N	2026-08-20 10:23:36.726078	2026-08-20 10:23:36.748403
a8d960c7-8858-4c6a-9724-3610508acf6a	wamid.TEST_569a084c	whatsapp	t	\N	46	\N	2026-08-20 08:49:44.353916	2026-08-20 08:49:44.376275
f5274c38-8842-4b7a-877d-b90cf43ba47f	wamid.TEST_927c6e9e	whatsapp	t	\N	48	\N	2026-08-20 08:49:44.40886	2026-08-20 08:49:44.431882
a86f971c-9bd2-4749-a5a1-5c835b9c332f	wamid.TEST_770354f0	whatsapp	t	\N	43	\N	2026-08-20 10:23:36.839809	2026-08-20 10:23:36.859748
a808196e-5f8c-4e2f-b171-6d64318d0441	wamid.TEST_3d7c4b7f	whatsapp	t	\N	8	\N	2026-08-20 08:49:44.435722	2026-08-20 08:49:44.443514
c3c0c154-d101-4173-8b1f-3aa3ecb89964	wamid.DEDUP_8af46797	whatsapp	t	\N	42	\N	2026-08-20 08:49:44.472663	2026-08-20 08:49:44.491845
ed4c87ff-76b2-4fce-a994-c2d661969d1e	wamid.TEST_e6457c96	whatsapp	t	\N	8	\N	2026-08-20 10:23:36.863387	2026-08-20 10:23:36.871334
a21b67da-68e0-4efd-a9c8-0e06a208b11d	wamid.TEST_1c7dd274	whatsapp	t	\N	47	\N	2026-08-20 10:23:36.950666	2026-08-20 10:23:36.974075
1eb8e2d1-8d68-47ba-9b09-d8b112645253	wamid.TEST_75ddeec2	whatsapp	t	\N	11	\N	2026-08-20 10:23:36.97829	2026-08-20 10:23:36.987973
37dfb40a-b165-4478-b95d-eb504742ff9b	m_ws_broadcast_test_12a6eecd	instagram	t	\N	\N	{"sender": {"id": "23086741_dc57"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_12a6eecd", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 10:23:58.068455	\N
d839c603-507d-4d53-9ac7-c63e2a398595	m_ws_broadcast_test_f5d8a0f2	instagram	t	\N	\N	{"sender": {"id": "23086741_add8"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f5d8a0f2", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 08:49:50.747205	\N
44cb0be3-c3fb-44b7-9cd8-fdf67a603186	m_exact_test_9d881106	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_9d881106", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 08:49:50.809683	\N
3b80a0ad-08ae-46eb-ae1b-3eb668e6be70	wamid.TEST_44cf5e7e	whatsapp	t	\N	46	\N	2026-08-20 11:15:17.066533	2026-08-20 11:15:17.089276
aa33d357-080c-4f75-b2c3-ddc1b3720c1f	wamid.TEST_af1ae843	whatsapp	t	\N	51	\N	2026-08-20 11:15:17.192949	2026-08-20 11:15:17.218405
259d9d87-ac9d-4e8d-bc9d-f448cd4afa35	wamid.TEST_fdf952a2	whatsapp	t	\N	9	\N	2026-08-20 11:15:17.222051	2026-08-20 11:15:17.230951
fe866eba-0e43-48d9-a28c-504e928a5c62	wamid.TEST_24849883	whatsapp	t	\N	46	\N	2026-08-20 11:15:17.31381	2026-08-20 11:15:17.335763
8c7aad88-e84f-4b1b-b3d1-0f3ee192ba49	wamid.TEST_9bbc72f1	whatsapp	t	\N	8	\N	2026-08-20 11:15:17.339659	2026-08-20 11:15:17.346748
5547a874-d63a-425c-a90e-e21dcc4b4f24	m_ws_broadcast_test_f4323a5a	instagram	t	\N	\N	{"sender": {"id": "23086741_2df3"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f4323a5a", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 11:15:28.991705	\N
6e72d6dc-0df6-4a8f-ab50-ac4dba7ab04f	wamid.TEST_e7e17d18	whatsapp	t	\N	59	\N	2026-08-20 11:17:15.855477	2026-08-20 11:17:15.880605
51a78a44-fa7a-42a9-9ffc-f8c96120bc2e	wamid.TEST_6616d326	whatsapp	t	\N	51	\N	2026-08-20 11:17:15.912639	2026-08-20 11:17:15.939955
c2fb0512-6f9d-4878-b889-acb9a6104944	wamid.TEST_bc23d850	whatsapp	t	\N	9	\N	2026-08-20 11:17:15.944161	2026-08-20 11:17:15.95237
c41a6e40-0cc4-40eb-a799-d1477a938087	wamid.TEST_c00bd417	whatsapp	t	\N	44	\N	2026-08-20 11:17:15.98513	2026-08-20 11:17:16.004473
fccc8f68-c579-4a96-b86e-380efccc29c1	wamid.TEST_c3c17fc7	whatsapp	t	\N	10	\N	2026-08-20 11:17:16.008776	2026-08-20 11:17:16.018543
df3bd7c4-b8b0-45bd-aa09-352b5c97f237	wamid.TEST_4a97aa13	whatsapp	t	\N	50	\N	2026-08-20 11:17:16.058337	2026-08-20 11:17:16.077773
eb2c242c-0c0a-4d10-bdbd-210ffe4db1c7	wamid.TEST_74c7d964	whatsapp	t	\N	44	\N	2026-08-20 11:17:16.108429	2026-08-20 11:17:16.129426
5aa2710c-984a-470f-b4d8-5f1abe179bc9	wamid.TEST_d6bf0bf4	whatsapp	t	\N	8	\N	2026-08-20 11:17:16.133339	2026-08-20 11:17:16.140948
1f35362a-c47a-4b6c-8f26-3ea5ec6cccbd	wamid.DEDUP_5fb5917c	whatsapp	t	\N	51	\N	2026-08-20 11:17:16.176694	2026-08-20 11:17:16.199456
265d98ee-b762-484d-b501-48fd02d50ed6	wamid.TEST_9fd387e9	whatsapp	t	\N	50	\N	2026-08-20 12:13:01.665965	2026-08-20 12:13:01.690515
31637712-0d38-4681-9c31-76b95f3d6627	m_ws_broadcast_test_3d14f052	instagram	t	\N	\N	{"sender": {"id": "23086741_d77b"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_3d14f052", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 12:13:12.725259	\N
748284be-4ca1-416e-95c8-f9925cf5864c	wamid.TEST_d12719bf	whatsapp	t	\N	47	\N	2026-08-20 12:14:57.898212	2026-08-20 12:14:57.922071
33609a13-97a9-4031-b30a-37a61647e5b2	wamid.TEST_359739ae	whatsapp	t	\N	55	\N	2026-08-20 13:34:20.851201	2026-08-20 13:34:20.878709
c577ebd6-78d9-418d-a68e-fdd4fdc7c855	wamid.TEST_f3ba18bd	whatsapp	t	\N	8	\N	2026-08-20 12:14:57.926395	2026-08-20 12:14:57.933378
6ddf40d5-3917-4b35-aba0-fc4c952e26b1	wamid.TEST_baa71342	whatsapp	t	\N	46	\N	2026-08-21 06:16:10.909412	2026-08-21 06:16:10.931704
8a198dd4-c6c0-46ba-8db4-f327c0b429bf	wamid.TEST_079d75fe	whatsapp	t	\N	47	\N	2026-08-20 12:14:58.036878	2026-08-20 12:14:58.059247
679539bd-5abd-4a8f-b52d-d21be22e4f5c	wamid.TEST_a9540ff7	whatsapp	t	\N	10	\N	2026-08-20 13:34:20.884164	2026-08-20 13:34:20.892874
768a42c3-244b-4830-804b-652f27192851	wamid.DEDUP_760d36ba	whatsapp	t	\N	50	\N	2026-08-20 12:14:58.160361	2026-08-20 12:14:58.183794
8b95d58d-6e97-4577-998b-1ceb7ddf1e22	wamid.TEST_cd0b0fd4	whatsapp	t	\N	8	\N	2026-08-21 06:16:10.936393	2026-08-21 06:16:10.944005
1a5dd064-218f-4649-80b3-4b8d06b4f1c4	wamid.DEDUP_cbac7847	whatsapp	t	\N	47	\N	2026-08-21 06:16:11.15158	2026-08-21 06:16:11.173709
0499463d-a92e-4e36-bf1b-a2b8650134b4	wamid.TEST_e5245092	whatsapp	t	\N	53	\N	2026-08-20 13:35:47.428874	2026-08-20 13:35:47.456329
9f55adfb-c27b-4f41-97b8-024d2fd80a91	m_ws_broadcast_test_f27d3b07	instagram	t	\N	\N	{"sender": {"id": "23086741_bb43"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f27d3b07", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 11:17:27.144068	\N
ef03e1d9-ca26-47da-a114-029b698ee5a8	m_exact_test_f8a4dead	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_f8a4dead", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 12:15:08.971725	\N
bd5222ce-4f44-43a9-8cc8-8396abd9df65	m_exact_test_3c156f3a	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_3c156f3a", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 11:17:27.487722	\N
4d59a1df-b5a9-4518-ad8c-4fc8e0119914	wamid.TEST_978124e4	whatsapp	t	\N	45	\N	2026-08-20 12:37:56.342717	2026-08-20 12:37:56.365378
ec17bc1f-f073-4fd4-8ed4-a73f465c5027	wamid.TEST_595f6aff	whatsapp	t	\N	59	\N	2026-08-20 13:35:47.710739	2026-08-20 13:35:47.740389
a5556321-2312-4457-aa6b-ef6eed91b29c	wamid.TEST_a78a08e3	whatsapp	t	\N	8	\N	2026-08-20 12:37:56.369139	2026-08-20 12:37:56.37657
0511d4ed-7dfc-490c-804b-398106ac1157	wamid.TEST_431c1dfb	whatsapp	t	\N	43	\N	2026-08-20 12:37:56.470939	2026-08-20 12:37:56.491128
0f362750-7d3a-4597-8687-eab0778ed9f9	wamid.TEST_decace6f	whatsapp	t	\N	13	\N	2026-08-20 13:35:47.746393	2026-08-20 13:35:47.757926
53f561f6-4a85-4317-bb0f-ed138179a5cd	wamid.DEDUP_78662447	whatsapp	t	\N	42	\N	2026-08-20 12:37:56.579854	2026-08-20 12:37:56.599153
0d97be42-01df-478a-855f-236748d6c248	wamid.TEST_861ab004	whatsapp	t	\N	42	\N	2026-08-21 06:41:21.905483	2026-08-21 06:41:21.924595
3f3b9263-2478-4247-9a68-084b6b73c98e	wamid.TEST_5bfbfddc	whatsapp	t	\N	7	\N	2026-08-21 06:41:21.927955	2026-08-21 06:41:21.935086
038bdff5-cbea-4961-b554-46eff6e0730b	m_ws_broadcast_test_c499afab	instagram	t	\N	\N	{"sender": {"id": "23086741_725c"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_c499afab", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 13:35:59.671015	\N
1e76cc82-dcbc-41a3-b665-8bd3c9345552	wamid.TEST_b9c31507	whatsapp	t	\N	46	\N	2026-08-21 04:35:27.83517	2026-08-21 04:35:27.857221
dae49d4f-477f-444e-a33d-0b7e15f39572	wamid.DEDUP_6ba68c4b	whatsapp	t	\N	49	\N	2026-08-21 06:41:22.134002	2026-08-21 06:41:22.158695
a742b3d3-d563-4061-be58-bf14f4cd9314	m_exact_test_30ba55de	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_30ba55de", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 12:38:07.260297	\N
0d59714e-25b4-4de6-8d90-625a0342c7cf	wamid.TEST_6213184f	whatsapp	t	\N	11	\N	2026-08-21 04:35:27.86105	2026-08-21 04:35:27.87132
fc8db7bd-0dbe-43eb-a666-5d4a2179c77b	wamid.TEST_936c3398	whatsapp	t	\N	43	\N	2026-08-20 12:55:08.309279	2026-08-20 12:55:08.329503
46b1b116-b734-465a-8bee-0d1e91d72adf	wamid.TEST_5fcc6d2d	whatsapp	t	\N	8	\N	2026-08-20 12:55:08.333174	2026-08-20 12:55:08.34033
9ce92bb3-68f7-44e3-9404-8cf84562b838	wamid.TEST_5869d753	whatsapp	t	\N	50	\N	2026-08-20 12:55:08.44278	2026-08-20 12:55:08.466802
41d3170c-17bc-49c5-8413-89fbd147809b	wamid.DEDUP_601dcc5e	whatsapp	t	\N	42	\N	2026-08-20 12:55:08.556282	2026-08-20 12:55:08.575623
719edd07-1488-4c1e-86e6-b93bb94ac353	wamid.TEST_653acfcb	whatsapp	t	\N	51	\N	2026-08-21 05:44:23.100165	2026-08-21 05:44:23.124948
a351334f-874b-40ba-ac77-ef1c63f67df7	wamid.TEST_a84cf2df	whatsapp	t	\N	48	\N	2026-08-21 05:44:23.354148	2026-08-21 05:44:23.373895
82f15278-f68c-4d32-aff0-467167822202	m_ws_broadcast_test_d984fcd5	instagram	t	\N	\N	{"sender": {"id": "23086741_b9ea"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_d984fcd5", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 12:55:18.890987	\N
eae52b17-887e-4cfc-b2c2-22705783f587	wamid.TEST_f6d60acd	whatsapp	t	\N	43	\N	2026-08-21 08:14:33.880708	2026-08-21 08:14:33.90025
66a9f1da-d989-42b9-a7f7-dd138bd60e38	wamid.TEST_95330ef3	whatsapp	t	\N	52	\N	2026-08-20 12:59:40.525596	2026-08-20 12:59:40.55249
3fa04c79-1504-459e-8b52-0ec2f3e12714	wamid.TEST_b59fe5f2	whatsapp	t	\N	9	\N	2026-08-21 05:44:23.377394	2026-08-21 05:44:23.385927
fb9f090c-5837-4eaa-8d1c-ebef91e07af8	wamid.TEST_0306d994	whatsapp	t	\N	44	\N	2026-08-20 12:59:40.650897	2026-08-20 12:59:40.671749
a157fa74-c9f9-460a-8bb5-f8f6b4145f40	wamid.TEST_a7350dbf	whatsapp	t	\N	10	\N	2026-08-20 12:59:40.675475	2026-08-20 12:59:40.684885
51c27415-85ee-4527-9079-27ebc8bd8c6a	wamid.TEST_f4e9308d	whatsapp	t	\N	8	\N	2026-08-21 08:14:33.90372	2026-08-21 08:14:33.911101
ca337dc6-85b7-46d6-82a4-544734026ec1	wamid.TEST_2fd75430	whatsapp	t	\N	43	\N	2026-08-20 12:59:40.767366	2026-08-20 12:59:40.787186
b5097ea5-0f9d-412c-b8a4-e008059ba5a2	wamid.TEST_4c992c7c	whatsapp	t	\N	9	\N	2026-08-20 12:59:40.790735	2026-08-20 12:59:40.799008
8a8a0e94-e4e2-42ff-98d5-de7f12ff5bdb	m_ws_broadcast_test_3c1afbb6	instagram	t	\N	\N	{"sender": {"id": "23086741_28f6"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_3c1afbb6", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 05:44:33.738229	\N
a438cdd4-e6c3-4822-b808-bb21603e618b	wamid.TEST_d96c8953	whatsapp	t	\N	42	\N	2026-08-21 08:14:34.00659	2026-08-21 08:14:34.025753
d5a3c7a5-0eb9-4703-a17f-9e5982e3c45c	wamid.TEST_0dc4e71a	whatsapp	t	\N	42	\N	2026-08-21 05:51:03.751806	2026-08-21 05:51:03.771133
f74c0eac-5e8c-4839-8547-982fcea1497f	wamid.TEST_4eac96b3	whatsapp	t	\N	8	\N	2026-08-21 05:51:03.774813	2026-08-21 05:51:03.782572
db71d7ab-e04d-4d17-86d5-a12989f32d43	wamid.DEDUP_453bbf4d	whatsapp	t	\N	50	\N	2026-08-21 08:14:34.115566	2026-08-21 08:14:34.142384
98aba37d-fc4b-42e1-90c4-23a07ffff8db	wamid.TEST_84dbd895	whatsapp	t	\N	57	\N	2026-08-21 11:13:12.828838	2026-08-21 11:13:12.85838
cef2ec4e-68ee-48ac-a6ec-43f36ca2dfd2	wamid.TEST_cce5459e	whatsapp	t	\N	53	\N	2026-08-21 05:54:20.135285	2026-08-21 05:54:20.163146
bc68e894-2292-4552-a6f0-a486c0f3f7d9	wamid.TEST_ec67dcf1	whatsapp	t	\N	42	\N	2026-08-21 05:54:20.36335	2026-08-21 05:54:20.382341
2f707c9d-6985-4588-8701-7bd6b497d7e4	wamid.TEST_88226efe	whatsapp	t	\N	8	\N	2026-08-21 05:54:20.385963	2026-08-21 05:54:20.393413
aa237c4a-d046-477a-9850-c57a89eebd3d	m_ws_broadcast_test_e51c337a	instagram	t	\N	\N	{"sender": {"id": "23086741_a8ff"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_e51c337a", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 05:55:16.852926	\N
bbdebc6f-12b4-43b3-81fe-1a6a3a378ea0	wamid.TEST_9b08f964	whatsapp	t	\N	43	\N	2026-08-21 06:01:38.621815	2026-08-21 06:01:38.641845
446051a5-fde2-456d-8452-a9e04c87e1fd	wamid.TEST_8d586180	whatsapp	t	\N	9	\N	2026-08-21 06:01:38.645569	2026-08-21 06:01:38.654235
dd4b4c75-73af-486b-94fa-8e3c592a683d	wamid.TEST_18220ea6	whatsapp	t	\N	48	\N	2026-08-21 06:07:39.955065	2026-08-21 06:07:39.979769
0242c080-2147-4d17-9c06-7402a8e0899f	wamid.TEST_6d48e8b1	whatsapp	t	\N	42	\N	2026-08-21 06:07:40.197626	2026-08-21 06:07:40.216804
fdf3799f-8ce1-4bd9-a1c9-3988e462832f	wamid.TEST_003683b5	whatsapp	t	\N	8	\N	2026-08-21 06:07:40.220347	2026-08-21 06:07:40.227734
b4e6082e-d589-4617-8a35-a02cec0211b7	m_ws_broadcast_test_c86c723d	instagram	t	\N	\N	{"sender": {"id": "23086741_6751"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_c86c723d", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 06:08:36.411352	\N
c12b9044-28d5-4a4c-a38e-6eb50b1c636f	wamid.TEST_e27f6c66	whatsapp	t	\N	47	\N	2026-08-24 05:20:21.814755	2026-08-24 05:20:21.839132
09202879-43d5-45b0-982a-b0860e655e31	wamid.TEST_52941b7d	whatsapp	t	\N	46	\N	2026-08-20 12:13:01.724077	2026-08-20 12:13:01.746103
577982fe-d07a-4bd1-9783-ca92b953513d	m_exact_test_7385cc8d	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_7385cc8d", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 12:13:13.097998	\N
8c083315-c37d-460f-b1c4-c92acde25661	wamid.TEST_1cc5613e	whatsapp	t	\N	9	\N	2026-08-20 12:13:01.749604	2026-08-20 12:13:01.758332
e52dde16-50df-40ba-bdb3-4900d2b2a325	wamid.TEST_f101fb15	whatsapp	t	\N	65	\N	2026-08-20 13:34:20.941994	2026-08-20 13:34:20.969062
1a0dad5a-97d8-44a8-b4b1-d1eb0c71688a	wamid.TEST_cc035032	whatsapp	t	\N	48	\N	2026-08-20 12:13:01.792117	2026-08-20 12:13:01.814613
833ab701-5224-4672-8451-37a4c427c8bc	wamid.TEST_0b0daffc	whatsapp	t	\N	48	\N	2026-08-20 12:14:57.968066	2026-08-20 12:14:57.991201
8ef1b98f-6cba-4341-a867-f1852e827b97	wamid.TEST_7c2e01fd	whatsapp	t	\N	11	\N	2026-08-20 12:13:01.818035	2026-08-20 12:13:01.828414
fd54c190-6b8e-47e7-b1da-a95c34e1406f	wamid.TEST_546d455e	whatsapp	t	\N	43	\N	2026-08-21 06:16:10.976602	2026-08-21 06:16:10.996268
c4124780-8506-4e38-b109-9de28bc631b7	wamid.TEST_1e38df50	whatsapp	t	\N	46	\N	2026-08-20 12:13:01.861509	2026-08-20 12:13:01.882071
c6e89d86-9e18-4c4f-8296-5ef080b077dc	wamid.TEST_b400c0e6	whatsapp	t	\N	9	\N	2026-08-20 12:14:57.994921	2026-08-20 12:14:58.003993
f51bb177-2ee2-4892-b015-2c8969d53a2b	wamid.TEST_b6ce2bfb	whatsapp	t	\N	45	\N	2026-08-20 12:13:01.914091	2026-08-20 12:13:01.934717
6238f14c-1074-402a-bf4e-d980a4f369e5	wamid.TEST_988a2a44	whatsapp	t	\N	10	\N	2026-08-20 13:34:20.972805	2026-08-20 13:34:20.982273
d9ef64c4-ea60-4024-be28-6a928dec9c30	wamid.TEST_6ffe361d	whatsapp	t	\N	9	\N	2026-08-20 12:13:01.938836	2026-08-20 12:13:01.946921
ef757941-cb64-4310-b146-a2128eea73f9	wamid.TEST_a9ab548c	whatsapp	t	\N	48	\N	2026-08-20 12:14:58.091831	2026-08-20 12:14:58.114226
1def5826-5c36-42f4-8c46-ba273d5ccc0f	wamid.DEDUP_c3907b8d	whatsapp	t	\N	51	\N	2026-08-20 12:13:01.980932	2026-08-20 12:13:02.005681
fb27c97e-7310-433d-812d-acd2062668b9	wamid.TEST_a6b80534	whatsapp	t	\N	43	\N	2026-08-21 13:22:24.030296	2026-08-21 13:22:24.049547
7d4a2178-a9e0-44d2-9214-b0979a9a5a64	wamid.TEST_a1004c82	whatsapp	t	\N	10	\N	2026-08-20 12:14:58.117474	2026-08-20 12:14:58.127199
68bf4790-2394-4840-af95-59a1a456893c	wamid.TEST_0e999eb6	whatsapp	t	\N	8	\N	2026-08-21 06:16:10.999776	2026-08-21 06:16:11.007756
b205afc8-d812-4c6f-bd3b-6f298579c917	wamid.TEST_8f865774	whatsapp	t	\N	7	\N	2026-08-21 13:22:24.052714	2026-08-21 13:22:24.059692
ea055f5b-37aa-4d76-9afb-770e994beb25	wamid.TEST_a01f4933	whatsapp	t	\N	45	\N	2026-08-20 13:35:47.490686	2026-08-20 13:35:47.512456
d455ae8d-8abe-4a09-9228-3fcd6b0f1efc	wamid.TEST_da369d68	whatsapp	t	\N	45	\N	2026-08-21 13:22:24.155385	2026-08-21 13:22:24.17516
7db4ffe8-6030-4b73-8ca4-ac089bff1f3f	wamid.TEST_0a2184b0	whatsapp	t	\N	8	\N	2026-08-20 13:35:47.516194	2026-08-20 13:35:47.523239
dbc51a94-90cb-453c-a043-4b7131f71ec1	wamid.DEDUP_496e960e	whatsapp	t	\N	80	\N	2026-08-20 13:35:47.806458	2026-08-20 13:35:47.848126
49cbaff6-b048-4bc6-b7b9-66207ce31e28	m_ws_broadcast_test_d61d1e14	instagram	t	\N	\N	{"sender": {"id": "23086741_9e4f"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_d61d1e14", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 12:15:08.601625	\N
1d110cd3-9910-48e2-b84f-0af188852251	m_ws_broadcast_test_e689d58c	instagram	t	\N	\N	{"sender": {"id": "23086741_a754"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_e689d58c", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 06:17:08.058073	\N
6a94cbda-aa3e-4825-a556-1e41b803e7e1	wamid.TEST_d1855abd	whatsapp	t	\N	50	\N	2026-08-20 12:37:56.287294	2026-08-20 12:37:56.31068
f589b5a4-72d9-4a74-9317-9cbae659d882	wamid.DEDUP_2153f79b	whatsapp	t	\N	49	\N	2026-08-21 13:22:24.267824	2026-08-21 13:22:24.291534
712291c1-aae1-4b9b-bcf3-5b10baa7f715	wamid.TEST_4348e30b	whatsapp	t	\N	43	\N	2026-08-20 12:37:56.408272	2026-08-20 12:37:56.428689
16f408cb-6fe8-41a9-87ea-da8c283484e7	wamid.TEST_7dab99af	whatsapp	t	\N	41	\N	2026-08-21 06:41:21.96533	2026-08-21 06:41:21.984202
3b616dfa-9e29-4eac-a85a-132a79e3c888	wamid.TEST_83a92a25	whatsapp	t	\N	9	\N	2026-08-20 12:37:56.432259	2026-08-20 12:37:56.440618
48cbb40b-154d-4315-a4ad-c6397976fe95	m_exact_test_7c1a8d30	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_7c1a8d30", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 13:36:00.062829	\N
e5b3d6c6-ea19-418f-8561-81ad8f8f2d97	wamid.TEST_44c16fb7	whatsapp	t	\N	42	\N	2026-08-20 12:37:56.520951	2026-08-20 12:37:56.540102
1f5a19ef-3dbe-4c5d-8aac-204d58c7fe90	wamid.TEST_b971d0a3	whatsapp	t	\N	8	\N	2026-08-20 12:37:56.54367	2026-08-20 12:37:56.551076
9389cd13-1746-4c43-a2cb-9400b1e565d0	wamid.TEST_36933d32	whatsapp	t	\N	45	\N	2026-08-21 04:35:27.904747	2026-08-21 04:35:27.924876
7923a128-3e3c-457f-8a1d-e4df27a47fc3	wamid.TEST_0aadd08a	whatsapp	t	\N	8	\N	2026-08-21 06:41:21.987779	2026-08-21 06:41:21.995568
fb53bc25-d9f4-4e19-82fb-8bdec3c2cea1	wamid.TEST_7faf7cbc	whatsapp	t	\N	53	\N	2026-08-21 05:44:23.163937	2026-08-21 05:44:23.188304
cc3d07e2-e491-420f-9729-d098be2b4616	wamid.TEST_2d2b0225	whatsapp	t	\N	8	\N	2026-08-21 05:44:23.191828	2026-08-21 05:44:23.199313
470de1e2-682d-4060-a541-6772d85da1c4	m_ws_broadcast_test_6f2d1a82	instagram	t	\N	\N	{"sender": {"id": "23086741_14d5"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_6f2d1a82", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 12:38:06.91671	\N
ab6c270c-0fc2-48ae-b3b0-ee219eebe162	wamid.TEST_aee9dbfc	whatsapp	t	\N	46	\N	2026-08-20 12:55:08.254202	2026-08-20 12:55:08.277197
cd1dcea2-44ad-4ce7-b31b-46f4c25af6a5	wamid.DEDUP_b1de4856	whatsapp	t	\N	44	\N	2026-08-21 05:44:23.417246	2026-08-21 05:44:23.436361
e35bb52d-692f-42b8-904b-0062a811d9ba	wamid.TEST_d7ac532d	whatsapp	t	\N	46	\N	2026-08-20 12:55:08.371632	2026-08-20 12:55:08.394004
00c5052e-875c-4ba7-9baa-bfb01f57bd23	wamid.TEST_ef620b4c	whatsapp	t	\N	10	\N	2026-08-20 12:55:08.39853	2026-08-20 12:55:08.408271
dc0907ff-4fc5-42dc-8b36-9ad478889c13	wamid.TEST_bcb95470	whatsapp	t	\N	43	\N	2026-08-20 12:55:08.497639	2026-08-20 12:55:08.517211
35e14215-5640-428b-a3ea-4b791456c47d	wamid.TEST_54821eed	whatsapp	t	\N	7	\N	2026-08-20 12:55:08.520364	2026-08-20 12:55:08.527113
667f5784-92bb-44d0-9838-732dadc64201	m_exact_test_28951bfa	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_28951bfa", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 05:44:34.095813	\N
30ad6977-5e95-4018-a5e6-4a8064576db1	wamid.TEST_a4723a1b	whatsapp	t	\N	50	\N	2026-08-21 05:51:03.816452	2026-08-21 05:51:03.840431
48629f01-3b7f-4813-9f1c-cf8004d18d61	wamid.TEST_a65b85d9	whatsapp	t	\N	41	\N	2026-08-21 05:54:20.195846	2026-08-21 05:54:20.214462
46c35107-ed85-4214-934e-319b5739932e	m_exact_test_f402a026	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_f402a026", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 12:55:19.236535	\N
bf9183b7-da5c-42d1-bc8c-cbc860012ec7	wamid.TEST_889cfcfd	whatsapp	t	\N	45	\N	2026-08-20 12:59:40.588211	2026-08-20 12:59:40.608896
a23fa77e-e834-4ebc-9ab6-48ab5996f1bc	wamid.TEST_5ca34fbc	whatsapp	t	\N	7	\N	2026-08-21 05:54:20.217974	2026-08-21 05:54:20.224769
e3288c38-3433-4983-8e12-85fcf52513c7	wamid.TEST_dd17b382	whatsapp	t	\N	7	\N	2026-08-20 12:59:40.612566	2026-08-20 12:59:40.619466
9ab4be53-2906-4a61-9366-5a266a665732	wamid.TEST_286cb9d1	whatsapp	t	\N	44	\N	2026-08-20 12:59:40.716936	2026-08-20 12:59:40.737381
7d27b798-39a7-4024-a0a4-2f977dad4226	wamid.DEDUP_08d0cfd1	whatsapp	t	\N	47	\N	2026-08-21 05:54:20.424224	2026-08-21 05:54:20.446351
85fc86f3-6516-4862-805f-94ff07cbf078	wamid.DEDUP_b8f65403	whatsapp	t	\N	44	\N	2026-08-20 12:59:40.828182	2026-08-20 12:59:40.849416
43b4cfd2-d3a8-4630-a4c0-79cf9950a49b	m_exact_test_56da62e3	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_56da62e3", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 05:55:17.203441	\N
bcc79524-d35c-4533-af02-99ae4351c137	wamid.TEST_8526a8f5	whatsapp	t	\N	48	\N	2026-08-21 06:01:38.687648	2026-08-21 06:01:38.710796
dda764c4-6a35-4f7e-b0b7-c4c7657738a0	wamid.TEST_9310265f	whatsapp	t	\N	43	\N	2026-08-21 06:07:40.012143	2026-08-21 06:07:40.032026
404c395c-78fc-4398-b393-690e5e6924ac	wamid.TEST_eaa4667b	whatsapp	t	\N	7	\N	2026-08-21 06:07:40.035334	2026-08-21 06:07:40.042282
5ffdfd1c-c2ea-41c0-aa0b-2e44c6adab52	wamid.DEDUP_cbf40113	whatsapp	t	\N	43	\N	2026-08-21 06:07:40.256559	2026-08-21 06:07:40.276739
c5b0847f-6d92-43dd-8665-85caf349c1b6	m_exact_test_c7eb950f	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_c7eb950f", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 06:08:36.768692	\N
6d7ad5b9-a806-4228-89d0-b5bf817a2361	wamid.TEST_f6652259	whatsapp	t	\N	83	\N	2026-08-25 07:02:07.996425	2026-08-25 07:02:08.041974
7a65f751-6c62-484e-bebc-5ea3022afa0d	wamid.TEST_3ce94d1f	whatsapp	t	\N	47	\N	2026-08-20 13:34:21.015474	2026-08-20 13:34:21.037999
5ae13e66-08d3-4f5a-bb68-f4b60e76c20a	wamid.TEST_a6f844fd	whatsapp	t	\N	43	\N	2026-08-21 06:16:11.038642	2026-08-21 06:16:11.058135
f4e77120-3930-4408-9d96-0dc2aa4158b8	m_ws_broadcast_test_ec215550	instagram	t	\N	\N	{"sender": {"id": "23086741_3a13"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_ec215550", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 13:34:32.892733	\N
226d5a8f-885e-43f9-94ac-d161a275b12a	m_ws_broadcast_test_78c5a7c2	instagram	t	\N	\N	{"sender": {"id": "23086741_c2e5"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_78c5a7c2", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 12:59:51.266444	\N
f793e86f-d66c-474c-943f-81c4fe976d7f	m_exact_test_2d5a9ec3	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_2d5a9ec3", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 12:59:51.608647	\N
d7469cd0-08e3-4c7e-9b50-11f0669db3c7	wamid.TEST_5d6c3287	whatsapp	t	\N	63	\N	2026-08-20 13:35:47.556577	2026-08-20 13:35:47.59613
9ff6ae4c-cc41-479e-ae71-57dc2e627175	wamid.TEST_860945c6	whatsapp	t	\N	10	\N	2026-08-20 13:35:47.599961	2026-08-20 13:35:47.609072
78bae221-5611-45f2-bc7a-760f08b41f0a	wamid.TEST_628ae6c5	whatsapp	t	\N	7	\N	2026-08-21 04:35:27.979431	2026-08-21 04:35:27.986417
7a6331df-31a1-4233-99c3-3ea0f6ab2234	wamid.TEST_99da4adb	whatsapp	t	\N	143	\N	2026-08-27 08:12:57.350507	2026-08-27 08:12:57.411663
5b8b2762-6ee3-45f6-8559-e26ce90e10a8	m_ws_broadcast_test_fa0a6e79	instagram	t	\N	\N	{"sender": {"id": "23086741_8f11"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_fa0a6e79", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 04:35:38.20075	\N
d572d3b0-7d06-4f48-a9a0-5962eaec87ba	m_ws_broadcast_test_0542aea7	instagram	t	\N	\N	{"sender": {"id": "23086741_bfb7"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_0542aea7", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 06:42:19.204147	\N
bc996886-f8cc-43a2-9d62-aed1dda0094b	wamid.TEST_b0454597	whatsapp	t	\N	44	\N	2026-08-21 05:44:23.232081	2026-08-21 05:44:23.251419
8b80f5ca-1f03-417d-b531-cea491dd977b	m_exact_test_dbc9f0fe	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_dbc9f0fe", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 06:42:19.543532	\N
eb4e97dd-0160-4ca3-9c9e-176bc7d8a68c	wamid.TEST_6a123eee	whatsapp	t	\N	8	\N	2026-08-21 05:44:23.254905	2026-08-21 05:44:23.262486
a17ddd6a-6112-4c64-ab8d-481be1cc68af	wamid.TEST_4f248312	whatsapp	t	\N	42	\N	2026-08-21 08:14:33.941934	2026-08-21 08:14:33.96157
61480f62-039d-4c88-ae31-7df7f5426faf	wamid.TEST_e38d9f51	whatsapp	t	\N	9	\N	2026-08-21 08:14:33.965548	2026-08-21 08:14:33.974303
6d7c5b68-64b1-4cf2-a75d-3614aff70e3e	wamid.TEST_6b4f6dfc	whatsapp	t	\N	42	\N	2026-08-21 08:14:34.05514	2026-08-21 08:14:34.074539
243f5708-84b6-45f9-a06a-e89bbf32dd34	wamid.TEST_9d0bf5e3	whatsapp	t	\N	45	\N	2026-08-21 05:51:03.63763	2026-08-21 05:51:03.659161
53ccee0f-9747-45cf-a7a0-a59f17f2888e	wamid.TEST_0c7d4d8a	whatsapp	t	\N	7	\N	2026-08-21 08:14:34.078585	2026-08-21 08:14:34.085482
d9c434c8-e63f-4e91-b20d-e9ffbc086129	wamid.TEST_29f9c5b6	whatsapp	t	\N	46	\N	2026-08-21 05:51:03.872062	2026-08-21 05:51:03.893379
47287cec-ffd2-4fba-8c51-80eb630a947a	wamid.TEST_ddda7d91	whatsapp	t	\N	8	\N	2026-08-21 05:51:03.897016	2026-08-21 05:51:03.904984
77ce98fc-9aef-4b5d-aff9-e9c2f1003537	m_ws_broadcast_test_ea10cb21	instagram	t	\N	\N	{"sender": {"id": "23086741_d42e"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_ea10cb21", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 05:52:01.080549	\N
94d324bb-7159-424d-88bd-f8c5d2a06163	wamid.TEST_32c33e47	whatsapp	t	\N	42	\N	2026-08-21 05:54:20.255457	2026-08-21 05:54:20.27426
7f2b65d3-314b-4e8f-81f5-d42ee5d8f2d7	wamid.TEST_33a77786	whatsapp	t	\N	8	\N	2026-08-21 05:54:20.277518	2026-08-21 05:54:20.285633
5fe017eb-871f-4524-94ca-b966c57fb08d	wamid.TEST_78066574	whatsapp	t	\N	49	\N	2026-08-21 06:01:38.505142	2026-08-21 06:01:38.530378
c2e084c1-e2fe-42fc-a48d-f5c55021242e	wamid.TEST_0f257400	whatsapp	t	\N	45	\N	2026-08-21 06:01:38.742898	2026-08-21 06:01:38.762676
8f4fd00d-0231-4806-a939-e09798a51fa2	wamid.TEST_4775882a	whatsapp	t	\N	7	\N	2026-08-21 06:01:38.766491	2026-08-21 06:01:38.773555
b1536b92-d7be-48e0-a716-457a0d961deb	m_ws_broadcast_test_5a64ba53	instagram	t	\N	\N	{"sender": {"id": "23086741_284c"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_5a64ba53", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 08:15:31.198606	\N
c2ebb058-ee76-413c-8754-16e772199fff	m_exact_test_1aa5e4db	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_1aa5e4db", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 08:15:31.554525	\N
a7f315c7-7b53-4917-a1ce-1771589e830a	m_ws_broadcast_test_703cbea8	instagram	t	\N	\N	{"sender": {"id": "23086741_ba5a"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_703cbea8", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 06:02:35.489082	\N
6c29b641-6a5b-4213-84f9-95d8d7599e60	wamid.TEST_ddbbc0d4	whatsapp	t	\N	43	\N	2026-08-21 06:07:40.0736	2026-08-21 06:07:40.093666
8df3f0d2-e82f-484e-a63e-92e023da5342	wamid.TEST_184a82ff	whatsapp	t	\N	47	\N	2026-08-21 11:13:12.896345	2026-08-21 11:13:12.915735
94e005bb-361a-41dc-a864-6da7d2ce06b1	wamid.TEST_21ea756f	whatsapp	t	\N	9	\N	2026-08-21 06:07:40.09752	2026-08-21 06:07:40.105494
8d62d9c8-0f88-497a-84d8-775f99896f97	wamid.TEST_76a8a92e	whatsapp	t	\N	10	\N	2026-08-21 11:13:12.919625	2026-08-21 11:13:12.929086
be1c7626-2294-427f-bfab-581f2a38dd1e	wamid.TEST_1253a71a	whatsapp	t	\N	49	\N	2026-08-21 11:13:12.962624	2026-08-21 11:13:12.986075
eed48a1f-26b8-4384-b59e-68dd640b6b15	wamid.TEST_bf20abed	whatsapp	t	\N	11	\N	2026-08-21 11:13:12.992401	2026-08-21 11:13:13.002032
80674dd2-ed53-4035-b299-5abe79124405	wamid.TEST_51513f82	whatsapp	t	\N	53	\N	2026-08-21 11:13:13.046257	2026-08-21 11:13:13.067269
4625054a-514b-43e6-b167-afe37470d278	wamid.TEST_0d5fe300	whatsapp	t	\N	49	\N	2026-08-21 11:13:13.103276	2026-08-21 11:13:13.126195
87e6eab5-c83b-481c-b20a-a422f026219d	wamid.TEST_10dd53db	whatsapp	t	\N	9	\N	2026-08-21 11:13:13.130266	2026-08-21 11:13:13.138797
ec03b8ba-e62d-4553-a157-bfae71812657	wamid.DEDUP_54233e46	whatsapp	t	\N	46	\N	2026-08-21 11:13:13.169954	2026-08-21 11:13:13.192084
9c3729f6-1329-4eb0-b5fb-8decf3d0cfeb	m_ws_broadcast_test_f68be478	instagram	t	\N	\N	{"sender": {"id": "23086741_78c1"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f68be478", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 11:14:10.633744	\N
d8f85334-e18b-480c-9049-8797e9dfdeb9	m_exact_test_d6df5942	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_d6df5942", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 11:14:10.980962	\N
4bca2833-21ce-48ee-a0d9-ce0403ba4b83	wamid.TEST_4483f08d	whatsapp	t	\N	61	\N	2026-08-21 11:25:04.228306	2026-08-21 11:25:04.258885
9733b28a-fefb-4b18-97dc-7ef17857a38f	wamid.TEST_633f97b5	whatsapp	t	\N	65	\N	2026-08-21 11:25:04.299866	2026-08-21 11:25:04.338079
4712d42e-0b88-4d3d-b289-0d072f4fd657	wamid.TEST_67980ed8	whatsapp	t	\N	8	\N	2026-08-21 11:25:04.342159	2026-08-21 11:25:04.349904
d4c67201-7fc1-4793-90c3-8eb7eeb1b280	wamid.TEST_bc3b09bc	whatsapp	t	\N	54	\N	2026-08-21 11:25:04.389563	2026-08-21 11:25:04.418279
af286867-e403-4502-b8c4-35865b6c0673	wamid.TEST_08738ca7	whatsapp	t	\N	17	\N	2026-08-21 11:25:04.4242	2026-08-21 11:25:04.439684
e0fd6716-6d56-423e-989d-f0062b01fa29	wamid.TEST_f27c233d	whatsapp	t	\N	64	\N	2026-08-21 11:25:04.476247	2026-08-21 11:25:04.513216
05a89caa-0c17-47cf-b851-5302d1362032	wamid.TEST_1b64c60d	whatsapp	t	\N	53	\N	2026-08-20 13:09:39.046701	2026-08-20 13:09:39.075005
f44c2ac6-9036-4b73-8d38-8d9e8ca19d51	wamid.TEST_7483e5ad	whatsapp	t	\N	42	\N	2026-08-21 13:22:24.089968	2026-08-21 13:22:24.109835
b2019d92-b8df-4619-9704-b12eb2191f93	wamid.TEST_25691fda	whatsapp	t	\N	51	\N	2026-08-20 13:09:39.112628	2026-08-20 13:09:39.136355
7e497dbf-61e6-4367-bfc0-2d69b3e2ae44	wamid.TEST_1fc6ee52	whatsapp	t	\N	50	\N	2026-08-20 13:34:21.071629	2026-08-20 13:34:21.095136
a85dcc4c-ee43-4752-8954-a8d9047de08d	wamid.TEST_b4984a40	whatsapp	t	\N	10	\N	2026-08-20 13:09:39.141789	2026-08-20 13:09:39.150614
12b827ba-5436-407e-951c-2f69ace88cc2	wamid.TEST_471536d6	whatsapp	t	\N	43	\N	2026-08-21 06:16:11.08834	2026-08-21 06:16:11.107976
20a9b307-b3ae-49c6-abd1-8bfc5742e0f9	wamid.TEST_40883d71	whatsapp	t	\N	45	\N	2026-08-20 13:09:39.184803	2026-08-20 13:09:39.206139
af694763-e4f8-4790-8875-9382baf49f4b	wamid.TEST_6afbc664	whatsapp	t	\N	10	\N	2026-08-20 13:34:21.100298	2026-08-20 13:34:21.109122
e0843667-e9db-4e49-8c55-3daa1f4e3125	wamid.TEST_5b90234c	whatsapp	t	\N	9	\N	2026-08-20 13:09:39.210343	2026-08-20 13:09:39.218985
df7216de-3190-424c-b4eb-129b5fe2d0b7	wamid.TEST_0c8dbc4a	whatsapp	t	\N	48	\N	2026-08-20 13:09:39.253362	2026-08-20 13:09:39.27662
d587087c-4b3a-400a-8ec9-8eda3ee8fcf5	wamid.TEST_f4c9dd9d	whatsapp	t	\N	8	\N	2026-08-21 06:16:11.111686	2026-08-21 06:16:11.119124
0bbf0213-d1d5-4f2e-9d30-621d1fda4203	wamid.TEST_3ebb5f34	whatsapp	t	\N	48	\N	2026-08-20 13:09:39.310278	2026-08-20 13:09:39.332491
e4864cc8-249d-466a-9bb7-56c850bb5a6a	wamid.TEST_82a424a5	whatsapp	t	\N	33	\N	2026-08-20 13:09:39.336398	2026-08-20 13:09:39.36851
95fbfdf5-53a5-445e-92e4-6a0a89c3c991	m_exact_test_78d5a81a	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_78d5a81a", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 13:34:33.261394	\N
37b1316d-d1ed-4ad5-809a-6c6c588f0938	wamid.DEDUP_c710b0a5	whatsapp	t	\N	43	\N	2026-08-20 13:09:39.398902	2026-08-20 13:09:39.418004
d22b33c4-5092-49ce-a91a-352dec30b1f7	wamid.TEST_4737d231	whatsapp	t	\N	52	\N	2026-08-20 13:35:47.646287	2026-08-20 13:35:47.670896
219c2623-69d8-4e14-b123-bbe5a86acfbe	wamid.TEST_07eb8e12	whatsapp	t	\N	48	\N	2026-08-21 06:41:21.849452	2026-08-21 06:41:21.873951
3dfdcc4a-209a-4c03-8662-6a3937198821	wamid.TEST_d1be25f0	whatsapp	t	\N	42	\N	2026-08-21 06:41:22.074014	2026-08-21 06:41:22.093188
ff13406b-36b8-4862-9c16-d05221863bff	wamid.TEST_4988cc34	whatsapp	t	\N	7	\N	2026-08-21 06:41:22.096754	2026-08-21 06:41:22.103885
59e8754c-c435-4c07-bd4b-93039379b435	wamid.TEST_ea37936c	whatsapp	t	\N	43	\N	2026-08-21 04:35:27.772467	2026-08-21 04:35:27.792559
1f7f93ff-b1ad-4c8b-b1fa-1718212de066	wamid.TEST_788832f4	whatsapp	t	\N	7	\N	2026-08-21 04:35:27.795968	2026-08-21 04:35:27.80294
eb10c99d-2390-449a-bb88-cbf66ba7ef79	wamid.TEST_adb66b1a	whatsapp	t	\N	49	\N	2026-08-21 08:14:33.823364	2026-08-21 08:14:33.848311
06755f55-33b0-44ad-80f2-1d17f4489994	wamid.DEDUP_28fbe9e7	whatsapp	t	\N	43	\N	2026-08-21 04:35:28.015864	2026-08-21 04:35:28.035703
48358d8b-dfbe-4119-a248-870f4b237727	m_ws_broadcast_test_a2458549	instagram	t	\N	\N	{"sender": {"id": "23086741_8a08"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a2458549", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 13:09:49.548952	\N
42067e16-7443-4a10-9810-f0824fa58a10	m_exact_test_a95c82a9	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_a95c82a9", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 04:35:38.543376	\N
f8c95957-6c9c-4646-b1fb-124d17a5be74	m_exact_test_d70ab681	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_d70ab681", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 13:09:49.884718	\N
55cf906a-2906-4570-babb-5d9391c8ebef	wamid.TEST_576ed3f8	whatsapp	t	\N	54	\N	2026-08-20 13:31:21.233037	2026-08-20 13:31:21.259092
8f8b6827-bd71-4a57-8f3c-5b6b1664ffb8	wamid.TEST_81b67e50	whatsapp	t	\N	48	\N	2026-08-21 05:44:23.296015	2026-08-21 05:44:23.31892
fa919757-9b4e-42a8-b00e-6ed1aaac7fe2	wamid.TEST_44a406ca	whatsapp	t	\N	52	\N	2026-08-20 13:31:21.297263	2026-08-20 13:31:21.322828
e89a95da-6f48-45c5-91d1-af438a86293f	wamid.TEST_d48c41b9	whatsapp	t	\N	11	\N	2026-08-20 13:31:21.328358	2026-08-20 13:31:21.337443
aa0fb46e-4716-4a94-97f9-92db743b0301	wamid.TEST_151f657b	whatsapp	t	\N	46	\N	2026-08-20 13:31:21.370846	2026-08-20 13:31:21.391815
5fc9d133-8206-40d3-8e6d-9929d8d7e6f4	wamid.TEST_8311144b	whatsapp	t	\N	10	\N	2026-08-20 13:31:21.395306	2026-08-20 13:31:21.405342
a58d22ca-fee8-43b4-a4a5-a75f73fa95ac	wamid.TEST_dfc0e22b	whatsapp	t	\N	46	\N	2026-08-20 13:31:21.438104	2026-08-20 13:31:21.459038
355251c8-e208-4b15-979e-508dff8e0ca6	wamid.TEST_98ee164e	whatsapp	t	\N	46	\N	2026-08-20 13:31:21.4906	2026-08-20 13:31:21.511953
8e4b8fd4-4fa6-4808-ba64-942d107d4e27	wamid.TEST_f9c4cb89	whatsapp	t	\N	42	\N	2026-08-21 05:51:03.690536	2026-08-21 05:51:03.710563
43f3ed68-649c-4eae-be95-1f008b8bfda8	wamid.TEST_4dc040a2	whatsapp	t	\N	9	\N	2026-08-20 13:31:21.515743	2026-08-20 13:31:21.524008
0ccc4780-00f2-4b60-b394-4d88342c8228	wamid.DEDUP_4af47168	whatsapp	t	\N	46	\N	2026-08-20 13:31:21.55571	2026-08-20 13:31:21.576636
e06319ac-ced9-49d2-8ce8-a28cd91c4864	wamid.TEST_d34cf7c4	whatsapp	t	\N	7	\N	2026-08-21 05:51:03.714485	2026-08-21 05:51:03.721482
04924dec-b252-41d6-897a-6070ec84059f	wamid.DEDUP_fa682f04	whatsapp	t	\N	42	\N	2026-08-21 05:51:03.935376	2026-08-21 05:51:03.954256
9c2d4d01-5348-4719-9525-f6ec7f6aaaf8	m_exact_test_c19f3f5f	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_c19f3f5f", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 05:52:01.442485	\N
aface1fa-806f-4c9e-ad12-bf7f3e81f332	wamid.TEST_3deb4074	whatsapp	t	\N	41	\N	2026-08-21 05:54:20.316282	2026-08-21 05:54:20.334429
b17483f7-8dd2-4f5c-8051-41b049979ff1	wamid.TEST_1dece700	whatsapp	t	\N	42	\N	2026-08-21 06:01:38.561336	2026-08-21 06:01:38.581243
f1fa86fc-1357-4374-a8a5-a8187e2b6c11	m_ws_broadcast_test_83621e18	instagram	t	\N	\N	{"sender": {"id": "23086741_d1ce"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_83621e18", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 13:31:32.446442	\N
59e19c79-bb8a-45e2-a72b-5cebab1c6e96	m_exact_test_a4c70b2d	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_a4c70b2d", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 13:31:32.889896	\N
eda70fc3-414b-46bc-a6dd-fdec156897fb	wamid.TEST_7b1aaf21	whatsapp	t	\N	7	\N	2026-08-21 06:01:38.584639	2026-08-21 06:01:38.59139
648ca503-9db4-4130-916f-5ec8a0f72467	wamid.TEST_2cdd5cb5	whatsapp	t	\N	51	\N	2026-08-20 13:32:34.454798	2026-08-20 13:32:34.481381
938b93cd-183b-4b3b-8e0f-acdf58ded337	wamid.TEST_f14983f7	whatsapp	t	\N	67	\N	2026-08-20 13:32:34.529669	2026-08-20 13:32:34.561267
96ec5322-5855-4470-aa4a-557bb686593e	wamid.DEDUP_84f659ef	whatsapp	t	\N	43	\N	2026-08-21 06:01:38.802614	2026-08-21 06:01:38.822538
87a90d5c-88f7-4ef1-9bac-ede673fb06ff	wamid.TEST_6c01e2bd	whatsapp	t	\N	8	\N	2026-08-20 13:32:34.573636	2026-08-20 13:32:34.580593
6f37c251-6805-4708-823c-6e519da2022c	wamid.TEST_2bf4262b	whatsapp	t	\N	45	\N	2026-08-20 13:32:34.613259	2026-08-20 13:32:34.635271
2d83f4b0-2f73-4336-b3d7-43201b0cd573	wamid.TEST_fcebd32b	whatsapp	t	\N	9	\N	2026-08-20 13:32:34.639167	2026-08-20 13:32:34.647966
c4abb983-c814-4489-8964-6a62e9bf015c	wamid.TEST_f88fd1e8	whatsapp	t	\N	58	\N	2026-08-20 13:32:34.683523	2026-08-20 13:32:34.713936
3d8464a4-9728-476d-8004-d85bf4a1c33e	m_exact_test_700bf218	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_700bf218", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 06:02:35.825751	\N
a39267e4-af52-4736-98f8-ffcb99da3f5c	wamid.TEST_0e07cf12	whatsapp	t	\N	59	\N	2026-08-20 13:32:34.752291	2026-08-20 13:32:34.782781
60510044-2c19-4a33-80fb-20f7c842695e	wamid.TEST_5dbf81d2	whatsapp	t	\N	8	\N	2026-08-20 13:32:34.786661	2026-08-20 13:32:34.794381
52da4cb7-214d-4982-99ac-6132c2fe6af5	wamid.TEST_fe0bf344	whatsapp	t	\N	53	\N	2026-08-21 06:07:40.140809	2026-08-21 06:07:40.166866
bacf3d0c-ea4d-4056-ac13-94d5c863fce2	wamid.DEDUP_2430640d	whatsapp	t	\N	44	\N	2026-08-20 13:32:34.82438	2026-08-20 13:32:34.84469
37c6b45e-cdaa-417e-9861-032d3470396b	m_ws_broadcast_test_7c4db05b	instagram	t	\N	\N	{"sender": {"id": "23086741_1f39"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_7c4db05b", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-20 13:32:45.750329	\N
0378fb1d-0e08-4c0a-afcb-1e99d57eb43b	m_exact_test_ffa9abcd	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_ffa9abcd", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-20 13:32:46.095606	\N
e6bc12ee-ef25-478a-abbc-8d61683e915e	wamid.TEST_d66d86fc	whatsapp	t	\N	55	\N	2026-08-25 12:37:21.865938	2026-08-25 12:37:21.894779
17312e92-27e8-47e4-8bee-40ca3b1d9416	wamid.TEST_9f3cef7e	whatsapp	t	\N	55	\N	2026-08-21 11:25:04.548124	2026-08-21 11:25:04.576261
53c041c6-d704-4f1f-bb6b-bf277f087444	wamid.TEST_495cb86c	whatsapp	t	\N	8	\N	2026-08-21 13:22:24.113241	2026-08-21 13:22:24.121211
1b986525-e0df-4ce2-ab12-4d9f8603f3b4	wamid.TEST_5d3652d2	whatsapp	t	\N	11	\N	2026-08-21 11:25:04.580855	2026-08-21 11:25:04.591148
79a8532a-14a2-4935-a2c5-f359a5fad0bf	wamid.TEST_c4facd6c	whatsapp	t	\N	48	\N	2026-08-24 05:20:21.874972	2026-08-24 05:20:21.897511
2c32a815-f61b-469d-8e7c-076b766bc7ff	wamid.DEDUP_9dc13d2d	whatsapp	t	\N	55	\N	2026-08-21 11:25:04.627612	2026-08-21 11:25:04.655659
75b96e6c-81cd-4771-a03a-3b915a14955f	wamid.TEST_9ffe2ac7	whatsapp	t	\N	43	\N	2026-08-21 13:22:24.204455	2026-08-21 13:22:24.224949
d4c3145e-ee06-46e2-add8-c641efbf4b57	wamid.TEST_85a03ce3	whatsapp	t	\N	9	\N	2026-08-21 13:22:24.229093	2026-08-21 13:22:24.236959
83498b71-4cb4-473d-bc54-c673f596bd62	wamid.TEST_ca089a1a	whatsapp	t	\N	9	\N	2026-08-24 05:20:21.901234	2026-08-24 05:20:21.909381
01c1756b-6a88-4dfc-baa2-611138e72854	wamid.TEST_9e95a38f	whatsapp	t	\N	53	\N	2026-08-24 05:20:22.05171	2026-08-24 05:20:22.081036
944d22e6-c6d2-437f-8943-6d6e053ea750	wamid.TEST_6efaa94a	whatsapp	t	\N	14	\N	2026-08-24 05:20:22.087935	2026-08-24 05:20:22.099165
f208bd04-9de1-4096-a1cb-a98ac990f7fb	m_ws_broadcast_test_d02c3040	instagram	t	\N	\N	{"sender": {"id": "23086741_98f4"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_d02c3040", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 11:26:03.799589	\N
2b8dd91a-78fd-44b3-abb0-817d667b1959	m_exact_test_1c672041	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_1c672041", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 11:26:04.183716	\N
45d3c63a-c618-4a74-841a-fef19c5447c2	wamid.TEST_dd73dc7c	whatsapp	t	\N	83	\N	2026-08-21 11:30:36.923783	2026-08-21 11:30:36.979023
85536394-7afb-4edb-8aa4-2dac8cf0a491	wamid.TEST_b2bddaa3	whatsapp	t	\N	84	\N	2026-08-21 11:30:37.022283	2026-08-21 11:30:37.074663
1d880a80-a453-48d3-8fb5-39d0de4e2572	m_ws_broadcast_test_80970c38	instagram	t	\N	\N	{"sender": {"id": "23086741_3618"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_80970c38", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 13:23:24.471136	\N
21bd88f8-6ef1-457e-939f-f77e6bd9f32d	wamid.TEST_1ef5c218	whatsapp	t	\N	27	\N	2026-08-21 11:30:37.079099	2026-08-21 11:30:37.105576
e68fb1be-48d4-406e-ad4f-34e3bc9127ea	wamid.TEST_13fc2f16	whatsapp	t	\N	67	\N	2026-08-21 11:30:37.154028	2026-08-21 11:30:37.189238
72129319-ae91-4a36-8dfd-75c9c917c740	wamid.TEST_4b04735e	whatsapp	t	\N	24	\N	2026-08-26 10:09:11.443253	2026-08-26 10:09:11.46479
82886093-e22e-4b99-bb2e-79385d62c0c0	m_exact_test_46dc5125	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_46dc5125", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 13:23:24.81954	\N
4578f861-e3ed-45c5-9f49-ec84b521d9e8	wamid.TEST_dd4a7f2d	whatsapp	t	\N	17	\N	2026-08-21 11:30:37.193588	2026-08-21 11:30:37.210186
bc12d04d-ab5b-4c18-927a-226c63814cee	wamid.TEST_a7635cdf	whatsapp	t	\N	52	\N	2026-08-21 13:27:29.10624	2026-08-21 13:27:29.134053
676519f1-33c3-40c5-81f0-fba8dfaf6851	wamid.TEST_5bacb3eb	whatsapp	t	\N	65	\N	2026-08-21 11:30:37.253762	2026-08-21 11:30:37.287943
ae438fa0-20f5-4787-a197-f69a281ecbda	wamid.TEST_56bdc2ea	whatsapp	t	\N	86	\N	2026-08-21 11:30:37.34863	2026-08-21 11:30:37.39053
807886c9-6a57-4679-bb8a-d6e1dcb12366	wamid.TEST_e8f7d519	whatsapp	t	\N	45	\N	2026-08-21 13:27:29.16795	2026-08-21 13:27:29.188632
98ef38ce-fcee-4da8-8bce-4ec0fda1aa5e	wamid.TEST_035f6d4d	whatsapp	t	\N	8	\N	2026-08-21 11:30:37.394901	2026-08-21 11:30:37.402135
d712f825-ed35-4879-809f-61f2bdadc02d	wamid.DEDUP_2a2038e4	whatsapp	t	\N	54	\N	2026-08-21 11:30:37.435226	2026-08-21 11:30:37.463492
e28c71df-7012-426e-9b15-979c5d3268c2	wamid.TEST_1739cb21	whatsapp	t	\N	8	\N	2026-08-21 13:27:29.192109	2026-08-21 13:27:29.200158
c1dca69b-3446-4819-861e-78dcfa7b798f	wamid.TEST_1b03647e	whatsapp	t	\N	43	\N	2026-08-21 13:27:29.231044	2026-08-21 13:27:29.250482
0e1af6e9-9f01-4340-8db1-b14d019b650a	wamid.TEST_8198c692	whatsapp	t	\N	8	\N	2026-08-21 13:27:29.253906	2026-08-21 13:27:29.261928
52c6d5b2-c4f0-4978-bb46-ee675837bac6	wamid.TEST_76a32f65	whatsapp	t	\N	43	\N	2026-08-21 13:27:29.292109	2026-08-21 13:27:29.312144
948c1e19-de9d-4600-af91-0b2b5d2c5125	wamid.TEST_de4e1644	whatsapp	t	\N	43	\N	2026-08-21 13:27:29.34203	2026-08-21 13:27:29.362395
b8dd4423-7b5f-46f1-b789-7db0bd62f8c4	wamid.TEST_6fc6d105	whatsapp	t	\N	8	\N	2026-08-21 13:27:29.366584	2026-08-21 13:27:29.373871
bfdcfe6c-3eb8-448a-affe-baba0c41c11b	wamid.DEDUP_05f928e6	whatsapp	t	\N	43	\N	2026-08-21 13:27:29.403413	2026-08-21 13:27:29.423942
4e682111-5690-4cfa-bc2a-aecf3adc1523	m_ws_broadcast_test_fb596fcb	instagram	t	\N	\N	{"sender": {"id": "23086741_35b0"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_fb596fcb", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 11:31:37.652178	\N
475925e3-31ae-4013-bd88-67140f734e8d	m_exact_test_99073128	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_99073128", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 11:31:38.018312	\N
571ea367-0dac-4a03-96da-861621dfd3bd	wamid.TEST_e10d916d	whatsapp	t	\N	52	\N	2026-08-21 12:24:03.368585	2026-08-21 12:24:03.396519
cb06317b-4023-4c24-9b76-7f514bef3dce	wamid.TEST_789df388	whatsapp	t	\N	51	\N	2026-08-21 12:24:03.43252	2026-08-21 12:24:03.457972
b90bf8b3-850c-403b-8aac-dda6bfd19974	wamid.TEST_d74bfbc7	whatsapp	t	\N	7	\N	2026-08-21 12:24:03.461496	2026-08-21 12:24:03.468438
a7ee3106-89c2-439e-91f3-26777c09e8ae	wamid.TEST_753454c4	whatsapp	t	\N	54	\N	2026-08-21 12:24:03.510152	2026-08-21 12:24:03.533138
e79b1d0e-9476-435f-ba31-0c8263436bd2	wamid.TEST_e2e3ddd5	whatsapp	t	\N	15	\N	2026-08-21 12:24:03.536653	2026-08-21 12:24:03.551264
11596ead-5ed9-4c01-b0bc-f9f87d014f9d	wamid.TEST_4bcc71fd	whatsapp	t	\N	46	\N	2026-08-21 12:24:03.583831	2026-08-21 12:24:03.60554
a2fb8886-8a64-4e3f-a9c6-53e9c2229215	wamid.TEST_cf349e2a	whatsapp	t	\N	49	\N	2026-08-21 12:24:03.638497	2026-08-21 12:24:03.662667
429533e9-8bdf-4223-9c51-a7885eb718fa	wamid.TEST_4bb5b0f6	whatsapp	t	\N	10	\N	2026-08-21 12:24:03.667189	2026-08-21 12:24:03.676851
55a06483-61a2-4568-9d1f-dcd4702ed090	wamid.DEDUP_94cebccc	whatsapp	t	\N	50	\N	2026-08-21 12:24:03.709661	2026-08-21 12:24:03.73363
946dc3a6-7bfc-463f-940a-a23b54e3ca9a	m_ws_broadcast_test_56ac39ac	instagram	t	\N	\N	{"sender": {"id": "23086741_2770"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_56ac39ac", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 12:25:05.343338	\N
35a5be9a-b315-49b5-9ad7-69550dbb0382	m_exact_test_0f65e2a4	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_0f65e2a4", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 12:25:05.89874	\N
423e3835-d2d8-4f70-939a-b64af13b6648	wamid.TEST_362727f7	whatsapp	t	\N	50	\N	2026-08-21 13:10:30.646985	2026-08-21 13:10:30.67277
38ed4771-407e-4947-971d-120400a90c3f	wamid.TEST_95318673	whatsapp	t	\N	46	\N	2026-08-21 13:10:30.705213	2026-08-21 13:10:30.727503
43bd8109-eb4a-4fa8-9741-03357a4a1f3e	wamid.TEST_19d567df	whatsapp	t	\N	7	\N	2026-08-21 13:10:30.731198	2026-08-21 13:10:30.738192
58e85ac2-caaa-4184-986f-4cc338e9eb3c	wamid.TEST_69f1ce68	whatsapp	t	\N	44	\N	2026-08-21 13:10:30.770002	2026-08-21 13:10:30.790149
2911fa6d-4875-4574-b8a6-6bb684d3e65e	wamid.TEST_8effecf6	whatsapp	t	\N	10	\N	2026-08-21 13:10:30.793712	2026-08-21 13:10:30.803167
9affa3eb-ebe9-4bcf-9f5b-b97d1b7d70bd	wamid.TEST_b3392d39	whatsapp	t	\N	46	\N	2026-08-21 13:10:30.835648	2026-08-21 13:10:30.857221
b9315938-3592-4ae8-97d8-06a1ed04f3b5	wamid.TEST_5daaa7c8	whatsapp	t	\N	49	\N	2026-08-21 13:10:30.888728	2026-08-21 13:10:30.912751
ac594be4-6e18-405d-b7ac-ddf8d02af74f	wamid.TEST_9b1648ff	whatsapp	t	\N	9	\N	2026-08-21 13:10:30.917711	2026-08-21 13:10:30.925477
b8239409-08c3-44dd-a6be-858bedd0ac40	wamid.DEDUP_5e197479	whatsapp	t	\N	47	\N	2026-08-21 13:10:30.956254	2026-08-21 13:10:30.978353
cda4b546-c276-4d3e-8057-e54447e82cf4	m_ws_broadcast_test_6b11d06e	instagram	t	\N	\N	{"sender": {"id": "23086741_eb5e"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_6b11d06e", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 13:11:31.566146	\N
8ac33e85-d79c-46c1-8ce9-3e3a8be46122	m_exact_test_24b00b87	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_24b00b87", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 13:11:31.924195	\N
de607817-fe64-4c32-ac44-dc0da474c37c	m_ws_broadcast_test_f8342d6e	instagram	t	\N	\N	{"sender": {"id": "23086741_064c"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f8342d6e", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 05:19:17.727809	\N
896d4db0-c6ad-4df7-b09e-798a125ab76b	wamid.TEST_1f68e1e3	whatsapp	t	\N	45	\N	2026-08-25 07:02:08.075009	2026-08-25 07:02:08.095951
f4f9c81e-29a1-4145-a34a-d2d6de019f53	wamid.TEST_bd76049a	whatsapp	t	\N	42	\N	2026-08-24 05:20:21.940586	2026-08-24 05:20:21.959611
a2eae1dd-5976-4c1a-8e58-8039d9130df6	wamid.TEST_95ad8741	whatsapp	t	\N	9	\N	2026-08-24 05:20:21.962814	2026-08-24 05:20:21.971128
557ae52c-e584-4e9b-b706-b4cb50651382	wamid.DEDUP_845ffd39	whatsapp	t	\N	41	\N	2026-08-24 05:20:22.128519	2026-08-24 05:20:22.146847
e71fa38b-fc16-4d16-83f2-4bbc3d59f53c	m_exact_test_96653756	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_96653756", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 05:21:30.904153	\N
cbdf44ed-71b3-48e8-8db1-e28654983201	wamid.TEST_d678afd8	whatsapp	t	\N	43	\N	2026-08-24 05:27:41.647149	2026-08-24 05:27:41.667107
e7f9477b-9727-4490-8739-d100740843be	wamid.TEST_ece657c0	whatsapp	t	\N	9	\N	2026-08-24 05:27:41.671066	2026-08-24 05:27:41.678998
4f06a16a-8a23-4987-b133-86d598a7ef10	wamid.TEST_ed12fb37	whatsapp	t	\N	42	\N	2026-08-24 05:27:41.779397	2026-08-24 05:27:41.798417
6450d2a8-1f81-4022-8e62-464fd208cd3b	wamid.DEDUP_2055f578	whatsapp	t	\N	56	\N	2026-08-24 05:27:41.888256	2026-08-24 05:27:41.919697
9bdcd503-8c2d-45a1-a537-9f1229c4114f	m_exact_test_5b7eb490	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_5b7eb490", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 05:28:54.033392	\N
192579a8-161c-406a-99c0-77db6e725317	wamid.TEST_a0f50b8d	whatsapp	t	\N	46	\N	2026-08-24 05:35:08.300381	2026-08-24 05:35:08.322375
ac018dca-4000-4b92-9e55-f9856f68469f	wamid.TEST_308e3dde	whatsapp	t	\N	8	\N	2026-08-24 05:35:08.326187	2026-08-24 05:35:08.334008
2f9d07fa-c17a-4555-91d9-b79bec804c90	wamid.TEST_6d1e2052	whatsapp	t	\N	46	\N	2026-08-24 05:35:08.434458	2026-08-24 05:35:08.456162
ececa070-6f5e-4c29-8dc4-7bcbcb039ff4	wamid.DEDUP_0e07c1ea	whatsapp	t	\N	46	\N	2026-08-24 05:35:08.552194	2026-08-24 05:35:08.574262
27280c2c-64f8-44df-be8c-657150386cea	m_exact_test_c040770f	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_c040770f", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 05:36:20.015513	\N
3a285eff-ad56-4494-94a3-965a4097f799	wamid.TEST_bdc4efc9	whatsapp	t	\N	44	\N	2026-08-24 05:43:12.890408	2026-08-24 05:43:12.911374
9d5a10d4-b55b-426d-b1c1-b78d67b7b427	wamid.TEST_8f61b9b5	whatsapp	t	\N	8	\N	2026-08-24 05:43:12.915751	2026-08-24 05:43:12.92304
953127e2-d893-4110-b446-efbb238491e3	wamid.TEST_13446d29	whatsapp	t	\N	47	\N	2026-08-24 05:43:13.021462	2026-08-24 05:43:13.044738
4ebc594b-5619-4a02-8d00-49d969e6a70d	wamid.DEDUP_92e12663	whatsapp	t	\N	45	\N	2026-08-24 05:43:13.136201	2026-08-24 05:43:13.157858
a8a6fac6-aa34-41fd-ba04-9afd725a7e82	m_exact_test_a46469a0	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_a46469a0", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 05:44:36.560574	\N
643d0403-b1dd-4ecd-b0e9-a5996defe3aa	wamid.TEST_bdfbb723	whatsapp	t	\N	46	\N	2026-08-24 06:27:37.769967	2026-08-24 06:27:37.791409
92b23826-f35d-4d21-ab12-ecac20b5e39e	wamid.TEST_0eee89c2	whatsapp	t	\N	8	\N	2026-08-24 06:27:37.794713	2026-08-24 06:27:37.801933
37c143b3-8520-4de7-87d5-57904cf4b3cc	wamid.TEST_19f3c551	whatsapp	t	\N	49	\N	2026-08-24 06:27:37.898576	2026-08-24 06:27:37.924048
20f160f1-7a34-4171-b494-34c7ee9d1c8e	wamid.DEDUP_a756039a	whatsapp	t	\N	46	\N	2026-08-24 06:27:38.02287	2026-08-24 06:27:38.045407
56c2b427-5e6c-4751-b223-412b6089c26a	m_exact_test_a3146b38	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_a3146b38", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 06:36:06.189032	\N
06e2d93c-7084-40c0-ba57-8cbf58ae1f7f	wamid.TEST_4e951914	whatsapp	t	\N	45	\N	2026-08-24 06:40:59.019422	2026-08-24 06:40:59.039729
6e153b1b-7f1e-4e4d-a54a-5a03f33f4cdd	wamid.TEST_7aba8cf1	whatsapp	t	\N	13	\N	2026-08-24 06:40:59.044015	2026-08-24 06:40:59.05625
092e00ed-4bc5-446d-ac45-7ca891ad10ee	wamid.TEST_6bb66408	whatsapp	t	\N	50	\N	2026-08-24 06:40:59.154225	2026-08-24 06:40:59.179768
31c26527-f352-4e36-9a01-0ee1e1b7526f	wamid.DEDUP_e3c7e62c	whatsapp	t	\N	47	\N	2026-08-24 06:40:59.276844	2026-08-24 06:40:59.297598
15713c2d-9259-4e50-bfdd-a4e374403d0b	m_ws_broadcast_test_85578854	instagram	t	\N	\N	{"sender": {"id": "23086741_f71c"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_85578854", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 06:49:25.771698	\N
73b4ba79-469a-4f93-afe3-71cca4cc9f56	m_exact_test_d1cbf70f	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_d1cbf70f", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 06:49:26.303231	\N
1df8c837-aafb-4767-8f4e-58caed1abbf1	wamid.TEST_a0d19bd8	whatsapp	t	\N	62	\N	2026-08-24 07:54:12.650528	2026-08-24 07:54:12.681721
52e8a298-4a8b-4597-a8ef-1e5b2444a227	wamid.TEST_3e5b23ac	whatsapp	t	\N	13	\N	2026-08-24 07:54:12.686947	2026-08-24 07:54:12.698436
18d637e8-1d59-4c16-aa42-86308f64533a	wamid.TEST_86cf7933	whatsapp	t	\N	87	\N	2026-08-24 07:54:12.861434	2026-08-24 07:54:12.911275
506fdedc-c70b-4333-800f-fdc425eb9764	wamid.TEST_04ae92e5	whatsapp	t	\N	60	\N	2026-08-24 07:54:12.956535	2026-08-24 07:54:12.979938
7e8d1099-7719-473e-bf45-0aa0e69eb3ee	wamid.TEST_fd23735c	whatsapp	t	\N	9	\N	2026-08-24 07:54:12.984948	2026-08-24 07:54:12.993123
6d324113-8135-41af-95bd-543c7d292dcf	wamid.DEDUP_be07b06c	whatsapp	t	\N	48	\N	2026-08-24 07:54:13.027131	2026-08-24 07:54:13.048814
a950b4ea-a61b-431c-8d4b-a13c5d1be84a	m_ws_broadcast_test_3e8c5bc8	instagram	t	\N	\N	{"sender": {"id": "23086741_2d98"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_3e8c5bc8", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 08:03:02.964168	\N
18463b93-5523-4efa-8050-ea0a0abb77e7	m_exact_test_ed9cc619	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_ed9cc619", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 08:03:03.302761	\N
dbe8e512-3fab-48e7-93bd-78269e300b0b	wamid.TEST_35536bb6	whatsapp	t	\N	53	\N	2026-08-24 08:56:21.361612	2026-08-24 08:56:21.387831
01863f9b-2965-4578-a17b-a81cab31f2f5	wamid.TEST_9fc99e01	whatsapp	t	\N	49	\N	2026-08-24 08:56:21.42392	2026-08-24 08:56:21.44617
515932f0-fe5c-4774-bd24-bb445c0343bb	wamid.TEST_c463d644	whatsapp	t	\N	11	\N	2026-08-24 08:56:21.450615	2026-08-24 08:56:21.460596
93dc42d5-17b1-4d10-ba8c-a553bb64dad4	wamid.TEST_b1b7f562	whatsapp	t	\N	55	\N	2026-08-24 08:56:21.498406	2026-08-24 08:56:21.526213
9163b59b-a0d3-4b8f-862e-08e8802a5f94	wamid.TEST_b40fa740	whatsapp	t	\N	11	\N	2026-08-24 08:56:21.531193	2026-08-24 08:56:21.541514
dd3fbec8-1ac1-4af9-b2d6-f401ca738b56	wamid.TEST_c497d770	whatsapp	t	\N	48	\N	2026-08-24 08:56:21.577474	2026-08-24 08:56:21.600969
5a45a0ad-c56e-4f58-afe7-b01c7c9d1f1e	wamid.TEST_930003cc	whatsapp	t	\N	46	\N	2026-08-24 08:56:21.632064	2026-08-24 08:56:21.653892
fc07015e-503f-47c2-9f9c-956ecb5154aa	wamid.TEST_44ba62fa	whatsapp	t	\N	10	\N	2026-08-24 08:56:21.658564	2026-08-24 08:56:21.668492
947feaf9-7786-46f9-b2b3-9911bb7fd55d	wamid.DEDUP_cf03aeb9	whatsapp	t	\N	51	\N	2026-08-24 08:56:21.700753	2026-08-24 08:56:21.725777
77111246-8b8d-493e-854c-88afecc471d4	m_ws_broadcast_test_421a07b8	instagram	t	\N	\N	{"sender": {"id": "23086741_b294"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_421a07b8", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 09:05:14.266301	\N
b374278e-b67b-486c-86b7-f045ac6b68a0	wamid.TEST_0eb91131	whatsapp	t	\N	54	\N	2026-08-25 06:33:46.97664	2026-08-25 06:33:47.004302
d7442653-7174-4972-a7e8-29d46749777d	wamid.TEST_670c1fc0	whatsapp	t	\N	45	\N	2026-08-25 06:33:47.037011	2026-08-25 06:33:47.058488
15476c7a-0a7f-4394-b08a-9b5a340d4fb6	wamid.TEST_7d502fc6	whatsapp	t	\N	8	\N	2026-08-25 06:33:47.062648	2026-08-25 06:33:47.069743
e94de9b6-c8e2-4e7f-b1d2-1239c56d135d	m_ws_broadcast_test_bcd13ea8	instagram	t	\N	\N	{"sender": {"id": "23086741_9551"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_bcd13ea8", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 13:28:33.819727	\N
ebdbf1fe-eea8-4d73-81d0-42735eca4ab7	m_exact_test_88b4c840	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_88b4c840", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 13:28:34.421969	\N
d3b2aa8b-e5ab-43be-99d7-ccf56943c85d	wamid.TEST_be07d357	whatsapp	t	\N	50	\N	2026-08-21 13:30:05.79035	2026-08-21 13:30:05.814379
f9b6bfd5-0037-4969-965d-4055445ab2e5	wamid.TEST_37eb61ef	whatsapp	t	\N	44	\N	2026-08-21 13:30:05.846927	2026-08-21 13:30:05.867009
3b08215c-124c-41d3-8bbc-0b62a3a43ff9	wamid.TEST_00a5fe71	whatsapp	t	\N	9	\N	2026-08-21 13:30:05.871155	2026-08-21 13:30:05.878873
638a3a47-1230-4845-a9c1-84d3d10f0782	wamid.TEST_45b13cfa	whatsapp	t	\N	44	\N	2026-08-21 13:30:05.909843	2026-08-21 13:30:05.930321
f4245c86-addb-4bdd-a453-cc71194dcf48	wamid.TEST_b80dbdf4	whatsapp	t	\N	10	\N	2026-08-21 13:30:05.933723	2026-08-21 13:30:05.942993
1e81765c-03ff-4ebb-b2ad-3992167c3781	wamid.TEST_b8a8eabe	whatsapp	t	\N	45	\N	2026-08-21 13:30:05.97467	2026-08-21 13:30:05.995061
7866ce95-a980-4a11-b18e-8ef67bf58866	wamid.TEST_ddd42370	whatsapp	t	\N	45	\N	2026-08-21 13:30:06.025399	2026-08-21 13:30:06.045915
092f705d-c844-4a08-a3fb-dbe9e91a9822	wamid.TEST_8c240d3f	whatsapp	t	\N	8	\N	2026-08-21 13:30:06.049227	2026-08-21 13:30:06.056593
054e0f37-ceda-4c72-ab5c-fe4960fa65cc	wamid.DEDUP_688d27f3	whatsapp	t	\N	44	\N	2026-08-21 13:30:06.085591	2026-08-21 13:30:06.107074
94e24787-4ec3-4888-838c-4b7c586b6711	m_ws_broadcast_test_def05d56	instagram	t	\N	\N	{"sender": {"id": "23086741_9316"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_def05d56", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 13:31:10.179335	\N
bcb6be60-1f69-4fbd-a7c3-8ad17c8436f3	m_exact_test_195097ec	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_195097ec", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 13:31:10.550385	\N
c34bb49d-a6d3-43ed-b2d8-367d1948dbc1	wamid.TEST_b19d2fae	whatsapp	t	\N	48	\N	2026-08-21 13:32:49.839491	2026-08-21 13:32:49.863411
b93f54ff-d092-44f8-95f8-81f3c75818b3	wamid.TEST_f9532674	whatsapp	t	\N	44	\N	2026-08-21 13:32:49.89575	2026-08-21 13:32:49.916224
555e049c-6be0-4571-aff2-0f1e09de7465	wamid.TEST_4088ff64	whatsapp	t	\N	8	\N	2026-08-21 13:32:49.920044	2026-08-21 13:32:49.927353
3eac5b28-8309-4756-805f-a654404683a2	wamid.TEST_2a6b5509	whatsapp	t	\N	45	\N	2026-08-21 13:32:49.959595	2026-08-21 13:32:49.980066
b35b6a9d-fc57-4026-82ea-df923b54be75	wamid.TEST_5ceef04f	whatsapp	t	\N	8	\N	2026-08-21 13:32:49.9837	2026-08-21 13:32:49.991341
8961f2ef-b462-4b19-9302-21221bd90af8	wamid.TEST_3624718b	whatsapp	t	\N	43	\N	2026-08-21 13:32:50.02231	2026-08-21 13:32:50.042306
69a1aff2-5881-4fe9-9f68-cccbcd815d6c	wamid.TEST_56c5c238	whatsapp	t	\N	44	\N	2026-08-21 13:32:50.072488	2026-08-21 13:32:50.092912
1682b8f5-0382-4ae7-898e-2f60f6987d5b	wamid.TEST_e67a5dc8	whatsapp	t	\N	8	\N	2026-08-21 13:32:50.096899	2026-08-21 13:32:50.104095
3ee386ba-8421-4b4a-8c34-2704f9453eb4	wamid.DEDUP_19ada90b	whatsapp	t	\N	49	\N	2026-08-21 13:32:50.136064	2026-08-21 13:32:50.159652
faccdb60-7448-4d9d-b639-cce36401374b	wamid.TEST_8894df07	whatsapp	t	\N	135	\N	2026-08-26 12:30:37.106449	2026-08-26 12:30:37.167098
044a8912-b7d4-44ef-86bc-4d9ec0ac50a5	wamid.TEST_12bef6d3	whatsapp	t	\N	132	\N	2026-08-26 10:09:11.579561	2026-08-26 10:09:11.628518
0acf680c-59ce-4715-b95e-3d05df5d072a	m_ws_broadcast_test_a876e398	instagram	t	\N	\N	{"sender": {"id": "23086741_f4e6"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a876e398", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 13:33:54.492004	\N
c4921567-1f6b-4732-a765-99e141d16c01	m_exact_test_4deb6d29	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_4deb6d29", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 13:33:54.846788	\N
f2ac4d94-2ec6-46bd-8340-d6ae3f45ebdb	wamid.TEST_a9efc0fe	whatsapp	t	\N	46	\N	2026-08-21 13:35:40.240817	2026-08-21 13:35:40.262786
e8505498-484a-41d3-b410-8e83e247f96b	wamid.TEST_781b09bf	whatsapp	t	\N	42	\N	2026-08-21 13:35:40.293798	2026-08-21 13:35:40.313041
dee920a9-d258-4497-8f3b-8d61aa54307e	wamid.TEST_a2f165c1	whatsapp	t	\N	8	\N	2026-08-21 13:35:40.31636	2026-08-21 13:35:40.323564
a56c8956-6e5b-4c61-a653-f9d5acee16ea	wamid.TEST_8e5c91ab	whatsapp	t	\N	42	\N	2026-08-21 13:35:40.353484	2026-08-21 13:35:40.373506
1802d07e-ba4e-4479-acbc-0bcec27a21e6	wamid.TEST_26cd4d77	whatsapp	t	\N	8	\N	2026-08-21 13:35:40.376979	2026-08-21 13:35:40.384497
cd385707-80c2-4286-9c8f-218d3d0ad493	wamid.TEST_a2dfc263	whatsapp	t	\N	41	\N	2026-08-21 13:35:40.414485	2026-08-21 13:35:40.43326
0051e8d2-6cf7-4361-9a2e-7dcb70079379	wamid.TEST_0bbfbdd3	whatsapp	t	\N	45	\N	2026-08-21 13:35:40.463294	2026-08-21 13:35:40.484148
e26dcaab-b747-4d0c-b65d-52d8f444af17	wamid.TEST_8a1460e9	whatsapp	t	\N	11	\N	2026-08-21 13:35:40.487881	2026-08-21 13:35:40.498171
6582a7f0-7fd4-4b66-bd35-d94e02896f44	wamid.DEDUP_69d209c5	whatsapp	t	\N	44	\N	2026-08-21 13:35:40.529173	2026-08-21 13:35:40.549047
be9f45f4-241b-49d6-bc42-653e461d8a0d	m_ws_broadcast_test_fecf0976	instagram	t	\N	\N	{"sender": {"id": "23086741_035b"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_fecf0976", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 13:36:45.567559	\N
fea49f07-08ba-4396-ab62-6ad731b4d3b2	m_exact_test_c45d2295	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_c45d2295", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 13:36:45.928324	\N
c20acfb9-c655-4313-8011-2edca06a9ec4	wamid.TEST_710b0231	whatsapp	t	\N	46	\N	2026-08-21 13:42:07.017381	2026-08-21 13:42:07.039489
80fd03d8-80e4-4e1d-ba44-22f2cae0b5c5	wamid.TEST_1f050cf8	whatsapp	t	\N	42	\N	2026-08-21 13:42:07.070949	2026-08-21 13:42:07.089818
00480fc0-6981-4ce1-bee9-c0ffcd23b38e	wamid.TEST_d42f9aaf	whatsapp	t	\N	7	\N	2026-08-21 13:42:07.093595	2026-08-21 13:42:07.100239
6fac327e-a08f-4ddd-8d35-485bb0b338a9	wamid.TEST_d62ff3bd	whatsapp	t	\N	45	\N	2026-08-21 13:42:07.131411	2026-08-21 13:42:07.153223
f8aca9bc-0028-46e2-aa74-d9267bca48e4	wamid.TEST_a753442f	whatsapp	t	\N	9	\N	2026-08-21 13:42:07.157514	2026-08-21 13:42:07.166214
46d9e1f9-5378-47c3-bfa1-a89d11775580	wamid.TEST_6e9c2595	whatsapp	t	\N	43	\N	2026-08-21 13:42:07.197732	2026-08-21 13:42:07.217072
5f626f58-ae5e-4530-bfcb-067cc4fcd82a	wamid.TEST_32c523b6	whatsapp	t	\N	43	\N	2026-08-21 13:42:07.246818	2026-08-21 13:42:07.267004
ed7493ff-592d-44cf-a9af-5261539e0060	wamid.TEST_0dfee8a6	whatsapp	t	\N	10	\N	2026-08-21 13:42:07.271375	2026-08-21 13:42:07.279758
bc077dec-cc9f-496a-8433-60e38414e047	wamid.DEDUP_0cd0723f	whatsapp	t	\N	48	\N	2026-08-21 13:42:07.311783	2026-08-21 13:42:07.333914
e879d42f-7546-4f2f-a4d7-71f79ac76110	m_ws_broadcast_test_3b96645e	instagram	t	\N	\N	{"sender": {"id": "23086741_042f"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_3b96645e", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 13:43:12.054105	\N
393282a2-41a6-49cb-8c93-251509d56546	m_exact_test_6fffc7d1	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_6fffc7d1", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 13:43:12.418201	\N
4c9e83b3-d6ae-4802-ae95-d048c7431bb3	wamid.TEST_57467e52	whatsapp	t	\N	46	\N	2026-08-21 13:45:50.19705	2026-08-21 13:45:50.219703
488c83d7-cf0b-4c4e-b2cc-f8b63c2cbf77	wamid.TEST_4dbdf822	whatsapp	t	\N	42	\N	2026-08-21 13:45:50.25086	2026-08-21 13:45:50.270561
010e3194-d54a-438a-aa62-4fd3896ba776	wamid.TEST_8d1f1315	whatsapp	t	\N	7	\N	2026-08-21 13:45:50.274129	2026-08-21 13:45:50.280887
405b7a60-df44-46bf-a948-03b19b0589e4	wamid.TEST_57f1d9e3	whatsapp	t	\N	43	\N	2026-08-21 13:45:50.311784	2026-08-21 13:45:50.331608
1b40d86d-09b8-44a1-b52d-898537722aae	wamid.TEST_119b57b4	whatsapp	t	\N	9	\N	2026-08-21 13:45:50.33483	2026-08-21 13:45:50.343332
69259992-8759-4c48-a0ab-69eaa7be1f2a	wamid.TEST_fc574723	whatsapp	t	\N	42	\N	2026-08-21 13:45:50.373613	2026-08-21 13:45:50.392844
6cb1965f-c9e1-4845-91f3-bb28353fc15f	wamid.TEST_c599f1db	whatsapp	t	\N	44	\N	2026-08-21 13:45:50.422628	2026-08-21 13:45:50.442885
d01ef513-ae3a-410b-ab6a-f06f20ae40ce	wamid.TEST_8471ba5a	whatsapp	t	\N	7	\N	2026-08-21 13:45:50.44609	2026-08-21 13:45:50.453172
5f9d168c-b89b-4f0d-8aa7-a871bf7ff698	wamid.DEDUP_2217555d	whatsapp	t	\N	42	\N	2026-08-21 13:45:50.482115	2026-08-21 13:45:50.501841
b4bdefc8-2f63-464c-9356-02c7226fb9f1	m_exact_test_1d3de003	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_1d3de003", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 05:19:18.096589	\N
565f48f5-6646-4bf9-ace2-8fe383f5ba3a	wamid.TEST_87a66b99	whatsapp	t	\N	43	\N	2026-08-24 05:20:22.001355	2026-08-24 05:20:22.021896
bf574471-7e87-42ea-a23a-c3087026daa7	m_ws_broadcast_test_f6166cfb	instagram	t	\N	\N	{"sender": {"id": "23086741_2bc8"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f6166cfb", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 05:21:30.536058	\N
475f6e99-6a77-4cd9-a687-2ee1ead4b1be	wamid.TEST_4399dcd5	whatsapp	t	\N	56	\N	2026-08-24 05:27:41.58412	2026-08-24 05:27:41.614723
495c1cbd-5b27-4d84-ab78-f65849821e6a	m_ws_broadcast_test_fe9d00f6	instagram	t	\N	\N	{"sender": {"id": "23086741_88ba"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_fe9d00f6", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-21 13:46:59.034675	\N
85460fa5-0cf1-45fd-bad2-866088eb7e69	m_exact_test_9caef0ea	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_9caef0ea", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-21 13:46:59.375112	\N
57e334f2-fce9-4e2a-b99e-6482e0f3df69	wamid.TEST_2d80a5cf	whatsapp	t	\N	47	\N	2026-08-24 05:27:41.709451	2026-08-24 05:27:41.734279
31e3cf24-3024-4d74-a50c-2ae7353459d2	wamid.TEST_68e4d17e	whatsapp	t	\N	51	\N	2026-08-24 05:15:42.970306	2026-08-24 05:15:42.995164
b98bdab9-b80e-4b78-985b-4caeac786c1a	wamid.TEST_819960d9	whatsapp	t	\N	43	\N	2026-08-24 05:15:43.02715	2026-08-24 05:15:43.047074
520185f1-cc8a-4b6e-8eee-dae38a795736	wamid.TEST_4932f5bb	whatsapp	t	\N	10	\N	2026-08-24 05:27:41.738444	2026-08-24 05:27:41.747808
f2c11366-4ec7-4ca2-a24a-62629ca771f4	wamid.TEST_d583017e	whatsapp	t	\N	8	\N	2026-08-24 05:15:43.050936	2026-08-24 05:15:43.057901
d6ca483b-e87f-4cc8-9851-88acd456ab72	wamid.TEST_70944866	whatsapp	t	\N	42	\N	2026-08-24 05:15:43.087865	2026-08-24 05:15:43.106959
ca207774-b3f6-42da-85e9-8651d26e58cd	wamid.TEST_f09aa24e	whatsapp	t	\N	43	\N	2026-08-24 05:27:41.827935	2026-08-24 05:27:41.847279
8c4dc818-9668-4da0-869a-6139f4844d94	wamid.TEST_c11f4aa6	whatsapp	t	\N	8	\N	2026-08-24 05:15:43.110497	2026-08-24 05:15:43.117959
aab9b2f1-6bf2-42cb-aab6-87beaff69dda	wamid.TEST_66d7001b	whatsapp	t	\N	44	\N	2026-08-24 05:15:43.148345	2026-08-24 05:15:43.168971
dd8af2ac-d634-4fcd-888b-e7d5ac8de38a	wamid.TEST_bdb99b3b	whatsapp	t	\N	8	\N	2026-08-24 05:27:41.850927	2026-08-24 05:27:41.85796
4da5f6d8-e939-4743-b834-2a3ef5a7442c	wamid.TEST_597661d4	whatsapp	t	\N	45	\N	2026-08-24 05:15:43.200672	2026-08-24 05:15:43.221598
dfe10377-80a8-4331-90fb-30e550e5fdc0	wamid.TEST_86a47c22	whatsapp	t	\N	7	\N	2026-08-24 05:15:43.225089	2026-08-24 05:15:43.23178
eebca225-ae94-4ad3-8e1d-c6789487058b	wamid.DEDUP_f8d331f5	whatsapp	t	\N	42	\N	2026-08-24 05:15:43.260561	2026-08-24 05:15:43.280535
edef2ff3-bb40-4396-8d84-c4b67005d21b	m_ws_broadcast_test_35d4e65c	instagram	t	\N	\N	{"sender": {"id": "23086741_d76a"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_35d4e65c", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 05:28:53.644352	\N
4c94073c-dc08-4ea1-89b5-b901d4fdda14	wamid.TEST_38d7730a	whatsapp	t	\N	59	\N	2026-08-24 05:35:08.234604	2026-08-24 05:35:08.266834
ce93f8fd-edee-4e95-9900-6618f43bb018	wamid.TEST_9c0615b6	whatsapp	t	\N	45	\N	2026-08-24 05:35:08.365506	2026-08-24 05:35:08.386687
09f982a0-f1c1-45c4-a973-8ed8c0305598	wamid.TEST_3b790117	whatsapp	t	\N	13	\N	2026-08-24 05:35:08.390527	2026-08-24 05:35:08.402519
7ad45a99-9097-4e12-8a57-e74370545975	wamid.TEST_069fbfe6	whatsapp	t	\N	137	\N	2026-09-01 09:06:11.283536	2026-09-01 09:06:11.337249
e61c31c9-884e-4061-9a7a-bec33736efd5	wamid.TEST_5f64b34a	whatsapp	t	\N	22	\N	2026-08-26 10:09:11.634148	2026-08-26 10:09:11.653459
68a1fbf1-9ac5-4b41-a8f6-525636f19573	m_ws_broadcast_test_fb3e76e5	instagram	t	\N	\N	{"sender": {"id": "23086741_6d9d"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_fb3e76e5", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 05:16:53.123644	\N
de6ae294-0dbf-4e3b-854b-669e23fb0c06	wamid.TEST_50043a54	whatsapp	t	\N	45	\N	2026-08-24 05:35:08.486527	2026-08-24 05:35:08.507444
d64f526f-dd96-46ef-a72d-1fb1d5bbdf5c	m_exact_test_ca1a6570	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_ca1a6570", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 05:16:53.487009	\N
651718cc-97aa-4f1b-a826-fca871044b94	wamid.TEST_408bc69a	whatsapp	t	\N	48	\N	2026-08-24 05:18:08.390378	2026-08-24 05:18:08.412879
96a9151b-9c14-4a88-8749-8413d757c53e	wamid.TEST_14c00a6c	whatsapp	t	\N	11	\N	2026-08-24 05:35:08.511472	2026-08-24 05:35:08.52188
0b50019a-b286-40ea-bfad-806b6e42f5fd	wamid.TEST_f1a89ee0	whatsapp	t	\N	42	\N	2026-08-24 05:18:08.444388	2026-08-24 05:18:08.463187
e39ed3e0-97a9-4ed4-b4e5-2b36b3993d15	wamid.TEST_8e7803f4	whatsapp	t	\N	8	\N	2026-08-24 05:18:08.46674	2026-08-24 05:18:08.474229
6704f216-4f24-4e91-aefa-da00f6ea2119	wamid.TEST_8965f0b5	whatsapp	t	\N	43	\N	2026-08-24 05:18:08.504454	2026-08-24 05:18:08.524013
a7de455a-f65f-4f76-b200-b430bacedf73	wamid.TEST_f31c1e77	whatsapp	t	\N	8	\N	2026-08-24 05:18:08.527522	2026-08-24 05:18:08.535037
9c55471c-bd64-433f-b1fb-3b06d161cb2a	wamid.TEST_97204de2	whatsapp	t	\N	42	\N	2026-08-24 05:18:08.565609	2026-08-24 05:18:08.585162
ae5c0afe-7dc8-4cc8-a97f-81fbedc66043	wamid.TEST_e3fa54b4	whatsapp	t	\N	44	\N	2026-08-24 05:18:08.6163	2026-08-24 05:18:08.635751
bdd1135f-f7e1-4195-93ad-a48e83e0630c	wamid.TEST_86854fb3	whatsapp	t	\N	7	\N	2026-08-24 05:18:08.64005	2026-08-24 05:18:08.646869
96d4c934-b2c2-406a-87b6-08a41106eeb2	wamid.DEDUP_d3b0b0a0	whatsapp	t	\N	44	\N	2026-08-24 05:18:08.678602	2026-08-24 05:18:08.697282
845be548-3b23-4ab1-9a95-b89aa1cbbe8e	m_ws_broadcast_test_598d3565	instagram	t	\N	\N	{"sender": {"id": "23086741_86d1"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_598d3565", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 05:36:19.629061	\N
20827f13-8f31-4a9d-acd8-0938df6985af	wamid.TEST_ebc911e0	whatsapp	t	\N	57	\N	2026-08-24 05:43:12.827049	2026-08-24 05:43:12.857844
9a81c735-cf84-4712-b019-a2974d822adc	wamid.TEST_69297c06	whatsapp	t	\N	45	\N	2026-08-24 05:43:12.955153	2026-08-24 05:43:12.976765
738042e2-d2ae-434e-ae1a-f8881b5c82fd	wamid.TEST_1c4f07d4	whatsapp	t	\N	8	\N	2026-08-24 05:43:12.981307	2026-08-24 05:43:12.989113
44f3d345-52fc-444e-9148-01ed82843154	wamid.TEST_87ba117c	whatsapp	t	\N	45	\N	2026-08-24 05:43:13.075194	2026-08-24 05:43:13.096171
1f3d075a-f2ac-45c1-a8f5-56fbe4afde04	wamid.TEST_6d0707d5	whatsapp	t	\N	7	\N	2026-08-24 05:43:13.099655	2026-08-24 05:43:13.106057
418a4bdc-c886-4e3d-b2f7-c9dc0cc0ec57	m_ws_broadcast_test_a1851050	instagram	t	\N	\N	{"sender": {"id": "23086741_880f"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a1851050", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 05:44:36.199296	\N
d4f22325-1538-4e1c-ae1f-ce8ccab20176	wamid.TEST_d45df382	whatsapp	t	\N	53	\N	2026-08-24 06:27:37.707574	2026-08-24 06:27:37.735838
b38ea2ce-73c6-4812-bd59-fbd35d05d093	wamid.TEST_7b53f697	whatsapp	t	\N	47	\N	2026-08-24 06:27:37.833342	2026-08-24 06:27:37.856254
d320a9cd-7eca-475e-a5a9-655a807f5d49	wamid.TEST_97db7090	whatsapp	t	\N	8	\N	2026-08-24 06:27:37.859412	2026-08-24 06:27:37.867002
97ba59e7-797c-426b-80e9-8d70a483dea8	wamid.TEST_467f7c71	whatsapp	t	\N	50	\N	2026-08-24 06:27:37.95781	2026-08-24 06:27:37.98088
e9b97d4f-56c8-440d-836e-41d9694b55b3	wamid.TEST_0103d908	whatsapp	t	\N	9	\N	2026-08-24 06:27:37.985316	2026-08-24 06:27:37.992935
24349e28-e1be-4d23-8437-533ad5b34138	m_ws_broadcast_test_2ccff040	instagram	t	\N	\N	{"sender": {"id": "23086741_479a"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_2ccff040", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-24 06:36:05.717729	\N
49deaf36-cb11-4b00-a54e-72de41c75341	wamid.TEST_70502155	whatsapp	t	\N	60	\N	2026-08-24 06:40:58.958104	2026-08-24 06:40:58.98592
3f5f1572-1409-45b9-8dc6-c7d137ebe3d3	wamid.TEST_40b28a1d	whatsapp	t	\N	45	\N	2026-08-24 06:40:59.088394	2026-08-24 06:40:59.109683
bfcfa823-2c1e-433e-8a9b-57851818ad73	wamid.TEST_e16d0abd	whatsapp	t	\N	9	\N	2026-08-24 06:40:59.113437	2026-08-24 06:40:59.122117
f5aab3dc-3071-4530-8685-bacda5bec55a	wamid.TEST_1d7c9c42	whatsapp	t	\N	45	\N	2026-08-24 06:40:59.211513	2026-08-24 06:40:59.231997
671676e1-6cee-4a1b-b706-a3623c80c9d0	wamid.TEST_63ba5e05	whatsapp	t	\N	8	\N	2026-08-24 06:40:59.236322	2026-08-24 06:40:59.244264
2a14aa38-01db-48ec-b40d-fccce0a736a4	wamid.TEST_2fed8290	whatsapp	t	\N	55	\N	2026-08-24 07:54:12.583764	2026-08-24 07:54:12.609141
fdb4c3fd-b77b-41b2-ac1a-51d1d8fd6e19	wamid.TEST_594dfd1c	whatsapp	t	\N	85	\N	2026-08-24 07:54:12.754865	2026-08-24 07:54:12.796302
8974631c-a365-41dc-87c2-4c8f3aa3af50	wamid.TEST_dab85c21	whatsapp	t	\N	13	\N	2026-08-24 07:54:12.801094	2026-08-24 07:54:12.813574
2e9e09d5-e3cc-4e63-a97b-55d5f4d02731	wamid.TEST_998375f7	whatsapp	t	\N	51	\N	2026-08-25 12:37:21.931474	2026-08-25 12:37:21.956061
be93c431-ff92-474e-9479-e2b265910cda	m_exact_test_714a9eea	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_714a9eea", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-24 09:05:14.663343	\N
c964d1a2-ed66-4e02-8822-a82d3308e7e3	m_ws_broadcast_test_d9f5123d	instagram	t	\N	\N	{"sender": {"id": "23086741_ad20"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_d9f5123d", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 07:01:04.247634	\N
12814389-9be8-40ab-ae7b-74b7d99497a9	wamid.TEST_0a02612d	whatsapp	t	\N	8	\N	2026-08-25 07:02:08.099781	2026-08-25 07:02:08.107604
f248021e-68ee-420d-bd16-451fbb63f0d4	wamid.TEST_348a330e	whatsapp	t	\N	56	\N	2026-08-25 07:02:08.214497	2026-08-25 07:02:08.247303
b68d476f-7335-4fe1-83cc-f86af37b238b	wamid.DEDUP_f25afb1c	whatsapp	t	\N	51	\N	2026-08-25 07:02:08.350578	2026-08-25 07:02:08.374989
d6bb16d8-f032-4170-a57c-847388678741	m_exact_test_5f6230f4	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_5f6230f4", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 07:10:47.056697	\N
8dc0eec7-2159-4174-91de-0f9e67d95fba	wamid.TEST_a17c4b50	whatsapp	t	\N	45	\N	2026-08-25 08:17:16.278089	2026-08-25 08:17:16.29872
6ef4c7c0-cb7c-4069-ae3d-0b94d4ecbb1c	wamid.TEST_c4dc50cb	whatsapp	t	\N	8	\N	2026-08-25 08:17:16.302529	2026-08-25 08:17:16.309695
e8444664-bb22-498d-90ac-af3765a6734b	wamid.TEST_91262b21	whatsapp	t	\N	43	\N	2026-08-25 08:17:16.404297	2026-08-25 08:17:16.424231
4a38e45c-a221-45e7-a880-ae9cb60250a9	wamid.DEDUP_2fdb1674	whatsapp	t	\N	46	\N	2026-08-25 08:17:16.516287	2026-08-25 08:17:16.539099
fa36eb62-d794-47e3-9ea9-dc90cbe5d1e9	m_exact_test_47e2dead	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_47e2dead", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 08:25:55.966672	\N
6174175b-d54e-4c26-9f9a-29ef6e9651bc	wamid.TEST_1051918b	whatsapp	t	\N	48	\N	2026-08-25 08:27:50.054689	2026-08-25 08:27:50.076511
6e141bbb-4f8c-4cc1-96a3-cabbc9b207b6	wamid.DEDUP_c03ce5b7	whatsapp	t	\N	46	\N	2026-08-25 08:27:50.19246	2026-08-25 08:27:50.212636
c1573348-c288-4c90-aa68-28ac446706f8	m_exact_test_96c4e37a	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_96c4e37a", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 08:36:32.022124	\N
bcdbe3fc-b1e8-4285-a91d-90496d94ce1f	wamid.TEST_14bf3089	whatsapp	t	\N	50	\N	2026-08-25 08:38:14.921039	2026-08-25 08:38:14.945304
d4da3dae-401a-40a3-a70f-dc33791e8a96	wamid.TEST_a60543d2	whatsapp	t	\N	46	\N	2026-08-25 08:38:15.046473	2026-08-25 08:38:15.068717
0b256563-85f2-4bc6-b5e3-1aa9e1176b01	wamid.TEST_cf39201f	whatsapp	t	\N	9	\N	2026-08-25 08:38:15.073021	2026-08-25 08:38:15.081487
4d132eb4-0091-40d8-8354-cae4ace44235	wamid.TEST_6f6729b2	whatsapp	t	\N	45	\N	2026-08-25 08:38:15.200092	2026-08-25 08:38:15.220256
b2fd2bcf-51dc-401a-b8a8-8e7403925fc1	wamid.TEST_70278447	whatsapp	t	\N	8	\N	2026-08-25 08:38:15.224625	2026-08-25 08:38:15.23177
d669f2bc-4baf-4cb1-bbf0-f0b7e85ca30d	m_ws_broadcast_test_ebdc8ad3	instagram	t	\N	\N	{"sender": {"id": "23086741_8bb1"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_ebdc8ad3", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 08:46:53.628046	\N
cd61ce46-8bc1-4b07-9d07-e72f9b81e506	wamid.TEST_4961db5d	whatsapp	t	\N	72	\N	2026-08-25 10:00:18.462649	2026-08-25 10:00:18.495658
78e44452-6307-432e-a228-ddf0f5405d58	wamid.TEST_e6f60242	whatsapp	t	\N	44	\N	2026-08-25 10:00:18.594841	2026-08-25 10:00:18.614744
df3ae597-e70c-49c3-9f6d-60b9bb85b8e6	wamid.TEST_98142a7e	whatsapp	t	\N	9	\N	2026-08-25 10:00:18.61834	2026-08-25 10:00:18.626833
feacfc11-cf4e-42c6-8734-85fc43f13a39	wamid.TEST_61ffc106	whatsapp	t	\N	42	\N	2026-08-25 10:00:18.706731	2026-08-25 10:00:18.725856
52ae9335-c19a-4738-88f4-f5135b968bac	wamid.TEST_1bab0579	whatsapp	t	\N	8	\N	2026-08-25 10:00:18.730366	2026-08-25 10:00:18.737784
16a5a35c-2add-41d7-8fff-236847e540d7	m_ws_broadcast_test_a182635d	instagram	t	\N	\N	{"sender": {"id": "23086741_5411"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a182635d", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 10:08:56.95103	\N
13880145-4b53-4f2f-8a51-31ad1d8b3752	wamid.TEST_0b90ebb7	whatsapp	t	\N	54	\N	2026-08-25 10:25:47.163514	2026-08-25 10:25:47.19108
16058d87-b1ba-4197-b34e-fcdebca9406b	wamid.TEST_aa0cb21f	whatsapp	t	\N	44	\N	2026-08-25 10:25:47.297107	2026-08-25 10:25:47.317815
1e117947-f7a4-48d8-8037-901153c674d9	wamid.TEST_ac0b0ef6	whatsapp	t	\N	8	\N	2026-08-25 10:25:47.321515	2026-08-25 10:25:47.329441
9e9b66cb-974b-41d1-80ce-9a6bc05d2fe2	wamid.TEST_59779f2e	whatsapp	t	\N	61	\N	2026-08-25 10:25:47.428828	2026-08-25 10:25:47.455217
3469566f-42bf-4b69-bc93-bc107d43aa9d	wamid.TEST_f8b55287	whatsapp	t	\N	9	\N	2026-08-25 10:25:47.460679	2026-08-25 10:25:47.469016
c81b827c-1e83-4ab1-a974-04d4dbf9766e	m_ws_broadcast_test_59f8b6a7	instagram	t	\N	\N	{"sender": {"id": "23086741_902f"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_59f8b6a7", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 10:34:26.908277	\N
62d7c524-90d9-46f3-ba79-b5428ff34967	wamid.TEST_c9a69a3c	whatsapp	t	\N	52	\N	2026-08-25 11:47:39.631981	2026-08-25 11:47:39.659207
c4e4a315-b86e-468e-908c-92627046c45b	wamid.TEST_fbbf5123	whatsapp	t	\N	47	\N	2026-08-25 11:47:39.764593	2026-08-25 11:47:39.7877
3aa5d8b7-0a9b-41b0-bbf9-f7f40e70b803	wamid.TEST_78a2f0b9	whatsapp	t	\N	9	\N	2026-08-25 11:47:39.791792	2026-08-25 11:47:39.800567
170ac2b4-48c1-428b-8057-7ea0a7c77470	wamid.TEST_b98180ff	whatsapp	t	\N	47	\N	2026-08-25 11:47:39.900009	2026-08-25 11:47:39.921635
5aea1c16-99c6-4798-8f98-a2545444e1db	wamid.TEST_6f5a4efe	whatsapp	t	\N	7	\N	2026-08-25 11:47:39.925905	2026-08-25 11:47:39.932861
f1313521-a7be-4964-9280-98de828111d0	m_ws_broadcast_test_a741c3d2	instagram	t	\N	\N	{"sender": {"id": "23086741_2489"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a741c3d2", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 11:56:19.20024	\N
b88ed772-530e-4b1f-9200-df225dbe40f3	m_exact_test_99e755e9	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_99e755e9", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 11:56:19.592577	\N
6dec6452-6caf-4cc0-a21c-d7638e153fd5	wamid.TEST_87b7c294	whatsapp	t	\N	59	\N	2026-08-25 12:00:56.000841	2026-08-25 12:00:56.031687
37fa1652-850f-4bb3-8399-608a311010bb	wamid.TEST_a5244e7e	whatsapp	t	\N	46	\N	2026-08-25 12:00:56.066879	2026-08-25 12:00:56.087764
c3002a21-7bc6-482b-a424-af69e059ce8b	wamid.TEST_01369afd	whatsapp	t	\N	11	\N	2026-08-25 12:00:56.091909	2026-08-25 12:00:56.101979
a1dcc1b7-a9c2-4cc1-afac-5efb688b57c2	wamid.TEST_f862e0c2	whatsapp	t	\N	52	\N	2026-08-25 12:00:56.13708	2026-08-25 12:00:56.162341
327cade2-2eb7-4f5e-b442-aebd3bcf9962	wamid.TEST_be5f8cbc	whatsapp	t	\N	10	\N	2026-08-25 12:00:56.167619	2026-08-25 12:00:56.176026
b97f590b-6b5d-479b-ac01-0f3b556b36aa	wamid.TEST_e4136f0d	whatsapp	t	\N	43	\N	2026-08-25 12:00:56.20809	2026-08-25 12:00:56.227251
4a1a9063-7890-43a8-8f04-a3b7820acfef	wamid.TEST_1afaa69a	whatsapp	t	\N	44	\N	2026-08-25 12:00:56.258614	2026-08-25 12:00:56.278087
b872cdf8-7343-423e-80a6-25b8fd8407bb	wamid.TEST_427e1fba	whatsapp	t	\N	9	\N	2026-08-25 12:00:56.283176	2026-08-25 12:00:56.291521
6f6f7042-23a2-4358-a6fe-1a0a59497cb8	wamid.DEDUP_8742021b	whatsapp	t	\N	46	\N	2026-08-25 12:00:56.323054	2026-08-25 12:00:56.344283
d6574506-4da4-4343-b609-0963332af1c2	m_ws_broadcast_test_7355de08	instagram	t	\N	\N	{"sender": {"id": "23086741_3e5b"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_7355de08", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 12:09:37.672734	\N
31a9380d-393c-45cd-bf98-ad7b3fd0ad34	wamid.TEST_2d0f9a85	whatsapp	t	\N	51	\N	2026-08-25 12:31:47.699055	2026-08-25 12:31:47.726437
03427f85-9907-444d-ab4e-24eaeeb53181	wamid.TEST_db4e7a23	whatsapp	t	\N	45	\N	2026-08-25 12:31:47.759193	2026-08-25 12:31:47.780659
d4a4b1bc-dc6e-45c5-9749-9f31d73e522c	wamid.TEST_3d9f47fb	whatsapp	t	\N	9	\N	2026-08-25 12:31:47.784301	2026-08-25 12:31:47.7924
e9c01273-c2b7-4f09-8249-7168c97414c7	wamid.TEST_d692d3f6	whatsapp	t	\N	62	\N	2026-08-25 06:33:47.114515	2026-08-25 06:33:47.140536
32328207-3aca-43ad-9cfa-64d390105c52	wamid.TEST_2f8df361	whatsapp	t	\N	12	\N	2026-08-25 06:33:47.146111	2026-08-25 06:33:47.157008
d955d88f-01d1-4bd7-94f5-930e9c6dc05e	wamid.TEST_afb1b8a9	whatsapp	t	\N	10	\N	2026-08-25 12:37:21.960504	2026-08-25 12:37:21.969709
af182a45-aae5-40f4-8d39-bdee77bb0bc2	wamid.TEST_e4bfc024	whatsapp	t	\N	49	\N	2026-08-25 06:33:47.194934	2026-08-25 06:33:47.217563
0b123ef3-2304-4b22-a0f0-4860160bfb90	wamid.TEST_2cc99c96	whatsapp	t	\N	53	\N	2026-08-25 06:33:47.25786	2026-08-25 06:33:47.277389
76c97e8c-ad61-465c-a905-1a829a436506	wamid.TEST_7b00c642	whatsapp	t	\N	54	\N	2026-08-25 12:37:22.137879	2026-08-25 12:37:22.165309
863434ea-80be-4849-be67-6fdec6ab74b6	wamid.TEST_aef02695	whatsapp	t	\N	8	\N	2026-08-25 06:33:47.280993	2026-08-25 06:33:47.288278
b494bbab-0fa0-42e1-81d0-3644dd6134f4	wamid.DEDUP_53aa3a63	whatsapp	t	\N	46	\N	2026-08-25 06:33:47.320049	2026-08-25 06:33:47.340978
4d422b6a-bcfe-4eba-8975-a49878a6c239	m_exact_test_d488510f	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_d488510f", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 07:01:04.654397	\N
5b4b76f6-1142-4d19-a8d7-0f2fa868f067	wamid.TEST_b069930d	whatsapp	t	\N	53	\N	2026-08-25 07:02:08.141833	2026-08-25 07:02:08.169492
504ea9bf-f25f-49e3-8976-dc7fed4a921b	wamid.TEST_29d99a04	whatsapp	t	\N	9	\N	2026-08-25 07:02:08.173407	2026-08-25 07:02:08.182111
8a3d2021-766f-4bf7-a376-5f5ebae7d797	wamid.TEST_420d3d7c	whatsapp	t	\N	49	\N	2026-08-25 07:02:08.279779	2026-08-25 07:02:08.303306
eb2c4c11-f03c-4a7d-afd9-549153977b11	wamid.TEST_69e7c27a	whatsapp	t	\N	9	\N	2026-08-25 07:02:08.309154	2026-08-25 07:02:08.317036
61237dc7-2caa-4200-b9e2-ca1f13a5362a	m_ws_broadcast_test_a865bdc3	instagram	t	\N	\N	{"sender": {"id": "23086741_3220"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a865bdc3", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 06:42:28.983405	\N
49f7ff12-a117-4c5e-b91e-ee0407465942	m_exact_test_2eb890b4	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_2eb890b4", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 06:42:29.326597	\N
e057daf1-4fd1-47b3-9f0c-b5290597235d	wamid.TEST_043f5e03	whatsapp	t	\N	50	\N	2026-08-25 06:52:47.079992	2026-08-25 06:52:47.105528
60797224-3971-4c81-9df7-7dea2054cf3b	wamid.TEST_49a3540a	whatsapp	t	\N	50	\N	2026-08-25 06:52:47.141625	2026-08-25 06:52:47.166195
1bc2d37a-56ea-46c9-b9d0-422bb539f105	wamid.TEST_07066ad0	whatsapp	t	\N	14	\N	2026-08-25 06:52:47.170478	2026-08-25 06:52:47.183645
afca080c-0a61-47c2-b797-4436eab6ce9d	wamid.TEST_b10b6283	whatsapp	t	\N	48	\N	2026-08-25 06:52:47.220506	2026-08-25 06:52:47.242943
e969523b-41d6-4bf9-90d2-fb0764bb02ef	m_ws_broadcast_test_a5e9a6a6	instagram	t	\N	\N	{"sender": {"id": "23086741_f531"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a5e9a6a6", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 07:10:46.695418	\N
b1f4cce0-7055-4144-8b1c-302714f95ec8	wamid.TEST_bf5902d7	whatsapp	t	\N	11	\N	2026-08-25 06:52:47.247246	2026-08-25 06:52:47.25732
9b005ded-3003-4086-89e9-fc05defd0dc5	wamid.TEST_a109bc4a	whatsapp	t	\N	48	\N	2026-08-25 06:52:47.291372	2026-08-25 06:52:47.314041
93c08a47-43b6-4ed4-9ecc-32f606cf2b51	wamid.TEST_bd4a1de5	whatsapp	t	\N	55	\N	2026-08-25 08:17:16.215557	2026-08-25 08:17:16.243106
81e2b787-10ac-43dd-8e1e-7b2e2fd041b3	wamid.TEST_8df2a328	whatsapp	t	\N	51	\N	2026-08-25 06:52:47.346645	2026-08-25 06:52:47.37312
538c0550-8b9c-404c-8699-ab0d01798dcf	wamid.TEST_debfcc8e	whatsapp	t	\N	9	\N	2026-08-25 06:52:47.378575	2026-08-25 06:52:47.387093
a96e6c32-281d-479d-8478-86a417eb8197	wamid.TEST_6c8a6f22	whatsapp	t	\N	44	\N	2026-08-25 08:17:16.341152	2026-08-25 08:17:16.361551
0c1deb01-d9cd-4858-bbfe-854e022ae095	wamid.DEDUP_c643aea8	whatsapp	t	\N	50	\N	2026-08-25 06:52:47.418509	2026-08-25 06:52:47.443876
92466d65-e66e-4ceb-9010-8c54d47a029c	wamid.TEST_d4ea8536	whatsapp	t	\N	8	\N	2026-08-25 08:17:16.365143	2026-08-25 08:17:16.373105
0a9d55f0-2f53-492d-a571-e05c94e457fb	wamid.TEST_3fdb9322	whatsapp	t	\N	44	\N	2026-08-25 08:17:16.454432	2026-08-25 08:17:16.474503
34591dce-a0d1-4895-9739-b26063aac160	wamid.TEST_9f34d159	whatsapp	t	\N	7	\N	2026-08-25 08:17:16.478892	2026-08-25 08:17:16.48585
6660325d-26bc-4705-b583-9f9ec2071efb	m_ws_broadcast_test_8f8c2718	instagram	t	\N	\N	{"sender": {"id": "23086741_50de"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_8f8c2718", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 08:25:55.564113	\N
38ebff69-f9b8-4f6f-8b8e-158904e37553	wamid.TEST_b00a6cf9	whatsapp	t	\N	50	\N	2026-08-25 08:27:49.721641	2026-08-25 08:27:49.745936
4ef5d548-c56e-4fb0-b580-1379d789cfab	wamid.TEST_dd7f1283	whatsapp	t	\N	54	\N	2026-08-25 08:27:49.963735	2026-08-25 08:27:49.993765
5412770b-3019-480b-a4f0-108044a62278	wamid.TEST_9db6adf9	whatsapp	t	\N	10	\N	2026-08-25 08:27:50.010586	2026-08-25 08:27:50.020166
8629c76f-7b50-4832-a5dc-c8a53bc311f4	wamid.TEST_5e50e60d	whatsapp	t	\N	60	\N	2026-08-25 08:27:50.119745	2026-08-25 08:27:50.145546
aaaa6f12-e14a-4c08-9e39-264a643f7c9b	wamid.TEST_2e200acf	whatsapp	t	\N	10	\N	2026-08-25 08:27:50.15004	2026-08-25 08:27:50.159099
5987f3f4-a56d-4a26-bd46-583706071c52	m_ws_broadcast_test_8de72632	instagram	t	\N	\N	{"sender": {"id": "23086741_0fd3"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_8de72632", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 08:36:31.664629	\N
f364b5af-304e-4ccc-97df-8b56b4d91935	wamid.TEST_9867534b	whatsapp	t	\N	99	\N	2026-08-25 08:37:00.541351	2026-08-25 08:37:00.589944
1be2bb2d-63ba-4da5-b632-8acbf3f7e59f	wamid.TEST_079edc25	whatsapp	t	\N	16	\N	2026-08-25 08:37:00.595891	2026-08-25 08:37:00.610057
ca4bd73d-4d0b-4121-a3c1-4f0bbd4e39d1	wamid.TEST_e8dc70c5	whatsapp	t	\N	46	\N	2026-08-25 08:38:14.981301	2026-08-25 08:38:15.003276
d09e4401-d7d7-43e0-82b3-ac59fade56bf	wamid.TEST_f0821e97	whatsapp	t	\N	8	\N	2026-08-25 08:38:15.006804	2026-08-25 08:38:15.013939
322e9a86-ee9d-44d9-9b11-7d020698521e	wamid.TEST_4d8013a5	whatsapp	t	\N	79	\N	2026-08-25 08:38:15.127504	2026-08-25 08:38:15.169449
878f5a56-e4cc-495d-8d14-7e7591a9caad	wamid.DEDUP_4c5f7baf	whatsapp	t	\N	44	\N	2026-08-25 08:38:15.264112	2026-08-25 08:38:15.282864
4705cc5e-ddc5-42ab-8542-1a00cd758e14	m_exact_test_bda925a4	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_bda925a4", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 08:46:54.090594	\N
a4507d1a-c6f3-4dd3-9241-411d3a40f752	wamid.TEST_77ca1457	whatsapp	t	\N	47	\N	2026-08-25 10:00:18.529401	2026-08-25 10:00:18.551844
9eafc5b1-4cec-4342-81ed-a9c57b3d71a2	wamid.TEST_831c4792	whatsapp	t	\N	8	\N	2026-08-25 10:00:18.555517	2026-08-25 10:00:18.56334
47654b69-6550-4fd0-a202-ce5b63735b00	wamid.TEST_e5a98e3f	whatsapp	t	\N	42	\N	2026-08-25 10:00:18.657375	2026-08-25 10:00:18.676765
0e757384-8f0e-4a52-a30a-bd017b77a7d5	wamid.DEDUP_cb06f73f	whatsapp	t	\N	47	\N	2026-08-25 10:00:18.767921	2026-08-25 10:00:18.792268
f43124b3-c3e7-461a-b938-7818091e8f71	m_exact_test_d72089a3	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_d72089a3", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 10:08:57.3728	\N
72257191-3ddd-41c9-bbf1-8ac800ce7277	wamid.TEST_e6159029	whatsapp	t	\N	51	\N	2026-08-25 10:25:47.227909	2026-08-25 10:25:47.254049
8f3f2f03-0a5d-4fab-bb9b-721d6bceb5cb	wamid.TEST_0624837c	whatsapp	t	\N	8	\N	2026-08-25 10:25:47.257524	2026-08-25 10:25:47.265045
6ff87d7e-9cb2-4e8e-8d19-ece3839c8dab	wamid.TEST_b6e9a072	whatsapp	t	\N	49	\N	2026-08-25 10:25:47.361627	2026-08-25 10:25:47.386474
c2540a12-3ebe-4760-9b90-08b4f5724f80	wamid.DEDUP_9bbe3159	whatsapp	t	\N	47	\N	2026-08-25 10:25:47.501305	2026-08-25 10:25:47.522827
df79601a-e1d9-4339-8bc5-5d7bafd1af2c	m_exact_test_e9f38977	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_e9f38977", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 10:34:27.406477	\N
a5215f5d-98e9-46ab-8c49-e797e1510024	wamid.TEST_d033bc35	whatsapp	t	\N	51	\N	2026-08-25 11:47:39.692439	2026-08-25 11:47:39.71932
73beccd4-d117-45de-9e63-b94898eee123	wamid.TEST_864f0d7a	whatsapp	t	\N	8	\N	2026-08-25 11:47:39.723727	2026-08-25 11:47:39.731003
856caed7-f6b8-470f-96ea-ee16b27354ed	wamid.TEST_d8defa80	whatsapp	t	\N	58	\N	2026-08-25 11:47:39.844582	2026-08-25 11:47:39.867285
998d1985-d1f0-4cd0-9feb-73301b9befeb	wamid.DEDUP_e8f37f05	whatsapp	t	\N	44	\N	2026-08-25 11:47:39.964095	2026-08-25 11:47:39.984188
46d49dc1-7655-42be-b79a-1132ddbed8f9	m_exact_test_209f2812	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_209f2812", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 12:09:38.040397	\N
4f194e44-68c0-47b3-918b-bd63d8394026	wamid.TEST_dae8bd88	whatsapp	t	\N	50	\N	2026-08-25 12:37:22.004136	2026-08-25 12:37:22.029456
8ed7a3fd-3abd-47e1-a67b-37c079e1827e	wamid.TEST_7f4ff709	whatsapp	t	\N	12	\N	2026-08-25 12:37:22.033541	2026-08-25 12:37:22.044721
7e9d7848-0ee7-4b08-a12d-03562acdde44	wamid.TEST_1ef5ee0f	whatsapp	t	\N	11	\N	2026-08-25 12:37:22.17145	2026-08-25 12:37:22.181212
d8a3c0cb-cc4f-46bf-9726-e1921a186956	wamid.TEST_94ff72ae	whatsapp	t	\N	84	\N	2026-08-25 12:38:18.144559	2026-08-25 12:38:18.202136
3d9ae2c5-9a60-40a0-8f0c-30eac779547b	wamid.TEST_8aa8a0c6	whatsapp	t	\N	55	\N	2026-08-25 12:38:18.353579	2026-08-25 12:38:18.380719
78a027b4-9e1a-44db-bda1-c439726b1ed7	wamid.TEST_335fb436	whatsapp	t	\N	15	\N	2026-08-25 12:38:18.38579	2026-08-25 12:38:18.399372
0cac23d8-4630-45ce-81e3-456c05ee91f5	wamid.TEST_4ee6072f	whatsapp	t	\N	84	\N	2026-08-25 12:38:18.549592	2026-08-25 12:38:18.597039
2bd0516b-6b49-4b4c-92e7-25fd6218a65b	wamid.TEST_0a64e3a4	whatsapp	t	\N	9	\N	2026-08-25 12:38:18.602285	2026-08-25 12:38:18.610752
4a2c1c25-e0dc-449a-8fa8-8da99018d75b	m_ws_broadcast_test_b1bc2e7e	instagram	t	\N	\N	{"sender": {"id": "23086741_def8"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_b1bc2e7e", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 12:40:27.990063	\N
94f246d1-657b-4122-b0a5-63b5dd12ff27	m_ws_broadcast_test_d53bd531	instagram	t	\N	\N	{"sender": {"id": "23086741_839d"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_d53bd531", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 12:41:26.010629	\N
4109c0f9-37ea-47ce-9ddb-4964b8bf0732	m_ws_broadcast_test_cc422a69	instagram	t	\N	\N	{"sender": {"id": "23086741_66bc"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_cc422a69", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 12:46:02.578994	\N
ab31244d-883a-4ec1-af20-359a25ec7197	m_ws_broadcast_test_05201078	instagram	t	\N	\N	{"sender": {"id": "23086741_f41e"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_05201078", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-25 12:46:57.252879	\N
5d6a23ae-0368-4f05-b9a1-b9d79b80278f	wamid.TEST_9b84c36b	whatsapp	t	\N	57	\N	2026-08-26 05:11:37.692408	2026-08-26 05:11:37.723357
83798d99-648b-4249-983e-02b1c6c4fe00	wamid.TEST_8f2a60b1	whatsapp	t	\N	48	\N	2026-08-26 05:11:37.825531	2026-08-26 05:11:37.848765
68aef51d-d23c-49fb-9d07-a6ab33c6521f	wamid.TEST_0e3b2663	whatsapp	t	\N	8	\N	2026-08-26 05:11:37.852238	2026-08-26 05:11:37.859819
9c359faf-9869-4874-84c7-664a38ef8215	wamid.TEST_e797e595	whatsapp	t	\N	43	\N	2026-08-26 05:11:37.943582	2026-08-26 05:11:37.962601
93461c60-e867-469a-8949-8885ec2bb0be	wamid.TEST_5c2c0143	whatsapp	t	\N	8	\N	2026-08-26 05:11:37.967092	2026-08-26 05:11:37.974523
047d244d-22e7-4d24-bdef-11ad20c40ce0	m_ws_broadcast_test_52d1bb56	instagram	t	\N	\N	{"sender": {"id": "23086741_4872"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_52d1bb56", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 05:20:18.773649	\N
a5e2c2ab-8b6e-47e1-bb5a-a89378297365	wamid.TEST_d007c8ff	whatsapp	t	\N	45	\N	2026-08-25 12:31:47.824005	2026-08-25 12:31:47.845393
bbd4772d-9d75-409c-94ca-994ff3531ac3	wamid.TEST_72548074	whatsapp	t	\N	50	\N	2026-08-25 12:37:22.079686	2026-08-25 12:37:22.103427
987f7e58-33e2-49c3-adf7-c82aa12626b3	wamid.TEST_e93b57b1	whatsapp	t	\N	9	\N	2026-08-25 12:31:47.84908	2026-08-25 12:31:47.857574
a0bd9fef-ee12-4ea2-aa3f-707eb4df0241	wamid.TEST_f09b4225	whatsapp	t	\N	45	\N	2026-08-25 12:31:47.88934	2026-08-25 12:31:47.911504
8313c641-5cf9-44f3-8f9c-952bb07798db	wamid.DEDUP_8abb9828	whatsapp	t	\N	53	\N	2026-08-25 12:37:22.218191	2026-08-25 12:37:22.244352
4e619f69-880d-4f60-9be4-55b67e810be5	wamid.TEST_23257be7	whatsapp	t	\N	83	\N	2026-08-25 12:31:47.951076	2026-08-25 12:31:48.003148
5f710f92-0ab4-441c-85ad-e1cb09cf5b2a	wamid.TEST_3db35652	whatsapp	t	\N	8	\N	2026-08-25 12:31:48.008611	2026-08-25 12:31:48.01621
a877492b-273f-4225-88a7-a560e4eab8c5	wamid.DEDUP_f73f2dcd	whatsapp	t	\N	47	\N	2026-08-25 12:31:48.047826	2026-08-25 12:31:48.070028
0b8761be-85b0-4831-b572-4d00c26d03a4	wamid.TEST_b3ea15cc	whatsapp	t	\N	86	\N	2026-08-25 12:38:18.255	2026-08-25 12:38:18.301892
bc5743c1-5282-4da3-896c-c0200a00a32a	wamid.TEST_5e4eabeb	whatsapp	t	\N	10	\N	2026-08-25 12:38:18.306298	2026-08-25 12:38:18.315355
bea32bdb-0897-4875-9b1b-b27cc352e847	wamid.TEST_93e39d63	whatsapp	t	\N	95	\N	2026-08-25 12:38:18.449665	2026-08-25 12:38:18.504252
47f4250a-230a-4b80-afa6-41c1a3637aa8	wamid.DEDUP_f464bf2c	whatsapp	t	\N	53	\N	2026-08-25 12:38:18.645923	2026-08-25 12:38:18.67187
347c3fe6-f6a5-40af-8fa2-02353008661f	wamid.TEST_5330b780	whatsapp	t	\N	54	\N	2026-08-25 12:32:46.766369	2026-08-25 12:32:46.795186
3fbd2fc3-5315-471b-92b0-97d204e32ff2	wamid.TEST_d0c30c75	whatsapp	t	\N	48	\N	2026-08-25 12:32:46.831094	2026-08-25 12:32:46.854206
7866e3c7-eafc-4443-858b-a669be7d2c14	wamid.TEST_9b7fc2c4	whatsapp	t	\N	10	\N	2026-08-25 12:32:46.858835	2026-08-25 12:32:46.86818
fd9ff8b8-655c-4225-85b6-bdbb2f50d3ce	wamid.TEST_cda84cea	whatsapp	t	\N	71	\N	2026-08-25 12:32:46.904653	2026-08-25 12:32:46.950187
2b0b5c9c-3f05-4c18-9c6c-99c5637d9325	wamid.TEST_06d184e0	whatsapp	t	\N	12	\N	2026-08-25 12:32:46.954695	2026-08-25 12:32:46.965661
412f5834-7f19-42e5-9d5b-49632abbcf74	m_exact_test_760c6194	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_760c6194", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 12:40:28.359626	\N
3f9c3c7b-11aa-4af1-a61e-b16e00656c54	wamid.TEST_2e7c97e3	whatsapp	t	\N	50	\N	2026-08-25 12:32:47.001696	2026-08-25 12:32:47.027372
ee6ba6d9-02e1-4fb5-94e0-f9a3dba6c705	wamid.TEST_a26719b5	whatsapp	t	\N	61	\N	2026-08-25 12:32:47.073953	2026-08-25 12:32:47.097244
b80b1334-f3c1-4d20-b493-3835b1c97c2a	m_exact_test_015018e5	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_015018e5", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 12:41:26.384042	\N
7d1dd4c7-3604-4da3-af74-c2cb1e535a26	wamid.TEST_d786c59f	whatsapp	t	\N	12	\N	2026-08-25 12:32:47.102334	2026-08-25 12:32:47.113094
2cb5beba-65a8-43bd-9e06-219dc1e47be5	wamid.DEDUP_cb22b5be	whatsapp	t	\N	89	\N	2026-08-25 12:32:47.158321	2026-08-25 12:32:47.211974
74cc13fd-2d14-4563-9688-8517b61cba12	m_exact_test_38fb2b8a	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_38fb2b8a", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 12:46:02.959049	\N
b666cfe0-cbe1-4df7-956f-4f7c2e568d70	m_exact_test_dc5bec03	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_dc5bec03", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-25 12:46:57.641784	\N
8d44029a-4798-4c5a-9dfe-dbce2799270b	wamid.TEST_c2594d89	whatsapp	t	\N	48	\N	2026-08-26 05:11:37.757199	2026-08-26 05:11:37.781008
2ca09ddc-ab94-4760-8af6-0a9027a25f18	wamid.TEST_7fb7ffcc	whatsapp	t	\N	8	\N	2026-08-26 05:11:37.785418	2026-08-26 05:11:37.792921
e4115653-6e1f-4e86-84a0-2dd707f2501a	wamid.TEST_4ee8bbf6	whatsapp	t	\N	46	\N	2026-08-26 05:11:37.891251	2026-08-26 05:11:37.912822
c5ca5445-4c7e-4668-843a-05352617cf6f	wamid.DEDUP_aed82dc6	whatsapp	t	\N	46	\N	2026-08-26 05:11:38.006865	2026-08-26 05:11:38.02732
905e814d-e990-494a-964c-73de1b656aaf	m_exact_test_9b30ad76	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_9b30ad76", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 05:20:19.139051	\N
0ca116de-8fca-4113-8b78-5bb41ffa40b7	wamid.TEST_814630f0	whatsapp	t	\N	101	\N	2026-08-26 10:09:11.72785	2026-08-26 10:09:11.771254
9fdcbd57-b168-42f7-8745-19be90b45344	m_ws_broadcast_test_f14bec52	instagram	t	\N	\N	{"sender": {"id": "23086741_ea10"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f14bec52", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 06:29:39.945486	\N
ced25756-dc5e-46da-a7fb-12b59de51b14	wamid.TEST_9f189b07	whatsapp	t	\N	22	\N	2026-08-26 12:30:37.174479	2026-08-26 12:30:37.193136
8cc04e0e-31b0-4e59-b04c-6408db9b590d	wamid.TEST_2c0d507b	whatsapp	t	\N	127	\N	2026-08-27 08:12:57.510716	2026-08-27 08:12:57.56597
6e808cff-f960-4425-83b8-7e3b940a9633	wamid.DEDUP_84a3b3d8	whatsapp	t	\N	91	\N	2026-08-26 10:31:31.15744	2026-08-26 10:31:31.198578
b2ff0f35-eb66-45ea-8887-09fac3e14a12	m_ws_broadcast_test_ef6cdb1f	instagram	t	\N	\N	{"sender": {"id": "23086741_f79e"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_ef6cdb1f", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-09-01 08:36:03.679113	\N
1fbda014-d5f0-4c1b-a4d6-c67f609666e9	m_exact_test_28bdfef1	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_28bdfef1", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 10:40:33.867209	\N
50992255-95af-43bf-862f-3f7497cf6abb	wamid.TEST_dce2226b	whatsapp	t	\N	22	\N	2026-08-27 08:12:57.573355	2026-08-27 08:12:57.591861
7f74bd15-da7d-4a38-a93e-9f9bc6951c60	wamid.TEST_53f84bfe	whatsapp	t	\N	80	\N	2026-08-26 10:59:31.193624	2026-08-26 10:59:31.230041
8f6ac726-2683-4360-8d69-976865597aa8	wamid.TEST_e9744275	whatsapp	t	\N	141	\N	2026-08-26 13:05:30.267215	2026-08-26 13:05:30.331569
9a97117b-57b0-4c32-974b-526ed3107611	wamid.TEST_3e7474a5	whatsapp	t	\N	16	\N	2026-08-26 10:59:31.23453	2026-08-26 10:59:31.248554
fc7d523f-cf6d-4cda-9c8a-c77f73518005	m_real_test_fab8a440	instagram	f	(sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "ix_tickets_ref"\nDETAIL:  Key (ref)=(TCK-25794) already exists.\n[SQL: INSERT INTO tickets (id, ref, customer_id, agent_id, subject, category, channel, status, priority, sla_due_at, sla_breached, sentiment, ai_confidence, ai_resolved, ai_summary, deleted_at, created_at, updated_at) VALUES ($1::UUID, $2::VARCHAR, $3::UUID, $4::UUID, $5::VARCHAR, 	\N	{"sender": {"id": "23086741_5e0e"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_real_test_fab8a440", "text": "INSTAGRAM E2E TEST 2026-NEW-001"}}	2026-08-27 08:13:04.851728	\N
7e1fdebb-9b22-4d07-b2d7-133cbd6e4b1c	wamid.DEDUP_eb12db5b	whatsapp	t	\N	88	\N	2026-08-26 11:05:41.279881	2026-08-26 11:05:41.318189
78a78402-3713-41ef-806e-8bc0ba22cbf7	wamid.DEDUP_e5a5ac9a	whatsapp	t	\N	168	\N	2026-08-26 13:15:30.740557	2026-08-26 13:15:30.810717
e3e30e59-5915-46bd-919b-794732e6c80a	wamid.DEDUP_947cd95f	whatsapp	t	\N	78	\N	2026-08-31 06:36:55.786742	2026-08-31 06:36:55.823951
e44ab552-4159-4a83-a4d7-79e822d0550c	wamid.TEST_3afe2f84	whatsapp	t	\N	84	\N	2026-08-26 11:22:04.122405	2026-08-26 11:22:04.15918
e4b1b859-b99e-41f8-ad86-0010df1d89ab	m_exact_test_f580e587	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_f580e587", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 06:38:18.790908	\N
84c9716c-2ad7-481c-b4c5-b51797f6e4a9	wamid.TEST_91ecc22e	whatsapp	t	\N	17	\N	2026-08-26 11:22:04.165774	2026-08-26 11:22:04.179762
3423e325-5f59-4aea-86f0-e894fcd1e1f6	wamid.TEST_0d18d23c	whatsapp	t	\N	149	\N	2026-08-27 04:28:59.818071	2026-08-27 04:28:59.877377
fa374626-00b2-4d09-ad69-f71edd3782db	wamid.TEST_ac9cb568	whatsapp	t	\N	26	\N	2026-08-27 04:28:59.884918	2026-08-27 04:28:59.907498
de154686-f5d2-44dc-817c-ee49074a35fb	wamid.TEST_5ba535bb	whatsapp	t	\N	82	\N	2026-08-26 11:41:32.436981	2026-08-26 11:41:32.471041
3590d2f3-e0bc-4c59-a628-1feed7cb9d7b	wamid.DEDUP_7e4f02fe	whatsapp	t	\N	82	\N	2026-08-26 11:51:41.797113	2026-08-26 11:51:41.834471
4f82e58e-ff52-43ba-adc5-e3f6de173a57	wamid.TEST_bb7160c1	whatsapp	t	\N	89	\N	2026-08-27 04:53:36.501493	2026-08-27 04:53:36.539994
34723ee1-9bd6-40fd-a026-53790e19d2f6	m_exact_test_f3f017f2	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_f3f017f2", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 04:54:47.36686	\N
549b0cb0-2c7f-4e71-8531-10e67e2c3bec	wamid.TEST_fd195117	whatsapp	t	\N	82	\N	2026-08-27 05:08:11.059082	2026-08-27 05:08:11.101423
c6d9ce8c-3c7e-4368-8abe-6b04fa660fcf	wamid.TEST_f374a0a8	whatsapp	t	\N	15	\N	2026-08-27 05:08:11.108627	2026-08-27 05:08:11.121404
0ea5a56e-7196-4889-b654-b58f5efa5271	wamid.TEST_23c23d4d	whatsapp	t	\N	162	\N	2026-08-27 05:37:30.571503	2026-08-27 05:37:30.624971
c44bac5f-4cd0-4df9-bbcd-c17b6e653bd9	wamid.DEDUP_e51f6776	whatsapp	t	\N	118	\N	2026-08-27 05:54:13.001929	2026-08-27 05:54:13.068558
637b7bb0-c2a5-41ea-b121-ed7e12fc3180	m_exact_test_aa89372a	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_aa89372a", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 05:55:19.081382	\N
b3caa0bd-a3a8-464b-bf10-e8e9c58546e6	wamid.TEST_9e135c8c	whatsapp	t	\N	89	\N	2026-08-27 06:26:44.576247	2026-08-27 06:26:44.622994
6af4220d-8cbe-4c56-a95e-56e82e11292b	wamid.TEST_e462ba0b	whatsapp	t	\N	15	\N	2026-08-27 06:26:44.628188	2026-08-27 06:26:44.641287
14e8f901-2f5c-424e-bf62-dcad837317f2	wamid.TEST_50352168	whatsapp	t	\N	103	\N	2026-08-26 10:09:11.840881	2026-08-26 10:09:11.885048
cf51e91e-6e70-4316-9396-97c9fb9c9d03	m_exact_test_e0d757ac	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_e0d757ac", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 06:29:40.405451	\N
8054f71f-a175-4fc0-a77f-b8d8f4d8a1e7	wamid.TEST_88390283	whatsapp	t	\N	21	\N	2026-08-26 10:09:11.893664	2026-08-26 10:09:11.911977
54aea3bf-1159-4513-a00d-806522533b0f	wamid.TEST_92b87952	whatsapp	t	\N	128	\N	2026-09-01 09:06:11.42339	2026-09-01 09:06:11.477719
c040bbd7-a35d-4c68-b5e7-d331803fc6b1	m_ws_broadcast_test_cfc50c29	instagram	t	\N	\N	{"sender": {"id": "23086741_f998"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_cfc50c29", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 10:10:38.305237	\N
44cd9a7e-c137-4dd8-8592-faa450b4e58d	wamid.TEST_0f51f31f	whatsapp	t	\N	137	\N	2026-08-26 12:30:37.290108	2026-08-26 12:30:37.354318
022e884e-67e3-4318-93bd-d73ca4b6e6be	wamid.TEST_949f7889	whatsapp	t	\N	128	\N	2026-08-27 08:12:57.681777	2026-08-27 08:12:57.737016
6263b612-8e1b-428b-b5d7-83ebe5e9ebfe	wamid.TEST_edada33b	whatsapp	t	\N	27	\N	2026-08-26 12:30:37.36103	2026-08-26 12:30:37.38574
3c3ed679-c850-47ee-8e09-338f787cb3f1	wamid.TEST_b4b9dbd9	whatsapp	t	\N	25	\N	2026-08-27 08:12:57.74591	2026-08-27 08:12:57.767007
5457af3b-dc05-4c83-acb5-12927fe113c6	wamid.TEST_c053fb78	whatsapp	t	\N	23	\N	2026-09-01 09:06:11.484644	2026-09-01 09:06:11.504967
13d3b700-41c7-40c5-b46c-52e1844ddd07	wamid.TEST_fc3f4bc7	whatsapp	t	\N	139	\N	2026-09-01 09:57:17.326619	2026-09-01 09:57:17.389558
3572428d-3549-4f09-b3de-cf9f12094297	wamid.TEST_07b45819	whatsapp	t	\N	105	\N	2026-08-26 11:06:43.654075	2026-08-26 11:06:43.709195
e4f0631e-54f7-48ee-bc9d-d7499b33d38e	m_ws_broadcast_test_74c47e60	instagram	f	(sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class 'asyncpg.exceptions.UniqueViolationError'>: duplicate key value violates unique constraint "ix_tickets_ref"\nDETAIL:  Key (ref)=(TCK-14742) already exists.\n[SQL: INSERT INTO tickets (id, ref, customer_id, agent_id, subject, category, channel, status, priority, sla_due_at, sla_breached, sentiment, ai_confidence, ai_resolved, ai_summary, deleted_at, created_at, updated_at) VALUES ($1::UUID, $2::VARCHAR, $3::UUID, $4::UUID, $5::VARCHAR, 	\N	{"sender": {"id": "23086741_8d0f"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_74c47e60", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 13:14:58.025481	\N
17d419fe-9ab8-4303-b6bf-10904f72e490	wamid.TEST_07a21de4	whatsapp	t	\N	93	\N	2026-08-26 11:22:04.249883	2026-08-26 11:22:04.28745
43a2c0b4-cf28-4617-a42d-fca79faf72ac	m_ws_broadcast_test_70492f0f	instagram	t	\N	\N	{"sender": {"id": "23086741_6806"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_70492f0f", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 13:15:30.933861	\N
31898f4c-84d8-495e-84ab-a102043c4afd	wamid.TEST_e50d9465	whatsapp	t	\N	19	\N	2026-08-26 11:22:04.291924	2026-08-26 11:22:04.30988
9e789d8d-5593-4123-837a-edd12fcf1094	wamid.TEST_ca51f478	whatsapp	t	\N	26	\N	2026-09-01 09:57:17.398697	2026-09-01 09:57:17.420717
f7b7ab19-4500-43fb-844c-67ce54cb5488	wamid.TEST_52fe5b2e	whatsapp	t	\N	423	\N	2026-08-27 04:14:22.527061	2026-08-27 04:14:22.71613
65d1ac46-9f66-4aa0-a196-d875712c9f52	wamid.TEST_46727dfc	whatsapp	t	\N	181	\N	2026-09-02 04:19:15.092808	2026-09-02 04:19:15.155882
3e92f39d-b31c-421f-80c5-f6927d136140	wamid.TEST_0ee007e0	whatsapp	t	\N	87	\N	2026-08-31 07:08:02.657245	2026-08-31 07:08:02.69813
57d06f3c-bef7-4296-8c4a-fa8783f21cc7	wamid.TEST_d522a06e	whatsapp	t	\N	88	\N	2026-08-26 11:41:32.533611	2026-08-26 11:41:32.569168
c1ff4ba3-26a3-49f0-81e5-2c8d2d4154f4	wamid.TEST_92361f86	whatsapp	t	\N	138	\N	2026-08-27 04:29:00.006223	2026-08-27 04:29:00.064834
64676d5b-0f0d-467f-96d7-9fefd5cc42f5	wamid.TEST_4a52d93b	whatsapp	t	\N	14	\N	2026-08-26 11:41:32.573646	2026-08-26 11:41:32.586198
6490dc0d-3f07-4fa8-a084-bbffa58118b4	m_ws_broadcast_test_27394eba	instagram	t	\N	\N	{"sender": {"id": "23086741_ad5d"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_27394eba", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 11:50:20.021517	\N
396da682-d73f-4c79-9eb5-145adae141a9	wamid.TEST_1af5116b	whatsapp	t	\N	24	\N	2026-08-27 04:29:00.072644	2026-08-27 04:29:00.093381
a50c43db-beb2-483d-a7e9-94b86ab1cb73	wamid.TEST_779b3fa4	whatsapp	t	\N	121	\N	2026-08-31 07:29:14.961294	2026-08-31 07:29:15.013321
f98e342f-75aa-46e8-8dd1-9f9650ae9aa3	wamid.TEST_cc4df364	whatsapp	t	\N	92	\N	2026-08-27 04:53:36.599029	2026-08-27 04:53:36.641061
901f5a6c-6b1e-4e60-a212-56330cce4843	wamid.TEST_3966cfee	whatsapp	t	\N	149	\N	2026-08-31 07:46:46.688093	2026-08-31 07:46:46.749139
7e913d2c-e053-4995-a735-0065e803163a	wamid.TEST_b5fb5cb0	whatsapp	t	\N	13	\N	2026-08-27 04:53:36.645364	2026-08-27 04:53:36.657058
58012646-14ff-4d12-9cc8-f622f8b584d9	wamid.TEST_a70b500b	whatsapp	t	\N	127	\N	2026-08-27 04:53:55.502476	2026-08-27 04:53:55.566182
3b029b20-bb4c-445c-b653-311ba3b04e29	wamid.TEST_1f9702a2	whatsapp	t	\N	152	\N	2026-08-31 08:18:41.096335	2026-08-31 08:18:41.169085
cc1b766b-ccf3-4d0e-908c-d36c3e0b6396	wamid.TEST_f8ce0afd	whatsapp	t	\N	147	\N	2026-08-27 04:54:55.223948	2026-08-27 04:54:55.276175
5baea2eb-55a8-4f36-a9d2-67f5796c8350	wamid.TEST_a9f133be	whatsapp	t	\N	76	\N	2026-08-27 05:08:11.175362	2026-08-27 05:08:11.209106
40257550-0a81-4f3a-880a-0bc063f3feda	wamid.TEST_35507894	whatsapp	t	\N	23	\N	2026-08-27 05:08:11.214132	2026-08-27 05:08:11.23586
ca4cf360-7049-46fc-8db5-b437c46c5724	wamid.TEST_63ec15a7	whatsapp	t	\N	229	\N	2026-08-31 08:34:27.314722	2026-08-31 08:34:27.402524
ae87a79f-f68e-42f3-8e00-d01d46182171	wamid.TEST_abcd4c8f	whatsapp	t	\N	128	\N	2026-08-27 05:37:30.708365	2026-08-27 05:37:30.76658
78266d19-c08e-4559-8be4-e3a647925de6	wamid.TEST_eac3c646	whatsapp	t	\N	147	\N	2026-08-31 09:00:23.616009	2026-08-31 09:00:23.679421
25d66f63-2fb8-48b0-ae54-edfc1485d3d5	wamid.TEST_d12b7b68	whatsapp	t	\N	23	\N	2026-08-27 05:37:30.771834	2026-08-27 05:37:30.793105
e2a8b16b-cdd8-4163-9db1-64670a46af0f	m_ws_broadcast_test_5d1fa8d6	instagram	t	\N	\N	{"sender": {"id": "23086741_69a2"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_5d1fa8d6", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 05:38:43.812845	\N
ef13c11a-03e2-42ed-a385-3c435e5b1a29	wamid.TEST_9fa578dc	whatsapp	t	\N	181	\N	2026-08-31 09:41:27.68829	2026-08-31 09:41:27.758751
a0677bc2-a932-4d95-a74a-d11a73fdad14	wamid.TEST_e5e5b4b8	whatsapp	t	\N	83	\N	2026-08-27 06:03:37.577314	2026-08-27 06:03:37.616811
816b7473-0018-419c-8983-125b0360ae48	wamid.TEST_84770c2a	whatsapp	t	\N	88	\N	2026-08-27 06:26:44.695708	2026-08-27 06:26:44.741323
8bc00dd6-f565-49fa-96d5-8bde76ac15a2	wamid.TEST_45c99038	whatsapp	t	\N	100	\N	2026-08-31 10:03:07.499591	2026-08-31 10:03:07.545802
055e1c98-fddb-41d2-9b99-d0dd285c1289	wamid.TEST_bb9423a2	whatsapp	t	\N	17	\N	2026-08-27 06:26:44.746727	2026-08-27 06:26:44.762174
f6d49f21-68d4-4535-97b9-dc23c5d23936	m_exact_test_c8b26c9a	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_c8b26c9a", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 10:04:30.208248	\N
1130a798-707c-4222-871a-d193a55ff056	wamid.DEDUP_dd164ddc	whatsapp	t	\N	99	\N	2026-08-31 10:45:49.942291	2026-08-31 10:45:49.983993
e71c2e33-d366-4ff7-ab24-d709838b7a09	wamid.TEST_835fc559	whatsapp	t	\N	96	\N	2026-08-27 06:28:19.656013	2026-08-27 06:28:19.695962
c0a42e35-2a89-410f-9b21-662d773e88ff	wamid.TEST_27f6616c	whatsapp	t	\N	19	\N	2026-08-27 06:28:19.701285	2026-08-27 06:28:19.717963
9e269b55-6631-45ad-8e32-f2c0206a2158	m_exact_test_61036875	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_61036875", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-09-01 05:59:02.806913	\N
67735faf-9cfa-42a2-bfd1-db506e7445d2	wamid.TEST_c6812337	whatsapp	t	\N	75	\N	2026-09-01 06:51:02.878754	2026-09-01 06:51:02.911368
8bd89692-4b2e-4300-bfec-6fd2634f5e9c	wamid.TEST_263dcf5f	whatsapp	t	\N	122	\N	2026-09-01 08:34:18.333174	2026-09-01 08:34:18.386614
904bfb16-dbf7-4653-9f58-a867fa6da172	wamid.TEST_19120096	whatsapp	t	\N	22	\N	2026-09-01 08:34:18.392901	2026-09-01 08:34:18.412309
1777c5e0-555a-4c41-b3f6-4393396531ba	wamid.DEDUP_15d06777	whatsapp	t	\N	90	\N	2026-08-26 10:09:11.974134	2026-08-26 10:09:12.013768
0a9d6794-c3e5-447c-80fe-66ed47858edf	wamid.TEST_18bb6861	whatsapp	t	\N	160	\N	2026-08-27 06:37:40.442662	2026-08-27 06:37:40.499022
d237cc0a-4a0c-4cc0-a4bb-6f408ec32bba	m_exact_test_1de027bd	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_1de027bd", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 10:10:48.895846	\N
5307f74c-5bac-43ad-8024-c90075f06c8e	wamid.DEDUP_7bd04e98	whatsapp	t	\N	134	\N	2026-09-01 09:06:11.593946	2026-09-01 09:06:11.653941
38fb4397-9af7-4e16-85f5-bf7e2d54e392	wamid.TEST_d59c4038	whatsapp	t	\N	127	\N	2026-08-26 12:30:37.474139	2026-08-26 12:30:37.529085
f4ce0c14-e94e-4c53-8480-c273e9dd6b52	wamid.TEST_3ff69f6a	whatsapp	t	\N	136	\N	2026-08-27 08:12:57.860183	2026-08-27 08:12:57.92174
210dcd31-984a-4027-b2a0-70602527b064	wamid.TEST_7484a470	whatsapp	t	\N	83	\N	2026-08-26 10:59:31.642985	2026-08-26 10:59:31.682495
3d10d582-e04f-4822-8115-1c39e2c00db3	wamid.TEST_4e5d487c	whatsapp	t	\N	134	\N	2026-09-01 09:57:17.511204	2026-09-01 09:57:17.574553
b6d0cb1f-6c1c-45c0-87a6-d240c034ddcf	wamid.DEDUP_d1474c18	whatsapp	t	\N	223	\N	2026-08-26 13:05:30.905073	2026-08-26 13:05:31.025487
2b252de3-56e7-4d0d-9c46-4a96a9f66b94	wamid.TEST_9c7c9486	whatsapp	t	\N	86	\N	2026-08-26 11:06:43.772934	2026-08-26 11:06:43.811966
8c02b2d1-5988-4675-a2d6-e8e2ee673e10	wamid.TEST_1de1378f	whatsapp	t	\N	15	\N	2026-08-26 11:06:43.817815	2026-08-26 11:06:43.830139
dc8740a3-0607-4d3c-991a-8f0dc10f3c39	m_exact_test_cefedfee	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_cefedfee", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 13:14:58.877907	\N
67ffe963-2c48-403c-90ce-4e69224b231c	wamid.TEST_da5b53fb	whatsapp	t	\N	27	\N	2026-09-01 09:57:17.582811	2026-09-01 09:57:17.606393
3ea91f8f-5de3-4816-93d1-52d2a716a5c7	m_exact_test_9b2ce1c7	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_9b2ce1c7", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 13:15:31.805576	\N
2b948b93-1cf8-45d8-933f-6648d030684b	wamid.TEST_87b6803b	whatsapp	t	\N	97	\N	2026-08-26 11:22:04.386062	2026-08-26 11:22:04.421227
7c522239-7808-4e07-9d73-7e9987e18dab	wamid.TEST_0214bf22	whatsapp	t	\N	345	\N	2026-08-27 04:14:22.973508	2026-08-27 04:14:23.116363
31a9bef8-9dd4-414c-8545-ed782bad1f42	wamid.TEST_0e1e373f	whatsapp	t	\N	84	\N	2026-08-31 07:08:02.757389	2026-08-31 07:08:02.797467
748a641f-c75a-4aed-980d-b42edbb170a0	wamid.DEDUP_7cf32dc7	whatsapp	t	\N	93	\N	2026-08-26 11:41:32.651769	2026-08-26 11:41:32.689294
20e859b1-55a8-4fa6-8989-bed8bd60a250	wamid.TEST_d904036e	whatsapp	t	\N	89	\N	2026-08-27 04:14:23.137953	2026-08-27 04:14:23.217229
ec05ed9c-84c6-439c-9063-21a4eee0832e	m_exact_test_fe3538b4	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_fe3538b4", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 11:50:23.847918	\N
955caae2-b318-457d-a75f-e9a4abf06b88	wamid.TEST_e8749b79	whatsapp	t	\N	151	\N	2026-09-02 04:19:15.252177	2026-09-02 04:19:15.321085
03c864da-00e3-4be1-8a61-2e1702cac7c9	wamid.TEST_0efb91c9	whatsapp	t	\N	22	\N	2026-08-31 07:08:02.806766	2026-08-31 07:08:02.823664
103db90c-e453-4ec8-b539-feb26b61875a	wamid.TEST_76f5e7ff	whatsapp	t	\N	129	\N	2026-08-27 04:29:00.185953	2026-08-27 04:29:00.240882
6d16be50-a7b7-4ebc-9ded-cbc98a035404	wamid.TEST_1e926601	whatsapp	t	\N	22	\N	2026-09-02 04:19:15.328328	2026-09-02 04:19:15.346695
de4efb9f-6d56-4241-a458-484d2dbf2ed7	wamid.TEST_3147e702	whatsapp	t	\N	88	\N	2026-08-31 07:29:15.081859	2026-08-31 07:29:15.120405
db3a53cb-abbd-42fa-9045-9bdf5d71eb25	wamid.DEDUP_ac5922fc	whatsapp	t	\N	87	\N	2026-08-27 04:53:36.713696	2026-08-27 04:53:36.752756
5fcdf9c8-60fc-47ae-bcfa-a6de840b3047	wamid.TEST_c49fec12	whatsapp	t	\N	107	\N	2026-08-27 04:53:55.645817	2026-08-27 04:53:55.696106
4cef723f-357e-4a04-aa45-4abdeca7b4f0	wamid.TEST_93b990e0	whatsapp	t	\N	17	\N	2026-08-31 07:29:15.126704	2026-08-31 07:29:15.140465
41daa37d-09f5-4a44-ba7d-c9741f3844c5	wamid.TEST_1f98e4d1	whatsapp	t	\N	25	\N	2026-08-27 04:53:55.703067	2026-08-27 04:53:55.725361
74c5343e-4f1d-4f76-b454-9933aa06c79b	wamid.TEST_0222855a	whatsapp	t	\N	82	\N	2026-08-27 04:54:55.335225	2026-08-27 04:54:55.373547
d26867d5-d7c5-4b13-b8dd-8fa9be977209	wamid.TEST_2c0ceabe	whatsapp	t	\N	123	\N	2026-08-31 07:46:46.842357	2026-08-31 07:46:46.894695
773b6b3b-5723-4b11-a7a0-5062aaf9186c	wamid.TEST_b162883a	whatsapp	t	\N	15	\N	2026-08-27 04:54:55.378685	2026-08-27 04:54:55.39143
963fe84b-182f-4236-8d2f-221f45e01489	wamid.TEST_031ce116	whatsapp	t	\N	87	\N	2026-08-27 05:08:11.299295	2026-08-27 05:08:11.338652
247723f1-142c-4886-ba32-176c7c5d72e5	wamid.TEST_c8d18a05	whatsapp	t	\N	22	\N	2026-08-31 07:46:46.902062	2026-08-31 07:46:46.92107
2dbd784a-4ecc-4421-8673-f678a818a320	wamid.DEDUP_fdd83391	whatsapp	t	\N	108	\N	2026-08-27 05:37:30.861605	2026-08-27 05:37:30.914932
d80fc30c-9302-4227-8fa8-b5880d4c7cf2	m_exact_test_2748aaad	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_2748aaad", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 05:38:44.280974	\N
fb4419a4-25c1-475f-9d5c-eab6be69fdbd	wamid.TEST_8dcd90a1	whatsapp	t	\N	127	\N	2026-08-31 08:18:41.266233	2026-08-31 08:18:41.319693
cd2bd57a-d070-4915-9e2e-0ab3c3cfe5fd	wamid.TEST_db9cf371	whatsapp	t	\N	21	\N	2026-08-31 08:18:41.327102	2026-08-31 08:18:41.345947
aa3fdb0c-14c0-401e-9cd0-acd11afcdf65	wamid.TEST_7d179938	whatsapp	t	\N	84	\N	2026-08-27 06:03:37.674563	2026-08-27 06:03:37.715631
4072e49b-491e-4273-a403-205d95bd97cc	wamid.TEST_cb1b61c2	whatsapp	t	\N	13	\N	2026-08-27 06:03:37.722038	2026-08-27 06:03:37.733162
44474653-e8fd-4756-9360-636169dc9a3a	wamid.TEST_be81939a	whatsapp	t	\N	196	\N	2026-08-31 08:34:27.548314	2026-08-31 08:34:27.631948
8cf92da7-b4ad-4e29-8c03-efddb1639264	wamid.TEST_a4d5ea90	whatsapp	t	\N	87	\N	2026-08-27 06:26:44.816396	2026-08-27 06:26:44.861936
ebefbffd-dd41-4abc-b891-5ab466a506ea	wamid.TEST_cb2270ca	whatsapp	t	\N	36	\N	2026-08-31 08:34:27.647853	2026-08-31 08:34:27.678075
c7ae972e-a242-4b6f-88a9-f5cca01eda43	wamid.DEDUP_38e3b9bb	whatsapp	t	\N	99	\N	2026-08-27 06:28:19.785441	2026-08-27 06:28:19.826156
c512f43a-32c4-48f0-887a-ecb5b8e1a3a9	wamid.TEST_e64ee155	whatsapp	t	\N	135	\N	2026-08-31 09:00:23.781075	2026-08-31 09:00:23.837372
d5711d8a-8b72-412a-a38c-e9a613752421	wamid.TEST_6c7ba2fd	whatsapp	t	\N	22	\N	2026-08-31 09:00:23.846248	2026-08-31 09:00:23.864827
314f6c90-6230-4183-ac80-3591d512fe0a	wamid.TEST_0c677157	whatsapp	t	\N	133	\N	2026-08-31 09:41:27.862392	2026-08-31 09:41:27.918145
3e45b942-c12d-4015-924d-030cfe34742b	wamid.TEST_b53040a4	whatsapp	t	\N	22	\N	2026-08-31 09:41:27.925834	2026-08-31 09:41:27.944961
3a47b36b-2eb0-4c80-aa74-f1b2b679183d	wamid.TEST_99892967	whatsapp	t	\N	104	\N	2026-08-31 10:03:07.628159	2026-08-31 10:03:07.666901
8d75fb40-d3a2-488f-a841-8a28c1146a48	wamid.TEST_29385611	whatsapp	t	\N	15	\N	2026-08-31 10:03:07.673096	2026-08-31 10:03:07.685885
669fd6f2-cdfe-472a-b0ff-163574eff423	wamid.TEST_96fe0d70	whatsapp	t	\N	102	\N	2026-08-31 10:45:49.021558	2026-08-31 10:45:49.069943
f9167632-c637-40fa-a64e-e6d1b819e407	wamid.DEDUP_22e27ab6	whatsapp	t	\N	120	\N	2026-09-01 05:57:57.556466	2026-09-01 05:57:57.607898
f7e2ae62-ef6b-489c-ac2d-d17e18661ba6	wamid.TEST_d24bfd6c	whatsapp	t	\N	132	\N	2026-09-01 05:59:14.580272	2026-09-01 05:59:14.628019
e8c943fb-62ba-4c23-aa5f-eb3c7313f302	wamid.TEST_e39d55e1	whatsapp	t	\N	13	\N	2026-09-01 05:59:14.633128	2026-09-01 05:59:14.644747
36796634-fee0-4826-9975-63cfd8ea442b	wamid.TEST_aa8ace25	whatsapp	t	\N	71	\N	2026-09-01 06:51:02.959179	2026-09-01 06:51:02.990371
a767e76e-78de-444d-a12e-9a13bb5bb519	wamid.TEST_b32b08d5	whatsapp	t	\N	13	\N	2026-09-01 06:51:02.99481	2026-09-01 06:51:03.006614
5f0e38c2-015b-4e29-a5e2-ae655d94cf8e	m_ws_broadcast_test_f440a065	instagram	t	\N	\N	{"sender": {"id": "23086741_5da1"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f440a065", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-09-01 06:52:23.986009	\N
685d562f-ee7d-4c79-b856-6e0db69843ab	wamid.TEST_a62e6693	whatsapp	t	\N	144	\N	2026-09-01 08:34:18.520933	2026-09-01 08:34:18.575121
b7b6d3eb-9008-4105-8ba8-329ba50a8c85	wamid.TEST_36c66762	whatsapp	t	\N	89	\N	2026-08-27 06:37:40.57801	2026-08-27 06:37:40.617074
1aedc0f7-3190-4b0c-a049-9020afcbc695	m_exact_test_b3333d8d	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_b3333d8d", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-09-01 08:36:04.475071	\N
ae39e5b2-72ea-490b-a4d6-cc5207373cae	wamid.TEST_39041c79	whatsapp	t	\N	112	\N	2026-08-26 10:31:30.455798	2026-08-26 10:31:30.520529
9c028b92-8be3-4ffd-9262-ad4851c05511	wamid.TEST_261e55c9	whatsapp	t	\N	123	\N	2026-08-26 12:30:37.613068	2026-08-26 12:30:37.66485
080299ea-d5bf-49eb-a8f6-c348396941ab	wamid.TEST_a09cfc58	whatsapp	t	\N	17	\N	2026-08-27 06:37:40.623636	2026-08-27 06:37:40.63791
c62cb592-b37f-4583-9fcf-79aeedca7f92	wamid.TEST_dcea71e5	whatsapp	t	\N	20	\N	2026-08-26 12:30:37.671503	2026-08-26 12:30:37.689368
8a3b028f-6a58-4e61-93a2-67d153bbed99	wamid.TEST_70397e2f	whatsapp	t	\N	83	\N	2026-08-26 10:59:31.739887	2026-08-26 10:59:31.777597
2e6c59cb-2066-46b3-9aaa-280b84cb0c92	wamid.TEST_2071d305	whatsapp	t	\N	14	\N	2026-08-26 10:59:31.782335	2026-08-26 10:59:31.794778
6cc73891-d6ec-4b20-986f-b1f889060e43	m_ws_broadcast_test_950071f5	instagram	t	\N	\N	{"sender": {"id": "23086741_73a6"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_950071f5", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 12:39:44.139871	\N
023f14b9-b6fa-4e2a-af86-a20514bca258	wamid.TEST_20774d37	whatsapp	t	\N	155	\N	2026-08-26 11:05:40.641651	2026-08-26 11:05:40.706204
7d0caa18-110a-4f52-b04d-65528547e23d	wamid.TEST_ed1b54a1	whatsapp	t	\N	144	\N	2026-08-27 08:12:58.020404	2026-08-27 08:12:58.079717
9c373a4a-a379-476d-87aa-7c8078e54d7d	wamid.TEST_2acc6365	whatsapp	t	\N	81	\N	2026-08-26 11:06:43.890218	2026-08-26 11:06:43.925184
3501818f-431e-4cb2-a8a2-10899a089624	wamid.TEST_13ce16ec	whatsapp	t	\N	16	\N	2026-08-26 11:06:43.929819	2026-08-26 11:06:43.944167
81cde44e-2b40-4646-a924-17dadd688bb3	wamid.TEST_6641bc9c	whatsapp	t	\N	25	\N	2026-08-27 08:12:58.089103	2026-08-27 08:12:58.109904
445e5d2d-be97-42fa-ab10-2404a282cc74	wamid.TEST_4ea3e477	whatsapp	t	\N	228	\N	2026-08-26 13:15:29.466474	2026-08-26 13:15:29.54706
3b0ad22a-0321-4184-861e-956bb0880e1a	wamid.TEST_2d7159b2	whatsapp	t	\N	413	\N	2026-08-27 04:14:23.488741	2026-08-27 04:14:23.672309
0760722d-d1fa-47b2-ace8-c0d9c6c9ce00	wamid.TEST_ed062979	whatsapp	t	\N	51	\N	2026-09-09 09:05:16.277605	2026-09-09 09:05:16.301402
87e360e0-683b-4c4e-934a-962a8f463433	m_ws_broadcast_test_a275a89a	instagram	t	\N	\N	{"sender": {"id": "23086741_e59d"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a275a89a", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 08:15:08.250831	\N
c3541142-9194-4ddb-a8dd-af6a02491b97	wamid.TEST_a62123cd	whatsapp	t	\N	82	\N	2026-08-26 11:22:04.474649	2026-08-26 11:22:04.513597
58e46355-ca30-411d-8f1b-df69f5420523	wamid.TEST_2272a82e	whatsapp	t	\N	89	\N	2026-08-27 04:14:23.699481	2026-08-27 04:14:23.77525
9096716c-9730-4f40-9c52-df1be5b50918	wamid.TEST_6d07077c	whatsapp	t	\N	15	\N	2026-08-26 11:22:04.518724	2026-08-26 11:22:04.531976
1f52a190-490a-4b32-86bb-e830d906542f	m_ws_broadcast_test_a55e1e14	instagram	t	\N	\N	{"sender": {"id": "23086741_bd72"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_a55e1e14", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 11:31:03.657713	\N
005dc001-4092-4a0e-94e4-e936cd9eeb95	wamid.TEST_25ec10aa	whatsapp	t	\N	111	\N	2026-08-31 06:36:55.276903	2026-08-31 06:36:55.317673
2c3c8794-18aa-4143-87ee-b9f897c0243f	m_ws_broadcast_test_977ddda2	instagram	t	\N	\N	{"sender": {"id": "23086741_cae5"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_977ddda2", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-09-01 09:07:53.336169	\N
3a12d1ad-c828-41d9-808c-37ee8ccc2fa5	wamid.TEST_0f94fa93	whatsapp	t	\N	95	\N	2026-08-26 11:51:41.241246	2026-08-26 11:51:41.286195
d7b24310-f4d0-4ae0-99c2-79689f97a717	wamid.TEST_534c6258	whatsapp	t	\N	139	\N	2026-08-27 04:29:00.332953	2026-08-27 04:29:00.392036
9c48fb65-d7c1-4685-acd4-f1b942963954	wamid.TEST_42dc1fd4	whatsapp	t	\N	101	\N	2026-08-31 07:08:02.89058	2026-08-31 07:08:02.942076
9ae0600b-a680-420a-bc62-887f93883867	wamid.TEST_63168df0	whatsapp	t	\N	23	\N	2026-08-27 04:29:00.398451	2026-08-27 04:29:00.418943
2c83e7d8-92cc-473e-8f20-bcf5940a7ac1	wamid.TEST_dfa0ab3f	whatsapp	t	\N	132	\N	2026-09-01 09:57:17.701458	2026-09-01 09:57:17.758136
00310608-62c7-4ffe-aaf7-96e132460bdd	m_ws_broadcast_test_0c502d9c	instagram	t	\N	\N	{"sender": {"id": "23086741_d677"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_0c502d9c", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 04:30:37.396399	\N
11c5115d-3029-4167-87ac-7f0c07941490	wamid.TEST_c5f8077d	whatsapp	t	\N	20	\N	2026-08-31 07:08:02.94886	2026-08-31 07:08:02.966346
771a6259-b216-4f29-8156-f27d0242876b	wamid.TEST_0c7b59ef	whatsapp	t	\N	80	\N	2026-08-31 07:29:15.200639	2026-08-31 07:29:15.233784
c6887834-7b5f-45b3-920e-1c45b9eacc19	wamid.TEST_ba5a68c3	whatsapp	t	\N	15	\N	2026-08-31 07:29:15.238046	2026-08-31 07:29:15.251389
35d41ee4-be39-4c6b-85b0-c2113239389b	wamid.TEST_f9d2f99b	whatsapp	t	\N	83	\N	2026-08-27 04:54:55.450763	2026-08-27 04:54:55.487481
fb8a494e-d2e4-48cf-8f5d-fa0e88af4843	wamid.TEST_9c72c732	whatsapp	t	\N	18	\N	2026-08-27 04:54:55.492247	2026-08-27 04:54:55.508921
84dc4b82-a62f-46ca-842a-5d22f6803f64	wamid.TEST_1a167e2d	whatsapp	t	\N	91	\N	2026-08-27 05:08:11.400358	2026-08-27 05:08:11.439105
99484be6-a8ea-41a6-b0b4-2777cfc928b7	wamid.TEST_39ee1c44	whatsapp	t	\N	142	\N	2026-08-31 07:46:47.01812	2026-08-31 07:46:47.083916
3b4e734c-c05b-4f52-95b3-42aceb503621	wamid.TEST_e5c17c64	whatsapp	t	\N	14	\N	2026-08-27 05:08:11.447038	2026-08-27 05:08:11.459466
23faddce-ecf5-4a10-803d-833737c4e031	m_exact_test_e6b446a7	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_e6b446a7", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-09-01 09:59:02.193753	\N
cc3b1e41-c9fb-4873-bb94-048e3222ef2c	m_ws_broadcast_test_5d87424b	instagram	t	\N	\N	{"sender": {"id": "23086741_b8ea"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_5d87424b", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 05:09:17.084647	\N
325e8435-b5a6-4be4-bd59-f0040f2ea84c	wamid.TEST_9a8606fa	whatsapp	t	\N	32	\N	2026-08-31 07:46:47.093097	2026-08-31 07:46:47.121285
34789394-223b-44c2-92dd-92f216d50f1e	wamid.DEDUP_933587f7	whatsapp	t	\N	132	\N	2026-09-02 04:19:15.433216	2026-09-02 04:19:15.490715
a79c520a-a408-4e43-a6df-0b9d8833d1e8	wamid.TEST_239c898d	whatsapp	t	\N	113	\N	2026-08-27 05:54:12.373208	2026-08-27 05:54:12.428117
a1f344e7-f90e-4b07-841d-4f19d89e66a2	wamid.TEST_fd524aee	whatsapp	t	\N	157	\N	2026-08-31 08:18:41.464979	2026-08-31 08:18:41.521945
c4555fa5-c6f9-4c4e-8ec4-f0a125bf5faa	wamid.TEST_74494427	whatsapp	t	\N	71	\N	2026-08-27 06:03:37.784049	2026-08-27 06:03:37.815839
24bd2d2b-54fc-48c5-a157-24daf7adc4a4	wamid.TEST_2b10884c	whatsapp	t	\N	28	\N	2026-08-31 08:18:41.531589	2026-08-31 08:18:41.555276
81a26480-bd93-4fca-9821-a7d053c73d78	wamid.TEST_8734ea52	whatsapp	t	\N	16	\N	2026-08-27 06:03:37.821551	2026-08-27 06:03:37.836373
3fdebc43-33f6-422c-88d3-da6ca3e19090	wamid.TEST_03c714af	whatsapp	t	\N	171	\N	2026-08-31 08:34:27.799858	2026-08-31 08:34:27.871541
f259994d-9578-46bd-b344-bc69adb756b8	wamid.TEST_f4e9c1f0	whatsapp	t	\N	81	\N	2026-08-27 06:26:44.918376	2026-08-27 06:26:44.951971
3e819b14-b3f9-4383-896b-0d5084edc331	wamid.TEST_1e7c40ec	whatsapp	t	\N	26	\N	2026-08-31 08:34:27.879028	2026-08-31 08:34:27.902322
248e9be6-d2ff-43cf-877f-ec8e5f5d5881	wamid.TEST_131a036e	whatsapp	t	\N	13	\N	2026-08-27 06:26:44.956705	2026-08-27 06:26:44.967919
bf4711f2-e482-4ccc-8a8c-b610be48d516	m_ws_broadcast_test_9d4d2fbd	instagram	t	\N	\N	{"sender": {"id": "23086741_82e9"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_9d4d2fbd", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 06:27:50.602068	\N
ebf4d8a9-7dc3-4ce9-af3b-87e2d13f70de	wamid.TEST_af57fac9	whatsapp	t	\N	150	\N	2026-08-31 09:00:23.971938	2026-08-31 09:00:24.033
9ad7f4e9-c423-4e2e-9b0e-47658563e96f	wamid.TEST_de43bd34	whatsapp	t	\N	27	\N	2026-08-31 09:00:24.043593	2026-08-31 09:00:24.065424
f7a152b8-e85c-4a70-b08a-276e627eac6a	wamid.TEST_b6b0cc47	whatsapp	t	\N	133	\N	2026-08-31 09:41:28.03977	2026-08-31 09:41:28.096289
3341caac-6dcf-4633-8701-d555e9ebeffa	wamid.TEST_b58f31df	whatsapp	t	\N	23	\N	2026-08-31 09:41:28.104162	2026-08-31 09:41:28.12445
4405b2fe-9e18-4b9e-9b30-f580199cce3d	wamid.TEST_4700d5c8	whatsapp	t	\N	88	\N	2026-08-31 10:03:07.747764	2026-08-31 10:03:07.786314
37bbb698-b0b5-4807-ad91-eacaa50a3d40	wamid.TEST_6fa4280f	whatsapp	t	\N	17	\N	2026-08-31 10:03:07.791853	2026-08-31 10:03:07.806612
e40be95f-2ee2-4959-9b2f-50e0b4f17d69	wamid.TEST_10dfa247	whatsapp	t	\N	107	\N	2026-08-27 06:37:40.707413	2026-08-27 06:37:40.758526
685139bd-8e33-422a-9e42-261451f32e2d	wamid.TEST_48b2a99e	whatsapp	t	\N	100	\N	2026-08-26 10:31:30.592905	2026-08-26 10:31:30.639474
100a3372-d080-46a5-94b5-d0698dbe29bc	wamid.TEST_b413ec63	whatsapp	t	\N	22	\N	2026-08-27 06:37:40.764884	2026-08-27 06:37:40.784475
7f7ce53e-6a9a-4994-b366-553fd63e51d3	wamid.TEST_dc88103d	whatsapp	t	\N	24	\N	2026-08-26 10:31:30.644746	2026-08-26 10:31:30.667006
cce2120e-f7d2-45f8-a991-255e5d8eb731	wamid.DEDUP_fd80a2d5	whatsapp	t	\N	127	\N	2026-08-26 12:30:37.771579	2026-08-26 12:30:37.828596
c157968e-9551-4a5c-9df8-10729dea6363	wamid.DEDUP_69ba7c34	whatsapp	t	\N	128	\N	2026-08-27 08:12:58.198074	2026-08-27 08:12:58.251358
70f0a298-3372-4688-967b-7b20e35f7947	wamid.DEDUP_60c1ad8f	whatsapp	t	\N	81	\N	2026-08-26 10:59:31.849344	2026-08-26 10:59:31.88387
936ae9d8-1b6a-4431-970d-471b86d51ad4	m_exact_test_e129da4f	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_e129da4f", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 12:39:44.753443	\N
ee82a80f-3f73-4eb0-a341-8eb875e971be	wamid.TEST_1e177b5a	whatsapp	t	\N	95	\N	2026-08-26 11:05:40.794083	2026-08-26 11:05:40.837958
7679def3-807a-4f06-be97-7574c297bd36	wamid.TEST_163bfb60	whatsapp	t	\N	18	\N	2026-08-26 11:05:40.846445	2026-08-26 11:05:40.861812
145328d1-ba93-458b-9539-80702536ab3c	m_exact_test_46f6b2ea	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_46f6b2ea", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 08:15:08.772513	\N
8b9597a2-61a3-45c7-95ee-d0c640001a33	wamid.TEST_61cd2862	whatsapp	t	\N	80	\N	2026-08-26 11:06:43.999196	2026-08-26 11:06:44.036925
ca28a8ba-9d5f-4deb-b92e-2f8ec358dd6b	wamid.TEST_388b40eb	whatsapp	t	\N	141	\N	2026-08-26 13:15:29.651026	2026-08-26 13:15:29.712435
8709708f-b979-4c7b-8e84-5b195d8d28a7	wamid.TEST_2f1a4ee3	whatsapp	t	\N	78	\N	2026-08-31 06:36:55.373959	2026-08-31 06:36:55.410782
778359c5-1dbf-4c80-a893-1c208bde97f4	wamid.DEDUP_bb6fe7c3	whatsapp	t	\N	90	\N	2026-08-26 11:22:04.591527	2026-08-26 11:22:04.631561
0e0db248-0b78-4890-aefe-b20d4f4b4619	wamid.TEST_bc3d7922	whatsapp	t	\N	23	\N	2026-08-26 13:15:29.721431	2026-08-26 13:15:29.74179
627bd45e-4086-4c86-a696-f1a24f3712b0	m_exact_test_befe03a5	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_befe03a5", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 11:31:05.710969	\N
89ee90b6-f62f-4df3-8692-a4800dfd6ed1	wamid.TEST_83262d64	whatsapp	t	\N	182	\N	2026-08-27 04:14:23.912897	2026-08-27 04:14:23.993844
100020d3-a600-4974-8186-d6872bf325cd	wamid.TEST_8813ced8	whatsapp	t	\N	14	\N	2026-08-31 06:36:55.415692	2026-08-31 06:36:55.428088
0c7558f3-4049-4c88-a89f-6fcbbc74aeb3	wamid.TEST_18c2a11a	whatsapp	t	\N	78	\N	2026-08-26 11:51:41.346306	2026-08-26 11:51:41.380443
63c8a004-299e-4d88-ab54-435bef3f0546	wamid.TEST_edce6451	whatsapp	t	\N	12	\N	2026-08-26 11:51:41.385527	2026-08-26 11:51:41.396524
ab3b1e80-d737-4770-96f4-0c93ac81660a	wamid.DEDUP_405b19f0	whatsapp	t	\N	167	\N	2026-08-27 04:29:00.522511	2026-08-27 04:29:00.597997
e03a7d07-215d-4f82-80da-c04f90b76f52	m_exact_test_358f3ea7	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_358f3ea7", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 04:30:38.220886	\N
256e37ac-e59b-47d3-bdcc-8d9072681d76	wamid.TEST_b8ef14ac	whatsapp	t	\N	82	\N	2026-08-31 07:08:03.025174	2026-08-31 07:08:03.06155
e69ebf25-a3d3-4514-839f-9a75516a5ff8	wamid.TEST_3354ab4c	whatsapp	t	\N	88	\N	2026-08-27 04:53:56.150585	2026-08-27 04:53:56.186833
9d3a6b38-0cdb-4bb2-8bd0-cc31e7a950f4	wamid.TEST_50314328	whatsapp	t	\N	96	\N	2026-08-27 04:54:55.567519	2026-08-27 04:54:55.619361
6ad222ef-2b65-4147-a5b7-58a35934a88a	wamid.TEST_0e0157fb	whatsapp	t	\N	80	\N	2026-08-31 07:29:15.308155	2026-08-31 07:29:15.343265
335a0642-9d8b-414b-80f2-c43e27196ead	wamid.DEDUP_68e43f60	whatsapp	t	\N	116	\N	2026-08-27 05:08:11.538119	2026-08-27 05:08:11.584122
b10bd578-68e3-48d2-9f64-14c9926a42c6	m_exact_test_0ca0966b	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_0ca0966b", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 05:09:17.640269	\N
8f5eb121-a0b8-4fb1-8edf-d0871c5885ee	wamid.TEST_2fe5fb7f	whatsapp	t	\N	101	\N	2026-08-27 05:54:12.498041	2026-08-27 05:54:12.548667
742f0361-c9c2-42ea-a88b-42a245f9f2e4	wamid.TEST_0190cb15	whatsapp	t	\N	20	\N	2026-08-27 05:54:12.562901	2026-08-27 05:54:12.579247
375fd3e1-5759-4a8c-92f8-811eb982b69c	wamid.TEST_18e67825	whatsapp	t	\N	150	\N	2026-08-31 07:46:47.220916	2026-08-31 07:46:47.293153
b1a501df-dcbb-4be8-9037-e8b6fd7455ed	wamid.TEST_53a4cf74	whatsapp	t	\N	92	\N	2026-08-27 06:03:37.897269	2026-08-27 06:03:37.943507
3f1dba94-8c33-49ee-8bbf-ecc815e55085	wamid.DEDUP_6617918a	whatsapp	t	\N	92	\N	2026-08-27 06:26:45.028498	2026-08-27 06:26:45.068666
adfb5941-9611-4044-a382-341c3121ddb5	wamid.TEST_a3333cf2	whatsapp	t	\N	131	\N	2026-08-31 08:18:41.651349	2026-08-31 08:18:41.706266
58e45f9b-55da-4fa8-b4c5-915e831f3e89	m_exact_test_9eaf2847	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_9eaf2847", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 06:27:51.018588	\N
fda5ddc6-455b-40e7-bae5-9dc4ab1bf418	wamid.TEST_a614061f	whatsapp	t	\N	225	\N	2026-08-31 08:34:28.050373	2026-08-31 08:34:28.151138
7ca7dbdb-66bf-4390-8c37-13b7a0866c77	wamid.TEST_21f0d310	whatsapp	t	\N	210	\N	2026-08-31 09:00:24.166743	2026-08-31 09:00:24.297886
44ba769f-b113-4ef8-8b6f-3dbb4767caed	wamid.TEST_8e1aa0d9	whatsapp	t	\N	134	\N	2026-08-31 09:41:28.21905	2026-08-31 09:41:28.27689
85a7b5ae-9512-40d1-bf70-3f3cfc017b44	wamid.TEST_4fba5049	whatsapp	t	\N	92	\N	2026-08-31 10:03:07.876503	2026-08-31 10:03:07.910802
c9d47eea-f16f-40f1-9be4-8aac9f39da82	wamid.TEST_68f09623	whatsapp	t	\N	111	\N	2026-08-31 10:45:49.149086	2026-08-31 10:45:49.20278
0eea65b7-ec70-482d-8a25-5597cdb93398	wamid.TEST_4235022e	whatsapp	t	\N	24	\N	2026-08-31 10:45:49.21084	2026-08-31 10:45:49.231543
60945adb-5359-44b3-8377-c796ef3446d5	m_ws_broadcast_test_61383f6b	instagram	t	\N	\N	{"sender": {"id": "23086741_a470"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_61383f6b", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 10:47:07.098441	\N
fbb55ef9-63ab-4cb8-9592-0c6e44f49c51	wamid.TEST_edd23394	whatsapp	t	\N	103	\N	2026-09-01 05:57:56.72292	2026-09-01 05:57:56.774413
aba00ad1-6e2e-4ef6-8284-bd610bdba9c9	wamid.TEST_715cf16a	whatsapp	t	\N	144	\N	2026-09-01 05:59:23.546473	2026-09-01 05:59:23.598652
6a43469e-8947-4bb8-a80e-3bf6f862384a	wamid.TEST_f64ab917	whatsapp	t	\N	15	\N	2026-09-01 05:59:23.604196	2026-09-01 05:59:23.61689
9b084d8e-3956-48a1-b2a2-d9c18775cd53	wamid.DEDUP_d2f5b58a	whatsapp	t	\N	74	\N	2026-09-01 06:51:03.05648	2026-09-01 06:51:03.088508
cf48bb5e-81d6-41ad-9125-f913d4a31156	m_exact_test_668cf054	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_668cf054", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-09-01 06:52:25.197872	\N
7cb47ac7-95e6-40c1-a30d-151ac02a5aa1	wamid.TEST_0dfffd3f	whatsapp	t	\N	171	\N	2026-09-01 08:34:18.694647	2026-09-01 08:34:18.761881
255165c6-43d3-4c01-bb9a-4ac4641c157a	wamid.TEST_5463bedb	whatsapp	t	\N	23	\N	2026-09-01 08:34:18.770243	2026-09-01 08:34:18.790378
421f181a-de61-460e-8bb1-a325c6eaf5e6	wamid.TEST_d73010f5	whatsapp	t	\N	104	\N	2026-08-27 06:37:40.861232	2026-08-27 06:37:40.903302
f3f63617-8b97-4ab7-8077-d165d974c3f5	wamid.TEST_6fbed84a	whatsapp	t	\N	135	\N	2026-09-01 09:06:10.683894	2026-09-01 09:06:10.742133
a53dc738-651f-420b-96a2-f0f1e49bfe79	wamid.TEST_22da94fa	whatsapp	t	\N	104	\N	2026-08-26 10:31:30.753127	2026-08-26 10:31:30.801793
6e176c94-79df-46f6-bca1-ed0c1996219f	wamid.TEST_9fb43163	whatsapp	t	\N	22	\N	2026-08-26 10:31:30.807954	2026-08-26 10:31:30.827905
3b0e82ae-2551-47d8-87ff-a8d723e8b9a9	wamid.TEST_b5824a0a	whatsapp	t	\N	138	\N	2026-09-01 09:57:17.849448	2026-09-01 09:57:17.911304
10c88fbb-a5ec-4d96-851e-aa1c6b2ba71f	wamid.TEST_fd12b539	whatsapp	t	\N	270	\N	2026-08-26 13:05:28.942397	2026-08-26 13:05:29.034788
d7d27a11-db3a-4d3d-b3b9-93d4c1df04ee	wamid.TEST_ce4e6ac1	whatsapp	t	\N	28	\N	2026-09-01 09:57:17.920079	2026-09-01 09:57:17.944518
3210e9c8-ec6d-4b86-92df-50a095ab3ec6	wamid.TEST_488d8cdb	whatsapp	t	\N	83	\N	2026-08-31 06:36:55.486	2026-08-31 06:36:55.522915
41b45ee4-a9ba-4dff-a7fc-06b5778fef96	wamid.TEST_a6162f09	whatsapp	t	\N	284	\N	2026-08-26 13:15:29.940078	2026-08-26 13:15:30.059188
b33293a3-8afe-42f2-a4ce-4a931ad17866	wamid.TEST_cf75c223	whatsapp	t	\N	79	\N	2026-08-26 11:05:40.918681	2026-08-26 11:05:40.954505
e965c91e-1d56-4cd2-8f43-63be9e199ef2	wamid.TEST_37db0a31	whatsapp	t	\N	58	\N	2026-08-26 13:15:30.075122	2026-08-26 13:15:30.126158
36a27615-be37-498e-bfc8-e972a0f840d6	wamid.TEST_b38bd553	whatsapp	t	\N	17	\N	2026-08-26 11:05:40.959786	2026-08-26 11:05:40.974913
280684ce-bffa-47fc-a3f0-753edd4260b2	wamid.TEST_b3d90721	whatsapp	t	\N	18	\N	2026-08-31 06:36:55.527885	2026-08-31 06:36:55.544678
037326f1-f69c-4f71-9ccf-93906d88f89b	wamid.TEST_89d8130f	whatsapp	t	\N	80	\N	2026-08-26 11:06:44.093668	2026-08-26 11:06:44.127445
c612d39e-d240-48b6-95fd-c7b6941ab2e9	wamid.TEST_50dc87a7	whatsapp	t	\N	141	\N	2026-08-27 04:14:24.083411	2026-08-27 04:14:24.150121
1ac324c3-56d1-43b3-b42e-a8f5a3a8e29e	wamid.TEST_954888d3	whatsapp	t	\N	13	\N	2026-08-26 11:06:44.132496	2026-08-26 11:06:44.144225
94ab3442-d7d4-4fdc-abeb-f9cc939500b1	wamid.TEST_c608ccf5	whatsapp	t	\N	154	\N	2026-09-02 04:19:14.229825	2026-09-02 04:19:14.296972
c0fd6e46-9b1c-468b-93ba-a94119fe6bfd	m_ws_broadcast_test_17dd924e	instagram	t	\N	\N	{"sender": {"id": "23086741_b726"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_17dd924e", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 11:15:44.102719	\N
349eaad8-e516-4ae2-b2b5-976131fa93ef	wamid.TEST_f7b8db23	whatsapp	t	\N	31	\N	2026-08-27 04:14:24.158928	2026-08-27 04:14:24.186543
5ffd9d57-a437-4642-aca4-137d6bdf6e7f	m_ws_broadcast_test_83f16421	instagram	t	\N	\N	{"sender": {"id": "23086741_e193"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_83f16421", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 04:15:49.928268	\N
1bb22519-5d40-46a6-bb23-4b793a1adb42	wamid.TEST_43c012d7	whatsapp	t	\N	106	\N	2026-08-26 11:41:32.087995	2026-08-26 11:41:32.134521
e0a1e2ae-3115-43eb-9c65-c66efd0dcc31	wamid.TEST_289f6f6d	whatsapp	t	\N	81	\N	2026-08-26 11:51:41.454354	2026-08-26 11:51:41.489737
fbf46bcc-5f5a-4674-88ce-e0f4e4617141	wamid.TEST_d6aa37bb	whatsapp	t	\N	145	\N	2026-08-27 04:53:36.074497	2026-08-27 04:53:36.138643
f5415ed6-fbdb-4c46-849c-cc904acc364f	wamid.TEST_b12a288b	whatsapp	t	\N	15	\N	2026-08-26 11:51:41.493591	2026-08-26 11:51:41.507643
cdb43dd5-c291-42df-ad2f-25c4be3a5582	wamid.TEST_8bce9d1e	whatsapp	t	\N	91	\N	2026-08-31 07:08:03.120557	2026-08-31 07:08:03.162841
b94aef6e-85e6-438d-82b3-dd09fa988e14	wamid.TEST_01857726	whatsapp	t	\N	15	\N	2026-08-31 07:08:03.168598	2026-08-31 07:08:03.182163
e4d1dca1-a014-4217-975e-241efeba7eeb	wamid.TEST_afc583bc	whatsapp	t	\N	109	\N	2026-08-27 04:53:56.26696	2026-08-27 04:53:56.308123
cd924ad9-f6bd-4da7-8685-798b84ad4545	wamid.TEST_edc29c0e	whatsapp	t	\N	11	\N	2026-08-27 04:53:56.312527	2026-08-27 04:53:56.321854
630eb698-515d-4ab0-8cbb-3fda671b9875	m_ws_broadcast_test_81d69bc9	instagram	t	\N	\N	{"sender": {"id": "23086741_6d72"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_81d69bc9", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 04:54:43.19994	\N
8242554f-c3e9-4fb9-914b-aecf0ebc99e4	wamid.TEST_4af72e48	whatsapp	t	\N	160	\N	2026-08-27 04:54:55.736835	2026-08-27 04:54:55.799043
794ba12f-4979-4fa7-b563-566cc354fa9a	wamid.TEST_33578f72	whatsapp	t	\N	80	\N	2026-08-31 07:29:15.3978	2026-08-31 07:29:15.433065
7817b946-990f-4d4c-bd58-c86bf443f572	wamid.TEST_78fcc978	whatsapp	t	\N	36	\N	2026-08-27 04:54:55.807487	2026-08-27 04:54:55.839738
48f5f6d9-80a8-4b32-9838-d7cde5c992f7	wamid.TEST_0edf3fe0	whatsapp	t	\N	13	\N	2026-08-31 07:29:15.437752	2026-08-31 07:29:15.448985
457e782a-4db3-4834-a17c-313ec0f52e95	wamid.TEST_65a65326	whatsapp	t	\N	111	\N	2026-08-27 05:37:30.089078	2026-08-27 05:37:30.147357
e61dfcfb-565a-4994-8e20-3e6510ee7877	wamid.TEST_5a1837c0	whatsapp	t	\N	137	\N	2026-08-31 07:46:47.380957	2026-08-31 07:46:47.443663
a5fab8ea-a534-41a0-91a3-5c463942cdd3	wamid.TEST_7b1305a5	whatsapp	t	\N	90	\N	2026-08-27 05:54:12.651246	2026-08-27 05:54:12.690557
e007fd17-215e-4f6f-978b-f5eba2f411dd	wamid.TEST_8540c29d	whatsapp	t	\N	19	\N	2026-08-27 05:54:12.695922	2026-08-27 05:54:12.712599
639af8c5-dfca-4123-bd95-bc2de47614cf	wamid.TEST_d990d6bf	whatsapp	t	\N	28	\N	2026-08-31 07:46:47.451848	2026-08-31 07:46:47.477105
81939a09-7f0b-479c-a884-94126e092b3e	wamid.TEST_6d45e5c8	whatsapp	t	\N	139	\N	2026-08-31 08:18:41.80053	2026-08-31 08:18:41.860935
eb49a560-b9d5-436e-9fad-dc9144709c2a	wamid.TEST_eda3c79d	whatsapp	t	\N	84	\N	2026-08-27 06:03:38.006502	2026-08-27 06:03:38.040528
6cf7f81c-9b5a-42fd-a3fb-d911c08fe273	wamid.TEST_b75d5f3d	whatsapp	t	\N	14	\N	2026-08-27 06:03:38.045172	2026-08-27 06:03:38.057842
1878cc56-c488-4c41-9e6d-73f1731cc238	wamid.TEST_f7b10a26	whatsapp	t	\N	23	\N	2026-08-31 08:18:41.871207	2026-08-31 08:18:41.889325
7bc1e07e-cca4-463f-9c36-fb07ae9f220a	m_ws_broadcast_test_cbb9deb4	instagram	t	\N	\N	{"sender": {"id": "23086741_3af4"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_cbb9deb4", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 06:04:45.536693	\N
87256a16-89a9-4474-9b0c-f667f6487f1a	wamid.TEST_cc805d2e	whatsapp	t	\N	98	\N	2026-08-27 06:28:18.822049	2026-08-27 06:28:18.868828
c0cb32fd-4b51-4bfb-81d3-10b5c4ca217f	wamid.TEST_19ca464c	whatsapp	t	\N	170	\N	2026-08-31 08:34:28.258576	2026-08-31 08:34:28.338792
da817456-7228-48df-9453-95520a121f5e	wamid.TEST_5918bd04	whatsapp	t	\N	30	\N	2026-08-31 08:34:28.348614	2026-08-31 08:34:28.374145
51df3ecd-961f-4a61-acc2-0d44accdb0dc	wamid.TEST_0df9bee7	whatsapp	t	\N	321	\N	2026-08-31 09:00:24.518871	2026-08-31 09:00:24.655416
03d3d780-7ae2-4f37-a450-7427ad670093	wamid.TEST_dd6fb42e	whatsapp	t	\N	48	\N	2026-08-31 09:00:24.671155	2026-08-31 09:00:24.71183
e5e66f12-991a-416d-b63c-c20e394fff5d	wamid.TEST_775d935d	whatsapp	t	\N	140	\N	2026-08-31 09:41:28.369751	2026-08-31 09:41:28.43071
b6d18f80-3e89-4aec-9e6d-9d7ee7d1ad79	wamid.TEST_c1d70344	whatsapp	t	\N	22	\N	2026-08-31 09:41:28.437363	2026-08-31 09:41:28.456339
d62de344-4be8-4a3b-8e95-a90a0180b2f8	wamid.TEST_545b69ac	whatsapp	t	\N	82	\N	2026-08-31 10:03:07.966941	2026-08-31 10:03:08.002299
01ef8999-00a7-4af6-9f96-9fa6516250f6	wamid.TEST_c03ad296	whatsapp	t	\N	13	\N	2026-08-31 10:03:08.007402	2026-08-31 10:03:08.018865
8fc9fac9-c5c9-4b20-8c15-226692141098	wamid.TEST_532a1719	whatsapp	t	\N	98	\N	2026-08-31 10:45:49.302611	2026-08-31 10:45:49.348944
556eed0e-79bf-4143-80c5-8c87a44ae984	wamid.TEST_dce249b6	whatsapp	t	\N	21	\N	2026-08-31 10:45:49.355225	2026-08-31 10:45:49.373122
054d8c72-a8b1-46fb-9bb8-c0fdb8fbcbb1	m_exact_test_cbcb0273	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_cbcb0273", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 10:47:07.980419	\N
59b03ee6-ce28-443b-aa3d-0587f862454e	wamid.TEST_1e24f090	whatsapp	t	\N	87	\N	2026-09-01 05:57:56.841046	2026-09-01 05:57:56.879827
b5a0b8d6-c7ef-4484-9faf-3d583db8fd90	wamid.TEST_1a350294	whatsapp	t	\N	15	\N	2026-09-01 05:57:56.884477	2026-09-01 05:57:56.897566
52fb812a-2327-4422-9c4b-cddceb173323	m_ws_broadcast_test_6474b00f	instagram	t	\N	\N	{"sender": {"id": "23086741_abbf"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_6474b00f", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-09-01 05:59:01.821517	\N
f865b09a-a83b-4e33-83c9-fac9506594e5	wamid.TEST_5fe05e3a	whatsapp	t	\N	77	\N	2026-09-01 06:51:02.589014	2026-09-01 06:51:02.621745
2bc64ad5-719a-465f-93fd-75de21a1162a	wamid.TEST_d2e52df6	whatsapp	t	\N	142	\N	2026-09-01 08:34:18.004021	2026-09-01 08:34:18.067556
826aa4aa-48d0-4399-beac-4909b471cf75	wamid.DEDUP_375a0d0a	whatsapp	t	\N	128	\N	2026-09-01 08:34:18.878326	2026-09-01 08:34:18.931768
ecdc1477-65d0-405c-a800-77862934d883	m_ws_broadcast_test_95eaf1c3	instagram	t	\N	\N	{"sender": {"id": "23086741_2607"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_95eaf1c3", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 12:00:37.271315	\N
ed06ad79-9228-43fe-bc33-86bde609d338	wamid.TEST_7d379b05	whatsapp	t	\N	114	\N	2026-08-27 06:37:40.976325	2026-08-27 06:37:41.028463
a2877668-dfba-4245-a5f2-182b7e6d5f5a	wamid.TEST_fd121d08	whatsapp	t	\N	108	\N	2026-08-26 10:31:30.903893	2026-08-26 10:31:30.952099
1ae03155-d854-495b-9546-2b00024b64de	wamid.TEST_ab1c2463	whatsapp	t	\N	17	\N	2026-08-27 06:37:41.034843	2026-08-27 06:37:41.049306
a59a51b4-b22a-412a-9431-0cf51a9c9f09	wamid.TEST_cc85c677	whatsapp	t	\N	170	\N	2026-08-26 13:05:29.158591	2026-08-26 13:05:29.22919
ccb646f4-c702-4a46-aaf2-0531585cb530	wamid.TEST_05d14e5d	whatsapp	t	\N	25	\N	2026-08-26 13:05:29.238079	2026-08-26 13:05:29.259277
2d64051c-7dd3-4aa8-8a5b-66b87f2bc51d	wamid.TEST_cce22606	whatsapp	t	\N	88	\N	2026-08-26 11:05:41.033606	2026-08-26 11:05:41.074291
fa52ec28-158b-4dd5-9a1a-db53b418bb9a	wamid.DEDUP_fa6f301c	whatsapp	t	\N	81	\N	2026-08-26 11:06:44.197857	2026-08-26 11:06:44.235261
946ab5f3-f179-4605-8665-a4529231d118	m_exact_test_b0e5b811	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_b0e5b811", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 11:15:48.752911	\N
c96f0198-eb14-4eb8-b2a6-3fa0efca70ba	wamid.TEST_382af855	whatsapp	t	\N	78	\N	2026-08-31 06:36:55.60091	2026-08-31 06:36:55.635141
b7cddf82-cbcc-4597-a316-408d8eaebd15	wamid.TEST_56596110	whatsapp	t	\N	261	\N	2026-08-26 13:15:30.348036	2026-08-26 13:15:30.427389
6986e799-aefd-476f-b67a-fc20432451e6	wamid.TEST_bba2265e	whatsapp	t	\N	90	\N	2026-08-26 11:41:32.200868	2026-08-26 11:41:32.23909
8068c068-6f90-4b31-b810-dc978bfb7fc0	wamid.DEDUP_04e89c01	whatsapp	t	\N	183	\N	2026-08-27 04:14:24.318895	2026-08-27 04:14:24.388916
7d9a6152-3514-4a15-899a-6458b53c683a	wamid.TEST_e3761e86	whatsapp	t	\N	15	\N	2026-08-26 11:41:32.243702	2026-08-26 11:41:32.256689
c3fa6640-0cef-43ed-a161-0ca9f2ea4a65	m_exact_test_12842f31	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_12842f31", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 04:15:50.568689	\N
49e1520a-295c-4d7e-9b49-17c4e5387c1a	wamid.TEST_f05f1418	whatsapp	t	\N	94	\N	2026-08-26 11:51:41.571488	2026-08-26 11:51:41.613715
99859a09-23c8-45c5-9f42-6792437f8b90	wamid.DEDUP_1ccf7afc	whatsapp	t	\N	84	\N	2026-08-31 07:08:03.238592	2026-08-31 07:08:03.277058
df986419-8cda-4110-884a-0d38abeca0ad	wamid.TEST_a598a130	whatsapp	t	\N	111	\N	2026-08-27 04:53:36.233755	2026-08-27 04:53:36.272473
a56ae973-e5fc-4910-8da1-36c620b1c57e	m_ws_broadcast_test_e7a6cc1f	instagram	t	\N	\N	{"sender": {"id": "23086741_d6f9"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_e7a6cc1f", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 07:09:29.059193	\N
bd7cc9c2-c75b-4fbd-9cb7-2448d0dbb370	wamid.TEST_f98fc344	whatsapp	t	\N	16	\N	2026-08-27 04:53:36.277694	2026-08-27 04:53:36.291751
d04e9c74-dc40-4aed-9171-3ab21ee47984	wamid.DEDUP_b8c64406	whatsapp	t	\N	91	\N	2026-08-31 07:29:15.51813	2026-08-31 07:29:15.550328
7376123f-b7b1-40c4-a8e4-91cb578d6d66	wamid.DEDUP_508ce522	whatsapp	t	\N	74	\N	2026-08-27 04:53:56.376036	2026-08-27 04:53:56.406538
69287bc8-fdac-4824-a6ed-4d6d3874a468	m_ws_broadcast_test_2bd5330c	instagram	t	\N	\N	{"sender": {"id": "23086741_e634"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_2bd5330c", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 07:31:03.209776	\N
4a5e2e7b-c05e-4c34-9393-c2d12f73375f	m_exact_test_1a006548	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_1a006548", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 04:54:43.652672	\N
17794459-c0ad-4f64-b59b-fe0a36e12076	wamid.DEDUP_9432fc32	whatsapp	t	\N	95	\N	2026-08-27 04:54:55.913853	2026-08-27 04:54:55.951431
d667bb78-a8bd-4123-894c-132f7aef389f	wamid.DEDUP_b82d816b	whatsapp	t	\N	151	\N	2026-08-31 07:46:47.585443	2026-08-31 07:46:47.643756
a14e1ae7-3723-4e2a-bc4c-5fe3cfd06a20	m_ws_broadcast_test_8c48c4e0	instagram	t	\N	\N	{"sender": {"id": "23086741_6c80"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_8c48c4e0", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 07:48:46.15917	\N
93e806e2-48f1-4b3f-8572-a091fb953b84	wamid.TEST_77693522	whatsapp	t	\N	89	\N	2026-08-27 05:37:30.213334	2026-08-27 05:37:30.252428
f00d8aa8-7003-4b1d-aac7-849bb8f9a24a	wamid.TEST_97388499	whatsapp	t	\N	23	\N	2026-08-27 05:37:30.267164	2026-08-27 05:37:30.285075
11b0ed45-f672-48c2-b514-8b179e2e4966	wamid.DEDUP_289b3598	whatsapp	t	\N	128	\N	2026-08-31 08:18:41.975695	2026-08-31 08:18:42.030124
1254b2d6-1619-458f-91c7-25c3587640da	m_ws_broadcast_test_7bf8f151	instagram	t	\N	\N	{"sender": {"id": "23086741_1e38"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_7bf8f151", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 08:20:30.184819	\N
6a174804-87b8-4f79-b07b-ccf6d7646a66	wamid.TEST_23c0afa0	whatsapp	t	\N	88	\N	2026-08-27 05:54:12.774728	2026-08-27 05:54:12.814902
866f9b69-81bc-4d0c-92d8-2aaba2732c4a	wamid.DEDUP_27eed01b	whatsapp	t	\N	167	\N	2026-08-31 08:34:28.499452	2026-08-31 08:34:28.557015
295be4d7-5de7-4d97-84a0-21ddab264843	wamid.DEDUP_49ef3ceb	whatsapp	t	\N	76	\N	2026-08-27 06:03:38.106265	2026-08-27 06:03:38.141417
d40ac805-196b-43a4-a650-1c3d2a6d64f3	m_ws_broadcast_test_8d8cf1c9	instagram	t	\N	\N	{"sender": {"id": "23086741_4326"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_8d8cf1c9", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 08:36:07.315948	\N
c20c2758-8b15-4593-b076-f5d66be79e32	m_exact_test_f985a02d	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_f985a02d", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-27 06:04:46.072562	\N
fee59882-d8d1-4748-9fc6-f8cd9d16f3e6	wamid.DEDUP_2af35769	whatsapp	t	\N	308	\N	2026-08-31 09:00:24.913131	2026-08-31 09:00:25.045731
0c222162-ab94-4783-8268-1428e5fa7139	m_ws_broadcast_test_5b2768a2	instagram	t	\N	\N	{"sender": {"id": "23086741_ed5a"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_5b2768a2", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 09:02:10.613918	\N
988d2126-4b00-48ac-810d-ba2d09eb65b7	wamid.DEDUP_5ba5ecb2	whatsapp	t	\N	182	\N	2026-08-31 09:41:28.558223	2026-08-31 09:41:28.656282
9cc01372-1ad6-49ed-9a63-35c3b958eeb2	m_ws_broadcast_test_156b3261	instagram	t	\N	\N	{"sender": {"id": "23086741_0e1f"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_156b3261", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 09:42:50.291057	\N
fc59e7ec-673e-4366-8271-60b5737e99f2	wamid.DEDUP_99e64d35	whatsapp	t	\N	79	\N	2026-08-31 10:03:08.073316	2026-08-31 10:03:08.107442
6ccd8536-636c-44f1-b38e-95c6f3b791b6	m_ws_broadcast_test_799d7549	instagram	t	\N	\N	{"sender": {"id": "23086741_255a"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_799d7549", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 10:04:29.188549	\N
8a4519ae-6ebc-4a39-be55-765434dfe7c8	wamid.TEST_e0050f8e	whatsapp	t	\N	89	\N	2026-08-31 10:45:49.437973	2026-08-31 10:45:49.476761
cee14251-1365-40c6-8127-32c328cf5286	wamid.TEST_128c733e	whatsapp	t	\N	145	\N	2026-08-31 10:47:30.219879	2026-08-31 10:47:30.273636
d3ac357a-ca05-489b-86fe-25b6250a9f1b	wamid.TEST_91ef0389	whatsapp	t	\N	16	\N	2026-08-31 10:47:30.28025	2026-08-31 10:47:30.293166
9b6813b2-51ce-49e0-8473-5a7921715793	wamid.TEST_a561752c	whatsapp	t	\N	85	\N	2026-09-01 05:57:56.955915	2026-09-01 05:57:56.994659
fbfe1b73-8961-4e0a-a118-3418ae03da13	wamid.TEST_ad4a04af	whatsapp	t	\N	17	\N	2026-09-01 05:57:56.999775	2026-09-01 05:57:57.015132
bb33cfe7-5290-4c5d-9a33-643e018b945c	wamid.TEST_0b14fc85	whatsapp	t	\N	72	\N	2026-09-01 06:51:02.675216	2026-09-01 06:51:02.70706
855721c6-74a0-4124-bb1a-914307dfbaeb	wamid.TEST_1659a6f2	whatsapp	t	\N	11	\N	2026-09-01 06:51:02.711379	2026-09-01 06:51:02.72063
d3a78859-be67-443e-aee4-8e74a327ec05	wamid.TEST_4ac22253	whatsapp	t	\N	132	\N	2026-09-01 08:34:18.157425	2026-09-01 08:34:18.220844
3a3c042e-e614-4921-a3c7-7a7b09c71463	m_exact_test_da2d7149	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_da2d7149", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-26 12:00:37.741507	\N
b507bc20-5b77-4504-a2bc-7da32f62b6b2	wamid.DEDUP_d02d0c0b	whatsapp	t	\N	98	\N	2026-08-27 06:37:41.106017	2026-08-27 06:37:41.157543
5d4da2cb-5d15-4fe2-aca3-3ec623bb6f3d	wamid.TEST_78984555	whatsapp	t	\N	139	\N	2026-09-01 09:06:10.841777	2026-09-01 09:06:10.906957
fb2fe531-2bbb-4b81-8479-24127c7f9a43	wamid.TEST_1a44f0ad	whatsapp	t	\N	109	\N	2026-08-26 10:31:31.010916	2026-08-26 10:31:31.070554
d322ab99-211a-4679-a607-5ef44ffad436	wamid.TEST_f56e947f	whatsapp	t	\N	29	\N	2026-09-01 09:06:10.915048	2026-09-01 09:06:10.940237
f672d6ea-934b-4abd-bea8-42f10213264b	wamid.TEST_dc33a95d	whatsapp	t	\N	21	\N	2026-08-26 10:31:31.076895	2026-08-26 10:31:31.095805
0e24ecdd-12dd-4b50-ba39-693ed01c7b27	wamid.TEST_8d8dbd81	whatsapp	t	\N	77	\N	2026-08-31 06:36:55.687502	2026-08-31 06:36:55.721321
a4c6704c-3cf7-48bc-973d-468ecc9faf2d	m_ws_broadcast_test_5f0884c0	instagram	t	\N	\N	{"sender": {"id": "23086741_78cf"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_5f0884c0", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-26 10:40:32.699424	\N
720398f7-5f2a-4256-874a-b6e2418cd1cf	wamid.TEST_2e03c18e	whatsapp	t	\N	87	\N	2026-08-26 10:59:31.093522	2026-08-26 10:59:31.134818
40fa6895-1521-41f5-813d-a39f9ae06245	wamid.TEST_379e92bf	whatsapp	t	\N	13	\N	2026-08-31 06:36:55.7264	2026-08-31 06:36:55.73758
1792a4f9-81e5-47f4-a9af-d8a81eb61829	wamid.TEST_eba583ed	whatsapp	t	\N	153	\N	2026-08-26 13:15:30.534313	2026-08-26 13:15:30.595764
63488664-e9ff-41fc-b746-1d7d02c7606a	wamid.TEST_068674cb	whatsapp	t	\N	110	\N	2026-08-26 11:05:41.141896	2026-08-26 11:05:41.194015
8cba5310-bfc0-4cb9-8c49-0036500fb65a	m_ws_broadcast_test_f0c78a4d	instagram	t	\N	\N	{"sender": {"id": "23086741_2adb"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_f0c78a4d", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-31 06:38:17.669446	\N
5c1bf2cf-002d-421f-a366-3cafd659a0bd	wamid.TEST_a32e9b84	whatsapp	t	\N	20	\N	2026-08-26 11:05:41.202516	2026-08-26 11:05:41.219235
76a03892-712b-4a2b-8166-61f7681e81bb	wamid.TEST_d923921d	whatsapp	t	\N	25	\N	2026-08-26 13:15:30.607275	2026-08-26 13:15:30.628657
a6f4f711-6447-4aa6-b24c-84c093189eff	wamid.TEST_f2a40063	whatsapp	t	\N	87	\N	2026-08-26 11:22:04.020068	2026-08-26 11:22:04.059999
18b4ec39-2989-4ef3-9781-23fa4a695bd3	wamid.TEST_d15044d9	whatsapp	t	\N	168	\N	2026-08-27 04:28:59.624132	2026-08-27 04:28:59.704153
bd8ae327-b724-468f-b390-28db4261d740	m_exact_test_30f3927a	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_30f3927a", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 07:09:29.95741	\N
da349e86-3cb5-4347-a844-fe3391ae4bc3	wamid.TEST_2d725933	whatsapp	t	\N	85	\N	2026-08-26 11:41:32.319014	2026-08-26 11:41:32.355575
d5583358-325f-4359-9bd5-1a6c960a5ce8	wamid.TEST_5b70f772	whatsapp	t	\N	17	\N	2026-08-26 11:41:32.360305	2026-08-26 11:41:32.375899
dafe83b7-6a56-44c5-a606-eb0a40cb10cf	wamid.TEST_9791e548	whatsapp	t	\N	105	\N	2026-08-27 04:53:36.369059	2026-08-27 04:53:36.414995
49b0441e-32af-4185-a165-130b49a2c0d6	m_exact_test_1fc30067	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_1fc30067", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-09-01 09:07:54.24643	\N
bb6d3929-a422-4745-822a-1dcea151b7eb	wamid.TEST_2050c0e7	whatsapp	t	\N	17	\N	2026-08-27 04:53:36.419805	2026-08-27 04:53:36.435329
f07d2a12-5a58-49f6-97b4-5b4f2de0ea10	m_exact_test_3e807278	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_3e807278", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 07:31:04.369115	\N
66cd103c-317c-42bf-8786-c6c9bdfb913c	wamid.TEST_cb5e9f98	whatsapp	t	\N	95	\N	2026-08-26 11:51:41.683876	2026-08-26 11:51:41.722532
bfb6d7fa-ec68-496f-87e9-b75c706c97fd	wamid.TEST_ffc650bb	whatsapp	t	\N	16	\N	2026-08-26 11:51:41.727893	2026-08-26 11:51:41.741948
03c4f328-3f35-42ef-8fe1-007fd1030dd4	wamid.DEDUP_b97ccb7f	whatsapp	t	\N	140	\N	2026-09-01 09:57:18.039647	2026-09-01 09:57:18.099759
ab83e607-2ee2-4dcb-bc2b-35440745c152	m_exact_test_80537375	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_80537375", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 07:48:46.954994	\N
db950316-896a-498f-b48c-5f8ef93b0660	m_ws_broadcast_test_84a98ede	instagram	t	\N	\N	{"sender": {"id": "23086741_4aad"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_84a98ede", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 04:54:46.801816	\N
84e9d729-1da3-460b-8324-c34a9a45a3d0	wamid.TEST_7c6f9fcd	whatsapp	t	\N	94	\N	2026-08-27 05:08:10.955555	2026-08-27 05:08:11.005298
2ddbea99-c2a5-4417-a3aa-3c79d77f6974	m_exact_test_eb69957d	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_eb69957d", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 08:20:30.984337	\N
865f5bca-0e92-4740-83e9-0f8c08d1f87c	wamid.TEST_acfebf15	whatsapp	t	\N	147	\N	2026-09-02 04:19:14.412145	2026-09-02 04:19:14.473385
7eb5079c-3e29-4e9d-85d0-f832c836dcd5	wamid.TEST_e9fc9998	whatsapp	t	\N	96	\N	2026-08-27 05:37:30.351632	2026-08-27 05:37:30.395447
3e084aa4-30fe-477f-9fdb-3192b7bc1167	wamid.TEST_697807b4	whatsapp	t	\N	27	\N	2026-08-27 05:37:30.402779	2026-08-27 05:37:30.427297
2317b826-5dc6-4d6c-9240-a91c914bb236	m_exact_test_8cc18c35	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_8cc18c35", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 08:36:08.395944	\N
8f6667fe-3cb8-420f-b712-3794028bcf66	wamid.TEST_322c60c2	whatsapp	t	\N	34	\N	2026-09-02 04:19:14.482658	2026-09-02 04:19:14.512381
76a927dc-1940-4a70-8225-a9821033c075	m_exact_test_51431321	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_51431321", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 09:02:12.128345	\N
ea2757f3-b574-482a-91df-376fc496e662	wamid.TEST_419c120c	whatsapp	t	\N	91	\N	2026-08-27 05:54:12.873178	2026-08-27 05:54:12.916013
f076c3b7-1925-4af1-ad68-47544059dde8	wamid.TEST_2b42d4cd	whatsapp	t	\N	21	\N	2026-08-27 05:54:12.922852	2026-08-27 05:54:12.940691
6086be8b-a5e2-414b-b6b8-bcb6796a1010	m_ws_broadcast_test_343736e6	instagram	t	\N	\N	{"sender": {"id": "23086741_829d"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_343736e6", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-08-27 05:55:18.512515	\N
7d5ea830-1f26-488d-a297-7ce2302d3eeb	m_exact_test_02a922e4	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_02a922e4", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-08-31 09:42:51.160044	\N
73611ba6-e1e6-4bed-98e3-403c162d633a	wamid.TEST_13a740b5	whatsapp	t	\N	104	\N	2026-08-27 06:26:44.475934	2026-08-27 06:26:44.515707
cfcb09e2-1e73-4fc2-8586-e8061a402821	wamid.TEST_2db82c72	whatsapp	t	\N	76	\N	2026-08-27 06:28:19.290651	2026-08-27 06:28:19.325867
cbdffaac-b970-4821-91ba-3a9a0dbc6f0d	wamid.TEST_7d70c880	whatsapp	t	\N	15	\N	2026-08-27 06:28:19.330299	2026-08-27 06:28:19.344101
98ebb256-148e-4a84-9e9a-5531e03937c4	wamid.TEST_8f4126da	whatsapp	t	\N	82	\N	2026-09-01 05:57:57.074374	2026-09-01 05:57:57.109827
224d6066-81bb-4db9-92da-42482af541a9	wamid.TEST_5ccb30e3	whatsapp	t	\N	75	\N	2026-09-01 06:51:02.771988	2026-09-01 06:51:02.806316
90cc150c-04f0-494b-be55-d19db932a94f	wamid.TEST_70a616cb	whatsapp	t	\N	16	\N	2026-09-01 06:51:02.810811	2026-09-01 06:51:02.82517
a06c31e2-1d74-4331-b8cc-e90350e26f63	wamid.TEST_c755adc2	whatsapp	t	\N	21	\N	2026-09-01 08:34:18.229227	2026-09-01 08:34:18.247251
19e0bea4-a7fc-471f-b7a2-76e2f7a92971	wamid.TEST_97f65ef3	whatsapp	t	\N	186	\N	2026-09-01 09:06:11.075606	2026-09-01 09:06:11.147903
290e5839-4d1b-4c16-adef-e0f093979d5e	wamid.TEST_151f5ca5	whatsapp	t	\N	27	\N	2026-09-01 09:06:11.155187	2026-09-01 09:06:11.180074
b342c844-3401-4b63-ab12-3bbaeee8e110	wamid.TEST_9b2bb9cc	whatsapp	t	\N	161	\N	2026-09-01 09:57:17.147047	2026-09-01 09:57:17.227842
fa657dd1-a91c-4867-83ee-ee916445bf7b	m_ws_broadcast_test_c3e3e3bf	instagram	t	\N	\N	{"sender": {"id": "23086741_80dd"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_c3e3e3bf", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-09-01 09:59:01.315044	\N
2457d4b6-d4ac-4c9c-bea8-3db438f0c740	wamid.TEST_b6f73e2a	whatsapp	t	\N	319	\N	2026-09-02 04:19:14.730111	2026-09-02 04:19:14.863603
03f1001b-5a36-4cdf-a7b4-f4c0ad6bbd0a	wamid.TEST_9747b46c	whatsapp	t	\N	60	\N	2026-09-02 04:19:14.878903	2026-09-02 04:19:14.931521
a73e4849-f25e-48b4-8803-9115937e1070	m_ws_broadcast_test_4949b38c	instagram	t	\N	\N	{"sender": {"id": "23086741_ec96"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_4949b38c", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-09-02 04:21:00.528028	\N
8d5f9bf9-8aae-4ac5-bf15-9c4eaca23857	m_exact_test_d024dcc6	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_d024dcc6", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-09-02 04:21:01.698437	\N
7d2b80f2-8044-4c3a-a4a8-0d9c153f0af0	wamid.TEST_d63429c5	whatsapp	t	\N	44	\N	2026-09-09 09:05:16.333594	2026-09-09 09:05:16.354361
3532e361-ee75-448c-b604-d5cc3a122a05	wamid.TEST_3e8a1911	whatsapp	t	\N	8	\N	2026-09-09 09:05:16.358381	2026-09-09 09:05:16.365316
394d4bd8-a74f-4d33-b6ab-8419df9f9b43	wamid.TEST_18f3f805	whatsapp	t	\N	41	\N	2026-09-09 09:05:16.395236	2026-09-09 09:05:16.414101
5d72839f-f82d-40fb-8791-6e9286ff8056	wamid.TEST_29870693	whatsapp	t	\N	8	\N	2026-09-09 09:05:16.41751	2026-09-09 09:05:16.425101
2038ea84-a4c0-4722-bb8b-71c1ed3ea99a	wamid.TEST_c4b9e9b6	whatsapp	t	\N	42	\N	2026-09-09 09:05:16.454755	2026-09-09 09:05:16.474439
d288bbc3-70f8-4b62-a516-8b71e22cbc89	wamid.TEST_8650564e	whatsapp	t	\N	41	\N	2026-09-09 09:05:16.503455	2026-09-09 09:05:16.522369
21092245-25ca-4957-8614-40ba283c690d	wamid.TEST_d0aa9418	whatsapp	t	\N	7	\N	2026-09-09 09:05:16.525891	2026-09-09 09:05:16.532638
5a057f46-e30c-4f81-9345-74dfdd858c38	wamid.DEDUP_61515f88	whatsapp	t	\N	42	\N	2026-09-09 09:05:16.562228	2026-09-09 09:05:16.581191
61c96ad2-899e-4909-a985-e928074cc5f5	wamid.TEST_567c780c	whatsapp	t	\N	49	\N	2026-09-09 09:19:23.514778	2026-09-09 09:19:23.539255
d8fbd1b7-aef7-4203-8aed-b4ed7d7c753d	wamid.TEST_a07c0fb6	whatsapp	t	\N	43	\N	2026-09-09 09:19:23.572695	2026-09-09 09:19:23.592197
ac8598f3-6434-4464-bc76-6443fc797af5	wamid.TEST_3fccb8e3	whatsapp	t	\N	10	\N	2026-09-09 09:19:23.595426	2026-09-09 09:19:23.604804
460968f0-c6d9-4e1e-a915-00c26952a772	wamid.TEST_cad8dbec	whatsapp	t	\N	44	\N	2026-09-09 09:19:23.644359	2026-09-09 09:19:23.66308
5be5a115-2312-4381-b342-80b05794a4d7	wamid.TEST_9bc69b7a	whatsapp	t	\N	8	\N	2026-09-09 09:19:23.666398	2026-09-09 09:19:23.674367
7d8d3b2c-6c29-425a-8874-696831538bf3	wamid.TEST_871718bc	whatsapp	t	\N	44	\N	2026-09-09 09:19:23.70574	2026-09-09 09:19:23.726673
2d266921-c566-46fb-bbcf-f57c88d1947e	wamid.TEST_640b069f	whatsapp	t	\N	50	\N	2026-09-09 09:19:23.760591	2026-09-09 09:19:23.78318
401ed7cc-a3d7-412f-b389-bfbb03090223	wamid.TEST_ad0dd080	whatsapp	t	\N	8	\N	2026-09-09 09:19:23.787009	2026-09-09 09:19:23.794293
d5b8c4f4-74e5-446a-904c-8f30ddfed949	wamid.DEDUP_b5865d87	whatsapp	t	\N	43	\N	2026-09-09 09:19:23.823828	2026-09-09 09:19:23.843299
1d1402e2-b737-4a34-9b71-6d153a9ed1ac	mid_38bf6a1f1515	facebook	t	\N	\N	{"sender": {"id": "test_fb_dfdbf919"}, "recipient": {"id": "mock_page_id"}, "message": {"mid": "mid_38bf6a1f1515", "text": "Hello SupportHub from Messenger!"}}	2026-09-09 09:21:39.487258	\N
a6678a1c-7715-4645-92bb-40b522b8559d	wamid.TEST_1db7d309	whatsapp	t	\N	53	\N	2026-09-09 09:24:15.135269	2026-09-09 09:24:15.162761
d8a15e3a-a9f9-4d5b-add6-27a0f3a1ee4e	wamid.TEST_9af03400	whatsapp	t	\N	51	\N	2026-09-09 09:24:15.206896	2026-09-09 09:24:15.226774
f963786b-d50e-476d-9859-597acb98f070	wamid.TEST_6be84523	whatsapp	t	\N	8	\N	2026-09-09 09:24:15.230111	2026-09-09 09:24:15.237432
57d5a26c-804b-4b3e-89b3-491dfe1a0a15	wamid.TEST_03397b00	whatsapp	t	\N	40	\N	2026-09-09 09:24:15.267856	2026-09-09 09:24:15.285763
bc817ceb-b9b7-4390-92fa-613403ec6fe0	wamid.TEST_18721f0a	whatsapp	t	\N	8	\N	2026-09-09 09:24:15.289049	2026-09-09 09:24:15.296609
33f114b8-2c95-46e1-9817-cc66b3fe6de0	wamid.TEST_48aa8864	whatsapp	t	\N	41	\N	2026-09-09 09:24:15.326854	2026-09-09 09:24:15.345145
b7fadaaf-25fb-4960-af4d-1ec02a0fdb73	wamid.TEST_bfc454f5	whatsapp	t	\N	42	\N	2026-09-09 09:24:15.374052	2026-09-09 09:24:15.392809
df46036b-cd94-4e21-ae95-6bdc95a9f7db	wamid.TEST_5e232bfc	whatsapp	t	\N	7	\N	2026-09-09 09:24:15.396299	2026-09-09 09:24:15.403039
7d010836-00de-4680-bad1-3c9223faa414	wamid.DEDUP_ba19fecc	whatsapp	t	\N	41	\N	2026-09-09 09:24:15.432246	2026-09-09 09:24:15.450641
7021e182-6a64-4d5c-bb28-928c0e2ca257	m_ws_broadcast_test_d33d30ea	instagram	t	\N	\N	{"sender": {"id": "23086741_c8cd"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_ws_broadcast_test_d33d30ea", "text": "WS BROADCAST INTEGRATION TEST"}}	2026-09-09 09:25:31.751995	\N
d45eba83-f67c-40d5-b98a-65a7f97429a5	m_exact_test_34580e08	instagram	t	\N	\N	{"sender": {"id": "2308674163238603"}, "recipient": {"id": "17841435478991883"}, "timestamp": 1786363356298, "message": {"mid": "m_exact_test_34580e08", "text": "PRODUCTION REALTIME FINAL TEST 1835"}}	2026-09-09 09:25:32.124841	\N
67439933-73a7-45e2-9e8e-f2e2e2cda73c	9097a732-bb97-4c3b-8593-80723ea0d834	whatsapp	f	\N	\N	\N	2026-09-09 11:11:39.853022	\N
\.


--
-- Name: ai_settings ai_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_settings
    ADD CONSTRAINT ai_settings_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: audit_log audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT audit_log_pkey PRIMARY KEY (id);


--
-- Name: automations automations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.automations
    ADD CONSTRAINT automations_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- Name: channel_integrations channel_integrations_channel_type_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channel_integrations
    ADD CONSTRAINT channel_integrations_channel_type_key UNIQUE (channel_type);


--
-- Name: channel_integrations channel_integrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channel_integrations
    ADD CONSTRAINT channel_integrations_pkey PRIMARY KEY (id);


--
-- Name: company company_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (company_id);


--
-- Name: csat_ratings csat_ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.csat_ratings
    ADD CONSTRAINT csat_ratings_pkey PRIMARY KEY (id);


--
-- Name: email_logs email_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_logs
    ADD CONSTRAINT email_logs_pkey PRIMARY KEY (id);


--
-- Name: email_templates email_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_templates
    ADD CONSTRAINT email_templates_pkey PRIMARY KEY (id);


--
-- Name: kb_articles kb_articles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kb_articles
    ADD CONSTRAINT kb_articles_pkey PRIMARY KEY (id);


--
-- Name: kb_chunk_embeddings kb_chunk_embeddings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kb_chunk_embeddings
    ADD CONSTRAINT kb_chunk_embeddings_pkey PRIMARY KEY (id);


--
-- Name: macros macros_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.macros
    ADD CONSTRAINT macros_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (order_item_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: quick_replies quick_replies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.quick_replies
    ADD CONSTRAINT quick_replies_pkey PRIMARY KEY (id);


--
-- Name: refunds refunds_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_pkey PRIMARY KEY (refund_id);


--
-- Name: returns returns_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_pkey PRIMARY KEY (return_id);


--
-- Name: sellers sellers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_pkey PRIMARY KEY (seller_id);


--
-- Name: shipments shipments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_pkey PRIMARY KEY (shipment_id);


--
-- Name: ticket_embeddings ticket_embeddings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_embeddings
    ADD CONSTRAINT ticket_embeddings_pkey PRIMARY KEY (id);


--
-- Name: ticket_embeddings ticket_embeddings_ticket_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_embeddings
    ADD CONSTRAINT ticket_embeddings_ticket_id_key UNIQUE (ticket_id);


--
-- Name: tickets tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: webhook_events webhook_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.webhook_events
    ADD CONSTRAINT webhook_events_pkey PRIMARY KEY (id);


--
-- Name: ix_audit_log_action; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_log_action ON public.audit_log USING btree (action);


--
-- Name: ix_audit_log_actor_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_log_actor_id ON public.audit_log USING btree (actor_id);


--
-- Name: ix_audit_log_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_log_created_at ON public.audit_log USING btree (created_at);


--
-- Name: ix_audit_log_entity_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_log_entity_id ON public.audit_log USING btree (entity_id);


--
-- Name: ix_audit_log_entity_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_log_entity_type ON public.audit_log USING btree (entity_type);


--
-- Name: ix_audit_log_ticket_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_audit_log_ticket_id ON public.audit_log USING btree (ticket_id);


--
-- Name: ix_csat_ratings_customer_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_csat_ratings_customer_id ON public.csat_ratings USING btree (customer_id);


--
-- Name: ix_csat_ratings_ticket_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_csat_ratings_ticket_id ON public.csat_ratings USING btree (ticket_id);


--
-- Name: ix_email_logs_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_logs_created_at ON public.email_logs USING btree (created_at);


--
-- Name: ix_email_logs_recipient_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_logs_recipient_email ON public.email_logs USING btree (recipient_email);


--
-- Name: ix_email_logs_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_logs_status ON public.email_logs USING btree (status);


--
-- Name: ix_email_logs_ticket_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_logs_ticket_id ON public.email_logs USING btree (ticket_id);


--
-- Name: ix_email_templates_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_email_templates_name ON public.email_templates USING btree (name);


--
-- Name: ix_kb_articles_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_kb_articles_category ON public.kb_articles USING btree (category);


--
-- Name: ix_kb_articles_title; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_kb_articles_title ON public.kb_articles USING btree (title);


--
-- Name: ix_kb_chunk_embeddings_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_kb_chunk_embeddings_category ON public.kb_chunk_embeddings USING btree (category);


--
-- Name: ix_kb_chunk_embeddings_chunk_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_kb_chunk_embeddings_chunk_id ON public.kb_chunk_embeddings USING btree (chunk_id);


--
-- Name: ix_kb_chunk_embeddings_source_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_kb_chunk_embeddings_source_id ON public.kb_chunk_embeddings USING btree (source_id);


--
-- Name: ix_kb_chunk_embeddings_source_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_kb_chunk_embeddings_source_type ON public.kb_chunk_embeddings USING btree (source_type);


--
-- Name: ix_kb_chunk_embeddings_vector; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_kb_chunk_embeddings_vector ON public.kb_chunk_embeddings USING hnsw (embedding public.vector_cosine_ops);


--
-- Name: ix_messages_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_messages_created_at ON public.messages USING btree (created_at);


--
-- Name: ix_messages_external_message_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_messages_external_message_id ON public.messages USING btree (external_message_id);


--
-- Name: ix_messages_ticket_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_messages_ticket_id ON public.messages USING btree (ticket_id);


--
-- Name: ix_quick_replies_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_quick_replies_category ON public.quick_replies USING btree (category);


--
-- Name: ix_quick_replies_tenant_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_quick_replies_tenant_id ON public.quick_replies USING btree (tenant_id);


--
-- Name: ix_ticket_embeddings_ticket_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_ticket_embeddings_ticket_id ON public.ticket_embeddings USING btree (ticket_id);


--
-- Name: ix_ticket_embeddings_vector; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ticket_embeddings_vector ON public.ticket_embeddings USING hnsw (embedding public.vector_cosine_ops);


--
-- Name: ix_tickets_agent_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_agent_id ON public.tickets USING btree (agent_id);


--
-- Name: ix_tickets_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_category ON public.tickets USING btree (category);


--
-- Name: ix_tickets_channel; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_channel ON public.tickets USING btree (channel);


--
-- Name: ix_tickets_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_created_at ON public.tickets USING btree (created_at);


--
-- Name: ix_tickets_customer_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_customer_id ON public.tickets USING btree (customer_id);


--
-- Name: ix_tickets_priority; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_priority ON public.tickets USING btree (priority);


--
-- Name: ix_tickets_ref; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_tickets_ref ON public.tickets USING btree (ref);


--
-- Name: ix_tickets_sla_due_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_sla_due_at ON public.tickets USING btree (sla_due_at);


--
-- Name: ix_tickets_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tickets_status ON public.tickets USING btree (status);


--
-- Name: ix_users_channel; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_channel ON public.users USING btree (channel);


--
-- Name: ix_users_channel_customer_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_channel_customer_id ON public.users USING btree (channel_customer_id);


--
-- Name: ix_users_company_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_company_id ON public.users USING btree (company_id);


--
-- Name: ix_users_customer_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_customer_id ON public.users USING btree (customer_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_phone; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_phone ON public.users USING btree (phone);


--
-- Name: ix_webhook_events_channel; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_webhook_events_channel ON public.webhook_events USING btree (channel);


--
-- Name: ix_webhook_events_event_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_webhook_events_event_id ON public.webhook_events USING btree (event_id);


--
-- Name: ix_webhook_events_processed; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_webhook_events_processed ON public.webhook_events USING btree (processed);


--
-- Name: ix_webhook_events_received_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_webhook_events_received_at ON public.webhook_events USING btree (received_at);


--
-- Name: audit_log audit_log_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT audit_log_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.users(id);


--
-- Name: audit_log audit_log_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT audit_log_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.tickets(id);


--
-- Name: automations automations_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.automations
    ADD CONSTRAINT automations_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: categories categories_company_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_company_fk FOREIGN KEY (company_id) REFERENCES public.company(company_id) ON DELETE CASCADE;


--
-- Name: categories categories_parent_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_parent_fk FOREIGN KEY (parent_category_id) REFERENCES public.categories(category_id) ON DELETE SET NULL;


--
-- Name: csat_ratings csat_ratings_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.csat_ratings
    ADD CONSTRAINT csat_ratings_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.users(id);


--
-- Name: csat_ratings csat_ratings_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.csat_ratings
    ADD CONSTRAINT csat_ratings_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.tickets(id);


--
-- Name: email_logs email_logs_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_logs
    ADD CONSTRAINT email_logs_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.tickets(id);


--
-- Name: kb_articles kb_articles_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kb_articles
    ADD CONSTRAINT kb_articles_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: macros macros_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.macros
    ADD CONSTRAINT macros_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: messages messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id);


--
-- Name: messages messages_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.tickets(id);


--
-- Name: order_items order_items_order_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_fk FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;


--
-- Name: order_items order_items_product_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_fk FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;


--
-- Name: orders orders_company_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_company_fk FOREIGN KEY (company_id) REFERENCES public.company(company_id) ON DELETE CASCADE;


--
-- Name: orders orders_customer_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_fk FOREIGN KEY (customer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: payments payments_customer_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_customer_fk FOREIGN KEY (customer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: payments payments_order_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_fk FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;


--
-- Name: products products_category_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_fk FOREIGN KEY (category_id) REFERENCES public.categories(category_id) ON DELETE CASCADE;


--
-- Name: products products_company_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_company_fk FOREIGN KEY (company_id) REFERENCES public.company(company_id) ON DELETE CASCADE;


--
-- Name: products products_seller_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_seller_fk FOREIGN KEY (seller_id) REFERENCES public.sellers(seller_id) ON DELETE CASCADE;


--
-- Name: refunds refunds_customer_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_customer_fk FOREIGN KEY (customer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: refunds refunds_order_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_order_fk FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;


--
-- Name: refunds refunds_return_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_return_fk FOREIGN KEY (return_id) REFERENCES public.returns(return_id) ON DELETE CASCADE;


--
-- Name: returns returns_customer_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_customer_fk FOREIGN KEY (customer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: returns returns_item_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_item_fk FOREIGN KEY (order_item_id) REFERENCES public.order_items(order_item_id) ON DELETE CASCADE;


--
-- Name: returns returns_order_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_order_fk FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;


--
-- Name: sellers sellers_company_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_company_fk FOREIGN KEY (company_id) REFERENCES public.company(company_id) ON DELETE CASCADE;


--
-- Name: shipments shipments_order_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_order_fk FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE;


--
-- Name: ticket_embeddings ticket_embeddings_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_embeddings
    ADD CONSTRAINT ticket_embeddings_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.tickets(id) ON DELETE CASCADE;


--
-- Name: tickets tickets_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.users(id);


--
-- Name: tickets tickets_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict WVVQKilai0qfhEiBNhYUJXz8ruseAERGowBh7R2NPlxSxYL3r5UPrQLvB7AIJK0


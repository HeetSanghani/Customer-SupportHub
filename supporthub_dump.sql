--
-- PostgreSQL database dump
--

\restrict qHz3h6RyHGrFxTlxx64M2U0iMGKAKK16MGRvXiHENzypDriTcqGAHwXZdnHoUFY

-- Dumped from database version 16.14 (Debian 16.14-1.pgdg12+1)
-- Dumped by pg_dump version 16.14 (Debian 16.14-1.pgdg12+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

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
    embedding public.vector(1536),
    views integer NOT NULL,
    helpful_count integer NOT NULL,
    published boolean NOT NULL,
    created_by uuid,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
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
    avatar_url character varying(500),
    totp_secret character varying,
    totp_enabled boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    email_signature text
);


--
-- Name: ai_settings ai_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_settings
    ADD CONSTRAINT ai_settings_pkey PRIMARY KEY (id);


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
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


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

\unrestrict qHz3h6RyHGrFxTlxx64M2U0iMGKAKK16MGRvXiHENzypDriTcqGAHwXZdnHoUFY

--
-- PostgreSQL database dump
--

\restrict KUeC4Dw4VRJOeWaAQJ2OWEhB879NnjQiUOh2q2NhzxXebPSXpps6oqUwjdhHLND

-- Dumped from database version 16.14 (Debian 16.14-1.pgdg12+1)
-- Dumped by pg_dump version 16.14 (Debian 16.14-1.pgdg12+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: ai_settings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ai_settings (id, enabled, auto_resolve, suggest_replies, auto_summary, sentiment_detection, confidence_threshold, model_name, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, email, name, password_hash, role, status, avatar_url, totp_secret, totp_enabled, created_at, updated_at, email_signature) FROM stdin;
0973322f-a661-40b3-bc6f-d957ac0625dc	email-test@supporthub.local	System Email Verifier	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-08-05 12:09:21.971209	2026-08-05 12:09:21.971337	\N
4a47565a-2ec1-404a-8f05-07490e1d9384	customer@supporthub.com	Customer User	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-07-28 08:00:26.475598	2026-07-28 08:00:26.47581	\N
56c164e8-bc29-4a30-916e-b5abe72ca52f	david.b@example.com	David Brown	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-07-31 05:50:46.599914	2026-07-31 05:50:46.600091	\N
63c1bca2-e351-49d5-8f43-a145bfc4ac52	test2@example.com	Test User	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-07-28 06:58:26.512776	2026-07-28 06:58:26.513007	\N
646b7a11-99f7-4721-b183-f74dbec4bcc5	agent@supporthub.com	Agent User	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	agent	active	\N	\N	f	2026-07-28 08:00:26.026051	2026-07-28 08:00:26.026223	\N
79884e27-3a53-4e94-b52f-8d3ab4cb8e59	priya.p@example.com	Priya Patel	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	manager	active	\N	\N	f	2026-07-31 05:50:45.65584	2026-07-31 05:50:45.656063	\N
98d7e49a-2551-4bb8-b425-3b3226046c7e	heets.brainerhub@gmail.com	Heet Patel	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	admin	active	\N	\N	f	2026-07-28 07:00:30.539021	2026-07-28 07:00:30.539253	\N
a0dbbcab-de50-46b6-a534-b3638ad07785	testcustomer@example.com	Testcustomer	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-08-04 08:15:53.070251	2026-08-04 08:15:53.070508	\N
b5f32890-e30b-4197-9861-40917ebe35d8	michael.c@example.com	Michael Chen	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-07-31 05:50:47.049447	2026-07-31 05:50:47.049627	\N
b7e52df6-21dd-4fa2-bb0d-11961f360cd1	manager@supporthub.com	Manager User	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	manager	active	\N	\N	f	2026-07-28 08:00:25.605791	2026-07-28 08:00:25.605974	\N
c64e3806-b382-4689-9f1a-94114205ce5f	admin@supporthub.com	Admin User	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	admin	active	\N	\N	f	2026-07-28 08:00:25.178256	2026-07-28 08:00:25.178446	\N
d2367976-fc79-4ad2-a1b6-debb378f9575	rahul.s@example.com	Rahul Sharma	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-07-31 05:50:45.212147	2026-07-31 05:50:45.212351	\N
decbc6cf-6fff-4590-b026-1a8ae9d6f15d	alex.t@example.com	Alex Thomas	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-07-31 05:50:46.141957	2026-07-31 05:50:46.142195	\N
f1f7ab32-97bb-41a0-8aa0-989664bfa2fa	elena.r@example.com	Elena Rostova	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-07-31 05:50:47.493631	2026-07-31 05:50:47.493835	\N
f44fdb74-d8b3-4c89-a337-e5d972b0fde6	sarah.j@example.com	Sarah Johnson	$2b$12$BOUQAi9klRhUqPinpbtkz.zGEVGegsb1Y4VNk7by5oasZZ9GtwNW6	customer	active	\N	\N	f	2026-07-31 05:50:44.760054	2026-07-31 05:50:44.760301	\N
\.


--
-- Data for Name: tickets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets (id, ref, customer_id, agent_id, subject, category, channel, status, priority, sla_due_at, sla_breached, sentiment, ai_confidence, ai_resolved, ai_summary, deleted_at, created_at, updated_at) FROM stdin;
c36dc01d-d17b-4314-9637-89468d768f40	TCK-42081	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	New Support Query	general	website_chat	resolved	high	2026-07-29 17:31:29.177955	f	\N	\N	t	\N	\N	2026-07-29 09:31:29.179205	2026-07-29 09:31:29.179898
02c8922b-d6bd-4125-96d4-91e726de716b	TCK-68768	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	how can i change my password	technical	website_chat	resolved	medium	2026-07-28 18:06:06.87391	f	\N	\N	t	\N	\N	2026-07-28 10:06:06.874325	2026-07-28 10:06:06.874496
37334a0c-89e9-4e9d-953c-902c0bf02ec6	TCK-88115	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Issue Resolved	general	website_chat	resolved	medium	2026-07-29 18:31:05.08372	f	\N	\N	t	\N	\N	2026-07-29 10:31:05.08502	2026-07-29 10:31:05.085829
844e7711-2832-4ca2-bcda-0eb9892feb8f	TCK-80598	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	GENERAL Support Query	general	website_chat	new	medium	2026-07-30 15:52:46.890004	f	\N	\N	f	\N	\N	2026-07-30 07:52:46.893251	2026-07-30 07:52:46.894005
3c874d66-d5ff-41ab-b61e-df633cb87cb1	TCK-99986	a0dbbcab-de50-46b6-a534-b3638ad07785	\N	Need help with my account	email	email	new	medium	\N	f	\N	\N	f	\N	\N	2026-08-04 08:15:53.109724	2026-08-04 08:15:53.11013
adaa9dee-e0d0-45f1-84fe-a098d509412f	TCK-62911	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	Hello	general	website_chat	resolved	medium	2026-07-28 16:50:07.132461	f	\N	\N	f	\N	\N	2026-07-28 08:50:07.133666	2026-07-28 09:19:36.885316
0c89ef0a-db9f-4fa9-ac8e-5f08d108f270	TCK-87434	0973322f-a661-40b3-bc6f-d957ac0625dc	\N	[Test Connection] Email Channel Diagnostic Verification	email_test	email	new	low	\N	f	\N	\N	f	\N	\N	2026-08-05 12:09:21.979009	2026-08-05 12:09:21.979135
c88e8bad-58d2-445c-bdcd-376b733a5d4e	TCK-35781	0973322f-a661-40b3-bc6f-d957ac0625dc	\N	[Test Connection] Email Channel Diagnostic Verification	email_test	email	new	low	\N	f	\N	\N	f	\N	\N	2026-08-05 12:10:43.970996	2026-08-05 12:10:43.971549
3c16bc6f-db9b-471f-aeff-fb266d3c905b	TCK-34057	c64e3806-b382-4689-9f1a-94114205ce5f	\N	Inquiry about billing details	billing	email	new	medium	2026-08-05 20:17:02.046627	f	\N	\N	f	\N	\N	2026-08-05 12:17:02.046971	2026-08-05 12:17:02.047095
76eda5ce-025d-41c8-9c2d-38e6fb755267	TCK-54787	4a47565a-2ec1-404a-8f05-07490e1d9384	646b7a11-99f7-4721-b183-f74dbec4bcc5	Upgrade plan and payment options	general	website_chat	resolved	medium	2026-07-29 17:04:15.60535	f	\N	\N	t	\N	\N	2026-07-29 09:04:15.606915	2026-07-29 09:04:15.607723
7903d2cf-33ea-49fd-855f-749b0ee82e6b	TCK-66381	0973322f-a661-40b3-bc6f-d957ac0625dc	646b7a11-99f7-4721-b183-f74dbec4bcc5	[Test Connection] Email Channel Diagnostic Verification	email_test	email	new	low	\N	f	\N	\N	f	\N	\N	2026-08-05 12:10:22.515145	2026-08-05 12:10:22.515262
be326382-a999-41cd-abec-78e7cbe40b4a	TCK-70849	c64e3806-b382-4689-9f1a-94114205ce5f	\N	Inquiry about billing details	billing	email	resolved	medium	2026-08-05 20:21:54.491542	f	\N	\N	f	\N	\N	2026-08-05 12:21:54.491828	2026-08-05 13:44:41.534792
48231bbd-7ed9-4589-a228-0a9dc6032818	TCK-50653	4a47565a-2ec1-404a-8f05-07490e1d9384	646b7a11-99f7-4721-b183-f74dbec4bcc5	Inquiry about billing details	billing	email	new	medium	2026-08-05 20:16:31.82663	f	\N	\N	f	\N	\N	2026-08-05 12:16:31.826883	2026-08-05 12:16:31.826987
6ef2fc35-1afd-40cc-8036-53b0f203d501	TCK-89269	4a47565a-2ec1-404a-8f05-07490e1d9384	646b7a11-99f7-4721-b183-f74dbec4bcc5	How do I reset my password	general	website_chat	resolved	medium	2026-07-28 18:11:11.647944	f	\N	\N	t	\N	\N	2026-07-28 10:11:11.64845	2026-07-28 10:11:11.648704
9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	TCK-98676	98d7e49a-2551-4bb8-b425-3b3226046c7e	646b7a11-99f7-4721-b183-f74dbec4bcc5	Test again - password help	email	email	new	medium	\N	f	\N	\N	f	\N	\N	2026-08-04 08:46:30.850904	2026-08-04 10:05:30.474839
a6b15714-29b0-4930-a495-f55fd5e404da	TCK-16534	4a47565a-2ec1-404a-8f05-07490e1d9384	646b7a11-99f7-4721-b183-f74dbec4bcc5	Password Reset Guide	general	website_chat	resolved	medium	2026-07-29 18:49:47.060878	f	\N	\N	t	\N	\N	2026-07-29 10:49:47.062179	2026-07-29 10:49:47.062846
bc18f726-c70e-4250-ba9d-aa776450af95	TCK-38811	4a47565a-2ec1-404a-8f05-07490e1d9384	646b7a11-99f7-4721-b183-f74dbec4bcc5	I Forget My Password	technical	website_chat	resolved	urgent	2026-07-28 09:45:26.271633	f	\N	\N	t	\N	\N	2026-07-28 08:45:26.274178	2026-07-28 09:21:05.27951
f3ba1e50-7e93-4680-aef0-17bab9230f05	TCK-18834	4a47565a-2ec1-404a-8f05-07490e1d9384	646b7a11-99f7-4721-b183-f74dbec4bcc5	Upgrade plan and payment options	general	website_chat	resolved	medium	2026-07-29 17:11:40.930726	f	\N	\N	f	\N	\N	2026-07-29 09:11:40.931334	2026-07-29 09:11:40.93167
4f9eee37-9f3a-4f2c-b0f7-8f91660fc888	TCK-38315	4a47565a-2ec1-404a-8f05-07490e1d9384	\N	GENERAL Support Query	general	website_chat	resolved	medium	2026-08-05 22:12:50.601956	f	\N	\N	t	\N	\N	2026-08-05 14:12:50.602443	2026-08-05 14:12:50.602679
8b143420-d8df-4fc9-a1fa-c1faba787dc7	TCK-23865	4a47565a-2ec1-404a-8f05-07490e1d9384	646b7a11-99f7-4721-b183-f74dbec4bcc5	GENERAL Support Query	general	website_chat	resolved	medium	2026-08-05 21:52:39.594603	f	\N	\N	t	\N	\N	2026-08-05 13:52:39.595082	2026-08-05 13:52:39.595306
36f0f5f3-c7b8-4465-986c-2b5eb7a98df4	TCK-39190	4a47565a-2ec1-404a-8f05-07490e1d9384	646b7a11-99f7-4721-b183-f74dbec4bcc5	GENERAL Support Query	general	website_chat	resolved	medium	2026-07-31 12:54:00.220156	f	\N	\N	t	\N	\N	2026-07-31 04:54:00.222063	2026-07-31 04:54:00.223241
daba0e8c-c1f1-49d8-8854-562752613ea8	TCK-11107	4a47565a-2ec1-404a-8f05-07490e1d9384	646b7a11-99f7-4721-b183-f74dbec4bcc5	Production Server Down	general	website_chat	resolved	urgent	2026-07-29 17:37:42.506164	f	\N	\N	t	\N	\N	2026-07-29 09:37:42.508278	2026-07-29 09:37:42.509371
\.


--
-- Data for Name: audit_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.audit_log (id, actor_id, action, entity_type, entity_id, ticket_id, diff_json, ip_address, created_at) FROM stdin;
28006373-4fa3-4413-a88a-4d9a1dd82f77	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.new", "new_status": "TicketStatus.open"}	\N	2026-07-28 09:11:49.703033
78a06249-fa93-4c74-a511-41e69fa590fc	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.open"}	\N	2026-07-28 09:11:52.505474
6b1c69a2-578e-400c-9205-38d34bac6119	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:23.219723
234e54c6-d038-4702-824d-fc747a6e7fbb	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:34.679319
ae8f8fa9-d4a4-4e48-871f-ae32cbe2b37a	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:35.060825
0328a31b-5aa4-4a39-bee4-f3f839870090	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:35.261628
034cda69-2ddb-42a9-8cad-c55784e2d519	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.resolved"}	\N	2026-07-28 09:14:35.939338
e8c38753-5b28-4cf3-8e6a-5a3ce5976993	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.resolved", "new_status": "TicketStatus.resolved"}	\N	2026-07-28 09:14:36.383825
b92c6a95-c3de-43e5-9326-92d267cabba8	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.resolved", "new_status": "TicketStatus.resolved"}	\N	2026-07-28 09:14:36.534083
95553dba-2190-47e1-8ed4-3d6ebc42b91c	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.resolved", "new_status": "TicketStatus.resolved"}	\N	2026-07-28 09:14:36.719061
05ae0ec3-6a75-4028-b67a-37b2269a4d55	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.resolved", "new_status": "TicketStatus.open"}	\N	2026-07-28 09:14:40.861969
ec6ec991-0f2a-4975-9a4f-caf77c2c69eb	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.open"}	\N	2026-07-28 09:14:41.012891
7531cdfa-8ac9-4be7-9923-faa87296e4c0	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:43.130676
0e51e9fb-c70a-4812-aa9d-3d9b7410351c	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:43.271558
a4f5c93e-bf18-4a9c-9cb7-5192c77b930a	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:43.444607
e852c601-7a62-4877-909c-51fec1e85485	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:43.611023
5694047f-8ee5-48f2-a92d-a1f00b64f559	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:43.770133
c8c778aa-afd2-4805-a119-2adb311cbd49	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:43.92957
848dafa9-41d9-4b32-a9f4-91c8f0352ab5	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:44.092718
9b71078e-e463-46dc-88df-aaf5f8c296d1	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:44.251754
fe929764-5523-43e8-95da-7ac9a9b0d237	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:14:44.392917
d40320d9-c256-496a-90d3-fcb5b4294b0e	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:33.968064
82ab2ff2-efb3-42a9-bb23-e6ed6c6ecf4f	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:37.092698
534527e6-cb12-4821-b70a-fd855a24595d	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:37.878532
f2452784-a603-4e0f-acbb-681f4c945a92	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:38.11
29192f52-c070-4c49-ae60-34a28cca8d57	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:38.281624
f06cdc66-40e7-45f2-9a23-51ba8f1850b9	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:38.460636
7cbc5f7b-c85b-47ac-bc65-d583c419d604	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:38.630487
fc3a851a-f79a-4cdb-af07-61a384c50cba	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:38.821795
6bf316e0-773b-429b-96e9-7daef916cbbf	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:47.292118
e55c96ab-4630-420c-8f0b-f1e0523946f5	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:47.811222
f735a1e5-ec94-41f8-9094-557100ec77d8	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:47.980745
0d078f25-6c69-4586-aed1-5eac5517a32f	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:48.112827
cd90f8e9-1daa-4bff-859f-9fba4f8b0916	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:48.291683
3e60f262-8510-4ecd-8f1c-063a8c928481	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:48.459567
860ca6cd-1a7b-4d18-b380-de2c778ad2b2	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:48.62212
8763f6a8-e84d-4f60-bcdf-bbcc9bc5c9cc	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.open"}	\N	2026-07-28 09:16:12.860272
04d1bd16-03d1-4886-8ba5-6dd1e2ee63dd	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:48.951774
58da3419-5459-4fbc-be82-671c3c5ec0ca	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.open"}	\N	2026-07-28 09:16:13.020834
09e10426-4037-4cdf-b364-17de3a87d534	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:15:49.120877
33d4bdc8-9124-4b50-b6d7-882097070871	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.open"}	\N	2026-07-28 09:16:12.392037
dd8f6a8a-499c-4595-b10d-b8cf4cd1db8e	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.open"}	\N	2026-07-28 09:16:13.209786
0779a412-bbd3-481d-96e0-124a37e700a2	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:16:53.175868
00ed0d5c-4203-451f-bd0a-b9f19b217ffd	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	adaa9dee-e0d0-45f1-84fe-a098d509412f	adaa9dee-e0d0-45f1-84fe-a098d509412f	{"old_status": "TicketStatus.waiting", "new_status": "TicketStatus.resolved"}	\N	2026-07-28 09:19:36.88671
d9899cdc-ed2a-41d0-829e-94ef3b6e16e8	646b7a11-99f7-4721-b183-f74dbec4bcc5	ticket.updated	ticket	bc18f726-c70e-4250-ba9d-aa776450af95	bc18f726-c70e-4250-ba9d-aa776450af95	{"old_status": "TicketStatus.new", "new_status": "TicketStatus.waiting"}	\N	2026-07-28 09:21:05.2801
f418ad7c-de9d-46a1-a898-4ad9c317c6be	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.new", "new_status": "TicketStatus.resolved"}	\N	2026-08-05 13:40:48.732016
333c1b8a-a047-4bf1-8bb2-7937ad64a738	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.resolved"}	\N	2026-08-05 13:42:13.232842
54c86c92-fc84-4069-9eb2-72b4f8bbf5f6	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.open"}	\N	2026-08-05 13:42:20.384617
6f874197-36cf-4afc-916c-569a8b8c2323	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.resolved"}	\N	2026-08-05 13:42:20.396128
26b16e03-148d-47cc-bad1-d73bccf78796	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.resolved", "new_status": "TicketStatus.open"}	\N	2026-08-05 13:42:37.080103
cc5b9230-f920-4124-be2f-4336ee9df691	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.resolved"}	\N	2026-08-05 13:42:37.09187
5ea69406-3db6-4abc-9065-11f9b1f276a2	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.resolved", "new_status": "TicketStatus.open"}	\N	2026-08-05 13:43:03.545098
2c6f20e0-32ec-4aec-9130-2f36c9dcb70a	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.resolved"}	\N	2026-08-05 13:43:03.554351
d0ee258b-db74-495a-9a9f-b86e1af90999	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.resolved", "new_status": "TicketStatus.open"}	\N	2026-08-05 13:43:29.319768
8a889c18-5257-49a0-b72f-01bd5b3f256a	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.resolved"}	\N	2026-08-05 13:43:29.329306
e1ad2d54-e7a6-4c48-87b4-25ca7b9ee615	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.resolved", "new_status": "TicketStatus.open"}	\N	2026-08-05 13:43:50.71493
5d190328-f20d-44a8-b194-3d0322e9283b	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.resolved"}	\N	2026-08-05 13:43:50.727944
0263fc73-0eb4-4eac-a063-c12f687b6182	c64e3806-b382-4689-9f1a-94114205ce5f	ticket.updated	ticket	be326382-a999-41cd-abec-78e7cbe40b4a	be326382-a999-41cd-abec-78e7cbe40b4a	{"old_status": "TicketStatus.open", "new_status": "TicketStatus.resolved"}	\N	2026-08-05 13:44:41.53503
\.


--
-- Data for Name: automations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.automations (id, name, trigger_json, action_json, is_active, priority, created_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: channel_integrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.channel_integrations (id, channel_type, status, credentials_encrypted, display_name, weekly_volume, last_checked_at, created_at, updated_at, config_json) FROM stdin;
7bc70a80-1e0c-4b95-9b62-751473ae6fd2	email	connected	\N	support@supporthub.com	2	\N	2026-08-05 06:10:41.009055	2026-08-05 06:10:41.009055	\N
c423ee30-5941-467e-ac26-2a74ca61a952	website_chat	connected	\N	chat.supporthub.com	12	\N	2026-08-05 06:10:41.009055	2026-08-05 06:10:41.009055	\N
\.


--
-- Data for Name: csat_ratings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.csat_ratings (id, ticket_id, customer_id, rating, comment, created_at) FROM stdin;
55cc3739-48a8-4b99-b145-43154ec87363	a6b15714-29b0-4930-a495-f55fd5e404da	4a47565a-2ec1-404a-8f05-07490e1d9384	5	Response is perfact!	2026-07-29 11:16:13.510198
55c4086d-7d6f-4512-bd42-20f62f0d7f18	37334a0c-89e9-4e9d-953c-902c0bf02ec6	4a47565a-2ec1-404a-8f05-07490e1d9384	5	model accuracy is perfact	2026-07-29 11:53:32.269369
6202b5ab-db9a-4e32-9755-6454365ef3de	c36dc01d-d17b-4314-9637-89468d768f40	4a47565a-2ec1-404a-8f05-07490e1d9384	5	Super fast resolution! The AI agent resolved my invoice update in less than 2 minutes.	2026-07-29 09:45:29.179205
0f68014f-30ff-4283-917c-e4aedc5a6663	bc18f726-c70e-4250-ba9d-aa776450af95	4a47565a-2ec1-404a-8f05-07490e1d9384	5	Emma was extremely helpful on live chat and fixed my account settings immediately.	2026-07-28 09:07:26.274178
d3fab5ee-b8c6-49be-bd7c-ab2a7c148c24	02c8922b-d6bd-4125-96d4-91e726de716b	4a47565a-2ec1-404a-8f05-07490e1d9384	5	Outstanding support! Received my bypass link quickly and was able to log back in.	2026-07-28 10:36:06.874325
df5ec7b8-2e8c-4391-87f2-fb9af9ae758a	76eda5ce-025d-41c8-9c2d-38e6fb755267	4a47565a-2ec1-404a-8f05-07490e1d9384	4	Good overall response. The issue was solved well within the SLA timeline.	2026-07-29 09:34:15.606915
02671caa-ef6e-4d66-8968-00e1a515718d	adaa9dee-e0d0-45f1-84fe-a098d509412f	4a47565a-2ec1-404a-8f05-07490e1d9384	5	Very smooth process. Highly impressed with the omnichannel support experience.	2026-07-28 09:05:07.133666
b1b902cb-938e-425f-afe6-00a63bc51074	6ef2fc35-1afd-40cc-8036-53b0f203d501	4a47565a-2ec1-404a-8f05-07490e1d9384	4	Clear instructions provided by the agent. Thank you!	2026-07-28 10:56:11.64845
f2337d8c-365f-474d-9e9b-b9c0fbddf2f2	be326382-a999-41cd-abec-78e7cbe40b4a	c64e3806-b382-4689-9f1a-94114205ce5f	5	Submitted via 1-Click Email Survey (5/5 stars)	2026-08-05 13:42:13.261468
4088adc4-c5ed-49ad-ae8a-0706b8ec4acc	4f9eee37-9f3a-4f2c-b0f7-8f91660fc888	4a47565a-2ec1-404a-8f05-07490e1d9384	5		2026-08-05 15:00:20.463829
5ba8e99d-71a2-4b3c-b1fc-e75c6020cf37	8b143420-d8df-4fc9-a1fa-c1faba787dc7	4a47565a-2ec1-404a-8f05-07490e1d9384	5		2026-08-05 15:00:42.953708
4d097641-3a15-4e79-93bd-2ac6f7d01b95	36f0f5f3-c7b8-4465-986c-2b5eb7a98df4	4a47565a-2ec1-404a-8f05-07490e1d9384	5		2026-08-05 15:01:06.980314
411366a8-d4b7-45fc-8000-eba9a555a930	daba0e8c-c1f1-49d8-8854-562752613ea8	4a47565a-2ec1-404a-8f05-07490e1d9384	5		2026-08-05 15:01:26.501468
\.


--
-- Data for Name: email_logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.email_logs (id, ticket_id, recipient_email, subject, status, error_detail, created_at) FROM stdin;
976d22d5-a9bf-45ee-940d-8d2ddf077ce4	\N	customer@supporthub.com	Resolution & CSAT Survey [TCK-70849]	delivered	\N	2026-08-05 14:15:37.544747
a4173a10-9000-4837-9547-acc076c3e57f	\N	customer@supporthub.com	Your Ticket TCK-70849 Has Been Updated	delivered	\N	2026-08-05 14:15:37.545006
a7f8a5bd-5625-4da8-9f67-68ce01ef9b25	\N	admin@supporthub.com	Diagnostic Test Connection	sent	\N	2026-08-05 14:15:37.545212
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

COPY public.kb_articles (id, title, category, body, embedding, views, helpful_count, published, created_by, created_at, updated_at) FROM stdin;
493dfc50-b8fe-4c36-95a3-fb7fb2e4f874	What are our standard business hours?	General	Our global support team operates across multiple time zones to ensure you always get the help you need!\n\n- Level 1 Support (General Inquiries): Available 24/7, 365 days a year.\n- Level 2 Support (Technical & Billing): Available Monday through Friday, 9:00 AM to 6:00 PM (EST).\n- Dedicated Account Managers: Available during standard local business hours based on your region.\n\nOutside of standard business hours, our AI Agent will automatically answer common questions or route your ticket to the correct team for the next morning.\n	[0.005209331,0.005045395,-0.005133035,-0.0065788915,-0.0035624818,0.024526222,-0.004125994,-0.019665765,0.015294608,-0.052182946,-0.012683635,-0.00076164654,-0.0124240555,0.005929129,0.0059063183,0.00049999345,0.016936388,-0.001383551,0.0052734227,-0.004549721,0.008023172,-0.0022353346,-0.013851496,0.018304493,0.011667156,0.02091428,0.0023264138,0.009036035,-0.0038432481,0.13754348,-0.00558784,0.0054318802,-0.030768495,-0.020336168,-0.0009121626,-0.017659402,-0.023715846,0.017643876,-0.0022976268,-0.022724252,0.0073950873,0.026977513,-0.006672333,0.0006117588,-0.013680053,0.013757679,-0.003554472,-0.0075069824,0.01659648,-0.017661389,0.017431846,0.010837388,0.0088044545,-0.024206957,0.010427237,0.006484822,0.016305618,0.0019468574,-0.0024244231,0.019024221,-0.014475358,0.0008109285,0.006328866,0.016106851,-0.0006752336,-0.009561225,-0.0059276153,-0.012881882,0.024335293,-0.00426907,0.0026764558,0.034060754,-0.019226698,-0.0055984645,-0.011640002,-0.029392468,-0.021091437,0.016388146,-0.029331183,-0.010939886,0.016470274,0.016604587,-0.03245729,-0.025675867,-0.008214308,0.009039853,0.004652376,0.0021489274,-0.00025750184,0.026763616,0.009962002,-0.013852728,-0.0057808734,-0.0042339847,-0.011268373,0.0068067815,-0.019907618,-0.018904742,-0.0067174556,0.016044917,0.011379365,-0.012544689,0.039987348,-0.0018327262,0.008747825,0.0049459687,0.00439689,0.0052408273,0.010106002,0.010830728,-0.018809512,-0.172141,0.0010014788,-0.0068802726,-0.0020798896,-0.04042275,-0.025060495,0.013884265,0.0064178007,-0.006926625,0.01462979,-0.0067910426,-0.0067269667,-0.012358972,0.009846761,0.028321225,0.022091987,0.011130236,-0.0020437026,0.0188205,0.044780567,0.020975435,-0.00061416783,-0.023702059,0.0065550976,-0.028870218,-0.009852184,0.005179148,0.012584741,-0.0057732733,-0.007769798,0.0025752024,-0.019644411,0.008084209,-0.034213487,-0.0052685146,0.013621463,-0.018456891,0.0100182975,-0.009495898,-0.016621377,-0.019463973,0.0063244044,0.0163674,0.004480862,0.003195115,-0.012668023,0.011827066,-0.006324781,-0.014760969,0.0018145061,-0.001393627,-0.024042053,-0.005725686,-0.031593703,-0.003122537,-0.0048123207,0.019548956,-0.008645715,0.018455315,-0.019592667,-0.0088547785,0.0024897626,0.0033886565,0.0066877594,0.012516517,0.013760971,0.01404601,0.013972162,0.013464754,-0.00073539646,-0.035002656,0.005570934,-0.005669192,0.008033476,0.011488054,-0.027949698,-0.013439515,-0.0067502265,0.00064746535,0.010206459,-0.017703097,0.010256944,-0.020844411,-0.008577466,-0.0062467693,0.004273588,-0.020127319,-0.005997393,0.027987584,-0.008438665,0.022759903,-0.011525655,0.025483944,-0.01172333,-0.0038077293,-0.023156187,0.0067758076,0.029857846,-0.00232784,0.03497513,0.009211299,-0.01511839,-0.008200148,-0.010267261,-0.03957339,-0.0058289496,0.043502938,0.018938797,0.021451514,-0.0026480102,0.027622357,0.009595797,0.007125724,-0.0034836696,0.009405051,0.012218599,0.02658489,0.009960515,0.0053947875,0.017598165,0.008838335,0.036817383,-0.0077644666,0.010360419,-0.011084111,-0.004948658,-0.0024031622,-0.0031279842,-0.006322428,0.0032544516,-0.0032372775,0.0022916282,0.019117596,-0.00574954,-0.018734196,-0.010094619,0.008191583,0.016305232,-0.00031656385,0.00671472,-0.005982212,-0.007752328,0.010668105,-0.0032530257,-0.010196854,-0.003800922,0.0009330297,0.042381726,-0.005997049,-0.0065156473,0.014611067,0.01686101,0.0052814065,0.024509227,-0.008921718,0.010619651,-0.022844259,0.021496158,-0.005275669,-0.008657081,0.0017034289,-0.011414568,-0.0017718353,-0.013898695,0.007902252,-0.00232705,-0.0029456376,-0.006288112,-0.012063897,-0.016089493,-0.016350074,-0.017790899,0.006756671,0.0018386618,0.0018614223,-0.015358248,-0.0072439504,0.023728775,0.0037489294,0.021091819,0.008553635,0.024880994,0.004201118,0.01866155,0.052491847,0.0013467744,-0.015962249,-0.010423855,0.008859096,-0.023719938,-0.014839098,-0.0071213194,0.016286787,0.0035588979,-0.007341148,0.01506603,0.01897153,0.0020678309,-0.016348625,-0.034590475,0.003705657,-0.013099102,-0.011916418,0.008294224,0.014986436,0.023194144,0.0057199993,-0.019376379,-0.1291583,-0.002757305,-0.029723445,0.018451756,-0.0011758127,0.028698009,0.0022409367,-0.0017131559,-0.00088085217,-0.008113854,-0.007299149,0.006018021,0.0142678805,-0.00305877,-0.0004163303,8.4640014e-05,0.005458912,0.0001133304,-0.01050774,0.001962863,0.00036500616,0.0031810587,-0.18765536,-0.027365796,0.023116779,0.004702218,0.011012894,-0.04389441,0.0085127605,0.0005146567,0.0039923093,-0.0018361454,-0.0024938544,-0.016965568,0.02794802,0.011858666,-0.012191929,0.01369163,0.014183134,0.020974727,-0.023462448,0.010706708,-0.012758219,0.019022044,-0.009961592,-0.005137265,-0.007882988,-0.01304419,-0.010593737,-0.022663932,0.0042984253,-0.0061915587,-0.008442499,0.0028009126,0.0064576506,0.015049653,0.009658605,-0.019841334,0.011808293,-0.030051924,-0.009374485,-0.017043175,0.010469237,0.012370438,6.927394e-05,0.023880867,-0.015529025,0.018425122,-0.006235542,-0.014770766,0.015470498,-0.008280146,0.012312901,-0.0054589123,-0.0050120414,-0.008967035,-0.022642735,-0.012766773,-0.01235908,-0.007912096,-0.014526258,0.02860171,0.02248329,0.031547993,0.003689034,0.018856384,0.0060165026,0.012122144,-0.0098882355,-0.001427979,-0.0249201,-0.006968748,-0.011131642,0.0028750591,0.0015926806,-0.0010994689,0.0035913838,-0.01650646,-0.015296585,-0.012533059,-0.0011209293,-0.0016440179,0.010744866,0.0027067086,-0.014508689,0.017331941,0.0034874524,0.010485471,-0.030241016,0.0075007896,0.034180578,0.004235654,-0.022102121,-0.016848126,-0.019098384,0.010251546,0.0061229044,-0.010596466,0.0070904926,0.008046927,0.0017275414,-0.0113267675,-0.019521222,0.015506105,-0.0012734876,-0.018005,0.006323336,0.0024136105,0.019360533,0.0045647216,-0.0049779746,0.024884302,0.0018225684,-0.0050213835,0.025275946,0.011807346,0.0016953724,-0.004635075,0.01682662,-0.0028266867,0.0025719008,0.00088808325,-0.0027109582,-0.000582053,-0.024675421,0.0062883664,0.011074041,-0.0047186892,-0.014205676,-0.0047313008,0.00046393133,-0.005568833,-0.001748009,0.01622311,0.00103119,0.010965985,0.0028304625,0.013577714,-0.022716692,0.002745523,-0.011592725,0.0057550664,-0.022082735,0.022873573,-0.019052338,0.013443029,-0.004690144,0.035838462,0.02470445,0.020658163,0.0023066627,-0.0055520474,-0.023257669,0.021523038,-0.02622918,0.01383751,-0.03424295,0.0077458825,-0.010724266,0.0017421459,-0.004644409,0.010971678,0.0018309876,-0.0101296,0.004991994,0.005349411,0.007243144,-0.032348443,-0.16637143,0.013808964,0.0066668764,0.006948004,-0.0071270727,0.0041700117,-0.0071363794,-0.0010903149,-0.020499125,-0.0049665384,0.02037114,-0.0119340755,-0.011894028,0.0022390175,-0.009574278,-0.0013185547,0.023019351,-0.019826638,-0.028881228,0.009489954,0.018416733,-0.028444938,0.00052537426,0.009246093,0.020612318,-0.013587915,0.004700139,-0.002431213,0.020503622,-0.03195551,-0.019529589,-0.02776901,-0.0040608435,-0.01586039,-0.006600345,2.8351227e-05,0.00981626,0.0039007731,0.0037395554,0.0020564846,0.01554475,0.005497043,0.040563866,-0.007313616,0.027386319,-0.017786792,0.02035514,-0.055550594,-0.013940379,0.0010902515,-0.04171922,-0.017242258,-0.021737464,0.00829994,0.019979144,0.014854698,-0.0076038335,-0.018450474,-0.013171213,-0.0029928857,-0.012644834,0.007831102,0.023375725,0.014555293,0.022280086,-0.018825652,0.007043854,0.078235246,-0.0030947935,-0.010336079,-0.0012304776,0.017740022,-0.004306279,0.0039228313,0.0053859036,-0.0024126444,-0.013942005,0.0014201751,-0.03537699,0.017190514,0.019831896,-0.019224992,0.021213844,0.010136745,0.009133404,0.016740633,0.017859152,-0.019411024,-0.01894579,0.008652374,-0.014933271,0.003967285,0.013391855,-0.0186008,-0.0068575344,-0.00809924,0.04100963,-0.00046623696,-0.0065301084,0.01394178,-0.018247353,-0.008621556,-0.0067757564,0.01114976,-0.006135832,-0.016989274,-0.00018156705,0.0066938526,0.022846,0.014741748,0.003182723,-0.00046341398,0.017187579,-0.022615662,-0.0034057696,-0.0224536,-0.014225632,0.0004228088,0.0008907546,-0.020282708,0.008434839,-0.0066531734,-0.016518816,-0.0034826675,0.005848657,0.008360039,0.030094016,0.027840897,-0.012444654,-0.0037615052,-0.015347171,-0.014708972,-0.0017674809,-0.0344257,0.012176244,0.012980847,0.0038627794,-0.010114607,0.00907554,0.008258982,0.005460726,-0.0040997197,-0.01829849,0.010945366,-0.019172592,0.011486508,-0.023680985,0.027185606,-0.037389543,-0.015776385,0.021146588,0.0058979434,-0.0023548284,0.013827665,0.0052307947,0.010953549,-0.0014141791,-0.0122702615,0.008920319,-0.0059295394,0.022037834,-0.006117738,-9.6899945e-05,-0.003898269,0.008979945,0.009253197,-0.008219938,-0.0033763081,-0.044762753,-0.007898309,-0.009191661,0.0038300888,0.0061721858,0.0031088856,0.011985673,0.0011277829,-0.01760143,0.01105799,0.003160088,-0.006838701,-0.015852252,-0.026702415,0.018258557,-0.009873081,0.050896145,0.014354656,0.0075315093,0.002355487,-0.012713163,0.006123438,-0.012310591,-0.018859623,-0.008683993,0.04438542,0.022290576,-0.005594244,0.026292883,0.014267695,-0.0016194527,-0.019138109,-0.0043999422,-0.0043769525,-0.0068912846,0.008312159,-0.014651166,0.01908921,0.028475258,-0.010535545,-0.025325542,0.0131095145,-0.01382728,0.00010632934,0.012518682,-0.020620197,0.000507168,-0.007947721,0.0005963562,0.0018164186,-0.018365307,0.007734561,-0.009530766,-0.02067118,0.0063781403,-0.01614709,-0.032494664,0.064875185,0.016445065,-0.020944605,-0.014005137,-0.012705588,0.004593747,0.009915219,9.955387e-05,0.028274836,-0.026238125,-0.012985022,0.0065412843,0.018076327,0.008898861,0.006203937,-0.00839685,0.0018944554,-0.01047553,0.01674739,-0.026018629,-0.00046586237,-0.0029512194,0.020141887,-0.021520255,-0.020147378,-0.025198625,-0.02041432,0.00435723,-0.032001942,0.0031447604,-0.0022358473,0.013975842,0.000114631315,0.013154994,0.0019838116,0.018407438,0.0059925746,-0.0021252646,-0.010180086,0.0044471086,0.017459596,0.006271241,-0.0077716485,-0.010762711,0.011354336,0.017434219,0.014752887,-0.015527872,-0.0049780696,-0.014744936,-0.0027951393,0.0010536483,-0.013333699,0.0007425426,-0.008158412,-0.0029275299,0.0069783684,0.0134393815,-0.013883773,-0.017070604,-0.009821584,-0.011817502,-0.015197338,-0.0097842775,-0.0016023996,-0.0032737255,-0.004659794,0.015294203,-0.002153302,-0.0065950793,-0.019761087,-0.0069643673,0.005551493,-0.026295701,0.009270516,-0.009086855,-0.0150061995,-0.015046559,-0.020865697,0.008239659,0.0005274861,0.0043288115,-0.014164083,-0.008965321,0.0020892818,0.002441198,-0.015771715,-0.0127005745,0.010371344,0.005720128,0.0035739823,0.0009957339,0.014605726,0.007840435,0.0049233427,-0.008052748,-0.0016234255,-0.03026641,-0.006670853,0.022752712,0.01893014,0.0055303057,-0.012072952,-0.0016718361,0.008790526,0.02530966,0.06302279,-0.012937915,-0.0054017426,-0.0037317504,-0.005152608,0.011214543,0.02219879,-0.010164371,-0.013377991,-0.0055630626,0.0016642364,0.001327009,-0.002952236,0.009780021,8.0710706e-05,0.0046348483,0.012794033,-0.0054905633,-0.015418231,-0.02290272,0.00016922063,-0.00062514644,-0.020470075,0.011024629,-0.02031116,0.13073948,-0.0053635202,-0.016428072,0.008281055,0.017158257,-0.0006494287,-0.0034014753,-0.00087107316,-0.006230002,0.016615909,0.009242151,0.0044875145,0.010177845,0.0030899409,0.0008251875,0.021374613,-0.023344869,-0.008492074,-0.0037572684,-0.03202489,0.0035177495,-0.0022887022,-0.013313828,0.025226012,-0.01116241,0.04844882,0.023079071,0.017567731,-0.01678369,0.004078247,-0.017644392,-0.00086629676,-0.0017756218,0.015560803,-0.00073306647,-0.0055642473,-0.00871395,-0.0036799295,-0.008832471,0.0009899088,-0.005875519,-0.016230514,-0.0013340253,0.0016766666,0.009248363,0.0027217474,0.007276262,0.0030721272,-0.009392162,0.0036093425,-0.011911672,-0.0010767988,0.01512344,0.009349098,0.0041889823,0.0037347144,0.014842098,-0.012925949,-0.007019244,-0.0019180023,-0.11213757,0.011424627,0.007805158,0.016655589,0.022318292,0.008888381,0.0067418306,-0.02068732,0.0076115453,-0.012500512,0.0034868936,0.0030943386,0.00024108442,-0.0102476245,-0.0037059449,-0.046236657,-0.0047763693,0.0034060844,0.010634264,-0.010365409,0.0052482993,0.028936094,-0.009151728,0.018191015,-0.0015185901,-0.0073788934,-0.014657726,-0.012184791,0.0076823607,0.004299402,-0.003572168,-0.014530774,5.1655104e-05,-0.025379017,-0.028314894,0.02173458,-0.000627785,-0.01099614,-0.0060014115,0.0015370644,-0.006322735,-0.027728152,0.013462089,0.00224345,0.0027467045,-0.008322154,-0.009002845,0.01907687,-0.04190594,-0.012019367,0.012420283,0.0062050996,0.00040424228,-0.00804802,-0.0031503804,0.014241239,0.002864378,0.017468633,0.0027082784,0.0034864407,0.09733264,-0.010249825,-0.025729664,-0.003936597,0.019296886,-0.018343415,-0.0052620624,-5.863923e-05,-0.014760847,-0.024308387,0.0060302075,0.009709317,-0.012410455,-0.021130951,0.0008707423,0.0035638576,-0.017103279,0.01656903,-0.014734648,0.0074033244,-0.0017232232,0.0023900638,-0.050803963,0.009984577,-0.003532208,-0.011834089,-0.0024315824,-0.0026280843,-0.01337025,-0.0036845966,0.0031588445,0.0020390428,-0.01438143,-0.009309447,-0.009452837,-0.006621351,-0.009545762,0.011824296,0.018462526,-0.008252047,0.014400729,-0.0032849447,-0.016212635,-0.0036649231,-0.0062111146,-0.010917837,0.0090829125,0.0115009155,-0.026740072,0.00092218746,-0.01198335,0.0066558593,0.020464538,-0.008415363,-0.0094124535,0.0008441583,-0.02469566,-0.0011766285,-0.026529996,-0.01591084,-0.011724853,0.0018841327,-0.010517995,-0.0003456028,0.0055735004,-0.013761183,0.01611919,0.00207284,0.015919605,0.010770315,-0.00023066722,0.0077585243,0.0038788582,0.024519231,-0.00062074483,0.00076188304,0.0017776929,0.011374165,0.00025802583,0.019255662,0.0100282,0.016279524,-0.0056371605,-0.018893605,-0.006239834,-0.0017298447,0.00961363,0.017727062,0.015202922,-0.010174154,0.019524118,-0.0064753895,0.00058204256,0.023610001,-0.015177098,0.115488835,0.020557417,-0.005337789,-0.0010982581,0.015357009,-0.008945206,-0.016057203,-0.0006162084,-3.8850216e-05,-0.016258577,-0.0024225456,0.021234354,-0.035069685,0.0014159966,-0.011921527,0.0077816295,0.019078482,-0.0127848955,-0.02002035,0.00032187326,-0.021123137,-0.024088467,0.0010347061,-0.004815265,-0.004171223,-0.025665298,0.028888013,0.011586404,-0.012937677,0.01657904,0.0040040994,0.01592064,0.00056794094,0.0045425524,0.0007872172,-0.0054462925,-0.0003920798,-0.0001601924,-0.0022153833,0.0023635451,-0.00047226506,-0.007454505,0.00240626,0.0066050114,-0.003822288,-0.020651603,-0.0063178823,0.007689747,0.017005833,0.0051541287,0.0054561077,-0.0038000275,0.0029465973,0.0037670657,-0.005643024,0.015046535,-0.0033313879,-0.011909426,-0.011985764,-0.0034930438,-1.852692e-05,-0.028903836,0.004451582,-0.007903739,-0.04264619,0.009707169,0.0050594714,0.009867556,-0.0017736829,0.009445367,0.015453989,-0.024927547,0.008747614,-0.025560604,0.00035674806,-0.007009796,0.002352813,0.018848559,0.018934006,-0.007902412,-0.0008770281,0.007826954,-0.020366732,0.011069376,-0.041753754,0.009494861,0.018394025,-0.013095822,-0.0021001892,0.0037980422,-0.01725301,0.022998732,0.000700797,0.008913983,-0.019516902,0.004372117,-0.0058768853,0.0076208226,-0.014941916,-0.015165422,0.0031822347,-0.015760398,0.0040996363,-0.006473981,-0.018321361,-0.012920107,-0.0054380046,0.023116458,-0.011856324,0.0012380233,0.0072036423,-0.013633002,0.007771338,-0.0038282438,-0.0031895365,0.0114697665,0.006429604,0.010116345,-0.034088686,-0.00022931265,-0.013534604,0.0013997142,-0.0029701265,0.008822486,0.04543314,0.010312221,0.008522296,-0.0003498379,-0.038400404,0.0044925604,-0.003034647,0.016740534,-0.0058673797,0.012494358,0.016010515,0.0053417985,0.0017782637,0.00927081,-0.0051538236,0.008401854,0.015990734,0.0063641826,0.017539052,-0.0065666945,-0.028216105,0.005997302,-0.03126089,-0.0016927111,0.024245393,0.011839676,0.0074226987,0.026742537,0.026008172,-0.0019625912,-0.030797504,-0.0017894157,-0.00094718044,0.00036963605,-0.013760357,0.005550761,-0.0028347261,-0.01750483,0.0048158965,0.0016465097,-0.0038908026,-0.00049920415,0.0009708406,0.0027784572,-0.023002107,-0.019552026,-0.010677852,-0.00576715,-0.0077615106,-0.014956315,0.0015405546,0.011635195,-0.004520177,0.01928033,-0.012163217,0.012297275,0.011210233,0.0045412364,-0.0065860893,0.014460861,-0.0136017585,-0.017359633,-0.004311074,0.004341704,-0.011627409,-0.015423263,-0.0034602042,0.008282411,0.006739085,-0.0035972402,0.007886943,0.02456348,-0.019179491,0.008341697,0.0041981707,0.024265835,0.005053864,-0.0033557285,0.009489079,-0.018052058,7.389303e-05,0.0019305433,0.009153957,0.008963314,0.012459773,-0.00485748,0.0019400923,-0.0027662225,0.012615536,-0.019779608,-0.0046855593,-0.011414017,-0.006822768,-0.018537179,-0.015509539,-0.0073744636,0.0017705619,0.012631293,-0.017517244,0.0045015384,0.017931018,-0.006295312,0.003042164,-0.024755776,0.013609158,-0.0007331963,0.008652379,0.0020416665,-0.00029561226,-0.0066616274,0.07295615,-0.006558063,-0.0060525504,0.029008394,0.021134937,-0.015338552,0.015781233,0.017276442,0.005524449,-0.010690482,-0.01734437,-0.0003233005,-0.015204652,0.042180516,0.007186278,0.022778269,-0.0075411005,-0.001693785,-0.005440656,-0.022201478,-0.010815811,-0.0010636222,0.009873052,0.008418546,-0.0023434332,-0.013355016,-0.0005249016,-0.01363811,-0.016565729,-0.0028747262,-0.0046792547,0.0031677315,-0.006289101,-0.010669884,0.01727851,-0.011028847,0.00844703,0.0027268927,-0.014766423,0.017993802,0.012498489,-0.0032179465,-0.015817923,-0.0052895024,0.0082856715,0.0014673312,0.0010668817,0.0043599303,-0.005773257,-0.015670829,0.0111592,0.007407955,0.02641146,-0.014391324,0.017288063,-0.00032175917,0.07288221,-0.0021233396,0.010257774,0.0012790692,-0.0036323362,-0.006237184,-0.014508204,-0.0030594599,0.015369708,0.030952087,-0.0044309166,0.009207959,0.017013427,0.009192063,-0.0038177858,0.019686095,0.0020141236,-0.010758778,-0.012110476,0.013038161,-0.0036175172,-0.0070661306,-0.0024012749,0.011737489,0.02359842,-0.00010631736,0.0073330435,-0.0047114696,-0.01623634,-0.0020164526,-0.008327567,-0.00451638,0.013830628,0.0025957287,0.026786864,0.00050647196,0.011609621,-0.0011894171,0.0053383755,-0.000831275,0.0012614321,-0.005822938,0.011195153,0.02062041,0.02042509,0.0016487178,-0.01622346,0.007557757,-0.019027371,-0.0032048621,0.008423056,-0.009161742,0.0036447523,-0.026869845,0.004086577,-0.014969361,-0.0019766684,0.00254227,0.125881,-0.025192387,9.909019e-05,0.0055985968,-0.0012993247,0.0013204998,0.00941191,-0.0066460343,-0.007446087,0.0060137785,0.003920963,0.0074321465,-0.0031841223,0.020365454,0.00662187,-0.0044939355,-0.0018894547,-0.004780551,-0.013688027,-0.00017201575,0.0025443383,0.035354264,0.0012252502,-0.009756155,-0.032086626,-0.0009098325,0.0061477106,-0.006901094,-0.0028071,0.01709267,-0.011871655,0.011508238,-0.013960904,0.005441622,-0.027595416,0.010353837,-0.010405981,-0.0041557485,0.00917298,-0.025717635,-0.006116147,0.01355997,-0.029606737,-0.026728416,-0.00036018947,-0.009347022,-0.00471562,0.012384798,-0.01070162,-0.003465484,-0.0017535659,0.011107862,-0.021658996,0.00037800445,0.013658742,0.0012838284,0.02159515,-0.015980573,0.016317882,-0.0056027314,0.0025508443,0.0050204163,-0.023145111,-0.021891372,-0.01482588,0.0016774988,0.00650966,-0.0003545685,-0.01730929,-0.00465234,0.009703576,0.015487804,0.008409933,-0.0044017825,-0.007268412,0.008713779,-0.005231528,0.0119845215,-0.018692017,-0.014736867,0.0029863059,-0.0147630945,-0.0010212938,0.018699298,-0.0012530239,-0.015856823,-0.011244662,0.0059654466,-0.011856058,-0.013782399,0.004813125,-9.942831e-06,-0.012426577,0.006752531,-0.008393762,0.015547436,-0.006731933,0.00423679,-0.010142925,0.00121298,-0.0043067206,-0.02910157,0.0025510036,-0.021397907,-0.010870904,0.021005286,-0.00585125,0.0014336867,0.0038726078,0.0010149573]	0	0	t	b7e52df6-21dd-4fa2-bb0d-11961f360cd1	2026-07-28 09:50:40.805378	2026-07-28 09:50:40.805711
54b5ba3d-c45a-4bee-8f53-ffdcf430bd17	How to reset your password 	Account	If you have forgotten your password or simply want to change it for security reasons, follow these steps:\n\n1. Go to the login page and click on the "Forgot Password?" link located below the login button.\n2. Enter the email address associated with your SupportHub account.\n3. Check your email inbox. You should receive a secure password reset link within 2 minutes. (Be sure to check your spam folder just in case!)\n4. Click the link and enter your new password.\n\nPlease ensure your new password is at least 8 characters long and contains a mix of letters, numbers, and special characters. If you no longer have access to your email address, please contact support for manual verification.\n	[-0.00362842,0.02258128,-0.0038841807,-0.026539054,-0.014084543,0.022583384,0.021357028,0.0051153144,0.010056204,-0.03569452,-0.038624417,0.007847347,0.007885504,-0.026548782,0.026927464,-0.009070379,0.034240752,-0.032530446,-0.010322455,-0.011204278,-0.011750169,-0.0008671844,0.014709003,0.029078167,0.010429602,0.0013471881,-0.01440737,-0.0024905456,0.0077550327,0.12524375,-0.0024716577,-0.018780965,-0.013282237,-0.030354515,0.014395654,-0.0042211157,0.0057051764,0.03066569,0.00043370004,-0.007829507,0.012932767,-0.018472219,-0.014645764,-0.0060673226,-0.021487625,0.0041710217,0.0012194952,-0.015351269,0.018553063,-0.014567201,0.009310266,0.008601088,0.01488046,-0.012562163,-0.028780023,-0.005179389,0.013374677,0.004216477,0.015110147,0.005631388,-0.006394453,-0.009946731,0.017270535,0.008997613,0.008746747,-0.015818322,0.024418047,-0.0018478823,0.0014364352,-0.015141646,-0.006708244,-0.021897659,-0.016588958,0.017927721,-0.0059343907,-0.02446256,-0.029250275,0.029379664,-0.014769916,-0.01057563,0.014748281,-0.0007588901,-0.008154202,-0.0050126575,0.025236834,0.0032234099,0.002431982,-0.008261277,-0.008398474,0.014792537,-0.0031718456,0.008570041,-0.00055897766,0.01731545,-0.010850209,-0.014108313,-0.028321803,0.011021993,0.0043521975,0.009606232,-0.00089356647,-0.0010504869,0.014355744,-0.0069975806,0.043428607,-0.013151729,0.018154029,0.005554508,0.02855049,0.016895043,-0.028558895,-0.17505908,0.010164487,0.01204348,-0.011601513,-0.052190837,0.0027929575,0.019765347,0.0042281765,0.0037511638,-0.0032853216,0.009974823,-0.021949496,-0.016726281,-0.013230907,0.016873347,0.022056157,0.0151616875,-0.00963742,0.027741104,0.00044898372,0.0057677277,0.015987156,-0.00053252367,-0.0047090617,-0.009246889,-0.02379224,-0.009255897,-0.0039761066,0.00754687,0.0005890802,-0.015509795,0.0035012716,-0.023869073,-0.0028484992,0.010885611,0.0011480601,-0.008490676,0.027656823,0.017756779,-0.0020255859,0.0041057677,0.027085993,0.0086817825,-0.005130429,-0.010815506,-0.011350183,0.013808489,0.02248127,-0.0037271008,-0.021729143,-0.024422362,-0.032625224,0.008748783,0.0028088887,0.009562015,-0.025457375,0.036190074,-0.020826029,0.01392598,-0.0054870103,0.0049449587,0.0094066495,-0.0062751593,0.001376831,0.009375104,-0.0026845995,0.010101098,-0.010133453,0.016119797,-0.011560724,-0.012752061,-0.011179563,-0.0015575464,0.034525037,-0.008165145,-0.021783706,-0.016259361,0.012932957,0.009127456,0.009796892,-0.012031856,0.0073522907,0.00059768,0.012740543,-0.015622214,-0.0078120762,0.011563221,-0.036220007,-9.3212555e-05,-0.0019854358,0.017107716,0.028019568,0.008254365,-0.019333705,-0.017849853,0.006165898,0.006443729,0.015305203,-0.017751234,0.022468027,0.0087763155,-0.0056066616,0.003375956,-0.00050781626,-0.007659048,-0.0097258445,0.07704351,0.00044316187,-0.017656058,-0.0011065576,0.021301169,0.012080627,0.019386927,0.012590358,0.010398604,-0.0027480586,0.011422977,-0.011962567,-0.010987265,0.0129063185,-0.01809023,0.031297605,-0.016743442,0.0025454655,-0.009760384,-0.0016442068,0.010051131,0.0020321747,0.002491033,-0.013209383,0.007016622,-0.0059767826,0.012270652,-0.022356931,0.0012662273,-0.010737603,-0.001253346,0.0034833394,0.0196857,-0.006563214,0.0049638115,-0.0022872495,-0.0072727674,-0.002817432,0.013769131,-0.03014002,0.007428012,0.021277338,-0.01806354,0.010398897,0.007616517,0.009097911,-0.0064663347,0.0054854215,0.005964527,0.015189132,-0.024699429,0.013994267,0.0048935236,-0.005297934,-0.0062483903,-0.0054102065,-0.027514892,-0.013343767,0.02078045,0.012393686,-0.011966373,0.0057775946,-0.009093292,0.0054675355,-0.001075165,0.043657117,0.015019048,0.01780602,0.0060733743,0.00017109457,0.0079694465,0.03437852,-0.011298117,0.009636847,-0.0057267584,0.009944187,-0.014524993,0.007002913,0.02399686,-0.012154528,0.0009312013,0.0058820895,-0.02182023,-0.010263492,-0.021710677,0.0041095326,0.016418032,0.014252598,-0.0060669063,-0.0060129496,0.022274457,0.0048661334,-0.0095628565,0.000988408,0.0058398084,-0.022952655,-0.004445466,0.014034315,0.00019047329,0.027001973,-0.016999781,-0.01186791,-0.11605724,-0.004282307,-0.002707754,-0.022172168,-0.007738882,0.01781402,-0.01920846,-0.02132958,-0.014953217,-0.021905046,-0.014740588,-0.002904867,-0.009913426,0.014592695,-0.01703696,-0.008169425,-0.0070855636,-0.023030436,0.012919825,-0.0035981156,0.000934558,-0.009886204,-0.17367823,0.0034183108,0.00066621637,-0.018328318,0.007947591,-0.0225444,0.016991014,0.023678903,0.02516654,0.006215442,-0.007891534,0.0051291385,0.0073553217,-0.016163781,-0.010513498,-0.008599311,0.01016424,0.02185065,-0.004491929,0.010895044,-0.0025318295,0.0010366901,0.01588669,0.024815759,-0.003776105,0.012488884,0.0021233195,0.021315273,0.008431015,-0.015620583,-0.001930845,0.0003230439,0.0026059984,0.016602723,0.023340218,-0.0071488856,0.02310898,0.021719242,0.01161176,0.00036333592,0.0023230817,-0.009986577,0.018326733,0.024001427,-0.0174855,0.014478205,0.02453793,-0.014314869,-0.008812493,-0.00042133528,0.027536314,0.024207054,0.0006226545,-0.011960112,-0.018469218,-0.017267115,0.0016114848,-0.0151375,0.009764046,0.022505589,0.023883795,0.008420005,-0.015953833,-0.014754651,-0.011351195,0.010266122,-0.008129686,0.004372016,-0.015405618,0.006589046,-0.017674405,-0.0010064694,0.011651596,0.0056552766,-0.002274521,-0.0051235463,-0.03611904,-0.004822488,0.0054294607,-0.018517386,0.009227574,-0.02551792,0.016061349,0.035514537,-0.015746817,0.014695325,-0.01882144,-0.012336057,0.0300435,0.007295978,-0.004522882,-0.0015046899,0.0037828754,0.015651055,0.006912129,-0.01601832,0.0029337932,-0.0056093275,0.01705836,0.0037478944,-0.012802285,0.019349694,-0.012900075,-0.00910018,0.005493762,-0.02078612,-0.02842059,-0.012546421,0.0053294892,0.009086302,-0.016429026,-0.006451693,0.019728225,0.013469402,0.017425511,-0.014403882,-0.0074857664,0.0024265186,0.012377061,-0.010436611,-0.010764038,0.0047717504,0.0054300553,0.023058467,-0.005945195,0.008471819,-0.026030056,-0.0021653539,-0.004652055,-0.01574573,-0.017128004,0.036115184,0.00062734,0.017237827,0.012121903,-0.003250486,-0.01296571,-0.016543044,-0.018715002,0.02851657,-0.0040536257,-0.01124212,0.01663176,0.004258768,-0.0017520905,0.020380953,0.035789974,0.023241749,0.013557344,-0.020941457,-0.015407362,-0.008738365,-0.008157915,-0.019097954,-0.01840295,-0.008348097,-0.019309385,0.025979504,-0.0037134737,0.017814953,-0.0040176753,-0.008193156,0.008333039,-0.011494155,0.0270677,-0.008563267,-0.18035835,0.003657364,-0.007156483,-0.03640532,-0.03144363,0.0036816201,-0.013801978,0.017768806,0.0053785937,-0.009481779,0.020831099,0.01334211,-0.021857804,-0.0010866493,0.016245546,-0.022304812,0.02336652,-0.0005406483,-0.017679019,0.0038248724,-0.010002477,-0.029785912,0.018314501,-0.0036439097,0.0066603674,-0.01736953,-0.0042691412,-0.013390779,-0.008476693,-0.016664675,-0.030830309,-0.007740844,-0.0009843403,-0.013716972,0.0062332563,-0.0006850386,-0.0053639663,0.02154047,-0.022854328,-0.0019850333,0.024851134,0.01218698,0.010825299,-0.003129501,0.0018584798,0.011454067,0.021905135,-0.058524292,-0.0023825024,0.0056517767,-0.0038555535,-0.012491334,-0.007782001,0.0273874,-0.015862823,-0.009940505,-0.0043362323,-0.030312255,-0.014067141,-0.006387757,0.0059105386,0.0014961361,0.008375498,-0.00015647737,0.02829597,0.0063497284,0.01641239,0.07587706,-0.015204302,-0.017291056,-0.0009234367,0.021889206,-0.011208706,-0.015393183,0.0053226044,0.032390382,-0.027068458,-0.023053426,-0.018522017,0.016885698,-0.009163752,0.01034499,0.040363707,0.013388542,-0.019472437,0.009697764,0.014348043,-0.0055714455,-0.015163056,0.046039533,-0.010179726,0.021984162,-0.0013933766,0.009140536,-0.010544432,-0.003347302,-0.0047289203,-0.01728949,-0.025207374,0.0069151805,-0.005803331,-0.0007717049,0.0074733733,0.013687383,-0.016586678,-0.0114131635,-0.014298347,0.01069484,0.019078158,0.018089112,-0.0078788735,0.017252266,0.015253035,-0.011838506,-0.0064263144,-0.012484957,0.003395008,0.009939449,-0.0192346,0.006815524,0.017313536,-0.017784964,0.0012196193,-0.002375726,-0.0037516342,-0.014011158,0.01320144,-0.0039167837,0.020789688,0.020706164,-0.001429878,-0.020467784,0.007150536,0.00939046,-0.000962352,0.008121406,-0.014585525,-0.020416826,-0.023648435,0.005723828,0.0029967953,-0.011818923,-0.0011033821,0.015658285,-0.0027024248,0.009544625,-0.023351073,0.0138132665,-0.02547094,-0.010706508,-0.011796161,0.009367348,-0.012529498,0.010857705,-0.011944768,0.012415882,-0.009449169,-0.021494227,-0.008257601,0.0019138816,-0.005512806,-0.022681726,0.03366152,0.008092326,0.00084052753,-0.021084405,-0.022443937,-0.009676916,-0.013014569,0.010506477,-0.009178636,0.02842242,-0.010965161,-0.0018956898,-0.0029531913,-0.0022386585,-0.0071018194,0.00054383936,0.015330234,-0.007666677,-0.008255192,-0.013227555,0.041861687,-0.010192442,0.01730608,0.003200301,-0.011805808,-0.004827299,-0.0104043875,-0.00556107,0.011655133,-0.01530358,-0.003839653,0.059963237,0.013128597,0.003990754,-0.009755774,0.016606936,-0.020691339,-0.010973567,-0.015509158,-0.0077044526,0.0051365867,-0.007557516,-0.0072476203,-0.0020533935,0.023564354,0.011916458,-0.016006382,0.028427217,-0.003100836,0.009374074,-0.00031207094,-0.011594464,-0.0021718522,0.001980418,0.012507802,0.005678527,-0.018109186,-0.0020265172,-0.012515637,0.016174532,0.00061471254,-0.0016445887,0.012973175,0.05235726,0.0058123874,0.0023595183,0.000484879,0.011605587,0.006908222,-0.00075428677,-0.02054569,0.031486966,-0.02722344,-0.001791144,0.009969798,0.007832705,0.02440625,-0.002024208,0.009576758,0.0077737393,-0.0066524795,0.0009041573,-0.007404866,0.016348515,-0.018314594,0.035947047,-0.0023888736,0.014418911,-0.00379365,-0.0008008073,-0.018498447,-0.031477623,0.012197755,-0.017620329,0.008421232,-0.016286002,0.027649967,-0.0019525997,0.025701173,0.0018626737,-0.019778438,-0.02057429,-0.00096475496,-0.008783757,0.005304983,-0.010239915,-0.005827471,-0.0029979497,-0.011642717,0.023598693,-0.018145924,-0.012346746,0.016960291,-0.0075683934,0.012305101,-0.0013355837,0.023890752,-0.011938533,-0.015202743,-0.013630241,0.009548221,0.008149771,0.015646841,0.0055241347,0.015009116,-0.01710891,-0.00076135475,0.007833718,-0.019519085,-0.016994769,0.011948971,0.0144888,0.0134227825,-0.0140001485,0.021308554,0.015017461,0.0019339679,-0.01831892,-0.022964388,0.0010633155,-0.012230648,-0.013793348,0.020036835,0.0029837298,-0.015766948,0.01675416,-0.0048692254,0.02181462,-0.008088991,0.013009599,-0.009601513,0.020934071,-0.014129408,-0.0047567612,0.0040561217,-0.0021900556,-0.009354421,0.008878864,0.005051889,0.009249404,-0.018600272,-0.0010777684,-0.0026646014,-0.013477431,0.012945645,-0.01713252,-0.023161583,0.022686634,-0.0045803892,0.054243006,-0.0063161557,0.0022347688,-0.014670994,0.0006117396,-0.002026588,0.018950216,-0.00095836725,-0.015143242,-0.013874425,0.002967442,0.00042953322,0.00010841409,0.00031900877,0.01289231,-0.0019813417,0.028192123,0.021702668,-0.004507915,-0.0146459555,0.00072058535,0.011855847,0.001548026,0.0043221246,-0.0015574594,0.12762097,0.0061957603,-0.024415048,0.01636979,-0.0031075762,0.0024760852,0.0036463754,0.013232237,0.0042031724,-0.018504616,-0.008652408,-0.011969381,0.016059287,0.0014969027,0.006797328,0.012999771,-0.0046189404,-0.0013049653,-0.00860734,0.011701447,0.021639066,0.007492646,0.0013459079,0.011122375,-0.016060887,0.05588536,-0.020486498,0.0020028385,0.0027377952,0.0067179524,-0.013341181,0.004618563,-0.016065015,0.0048706145,0.022441985,-0.025339168,-0.0007708853,-0.011518161,0.008016022,-0.004602032,-0.003913079,-0.0021030128,0.0077940207,0.016270787,0.011812612,0.0023213327,0.0047449665,0.0008790206,0.0013149286,-0.0049530547,0.0012088867,0.018209925,0.0075309183,0.012135718,-0.0009382177,0.013674214,-0.0061764116,-0.02274928,-0.015618857,0.017830467,-0.11349085,0.019358749,-0.023014866,0.0029092147,-0.0044539883,0.011210291,0.011950999,0.0011144729,0.008714924,-0.013908586,0.0062610535,0.005044163,0.0039566024,-0.015786774,0.00044143054,-0.046663586,-0.010201061,0.014008395,-0.020147203,-0.0065859947,0.011572462,0.0049316343,-0.03271287,0.003029521,-0.00019496323,-0.02788955,-0.002912063,-0.018898688,0.0027865341,-0.00025269523,-0.019373933,0.006478528,-0.003760188,-0.00948892,0.00014773128,0.0078441,0.0008177583,-0.0043039313,-0.014460402,0.010524333,-0.018221896,-0.03145686,0.0075014466,0.004994238,0.0048285765,-0.007394205,0.017537162,-0.014716436,-0.04792405,-0.031621315,-0.012430705,0.007696808,-0.012366216,7.6249606e-05,0.0013163607,-0.0068329754,0.0055749984,0.002125289,-0.019815793,0.0009639689,0.09986942,-0.003671942,-0.024700163,0.012793891,-0.004369038,-0.0076682335,0.0018284767,0.0018917057,0.00045665007,-0.006147986,-0.0048534856,0.008220954,0.0028684274,-0.0029783065,0.014826764,0.010937808,-0.0043998123,0.011296107,-0.0039545516,-0.0151907485,-0.015654774,0.003269623,-0.06575736,0.020780686,-0.011065298,-0.0038058404,-0.0069989753,-0.0022817685,0.0015837506,-0.029993318,-0.0013148631,-0.0024045545,-0.0034813047,0.016387729,-0.006167158,-0.015367493,-0.00885915,-0.0071702055,0.017523471,-0.007515404,0.0063249883,-0.021113407,0.0055599255,-0.008860169,0.0050177923,0.0005320995,0.0033571867,-0.013786338,0.0006887643,0.009236919,-0.0110350065,0.0068985363,-0.0010476082,-0.016881784,0.009641617,0.0042011547,-0.017399628,0.007082717,-0.019016,0.026301054,0.0015705648,-0.03342272,-0.014605275,-0.009302707,0.025825638,-0.01749567,0.00036706644,0.014444925,0.010412407,0.00028262567,0.022984087,0.02112065,-0.0038265735,0.018826462,-0.0026255816,-0.0015725367,-0.005838742,0.011904287,-0.009993739,-0.0042550224,0.01012245,0.035206765,0.011259888,-0.003983764,0.0070919897,0.005773325,-0.00966933,0.007886994,-0.0043926095,-0.0069513232,-0.0016507844,-0.011244082,-0.012237337,0.012139276,-0.01360449,0.10871297,-0.00081009546,0.00047302988,0.002670557,-0.016098035,0.0043882392,0.011106861,0.029692473,-0.012919575,-0.005434955,0.009032106,-0.02068164,-0.0279395,-0.008676593,-0.011999462,-0.007303555,0.01106282,-0.009731415,-0.025507962,0.020009283,-0.00818943,-0.008408158,-0.0078927735,-0.014996175,-0.01796457,0.00536283,0.00432526,-0.029929573,0.0052244426,-0.001130649,0.012140685,0.004683038,0.008479787,0.006865561,0.001285727,0.0038975833,-0.029999651,0.0012599869,-0.007853405,-0.008484123,0.008384147,0.007269558,0.0009926154,0.00068108545,0.015154515,-0.018347168,0.000101411846,0.004220575,-0.033965513,-0.016079593,0.0019816163,-0.0023097135,0.009296977,0.00812739,0.00094163185,0.007961381,-0.020838043,0.0015880533,-0.010553376,0.006410379,-0.0047161276,-0.012889409,-0.016789764,-0.01514252,-0.015363851,-0.005330639,-0.00019265922,0.003020634,0.006506683,-0.008330421,-0.005639955,0.0073816474,0.007535806,-0.012098672,-0.021416081,0.0053471522,0.0058259577,0.020475915,0.015171079,-0.009354647,0.009015861,-0.015799167,-0.010142321,0.006375887,-0.05235054,0.0030475606,0.012781221,-0.0057529164,0.009167845,0.0019556982,-0.008550452,-0.0010200569,-0.008810591,0.030869309,-0.004738585,0.008888562,0.015696295,-0.013470555,0.00030143725,0.0059873587,0.0069014803,0.003002377,-0.011494074,0.00486524,-0.017316077,-0.012235151,-0.011600496,0.03926661,-5.9937563e-05,-0.013263533,-0.01606424,0.0027361908,-0.0051967083,0.00019454944,0.004349244,0.031335916,0.02077644,0.007520193,-0.011897673,0.011124068,-0.012551294,0.006958103,0.010230009,-0.00913185,0.04086409,0.0001014201,0.024593577,-0.012445639,-0.042103525,0.014929364,0.0020070332,-0.00467007,0.0058425115,0.0024377652,0.0013039104,-0.00922198,0.013865774,-0.006183667,-0.003316299,-0.011086315,0.0053443913,-0.022096762,0.014744667,0.00013393315,-0.023200532,0.0070701386,-0.006575507,0.011352134,0.020354653,0.023513215,-0.01117546,0.0057807085,0.021430856,-0.004277103,-0.001845198,-0.0040639997,0.008483594,0.010760466,0.0004978426,-0.013611028,-0.0075447154,-0.023807876,0.02512583,0.012758427,-0.01305312,0.0029679819,-0.0017932913,-0.02736476,0.0018575729,0.01197108,-0.008172173,-0.015392828,0.0056314087,-0.016722927,-0.018924462,0.017768923,-0.0052153324,0.030918082,-0.01091009,0.0046868334,0.022984156,0.019312747,-0.039169956,-0.0019652871,0.0046696723,-0.0064409683,-0.014446816,0.013964725,-0.0041693947,-0.025774822,0.0043537873,-0.01517527,0.010326238,-0.010991078,0.00026842346,0.00913531,-0.005096319,0.007947722,0.016535083,0.016574647,-0.005431396,0.00075023924,-0.0034160549,0.010101055,0.0057433657,0.012042453,-0.0113547435,-0.012034972,0.008187864,0.0067359665,0.011770718,0.0020723538,0.014807116,-0.0025132198,-0.0022890884,0.0041067298,-0.016468646,-0.01714321,0.003745219,-0.008668991,-0.006053832,0.00431237,-0.00636774,0.0026241373,0.0033099365,0.005887663,0.014482997,-0.022699127,-0.0012072828,-0.014029396,-0.017191933,0.026248474,0.024234444,-0.005669128,0.057080314,0.014486071,0.0059841373,0.0017861945,0.016092334,-0.015621799,0.017950088,0.029002924,-0.012762594,0.00067871297,-0.017999621,-0.0024523276,-0.019036043,0.047528874,-0.022791203,0.010029018,0.0071893698,0.00089079264,-0.015778122,-0.0051216744,-0.011708334,0.01570569,0.0034524684,0.011739238,0.0037896945,-0.021532545,-0.00024917748,0.017601738,-0.019953424,0.029647605,-0.004449736,-0.019879906,-0.0059941974,-0.012191354,-0.0088231275,-0.009686835,0.009637475,0.016866121,-0.01936468,0.011375184,0.020437978,0.008440231,-0.011326256,-0.016416319,0.013665298,0.018022414,-0.010145313,0.011745647,-0.0141684525,-0.006262154,0.025510602,0.014068916,0.0038187262,-0.0086790845,-0.008406811,-0.017631179,0.07826683,-0.00607678,0.0060984306,0.017051766,-0.02277446,-0.0015428688,-0.015167646,0.0034590873,-0.007858196,-0.015771784,-0.0032829773,0.009533658,-0.00017279047,0.00030943402,-0.0075345966,0.0009363873,0.007235714,-0.02851952,-0.013757412,0.00494477,0.0010471249,-0.0070007425,-0.0053225784,0.019815966,0.02087112,-0.033494916,-0.00071748695,-0.010771646,-0.008880747,-0.0023336252,0.0020902504,0.00095777295,0.011396451,0.006562024,-0.0016303296,0.00356572,0.011719298,-0.011860905,-0.0038250724,0.017102664,-0.013816386,0.01480671,-0.0036542357,0.010064375,0.021375183,0.0083330665,0.0029829217,0.0049078506,0.0018143585,-0.017397871,0.01559963,-0.010573285,0.013276308,-0.024237745,0.004969872,-0.0070521957,0.010338003,-0.001556836,0.107820146,0.0016458397,-0.0027574138,0.01298898,0.007252199,0.017959759,-0.0023396323,-0.008395876,-0.0011465804,0.0016994071,0.02060922,-0.001976459,-0.0015472937,-0.0043550488,0.009408467,0.012937649,-0.001599468,0.0022298554,-0.012920621,0.013166246,-0.0007092111,0.020506887,0.0051027318,-0.01337961,-0.007966064,-0.014532365,-0.0011885514,-0.0034221846,-0.0095636435,-0.0069096717,-0.00504371,0.008386463,-0.019710083,-0.0039029245,-0.022133932,0.0037515457,0.028284641,0.006133449,0.021742316,-0.027094219,-0.012062427,0.015791513,-0.007904255,-0.016127003,-0.031022375,0.0049026725,0.002750714,0.013976502,-0.004819785,-0.017540608,-0.0053300783,0.016421393,0.0053457934,-0.014175456,-0.0014234708,0.016337967,0.008128739,-0.006387882,0.00079500413,-0.02083703,-0.018463906,0.014783921,-0.018308181,-0.016839333,-0.02336391,0.012044255,-0.004114743,-0.0016290867,-0.013770224,-0.0063155177,0.014263715,0.0022361714,0.011112047,0.017432448,0.010511347,0.0019400712,-0.015279813,-0.0018277516,-0.010414424,-0.002464107,0.021099234,0.010644765,-0.004060473,0.01505062,0.0012469206,-0.025575988,0.0047630686,-0.004406076,-0.017123709,-0.016584322,-0.015597968,0.014270559,0.014403654,0.009444977,-0.0017994375,-0.002571011,-0.014968333,0.010583712,0.0023272892,0.0031345384,-0.011000423,-0.017788388,-0.0004640323,-0.003483981,0.02074444,0.004497859,-0.010848404,-1.4867762e-05,0.020971091,-0.018949945]	0	0	t	b7e52df6-21dd-4fa2-bb0d-11961f360cd1	2026-07-28 09:49:21.991425	2026-07-28 09:49:21.991746
681cebde-fa36-423e-a229-18986847c409	Troubleshooting WebSocket connection issues	Technical	Real-time chat requires an active WebSocket connection to function properly. If you are seeing messages fail to send or the chat window is delayed, please check the following:\n\n1. Corporate Firewalls: Some enterprise networks block WebSocket (WSS) traffic by default. Ask your IT department to whitelist traffic on port 8001 and 443 for our domain.\n2. Browser Extensions: Strict ad-blockers or privacy extensions (like uBlock Origin or Privacy Badger) can occasionally intercept WebSocket handshakes. Try disabling them temporarily.\n3. Network Drops: If you switch from Wi-Fi to a Cellular network, the connection may drop. Refresh the page to force a manual reconnection.\n\nIf the issue persists, please open a High Priority ticket with the Technical support team.\n	[0.0027637882,0.021507084,-0.006111829,-0.0095510995,-0.017673422,0.008279721,-0.0071051144,0.010527233,-0.005021158,-0.065253794,-0.021509102,-0.0031639172,0.009805266,-0.024674308,-0.014376929,0.0020499935,0.013789117,-0.028892063,-0.017263716,-0.0048255464,0.011548847,0.003627302,0.0047950936,-0.01910961,-0.0042623444,0.03357873,0.002158639,-0.0033218658,-0.02808725,0.13957697,-0.010528486,0.0034474034,-0.004530061,-0.019278696,0.030482573,-0.0056359684,0.0019137133,0.008255917,-0.012392975,-0.010268856,0.014460546,0.0173755,0.006909562,-0.0020226114,-0.006924486,0.0012682005,-0.010464444,-0.005491252,0.0064125503,0.0010231701,0.0075882324,0.026686199,-0.0008473495,0.006196302,0.008516645,-0.009313541,0.006031511,-0.0018321688,-0.00493072,0.0019388447,-0.003909949,0.009982154,0.009337196,-0.013120455,0.009614359,-0.0058426913,0.008560093,0.00067523256,0.0011164567,0.0008929783,-0.0038464244,0.004085171,0.0063636038,0.0072489204,-0.018369872,-0.022334663,-0.032174006,0.036117934,-0.022410864,0.020561134,0.0005339378,-0.01972112,-0.01667895,-0.014351488,0.006843318,0.017793184,0.00039979952,0.017939292,0.0063439594,0.014302693,-0.0134078385,0.0037880472,-0.0042211246,-0.009313379,-0.02164014,0.010392444,-0.0041567814,0.006341313,0.021931855,0.013793543,-0.012547902,-0.009115496,-0.023886124,0.002334723,0.02455644,-0.009555669,0.03048706,0.006641933,0.005622515,0.027194267,-0.014903075,-0.16644615,0.0148569625,-0.0074795927,0.007146235,-0.048472956,0.0005670618,0.007951137,-0.005894573,-0.025597429,0.0074334554,0.01232343,-0.009294356,-0.008752183,-0.012846335,0.013479564,0.014055377,-0.010006161,0.033432163,0.006937481,0.026927143,-0.0079421215,0.007419619,-0.034059945,-0.017907362,-0.034556367,-0.0147835715,-0.0076683927,0.0029553548,-0.013283736,-0.0027104956,0.013816405,-0.0026717298,0.0042732493,-0.0385729,-0.009473261,0.03620446,-0.023463089,0.007985842,0.0020488342,-0.0073978305,-0.0014309369,-0.019216852,-0.0071814256,0.004787526,-0.0070101847,0.008034349,0.024805784,0.01985358,-0.0037288805,-0.0019300571,0.01635098,-0.01552153,0.0024222713,-0.011959756,-0.0044809286,-0.028210089,0.035888907,-0.0031149623,-0.021698114,-0.010456294,-0.0076970793,0.010164417,0.001821985,0.01312439,-0.011319893,0.0143526895,0.018725304,0.00014363432,-0.0051359506,-0.016779395,-0.021976167,-0.011052203,0.021057364,-0.014597884,0.017321894,-0.027482169,-0.01610934,-0.014701413,0.0031055266,0.011572658,-0.019466106,0.008109557,-0.014738641,0.01895056,-0.02164399,-0.01512301,-0.001168537,-0.016271679,-0.0006415174,-4.672867e-05,0.009128323,0.0047078943,-0.0045459727,0.0006839785,0.00030548783,-0.0027790477,0.0032931184,-0.0033266756,-0.004409959,0.030579405,-0.004793437,-0.009412812,0.0023084185,-0.013863492,-0.016717093,0.0088252565,0.06277934,-0.0068248035,0.0020483655,0.005054879,0.011388146,-0.0047878185,-0.0013320468,0.00026981105,0.0029461663,0.017915893,0.005814322,-0.0016665629,0.009550225,0.015651824,-0.001472613,0.027428094,-0.026074458,0.0039559193,-0.003985095,0.013719019,0.0027319773,0.013535436,0.019279523,-0.0032995665,0.0021531135,0.018555975,-0.0030532607,-0.0033745868,-0.0102157,0.00526918,-0.011530021,-0.010242269,-0.005831742,0.0140378745,-0.01307384,0.009372442,-0.0011155517,0.011135071,-0.0078025428,0.01130593,0.0058043776,0.011043829,-0.0077544213,-0.017793903,0.010839127,0.029099569,0.014875561,0.013786941,0.0046474948,0.009355848,-0.0153611675,-0.006831714,0.03233847,-0.02572767,-0.024390483,-0.011016586,-0.004404862,-0.021028778,-0.01104832,0.0073243883,-0.0066359662,-0.0053531392,-0.009833855,-0.028878115,-0.017576993,-0.009206252,0.0003851093,-0.006254539,0.0023401473,0.0041158902,-0.005396851,0.029043483,-0.009855394,0.009743461,0.015212337,0.012926679,0.006968951,0.0013010552,0.016711835,0.018608335,0.0027964662,0.00072007027,-0.028548844,-0.0040016174,0.0091371825,0.0039966353,0.025761075,0.015545568,-0.014285924,0.010745354,0.014955479,0.027269533,0.024121877,-0.029765187,0.003785232,-0.018486742,0.014674183,-0.0030295444,0.007366753,0.0067519867,0.011401068,-0.012985274,-0.11973084,-0.02012935,-0.028576847,-0.0019106205,-0.00068594306,-0.002823745,-0.01606787,-0.0034891998,-0.0027785401,0.0078029893,0.004541578,0.004248181,0.03973866,-0.038003854,-0.010822132,-0.0021959257,0.00215136,-0.010202811,0.007064453,0.0047851526,0.021744436,-0.0033611,-0.1879654,-0.0011712752,0.0006698644,0.0028036057,0.020153297,-0.002840299,0.013658209,0.01981479,0.0040508644,0.012347255,-0.020268967,-0.00010313393,0.007437643,-0.0017311777,-0.012043188,-0.01639621,-0.005196586,0.00029476132,0.007114998,0.021036213,0.0016544118,0.0016511582,-0.002272079,0.014407001,0.011818096,-0.015461569,-0.021059554,0.0023228289,-0.009889539,-0.013566666,0.008673059,0.010809234,0.03113805,-0.00058101217,0.03458122,-0.0044295504,0.007968153,-0.018542461,-0.012220843,0.009920154,-0.0081604,-0.0016792448,0.015618118,0.03755062,-0.012030167,0.029225226,0.016139062,-0.0063012387,0.0022967593,-0.004580509,0.0344966,0.012601166,0.023349332,-0.013238474,-0.02327729,-0.017202843,0.0084719,0.0043074167,0.013326408,0.024280706,0.0398761,0.009127518,0.014827895,0.0051146685,0.0030052532,0.013046836,0.004942646,-0.026679853,-0.0032601259,0.0053811716,-0.0053397105,0.010132765,-0.013975302,-0.008684566,0.007624621,-0.02372341,-0.019508049,-0.004877295,-0.009653648,-0.0071873236,0.005271587,0.0073664077,-0.018440448,0.023596872,-0.038012322,0.0039176773,-0.032638356,0.009116924,0.008169498,0.005340374,-0.014689489,-0.013719505,0.013804078,0.0083924765,0.0020678006,0.0115162255,-0.011503319,-0.010826104,0.006317319,-0.013193042,0.015666036,0.020520268,0.01526967,0.0006899581,0.0054615047,-0.016379684,0.009653635,-0.010767395,-0.021857565,0.0035836755,-0.002807496,-0.0035029037,0.012891131,-0.009799062,-0.019772215,0.009509945,0.0015753738,-0.00933386,-0.002258538,-0.014290786,-0.008148533,-0.013198039,0.014034191,0.014417215,-0.0021295578,0.014308766,0.007085411,0.0011145028,0.0111549515,0.00022714898,-0.026520342,-0.0034813713,0.0030584377,0.0066564633,0.017671214,-0.011865209,-0.010879946,0.011232435,0.009982325,0.01861738,0.0003998873,-0.013185819,-0.0017728347,0.008668714,-0.004790568,0.019426756,0.008635939,0.028493732,0.004185938,-0.003440439,-0.027584562,-0.00013015361,-0.0032678475,0.011336038,0.0011685159,-0.013591868,-0.0037139074,0.011155096,0.01689067,0.020832606,0.012624224,0.0024991832,0.0121490965,0.01312799,-0.013583243,-0.016181607,-0.18818675,-0.006252849,-0.0053876196,-0.0053778556,-0.031264383,-0.017214764,0.011620616,0.010236085,0.0034514004,-0.008027415,0.029981434,-0.007219471,-0.017946564,0.00672107,0.002092917,0.0045999335,0.017406324,0.006877481,-0.010221467,0.0073574446,-0.0034152719,-0.049630698,-0.018489784,0.008630654,0.020690132,0.00067311624,-0.0047015497,-0.022093685,-0.010328952,0.0050595338,-0.0330692,-0.0005801962,-0.01872328,-0.011532461,0.026743386,0.014380855,0.010556048,0.0050919983,-0.007260628,0.007477016,0.02268772,0.016378338,0.030094113,0.022637082,0.013360822,-0.007006013,0.01360542,-0.054201674,-0.00105632,0.00260246,0.004091426,-0.020544635,-0.0104970345,0.0020505039,-0.038798332,-0.010364455,-0.00017813123,-0.03703914,-0.0053774454,-0.004313291,-0.022373926,-0.014401865,-0.0018227302,0.0023689743,-0.0035610097,0.0052222433,0.0008559179,0.08450561,-0.0074516386,-0.02402602,0.003428858,0.023566827,-0.0046570236,-0.0045767142,-0.005572948,0.002797432,-0.039201286,-0.020745952,0.002034662,-0.0013717212,0.01057964,0.00495737,0.042171463,0.004201012,-0.008749446,0.036524035,0.007567338,-0.006655644,-0.017652212,0.018417062,0.00037360349,0.008610321,-0.009727826,0.0116275,-0.0077872355,0.010571718,0.014980901,-0.0058827484,-0.006580154,0.017788742,-0.025753533,-0.0014276097,-0.011177967,0.012928412,-0.020128416,-0.011664204,0.004314905,0.031707875,-0.005498055,-2.474711e-06,-0.0040136776,0.0062092277,-0.008917596,-0.031433366,-0.019207466,-0.008122293,-0.017344618,-0.0072301114,-0.0063738045,-0.011809323,0.008980707,-0.008364569,-0.0004496569,-0.0027484095,-0.0010348092,0.0011775112,0.008229615,-0.006426297,-0.026919404,0.009608837,0.00029481496,-0.0018971432,0.014141873,0.01634234,-0.0026688636,0.013262107,-0.026060177,0.017408552,-0.0070818583,0.00039533753,-0.0018157515,0.0048836744,-0.003836704,0.0028030514,-0.019901013,0.0008839542,-0.0050105806,0.034815025,-0.019096881,0.00013316255,0.016184332,-0.009487653,0.004435881,-0.009067703,0.016687535,0.0044344272,-0.010553834,-0.004000226,-0.029126253,0.013713148,-0.006140453,-0.0030653041,0.030404104,-0.0007077529,-0.021763882,-0.008883364,-0.015619275,0.0067390753,-0.004046392,0.0033036785,-0.0042023873,0.021723172,-0.00028478773,0.017981905,0.010889544,-0.0044194935,-0.011359027,0.0058312817,0.00990165,-0.004458163,-0.012131532,-0.02785632,0.007324556,-0.028464258,-0.0010565857,0.0064839176,-0.001752979,-0.012890106,-0.014006317,0.021869136,-0.0020079564,-0.016605526,0.007583542,0.0727614,-0.0057843896,-0.009623491,-0.009187959,0.01704217,-0.0015972637,0.006084921,0.0021010167,0.005532863,-0.004545784,0.014953022,-0.013171107,0.00868115,-0.008049931,-0.002673824,-0.011170857,-0.00199743,-0.008571247,-0.0048919623,0.0015877181,0.0009994839,-0.004792457,0.00062579714,-0.0019755373,0.002530514,0.0018840213,0.011459938,-0.0034955142,-0.009641204,0.026266623,-0.020619418,-0.0054054237,0.05409092,0.03248985,-0.0030151722,-0.008865653,0.0037144634,-0.0017681557,0.03351234,-0.0031890725,-0.0010218417,-0.014171987,0.011193278,0.022225948,0.006016126,0.025410404,-0.0024576788,-0.0020770081,0.004230142,-0.010221046,-0.0181094,-0.00029758233,-0.010150028,0.007941631,0.01539012,-0.014357399,0.00687329,0.017018966,0.00951715,-0.011808912,-0.019152565,0.006261852,-0.012931727,0.016738653,0.0016730841,0.0014649341,0.008847051,0.025324585,0.0053832456,-0.007932805,0.01145843,-0.001928743,0.006422915,0.0017452514,-0.0031167676,-0.018264752,0.0033544067,-0.00086579856,0.013833919,-0.00487243,-0.011111767,0.00046350682,0.009733818,-0.00042618968,-0.02003771,0.021962317,0.0098830005,0.014777112,0.017916111,0.023485145,0.0056517506,0.011530198,-0.021927837,0.03303763,-0.022792237,-0.0021443127,-0.0063079624,-0.017378623,-0.006446215,-0.0019973603,0.006163666,-0.0026078504,0.00304998,0.0044278773,0.0043035536,-0.012655482,0.000615115,-0.0039149,-0.027513767,-0.010850883,-0.003642239,0.013543873,-0.018189412,-0.0031791143,0.0091017885,-0.017448079,-0.012421042,0.014594203,0.022082211,-0.018986464,-0.0066037164,-0.0054832157,0.01921581,-0.0025184825,0.0077612996,0.003048773,0.0011481089,-0.004675758,-0.0059953625,-0.019323915,-0.011207597,-0.026533725,0.008698137,-0.009411362,-0.0025791489,-0.00045028655,0.021839041,0.0025158033,0.06340761,-0.013159258,-0.00014913241,0.013491746,0.01880158,0.011587721,0.009320323,-0.013368161,-0.014846399,-0.022646893,0.007877071,-0.0027422758,0.013703138,-0.00032336722,0.0040637907,0.009646411,0.012717587,0.0031729678,-0.01519074,-0.028079523,-0.0123606725,0.005252467,-0.006425218,-0.001562212,-0.0012421177,0.12755218,-0.007154438,-0.019059688,0.0022098036,-0.0040932973,0.0028828885,0.006367322,0.012779566,-0.009554803,-0.0040341527,0.013087371,0.008388469,-0.012580443,-0.0028012507,0.0023040636,0.022804096,-0.028241152,-0.009261309,0.0039939885,-0.013948349,-0.0001508135,-0.0030785045,0.0011654069,-0.0023318895,-0.0054869694,0.031794842,0.00018104118,-0.0012609331,-0.008247599,0.005838826,0.005616672,0.022034707,-0.00020736636,-0.012307902,-0.0061448403,0.0027556191,0.0033037134,0.009459942,0.009998131,0.006280711,0.019287549,-0.01198907,0.016476259,0.00014989135,-0.011217508,0.0125941,0.010637582,0.01171694,-0.0008255219,-0.006462498,-0.021840831,0.013710534,0.016048716,-0.003928041,-0.023965599,-0.0039169975,0.004078051,-0.014564222,-0.004115669,0.011238965,-0.11967272,-0.0015562511,-0.0010574785,0.03303896,-0.0050709094,-0.000364037,0.0033478872,-0.009844908,0.009035895,-0.003962373,0.026028214,0.014326349,-0.0025985495,-0.009639926,-0.028208839,-0.04819838,0.0009220753,0.0021873887,0.0036156755,-0.0026777426,0.014825916,0.016417585,-0.028404579,0.002343091,-0.012443102,-0.009646997,-0.021196695,-0.01110096,0.0116703,0.014189225,-0.00025906446,-0.0019364699,0.008107674,-0.02440929,-0.021243686,0.013729911,0.017782351,0.019408843,0.0018231333,-0.005674745,0.000549836,-0.02787888,0.004608741,0.0016546623,-0.0049389466,-0.0011845686,0.00095049996,-0.0035603382,-0.051607825,0.00579992,0.018938946,-0.007885382,-0.003209841,-0.017549604,-0.012539116,0.015116665,0.01609364,-0.0019059601,-0.002047725,-0.0032805807,0.10092893,0.017651308,-0.008614327,0.008064605,0.023524772,-0.011083954,-0.006427702,0.0072233574,-0.019403538,-0.02123232,-0.0027128563,0.0016439811,0.01788507,-0.006272686,0.01584579,0.0093993675,-0.0120089585,0.010124956,0.0049319593,0.005323038,-0.007598847,0.007309508,-0.069480464,-0.006929855,-0.017287245,0.0017212592,0.008102205,0.0118562495,-0.015403147,-0.013576602,0.022864243,-0.0019577388,0.0004338103,-0.0026792518,-0.0047902935,-0.010077172,-0.00136994,-0.0009541591,0.021413188,-0.0141120935,0.020145765,-0.0077151437,-0.0035466945,-0.003618736,-0.0060280683,-0.0006835903,0.011661684,-0.015247291,-0.009744654,-0.013183181,-0.014409345,0.0006883562,-0.00015475246,-0.005188684,-0.013666135,0.002452864,-0.0075834743,-0.003829134,-0.007732578,-0.0036319306,-0.011075539,-0.022286205,-0.031277165,-0.0039743325,0.016551942,-0.009556749,0.0014207762,0.027804667,0.0038634224,0.0055255317,0.0038722514,0.0061649173,0.004432476,0.017690476,-0.0030265779,-0.012777789,0.00081792165,-0.009982268,-0.006369102,0.0050971815,0.0037665428,0.018504916,0.003309259,-0.028571608,-0.02524857,-0.008064766,-0.0017954266,-0.017202513,0.009963869,-0.013417314,-0.002926657,-0.03696303,-0.012374241,-0.010366173,-0.0021070915,0.11751402,-0.0064695417,0.0039697844,0.00409773,-0.004251896,-0.0057177176,-0.019368343,0.0059090317,-0.009648093,0.0048837326,0.009280532,0.013030194,-0.027862087,-0.012630497,-0.011932847,-0.01110063,0.0016519947,-0.010257011,0.0017832426,0.00041905176,-0.008202813,-0.011510934,0.028055636,0.0019110967,-0.015490517,-0.0005076659,0.0025739078,0.0068094414,0.0062232953,0.008332601,0.013788193,0.012036236,-0.005637068,-0.00052942574,-0.008522715,0.008653766,-0.021206608,-0.006867577,0.0019148709,-0.0018515567,0.019193148,0.013391869,0.026987365,-0.0024279864,-0.0026996657,-0.019654868,0.016942928,0.014972415,-0.0032936758,0.006296003,-0.00516553,0.0007136862,0.0015131953,0.005557257,-0.00071338506,0.014526062,-7.111404e-05,-0.008465179,-0.0068230564,0.01909587,0.00010097584,-0.023560131,-0.0036510115,-0.0012867156,-0.020014368,-0.0144176055,0.013807809,0.023015184,-0.0003951385,0.00031027934,-0.00011754955,-0.015245711,-0.003287073,-0.0037979605,0.007195417,-0.020223819,0.0069624055,0.026301356,0.011832988,-0.0068864664,-0.0081884125,-0.009120775,-0.004746238,-0.000804189,-0.04128925,0.0035130903,0.009419873,0.008718803,-0.012366599,-0.004428055,-0.017984256,-0.00049975317,0.0011071854,0.026432201,-0.012928249,0.013311024,0.011773787,-0.007868881,-0.020661037,0.005458795,0.0074077984,-0.005398647,0.015324964,0.005025824,-0.013360993,-0.016840408,-0.00047820117,0.0015402972,-0.00022794981,-0.0052466514,-0.0021819049,0.0005727123,0.0059981006,1.9564346e-05,0.014434835,-0.0030923677,0.0068245945,-0.014271734,-0.005436866,0.000902002,-0.01216642,0.0049047917,0.0029758168,-0.0027799136,0.046869185,0.006940298,0.02870438,-0.0012168818,-0.050143454,0.009312108,-0.015295467,-0.0022482958,-0.03447814,0.028344395,-0.0024421473,-0.00023528577,-0.0025106997,0.0003037968,-0.0011523836,-0.003174625,-0.008531276,0.00065185974,0.007644738,-0.011828501,-0.009134129,0.021182116,-0.013469631,0.008672034,0.012162403,0.014685989,-0.01130719,0.036223985,0.018397078,0.0177892,-0.028667292,0.0027945815,-0.0035732903,-0.0014048017,0.005343715,0.0038141466,0.011018534,-0.023183133,0.00092699303,0.015706213,-0.00879186,0.0065966737,-0.009494566,0.0075348984,-0.013530253,0.0032903147,-0.02084879,0.013575474,0.016614161,-0.00029834526,-0.0067759566,-0.0026228197,-0.001225394,0.001174975,0.0023832046,0.01946056,0.02152028,0.0119675845,-0.010484419,-0.0030553564,-0.018041406,-0.012651675,0.001133527,0.020126235,-0.00838029,-0.015792087,-0.00037997295,-0.0028559903,0.014803045,-0.0026119035,0.012976335,0.012265183,-0.004922313,-0.0071363226,0.01289774,0.023521176,-0.0050733816,-0.0027249272,0.010780626,-0.0015705602,-0.0034788505,-0.004684517,-0.013187197,0.007192842,0.012144601,0.0024476135,-0.00010615061,-0.00640664,0.0009947802,-0.010927257,0.016672961,0.0003042438,-0.014644393,0.0017505515,-0.00074713555,-0.012987296,0.008494989,-0.006136714,0.011782551,-0.0078921085,-0.0033198562,-0.013140254,-0.004378805,-0.017768625,0.01738938,-0.015447772,-0.0029677453,-0.0118458085,0.013440675,-0.009615191,0.06307327,0.0010821269,-0.0002698518,-0.0057889502,0.016323132,-0.012993098,0.029391745,0.017384032,0.0024397753,0.010879488,0.014444036,-0.004818066,-0.005426542,0.038090754,-0.0014869834,-0.018182904,0.006514069,-0.004304248,-0.0017106137,-0.021489793,-0.006135071,0.021620136,-0.0020631992,0.020954397,0.013120023,-0.003570815,0.011592511,0.007794021,-0.01814303,0.012926725,-0.0015128668,-0.01773085,0.007265791,0.003471231,-0.011104884,-0.011035065,0.010128961,0.0008658343,-0.00715386,-0.006853292,0.017914822,0.00906894,0.009062087,-0.021777965,0.016039234,-0.0045646643,-0.007821349,-0.009045805,-0.0035682735,-0.010617065,0.015429738,-0.015815806,0.011450696,-0.02355886,0.011244739,-0.0147135295,0.06838807,-0.0051566344,0.011278486,0.0026904254,-0.0017042126,-0.017514141,-0.011520997,0.0071211834,0.00481277,0.009903545,-0.007918153,0.0148257045,0.015381504,-0.00638328,-0.019258175,-0.00051431987,0.015972828,-0.017187618,0.00779745,0.0026153992,0.0016301239,-0.007077963,0.0026613518,-0.001458037,0.011944858,-0.018387621,-0.00011398264,0.0035809805,-0.010035014,-0.0045401133,0.010157705,0.0065002176,0.0091556115,0.0034778998,-0.0150385145,0.012850444,0.014874001,-0.0029546416,-0.019077042,0.0051972736,-0.021397881,0.019342273,0.0042281556,0.03611346,0.025052713,-0.019886173,-0.0015006551,0.0042286785,-0.0057165483,-0.018119026,-0.0037340524,-0.0005327682,0.028805042,-0.020151585,0.02489658,-0.0065833926,0.031376593,-0.015194617,0.13074394,0.007966835,0.0010961515,-0.0044851336,-0.0094138235,0.005361,0.0066979406,-0.00061230536,-0.0055976203,0.0073906826,0.0063004857,0.0056784526,0.0027612092,0.014381985,0.017873509,0.0060309665,-0.002102062,-0.0014210965,0.0009964346,0.0046210648,-0.007908803,0.030870214,-0.008016941,-0.0029218432,-0.024030445,-0.014183222,0.018881096,-0.007908801,-0.016654657,-0.0032813905,-0.015788523,-0.0025385355,-0.024396392,-0.021948209,-0.0151372105,0.017990846,0.011377528,-0.01199479,0.004022779,-0.014088822,-0.0125835985,0.009712961,-0.010894583,-0.019234497,-0.029684233,-0.0019636399,-0.008934442,0.006551212,0.01654581,-0.010089622,0.008002428,0.011817723,-0.008161316,-0.0024923352,-0.011612322,0.019524625,0.010302861,0.0015223668,0.0014860851,-0.009687604,-0.019411718,0.013073991,-0.030680276,-0.024475558,-0.024895122,0.0041028503,0.002573091,0.007050415,-0.0072811893,-0.010246584,0.011297929,-0.005226404,0.007594136,-0.029836787,0.007180222,0.02467556,0.007876739,0.017354894,-0.005174198,-0.012582223,-0.0030160663,-0.00617454,0.023161065,-0.015385423,0.005033304,-0.012178899,-0.011665448,0.0014221758,-0.0075902496,-0.009063947,0.006599648,0.01450463,0.009908499,0.0111495415,0.00010420988,0.00878474,-0.01551725,0.0068430495,-0.0014280258,0.0003694374,-0.024992375,-0.008186398,-0.0023812635,-0.002841175,0.0010371752,-0.016410885,0.0054295347,0.00027877002,0.0005061622,-0.003600419]	0	0	t	b7e52df6-21dd-4fa2-bb0d-11961f360cd1	2026-07-28 09:50:15.270651	2026-07-28 09:50:15.270845
83efcf29-d88c-4208-bef5-286fde78de72	Understanding your monthly subscription invoice	Billing	Your monthly subscription invoice contains a detailed breakdown of all charges incurred during the billing cycle. Here is how to read it:\n\n- Base Plan: This is the flat recurring fee for your chosen tier (Basic, Pro, or Enterprise).\n- Additional Seats: If you have added more agent seats beyond your plan's allowance, they will be billed here at a prorated daily rate.\n- Overages: Any usage that exceeds your plan limits (e.g., extra AI chatbot tokens or SMS messages) will be listed as overages.\n\nInvoices are generated on the 1st of every month. You can download PDF copies of all past invoices by navigating to Dashboard > Settings > Billing > Invoice History. \n	[-0.0016053247,0.007025965,0.015158858,-0.008929919,-0.0234253,0.0027827777,-0.0229014,0.012647109,0.015172963,-0.062630296,0.0007282669,0.015124642,0.009542367,-0.041378617,0.002220117,0.0054397574,0.010994077,-0.015145823,0.0009769294,-0.017844457,0.015379418,-0.00694039,-0.013593465,0.0037821196,-0.0022688168,-0.0041976594,0.010039743,0.00461599,-0.02619006,0.12295455,-0.009180227,-0.009610205,-0.016791567,-0.02152934,-0.011289237,-0.02743004,-0.005557339,0.015409699,-0.015607637,0.0034653926,0.008929785,0.03345833,-0.021762578,0.001677413,-0.042296465,0.0039751935,-0.0035972388,0.026239205,-0.00042494762,-0.013400624,-0.0035193001,0.007204878,-0.0052571963,-0.016687352,0.0010502972,0.0069401683,0.005427059,-0.016136654,-0.006566257,0.013718296,-0.020675134,0.014142693,0.015099785,-0.005825501,0.008215788,0.017639318,-0.003661074,-0.019753128,0.023066074,-0.0142287,-0.003921634,0.0043453234,-0.010380421,0.011805497,-0.018306283,-0.041490965,-0.027197879,0.0137452,0.0077777756,0.0049192635,-0.011367116,0.006622443,-0.030166052,-0.01741996,0.00046018913,-0.008586437,-0.0047671366,-0.0076558497,0.008761266,0.0030093652,0.025831945,-0.0139598055,-0.0005725163,-0.004550916,-0.004468983,0.0022589283,-0.002074528,0.0014517353,-0.0005152945,0.005074588,0.010692725,-0.010598477,0.020159854,0.0037679963,0.007169943,0.00044781028,0.012870947,0.014561618,0.02741505,-0.0018005527,-0.009142438,-0.17315121,0.0068188896,0.009228136,0.012871385,-0.050577138,-0.0133023355,0.01140173,-0.0065600215,0.009241757,0.009473183,0.00040238167,-0.018726079,-0.02054768,-0.016549371,0.009317503,0.018441238,0.025154624,0.0038084963,-0.007309288,0.017496504,0.0055317655,-0.02195922,-0.0129778,0.008870187,-0.031060508,-0.019229798,0.012757313,0.02043721,0.01316649,-0.018886458,0.00036627913,0.0034615484,-0.033270046,-0.010336481,-0.005750328,0.008207868,-0.01696305,0.01210384,-0.009605942,-0.018138668,0.012462015,0.024993425,0.0039013014,0.0140052205,-0.0045805452,0.026476568,0.0028578201,-0.005945202,-0.015796801,9.064997e-05,-0.024044836,-0.0062906053,0.0070312563,-0.009335138,-0.0045788377,-0.0084598055,0.018732399,0.00032256427,-0.010238862,0.0020562315,-0.0009553524,0.0047044563,-0.009418225,0.015060972,0.023254408,0.013844341,-0.008698702,0.0050910413,-0.00027146738,0.0011178919,-0.015222622,-0.007903399,-0.032211404,0.0022540581,0.01314097,-0.025183033,0.0029800504,0.013131896,-0.0038102467,-0.008476467,-0.0049142526,-0.009017721,0.016626181,0.005444969,-0.017335141,0.004449676,-0.013610472,-0.026031705,0.011349238,0.009669302,0.01988677,0.028032415,0.0073085176,-0.008365956,-0.01525304,-0.0057724128,-0.004647705,0.014314771,0.0070860637,-0.003765714,0.0071742074,-0.022035362,-0.00828901,-0.02527833,-0.018309873,-0.014248831,0.028471995,0.0007180291,0.00012547201,-0.002658742,0.026099116,-0.0074787736,0.0063095745,0.0049685943,0.009909836,0.027142696,0.02427422,-0.004762362,-0.0008224713,0.014058398,0.022284627,0.026717514,-0.010600035,-0.012073591,0.016995097,0.010220552,-0.0012042562,0.023828793,-0.00014010405,-0.017969081,-0.015277133,0.014399337,0.007348582,0.0125760995,0.005224814,-0.0074946294,0.0018979879,0.012099793,0.007979782,0.0022001131,0.007984631,0.0030733668,0.0052541047,0.026712587,-0.019429764,0.00840246,0.022456756,0.014872356,-0.013317639,0.0022583904,0.02106628,0.025056893,0.014257613,0.017891157,-0.0056858025,0.010754104,-0.018122096,0.013895635,0.026410898,-0.012502988,0.0041328482,0.00089613494,-0.0060387217,0.0024987503,0.001456055,0.006613134,-0.020462345,-0.014822221,-0.02181924,-0.00091614417,-0.013628226,-0.010075695,-0.007206583,0.01631969,-0.011077131,-0.021747816,-0.0067793555,0.02999858,0.009434165,0.0076709324,0.004058469,0.016053615,0.00570924,-0.0007548974,0.008716205,0.006249926,-0.015980097,0.0059949406,0.008326763,-0.016094299,-0.00040647888,-0.021304952,0.019383412,0.0011787822,-0.003928805,0.024301128,0.028805977,0.0014502802,0.0014648316,0.002085479,-0.012782903,-0.013006973,-0.018303037,0.0077769975,0.017340261,0.02767187,-0.005028093,-0.011722145,-0.118845776,-0.0007560159,-0.0136583075,0.0052044345,-0.02556244,0.030178739,-0.0011648628,-0.01715193,-0.028950676,0.008533884,-0.014677739,0.004757809,0.020846091,-0.036330324,0.0015888811,0.01704772,0.0053749788,4.642822e-05,-0.010358071,0.0074535594,0.014553233,-9.204134e-05,-0.19375637,-0.02223786,-0.0027313284,0.003543591,0.0130467955,0.006159899,0.004972285,-0.014476843,-0.0128671,0.012641908,-0.00020998712,0.006015831,-0.0049187695,0.016000517,-0.023515688,0.023816513,0.002926843,0.035054207,0.008785736,-0.00050589826,-0.00051568117,0.02214742,0.0030660455,0.022464557,0.0012658188,0.0011102383,-0.0030941097,-0.00072509533,-0.026236203,-0.020014139,0.011987191,0.023381123,0.01656887,0.004215717,0.01599856,0.004309585,0.010828276,-0.009760129,-0.0121505,0.008100319,-0.007307936,-0.002346418,0.012829657,0.028211057,-0.01070049,0.011713153,0.022187935,-0.023921642,0.0200304,0.007731818,0.02232579,-0.020483673,-0.0037020962,-0.008274544,-0.012551254,-0.0056326427,0.02399798,0.0008975306,-0.018504592,0.016720897,0.009476934,-0.0019836535,-0.013907008,0.020311538,0.0096366955,0.01763082,0.0036660598,0.023902185,-0.03692448,-0.0026792376,0.0008023088,-0.023346273,0.010149365,-0.0044153747,0.043835502,-0.011958576,-0.024665514,-0.0022098748,0.015619306,-0.007049895,-0.008903939,0.008805366,-0.0013090341,0.0011664231,-0.025104014,-0.011447774,-0.027709033,0.022546073,0.014427669,-0.0034239963,0.002244842,-0.002092184,0.0013366037,-0.016605768,-0.00632537,-0.013193731,0.0038718816,0.0062006,0.0029372915,-0.0053972993,-0.028721917,0.009304469,-0.0059974818,0.00968011,0.01573569,-0.025972795,0.009195888,0.00025393828,-0.0028524352,0.024693355,0.008241652,-0.010072187,0.038821,0.009955246,0.0034006154,0.0008931977,0.012233497,0.0071208132,0.010450246,-0.013082897,-0.0034617276,-0.014315605,0.012696776,0.012213048,-0.009631392,0.011727837,-0.024395078,0.0076508857,-0.044899467,0.010177332,-0.018126914,0.006258366,0.0068741953,0.011073179,0.011471188,0.0010873595,-0.014893382,0.00762338,0.0025108508,0.015576866,0.0053201346,0.0006511487,-0.009524568,0.0017962022,0.0066597904,-0.0072153136,0.017279873,0.0010711831,0.0028023655,0.011519944,-0.017237732,-0.012459318,0.008579936,-0.01109453,-0.01598872,-0.005754362,0.0006656824,0.0003447982,-0.00044294106,0.0008355896,0.009526074,0.008630719,0.01011955,0.003238978,-0.0017469936,-0.03307498,-0.18165128,0.028677223,-0.0027829444,0.0109473,-0.01470846,0.003242261,-0.0046107243,-0.013016188,-0.0049031023,0.0061241337,0.03870377,0.008126744,-0.014531894,0.006568846,-0.024342168,-0.014180403,0.0016329276,-0.00031353062,-0.045161303,-0.017589461,-0.002111639,-0.025045278,-0.015892323,-0.017673936,0.012680896,-0.019838925,-0.00030183204,-0.019377291,0.001117911,0.02540177,-0.017405791,-0.03294709,-0.024399905,-0.00975602,-0.00674349,-0.015138182,0.015378959,0.0037817727,-0.0214252,0.009957811,0.009417775,0.0011985687,-0.0010294172,0.0014821917,0.03151206,0.01183783,0.0256656,-0.060764324,0.013741744,-0.018259916,-0.011040887,-0.008156507,-0.016685696,0.006012704,0.0054249386,0.0013516354,0.015394398,-0.020798193,0.0064841113,-0.000451979,-0.014249,-0.017762477,0.015877098,-0.0065434678,0.02238913,-0.002342674,-0.01036987,0.07780118,-0.030232864,-0.010340499,-0.011893298,-0.020510046,-0.00194235,-0.014493601,-0.00093064556,-0.012919633,-0.025334667,-0.028802494,-0.022875153,-0.0052861064,0.012242837,-0.013869936,0.009045966,-0.007998194,-0.012721988,0.04182926,0.01709719,-0.0071922806,-0.002065978,0.008015714,-0.018508151,0.024119107,0.0033479647,-0.010923403,-0.016752182,-0.0051572495,0.02858605,-0.009154604,-0.010484173,0.007859336,-0.025117949,-0.0017321211,-0.0027729436,0.017835058,0.0207231,-0.017084466,-0.007281575,-0.015618755,0.020894263,-0.0017391344,-0.019604318,0.0051943464,0.0024156538,-0.024667988,-0.0048916293,-0.007587791,0.0057754247,0.0056399032,-0.02828206,0.01214068,-0.0042719278,-0.005327362,-0.006872331,-0.0063087936,-0.014944411,-0.0065680663,0.013936905,0.0022091852,0.0068089343,0.008151372,0.004512125,0.0057845004,0.016999299,-0.014099083,-0.007104545,0.00053625903,-0.026553081,-0.008491735,0.012131163,0.013179928,-0.0011913888,-0.003476037,0.017496834,-0.007913852,-0.003958018,0.013391995,0.008858713,0.024319146,0.0016909215,-0.008164708,0.020874979,-0.007280553,-0.0071046636,0.009255897,0.012452323,0.007931529,0.0060938024,-0.0030384436,-0.0033283893,0.019352365,0.028043758,-0.014986132,0.015175897,0.030594917,-0.0014547352,0.005298112,-0.0003707389,0.0013053162,-0.02441938,-0.0055914004,-0.013364838,-0.02214573,-0.0064650294,0.013939903,0.0016610129,-0.0036058028,-0.028103504,-0.007922881,0.018757261,0.010200937,-0.003384624,-0.01759996,0.007709325,-0.0030929137,0.013630984,0.021700215,-0.0069761886,0.012862825,-0.030691,0.034513965,-0.025085405,-0.0165657,0.004885402,0.04491286,-0.01315139,0.0021210911,-0.0068476927,-0.015908223,-0.026895143,-0.032235518,-0.011974648,0.0018904816,-0.0010890594,0.007917436,0.01091449,0.009603598,0.0097498065,-0.008533733,-0.023138635,0.0037678625,0.00021416067,-0.0071298755,0.009299232,-0.0053877323,-0.006663944,0.019654013,0.010192448,0.0036170718,0.013564577,0.007466938,-0.008855428,0.00782749,0.02504217,-0.0014623975,-0.01853823,0.049944524,0.034283243,-0.019670725,-0.0036781412,0.0023622278,-0.019136792,0.021693446,-0.023152223,0.024471536,-0.01209903,0.010256555,0.018670356,0.010574498,0.0064435927,-0.01345114,0.002779007,0.021707317,0.0034340946,-0.016408952,0.008964887,-0.020118428,0.024909018,0.0011059714,-0.0070905583,-0.007915961,-0.0056153657,0.008670121,-0.02885155,-0.017471923,0.005978176,-0.008556352,0.016370045,-0.022881957,0.012423057,0.018327244,0.019280944,-0.029781424,0.016762419,-0.011322232,0.013386099,0.019535784,0.0023753464,0.005318165,0.0045029465,-0.0014180137,0.01402531,0.011216201,0.0036135803,0.016657893,0.0008947923,-0.0034024406,0.009763596,-0.003466336,0.004388997,-0.001929939,0.013596381,0.032260083,0.009448413,-0.010275822,-0.004490023,0.011455077,0.025025632,-0.007773393,-0.008548751,0.0083552655,-0.005541124,-0.0005607724,0.010813329,0.0046312045,0.0117101995,-0.007999053,0.008593839,0.006777229,-0.023434421,-0.004567262,0.010263471,-0.037887163,-0.007312522,-0.006549991,-0.013916588,-0.008267773,0.00539047,-0.0013827702,-0.0051414804,0.011608845,0.011073781,7.555816e-05,-0.007350691,-0.0029177514,-0.011864658,0.011605726,0.015393484,0.009673752,-0.003000916,-0.0014993947,-0.009774083,0.0045472616,0.0016482419,-0.0063679055,-0.0058193156,0.009353056,0.014377102,-0.0016489694,-0.02032699,0.004976616,0.024375703,0.06321888,0.0041550784,0.0035583246,-0.011140217,0.00034700893,0.00029895318,0.004873095,-0.0074700285,-0.003576805,0.0054194774,0.008540435,0.010882984,0.015987165,0.013762012,-0.009907123,-0.0017053854,0.02836589,0.0053481027,0.0059645986,-0.017324733,-0.021232067,0.0017565519,-0.009642874,0.00901599,-0.009769407,0.13216189,-0.0061257756,-0.009517702,0.014541244,0.006094854,0.013449831,0.0022097481,0.003139386,0.0046526324,0.007064673,0.014253848,-0.0013563804,-0.012446109,0.007213515,0.0078122155,0.013654854,-0.026007548,-0.027082793,-0.011164981,-0.018433137,-0.018119723,-0.0073372554,0.0051692673,0.004983952,-0.009279916,0.005918972,0.0036818387,0.007826934,-0.020978948,0.015126166,-0.00973733,0.019291695,-0.008763817,0.005920359,-0.0019874277,0.0037276843,-0.009231625,-0.00036465508,0.0027726404,0.0038359712,0.011727361,0.02489336,-0.017104192,-0.011372531,0.0013084813,3.2736734e-05,0.022002222,0.0028495728,0.0070863618,-0.0080413455,-0.0070765684,-0.012186331,0.0004921137,0.017256355,-0.011344234,0.014725966,0.000126097,-0.020947164,-0.017529868,0.0036545792,-0.122767545,0.026170932,0.008169145,0.027484737,-0.005689503,0.0017467284,0.0119522,-0.016770247,-0.0060468963,-0.008047089,0.0036263524,0.015917202,-0.005342757,0.0030713608,-0.017112778,-0.05613707,-0.009020024,0.009676706,-0.004662268,-0.020994069,0.003289172,0.027887201,-0.012655804,-0.011135772,-0.010037907,-0.0003324449,-0.0032058407,-0.012082445,-0.009212104,0.010816027,-0.01572329,-0.004411562,-0.01811907,0.0011690748,-0.02781737,0.006423988,0.017565127,-0.0036239023,0.00069194747,0.011579184,0.014486961,-0.033616528,0.01401865,0.007325516,0.0070394035,-0.010574401,-0.003697104,0.008308539,-0.042502105,0.0066867485,0.013649722,0.007983468,0.0010487265,-0.00054967095,-0.0023614033,-0.008130766,0.020295598,0.022039138,-0.004793133,-0.006722467,0.097114764,-0.016470503,-0.0036102156,-0.011119201,0.013685648,-0.015148085,0.005397812,-0.0032348223,-0.0028582786,0.0025646135,0.0005277669,0.004348902,0.0093620885,-0.005965119,-0.0008070801,-0.0034249388,-0.013572277,0.012358797,-0.02209955,0.009668153,-0.005418925,-0.01894724,-0.05738144,-0.012135589,0.0064841574,-0.012687035,0.005517396,-0.0041402937,0.0052280203,0.015507918,0.0074976636,0.00069600774,-0.010110079,0.0069563137,-0.011152474,-0.033246335,-0.013951082,-0.020706732,-0.002274528,0.0049529606,-0.0018307053,-0.01709644,-0.0016954811,-0.010677429,-0.004437337,-0.01308788,0.034998696,0.0040557585,-0.02396423,-0.003922739,-0.0013598342,0.006493559,0.02187002,-0.011223836,0.007117774,-0.014858044,-0.00124092,0.008441032,0.0025234432,-0.013194977,-0.01720665,-0.012174591,-0.0056293374,0.013082192,0.023910059,-0.026983034,-0.002690721,0.0020511074,0.006062679,0.012037221,0.0006308645,-0.007621143,0.0055589094,0.021691676,-0.0029643348,-0.016096978,-0.001683717,-0.020010184,-0.009557132,-0.019050108,-0.008277977,0.0095720505,0.005101455,0.0058910106,0.0071378015,0.012960491,-0.007817816,-0.022921333,-0.004551609,-0.030366126,0.018351806,-0.013609936,-0.019679824,0.015688423,-0.0063646655,0.10411851,0.003982904,-0.0008931703,0.010956808,-0.027187414,-0.009438657,0.008117888,0.029845072,0.023345519,-0.0012863307,0.0017689143,0.0042056222,-0.020786308,6.094271e-05,-0.04256821,-0.014912396,0.0041936734,0.0056614387,0.015150507,0.0003312264,-0.013772484,-0.02859275,0.010800471,0.003146286,-0.005896067,9.248959e-05,0.0029412813,0.004118758,0.0026505208,0.016061902,-0.011018714,0.008052162,0.0037885865,0.011390943,0.0022600524,0.0086793,-0.021652684,-0.004220591,-0.004028189,-0.0004192392,-0.0054382733,0.0013911221,0.011766499,0.0047665685,-0.00027063407,-0.011756867,0.0086820675,0.010241529,0.0121503305,0.008435205,0.011757473,0.017904645,0.0066851894,0.0021200408,-0.0145837115,-0.0047864444,-0.007803949,-0.015100844,-0.019723037,0.0010480257,0.011146474,-0.0092282435,0.01375764,-0.008890522,-0.023773259,0.016317809,-0.0044958186,0.018029768,0.0007499947,0.0023875197,0.008693175,0.0015881333,0.00086973363,-0.01837801,0.009345878,0.009450284,0.03456754,-0.0002718112,0.0030375007,-0.016462397,-0.011793604,0.012131934,-0.0138556585,-0.0037131533,-0.038927432,0.0087030055,-0.016821492,0.004105893,-0.008382749,0.0007583608,-0.024042238,0.00085536775,-0.017192908,0.037434228,-0.026591394,0.0008812006,0.008729628,-0.0015130584,-0.009744368,0.0075912685,-0.009104131,-0.009228715,-0.013881388,-0.019301942,-0.015058607,-0.008281331,-0.008385889,0.017358882,0.019808937,0.0076198536,-0.00046406235,-0.003789706,0.012182463,0.004601125,0.0005680406,-0.007956577,0.0033253664,-0.0012878726,-0.030822055,0.009647575,-0.024374334,-0.0055618826,0.0205682,-0.0037089465,0.040457938,0.012004824,0.0062136496,-0.011548786,-0.036489885,0.011170232,-0.017900417,0.0052545886,-0.03112173,0.027666396,-0.0074856845,0.01755006,-0.0012831793,0.011935482,9.31842e-05,0.00082660414,-0.013766026,0.009950447,0.0042819744,-0.013971551,-0.019403102,0.010080683,-0.0115872985,-0.006802557,0.015640385,-0.007522768,0.025411727,0.025531175,0.0096513,-0.016371699,-0.033010818,-0.010443609,-0.00919829,0.020994814,-0.007958842,0.017974379,0.009030327,-0.001386526,0.004744533,-0.0014656998,-0.020989727,-0.018522892,0.010582562,-0.015399495,-0.009281871,-0.008007043,-0.0062105157,-0.0042417264,0.009184464,0.004239686,-0.009860466,0.01231125,-0.010040172,0.010974711,-0.012442629,-0.0017583738,0.0043759937,0.009846842,0.012320998,0.009506568,-0.026057009,-0.017228913,0.002739118,0.009092419,-0.0012821164,-0.009592793,0.007877123,-0.0093888985,0.0066496134,-0.006291732,0.026882445,0.001866372,0.004535121,0.029102013,0.011460796,0.019216517,0.017344516,-0.007091183,0.013408749,0.01201007,0.011518809,0.0063682194,-0.013696718,-0.014233001,-0.007884294,-0.0044885455,0.013617111,-0.016058099,0.011435418,-0.016718447,0.017949738,-0.016360102,-0.013763102,-0.01587546,-0.0034996064,-0.0014144147,-0.013215397,-0.004892649,0.0033908552,0.011176867,0.002818474,0.001587486,0.0019114567,-0.029511388,0.019280799,-0.022138342,-0.00065264443,-0.014663963,0.031349663,-0.017425556,0.06811763,-0.012066748,-0.019780215,0.01904286,-0.0009595953,-0.02729365,0.0072977752,0.002380101,0.005857904,0.0094302185,0.0051742992,0.0099782795,0.000588391,0.0363653,0.005974579,-0.0016584133,0.003965582,-0.008093536,-0.029529624,-0.012003576,-0.012540019,-0.004703606,-0.006831174,-0.0086949775,0.0070970124,-0.024619956,-0.0067234966,0.015061283,-0.01997446,0.0017904913,0.008458364,-0.0030546784,0.0028987937,-0.009288588,0.0049853264,-0.005329723,0.0147230765,0.002333351,-0.0058330805,0.0053058937,0.025318004,0.0017061202,-0.008324921,-0.013714731,-0.008648832,-0.005745539,-0.010887506,-0.018530019,0.002156379,0.009069509,0.019372715,0.0032497658,0.020643577,0.01400226,0.0051361048,-0.00953396,0.062722236,-0.012797755,-0.0035226317,0.0074529587,-0.006431911,-0.012725226,-0.00542101,-0.009570732,0.004905893,0.024333252,-0.0065637287,0.0072577395,-0.008828143,0.007988939,-0.0039803963,-0.0020675885,-0.007619407,-0.017589994,-0.0062786387,0.0031120246,-0.003994918,-0.013832598,-0.01375907,0.022865187,-0.0055259494,-0.029613473,0.01757481,0.0031226275,-0.008489461,-0.004598796,0.00511893,-0.0067041544,0.02051179,-8.174082e-05,0.008775965,-0.0027833239,0.019303905,0.003039204,0.00033409172,0.002337304,-0.0048702373,-0.013622257,-0.012257066,0.013175122,0.005615405,-0.012400145,-0.017287815,0.018741649,-0.0031381412,0.0105035445,0.0019685812,0.017411849,0.012686818,-0.00096013123,-0.0019770546,-0.0056977584,-0.010535414,-0.0052589453,0.116921134,0.0067676897,0.013159197,0.024193605,0.00452986,-0.0057486175,0.016275898,-0.001862611,0.013100144,0.019867152,-0.018236537,0.011885843,-0.0032325028,-0.0038609141,0.018324574,0.011067228,0.01770629,0.01999177,0.002400221,0.022271892,0.017385358,0.027858507,-0.006098695,0.0025956477,-0.011965198,-0.015163063,0.012984494,-0.015104902,-0.0106540695,-0.0009638615,0.015661241,0.019766225,-0.023419315,-0.014116004,-0.010024946,-0.002800597,-0.0060621058,-0.016180014,0.0012565833,-0.026931422,-0.011037895,0.0080511,0.0020103536,-0.017612318,-0.008583892,-0.0067945626,-0.00055673433,-0.01704877,-0.0067481766,-0.0062507475,0.0020706872,0.010623312,-0.014192698,-0.008800215,0.0036855298,-0.01141284,0.0043060784,0.013906324,0.010356051,-0.0087126065,-0.012469764,0.013663403,-0.021729946,-0.031276263,-0.018415421,-0.008015824,0.009812827,0.005542543,-0.009803851,0.0077837068,0.0205609,-0.011418454,0.0025262292,-0.01028412,0.007687784,-0.0018868123,0.003166673,0.018182835,-0.0034927784,0.004760841,-0.009238327,-0.009774197,-0.0072645238,-0.012032204,0.0043091923,-0.00017893495,-0.014044569,0.00573578,-0.019492518,-0.021102097,-0.006081183,0.016183455,-0.00041455834,0.013612025,0.012003801,-0.0021430636,-0.0008585188,0.020074418,0.01449329,0.02892768,-0.0050369096,-0.046336148,-0.015010948,-0.019002462,0.0011523482,-0.0046885256,-0.012362801,-0.006088652,0.0021062884,0.0072050686]	0	0	t	b7e52df6-21dd-4fa2-bb0d-11961f360cd1	2026-07-28 09:49:45.66964	2026-07-28 09:49:45.669841
b6977faa-2b77-4b04-a375-bb67505b6015	What file formats and attachments are supported in live chat?	Technical	SupportHub live chat supports images (.jpg, .png, .gif, .webp), PDF documents, text files, and logs up to 10MB in size. Click the Paperclip (📎) icon next to the chat composer to upload attachments.	\N	89	35	t	\N	2026-08-05 16:03:56.671441	2026-08-05 16:03:56.671548
15b631b3-69ba-4073-a620-f4a347b94d35	How do I reset my account password or enable 2FA?	Account	You can reset your password anytime from the Login page by clicking Forgot Password. To manage Two-Factor Authentication (TOTP), navigate to Customer Profile > Security Settings.	\N	120	54	t	\N	2026-08-05 16:03:56.67175	2026-08-05 16:03:56.671829
e4634581-a28f-4305-958e-81fa34d0d3cd	What are your support operating hours and AI response times?	General	SupportHub AI Assistant operates 24/7 with instant responses (<1 minute). Human support agents are available Monday through Friday from 9 AM to 6 PM EST with average response times under 15 minutes.	\N	64	28	t	\N	2026-08-05 16:03:56.671984	2026-08-05 16:03:56.672054
40ac66cf-a549-41e0-9f4c-ff5f0397bc71	How is Customer Satisfaction (CSAT) calculated?	General	When a support ticket or live chat is resolved, customers can rate their experience on a 1-to-5 star scale and leave feedback comments. The CSAT rating is calculated as the average of all verified customer reviews.	\N	31	14	t	\N	2026-08-05 16:03:56.672248	2026-08-05 16:03:56.672333
2e7bd3d4-dffd-4d13-9b6a-ecb2c43f0b83	How do I request an updated invoice or receipt?	Billing	To download or request your monthly invoice, go to Dashboard > Billing > Invoice History. You can click any invoice to generate a PDF download or send a copy directly to your account email address.	\N	42	19	t	\N	2026-08-05 16:03:56.671053	2026-08-05 16:03:56.671168
\.


--
-- Data for Name: macros; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.macros (id, title, body, category, created_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messages (id, ticket_id, sender_id, sender_type, body, attachments, created_at, external_message_id, body_html) FROM stdin;
ef58dc48-62de-4888-a9c6-8395c03d5e33	bc18f726-c70e-4250-ba9d-aa776450af95	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	how can i reset my password!	\N	2026-07-28 08:45:26.324762	\N	\N
20efacf1-d802-45b0-8b5c-0f558ab326a9	adaa9dee-e0d0-45f1-84fe-a098d509412f	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	how are you.	\N	2026-07-28 08:50:07.156523	\N	\N
3e141de5-4b64-41e8-b963-cf7c98ea0375	adaa9dee-e0d0-45f1-84fe-a098d509412f	646b7a11-99f7-4721-b183-f74dbec4bcc5	agent	hi , how can i help you?	\N	2026-07-28 09:12:08.475494	\N	\N
f633d6c3-6ce3-4532-bb36-a1fc05179899	adaa9dee-e0d0-45f1-84fe-a098d509412f	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	can i get your Mobile Number?	\N	2026-07-28 09:12:41.709635	\N	\N
de2c4016-2b96-4582-bb24-fbd20dc596db	adaa9dee-e0d0-45f1-84fe-a098d509412f	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	>>>	\N	2026-07-28 09:15:26.774026	\N	\N
0f4fcc5f-a221-4767-acf7-f17d2f6c409f	adaa9dee-e0d0-45f1-84fe-a098d509412f	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	ccc	\N	2026-07-28 09:15:43.468129	\N	\N
b2e79752-78ce-4db1-a801-4ff1e96f20b4	02c8922b-d6bd-4125-96d4-91e726de716b	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	can you help me to change my password	\N	2026-07-28 10:06:06.884387	\N	\N
e98dcf43-481e-48bc-8a72-345846689768	02c8922b-d6bd-4125-96d4-91e726de716b	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	I forgot my password, how do I reset it?	\N	2026-07-28 10:06:34.866321	\N	\N
217139b3-2b18-4520-912d-aafde9ed7bdf	6ef2fc35-1afd-40cc-8036-53b0f203d501	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	How do I reset my password	\N	2026-07-28 10:11:11.662368	\N	\N
aa08a30e-7bdb-4d9b-830b-66525c472211	6ef2fc35-1afd-40cc-8036-53b0f203d501	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	How do I reset my password	\N	2026-07-28 10:11:36.046333	\N	\N
e53fdd98-0410-4719-8771-001fbec056ca	6ef2fc35-1afd-40cc-8036-53b0f203d501	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	How do I reset my password	\N	2026-07-28 10:11:47.915874	\N	\N
22b39ca2-a044-4ab8-a094-de404c41d5ef	6ef2fc35-1afd-40cc-8036-53b0f203d501	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	How do I reset my password	\N	2026-07-28 10:22:06.502787	\N	\N
75c0a6c7-2052-49a3-807a-77e01d1e075d	6ef2fc35-1afd-40cc-8036-53b0f203d501	\N	ai	To reset your password, please follow these steps:\n\n1.  Go to the login page and click on the "Forgot Password?" link located below the login button.\n2.  Enter the email address associated with your SupportHub account.\n3.  Check your email inbox. You should receive a secure password reset link within 2 minutes. (Be sure to check your spam folder just in case!)\n4.  Click the link and enter your new password.\n\nPlease ensure your new password is at least 8 characters long and contains a mix of letters, numbers, and special characters. If you no longer have access to your email address, please contact support for manual verification.	\N	2026-07-28 10:22:09.283815	\N	\N
de5d3276-3ee2-4216-8350-1ccb82639b96	6ef2fc35-1afd-40cc-8036-53b0f203d501	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i am satisfied, thanks. That fixed my issue.	\N	2026-07-29 08:07:20.475493	\N	\N
78ed3562-6274-4021-a42c-dccc0d997af9	6ef2fc35-1afd-40cc-8036-53b0f203d501	\N	ai	It was my pleasure to assist you!\n	\N	2026-07-29 08:07:24.098906	\N	\N
a06f3d68-03f8-4be2-bbbf-677e5f5d4654	76eda5ce-025d-41c8-9c2d-38e6fb755267	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	I want to upgrade to the Pro plan, how do I do that? What are the payment options?	\N	2026-07-29 09:10:18.595227	\N	\N
a40a5187-e0c9-4960-a0ab-c4217591d1da	76eda5ce-025d-41c8-9c2d-38e6fb755267	\N	ai	I don't have enough information to answer that, but I will connect you with a human agent shortly.	\N	2026-07-29 09:10:23.007882	\N	\N
48529061-ac44-46fb-bc70-7acb57a11771	f3ba1e50-7e93-4680-aef0-17bab9230f05	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	I want to upgrade to the Pro plan, how do I do that? What are the payment options?	\N	2026-07-29 09:11:54.609355	\N	\N
bcbf82a4-f925-4a18-baf4-fa30e42c34a9	f3ba1e50-7e93-4680-aef0-17bab9230f05	\N	ai	I don't have enough information to answer that, but I will connect you with a human agent shortly.	\N	2026-07-29 09:11:58.859439	\N	\N
468317c9-e874-46b3-b52a-abdcdf06ef06	c36dc01d-d17b-4314-9637-89468d768f40	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	This is ridiculous and unacceptable. Your service keeps crashing and I demand to speak to a human manager RIGHT NOW!	\N	2026-07-29 09:32:05.50387	\N	\N
50fde39d-3ba6-4604-98be-ca93dff23d70	c36dc01d-d17b-4314-9637-89468d768f40	\N	ai	I have escalated your ticket to a human manager. They will contact you shortly.	\N	2026-07-29 09:32:09.240923	\N	\N
69eb3069-e710-461c-88e6-5c2879ad782d	daba0e8c-c1f1-49d8-8854-562752613ea8	\N	ai	Hello! I am your AI Assistant. How can I help you today?	\N	2026-07-29 09:37:42.545859	\N	\N
c832f403-3421-4d13-8c05-58434464844b	daba0e8c-c1f1-49d8-8854-562752613ea8	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	URGENT EMERGENCY: Our production server is completely down and all our users are getting 500 errors! Please help immediately!	\N	2026-07-29 09:38:02.305456	\N	\N
91ec4867-5a41-42ef-b7be-871f99f58ec4	daba0e8c-c1f1-49d8-8854-562752613ea8	\N	ai	Your ticket has been updated to urgent priority. We understand this is a critical situation and are escalating it to the appropriate team for immediate assistance.	\N	2026-07-29 09:38:06.553229	\N	\N
21c627f6-c872-4ad5-a80a-97746fb56089	c36dc01d-d17b-4314-9637-89468d768f40	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i am satisfied, thanks. That fixed my issue.	\N	2026-07-29 09:38:36.121601	\N	\N
8cdacaa2-2d72-44ae-97fd-52c133d35f8c	c36dc01d-d17b-4314-9637-89468d768f40	\N	ai	I'm glad I could help! Your ticket has been marked as resolved.\n	\N	2026-07-29 09:38:39.699754	\N	\N
a6123876-78e3-486b-bf9d-537fd6e2aea6	bc18f726-c70e-4250-ba9d-aa776450af95	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	i am satisfied, thanks. That fixed my issue.	\N	2026-07-29 09:56:12.876877	\N	\N
db24a3e3-219f-4c53-a557-39cd7838b4c6	02c8922b-d6bd-4125-96d4-91e726de716b	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:00:58.920087	\N	\N
251f9fed-fee9-44ad-a600-0f86fa195974	02c8922b-d6bd-4125-96d4-91e726de716b	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:07:44.211384	\N	\N
b9e74e4c-3bda-4115-9cc8-d7a24cce7e00	76eda5ce-025d-41c8-9c2d-38e6fb755267	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:17:02.678999	\N	\N
a69590f9-877e-4b61-91b7-afead33a4073	76eda5ce-025d-41c8-9c2d-38e6fb755267	\N	ai	I'm sorry, our AI assistant is temporarily unavailable due to high demand. A human agent will assist you shortly.	\N	2026-07-29 10:17:06.452942	\N	\N
b339bd1b-45cb-40d2-8eba-16b7e98ff976	daba0e8c-c1f1-49d8-8854-562752613ea8	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:17:23.522162	\N	\N
737cbb53-0744-4e64-adf3-91fa1f8f93d3	daba0e8c-c1f1-49d8-8854-562752613ea8	\N	ai	I'm sorry, our AI assistant is temporarily unavailable due to high demand. A human agent will assist you shortly.	\N	2026-07-29 10:17:25.442464	\N	\N
e7a47f10-7cc8-40b9-9e7a-c9cdfda3f3e5	daba0e8c-c1f1-49d8-8854-562752613ea8	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:19:37.916362	\N	\N
324c25a5-faab-46b3-a3ef-c5944e672205	daba0e8c-c1f1-49d8-8854-562752613ea8	\N	ai	I'm sorry, something went wrong on our end. Please try again in a moment.	\N	2026-07-29 10:19:41.232094	\N	\N
79bbef96-16ce-41f8-ba60-1b720beb6327	f3ba1e50-7e93-4680-aef0-17bab9230f05	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:20:27.948353	\N	\N
e7738016-729b-47d5-9c24-4980629ddc6c	f3ba1e50-7e93-4680-aef0-17bab9230f05	\N	ai	I'm sorry, something went wrong on our end. Please try again in a moment.	\N	2026-07-29 10:20:29.154979	\N	\N
30135c2c-fe43-4998-a561-7f65a3d7f02c	daba0e8c-c1f1-49d8-8854-562752613ea8	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:26:48.219465	\N	\N
56ff507a-03dc-47aa-b77d-a2c4ef458d60	daba0e8c-c1f1-49d8-8854-562752613ea8	\N	ai	I'm sorry, something went wrong on our end. Please try again in a moment.	\N	2026-07-29 10:26:50.092066	\N	\N
173c4eb7-32de-4fe9-92fd-50a654d1a7cc	37334a0c-89e9-4e9d-953c-902c0bf02ec6	\N	ai	Hello! I am your AI Assistant. How can I help you today?	\N	2026-07-29 10:31:05.123558	\N	\N
208e3ca6-16a9-4547-8229-c508c37f93e4	37334a0c-89e9-4e9d-953c-902c0bf02ec6	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	I want to upgrade to the Pro plan, how do I do that? What are the payment options?	\N	2026-07-29 10:31:10.718443	\N	\N
be167eea-3826-473f-a18b-e359e2312af5	37334a0c-89e9-4e9d-953c-902c0bf02ec6	\N	ai	I'm sorry, something went wrong on our end. Please try again in a moment.	\N	2026-07-29 10:31:12.237357	\N	\N
ff3e0864-1f1c-453b-9e38-ee0f67c58de2	daba0e8c-c1f1-49d8-8854-562752613ea8	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:38:26.436992	\N	\N
7b6cd7e4-2899-46a0-9f4e-f89be4539db6	daba0e8c-c1f1-49d8-8854-562752613ea8	\N	ai	I'm sorry, our AI assistant is temporarily unavailable due to high demand. A human agent will assist you shortly.	\N	2026-07-29 10:38:28.277557	\N	\N
9cce4423-aa48-4ecb-8f37-838368efc350	37334a0c-89e9-4e9d-953c-902c0bf02ec6	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:38:47.432977	\N	\N
ec28a2dd-99ca-4568-9076-d153b9bd1301	37334a0c-89e9-4e9d-953c-902c0bf02ec6	\N	ai	I'm sorry, our AI assistant is temporarily unavailable due to high demand. A human agent will assist you shortly.	\N	2026-07-29 10:38:48.4474	\N	\N
6ecbe156-bd15-4613-9a31-eeaef90e171e	37334a0c-89e9-4e9d-953c-902c0bf02ec6	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:45:05.750432	\N	\N
4bf123d5-79d2-4429-89a3-55ae36bc8425	37334a0c-89e9-4e9d-953c-902c0bf02ec6	\N	ai	I'm glad to hear that your issue is fixed! Have a wonderful day.	\N	2026-07-29 10:45:08.24613	\N	\N
0502a0cc-c565-44a8-a218-c020af64ef0f	a6b15714-29b0-4930-a495-f55fd5e404da	\N	ai	Hello! I am your AI Assistant. How can I help you today?	\N	2026-07-29 10:49:47.094345	\N	\N
113fcc29-b3ff-46c7-a20c-3ad5574356f1	a6b15714-29b0-4930-a495-f55fd5e404da	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	how can i reset my password!	\N	2026-07-29 10:49:49.905295	\N	\N
7351c6ec-42fb-4e77-88a3-581313bf096c	a6b15714-29b0-4930-a495-f55fd5e404da	\N	ai	I'm glad to hear that fixed your issue! I've marked this ticket as resolved. Have a great day!	\N	2026-07-29 10:50:08.588867	\N	\N
ccdef2b5-8916-4bbb-8647-d8067839a228	8b143420-d8df-4fc9-a1fa-c1faba787dc7	\N	ai	Hello Customer User! How can I assist you with your support request today?	\N	2026-08-05 13:52:39.604898	\N	\N
ea264ee9-68dd-45af-91e1-544e739dc918	a6b15714-29b0-4930-a495-f55fd5e404da	\N	ai	To reset your password, please follow these steps:\n\n1. Go to the login page and click on the **"Forgot Password?"** link located below the login button.\n2. Enter the email address associated with your SupportHub account.\n3. Check your email inbox. You should receive a secure password reset link within 2 minutes (be sure to check your spam folder just in case!).\n4. Click the link and enter your new password.\n\n*Note: Please ensure your new password is at least 8 characters long and contains a mix of letters, numbers, and special characters. If you no longer have access to your email address, please let me know so we can assist you with manual verification.*	\N	2026-07-29 10:49:53.646048	\N	\N
2a3b5dfc-870e-499d-b142-4f617560e319	a6b15714-29b0-4930-a495-f55fd5e404da	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-07-29 10:50:05.719377	\N	\N
e46b7191-ab02-4601-bdab-1a00915ef3ae	844e7711-2832-4ca2-bcda-0eb9892feb8f	\N	ai	Hello! I am your AI Assistant. How can I help you today?	\N	2026-07-30 07:52:46.938877	\N	\N
f763266a-5c6e-4d87-a116-b611b794cac6	844e7711-2832-4ca2-bcda-0eb9892feb8f	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	how are you.	\N	2026-07-30 07:52:52.332114	\N	\N
3b5c5635-d38f-44f7-a104-0d67eddc2c62	844e7711-2832-4ca2-bcda-0eb9892feb8f	\N	ai	Hello! I am doing well, thank you for asking. How can I help you with your SupportHub account or questions today?	\N	2026-07-30 07:52:55.204836	\N	\N
508a80f7-7a7c-4fdf-8a52-d0a69afb5065	844e7711-2832-4ca2-bcda-0eb9892feb8f	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	how can i reset my password!	\N	2026-07-30 07:53:17.207097	\N	\N
9e1a7152-44fd-4fab-80cb-b0ae3808e217	844e7711-2832-4ca2-bcda-0eb9892feb8f	\N	ai	To reset your password, please follow these steps:\n\n1. Go to the login page and click on the "Forgot Password?" link located below the login button.\n2. Enter the email address associated with your SupportHub account.\n3. Check your email inbox. You should receive a secure password reset link within 2 minutes (be sure to check your spam folder just in case).\n4. Click the link and enter your new password.\n\nPlease ensure your new password is at least 8 characters long and contains a mix of letters, numbers, and special characters. If you no longer have access to your email address, please contact support for manual verification.	\N	2026-07-30 07:53:19.840281	\N	\N
d2631c00-3b5d-4e9b-b55d-e4969f54d3fe	844e7711-2832-4ca2-bcda-0eb9892feb8f	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	can you explain me in gujarati / hindi language	\N	2026-07-30 07:54:05.262854	\N	\N
8ff3079c-d4f4-4c9d-abf0-c26491ce8f46	844e7711-2832-4ca2-bcda-0eb9892feb8f	\N	ai	I don't have enough information to answer that, but I will connect you with a human agent shortly.	\N	2026-07-30 07:54:07.804878	\N	\N
368f0da2-2da5-4738-b2b7-4c2ab3dd5266	844e7711-2832-4ca2-bcda-0eb9892feb8f	646b7a11-99f7-4721-b183-f74dbec4bcc5	agent	sure	\N	2026-07-30 09:28:59.250347	\N	\N
6319f8e7-74a8-4c9e-af08-d5a753de25f3	844e7711-2832-4ca2-bcda-0eb9892feb8f	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	can you give me past orders?	\N	2026-07-31 04:45:01.890767	\N	\N
c34bc262-8878-4421-b585-309f906ff54e	844e7711-2832-4ca2-bcda-0eb9892feb8f	\N	ai	I don't have enough information to answer that, but I will connect you with a human agent shortly.	\N	2026-07-31 04:45:04.769479	\N	\N
e2772c19-0059-45bc-8516-7f4a6d2b4c6b	36f0f5f3-c7b8-4465-986c-2b5eb7a98df4	\N	ai	Hello! I am your AI Assistant. How can I help you today?	\N	2026-07-31 04:54:00.277075	\N	\N
747b3ff2-fb2d-45c8-b59c-7fe45b1f3ad3	36f0f5f3-c7b8-4465-986c-2b5eb7a98df4	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	55	\N	2026-07-31 04:59:13.708307	\N	\N
32520693-8443-4e96-8df1-01997682f0c9	36f0f5f3-c7b8-4465-986c-2b5eb7a98df4	\N	ai	I don't have enough information to answer that, but I will connect you with a human agent shortly.	\N	2026-07-31 04:59:16.486351	\N	\N
d43d17f5-aeef-425b-af20-370e215967fa	3c874d66-d5ff-41ab-b61e-df633cb87cb1	a0dbbcab-de50-46b6-a534-b3638ad07785	customer	Hello SupportHub team, I need help resetting my password.	\N	2026-08-04 08:15:53.125528	\N	\N
8d19a0b8-b374-44c6-b4f4-c7ebd951dfab	3c874d66-d5ff-41ab-b61e-df633cb87cb1	\N	ai	Thank you for reaching out to SupportHub! A support representative will review your message shortly.	\N	2026-08-04 08:16:06.217892	\N	\N
9c1b4a1f-9663-4a2c-9dcc-ff9cb15e0add	3c874d66-d5ff-41ab-b61e-df633cb87cb1	a0dbbcab-de50-46b6-a534-b3638ad07785	customer	Hello SupportHub team, I need help resetting my password.	\N	2026-08-04 08:40:20.825662	\N	\N
a0c2c6ce-072e-4d41-a877-fc78403d8fb6	3c874d66-d5ff-41ab-b61e-df633cb87cb1	\N	ai	Hello! I'd be happy to help you with that. To reset your password, please check your inbox for a password reset email, or visit our login page and click "Forgot Password." Let me know if you need any further assistance!	\N	2026-08-04 08:41:00.163374	\N	\N
c4ed689a-6d85-40a5-9eae-0ce69e6ea9b9	3c874d66-d5ff-41ab-b61e-df633cb87cb1	a0dbbcab-de50-46b6-a534-b3638ad07785	customer	Hello SupportHub team, I need help resetting my password.	\N	2026-08-04 08:41:52.732421	\N	\N
aa950316-78dd-499c-8e0c-e0674dd7d654	3c874d66-d5ff-41ab-b61e-df633cb87cb1	\N	ai	Hello again! It looks like you're still having trouble. Have you had a chance to click "Forgot Password" on the login page, or would you like me to trigger a new reset email for you?	\N	2026-08-04 08:42:16.750579	\N	\N
6ebcdfdf-cab6-4ec4-b427-f1d55dcf4ad9	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	98d7e49a-2551-4bb8-b425-3b3226046c7e	customer	Hi, I forgot my password again, please help.\r\n\r\n\r\n[image: Mailsuite] Sender notified with Mailtrack  ·  Opt out\r\n<https://u.list-prefs.com/en/privacy/opt-out/unsubscribe/049ded615c2e1c76d1b9642eb54b121e86ca07c7/70e20e8b5de56835f5b0a6c503e3b7efa1bd3d3d844583869c219f79efd39209f25c097d3505503f6737ebdf329475d6e9f0642e7e0e7fd4562d9805a0e43af8>\r\n08/04/26, 02:15:58 PM	\N	2026-08-04 08:46:30.87483	\N	\N
e17d42b5-9a2a-428c-8ce9-b62f97a08412	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	\N	ai	Hi there! I'd be happy to help you reset your password. \n\nPlease click the "Forgot Password" link on the login page and enter your email address. We'll send you a link to create a new one right away! Let me know if you need any further assistance.	\N	2026-08-04 08:46:46.889045	\N	\N
1ffe6343-1d34-4ba0-b7e4-d8647f9b6ee4	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	98d7e49a-2551-4bb8-b425-3b3226046c7e	customer	- Hi, can you help me with billing?\r\n-\r\n[image: Mailsuite] Sender notified with Mailtrack  ·  Opt out\r\n<https://u.list-prefs.com/en/privacy/opt-out/unsubscribe/6928ce43e7d7327c44521d254f221d45179922f0/70e20e8b5de56835f5b0a6c503e3b7efa1bd3d3d844583869c219f79efd39209f25c097d3505503f6737ebdf329475d6e9f0642e7e0e7fd4562d9805a0e43af8>\r\n08/04/26, 02:24:19 PM	\N	2026-08-04 08:54:36.781208	\N	\N
d6de6b08-679b-46a6-aea0-941098e9f248	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	\N	ai	Hi there! I'd be happy to help you with your billing question. What specific details can I assist you with today?	\N	2026-08-04 08:54:56.374848	\N	\N
f86a40cf-897f-49a8-9419-5a868b981f08	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	98d7e49a-2551-4bb8-b425-3b3226046c7e	customer	Hi, I forgot my password again, please help.\r\n\r\n\r\n[image: Mailsuite] Sender notified with Mailtrack  ·  Opt out\r\n<https://u.list-prefs.com/en/privacy/opt-out/unsubscribe/049ded615c2e1c76d1b9642eb54b121e86ca07c7/70e20e8b5de56835f5b0a6c503e3b7efa1bd3d3d844583869c219f79efd39209f25c097d3505503f6737ebdf329475d6e9f0642e7e0e7fd4562d9805a0e43af8>\r\n08/04/26, 02:15:58 PM	\N	2026-08-04 08:56:41.175307	\N	\N
8cd43690-72df-444f-9003-7ba7949a70b9	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	\N	ai	Hi again! No worries at all. \n\nJust head over to the login page, click the "Forgot Password" link, and enter your email address. We'll send you a reset link right away. Let me know if you run into any trouble!	\N	2026-08-04 08:57:02.731847	\N	\N
a6ef0f2e-270b-4587-bfec-e27bcaa625e6	3c874d66-d5ff-41ab-b61e-df633cb87cb1	a0dbbcab-de50-46b6-a534-b3638ad07785	customer	Testing fast background response.	\N	2026-08-04 09:03:32.746956	\N	\N
ee056360-5101-4fde-8134-4442d9599e35	3c874d66-d5ff-41ab-b61e-df633cb87cb1	\N	ai	Hello! Loud and clear—how can I help you today?	\N	2026-08-04 09:03:33.903634	\N	\N
a118b495-5e23-4002-b063-b944a9110dc2	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	98d7e49a-2551-4bb8-b425-3b3226046c7e	customer	- Hi, can you help me with billing?\r\n-\r\n[image: Mailsuite] Sender notified with Mailtrack  ·  Opt out\r\n<https://u.list-prefs.com/en/privacy/opt-out/unsubscribe/6928ce43e7d7327c44521d254f221d45179922f0/70e20e8b5de56835f5b0a6c503e3b7efa1bd3d3d844583869c219f79efd39209f25c097d3505503f6737ebdf329475d6e9f0642e7e0e7fd4562d9805a0e43af8>\r\n08/04/26, 02:24:19 PM	\N	2026-08-04 09:04:47.528633	\N	\N
38fd8c22-cf62-4f1c-8df0-29f3a7821cea	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	\N	ai	Hi there! I'd be happy to help you with your billing. What specific question or issue can I assist you with today?	\N	2026-08-04 09:04:48.374738	\N	\N
63465785-e19c-443e-914f-692c4bffff70	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	98d7e49a-2551-4bb8-b425-3b3226046c7e	customer	First payload text.	\N	2026-08-04 09:09:20.683738	test-idempotency-msg-99999@mailgun.org	\N
67e91a79-7c01-4bf3-ae21-388c0b769aa1	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	\N	ai	Hi there! How can I help you with that payload text today?	\N	2026-08-04 09:09:21.763207	\N	\N
ea65ab8b-88ff-4ce9-b482-13abfe6c5016	8b143420-d8df-4fc9-a1fa-c1faba787dc7	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Yes, I need help with my invoice.	\N	2026-08-05 13:55:26.45754	\N	\N
8408377c-f269-48b1-9fb0-a9001657dd3a	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	98d7e49a-2551-4bb8-b425-3b3226046c7e	customer	after 3 days of return : i stll not receive the refund\r\n[image: Mailsuite] Sender notified with Mailtrack  ·  Opt out\r\n<https://u.list-prefs.com/en/privacy/opt-out/unsubscribe/8fe7d020173fe3f1487f464e9684685a39c7db1b/70e20e8b5de56835f5b0a6c503e3b7efa1bd3d3d844583869c219f79efd39209f25c097d3505503f6737ebdf329475d6e9f0642e7e0e7fd4562d9805a0e43af8>\r\n08/04/26, 03:33:20 PM	\N	2026-08-04 10:05:30.506428	CAB9RiY4FWM-H13cn1a_AYDvP2TVxO-k1sTB5uGAKzMB5J+7WXg@mail.gmail.com	\N
2ac455b7-3806-4441-9044-317e43a3dff6	9afbd5c7-68a7-47ea-9d72-2e236f7ab91c	\N	ai	Hi there! I'm sorry to hear you haven't received your refund yet. Typically, refunds take about 3-5 business days to process and appear in your account after we receive your return. \n\nCould you please share your order number? I'll be happy to look into the status for you!	\N	2026-08-04 10:05:31.959542	\N	\N
aeb89160-18ec-42d3-8006-a3b7b1de3119	0c89ef0a-db9f-4fa9-ac8e-5f08d108f270	0973322f-a661-40b3-bc6f-d957ac0625dc	customer	This is an automated test message generated by the Admin Email Verification Tool to confirm inbound processing and routing.	\N	2026-08-05 12:09:21.986448	\N	<p>This is an <strong>automated test message</strong> generated by the <em>Admin Email Verification Tool</em>.</p>
3f5b8319-b5a5-448c-a292-7d2473e9b354	7903d2cf-33ea-49fd-855f-749b0ee82e6b	0973322f-a661-40b3-bc6f-d957ac0625dc	customer	This is an automated test message generated by the Admin Email Verification Tool to confirm inbound processing and routing.	\N	2026-08-05 12:10:22.522752	\N	<p>This is an <strong>automated test message</strong> generated by the <em>Admin Email Verification Tool</em>.</p>
a2c1f26e-d134-4634-aa92-0c59fa30f3a3	c88e8bad-58d2-445c-bdcd-376b733a5d4e	0973322f-a661-40b3-bc6f-d957ac0625dc	customer	This is an automated test message generated by the Admin Email Verification Tool to confirm inbound processing and routing.	\N	2026-08-05 12:10:43.978164	\N	<p>This is an <strong>automated test message</strong> generated by the <em>Admin Email Verification Tool</em>.</p>
f92d788b-e956-43b3-b26a-cfd421eaad5c	48231bbd-7ed9-4589-a228-0a9dc6032818	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Hi team, I would like to request an updated invoice copy.	\N	2026-08-05 12:16:31.834182	\N	\N
b2aec773-cfff-427b-ad15-be49e41a2c05	48231bbd-7ed9-4589-a228-0a9dc6032818	\N	ai	Hello! I am your AI Assistant. How can I help you today?	\N	2026-08-05 12:16:31.834459	\N	\N
b3e0506e-4f6a-4694-9a88-f9bc6444446b	3c16bc6f-db9b-471f-aeff-fb266d3c905b	c64e3806-b382-4689-9f1a-94114205ce5f	customer	Hi team, I would like to request an updated invoice copy.	\N	2026-08-05 12:17:02.053546	\N	\N
9e040486-d926-4695-886b-8003e950ea8d	3c16bc6f-db9b-471f-aeff-fb266d3c905b	\N	ai	Hello! I am your AI Assistant. How can I help you today?	\N	2026-08-05 12:17:02.053902	\N	\N
ab24e69f-dedd-4aa1-a3fe-579edcdb3ac0	be326382-a999-41cd-abec-78e7cbe40b4a	c64e3806-b382-4689-9f1a-94114205ce5f	customer	Hi team, I would like to request an updated invoice copy.	\N	2026-08-05 12:21:54.499345	\N	\N
d98b4f29-cc5a-4291-8422-29d780b075e1	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Hello Admin User! Thank you for reaching out to SupportHub Email Support regarding 'Inquiry about billing details'. We have received your inquiry (Ref: TCK-70849). Our support team will review your request and get back to you shortly.	\N	2026-08-05 12:21:54.499598	\N	\N
4e78734f-44a6-4d19-b18b-fceb904f8bcf	be326382-a999-41cd-abec-78e7cbe40b4a	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Here is additional context regarding my invoice request.	\N	2026-08-05 12:23:49.221695	msg-reply-12345@mail.gmail.com	<p>Here is <strong>additional context</strong> regarding my invoice request.</p>
f88c4542-71da-487d-be67-070032793aab	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Hi there! Thanks for providing the extra details. I've gone ahead and added that to your ticket (TCK-70849). Our team is on it and will send over your updated invoice shortly!	\N	2026-08-05 12:23:50.141785	\N	\N
5f17fd02-1443-49ca-a3a1-856bbda88d92	be326382-a999-41cd-abec-78e7cbe40b4a	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Actually I still need help with the invoice formatting.	\N	2026-08-05 13:39:51.509085	msg-reopen-999@mail.gmail.com	\N
00c1589e-dd87-43a2-b293-eda6a995fbba	f3ba1e50-7e93-4680-aef0-17bab9230f05	\N	ai	Your email inquiry [TCK-18834] has been marked as resolved.	\N	2026-08-05 13:40:06.067258	\N	<div>Resolution Notice [TCK-18834]</div>
d66e344a-8a70-45f0-b1eb-26946637a539	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	No problem at all! I've added your note about the invoice formatting to your ticket (TCK-70849). Our team will make sure that's sorted out for you when they send over the updated invoice shortly!	\N	2026-08-05 13:40:13.939635	\N	\N
8e148ab6-2034-4294-b3b0-54c5b9b2c8c4	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Your email inquiry [TCK-70849] has been marked as resolved. If your issue is not fully resolved, simply reply to this email to automatically reopen your ticket.	\N	2026-08-05 13:40:48.731642	\N	\n        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">\n          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">\n             <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>\n             <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [TCK-70849]</strong>\n          </div>\n          <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your email support inquiry <strong>"Inquiry about billing details"</strong> has been resolved. How would you rate your support experience today?</p>\n          <div style="display: flex; gap: 8px; flex-wrap: wrap;">\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>\n          </div>\n          <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this email thread to automatically reopen your ticket.</p>\n        </div>\n        
474778fc-6562-4429-b767-4389e6472244	be326382-a999-41cd-abec-78e7cbe40b4a	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Actually I still need help with the invoice formatting.	\N	2026-08-05 13:40:48.792114	msg-reopen-1001@mail.gmail.com	\N
52134d4e-95bc-4224-ad07-a2a530d6cdab	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Your email inquiry [TCK-70849] has been marked as resolved. If your issue is not fully resolved, simply reply to this email to automatically reopen your ticket.	\N	2026-08-05 13:42:13.232482	\N	\n        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">\n          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">\n             <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>\n             <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [TCK-70849]</strong>\n          </div>\n          <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your email support inquiry <strong>"Inquiry about billing details"</strong> has been resolved. How would you rate your support experience today?</p>\n          <div style="display: flex; gap: 8px; flex-wrap: wrap;">\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>\n          </div>\n          <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this email thread to automatically reopen your ticket.</p>\n        </div>\n        
4f13779c-70a7-478c-bcca-13abe21a0119	be326382-a999-41cd-abec-78e7cbe40b4a	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Actually I still need help with the invoice formatting.	\N	2026-08-05 13:42:13.287428	msg-reopen-1004@mail.gmail.com	\N
417966b7-b9cc-49a4-8348-75ebcdc72985	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	No problem! I've automatically reopened your ticket (TCK-70849) and added your note about the invoice formatting. Our team will take a look and get back to you shortly!	\N	2026-08-05 13:42:26.079593	\N	\N
4aad2863-aa97-4c7b-b039-85e5498b910c	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Hi there! Since your previous ticket (TCK-70849) was closed, replying here has automatically reopened it for you. I've added your note about the invoice formatting to the ticket, and our team will get back to you shortly to help sort that out!	\N	2026-08-05 13:44:14.667981	\N	\N
1c94c6f6-b9db-49a5-92fa-d2e8960a2f6a	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Your email inquiry [TCK-70849] has been marked as resolved. If your issue is not fully resolved, simply reply to this email to automatically reopen your ticket.	\N	2026-08-05 13:42:20.395738	\N	\n        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">\n          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">\n             <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>\n             <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [TCK-70849]</strong>\n          </div>\n          <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your email support inquiry <strong>"Inquiry about billing details"</strong> has been resolved. How would you rate your support experience today?</p>\n          <div style="display: flex; gap: 8px; flex-wrap: wrap;">\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>\n          </div>\n          <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this email thread to automatically reopen your ticket.</p>\n        </div>\n        
2f944ceb-09c6-4d6f-917a-4e86e3ed6172	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Your email inquiry [TCK-70849] has been marked as resolved. If your issue is not fully resolved, simply reply to this email to automatically reopen your ticket.	\N	2026-08-05 13:42:37.091559	\N	\n        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">\n          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">\n             <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>\n             <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [TCK-70849]</strong>\n          </div>\n          <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your email support inquiry <strong>"Inquiry about billing details"</strong> has been resolved. How would you rate your support experience today?</p>\n          <div style="display: flex; gap: 8px; flex-wrap: wrap;">\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>\n          </div>\n          <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this email thread to automatically reopen your ticket.</p>\n        </div>\n        
be8a6992-da4d-4924-8ee9-f316cb318b16	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Your email inquiry [TCK-70849] has been marked as resolved. If your issue is not fully resolved, simply reply to this email to automatically reopen your ticket.	\N	2026-08-05 13:43:03.554017	\N	\n        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">\n          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">\n             <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>\n             <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [TCK-70849]</strong>\n          </div>\n          <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your email support inquiry <strong>"Inquiry about billing details"</strong> has been resolved. How would you rate your support experience today?</p>\n          <div style="display: flex; gap: 8px; flex-wrap: wrap;">\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>\n          </div>\n          <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this email thread to automatically reopen your ticket.</p>\n        </div>\n        
36f98efe-b1d3-417f-a9c5-f29e4c827150	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Your email inquiry [TCK-70849] has been marked as resolved. If your issue is not fully resolved, simply reply to this email to automatically reopen your ticket.	\N	2026-08-05 13:43:29.329027	\N	\n        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">\n          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">\n             <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>\n             <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [TCK-70849]</strong>\n          </div>\n          <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your email support inquiry <strong>"Inquiry about billing details"</strong> has been resolved. How would you rate your support experience today?</p>\n          <div style="display: flex; gap: 8px; flex-wrap: wrap;">\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>\n          </div>\n          <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this email thread to automatically reopen your ticket.</p>\n        </div>\n        
b4785424-238a-45ba-b522-6e3ed7de3ba3	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Your email inquiry [TCK-70849] has been marked as resolved. If your issue is not fully resolved, simply reply to this email to automatically reopen your ticket.	\N	2026-08-05 13:43:50.727676	\N	\n        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">\n          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">\n             <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>\n             <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [TCK-70849]</strong>\n          </div>\n          <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your email support inquiry <strong>"Inquiry about billing details"</strong> has been resolved. How would you rate your support experience today?</p>\n          <div style="display: flex; gap: 8px; flex-wrap: wrap;">\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>\n          </div>\n          <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this email thread to automatically reopen your ticket.</p>\n        </div>\n        
63379e2e-c728-49b7-b59b-94e4c59b6204	be326382-a999-41cd-abec-78e7cbe40b4a	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Actually I still need help with the invoice formatting.	\N	2026-08-05 13:43:50.751004	msg-reopen-1005@mail.gmail.com	\N
70d2f742-b19f-4c3f-a4f1-37bb6f9622bc	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	No problem! I've automatically reopened your ticket (TCK-70849) once again and added your note about the invoice formatting. Our team will make sure this gets sorted for you!	\N	2026-08-05 13:44:38.228615	\N	\N
2f430902-b6d9-48dc-83cf-acaecced5784	be326382-a999-41cd-abec-78e7cbe40b4a	\N	ai	Your email inquiry [TCK-70849] has been marked as resolved. If your issue is not fully resolved, simply reply to this email to automatically reopen your ticket.	\N	2026-08-05 13:44:41.534713	\N	\n        <div style="font-family: 'Plus Jakarta Sans', sans-serif; background: #F9FAFB; border: 1px solid #E5E7F3; border-radius: 16px; padding: 20px; margin-top: 10px;">\n          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">\n             <span style="background: #10B981; color: white; padding: 2px 8px; border-radius: 6px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Ticket Resolved</span>\n             <strong style="color: #1C1B2E; font-size: 14px;">Resolution Notice for [TCK-70849]</strong>\n          </div>\n          <p style="color: #6C7089; font-size: 13px; margin: 4px 0 16px 0;">Your email support inquiry <strong>"Inquiry about billing details"</strong> has been resolved. How would you rate your support experience today?</p>\n          <div style="display: flex; gap: 8px; flex-wrap: wrap;">\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=5" target="_blank" style="background: #10B981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐⭐ 5 - Excellent</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=4" target="_blank" style="background: #3B82F6; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐⭐ 4 - Good</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=3" target="_blank" style="background: #F59E0B; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐⭐⭐ 3 - Neutral</a>\n             <a href="http://localhost:8001/api/v1/tickets/be326382-a999-41cd-abec-78e7cbe40b4a/rate-email?rating=1" target="_blank" style="background: #EF4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 12px; display: inline-block;">⭐ 1 - Unsatisfied</a>\n          </div>\n          <p style="color: #9598B0; font-size: 11px; margin-top: 14px; margin-bottom: 0;">Need further assistance? Simply reply to this email thread to automatically reopen your ticket.</p>\n        </div>\n        
016db44e-55be-4637-b620-075c0a6b669b	8b143420-d8df-4fc9-a1fa-c1faba787dc7	\N	ai	I'd be happy to help you with your invoice! \n\nAccording to our billing information, your monthly subscription invoice contains a breakdown of charges including your **Base Plan** fee, **Additional Seats** (if you've added agents beyond your plan's allowance), and any **Overages** (such as extra AI chatbot tokens or SMS messages).\n\nInvoices are generated on the 1st of every month, and you can download PDF copies of past invoices anytime by going to **Dashboard > Settings > Billing > Invoice History**.\n\nAre you looking for help understanding a specific charge on your invoice, or is there something else I can assist you with today?	\N	2026-08-05 13:55:29.670039	\N	\N
5acbabd1-24e5-4676-8b04-47a1a264d22d	4f9eee37-9f3a-4f2c-b0f7-8f91660fc888	\N	ai	Hello Customer User! How can I assist you with your support request today?	\N	2026-08-05 14:12:50.61197	\N	\N
80ca93fa-e125-4ce9-8011-0f43a5b03a34	4f9eee37-9f3a-4f2c-b0f7-8f91660fc888	c64e3806-b382-4689-9f1a-94114205ce5f	agent	Test message for customer live chat verification.	\N	2026-08-05 14:26:43.420428	\N	\N
7901edd9-a9be-4a8f-964a-6c5eb831daad	4f9eee37-9f3a-4f2c-b0f7-8f91660fc888	c64e3806-b382-4689-9f1a-94114205ce5f	agent	📎 [Attachment: _.jpeg](http://localhost:8001/static/uploads/ec5cb1073fcb42d4a6fe2e0c3dd84783__.jpeg)	\N	2026-08-05 14:27:17.344738	\N	\N
37d287f3-9658-4621-99dd-973d0c12d756	8b143420-d8df-4fc9-a1fa-c1faba787dc7	c64e3806-b382-4689-9f1a-94114205ce5f	agent	📎 [Attachment: _.jpeg](http://localhost:8001/static/uploads/0273593d331545f5ad900dfa5568ecb9__.jpeg)	\N	2026-08-05 14:28:00.34035	\N	\N
c2d6b0b6-b3b7-4a7e-bfb6-739c2fb9a5a7	48231bbd-7ed9-4589-a228-0a9dc6032818	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	📎 [Attachment: _.jpeg](http://localhost:8001/static/uploads/0ed664e2762245d3927a224a1eae450b__.jpeg)	\N	2026-08-05 14:29:13.787987	\N	\N
b706d567-8b2a-4c5e-b9c6-2d55d67a5ce6	48231bbd-7ed9-4589-a228-0a9dc6032818	\N	ai	I don't have enough information to answer that, but I will connect you with a human agent shortly.	\N	2026-08-05 14:31:54.216373	\N	\N
b2050c45-7f69-4922-bce7-543f8497375d	4f9eee37-9f3a-4f2c-b0f7-8f91660fc888	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-08-05 15:00:12.772026	\N	\N
b06427e0-02d6-4c3d-a0f9-eef1873666cb	4f9eee37-9f3a-4f2c-b0f7-8f91660fc888	\N	ai	I'm glad to hear that fixed your issue! I've marked this ticket as resolved. If you need help with anything else in the future, don't hesitate to reach out. Have a great day!	\N	2026-08-05 15:00:14.908886	\N	\N
fc3c28a1-85b2-42d5-b6a9-7c0cfef112af	8b143420-d8df-4fc9-a1fa-c1faba787dc7	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-08-05 15:00:30.587503	\N	\N
97b31580-40e7-4564-a350-bf0defac0c75	8b143420-d8df-4fc9-a1fa-c1faba787dc7	\N	ai	I'm glad to hear that fixed your issue! I've gone ahead and marked your ticket as resolved. If you need any more help in the future, feel free to reach out. Have a great day!	\N	2026-08-05 15:00:32.610515	\N	\N
9829f22a-116b-40f4-a786-55ef94cd2e7d	36f0f5f3-c7b8-4465-986c-2b5eb7a98df4	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-08-05 15:00:58.027102	\N	\N
1abdfa2b-ab6a-410a-9afe-1abe2bf714ad	36f0f5f3-c7b8-4465-986c-2b5eb7a98df4	\N	ai	I'm glad to hear that! I have marked this ticket as resolved. Have a great day!	\N	2026-08-05 15:00:59.942506	\N	\N
95d0941a-bae6-45c0-836c-43e07434cd7d	daba0e8c-c1f1-49d8-8854-562752613ea8	4a47565a-2ec1-404a-8f05-07490e1d9384	customer	Thanks, that fixed it!	\N	2026-08-05 15:01:20.068899	\N	\N
0e7de762-87d1-4962-9ac3-56f690c4c0b4	daba0e8c-c1f1-49d8-8854-562752613ea8	\N	ai	I'm glad to hear that! If you have any more questions in the future, feel free to reach out. Have a great day!	\N	2026-08-05 15:01:22.186149	\N	\N
\.


--
-- PostgreSQL database dump complete
--

\unrestrict KUeC4Dw4VRJOeWaAQJ2OWEhB879NnjQiUOh2q2NhzxXebPSXpps6oqUwjdhHLND


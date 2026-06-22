--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

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

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: alert_level; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.alert_level AS ENUM (
    'INFO',
    'WARNING',
    'CRITICAL',
    'FATAL'
);


ALTER TYPE public.alert_level OWNER TO postgres;

--
-- Name: payment_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.payment_status AS ENUM (
    'PENDING',
    'SUCCESS',
    'FAILED',
    'REFUNDED'
);


ALTER TYPE public.payment_status OWNER TO postgres;

--
-- Name: role_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.role_type AS ENUM (
    'SUPER_ADMIN',
    'ORG_ADMIN',
    'DATA_SCIENTIST',
    'ANALYST',
    'VIEWER'
);


ALTER TYPE public.role_type OWNER TO postgres;

--
-- Name: sim_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.sim_status AS ENUM (
    'PENDING',
    'RUNNING',
    'PAUSED',
    'COMPLETED',
    'FAILED',
    'ROLLBACK'
);


ALTER TYPE public.sim_status OWNER TO postgres;

--
-- Name: sub_tier; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.sub_tier AS ENUM (
    'FREE',
    'PRO',
    'ENTERPRISE',
    'GOVERNMENT'
);


ALTER TYPE public.sub_tier OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ai_models; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_models (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    org_id uuid,
    name character varying(255) NOT NULL,
    architecture character varying(100) NOT NULL,
    is_active boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.ai_models OWNER TO postgres;

--
-- Name: api_keys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.api_keys (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    key_hash character varying(255) NOT NULL,
    key_prefix character varying(10) NOT NULL,
    name character varying(100),
    last_used_at timestamp with time zone,
    expires_at timestamp with time zone,
    is_revoked boolean DEFAULT false
);


ALTER TABLE public.api_keys OWNER TO postgres;

--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_logs (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    org_id uuid,
    action character varying(255) NOT NULL,
    ip_address inet,
    user_agent text,
    resource_id uuid,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.audit_logs OWNER TO postgres;

--
-- Name: climate_time_series; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.climate_time_series (
    "time" timestamp with time zone NOT NULL,
    iso_code character varying(3) NOT NULL,
    avg_temp_celsius numeric(5,2),
    co2_ppm numeric(6,2),
    sea_level_rise_mm numeric(6,2)
);


ALTER TABLE public.climate_time_series OWNER TO postgres;

--
-- Name: collab_cursors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.collab_cursors (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    session_id uuid,
    user_id uuid,
    pos_x numeric(10,4),
    pos_y numeric(10,4),
    last_updated timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.collab_cursors OWNER TO postgres;

--
-- Name: collab_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.collab_sessions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    request_id uuid,
    started_by uuid,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.collab_sessions OWNER TO postgres;

--
-- Name: compute_usage_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.compute_usage_logs (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    org_id uuid,
    request_id uuid,
    compute_minutes numeric(10,2) NOT NULL,
    gpu_type character varying(50),
    cost_incurred numeric(10,2) NOT NULL,
    logged_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.compute_usage_logs OWNER TO postgres;

--
-- Name: countries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.countries (
    iso_code character varying(3) NOT NULL,
    name character varying(255) NOT NULL,
    region character varying(100)
);


ALTER TABLE public.countries OWNER TO postgres;

--
-- Name: data_sources; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.data_sources (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(100) NOT NULL,
    api_endpoint character varying(500),
    auth_config jsonb,
    refresh_rate_seconds integer DEFAULT 3600
);


ALTER TABLE public.data_sources OWNER TO postgres;

--
-- Name: economic_time_series; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.economic_time_series (
    "time" timestamp with time zone NOT NULL,
    iso_code character varying(3) NOT NULL,
    gdp_usd numeric(20,2),
    inflation_rate numeric(5,2),
    interest_rate numeric(5,2),
    debt_to_gdp numeric(6,2)
);


ALTER TABLE public.economic_time_series OWNER TO postgres;

--
-- Name: geopolitical_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.geopolitical_events (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    iso_code character varying(3),
    event_type character varying(100),
    severity integer,
    description text,
    event_date date NOT NULL,
    CONSTRAINT geopolitical_events_severity_check CHECK (((severity >= 1) AND (severity <= 10)))
);


ALTER TABLE public.geopolitical_events OWNER TO postgres;

--
-- Name: gis_topology_layers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gis_topology_layers (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(255) NOT NULL,
    layer_type character varying(50),
    s3_geojson_path character varying(500) NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.gis_topology_layers OWNER TO postgres;

--
-- Name: invoice_ledgers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoice_ledgers (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    org_id uuid,
    stripe_invoice_id character varying(255),
    amount_due numeric(10,2) NOT NULL,
    currency character varying(3) DEFAULT 'USD'::character varying,
    status public.payment_status DEFAULT 'PENDING'::public.payment_status,
    billing_period_start timestamp with time zone,
    billing_period_end timestamp with time zone,
    issued_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.invoice_ledgers OWNER TO postgres;

--
-- Name: market_tick_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.market_tick_data (
    "time" timestamp with time zone NOT NULL,
    ticker_id uuid NOT NULL,
    price_open numeric(15,4),
    price_close numeric(15,4),
    price_high numeric(15,4),
    price_low numeric(15,4),
    volume bigint,
    volatility_index numeric(10,4)
);


ALTER TABLE public.market_tick_data OWNER TO postgres;

--
-- Name: market_tickers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.market_tickers (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    symbol character varying(20) NOT NULL,
    company_name character varying(255),
    sector character varying(100),
    exchange character varying(50)
);


ALTER TABLE public.market_tickers OWNER TO postgres;

--
-- Name: model_deployments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.model_deployments (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    version_id uuid,
    environment character varying(50) NOT NULL,
    deployed_by uuid,
    deployed_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.model_deployments OWNER TO postgres;

--
-- Name: model_versions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.model_versions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    model_id uuid,
    version_tag character varying(50) NOT NULL,
    dataset_id uuid,
    s3_weights_path character varying(500) NOT NULL,
    accuracy_score numeric(5,4),
    loss_metrics jsonb,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.model_versions OWNER TO postgres;

--
-- Name: news_sentiment_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news_sentiment_logs (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    source character varying(100),
    headline text NOT NULL,
    finbert_score numeric(5,4),
    impacted_tickers jsonb,
    published_at timestamp with time zone NOT NULL
);


ALTER TABLE public.news_sentiment_logs OWNER TO postgres;

--
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    type character varying(50) NOT NULL,
    title character varying(255) NOT NULL,
    message text,
    is_read boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- Name: oauth_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oauth_tokens (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    provider character varying(50) NOT NULL,
    access_token text NOT NULL,
    refresh_token text,
    expires_at timestamp with time zone NOT NULL
);


ALTER TABLE public.oauth_tokens OWNER TO postgres;

--
-- Name: org_plugins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.org_plugins (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    org_id uuid,
    plugin_id uuid,
    is_enabled boolean DEFAULT true,
    installed_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.org_plugins OWNER TO postgres;

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organizations (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(255) NOT NULL,
    domain character varying(255),
    subscription_tier public.sub_tier DEFAULT 'FREE'::public.sub_tier,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.organizations OWNER TO postgres;

--
-- Name: payment_methods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_methods (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    org_id uuid,
    stripe_pm_id character varying(255) NOT NULL,
    card_last4 character varying(4) NOT NULL,
    card_brand character varying(50),
    is_default boolean DEFAULT false
);


ALTER TABLE public.payment_methods OWNER TO postgres;

--
-- Name: permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permissions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    role_id uuid,
    resource character varying(100) NOT NULL,
    action character varying(50) NOT NULL
);


ALTER TABLE public.permissions OWNER TO postgres;

--
-- Name: pipeline_runs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pipeline_runs (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    source_id uuid,
    status character varying(50) NOT NULL,
    records_ingested integer DEFAULT 0,
    error_log text,
    started_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    completed_at timestamp with time zone
);


ALTER TABLE public.pipeline_runs OWNER TO postgres;

--
-- Name: plugins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plugins (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    developer_id uuid,
    name character varying(255) NOT NULL,
    version character varying(50) NOT NULL,
    description text,
    s3_bundle_path character varying(500),
    is_approved boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.plugins OWNER TO postgres;

--
-- Name: predictions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.predictions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    result_id uuid,
    domain character varying(50) NOT NULL,
    metric character varying(100) NOT NULL,
    predicted_value numeric(15,4),
    confidence_interval jsonb
);


ALTER TABLE public.predictions OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name public.role_type NOT NULL,
    description text
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: scenarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scenarios (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    request_id uuid,
    parent_scenario_id uuid,
    name character varying(255),
    variables jsonb NOT NULL,
    probability_score numeric(5,4),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.scenarios OWNER TO postgres;

--
-- Name: simulation_checkpoints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.simulation_checkpoints (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    request_id uuid,
    tick_number bigint NOT NULL,
    state_hash character varying(256) NOT NULL,
    s3_state_path character varying(500) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.simulation_checkpoints OWNER TO postgres;

--
-- Name: simulation_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.simulation_requests (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    org_id uuid,
    name character varying(255) NOT NULL,
    target_year integer NOT NULL,
    status public.sim_status DEFAULT 'PENDING'::public.sim_status,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.simulation_requests OWNER TO postgres;

--
-- Name: simulation_results; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.simulation_results (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    request_id uuid,
    scenario_id uuid,
    raw_payload jsonb NOT NULL,
    computed_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.simulation_results OWNER TO postgres;

--
-- Name: subscriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscriptions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    org_id uuid,
    stripe_sub_id character varying(255) NOT NULL,
    plan_type public.sub_tier NOT NULL,
    status character varying(50) NOT NULL,
    current_period_end timestamp with time zone NOT NULL
);


ALTER TABLE public.subscriptions OWNER TO postgres;

--
-- Name: system_alerts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.system_alerts (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    level public.alert_level NOT NULL,
    service_name character varying(100) NOT NULL,
    message text NOT NULL,
    is_resolved boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.system_alerts OWNER TO postgres;

--
-- Name: training_datasets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.training_datasets (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    source_id uuid,
    name character varying(255) NOT NULL,
    s3_path character varying(500) NOT NULL,
    num_records bigint,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.training_datasets OWNER TO postgres;

--
-- Name: user_mfa_devices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_mfa_devices (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    device_name character varying(100),
    secret_key character varying(255) NOT NULL,
    is_verified boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_mfa_devices OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    org_id uuid,
    role_id uuid,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    is_active boolean DEFAULT true,
    last_login timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: webhook_delivery_histories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.webhook_delivery_histories (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    endpoint_id uuid,
    event_type character varying(100) NOT NULL,
    payload jsonb,
    response_status integer,
    response_body text,
    delivered_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.webhook_delivery_histories OWNER TO postgres;

--
-- Name: webhook_endpoints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.webhook_endpoints (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    org_id uuid,
    target_url character varying(500) NOT NULL,
    secret_key character varying(255) NOT NULL,
    events jsonb NOT NULL,
    is_active boolean DEFAULT true
);


ALTER TABLE public.webhook_endpoints OWNER TO postgres;

--
-- Data for Name: ai_models; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_models (id, org_id, name, architecture, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: api_keys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.api_keys (id, user_id, key_hash, key_prefix, name, last_used_at, expires_at, is_revoked) FROM stdin;
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_logs (id, user_id, org_id, action, ip_address, user_agent, resource_id, "timestamp") FROM stdin;
\.


--
-- Data for Name: climate_time_series; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.climate_time_series ("time", iso_code, avg_temp_celsius, co2_ppm, sea_level_rise_mm) FROM stdin;
\.


--
-- Data for Name: collab_cursors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.collab_cursors (id, session_id, user_id, pos_x, pos_y, last_updated) FROM stdin;
\.


--
-- Data for Name: collab_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.collab_sessions (id, request_id, started_by, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: compute_usage_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.compute_usage_logs (id, org_id, request_id, compute_minutes, gpu_type, cost_incurred, logged_at) FROM stdin;
\.


--
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.countries (iso_code, name, region) FROM stdin;
\.


--
-- Data for Name: data_sources; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.data_sources (id, name, api_endpoint, auth_config, refresh_rate_seconds) FROM stdin;
\.


--
-- Data for Name: economic_time_series; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.economic_time_series ("time", iso_code, gdp_usd, inflation_rate, interest_rate, debt_to_gdp) FROM stdin;
\.


--
-- Data for Name: geopolitical_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.geopolitical_events (id, iso_code, event_type, severity, description, event_date) FROM stdin;
\.


--
-- Data for Name: gis_topology_layers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gis_topology_layers (id, name, layer_type, s3_geojson_path, updated_at) FROM stdin;
\.


--
-- Data for Name: invoice_ledgers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoice_ledgers (id, org_id, stripe_invoice_id, amount_due, currency, status, billing_period_start, billing_period_end, issued_at) FROM stdin;
\.


--
-- Data for Name: market_tick_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.market_tick_data ("time", ticker_id, price_open, price_close, price_high, price_low, volume, volatility_index) FROM stdin;
\.


--
-- Data for Name: market_tickers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.market_tickers (id, symbol, company_name, sector, exchange) FROM stdin;
\.


--
-- Data for Name: model_deployments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.model_deployments (id, version_id, environment, deployed_by, deployed_at) FROM stdin;
\.


--
-- Data for Name: model_versions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.model_versions (id, model_id, version_tag, dataset_id, s3_weights_path, accuracy_score, loss_metrics, created_at) FROM stdin;
\.


--
-- Data for Name: news_sentiment_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news_sentiment_logs (id, source, headline, finbert_score, impacted_tickers, published_at) FROM stdin;
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, user_id, type, title, message, is_read, created_at) FROM stdin;
\.


--
-- Data for Name: oauth_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.oauth_tokens (id, user_id, provider, access_token, refresh_token, expires_at) FROM stdin;
\.


--
-- Data for Name: org_plugins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.org_plugins (id, org_id, plugin_id, is_enabled, installed_at) FROM stdin;
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organizations (id, name, domain, subscription_tier, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: payment_methods; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payment_methods (id, org_id, stripe_pm_id, card_last4, card_brand, is_default) FROM stdin;
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permissions (id, role_id, resource, action) FROM stdin;
\.


--
-- Data for Name: pipeline_runs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pipeline_runs (id, source_id, status, records_ingested, error_log, started_at, completed_at) FROM stdin;
\.


--
-- Data for Name: plugins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plugins (id, developer_id, name, version, description, s3_bundle_path, is_approved, created_at) FROM stdin;
\.


--
-- Data for Name: predictions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.predictions (id, result_id, domain, metric, predicted_value, confidence_interval) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, name, description) FROM stdin;
\.


--
-- Data for Name: scenarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.scenarios (id, request_id, parent_scenario_id, name, variables, probability_score, created_at) FROM stdin;
\.


--
-- Data for Name: simulation_checkpoints; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.simulation_checkpoints (id, request_id, tick_number, state_hash, s3_state_path, created_at) FROM stdin;
\.


--
-- Data for Name: simulation_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.simulation_requests (id, user_id, org_id, name, target_year, status, created_at) FROM stdin;
\.


--
-- Data for Name: simulation_results; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.simulation_results (id, request_id, scenario_id, raw_payload, computed_at) FROM stdin;
\.


--
-- Data for Name: subscriptions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscriptions (id, org_id, stripe_sub_id, plan_type, status, current_period_end) FROM stdin;
\.


--
-- Data for Name: system_alerts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.system_alerts (id, level, service_name, message, is_resolved, created_at) FROM stdin;
\.


--
-- Data for Name: training_datasets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.training_datasets (id, source_id, name, s3_path, num_records, created_at) FROM stdin;
\.


--
-- Data for Name: user_mfa_devices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_mfa_devices (id, user_id, device_name, secret_key, is_verified, created_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, org_id, role_id, email, password_hash, is_active, last_login, created_at) FROM stdin;
\.


--
-- Data for Name: webhook_delivery_histories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.webhook_delivery_histories (id, endpoint_id, event_type, payload, response_status, response_body, delivered_at) FROM stdin;
\.


--
-- Data for Name: webhook_endpoints; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.webhook_endpoints (id, org_id, target_url, secret_key, events, is_active) FROM stdin;
\.


--
-- Name: ai_models ai_models_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_models
    ADD CONSTRAINT ai_models_pkey PRIMARY KEY (id);


--
-- Name: api_keys api_keys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: climate_time_series climate_time_series_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.climate_time_series
    ADD CONSTRAINT climate_time_series_pkey PRIMARY KEY ("time", iso_code);


--
-- Name: collab_cursors collab_cursors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collab_cursors
    ADD CONSTRAINT collab_cursors_pkey PRIMARY KEY (id);


--
-- Name: collab_sessions collab_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collab_sessions
    ADD CONSTRAINT collab_sessions_pkey PRIMARY KEY (id);


--
-- Name: compute_usage_logs compute_usage_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compute_usage_logs
    ADD CONSTRAINT compute_usage_logs_pkey PRIMARY KEY (id);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (iso_code);


--
-- Name: data_sources data_sources_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.data_sources
    ADD CONSTRAINT data_sources_pkey PRIMARY KEY (id);


--
-- Name: economic_time_series economic_time_series_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.economic_time_series
    ADD CONSTRAINT economic_time_series_pkey PRIMARY KEY ("time", iso_code);


--
-- Name: geopolitical_events geopolitical_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.geopolitical_events
    ADD CONSTRAINT geopolitical_events_pkey PRIMARY KEY (id);


--
-- Name: gis_topology_layers gis_topology_layers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gis_topology_layers
    ADD CONSTRAINT gis_topology_layers_pkey PRIMARY KEY (id);


--
-- Name: invoice_ledgers invoice_ledgers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice_ledgers
    ADD CONSTRAINT invoice_ledgers_pkey PRIMARY KEY (id);


--
-- Name: invoice_ledgers invoice_ledgers_stripe_invoice_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice_ledgers
    ADD CONSTRAINT invoice_ledgers_stripe_invoice_id_key UNIQUE (stripe_invoice_id);


--
-- Name: market_tick_data market_tick_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.market_tick_data
    ADD CONSTRAINT market_tick_data_pkey PRIMARY KEY ("time", ticker_id);


--
-- Name: market_tickers market_tickers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.market_tickers
    ADD CONSTRAINT market_tickers_pkey PRIMARY KEY (id);


--
-- Name: market_tickers market_tickers_symbol_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.market_tickers
    ADD CONSTRAINT market_tickers_symbol_key UNIQUE (symbol);


--
-- Name: model_deployments model_deployments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_deployments
    ADD CONSTRAINT model_deployments_pkey PRIMARY KEY (id);


--
-- Name: model_versions model_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_versions
    ADD CONSTRAINT model_versions_pkey PRIMARY KEY (id);


--
-- Name: news_sentiment_logs news_sentiment_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_sentiment_logs
    ADD CONSTRAINT news_sentiment_logs_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: oauth_tokens oauth_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth_tokens
    ADD CONSTRAINT oauth_tokens_pkey PRIMARY KEY (id);


--
-- Name: org_plugins org_plugins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.org_plugins
    ADD CONSTRAINT org_plugins_pkey PRIMARY KEY (id);


--
-- Name: organizations organizations_domain_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_domain_key UNIQUE (domain);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);


--
-- Name: payment_methods payment_methods_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_pkey PRIMARY KEY (id);


--
-- Name: payment_methods payment_methods_stripe_pm_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_stripe_pm_id_key UNIQUE (stripe_pm_id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_role_id_resource_action_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_role_id_resource_action_key UNIQUE (role_id, resource, action);


--
-- Name: pipeline_runs pipeline_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pipeline_runs
    ADD CONSTRAINT pipeline_runs_pkey PRIMARY KEY (id);


--
-- Name: plugins plugins_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plugins
    ADD CONSTRAINT plugins_name_key UNIQUE (name);


--
-- Name: plugins plugins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plugins
    ADD CONSTRAINT plugins_pkey PRIMARY KEY (id);


--
-- Name: predictions predictions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.predictions
    ADD CONSTRAINT predictions_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: scenarios scenarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scenarios
    ADD CONSTRAINT scenarios_pkey PRIMARY KEY (id);


--
-- Name: simulation_checkpoints simulation_checkpoints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation_checkpoints
    ADD CONSTRAINT simulation_checkpoints_pkey PRIMARY KEY (id);


--
-- Name: simulation_requests simulation_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation_requests
    ADD CONSTRAINT simulation_requests_pkey PRIMARY KEY (id);


--
-- Name: simulation_results simulation_results_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation_results
    ADD CONSTRAINT simulation_results_pkey PRIMARY KEY (id);


--
-- Name: subscriptions subscriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_pkey PRIMARY KEY (id);


--
-- Name: subscriptions subscriptions_stripe_sub_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_stripe_sub_id_key UNIQUE (stripe_sub_id);


--
-- Name: system_alerts system_alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.system_alerts
    ADD CONSTRAINT system_alerts_pkey PRIMARY KEY (id);


--
-- Name: training_datasets training_datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.training_datasets
    ADD CONSTRAINT training_datasets_pkey PRIMARY KEY (id);


--
-- Name: user_mfa_devices user_mfa_devices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_mfa_devices
    ADD CONSTRAINT user_mfa_devices_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: webhook_delivery_histories webhook_delivery_histories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.webhook_delivery_histories
    ADD CONSTRAINT webhook_delivery_histories_pkey PRIMARY KEY (id);


--
-- Name: webhook_endpoints webhook_endpoints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.webhook_endpoints
    ADD CONSTRAINT webhook_endpoints_pkey PRIMARY KEY (id);


--
-- Name: idx_audit_logs_org; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_audit_logs_org ON public.audit_logs USING btree (org_id, "timestamp" DESC);


--
-- Name: idx_climate_ts_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_climate_ts_time ON public.climate_time_series USING btree ("time" DESC);


--
-- Name: idx_compute_usage_org; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_compute_usage_org ON public.compute_usage_logs USING btree (org_id, logged_at DESC);


--
-- Name: idx_eco_ts_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_eco_ts_time ON public.economic_time_series USING btree ("time" DESC);


--
-- Name: idx_market_tick_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_market_tick_time ON public.market_tick_data USING btree ("time" DESC);


--
-- Name: idx_scenarios_req; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_scenarios_req ON public.scenarios USING btree (request_id);


--
-- Name: idx_sim_req_org; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sim_req_org ON public.simulation_requests USING btree (org_id);


--
-- Name: idx_users_org; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_org ON public.users USING btree (org_id);


--
-- Name: ai_models ai_models_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_models
    ADD CONSTRAINT ai_models_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id);


--
-- Name: api_keys api_keys_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_keys
    ADD CONSTRAINT api_keys_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: audit_logs audit_logs_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id);


--
-- Name: audit_logs audit_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: climate_time_series climate_time_series_iso_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.climate_time_series
    ADD CONSTRAINT climate_time_series_iso_code_fkey FOREIGN KEY (iso_code) REFERENCES public.countries(iso_code);


--
-- Name: collab_cursors collab_cursors_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collab_cursors
    ADD CONSTRAINT collab_cursors_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.collab_sessions(id) ON DELETE CASCADE;


--
-- Name: collab_cursors collab_cursors_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collab_cursors
    ADD CONSTRAINT collab_cursors_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: collab_sessions collab_sessions_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collab_sessions
    ADD CONSTRAINT collab_sessions_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.simulation_requests(id) ON DELETE CASCADE;


--
-- Name: collab_sessions collab_sessions_started_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.collab_sessions
    ADD CONSTRAINT collab_sessions_started_by_fkey FOREIGN KEY (started_by) REFERENCES public.users(id);


--
-- Name: compute_usage_logs compute_usage_logs_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compute_usage_logs
    ADD CONSTRAINT compute_usage_logs_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id);


--
-- Name: compute_usage_logs compute_usage_logs_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compute_usage_logs
    ADD CONSTRAINT compute_usage_logs_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.simulation_requests(id);


--
-- Name: economic_time_series economic_time_series_iso_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.economic_time_series
    ADD CONSTRAINT economic_time_series_iso_code_fkey FOREIGN KEY (iso_code) REFERENCES public.countries(iso_code);


--
-- Name: geopolitical_events geopolitical_events_iso_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.geopolitical_events
    ADD CONSTRAINT geopolitical_events_iso_code_fkey FOREIGN KEY (iso_code) REFERENCES public.countries(iso_code);


--
-- Name: invoice_ledgers invoice_ledgers_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice_ledgers
    ADD CONSTRAINT invoice_ledgers_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id);


--
-- Name: market_tick_data market_tick_data_ticker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.market_tick_data
    ADD CONSTRAINT market_tick_data_ticker_id_fkey FOREIGN KEY (ticker_id) REFERENCES public.market_tickers(id);


--
-- Name: model_deployments model_deployments_deployed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_deployments
    ADD CONSTRAINT model_deployments_deployed_by_fkey FOREIGN KEY (deployed_by) REFERENCES public.users(id);


--
-- Name: model_deployments model_deployments_version_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_deployments
    ADD CONSTRAINT model_deployments_version_id_fkey FOREIGN KEY (version_id) REFERENCES public.model_versions(id);


--
-- Name: model_versions model_versions_dataset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_versions
    ADD CONSTRAINT model_versions_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.training_datasets(id);


--
-- Name: model_versions model_versions_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_versions
    ADD CONSTRAINT model_versions_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.ai_models(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: oauth_tokens oauth_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth_tokens
    ADD CONSTRAINT oauth_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: org_plugins org_plugins_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.org_plugins
    ADD CONSTRAINT org_plugins_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: org_plugins org_plugins_plugin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.org_plugins
    ADD CONSTRAINT org_plugins_plugin_id_fkey FOREIGN KEY (plugin_id) REFERENCES public.plugins(id);


--
-- Name: payment_methods payment_methods_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: permissions permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: pipeline_runs pipeline_runs_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pipeline_runs
    ADD CONSTRAINT pipeline_runs_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.data_sources(id);


--
-- Name: plugins plugins_developer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plugins
    ADD CONSTRAINT plugins_developer_id_fkey FOREIGN KEY (developer_id) REFERENCES public.users(id);


--
-- Name: predictions predictions_result_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.predictions
    ADD CONSTRAINT predictions_result_id_fkey FOREIGN KEY (result_id) REFERENCES public.simulation_results(id) ON DELETE CASCADE;


--
-- Name: scenarios scenarios_parent_scenario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scenarios
    ADD CONSTRAINT scenarios_parent_scenario_id_fkey FOREIGN KEY (parent_scenario_id) REFERENCES public.scenarios(id);


--
-- Name: scenarios scenarios_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scenarios
    ADD CONSTRAINT scenarios_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.simulation_requests(id) ON DELETE CASCADE;


--
-- Name: simulation_checkpoints simulation_checkpoints_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation_checkpoints
    ADD CONSTRAINT simulation_checkpoints_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.simulation_requests(id) ON DELETE CASCADE;


--
-- Name: simulation_requests simulation_requests_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation_requests
    ADD CONSTRAINT simulation_requests_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id);


--
-- Name: simulation_requests simulation_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation_requests
    ADD CONSTRAINT simulation_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: simulation_results simulation_results_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation_results
    ADD CONSTRAINT simulation_results_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.simulation_requests(id) ON DELETE CASCADE;


--
-- Name: simulation_results simulation_results_scenario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation_results
    ADD CONSTRAINT simulation_results_scenario_id_fkey FOREIGN KEY (scenario_id) REFERENCES public.scenarios(id);


--
-- Name: subscriptions subscriptions_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscriptions_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: training_datasets training_datasets_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.training_datasets
    ADD CONSTRAINT training_datasets_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.data_sources(id);


--
-- Name: user_mfa_devices user_mfa_devices_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_mfa_devices
    ADD CONSTRAINT user_mfa_devices_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: users users_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: webhook_delivery_histories webhook_delivery_histories_endpoint_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.webhook_delivery_histories
    ADD CONSTRAINT webhook_delivery_histories_endpoint_id_fkey FOREIGN KEY (endpoint_id) REFERENCES public.webhook_endpoints(id) ON DELETE CASCADE;


--
-- Name: webhook_endpoints webhook_endpoints_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.webhook_endpoints
    ADD CONSTRAINT webhook_endpoints_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


-- Phase 2 Database Evolution

-- Population Data
CREATE TABLE IF NOT EXISTS population_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    iso_code VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    total_population BIGINT,
    population_density NUMERIC(10, 2),
    urban_population_pct NUMERIC(5, 2),
    UNIQUE(time, iso_code)
);

-- Trade Data
CREATE TABLE IF NOT EXISTS trade_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    reporter_iso VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    partner_iso VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    export_value_usd NUMERIC(20, 2),
    import_value_usd NUMERIC(20, 2),
    commodity_code VARCHAR(50),
    UNIQUE(time, reporter_iso, partner_iso, commodity_code)
);

-- Energy Data
CREATE TABLE IF NOT EXISTS energy_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    iso_code VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    oil_production_bpd NUMERIC(15, 2),
    oil_consumption_bpd NUMERIC(15, 2),
    renewable_pct NUMERIC(5, 2),
    UNIQUE(time, iso_code)
);

-- Health Data
CREATE TABLE IF NOT EXISTS health_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    iso_code VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    life_expectancy NUMERIC(5, 2),
    hospital_beds_per_1000 NUMERIC(5, 2),
    pandemic_active_cases BIGINT,
    UNIQUE(time, iso_code)
);

-- Market Data
CREATE TABLE IF NOT EXISTS market_tickers (
    id UUID PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL UNIQUE,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    exchange VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS market_tick_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    ticker_id UUID NOT NULL REFERENCES market_tickers(id),
    price_open NUMERIC(15, 4),
    price_close NUMERIC(15, 4),
    price_high NUMERIC(15, 4),
    price_low NUMERIC(15, 4),
    volume BIGINT,
    volatility_index NUMERIC(10, 4),
    UNIQUE(time, ticker_id)
);

-- Geopolitical Events
CREATE TABLE IF NOT EXISTS geopolitical_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    iso_code VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    event_type VARCHAR(100),
    severity INT,
    description TEXT,
    event_date DATE
);

-- Note: In a real TimescaleDB setup we would run:
-- SELECT create_hypertable('population_data', 'time');
-- SELECT create_hypertable('trade_data', 'time');
-- SELECT create_hypertable('energy_data', 'time');
-- SELECT create_hypertable('health_data', 'time');
-- SELECT create_hypertable('market_tick_data', 'time');

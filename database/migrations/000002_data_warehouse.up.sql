CREATE TABLE IF NOT EXISTS world_bank_gdp (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) NOT NULL,
    year INT NOT NULL,
    gdp_usd NUMERIC(20, 2),
    unemployment_rate NUMERIC(5, 2),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (country_code, year)
);

CREATE TABLE IF NOT EXISTS yahoo_finance_indices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    open_price NUMERIC(10, 2),
    close_price NUMERIC(10, 2),
    volume BIGINT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (ticker, trade_date)
);

CREATE TABLE IF NOT EXISTS gdelt_global_events (
    id SERIAL PRIMARY KEY,
    event_date DATE NOT NULL,
    actor1_country_code VARCHAR(3),
    actor2_country_code VARCHAR(3),
    event_type VARCHAR(50),
    avg_tone NUMERIC(5, 2),
    source_url TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Phase 2 Database Evolution

-- Population Data
CREATE TABLE IF NOT EXISTS population_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    iso_code VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    total_population BIGINT,
    population_density NUMERIC(10, 2),
    urban_population_pct NUMERIC(5, 2)
);

-- Trade Data
CREATE TABLE IF NOT EXISTS trade_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    reporter_iso VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    partner_iso VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    export_value_usd NUMERIC(20, 2),
    import_value_usd NUMERIC(20, 2),
    commodity_code VARCHAR(50)
);

-- Energy Data
CREATE TABLE IF NOT EXISTS energy_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    iso_code VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    oil_production_bpd NUMERIC(15, 2),
    oil_consumption_bpd NUMERIC(15, 2),
    renewable_pct NUMERIC(5, 2)
);

-- Health Data
CREATE TABLE IF NOT EXISTS health_data (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    iso_code VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    life_expectancy NUMERIC(5, 2),
    hospital_beds_per_1000 NUMERIC(5, 2),
    pandemic_active_cases BIGINT
);

-- Note: In a real TimescaleDB setup we would run:
-- SELECT create_hypertable('population_data', 'time');
-- SELECT create_hypertable('trade_data', 'time');
-- SELECT create_hypertable('energy_data', 'time');
-- SELECT create_hypertable('health_data', 'time');

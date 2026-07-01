-- Phase 1 Database Base Schema

CREATE TABLE IF NOT EXISTS countries (
    iso_code VARCHAR(3) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS economic_time_series (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    iso_code VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    gdp_usd NUMERIC(25, 2),
    inflation_rate DECIMAL(10, 4)
);

CREATE TABLE IF NOT EXISTS climate_time_series (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    iso_code VARCHAR(3) NOT NULL REFERENCES countries(iso_code),
    avg_temp_celsius DECIMAL(10, 4),
    co2_ppm DECIMAL(10, 4)
);

-- Note: In a real TimescaleDB setup we would run:
-- SELECT create_hypertable('economic_time_series', 'time');
-- SELECT create_hypertable('climate_time_series', 'time');

-- Insert Seed Data (so DAGs don't fail foreign key constraint)
INSERT INTO countries (iso_code, name, region) VALUES
('USA', 'United States', 'North America'),
('CHN', 'China', 'Asia'),
('RUS', 'Russia', 'Europe/Asia'),
('IND', 'India', 'Asia'),
('EU', 'European Union', 'Europe')
ON CONFLICT (iso_code) DO NOTHING;

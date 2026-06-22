import requests
import wbgapi as wb
import pandas as pd
from sqlalchemy import create_engine, text
import datetime 
import yfinance as yf
import uuid
import time

DB_URL = "postgresql://sribash:56789@localhost:5432/world_sim"

def populate_countries_and_economics(engine):
    print("1. Fetching countries from World Bank API...")
    economies = wb.economy.DataFrame()
    countries_only = economies[economies['aggregate'] == False]
    
    countries = []
    iso_codes = []
    
    for idx, row in countries_only.iterrows():
        iso_code = idx
        name = row['name']
        region = row['region']
        
        if iso_code and len(iso_code) == 3:
            countries.append({
                'iso_code': iso_code,
                'name': name,
                'region': region
            })
            iso_codes.append(iso_code)

    df_countries = pd.DataFrame(countries)
    print(f"Inserting {len(df_countries)} countries into the DB...")
    
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM economic_time_series"))
        
        # Avoid deleting population_data if it causes FK issues, but for now we try
        try:
            conn.execute(text("DELETE FROM population_data"))
        except Exception:
            pass
            
        existing_df = pd.read_sql("SELECT iso_code FROM countries", conn)
        existing_isos = set(existing_df['iso_code'].tolist())
        
        new_countries = df_countries[~df_countries['iso_code'].isin(existing_isos)]
        if not new_countries.empty:
            new_countries.to_sql('countries', engine, if_exists='append', index=False)
            print(f"Inserted {len(new_countries)} NEW countries.")

    all_iso_df = pd.read_sql("SELECT iso_code FROM countries", engine)
    all_iso = all_iso_df['iso_code'].tolist()
    
    print("\n2. Fetching World Bank Data (GDP, Population, Inflation)...")
    
    try:
        gdp_data = wb.data.DataFrame('NY.GDP.MKTP.CD', all_iso, mrv=1)
        pop_data = wb.data.DataFrame('SP.POP.TOTL', all_iso, mrv=1)
        inf_data = wb.data.DataFrame('FP.CPI.TOTL.ZG', all_iso, mrv=1)
    except Exception as e:
        print(f"Error fetching WB data: {e}")
        return
        
    now = datetime.datetime.now(datetime.timezone.utc)
    
    eco_records = []
    
    for iso in all_iso:
        gdp = float(gdp_data.loc[iso].iloc[0]) if iso in gdp_data.index and not pd.isna(gdp_data.loc[iso].iloc[0]) else None
        pop = int(pop_data.loc[iso].iloc[0]) if iso in pop_data.index and not pd.isna(pop_data.loc[iso].iloc[0]) else None
        inf = float(inf_data.loc[iso].iloc[0]) if iso in inf_data.index and not pd.isna(inf_data.loc[iso].iloc[0]) else None
        
        if gdp is not None or inf is not None:
            eco_records.append({
                'time': now,
                'iso_code': iso,
                'gdp_usd': gdp,
                'inflation_rate': inf,
                'interest_rate': 0.05,
                'debt_to_gdp': 0.5
            })

    if eco_records:
        pd.DataFrame(eco_records).to_sql('economic_time_series', engine, if_exists='append', index=False)
        print(f"Inserted {len(eco_records)} economic records.")

def fetch_yahoo_finance(engine):
    print("\n3. Fetching Yahoo Finance Live Feed...")
    tickers = ["SPY", "QQQ", "GLD", "USO"]
    records = []
    now = datetime.datetime.now(datetime.timezone.utc)
    
    # Ensure tickers exist in market_tickers table
    with engine.begin() as conn:
        existing_tickers = pd.read_sql("SELECT symbol, id FROM market_tickers", conn)
        existing_symbols = set(existing_tickers['symbol'].tolist())
        ticker_id_map = dict(zip(existing_tickers['symbol'], existing_tickers['id']))
        
        for t in tickers:
            if t not in existing_symbols:
                new_id = str(uuid.uuid4())
                conn.execute(text(f"INSERT INTO market_tickers (id, symbol, company_name) VALUES ('{new_id}', '{t}', '{t}')"))
                ticker_id_map[t] = new_id

    for symbol in tickers:
        try:
            ticker_obj = yf.Ticker(symbol)
            hist = ticker_obj.history(period="1d")
            if not hist.empty:
                row = hist.iloc[-1]
                records.append({
                    'time': now,
                    'ticker_id': ticker_id_map[symbol],
                    'price_open': row['Open'],
                    'price_close': row['Close'],
                    'price_high': row['High'],
                    'price_low': row['Low'],
                    'volume': row['Volume'],
                    'volatility_index': 0.0 # Placeholder
                })
        except Exception as e:
            print(f"Error fetching {symbol} from Yahoo Finance: {e}")

    if records:
        pd.DataFrame(records).to_sql('market_tick_data', engine, if_exists='append', index=False)
        print(f"Inserted {len(records)} market tick records.")

def fetch_gdelt_events(engine):
    print("\n4. Fetching GDELT Live Events...")
    # GDELT has a public 15-minute JSON feed for GKG or export
    # For simulation, we'll use a mocked fetch representing GDELT extraction
    url = "https://api.gdeltproject.org/api/v2/doc/doc?query=war%20OR%20sanctions%20OR%20crisis&mode=ArtList&format=json&maxrecords=5"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            records = []
            for art in articles:
                # Basic parsing, random severity for now
                records.append({
                    'id': str(uuid.uuid4()),
                    'iso_code': 'USA', # Mocking ISO code extraction
                    'event_type': 'GEO_EVENT',
                    'severity': 7,
                    'description': art.get('title', 'GDELT Event'),
                    'event_date': datetime.datetime.now().date()
                })
            if records:
                pd.DataFrame(records).to_sql('geopolitical_events', engine, if_exists='append', index=False)
                print(f"Inserted {len(records)} GDELT geopolitical events.")
    except Exception as e:
        print(f"Error fetching GDELT data: {e}")

def fetch_other_sources(engine):
    print("\n5. Fetching IMF, WHO, UN Population, UN Comtrade, NOAA Climate Data...")
    # These often require complex API keys or specific queries
    # We will implement the pipeline structure with dummy requests as placeholders for full integration
    now = datetime.datetime.now(datetime.timezone.utc)
    
    climate_records = [{
        'time': now,
        'iso_code': 'USA',
        'avg_temp_celsius': 15.5,
        'co2_ppm': 420.1,
        'sea_level_rise_mm': 3.2
    }]
    pd.DataFrame(climate_records).to_sql('climate_time_series', engine, if_exists='append', index=False)
    print("Inserted 1 NOAA Climate record.")
    
    print("IMF Data Sync - OK (Mocked)")
    print("WHO Health Data Sync - OK (Mocked)")
    print("UN Population Data Sync - OK (Mocked)")
    print("UN Comtrade Trade Data Sync - OK (Mocked)")


def main():
    engine = create_engine(DB_URL)
    populate_countries_and_economics(engine)
    fetch_yahoo_finance(engine)
    fetch_gdelt_events(engine)
    fetch_other_sources(engine)
    print("\nDatabase Population Complete.")

if __name__ == "__main__":
    main()

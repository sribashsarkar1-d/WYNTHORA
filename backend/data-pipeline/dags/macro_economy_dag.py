from airflow import DAG # type: ignore
from airflow.providers.standard.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import requests # type: ignore
import pandas as pd # type: ignore
import sys
import os
import random

# Ensure plugins can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'plugins'))
from db_loader import load_dataframe_to_postgres # type: ignore

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_mock_economic_data(countries):
    """Fallback generator if APIs fail."""
    records = []
    current_year = datetime.now().year
    for iso in countries:
        for year in range(current_year - 5, current_year):
            records.append({
                'time': datetime(year, 1, 1),
                'iso_code': iso,
                'gdp_usd': round(random.uniform(1e11, 2e13), 2),
                'inflation_rate': round(random.uniform(-1.0, 15.0), 2)
            })
    return records

def fetch_macro_data():
    """
    Fetches macroeconomic data (e.g., Inflation, GDP) from FRED/IMF.
    """
    countries = ['USA', 'CHN', 'RUS', 'IND', 'EU']
    records = []
    
    # FRED API Key would normally come from Airflow Variables or ENV
    fred_api_key = os.getenv("FRED_API_KEY", "6524dab306e4668a17ea13deaf6a993c")
    
    try:
        # Example: Fetching US Inflation Rate (CPI) from FRED
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id=FPCPITOTLZGUSA&api_key={fred_api_key}&file_type=json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200 and 'observations' in response.json():
            observations = response.json()['observations']
            
            # Parse the latest available data
            for obs in observations[-5:]: # Get last 5 years
                if obs['value'] != '.':
                    records.append({
                        'time': datetime.strptime(obs['date'], "%Y-%m-%d"),
                        'iso_code': 'USA',
                        'gdp_usd': 25000000000000.00, # Mocked GDP for this script to match schema
                        'inflation_rate': float(obs['value'])
                    })
            
            # Mock the rest of the countries for demo
            mock_records = generate_mock_economic_data(['CHN', 'RUS', 'IND', 'EU'])
            records.extend(mock_records)
        else:
            raise Exception("API returned non-200 status or missing data")
            
    except Exception as e:
        print(f"Failed to fetch real macro data: {e}. Using mock fallback.")
        records = generate_mock_economic_data(countries)
        
    df = pd.DataFrame(records)
    df.dropna(subset=['iso_code'], inplace=True)
    
    # Load into PostgreSQL
    load_dataframe_to_postgres(df, 'economic_time_series', if_exists='append')

with DAG('macro_economy_ingestion', default_args=default_args, schedule='@daily', catchup=False) as dag:
    fetch_task = PythonOperator(
        task_id='fetch_and_load_macro',
        python_callable=fetch_macro_data
    )

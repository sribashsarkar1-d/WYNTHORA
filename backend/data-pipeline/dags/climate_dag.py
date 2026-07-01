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

def generate_mock_climate_data(countries):
    """Fallback generator if APIs fail."""
    records = []
    current_year = datetime.now().year
    for iso in countries:
        for year in range(current_year - 5, current_year):
            records.append({
                'time': datetime(year, 1, 1),
                'iso_code': iso,
                'avg_temp_celsius': round(random.uniform(10.0, 30.0), 2),
                'co2_ppm': round(random.uniform(400.0, 420.0), 2)
            })
    return records

def fetch_climate_data():
    """
    Fetches climate data. Uses Open-Meteo for temp and falls back to mock for CO2 
    since global CO2 is harder to fetch per-country without an API key.
    """
    countries = ['USA', 'CHN', 'RUS', 'IND', 'EU']
    records = []
    
    try:
        # Example API call (Open-Meteo historical for a specific coordinate, e.g., Washington DC for USA)
        url = "https://archive-api.open-meteo.com/v1/archive?latitude=38.9&longitude=-77.0&start_date=2023-01-01&end_date=2023-12-31&daily=temperature_2m_mean&timezone=auto"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            daily_temps = data['daily']['temperature_2m_mean']
            dates = data['daily']['time']
            
            # Aggregate to yearly avg for USA
            avg_temp = sum(t for t in daily_temps if t is not None) / len([t for t in daily_temps if t is not None])
            
            records.append({
                'time': datetime(2023, 1, 1),
                'iso_code': 'USA',
                'avg_temp_celsius': round(avg_temp, 2),
                'co2_ppm': 419.3 # Mock CO2
            })
            
            # For simplicity in this demo DAG, mock the others
            mock_records = generate_mock_climate_data(['CHN', 'RUS', 'IND', 'EU'])
            records.extend(mock_records)
            
        else:
            raise Exception("API returned non-200 status")
            
    except Exception as e:
        print(f"Failed to fetch real climate data: {e}. Using mock fallback.")
        records = generate_mock_climate_data(countries)
        
    df = pd.DataFrame(records)
    df.dropna(subset=['iso_code'], inplace=True)
    
    # Load into PostgreSQL
    load_dataframe_to_postgres(df, 'climate_time_series', if_exists='append')

with DAG('climate_ingestion', default_args=default_args, schedule='@daily', catchup=False) as dag:
    fetch_task = PythonOperator(
        task_id='fetch_and_load_climate',
        python_callable=fetch_climate_data
    )

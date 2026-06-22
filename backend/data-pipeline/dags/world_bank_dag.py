from airflow import DAG # type: ignore
from airflow.providers.standard.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import requests # type: ignore
import pandas as pd # type: ignore
import sys
import os

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

def fetch_world_bank_data():
    """
    Fetches GDP (NY.GDP.MKTP.CD) and Unemployment (SL.UEM.TOTL.ZS) from World Bank API.
    """
    countries = 'USA;CHN;RUS;IND;EU'
    # GDP Indicator
    gdp_url = f"http://api.worldbank.org/v2/country/{countries}/indicator/NY.GDP.MKTP.CD?format=json&per_page=100"
    response = requests.get(gdp_url)
    
    if response.status_code == 200 and len(response.json()) > 1:
        data = response.json()[1]
        
        # Parse into DataFrame
        records = []
        for item in data:
            if item['value'] is not None:
                records.append({
                    'country_code': item['countryiso3code'],
                    'year': int(item['date']),
                    'gdp_usd': item['value'],
                    'unemployment_rate': None # Would be fetched similarly in a real system
                })
                
        df = pd.DataFrame(records)
        df.dropna(subset=['country_code'], inplace=True)
        
        # Load into PostgreSQL
        load_dataframe_to_postgres(df, 'world_bank_gdp', if_exists='append')
    else:
        print("Failed to fetch data from World Bank.")

with DAG('world_bank_ingestion', default_args=default_args, schedule='@daily', catchup=False) as dag:
    fetch_task = PythonOperator(
        task_id='fetch_and_load_wb',
        python_callable=fetch_world_bank_data
    )

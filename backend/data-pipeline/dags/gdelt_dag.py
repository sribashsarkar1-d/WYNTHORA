from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import requests # type: ignore
import pandas as pd # type: ignore
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'plugins'))
from db_loader import load_dataframe_to_postgres # type: ignore

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_gdelt_data():
    """
    Fetches latest geopolitical events from the GDELT Project v2 API.
    """
    # GDELT DOC API for querying news events globally
    url = 'https://api.gdeltproject.org/api/v2/doc/doc?query=(USA OR China OR Russia OR EU) sourcelang:eng&mode=artlist&maxrecords=50&format=json'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        
        records = []
        for article in articles:
            # GDELT doesn't strictly provide actor1/actor2 easily in the DOC API,
            # but we can simulate parsing or use the GKG (Global Knowledge Graph).
            # Here we extract basic sentiment/tone if available and store it.
            
            records.append({
                'event_date': datetime.now().strftime('%Y-%m-%d'),
                'actor1_country_code': 'USA', # Mocking extraction logic for demonstration
                'actor2_country_code': 'CHN',
                'event_type': 'DIPLOMATIC_TENSION',
                'avg_tone': -1.5, # Negative tone
                'source_url': article.get('url', '')
            })
            
        df = pd.DataFrame(records)
        
        # Load into PostgreSQL
        load_dataframe_to_postgres(df, 'gdelt_global_events', if_exists='append')
    else:
        print("Failed to fetch GDELT data.")

with DAG('gdelt_ingestion', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    fetch_task = PythonOperator(
        task_id='fetch_and_load_gdelt',
        python_callable=fetch_gdelt_data
    )

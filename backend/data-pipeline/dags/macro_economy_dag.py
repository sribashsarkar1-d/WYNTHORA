from airflow import DAG # type: ignore
from airflow.providers.standard.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'collectors')))

def run_fred_collector():
    from fred_collector import FredCollector
    collector = FredCollector()
    collector.execute(conflict_cols=["time", "iso_code"])

def run_imf_collector():
    from imf_collector import ImfCollector
    collector = ImfCollector()
    collector.execute(conflict_cols=["time", "iso_code"])

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(minutes=30)
}

with DAG(
    'macro_economy_ingestion',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['economy', 'fred', 'imf'],
) as dag:

    fetch_fred = PythonOperator(
        task_id='fetch_and_load_fred',
        python_callable=run_fred_collector
    )

    fetch_imf = PythonOperator(
        task_id='fetch_and_load_imf',
        python_callable=run_imf_collector
    )

    # Parallel execution
    [fetch_fred, fetch_imf]

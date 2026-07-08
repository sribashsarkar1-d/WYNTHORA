from airflow import DAG # type: ignore
from airflow.providers.standard.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'collectors')))

def run_yf_collector():
    from yahoo_finance_collector import YahooFinanceCollector
    collector = YahooFinanceCollector()
    collector.execute(conflict_cols=["time", "ticker_id"])

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(minutes=30)
}

with DAG(
    'yahoo_finance_ingestion',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['finance', 'yahoo'],
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_and_load_yf',
        python_callable=run_yf_collector
    )

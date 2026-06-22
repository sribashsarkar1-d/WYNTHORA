from airflow import DAG # type: ignore
from airflow.providers.standard.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import sys
import os

# Append paths to allow importing from scripts/collectors
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'collectors')))

# Import collectors
from world_bank_collector import WorldBankCollector # type: ignore
from yahoo_finance_collector import YahooFinanceCollector # type: ignore
from gdelt_collector import GdeltCollector # type: ignore
from who_collector import WhoCollector # type: ignore

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Wrapper functions for the operators
def run_world_bank():
    collector = WorldBankCollector()
    collector.execute()

def run_yahoo_finance():
    collector = YahooFinanceCollector()
    collector.execute()

def run_gdelt():
    collector = GdeltCollector()
    collector.execute()

def run_who():
    collector = WhoCollector()
    collector.execute()

# Master ETL Pipeline
with DAG(
    'master_simulation_etl_pipeline',
    default_args=default_args,
    description='A master DAG to orchestrate all data collectors for the Digital Twin Earth.',
    schedule='@daily',
    catchup=False
) as dag:

    task_world_bank = PythonOperator(
        task_id='collect_world_bank_data',
        python_callable=run_world_bank
    )

    task_yahoo_finance = PythonOperator(
        task_id='collect_yahoo_finance_data',
        python_callable=run_yahoo_finance
    )

    task_gdelt = PythonOperator(
        task_id='collect_gdelt_data',
        python_callable=run_gdelt
    )

    task_who = PythonOperator(
        task_id='collect_who_data',
        python_callable=run_who
    )

    # Define dependencies
    # Yahoo Finance and GDELT can run in parallel. 
    # World Bank and WHO can also run in parallel.
    [task_world_bank, task_yahoo_finance, task_gdelt, task_who]

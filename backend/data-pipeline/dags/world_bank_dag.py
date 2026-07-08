from airflow import DAG # type: ignore
from airflow.providers.standard.operators.python import PythonOperator # type: ignore
from airflow.providers.standard.operators.bash import BashOperator # type: ignore
from datetime import datetime, timedelta
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'collectors')))

def run_wb_collector():
    from world_bank_collector import WorldBankCollector
    collector = WorldBankCollector()
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
    'world_bank_ingestion',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['economy', 'world_bank'],
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_and_load_wb',
        python_callable=run_wb_collector
    )
    
    # We use BashOperator for PySpark local execution in this prototype
    spark_job_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'spark_jobs', 'clean_world_bank_data.py'))
    
    clean_task = BashOperator(
        task_id='clean_wb_data_spark',
        bash_command=f"python {spark_job_path} /tmp/world_bank_raw.csv"
    )

    fetch_task >> clean_task

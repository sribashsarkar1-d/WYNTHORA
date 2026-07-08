from airflow import DAG # type: ignore
from airflow.providers.standard.operators.python import PythonOperator # type: ignore
from airflow.providers.standard.operators.bash import BashOperator # type: ignore
from airflow.utils.task_group import TaskGroup # type: ignore
from datetime import datetime, timedelta
import sys
import os

# Append paths to allow importing from scripts/collectors
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'collectors')))

# Import collectors
from world_bank_collector import WorldBankCollector
from yahoo_finance_collector import YahooFinanceCollector
from gdelt_collector import GdeltCollector
from who_collector import WhoCollector
from fred_collector import FredCollector
from imf_collector import ImfCollector

def on_failure_callback(context):
    print(f"Task {context.get('task_instance').task_id} failed!")

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': on_failure_callback
}

# Wrapper functions for the operators
def run_world_bank():
    collector = WorldBankCollector()
    collector.execute(conflict_cols=["time", "iso_code"])

def run_yahoo_finance():
    collector = YahooFinanceCollector()
    collector.execute(conflict_cols=["time", "ticker_id"])

def run_gdelt():
    collector = GdeltCollector()
    collector.execute()

def run_who():
    collector = WhoCollector()
    collector.execute(conflict_cols=["time", "iso_code"])

def run_fred():
    collector = FredCollector()
    collector.execute(conflict_cols=["time", "iso_code"])
    
def run_imf():
    collector = ImfCollector()
    collector.execute(conflict_cols=["time", "iso_code"])


# Master ETL Pipeline
with DAG(
    'master_simulation_etl_pipeline',
    default_args=default_args,
    description='A master DAG to orchestrate all data collectors and Spark jobs for the Digital Twin Earth.',
    schedule='@daily',
    catchup=False
) as dag:

    with TaskGroup("Collectors") as collectors_group:
        task_world_bank = PythonOperator(task_id='collect_world_bank', python_callable=run_world_bank)
        task_yahoo_finance = PythonOperator(task_id='collect_yahoo_finance', python_callable=run_yahoo_finance)
        task_gdelt = PythonOperator(task_id='collect_gdelt', python_callable=run_gdelt)
        task_who = PythonOperator(task_id='collect_who', python_callable=run_who)
        task_fred = PythonOperator(task_id='collect_fred', python_callable=run_fred)
        task_imf = PythonOperator(task_id='collect_imf', python_callable=run_imf)
        
        [task_world_bank, task_yahoo_finance, task_gdelt, task_who, task_fred, task_imf]

    with TaskGroup("SparkETL") as spark_group:
        spark_job_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'spark_jobs', 'clean_world_bank_data.py'))
        task_spark_wb = BashOperator(
            task_id='spark_clean_wb',
            bash_command=f"python {spark_job_path} /tmp/world_bank_raw.csv"
        )
        
        climate_job_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'spark_jobs', 'aggregate_climate_data.py'))
        task_spark_climate = BashOperator(
            task_id='spark_aggregate_climate',
            bash_command=f"python {climate_job_path}"
        )
        
        [task_spark_wb, task_spark_climate]

    collectors_group >> spark_group

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime
with DAG("macro_economy_ingestion", start_date=datetime(2026, 1, 1)) as dag:
    start = DummyOperator(task_id="start")

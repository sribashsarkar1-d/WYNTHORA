from airflow import DAG # type: ignore
from airflow.operators.empty import EmptyOperator # type: ignore
from datetime import datetime
with DAG("macro_economy_ingestion", start_date=datetime(2026, 1, 1)) as dag:
    start = EmptyOperator(task_id="start")

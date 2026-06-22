from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import sys
import os

try:
    import yfinance as yf # type: ignore
    import pandas as pd # type: ignore
except ImportError:
    pass

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'plugins'))
from db_loader import load_dataframe_to_postgres # type: ignore

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_yahoo_finance():
    """
    Fetches historical stock indices data (e.g. S&P 500) using yfinance.
    """
    tickers = ['^GSPC', '^VIX'] # S&P 500 and Volatility Index
    
    records = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d") # Fetch last 5 days
        
        for date, row in hist.iterrows():
            records.append({
                'ticker': ticker,
                'trade_date': date.strftime('%Y-%m-%d'),
                'open_price': row['Open'],
                'close_price': row['Close'],
                'volume': row['Volume']
            })
            
    df = pd.DataFrame(records)
    
    # Load to PostgreSQL
    load_dataframe_to_postgres(df, 'yahoo_finance_indices', if_exists='append')

with DAG('yahoo_finance_ingestion', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    fetch_task = PythonOperator(
        task_id='fetch_and_load_yf',
        python_callable=fetch_yahoo_finance
    )

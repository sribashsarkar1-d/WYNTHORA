import pandas as pd # type: ignore
from sqlalchemy import create_engine # type: ignore
import logging

import os

# In production, this would be fetched from Airflow connections or ENV vars
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "postgresql://postgres:56789@localhost:5432/world_sim")

def get_engine():
    """Returns a SQLAlchemy engine connected to the PostgreSQL warehouse."""
    try:
        engine = create_engine(DB_CONNECTION_STRING)
        return engine
    except Exception as e:
        logging.error(f"Failed to create database engine: {e}")
        return None

def load_dataframe_to_postgres(df: pd.DataFrame, table_name: str, if_exists: str = 'append'):
    """
    Loads a Pandas DataFrame into the specified PostgreSQL table.
    """
    engine = get_engine()
    if engine is None:
        logging.error("Cannot load data; engine is None.")
        return False
        
    try:
        # Use pandas to_sql to easily load the dataframe
        # In a high-volume production scenario, we'd use psycopg2 execute_values for speed
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        logging.info(f"Successfully loaded {len(df)} rows into '{table_name}'.")
        return True
    except Exception as e:
        logging.error(f"Failed to load data into '{table_name}': {e}")
        return False

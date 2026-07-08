import pandas as pd # type: ignore
from sqlalchemy import create_engine # type: ignore
import logging

import os

# In production, this would be fetched from Airflow connections or ENV vars
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "postgresql://sribash:56789@localhost:5432/world_sim")

def get_engine():
    """Returns a SQLAlchemy engine connected to the PostgreSQL warehouse."""
    try:
        engine = create_engine(DB_CONNECTION_STRING)
        return engine
    except Exception as e:
        logging.error(f"Failed to create database engine: {e}")
        return None

import uuid
from sqlalchemy import text # type: ignore
from typing import Literal, Optional, List

def load_dataframe_to_postgres(df: pd.DataFrame, table_name: str, if_exists: Literal['fail', 'replace', 'append'] = 'append', conflict_cols: Optional[List[str]] = None):
    """
    Loads a Pandas DataFrame into the specified PostgreSQL table.
    If conflict_cols is provided, performs an UPSERT (ON CONFLICT DO UPDATE).
    """
    engine = get_engine()
    if engine is None:
        logging.error("Cannot load data; engine is None.")
        return False
        
    try:
        if not conflict_cols:
            # Standard insert
            df.to_sql(table_name, engine, if_exists=if_exists, index=False)
            logging.info(f"Successfully loaded {len(df)} rows into '{table_name}'.")
            return True
            
        # UPSERT approach using a temporary table
        temp_table = f"{table_name}_temp_{uuid.uuid4().hex[:8]}"
        df.to_sql(temp_table, engine, if_exists='replace', index=False)
        
        # Build the ON CONFLICT DO UPDATE statement
        columns = df.columns.tolist()
        update_set = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns if col not in conflict_cols])
        conflict_target = ", ".join(conflict_cols)
        
        with engine.begin() as conn:
            if update_set:
                sql = f"""
                    INSERT INTO {table_name} ({", ".join(columns)})
                    SELECT {", ".join(columns)} FROM {temp_table}
                    ON CONFLICT ({conflict_target}) DO UPDATE SET {update_set};
                """
            else:
                # If all columns are in conflict_target (nothing to update)
                sql = f"""
                    INSERT INTO {table_name} ({", ".join(columns)})
                    SELECT {", ".join(columns)} FROM {temp_table}
                    ON CONFLICT ({conflict_target}) DO NOTHING;
                """
            conn.execute(text(sql))
            conn.execute(text(f"DROP TABLE {temp_table};"))
            
        logging.info(f"Successfully UPSERTED {len(df)} rows into '{table_name}'.")
        return True
    except Exception as e:
        logging.error(f"Failed to load data into '{table_name}': {e}")
        return False

from abc import ABC, abstractmethod
import pandas as pd # type: ignore
import logging
import sys
import os
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Any, Optional, List, Literal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugins')))
from db_loader import load_dataframe_to_postgres # type: ignore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class BaseCollector(ABC):
    """
    Abstract base class for all Data Collectors in the World Simulation Engine.
    """
    def __init__(self, source_name: str, target_table: str):
        self.source_name = source_name
        self.target_table = target_table
        self.logger = logging.getLogger(f"{self.source_name}_Collector")
        self.session = self._create_http_session()

    def _create_http_session(self) -> requests.Session:
        """Creates a requests session with exponential backoff retries."""
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,  # 1s, 2s, 4s, 8s, 16s...
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @abstractmethod
    def fetch_data(self) -> Any:
        """Fetches raw data from the external API or source."""
        pass

    @abstractmethod
    def transform_data(self, raw_data: Any) -> pd.DataFrame:
        """Transforms raw data into a structured Pandas DataFrame suitable for the warehouse."""
        pass

    def save_to_db(self, df: pd.DataFrame, if_exists: Literal['fail', 'replace', 'append'] = 'append', conflict_cols: Optional[List[str]] = None) -> bool:
        """Saves the transformed DataFrame to PostgreSQL."""
        if df is None or df.empty:
            self.logger.warning("No data to save.")
            return False
            
        self.logger.info(f"Saving {len(df)} records to {self.target_table} (UPSERT: {bool(conflict_cols)})...")
        success = load_dataframe_to_postgres(df, self.target_table, if_exists=if_exists, conflict_cols=conflict_cols)
        if success:
            self.logger.info(f"Successfully saved data to {self.target_table}.")
        else:
            self.logger.error(f"Failed to save data to {self.target_table}.")
        return success

    def execute(self, conflict_cols: Optional[List[str]] = None):
        """Executes the full ETL pipeline for this collector."""
        start_time = time.perf_counter()
        self.logger.info(f"Starting collection for {self.source_name}...")
        try:
            raw_data = self.fetch_data()
            if raw_data is not None:
                df = self.transform_data(raw_data)
                self.save_to_db(df, conflict_cols=conflict_cols)
        except Exception as e:
            self.logger.error(f"Execution failed for {self.source_name}: {e}", exc_info=True)
        finally:
            duration = time.perf_counter() - start_time
            self.logger.info(f"Finished collection for {self.source_name}. Duration: {duration:.2f}s")

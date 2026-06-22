from abc import ABC, abstractmethod
import pandas as pd # type: ignore
import logging
import sys
import os

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

    @abstractmethod
    def fetch_data(self) -> any:
        """Fetches raw data from the external API or source."""
        pass

    @abstractmethod
    def transform_data(self, raw_data: any) -> pd.DataFrame:
        """Transforms raw data into a structured Pandas DataFrame suitable for the warehouse."""
        pass

    def save_to_db(self, df: pd.DataFrame, if_exists: str = 'append') -> bool:
        """Saves the transformed DataFrame to PostgreSQL."""
        if df is None or df.empty:
            self.logger.warning("No data to save.")
            return False
            
        self.logger.info(f"Saving {len(df)} records to {self.target_table}...")
        success = load_dataframe_to_postgres(df, self.target_table, if_exists=if_exists)
        if success:
            self.logger.info(f"Successfully saved data to {self.target_table}.")
        else:
            self.logger.error(f"Failed to save data to {self.target_table}.")
        return success

    def execute(self):
        """Executes the full ETL pipeline for this collector."""
        self.logger.info(f"Starting collection for {self.source_name}")
        raw_data = self.fetch_data()
        if raw_data is not None:
            df = self.transform_data(raw_data)
            self.save_to_db(df)
        self.logger.info(f"Finished collection for {self.source_name}")

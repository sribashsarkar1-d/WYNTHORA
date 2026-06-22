from base_collector import BaseCollector
import pandas as pd # type: ignore
import os

class FredCollector(BaseCollector):
    def __init__(self):
        super().__init__(source_name="FRED", target_table="economic_time_series")
        self.api_key = os.getenv("FRED_API_KEY")

    def fetch_data(self):
        self.logger.info("Fetching FRED data (Stub)...")
        if not self.api_key:
            self.logger.warning("FRED_API_KEY not set. Skipping.")
        return []

    def transform_data(self, raw_data) -> pd.DataFrame:
        return pd.DataFrame()

if __name__ == "__main__":
    collector = FredCollector()
    collector.execute()

from base_collector import BaseCollector
import pandas as pd # type: ignore
import os

class ImfCollector(BaseCollector):
    def __init__(self):
        super().__init__(source_name="IMF", target_table="economic_time_series")
        self.api_key = os.getenv("IMF_API_KEY")

    def fetch_data(self):
        self.logger.info("Fetching IMF data (Stub)...")
        return []

    def transform_data(self, raw_data) -> pd.DataFrame:
        return pd.DataFrame()

if __name__ == "__main__":
    collector = ImfCollector()
    collector.execute()

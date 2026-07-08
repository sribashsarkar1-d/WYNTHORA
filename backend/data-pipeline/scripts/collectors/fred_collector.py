import os
import pandas as pd # type: ignore
from datetime import datetime
from base_collector import BaseCollector

class FredCollector(BaseCollector):
    """
    Collects US Economic indicators from the Federal Reserve Economic Data (FRED) API.
    """
    def __init__(self):
        super().__init__(source_name="FRED", target_table="economic_time_series")
        self.api_key = os.getenv("FRED_API_KEY")
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        
        # Mapping of our internal metric names to FRED Series IDs
        self.series_mapping = {
            "gdp_usd": "GDP",                     # Gross Domestic Product
            "inflation_rate": "CPIAUCSL",         # Consumer Price Index
            "federal_funds_rate": "FEDFUNDS",
            "unemployment_rate": "UNRATE",
            "ppi": "PPIACO",                      # Producer Price Index
            "industrial_production": "INDPRO",
            "m2_money_supply": "M2SL",
            "10yr_treasury_yield": "GS10",
            "consumer_sentiment": "UMCSENT",
            "housing_starts": "HOUST",
            "retail_sales": "RSAFS",
            "business_inventories": "BUSINV"
        }

    def fetch_data(self) -> dict:
        if not self.api_key:
            self.logger.warning("FRED_API_KEY is missing. Skipping data collection.")
            return None

        self.logger.info("Starting FRED data fetch...")
        raw_data = {}
        
        for metric_name, series_id in self.series_mapping.items():
            self.logger.info(f"Fetching {metric_name} (Series: {series_id})...")
            params = {
                "series_id": series_id,
                "api_key": self.api_key,
                "file_type": "json",
                "frequency": "m", # Monthly for consistency
                "sort_order": "desc",
                "limit": 120 # Last 10 years of monthly data
            }
            
            try:
                response = self.session.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                raw_data[metric_name] = data.get("observations", [])
                self.logger.info(f"Fetched {len(raw_data[metric_name])} records for {metric_name}")
            except Exception as e:
                self.logger.error(f"Failed to fetch {series_id}: {e}")
                
        return raw_data

    def transform_data(self, raw_data: dict) -> pd.DataFrame:
        if not raw_data:
            return pd.DataFrame()

        records = []
        # FRED data is mostly US data, so we hardcode iso_code to 'USA'
        
        # We will pivot the data so that each date has a row with all metrics
        # First, flatten into a list of dicts: {date, metric_name, value}
        flat_records = []
        for metric_name, observations in raw_data.items():
            for obs in observations:
                val = obs.get("value", ".")
                if val == ".": 
                    continue # FRED represents missing as "."
                
                flat_records.append({
                    "time": obs.get("date"),
                    "iso_code": "USA",
                    metric_name: float(val)
                })

        if not flat_records:
            return pd.DataFrame()

        df_flat = pd.DataFrame(flat_records)
        df_flat['time'] = pd.to_datetime(df_flat['time'])
        
        # Group by time and iso_code, and aggregate (take first non-null for each metric)
        df = df_flat.groupby(['time', 'iso_code']).first().reset_index()
        
        # Validate and clean up
        # Reject future dates
        df = df[df['time'] <= pd.Timestamp.now()]
        
        self.logger.info(f"Transformed data into {len(df)} rows and {len(df.columns)} columns.")
        return df

if __name__ == "__main__":
    collector = FredCollector()
    # UPSERT matching on time and iso_code
    collector.execute(conflict_cols=["time", "iso_code"])

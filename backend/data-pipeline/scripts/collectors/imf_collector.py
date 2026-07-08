import os
import pandas as pd # type: ignore
from datetime import datetime
from base_collector import BaseCollector

class ImfCollector(BaseCollector):
    """
    Collects Macro-Economic data from the International Monetary Fund (IMF) API.
    Uses the IMF JSON REST API.
    """
    def __init__(self):
        super().__init__(source_name="IMF", target_table="economic_time_series")
        # IMF API doesn't strictly require an API key for public data, but we can pass it if we have one.
        self.api_key = os.getenv("IMF_API_KEY", "")
        self.base_url = "http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/"
        
        # Datasets and Indicators mapping
        # Example dataset: IFS (International Financial Statistics)
        self.dataset = "IFS"
        
        # Indicator Code to our metric mapping
        self.indicator_mapping = {
            "NGDP_XDC": "gdp_local_currency",      # Nominal GDP
            "PCPI_IX": "cpi_index",                # Consumer Price Index
            "LUR_PT": "unemployment_rate",         # Unemployment Rate
            "GGXWDG_NGDP": "debt_to_gdp"           # General government gross debt
        }
        
        # Countries to fetch (ISO 2-letter usually for IMF, but we map to ISO-3 later)
        # USA=US, China=CN, India=IN, Russia=RU, UK=GB, Germany=DE
        self.countries = ["US", "CN", "IN", "RU", "GB", "DE"]

    def fetch_data(self) -> dict:
        self.logger.info("Starting IMF data fetch...")
        raw_data = {}
        
        # Format: {Dataset}/{Frequency}.{Country}.{Indicator}
        frequency = "A" # Annual data
        countries_str = "+".join(self.countries)
        indicators_str = "+".join(self.indicator_mapping.keys())
        
        url = f"{self.base_url}{self.dataset}/{frequency}.{countries_str}.{indicators_str}"
        
        try:
            self.logger.info(f"Fetching from IMF URL: {url}")
            response = self.session.get(url, timeout=45)
            response.raise_for_status()
            data = response.json()
            
            # The structure of IMF JSON is nested: 
            # CompactData -> DataSet -> Series
            series_list = data.get("CompactData", {}).get("DataSet", {}).get("Series", [])
            if not isinstance(series_list, list):
                series_list = [series_list] # Sometimes returns a single dict if only one series matches
                
            raw_data["Series"] = series_list
            self.logger.info(f"Fetched {len(series_list)} time series blocks from IMF.")
        except Exception as e:
            self.logger.error(f"Failed to fetch IMF data: {e}")
            
        return raw_data

    def transform_data(self, raw_data: dict) -> pd.DataFrame:
        if not raw_data or "Series" not in raw_data:
            return pd.DataFrame()

        records = []
        
        # Map ISO-2 to ISO-3 manually for our tracked countries
        iso_map = {
            "US": "USA", "CN": "CHN", "IN": "IND", "RU": "RUS", "GB": "GBR", "DE": "DEU"
        }

        for series in raw_data["Series"]:
            # Series keys usually look like: @FREQ, @REF_AREA, @INDICATOR
            ref_area = series.get("@REF_AREA")
            indicator = series.get("@INDICATOR")
            
            iso_code = iso_map.get(ref_area)
            metric_name = self.indicator_mapping.get(indicator)
            
            if not iso_code or not metric_name:
                continue
                
            obs_list = series.get("Obs", [])
            if not isinstance(obs_list, list):
                obs_list = [obs_list]
                
            for obs in obs_list:
                period = obs.get("@TIME_PERIOD")
                value = obs.get("@OBS_VALUE")
                
                if period and value:
                    records.append({
                        "time": f"{period}-01-01", # Assume Jan 1st for annual data
                        "iso_code": iso_code,
                        metric_name: float(value)
                    })

        if not records:
            return pd.DataFrame()

        df_flat = pd.DataFrame(records)
        df_flat['time'] = pd.to_datetime(df_flat['time'])
        
        # Group and aggregate
        df = df_flat.groupby(['time', 'iso_code']).first().reset_index()
        
        # Validate (No future dates)
        df = df[df['time'] <= pd.Timestamp.now()]
        
        self.logger.info(f"Transformed IMF data into {len(df)} rows.")
        return df

if __name__ == "__main__":
    collector = ImfCollector()
    collector.execute(conflict_cols=["time", "iso_code"])

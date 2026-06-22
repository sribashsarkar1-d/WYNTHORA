from base_collector import BaseCollector
import requests # type: ignore
import pandas as pd # type: ignore
import zipfile
import io
import os
from datetime import datetime

class GdeltCollector(BaseCollector):
    """
    Collects geopolitical event data from the GDELT Project (v2.0).
    """
    def __init__(self):
        super().__init__(source_name="GDELT", target_table="geopolitical_events")
        self.last_update_url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
        
        # GDELT v2.0 column names (partial list of the 61 columns for what we need)
        self.columns = [
            "GLOBALEVENTID", "SQLDATE", "MonthYear", "Year", "FractionDate", 
            "Actor1Code", "Actor1Name", "Actor1CountryCode", "Actor1KnownGroupCode", "Actor1EthnicCode", 
            "Actor1Religion1Code", "Actor1Religion2Code", "Actor1Type1Code", "Actor1Type2Code", "Actor1Type3Code",
            "Actor2Code", "Actor2Name", "Actor2CountryCode", "Actor2KnownGroupCode", "Actor2EthnicCode",
            "Actor2Religion1Code", "Actor2Religion2Code", "Actor2Type1Code", "Actor2Type2Code", "Actor2Type3Code",
            "IsRootEvent", "EventCode", "EventBaseCode", "EventRootCode", "QuadClass", 
            "GoldsteinScale", "NumMentions", "NumSources", "NumArticles", "AvgTone",
            "Actor1Geo_Type", "Actor1Geo_FullName", "Actor1Geo_CountryCode", "Actor1Geo_ADM1Code", "Actor1Geo_ADM2Code", "Actor1Geo_Lat", "Actor1Geo_Long", "Actor1Geo_FeatureID",
            "Actor2Geo_Type", "Actor2Geo_FullName", "Actor2Geo_CountryCode", "Actor2Geo_ADM1Code", "Actor2Geo_ADM2Code", "Actor2Geo_Lat", "Actor2Geo_Long", "Actor2Geo_FeatureID",
            "ActionGeo_Type", "ActionGeo_FullName", "ActionGeo_CountryCode", "ActionGeo_ADM1Code", "ActionGeo_ADM2Code", "ActionGeo_Lat", "ActionGeo_Long", "ActionGeo_FeatureID",
            "DATEADDED", "SOURCEURL"
        ]

    def fetch_data(self):
        self.logger.info("Fetching GDELT last update URL...")
        response = requests.get(self.last_update_url)
        if response.status_code != 200:
            self.logger.error("Failed to fetch GDELT lastupdate.txt")
            return None
            
        # Parse the lastupdate.txt
        # Format: <size> <hash> <url>
        lines = response.text.strip().split('\n')
        export_url = None
        for line in lines:
            if "export.CSV.zip" in line:
                export_url = line.split(' ')[-1]
                break
                
        if not export_url:
            self.logger.error("Could not find export CSV in GDELT lastupdate.txt")
            return None
            
        self.logger.info(f"Downloading GDELT data from: {export_url}")
        csv_response = requests.get(export_url)
        if csv_response.status_code == 200:
            try:
                # Extract zip in memory
                with zipfile.ZipFile(io.BytesIO(csv_response.content)) as z:
                    csv_filename = z.namelist()[0]
                    with z.open(csv_filename) as f:
                        df = pd.read_csv(f, sep='\t', header=None, names=self.columns, dtype=str)
                        return df
            except Exception as e:
                self.logger.error(f"Failed to extract or parse GDELT zip: {e}")
                return None
        else:
            self.logger.error("Failed to download GDELT zip file.")
            return None

    def transform_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        if raw_data is None or raw_data.empty:
            return pd.DataFrame()
            
        df = raw_data.copy()
        
        # We need to map GDELT schema to our `geopolitical_events` table:
        # id (uuid, auto-generated), iso_code (varchar), event_type (varchar), severity (int), description (text), event_date (date)
        
        # Filter only events that have an Actor1CountryCode
        df = df.dropna(subset=['Actor1CountryCode'])
        
        # Map GoldsteinScale to severity (1 to 10 scale). 
        # Goldstein is -10 to +10. We'll map -10 to 10 severity, +10 to 1 severity.
        def map_severity(goldstein):
            try:
                g = float(goldstein)
                # Map -10 to 10, +10 to 1. Severity = 5.5 - (g / 2) -> roughly 1 to 10
                s = int(5.5 - (g / 2.0))
                return max(1, min(10, s))
            except:
                return 5
                
        df['severity'] = df['GoldsteinScale'].apply(map_severity)
        
        # Description can be the ActionGeo_FullName + EventCode
        df['description'] = df['Actor1Name'].fillna('Unknown') + " performed action " + df['EventCode'].fillna('00') + " in " + df['ActionGeo_FullName'].fillna('Unknown')
        
        # Parse date (YYYYMMDD)
        df['event_date'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d', errors='coerce').dt.date
        
        # Map FIPS 10-4 country code (which GDELT uses) to ISO-3. 
        # For prototype, we'll just take the first 3 chars or mock it.
        # GDELT uses FIPS codes like 'US', 'CH', 'RS'. We need ISO3 like 'USA', 'CHN', 'RUS'.
        fips_to_iso3 = {
            'US': 'USA', 'CH': 'CHN', 'RS': 'RUS', 'IN': 'IND', 'JA': 'JPN', 
            'GM': 'DEU', 'UK': 'GBR', 'FR': 'FRA', 'BR': 'BRA', 'SF': 'ZAF'
        }
        df['iso_code'] = df['Actor1CountryCode'].map(fips_to_iso3)
        df = df.dropna(subset=['iso_code']) # Keep only the ones we know
        
        # Event type
        df['event_type'] = "GDELT_EVENT_" + df['EventRootCode'].astype(str)
        
        # Select final columns
        final_df = df[['iso_code', 'event_type', 'severity', 'description', 'event_date']].copy()
        
        # Let's just take a small sample to avoid spamming the DB
        final_df = final_df.head(50)
        
        return final_df

if __name__ == "__main__":
    collector = GdeltCollector()
    collector.execute()

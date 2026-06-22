from base_collector import BaseCollector
import requests # type: ignore
import pandas as pd # type: ignore
from datetime import datetime

class WhoCollector(BaseCollector):
    """
    Collects Health data from the World Health Organization (WHO) OData API.
    """
    def __init__(self):
        super().__init__(source_name="WHO", target_table="health_data")
        # Indicator codes from WHO
        self.indicators = {
            'WHOSIS_000001': 'life_expectancy'
            # Could add hospital beds, etc.
        }
        
    def fetch_data(self):
        all_data = []
        for ind_code, col_name in self.indicators.items():
            self.logger.info(f"Fetching WHO indicator: {ind_code} ({col_name})")
            # Fetch data from Athena (WHO OData)
            url = f"https://ghoapi.azureedge.net/api/{ind_code}"
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    records = response.json().get('value', [])
                    for record in records:
                        # We only want country-level data (SpatialDimType == 'COUNTRY')
                        if record.get('SpatialDimType') == 'COUNTRY':
                            all_data.append({
                                'iso_code': record.get('SpatialDim'),
                                'year': record.get('TimeDim'),
                                'indicator': col_name,
                                'value': record.get('NumericValue')
                            })
                else:
                    self.logger.error(f"Failed to fetch {ind_code}. Status: {response.status_code}")
            except Exception as e:
                self.logger.error(f"Exception while fetching WHO data: {e}")
                
        return all_data

    def transform_data(self, raw_data) -> pd.DataFrame:
        if not raw_data:
            return pd.DataFrame()
            
        df = pd.DataFrame(raw_data)
        df = df.dropna(subset=['value'])
        
        # Pivot table
        df_pivot = df.pivot_table(index=['iso_code', 'year'], 
                                  columns='indicator', 
                                  values='value').reset_index()
                                  
        # Convert year to timestamp
        # WHO sometimes provides years as "2019" or "2010-2015"
        def parse_year(y):
            try:
                return datetime(int(y), 1, 1)
            except:
                # If range, take start year
                return datetime(int(str(y).split('-')[0]), 1, 1)
                
        df_pivot['time'] = df_pivot['year'].apply(parse_year)
        
        # Add required schema columns that we might not have fetched
        if 'life_expectancy' not in df_pivot.columns:
            df_pivot['life_expectancy'] = None
        df_pivot['hospital_beds_per_1000'] = None
        df_pivot['pandemic_active_cases'] = 0
        
        # We need to make sure countries exist or we get a foreign key error
        from db_loader import get_engine # type: ignore
        try:
            engine = get_engine()
            existing_countries = pd.read_sql("SELECT iso_code FROM countries", engine)
            existing_isos = existing_countries['iso_code'].tolist()
            # Filter to only insert data for countries that exist in our simulation subset
            df_pivot = df_pivot[df_pivot['iso_code'].isin(existing_isos)]
        except Exception as e:
            self.logger.warning(f"Failed to filter by existing countries: {e}")
        
        return df_pivot[['time', 'iso_code', 'life_expectancy', 'hospital_beds_per_1000', 'pandemic_active_cases']]

if __name__ == "__main__":
    collector = WhoCollector()
    collector.execute()

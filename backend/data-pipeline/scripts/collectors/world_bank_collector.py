from base_collector import BaseCollector
import requests # type: ignore
import pandas as pd # type: ignore
from datetime import datetime

class WorldBankCollector(BaseCollector):
    """
    Collects GDP and other economic indicators from the World Bank API.
    """
    def __init__(self):
        super().__init__(source_name="WorldBank", target_table="economic_time_series")
        self.indicators = {
            'NY.GDP.MKTP.CD': 'gdp_usd',           # GDP (current US$)
            'FP.CPI.TOTL.ZG': 'inflation_rate',    # Inflation, consumer prices (annual %)
            'FR.INR.LEND': 'interest_rate'         # Lending interest rate (%)
        }
        # Using a subset of major economies for the simulation
        self.countries = 'USA;CHN;RUS;IND;JPN;DEU;GBR;FRA;BRA;ZAF'

    def fetch_data(self):
        all_data = []
        for indicator, column_name in self.indicators.items():
            self.logger.info(f"Fetching {indicator} ({column_name}) from World Bank...")
            url = f"http://api.worldbank.org/v2/country/{self.countries}/indicator/{indicator}?format=json&per_page=1000"
            response = requests.get(url)
            
            if response.status_code == 200 and len(response.json()) > 1:
                data = response.json()[1]
                for item in data:
                    if item['value'] is not None:
                        all_data.append({
                            'iso_code': item['countryiso3code'],
                            'year': int(item['date']),
                            'indicator': column_name,
                            'value': item['value']
                        })
            else:
                self.logger.error(f"Failed to fetch {indicator}. Status: {response.status_code}")
                
        return all_data

    def transform_data(self, raw_data) -> pd.DataFrame:
        if not raw_data:
            return pd.DataFrame()
            
        df = pd.DataFrame(raw_data)
        
        # Pivot table so indicators become columns
        df_pivot = df.pivot_table(index=['iso_code', 'year'], 
                                  columns='indicator', 
                                  values='value').reset_index()
                                  
        # Convert year to timestamp (Jan 1st of that year)
        df_pivot['time'] = df_pivot['year'].apply(lambda y: datetime(y, 1, 1))
        df_pivot.drop(columns=['year'], inplace=True)
        
        # Reorder to match DB schema: time, iso_code, gdp_usd, inflation_rate, interest_rate, debt_to_gdp
        columns = ['time', 'iso_code']
        for col in ['gdp_usd', 'inflation_rate', 'interest_rate']:
            if col not in df_pivot.columns:
                df_pivot[col] = None
        
        # We don't have debt_to_gdp from this specific list yet, add as None
        df_pivot['debt_to_gdp'] = None
        
        # Ensure the countries exist in the database to satisfy the foreign key
        from db_loader import load_dataframe_to_postgres, get_engine # type: ignore
        try:
            engine = get_engine()
            existing_countries = pd.read_sql("SELECT iso_code FROM countries", engine)
            existing_isos = existing_countries['iso_code'].tolist()
            
            country_names = {
                'USA': 'United States', 'CHN': 'China', 'RUS': 'Russia', 'IND': 'India',
                'JPN': 'Japan', 'DEU': 'Germany', 'GBR': 'United Kingdom', 'FRA': 'France',
                'BRA': 'Brazil', 'ZAF': 'South Africa'
            }
            
            new_countries = []
            for iso in df_pivot['iso_code'].unique():
                if iso not in existing_isos:
                    new_countries.append({
                        'iso_code': iso,
                        'name': country_names.get(iso, iso),
                        'region': 'Global'
                    })
            
            if new_countries:
                pd.DataFrame(new_countries).to_sql('countries', engine, if_exists='append', index=False)
        except Exception as e:
            self.logger.warning(f"Could not insert countries (they might already exist): {e}")

        return df_pivot[['time', 'iso_code', 'gdp_usd', 'inflation_rate', 'interest_rate', 'debt_to_gdp']]

if __name__ == "__main__":
    collector = WorldBankCollector()
    collector.execute()

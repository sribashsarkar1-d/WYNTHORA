from base_collector import BaseCollector
import yfinance as yf # type: ignore
import pandas as pd # type: ignore
from datetime import datetime, timedelta

class YahooFinanceCollector(BaseCollector):
    """
    Collects stock market ticker data using yfinance.
    """
    def __init__(self):
        super().__init__(source_name="YahooFinance", target_table="market_tick_data")
        # Global indices to track the macro markets
        self.tickers = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'NASDAQ',
            '^FTSE': 'FTSE 100',
            '^N225': 'Nikkei 225'
        }

    def fetch_data(self):
        self.logger.info(f"Fetching market data for {list(self.tickers.keys())}...")
        
        # Fetch last 30 days of daily data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        data_frames = []
        for symbol, name in self.tickers.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date)
                
                if not hist.empty:
                    hist = hist.reset_index()
                    hist['symbol'] = symbol
                    data_frames.append(hist)
            except Exception as e:
                self.logger.error(f"Failed to fetch data for {symbol}: {e}")
                
        if data_frames:
            return pd.concat(data_frames, ignore_index=True)
        return None

    def transform_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        if raw_data is None or raw_data.empty:
            return pd.DataFrame()
            
        df = raw_data.copy()
        
        # Map columns to DB schema: time, ticker_id (we'll use symbol for now), price_open, price_close, price_high, price_low, volume
        df = df.rename(columns={
            'Date': 'time',
            'Open': 'price_open',
            'Close': 'price_close',
            'High': 'price_high',
            'Low': 'price_low',
            'Volume': 'volume'
        })
        
        # In a real DB we need to map 'symbol' to 'ticker_id' UUID.
        # For this prototype, if the DB schema requires a UUID, we'd need to lookup the UUID.
        # But we'll pass the symbol temporarily or generate a mock UUID if needed.
        # Wait, the schema market_tick_data has ticker_id as UUID. 
        # I should generate a deterministic UUID based on the symbol name.
        import uuid
        df['ticker_id'] = df['symbol'].apply(lambda s: str(uuid.uuid5(uuid.NAMESPACE_DNS, s)))
        df['volatility_index'] = None
        
        # Prepare tickers DataFrame to ensure foreign keys exist
        tickers_df = df[['ticker_id', 'symbol']].drop_duplicates()
        tickers_df = tickers_df.rename(columns={'ticker_id': 'id'})
        tickers_df['company_name'] = tickers_df['symbol']
        tickers_df['sector'] = 'Index'
        tickers_df['exchange'] = 'Global'
        
        # We need to save tickers first. We can call load_dataframe_to_postgres directly.
        from db_loader import load_dataframe_to_postgres # type: ignore
        try:
            # We use append, but since we generate deterministic UUIDs, if we run it twice it might fail with duplicate key.
            # To be safe for this prototype, we'll fetch existing and only insert new.
            from db_loader import get_engine # type: ignore
            engine = get_engine()
            existing_tickers = pd.read_sql("SELECT id FROM market_tickers", engine)
            existing_ids = existing_tickers['id'].astype(str).tolist()
            new_tickers = tickers_df[~tickers_df['id'].isin(existing_ids)]
            if not new_tickers.empty:
                load_dataframe_to_postgres(new_tickers, 'market_tickers', if_exists='append')
        except Exception as e:
            self.logger.warning(f"Could not insert tickers (they might already exist): {e}")

        return df[['time', 'ticker_id', 'price_open', 'price_close', 'price_high', 'price_low', 'volume', 'volatility_index']]

if __name__ == "__main__":
    collector = YahooFinanceCollector()
    collector.execute()

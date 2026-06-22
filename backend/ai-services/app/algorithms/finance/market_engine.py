from .black_scholes import BlackScholesPricer
from .gbm import GeometricBrownianMotion
from .arima_model import ARIMAModel
from .lstm_predictor import MarketLSTM
from .transformer_informer import InformerTransformer
from .finbert_sentiment import FinBERTSentiment
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from algorithms.data_loader import RealWorldDataLoader

class FinancialMarketEngine:
    """
    Integrates all Quantitative Finance and Time-Series AI models.
    """
    def __init__(self):
        self.bs_pricer = BlackScholesPricer(risk_free_rate=0.05)
        self.gbm = GeometricBrownianMotion(mu=0.08, sigma=0.2, dt=1/252)
        
        self.arima = ARIMAModel(p=3)
        self.lstm = MarketLSTM()
        self.transformer = InformerTransformer()
        self.finbert = FinBERTSentiment()
        
        self.data_loader = RealWorldDataLoader()
        self.rolling_stock_path = None

    def run_market_simulation(self, active_events=None, macro_context=None, news_feed=None):
        if active_events is None:
            active_events = []
        if macro_context is None:
            macro_context = [100.0, 0.02, 0.05, 400.0]
        if news_feed is None or len(news_feed) == 0:
            news_feed = ["Global market experiences routine trading day."]
            
        print("=== FINANCIAL MARKET ENGINE ANALYSIS ===")

        # 1. Fetch Real Stock Paths (Yahoo Finance)
        print("\n1. Fetching Real Stock Paths (Yahoo Finance)...")
        if self.rolling_stock_path is None:
            try:
                import yfinance as yf
                # SP500, NASDAQ, Crude Oil, Gold, EUR/USD
                tickers = ["^GSPC", "^IXIC", "CL=F", "GC=F", "EURUSD=X"]
                data = yf.download(tickers, period="3mo", interval="1d", progress=False)['Close']
                
                # Extract SP500 for the main simulation path
                sp500_data = data['^GSPC'].dropna().values
                if len(sp500_data) > 30:
                    stock_path = sp500_data[-30:] # Last 30 days
                else:
                    stock_path = sp500_data
                self.rolling_stock_path = list(stock_path)
                    
                current_price = stock_path[-1]
                start_price = stock_path[0]
                print(f"   SP500 Starting Price (30d ago): ${start_price:.2f} | Current Price: ${current_price:.2f}")
                print(f"   Current NASDAQ: ${data['^IXIC'].dropna().iloc[-1]:.2f} | Oil: ${data['CL=F'].dropna().iloc[-1]:.2f} | Gold: ${data['GC=F'].dropna().iloc[-1]:.2f} | EUR/USD: {data['EURUSD=X'].dropna().iloc[-1]:.4f}")
            except Exception as e:
                print(f"   Failed to fetch real data ({e}). Falling back to SDE (GBM)...")
                stock_path = self.gbm.simulate_path(S0=150.0, days=30)
                self.rolling_stock_path = list(stock_path)
                current_price = stock_path[-1]
                print(f"   Starting Price: $150.00 | Current Price (Day 30): ${current_price:.2f}")
        else:
            stock_path = np.array(self.rolling_stock_path)
            current_price = stock_path[-1]
            start_price = stock_path[0]
            print(f"   Using Rolling Stock Path. Current Price: ${current_price:.2f}")

        # 2. Options Pricing (Black-Scholes)
        strike = current_price * 1.05 # 5% out of the money
        call_price = self.bs_pricer.price(S=current_price, K=strike, T=30/365, sigma=0.2, option_type='call')
        print(f"\n2. Black-Scholes Options Pricing:")
        print(f"   Value of a Call Option (Strike ${strike:.2f}, 30 days to expiry): ${call_price:.2f}")

        # 3. ARIMA Baseline Forecasting (e.g. steady GDP growth history)
        gdp_history = self.data_loader.get_gdp_history()
        self.arima.fit(gdp_history)
        gdp_forecast = self.arima.predict(gdp_history, steps=2)
        print(f"\n3. ARIMA Macro Forecast:")
        print(f"   Next 2 Quarters GDP Forecast: ${gdp_forecast[0]:.2f}T, ${gdp_forecast[1]:.2f}T")

        # 4. Event Shock Calculation
        shock_penalty = 0.0
        for e in active_events:
            if e.__class__.__name__ == 'WarEvent':
                shock_penalty += 0.40 * (e.severity / 10.0)
            elif e.__class__.__name__ == 'EnergyCrisisEvent':
                shock_penalty += 0.25 * (e.severity / 10.0)
            elif e.__class__.__name__ == 'PandemicEvent':
                shock_penalty += 0.30 * (e.severity / 10.0)

        # 5. LSTM Next-Day Stock Prediction (Event-Aware 5D)
        lstm_pred = self.lstm.predict(stock_path, macro_context=macro_context, event_shock=shock_penalty)
        print(f"\n4. LSTM Neural Network Prediction (5D Macro Context + Events):")
        print(f"   Predicted Next-Day Stock Price: ${lstm_pred:.2f}")
        
        # Append prediction to rolling window and drop the oldest
        self.rolling_stock_path.append(float(lstm_pred))
        if len(self.rolling_stock_path) > 30:
            self.rolling_stock_path.pop(0)

        # 6. FinBERT NLP Sentiment Analysis
        # We aggregate the live news headlines
        aggregated_news = " ".join(news_feed)
        sentiment_score_raw = self.finbert.analyze(aggregated_news)
        final_sentiment = float(sentiment_score_raw[0] if isinstance(sentiment_score_raw, list) else sentiment_score_raw)
        
        print(f"\n5. FinBERT NLP Market Sentiment:")
        print(f"   Headline analyzed: '{news_feed[0]} ...'")
        
        status = "BULLISH" if final_sentiment > 0 else "BEARISH" if final_sentiment < 0 else "NEUTRAL"
        print(f"   Sentiment Score: {final_sentiment} ({status})")

        # 7. Transformer (Informer) Crash Risk
        # Simulate a high volatility spike
        volatility_history = self.data_loader.get_market_volatility()
        base_crash_risk = self.transformer.predict_crash_risk(volatility_history)
                
        crash_risk = min(0.99, base_crash_risk + shock_penalty)
        print(f"\n6. Transformer Long-Horizon Crash Risk:")
        print(f"   Base Tech Risk: {base_crash_risk * 100:.1f}% | Event Shock Adj: +{shock_penalty * 100:.1f}%")
        print(f"   Total Probability of Sudden Market Crash: {crash_risk * 100:.1f}%")
        
        print("\n=== END OF FINANCIAL ANALYSIS ===")
        
        # Return real AI insights to the global state
        return {
            "lstm_pred": float(lstm_pred),
            "sentiment_score": final_sentiment,
            "crash_risk": float(crash_risk),
            "arima_gdp_forecast": [float(gdp_forecast[0]), float(gdp_forecast[1])],
            "options_call_price": float(call_price)
        }

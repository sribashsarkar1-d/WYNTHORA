from black_scholes import BlackScholesPricer
from gbm import GeometricBrownianMotion
from arima_model import ARIMAModel
from lstm_predictor import MarketLSTM
from transformer_informer import InformerTransformer
from finbert_sentiment import FinBERTSentiment
import numpy as np

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

    def run_market_simulation(self):
        print("=== FINANCIAL MARKET ENGINE ANALYSIS ===")

        # 1. Simulate Stock Path using SDE (GBM)
        print("\n1. Simulating 30-day Stock Path (GBM SDE)...")
        stock_path = self.gbm.simulate_path(S0=150.0, days=30)
        current_price = stock_path[-1]
        print(f"   Starting Price: $150.00 | Current Price (Day 30): ${current_price:.2f}")

        # 2. Options Pricing (Black-Scholes)
        strike = 155.0
        call_price = self.bs_pricer.price(S=current_price, K=strike, T=30/365, sigma=0.2, option_type='call')
        print(f"\n2. Black-Scholes Options Pricing:")
        print(f"   Value of a Call Option (Strike ${strike:.2f}, 30 days to expiry): ${call_price:.2f}")

        # 3. ARIMA Baseline Forecasting (e.g. steady GDP growth history)
        gdp_history = [20.0, 20.2, 20.5, 20.7, 21.1, 21.4, 21.8]
        self.arima.fit(gdp_history)
        gdp_forecast = self.arima.predict(gdp_history, steps=2)
        print(f"\n3. ARIMA Macro Forecast:")
        print(f"   Next 2 Quarters GDP Forecast: ${gdp_forecast[0]:.2f}T, ${gdp_forecast[1]:.2f}T")

        # 4. LSTM Next-Day Stock Prediction
        lstm_pred = self.lstm.predict(stock_path)
        print(f"\n4. LSTM Neural Network Prediction:")
        print(f"   Predicted Next-Day Stock Price: ${lstm_pred:.2f}")

        # 5. FinBERT NLP Sentiment Analysis
        news_headline = "Global market faces severe crash as war sanctions isolate major economies."
        sentiment = self.finbert.analyze(news_headline)
        sentiment_label = "BULLISH" if sentiment > 0 else "BEARISH" if sentiment < 0 else "NEUTRAL"
        print(f"\n5. FinBERT NLP Market Sentiment:")
        print(f"   Headline: '{news_headline}'")
        print(f"   Sentiment Score: {sentiment} ({sentiment_label})")

        # 6. Transformer (Informer) Crash Risk
        # Simulate a high volatility spike
        volatility_history = [0.1, 0.12, 0.15, 0.14, 0.55, 0.60]
        crash_risk = self.transformer.predict_crash_risk(volatility_history)
        print(f"\n6. Transformer Long-Horizon Crash Risk:")
        print(f"   Probability of Sudden Market Crash: {crash_risk * 100:.1f}%")
        
        print("\n=== END OF FINANCIAL ANALYSIS ===")

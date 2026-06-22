import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np

# Add parent dir to path so we can import the models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from app.algorithms.finance.lstm_predictor import MarketLSTM # type: ignore
from app.algorithms.finance.transformer_informer import InformerTransformer # type: ignore

def get_training_data():
    """
    Fetches 10-year historical market data from Yahoo Finance for training.
    """
    try:
        import yfinance as yf
        print("Fetching 10-year SPY data from Yahoo Finance...")
        # Older yfinance returns a Series for single ticker, newer returns a DataFrame
        close_data = yf.download("SPY", period="10y", interval="1d", progress=False)['Close']
        if isinstance(close_data, pd.DataFrame):
            price_array = close_data.iloc[:, 0].values
        else:
            price_array = close_data.values
            
        price_array = price_array[~np.isnan(price_array)]
        if len(price_array) < 100:
            raise ValueError("Not enough historical data downloaded.")
            
        days = len(price_array)
        print(f"Loaded {days} days of real SPY data.")
        
        prices = np.zeros((days, 5))
        prices[:, 0] = price_array
        
        # Fill in realistic base numbers for the other 4 dimensions to match 5D inference
        prices[:, 1] = np.linspace(100.0, 150.0, days) # GDP (fake historical trend)
        prices[:, 2] = np.linspace(0.01, 0.05, days) # Inflation (fake historical trend)
        prices[:, 3] = np.linspace(0.01, 0.05, days) # Rates (fake historical trend)
        prices[:, 4] = np.linspace(350.0, 420.0, days) # CO2 (fake historical trend)
        
    except Exception as e:
        print(f"YFinance fetch failed ({e}). Generating synthetic 10-year market cycle for training...")
        # Generate synthetic data with some trend and volatility for 5 variables
        np.random.seed(42)
        days = 3650
        prices = np.zeros((days, 5)) # 0: Price, 1: GDP, 2: Inflation, 3: Rates, 4: CO2
        prices[0] = [1000.0, 100.0, 0.02, 0.05, 400.0]
        
        for i in range(1, days):
            drift = 0.0002
            volatility = 0.015
            shock = 0
            if i % 800 == 0:  # Simulate periodic crashes
                shock = -0.15
                
            # Price
            prices[i, 0] = prices[i-1, 0] * (1 + np.random.normal(drift, volatility) + shock)
            # GDP
            prices[i, 1] = prices[i-1, 1] * (1 + np.random.normal(0.0001, 0.001) + (shock*0.1))
            # Inflation
            prices[i, 2] = max(0.0, prices[i-1, 2] + np.random.normal(0, 0.001) - (shock*0.05))
            # Rates
            prices[i, 3] = max(0.0, prices[i-1, 3] + np.random.normal(0, 0.001))
            # CO2
            prices[i, 4] = prices[i-1, 4] + np.random.normal(0.1, 0.05)
            
    return prices

def train_lstm(prices, save_path):
    print("--- Training MarketLSTM ---")
    
    # Create sequences (e.g., look back 30 days to predict next day)
    seq_length = 30
    X, y = [], []
    for i in range(len(prices) - seq_length):
        seq = prices[i:i+seq_length, :] # All 5 features
        next_price = prices[i+seq_length, 0] # Predicting just price
        
        last_day = seq[-1, :]
        if np.any(last_day == 0):
            continue
            
        # Normalize sequence based on the last day's values
        norm_seq = seq / last_day
        X.append(norm_seq)
        y.append(next_price / last_day[0])
        
    X_array = np.array(X)
    y_array = np.array(y)
    
    # Validation split (last 20%)
    split_idx = int(len(X_array) * 0.8)
    X_train, X_val = X_array[:split_idx], X_array[split_idx:]
    y_train, y_val = y_array[:split_idx], y_array[split_idx:]
    
    X_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_tensor = torch.tensor(y_train, dtype=torch.float32).unsqueeze(-1)
    
    # Updated input_size to 5
    model = MarketLSTM(input_size=5, hidden_layer_size=50, output_size=1)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.lstm.parameters(), lr=0.001)
    
    epochs = 50 # Increased from 5 for real convergence
    for epoch in range(epochs):
        model.lstm.train()
        model.linear.train()
        optimizer.zero_grad()
        
        lstm_out, _ = model.lstm(X_tensor)
        predictions = model.linear(lstm_out[:, -1, :])
        
        loss = criterion(predictions, y_tensor)
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{epochs} | Training MSE Loss: {loss.item():.6f}")
            
    # Calculate Validation Metrics
    model.lstm.eval()
    model.linear.eval()
    with torch.no_grad():
        X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
        y_val_tensor = torch.tensor(y_val, dtype=torch.float32).unsqueeze(-1)
        val_out, _ = model.lstm(X_val_tensor)
        val_preds = model.linear(val_out[:, -1, :])
        
        val_mse = criterion(val_preds, y_val_tensor).item()
        rmse = np.sqrt(val_mse)
        mae = torch.mean(torch.abs(val_preds - y_val_tensor)).item()
        mape = torch.mean(torch.abs((val_preds - y_val_tensor) / y_val_tensor)).item() * 100
        
    print(f"\n--- LSTM Validation Metrics ---")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE:  {mae:.4f}")
    print(f"MAPE: {mape:.2f}%\n")
    
    # Save weights
    torch.save({
        'model_state_dict': model.lstm.state_dict(),
        'linear_state_dict': model.linear.state_dict(),
        'max_scalar': 1.0 # Legacy compat
    }, save_path)
    print(f"LSTM training complete. Saved to {save_path}\n")

def train_transformer(prices, save_path):
    print("--- Training InformerTransformer (Crash Risk) ---")
    # prices is now (days, 5). We extract column 0 (price) for volatility
    price_array = prices[:, 0]
    
    # Calculate rolling 30-day volatility as the input feature
    df = pd.DataFrame({'price': price_array})
    df['returns'] = df['price'].pct_change()
    df['volatility'] = df['returns'].rolling(30).std()
    
    # Label a "crash" as a drop of > 5% in the next 7 days
    df['future_return'] = df['price'].shift(-7) / df['price'] - 1
    df['is_crash'] = (df['future_return'] < -0.05).astype(float)
    
    df = df.dropna()
    volatility = df['volatility'].values
    is_crash = df['is_crash'].values
    
    seq_length = 30
    X, y = [], []
    for i in range(len(volatility) - seq_length):
        X.append(volatility[i:i+seq_length])
        y.append(is_crash[i+seq_length])
        
    X_tensor = torch.tensor(np.array(X), dtype=torch.float32).unsqueeze(-1)
    y_tensor = torch.tensor(np.array(y), dtype=torch.float32).unsqueeze(-1)
    
    model = InformerTransformer(feature_size=1, num_layers=2, nhead=1)
    criterion = nn.BCELoss() # Binary Cross Entropy for risk probability
    optimizer = optim.Adam(list(model.transformer_encoder.parameters()) + list(model.decoder.parameters()), lr=0.001)
    
    epochs = 50
    for epoch in range(epochs):
        optimizer.zero_grad()
        
        encoded = model.transformer_encoder(X_tensor)
        risk_score = torch.sigmoid(model.decoder(encoded[:, -1, :]))
        
        loss = criterion(risk_score, y_tensor)
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{epochs} | BCE Loss: {loss.item():.6f}")

    torch.save({
        'encoder_state_dict': model.transformer_encoder.state_dict(),
        'decoder_state_dict': model.decoder.state_dict()
    }, save_path)
    print(f"Transformer training complete. Saved to {save_path}\n")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'app', 'models', 'weights'))
    os.makedirs(base_dir, exist_ok=True)
    
    lstm_path = os.path.join(base_dir, 'lstm_weights.pth')
    transformer_path = os.path.join(base_dir, 'transformer_weights.pth')
    
    prices = get_training_data()
    train_lstm(prices, lstm_path)
    train_transformer(prices, transformer_path)
    print("ALL AI FORECASTING MODELS TRAINED SUCCESSFULLY.")

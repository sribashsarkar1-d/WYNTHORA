import os
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class MarketLSTM:
    """
    Long Short-Term Memory (LSTM) network for predicting next week's stock prices.
    Designed for Sequence-to-Sequence forecasting.
    """
    def __init__(self, input_size=5, hidden_layer_size=50, output_size=1):
        if not TORCH_AVAILABLE:
            return # Fallback graceful exit
            
        self.lstm = nn.LSTM(input_size, hidden_layer_size, batch_first=True)
        self.linear = nn.Linear(hidden_layer_size, output_size)
        self.max_scalar = 1000.0 # Default
        
        # Load weights if available
        weight_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'weights', 'lstm_weights.pth'))
        if os.path.exists(weight_path):
            try:
                checkpoint = torch.load(weight_path, map_location=torch.device('cpu'), weights_only=True)
                self.lstm.load_state_dict(checkpoint['model_state_dict'])
                self.linear.load_state_dict(checkpoint['linear_state_dict'])
                self.max_scalar = checkpoint.get('max_scalar', 1000.0)
                self.lstm.eval()
                self.linear.eval()
            except RuntimeError as e:
                print(f"Skipping weight load due to shape mismatch: {e}")
            
    def predict(self, sequence, macro_context=None, event_shock=0.0):
        """
        :param sequence: List or numpy array of historical prices
        :param macro_context: List of [gdp, inflation, interest_rate, co2]
        :param event_shock: Severity of global crises (0.0 to 1.0)
        """
        if not TORCH_AVAILABLE or len(sequence) == 0:
            return float(sequence[-1]) if len(sequence) > 0 else 0.0
            
        if macro_context is None:
            macro_context = [100.0, 0.02, 0.05, 400.0]

        # Normalize relative to the last known price to predict a multiplier
        last_price = float(sequence[-1])
        if last_price == 0:
            return 0.0
            
        gdp_n = macro_context[0] / 300000.0
        inf_n = max(0.01, macro_context[1] / 0.02)
        rate_n = max(0.01, macro_context[2] / 0.05)
        co2_n = macro_context[3] / 400.0
            
        normalized_seq = [[float(p) / last_price, gdp_n, inf_n, rate_n, co2_n] for p in sequence]
        
        # Ensure we only use the last 30 days if sequence is longer
        if len(normalized_seq) > 30:
            normalized_seq = normalized_seq[-30:]
        elif len(normalized_seq) < 30:
            # Pad with 1.0s at the beginning
            pad = [[1.0, 1.0, 1.0, 1.0, 1.0]] * (30 - len(normalized_seq))
            normalized_seq = pad + normalized_seq
            
        seq_tensor = torch.tensor(normalized_seq, dtype=torch.float32).view(1, 30, 5)
        
        with torch.no_grad():
            lstm_out, _ = self.lstm(seq_tensor)
            predictions = self.linear(lstm_out[:, -1, :])
        
        # De-normalize
        predicted_val = predictions.item() * last_price
        
        # Immediately factor in the event shock (e.g. 0.4 shock drops price by up to 10%)
        predicted_val *= (1.0 - (event_shock * 0.25))
        
        # Bound the daily jump to a realistic maximum of +/- 3% (unless shock is severe)
        max_jump = last_price * (0.03 + event_shock)
        if predicted_val > last_price + max_jump:
            predicted_val = last_price + max_jump
        elif predicted_val < last_price - max_jump:
            predicted_val = last_price - max_jump
            
        return max(0.0, predicted_val)



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
    def __init__(self, input_size=1, hidden_layer_size=50, output_size=1):
        if not TORCH_AVAILABLE:
            return # Fallback graceful exit
            
        self.lstm = nn.LSTM(input_size, hidden_layer_size, batch_first=True)
        self.linear = nn.Linear(hidden_layer_size, output_size)
        
    def predict(self, sequence):
        """
        :param sequence: List or numpy array of historical prices
        """
        if not TORCH_AVAILABLE:
            # Fallback: Just return the last known value (Naive Forecast) if PyTorch isn't installed
            return float(sequence[-1])

        seq_tensor = torch.tensor(sequence, dtype=torch.float32).view(1, -1, 1)
        lstm_out, _ = self.lstm(seq_tensor)
        
        # Take the output of the last time step
        predictions = self.linear(lstm_out[:, -1, :])
        return predictions.item()

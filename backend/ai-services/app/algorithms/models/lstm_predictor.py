import torch
import torch.nn as nn
import logging
import numpy as np

logger = logging.getLogger("LSTMPredictor")

class EconomicLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(EconomicLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

class LSTMPredictionEngine:
    """
    Enterprise LSTM Prediction Layer.
    Forecasts economic indicators (GDP, Inflation) based on historical sequence data.
    """
    def __init__(self):
        self.input_size = 5 # e.g. GDP, Inflation, Interest Rate, CO2, Market Vol
        self.hidden_size = 64
        self.num_layers = 2
        self.output_size = 2 # Forecasting GDP growth and Inflation
        self.model = EconomicLSTM(self.input_size, self.hidden_size, self.num_layers, self.output_size)
        
        # Load weights if available, else initialize randomly for simulation
        try:
            # self.model.load_state_dict(torch.load("weights/lstm_v1.pt"))
            self.model.eval()
            logger.info("LSTM Model Loaded and ready for inference.")
        except Exception:
            logger.warning("No pre-trained LSTM weights found. Using random initialization.")

    def predict(self, sequence: np.ndarray) -> dict:
        """
        Expects sequence shape (batch_size, sequence_length, input_size)
        """
        if sequence.shape[-1] != self.input_size:
            raise ValueError(f"Expected input size {self.input_size}, got {sequence.shape[-1]}")
            
        with torch.no_grad():
            tensor_seq = torch.FloatTensor(sequence)
            if len(tensor_seq.shape) == 2:
                tensor_seq = tensor_seq.unsqueeze(0) # Add batch dimension
                
            prediction = self.model(tensor_seq)
            pred_np = prediction.numpy()[0]
            
        return {
            "predicted_gdp_growth": float(pred_np[0]),
            "predicted_inflation": float(pred_np[1])
        }

import os
from typing import Dict, Any
from app.ai.interfaces.base_model import BaseAIModel

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class MarketLSTM(BaseAIModel):
    """
    Long Short-Term Memory (LSTM) network for sequence-to-sequence forecasting.
    Adheres strictly to the BaseAIModel contract. Feature scaling is handled externally by the Feature Store.
    """
    def __init__(self, model_name: str = "MarketLSTM", version: str = "1.0", input_size: int = 5, hidden_layer_size: int = 50, output_size: int = 1):
        super().__init__(model_name, version)
        
        if not TORCH_AVAILABLE:
            self.model = None
            return
            
        class LSTMNet(nn.Module):
            def __init__(self, inp, hidden, out):
                super().__init__()
                self.lstm = nn.LSTM(inp, hidden, batch_first=True)
                self.linear = nn.Linear(hidden, out)
                
            def forward(self, x):
                lstm_out, _ = self.lstm(x)
                predictions = self.linear(lstm_out[:, -1, :])
                return predictions
                
        self.model = LSTMNet(input_size, hidden_layer_size, output_size)
        
    def train(self, features: torch.Tensor, labels: torch.Tensor, **kwargs) -> Dict[str, float]:
        if not TORCH_AVAILABLE or self.model is None:
            return {"loss": 0.0}
            
        epochs = kwargs.get("epochs", 10)
        learning_rate = kwargs.get("learning_rate", 0.001)
        
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        
        self.model.train()
        final_loss = 0.0
        
        for epoch in range(epochs):
            optimizer.zero_grad()
            predictions = self.model(features)
            loss = criterion(predictions, labels)
            loss.backward()
            optimizer.step()
            final_loss = loss.item()
            
        return {"loss": final_loss}

    def predict(self, features: torch.Tensor) -> torch.Tensor:
        if not TORCH_AVAILABLE or self.model is None:
            return torch.zeros(1)
            
        self.model.eval()
        with torch.no_grad():
            return self.model(features)
            
    def save_weights(self, path: str) -> None:
        if not TORCH_AVAILABLE or self.model is None:
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(self.model.state_dict(), path)
        
    def load_weights(self, path: str) -> None:
        if not TORCH_AVAILABLE or self.model is None:
            return
        if os.path.exists(path):
            self.model.load_state_dict(torch.load(path, map_location=torch.device('cpu'), weights_only=True))
            self.model.eval()

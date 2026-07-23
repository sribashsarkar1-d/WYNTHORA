from abc import ABC, abstractmethod
from typing import Any, Dict
import torch

class BaseAIModel(ABC):
    """
    Standard interface for all AI Models (LSTM, ARIMA, GNN, RL Agents).
    Enforces a consistent ML lifecycle across the Simulation Engine.
    """
    
    def __init__(self, model_name: str, version: str = "1.0"):
        self.model_name = model_name
        self.version = version
        self.model = None # Subclasses must initialize their specific PyTorch/SKLearn model here
        
    @abstractmethod
    def train(self, features: torch.Tensor, labels: torch.Tensor, **kwargs) -> Dict[str, float]:
        """
        Trains the model using Tensors provided by the Feature Store.
        Returns a dictionary of metrics (e.g., {"loss": 0.05, "accuracy": 0.92})
        """
        pass
        
    @abstractmethod
    def predict(self, features: torch.Tensor) -> torch.Tensor:
        """
        Runs inference on the provided feature Tensor.
        """
        pass
        
    @abstractmethod
    def save_weights(self, path: str) -> None:
        """
        Serializes and saves the model weights/state.
        """
        pass
        
    @abstractmethod
    def load_weights(self, path: str) -> None:
        """
        Loads the model weights/state from disk.
        """
        pass

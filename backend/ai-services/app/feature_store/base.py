from abc import ABC, abstractmethod
from typing import Any, List, Dict
import torch

class BaseFeatureStore(ABC):
    """
    Abstract Base Class for the AI Feature Store.
    Responsible for converting raw Data Warehouse records into ML-ready Tensors.
    """
    
    @abstractmethod
    def get_historical_features(self, entity_id: str, feature_names: List[str], start_time: Any, end_time: Any) -> torch.Tensor:
        """
        Retrieves historical features for training models (e.g., LSTMs, ARIMA).
        Returns a PyTorch Tensor.
        """
        pass
        
    @abstractmethod
    def get_online_features(self, entity_ids: List[str], feature_names: List[str]) -> Dict[str, torch.Tensor]:
        """
        Retrieves low-latency real-time features for live inference.
        """
        pass
        
    @abstractmethod
    def compute_features(self, raw_data: Any) -> torch.Tensor:
        """
        Calculates derived features (e.g., YoY Growth, Moving Averages) from raw data.
        """
        pass

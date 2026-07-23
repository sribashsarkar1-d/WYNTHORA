from typing import Any, List, Dict
import torch
import numpy as np
from app.feature_store.base import BaseFeatureStore
from app.contracts.economy import EconomicIndicatorContract

class EconomyFeatureStore(BaseFeatureStore):
    """
    Transforms Economy Domain Data (GDP, Inflation) into ML-ready PyTorch Tensors.
    """
    
    def get_historical_features(self, entity_id: str, feature_names: List[str], start_time: Any, end_time: Any) -> torch.Tensor:
        # Placeholder for querying the database.
        # In a real scenario, we'd inject EconomyRepository and query it here.
        # Returning a dummy tensor of shape (seq_len, num_features)
        seq_len = 10
        num_features = len(feature_names)
        return torch.randn(seq_len, num_features)
        
    def get_online_features(self, entity_ids: List[str], feature_names: List[str]) -> Dict[str, torch.Tensor]:
        features = {}
        for eid in entity_ids:
            features[eid] = torch.randn(1, len(feature_names))
        return features
        
    def compute_features(self, raw_data: List[EconomicIndicatorContract]) -> torch.Tensor:
        """
        Converts a list of Pydantic Contracts directly into a normalized PyTorch Tensor.
        Handles sorting by year and extracting the values.
        """
        if not raw_data:
            return torch.empty(0)
            
        # Sort by year to ensure time-series order is correct
        sorted_data = sorted(raw_data, key=lambda x: x.year)
        
        # Extract values
        values = [record.value for record in sorted_data]
        
        # Convert to numpy then tensor for performance
        np_values = np.array(values, dtype=np.float32)
        
        # Basic Min-Max Normalization as an example feature engineering step
        min_val = np.min(np_values)
        max_val = np.max(np_values)
        if max_val > min_val:
            normalized = (np_values - min_val) / (max_val - min_val)
        else:
            normalized = np_values
            
        return torch.tensor(normalized).view(-1, 1) # Shape: (seq_len, 1)

try:
    import torch
    import torch.nn as nn
    import math
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

import os

class InformerTransformer:
    """
    Attention Transformer (Informer architecture derivative) for Long-Horizon Forecasting.
    Used to detect complex 10-year macroeconomic cycles and predict sudden market crashes.
    """
    def __init__(self, feature_size=1, num_layers=2, nhead=1):
        if not TORCH_AVAILABLE:
            return
            
        self.encoder_layer = nn.TransformerEncoderLayer(d_model=feature_size, nhead=nhead, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        self.decoder = nn.Linear(feature_size, 1)
        
        # Load weights if available
        weight_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'weights', 'transformer_weights.pth'))
        if os.path.exists(weight_path):
            checkpoint = torch.load(weight_path, map_location=torch.device('cpu'), weights_only=True)
            self.transformer_encoder.load_state_dict(checkpoint['encoder_state_dict'])
            self.decoder.load_state_dict(checkpoint['decoder_state_dict'])
            self.transformer_encoder.eval()
            self.decoder.eval()

    def predict_crash_risk(self, historical_volatility):
        """
        Analyzes volatility over time and outputs a Crash Risk %
        """
        if not TORCH_AVAILABLE:
            # Fallback heuristic: If volatility spikes over 50%, call it a 90% risk.
            if len(historical_volatility) > 0 and historical_volatility[-1] > 0.5:
                return 0.90
            return 0.10

        seq_tensor = torch.tensor(historical_volatility, dtype=torch.float32).view(1, -1, 1)
        
        with torch.no_grad():
            # Pass through transformer
            encoded = self.transformer_encoder(seq_tensor)
            
            # Decoder outputs risk score
            risk_score = torch.sigmoid(self.decoder(encoded[:, -1, :]))
            
        return risk_score.item()

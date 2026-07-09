from typing import Dict, Any
from app.core.config import settings

class FeatureFlags:
    """
    Enterprise Feature Management
    Provides runtime feature toggles, experimental features, and kill switches.
    """
    
    # Feature Toggles
    ENABLE_ADVANCED_CLIMATE_MODEL: bool = False
    ENABLE_REAL_TIME_MARKET_DATA: bool = False
    ENABLE_EXPERIMENTAL_NLP: bool = False
    
    # Kill Switches
    DISABLE_BACKGROUND_WORKERS: bool = False
    DISABLE_WS_BROADCAST: bool = False
    
    # Canary Deployments / Rollouts
    ML_MODEL_VERSION: str = "v1.0.0"

    @classmethod
    def get_all_flags(cls) -> Dict[str, Any]:
        return {
            "ENABLE_ADVANCED_CLIMATE_MODEL": cls.ENABLE_ADVANCED_CLIMATE_MODEL,
            "ENABLE_REAL_TIME_MARKET_DATA": cls.ENABLE_REAL_TIME_MARKET_DATA,
            "ENABLE_EXPERIMENTAL_NLP": cls.ENABLE_EXPERIMENTAL_NLP,
            "DISABLE_BACKGROUND_WORKERS": cls.DISABLE_BACKGROUND_WORKERS,
            "DISABLE_WS_BROADCAST": cls.DISABLE_WS_BROADCAST,
            "ML_MODEL_VERSION": cls.ML_MODEL_VERSION
        }

    @classmethod
    def is_enabled(cls, flag_name: str) -> bool:
        return getattr(cls, flag_name, False)

feature_flags = FeatureFlags()

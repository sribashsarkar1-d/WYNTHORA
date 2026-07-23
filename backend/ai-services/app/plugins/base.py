from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseDataSource(ABC):
    """
    Abstract Base Class for all external data source plugins.
    Enforces a strict contract for data ingestion to maintain consistency.
    """
    
    @abstractmethod
    async def fetch(self) -> Any:
        """Fetch raw data from the external API or source."""
        pass
        
    @abstractmethod
    def normalize(self, raw_data: Any) -> Any:
        """Convert raw data into a standardized internal Pydantic schema."""
        pass
        
    @abstractmethod
    def validate(self, normalized_data: Any) -> bool:
        """Validate the normalized data to ensure data quality."""
        pass
        
    @abstractmethod
    def transform(self, validated_data: Any) -> Any:
        """Apply business transformations or feature engineering if necessary."""
        pass
        
    @abstractmethod
    async def save(self, final_data: Any) -> None:
        """Persist the data to the repository layer."""
        pass
        
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the external API is reachable and healthy."""
        pass
        
    @abstractmethod
    def metadata(self) -> Dict[str, str]:
        """Return metadata about this plugin (source, version, etc)."""
        pass

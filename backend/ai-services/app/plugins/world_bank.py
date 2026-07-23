import logging
import requests
import asyncio
from typing import Any, Dict
from app.plugins.base import BaseDataSource
from app.infrastructure.storage.data_lake import DataLakeManager
from app.normalizers.world_bank import WorldBankNormalizer
from app.validators.economy import EconomyValidator

logger = logging.getLogger(__name__)

class WorldBankPlugin(BaseDataSource):
    """
    Enterprise Plugin for World Bank Macroeconomic Data Ingestion.
    Follows the strict ETL contract defined by BaseDataSource.
    """
    
    BASE_URL = "http://api.worldbank.org/v2"
    
    def __init__(self, indicator_code: str = "NY.GDP.MKTP.CD"):
        self.indicator_code = indicator_code
        self.source_name = "world_bank"
        
    def _fetch_sync(self, url: str) -> Any:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    async def fetch(self) -> Any:
        logger.info(f"Fetching data from World Bank for {self.indicator_code}")
        # Fetching a large page size to get data efficiently
        url = f"{self.BASE_URL}/country/all/indicator/{self.indicator_code}?format=json&per_page=5000"
        
        try:
            raw_data = await asyncio.to_thread(self._fetch_sync, url)
            
            # Save raw payload to data lake immediately (Immutable principle)
            lake_path = await DataLakeManager.save_raw_payload(self.source_name, raw_data)
            logger.info(f"Raw data saved to Data Lake: {lake_path}")
            
            return raw_data
        except Exception as e:
            logger.error(f"Failed to fetch data from World Bank: {e}")
            raise
            
    def normalize(self, raw_data: Any) -> Any:
        logger.info("Normalizing World Bank data into Pydantic Contracts...")
        return WorldBankNormalizer.normalize(raw_data, self.indicator_code)
        
    def validate(self, normalized_data: Any) -> bool:
        logger.info("Validating normalized dataset...")
        self.validated_data = EconomyValidator.validate_dataset(normalized_data)
        logger.info(f"Validation complete. Valid records: {len(self.validated_data)} / {len(normalized_data)}")
        return len(self.validated_data) > 0
        
    def transform(self, validated_data: Any) -> Any:
        # Pass-through for Phase 1. 
        # Feature engineering (e.g. YoY growth) can be added here later.
        return validated_data
        
    async def save(self, final_data: Any) -> None:
        logger.info(f"Saving {len(final_data)} records to Data Warehouse via Repository...")
        # Placeholder for Phase 1 execution
        # Example: await economy_repo.bulk_add(final_data)
        pass
        
    async def health_check(self) -> bool:
        try:
            url = f"{self.BASE_URL}/country?format=json&per_page=1"
            await asyncio.to_thread(self._fetch_sync, url)
            return True
        except Exception:
            return False
            
    def metadata(self) -> Dict[str, str]:
        return {
            "source": self.source_name,
            "version": "1.0",
            "description": "World Bank Macroeconomic Data Pipeline"
        }

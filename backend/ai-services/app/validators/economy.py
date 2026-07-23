from typing import List
from app.contracts.economy import EconomicIndicatorContract
import logging

logger = logging.getLogger(__name__)

class EconomyValidator:
    """
    Business logic validator for Economic Indicators to ensure data quality
    before inserting into the Data Warehouse.
    """
    
    @classmethod
    def validate_dataset(cls, records: List[EconomicIndicatorContract]) -> List[EconomicIndicatorContract]:
        """
        Takes a list of normalized records and returns only the valid ones.
        Logs any anomalies.
        """
        valid_records = []
        
        for record in records:
            if not cls._is_valid(record):
                logger.warning(f"Validation failed for record: {record.country_code} - {record.year} - {record.indicator_code}")
                continue
            valid_records.append(record)
            
        return valid_records
        
    @classmethod
    def _is_valid(cls, record: EconomicIndicatorContract) -> bool:
        # GDP cannot be negative
        if record.indicator_code == "GDP_USD" and record.value <= 0:
            return False
            
        # Population cannot be negative or fractional
        if record.indicator_code == "POPULATION" and (record.value < 0 or not record.value.is_integer()):
            return False
            
        # Inflation can be negative (deflation), but bounds checking (e.g., > 1000000% is likely data error unless hyperinflation)
        if record.indicator_code == "INFLATION_RATE" and record.value > 1000000:
            return False
            
        return True

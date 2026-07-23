from typing import List, Dict, Any
from app.contracts.economy import EconomicIndicatorContract

class WorldBankNormalizer:
    """
    Transforms raw World Bank JSON responses into the standardized EconomicIndicatorContract.
    """
    
    # Map World Bank indicator codes to internal standard codes
    INDICATOR_MAP = {
        "NY.GDP.MKTP.CD": "GDP_USD",
        "SP.POP.TOTL": "POPULATION",
        "FP.CPI.TOTL.ZG": "INFLATION_RATE"
    }
    
    @classmethod
    def normalize(cls, raw_data: List[Any], indicator_code: str) -> List[EconomicIndicatorContract]:
        """
        World Bank API typically returns a list where index 1 contains the actual data array.
        [
            {"page": 1, ...},
            [ {"country": {"id": "US", "value": "USA"}, "date": "2022", "value": 25460000000}, ... ]
        ]
        """
        normalized_records = []
        
        if not isinstance(raw_data, list) or len(raw_data) < 2:
            return normalized_records
            
        data_points = raw_data[1]
        if not data_points:
            return normalized_records
            
        internal_code = cls.INDICATOR_MAP.get(indicator_code, indicator_code)
        
        for item in data_points:
            value = item.get("value")
            # Skip records with no data
            if value is None:
                continue
                
            try:
                record = EconomicIndicatorContract(
                    country_code=item["country"]["id"],
                    year=int(item["date"]),
                    indicator_code=internal_code,
                    value=float(value),
                    source="WORLD_BANK"
                )
                normalized_records.append(record)
            except (ValueError, KeyError, TypeError):
                # We could log parsing errors here
                continue
                
        return normalized_records

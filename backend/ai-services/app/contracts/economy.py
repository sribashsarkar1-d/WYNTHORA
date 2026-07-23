from pydantic import Field, field_validator
from typing import Optional
from app.contracts.base import BaseContract

class EconomicIndicatorContract(BaseContract):
    """
    Standardized schema for all macroeconomic indicators (GDP, Inflation, etc.)
    regardless of whether the source is World Bank, FRED, or IMF.
    """
    country_code: str = Field(..., description="ISO-3 Country Code (e.g., USA, BGD)")
    year: int = Field(..., description="Year of the data point")
    indicator_code: str = Field(..., description="Standardized internal indicator code (e.g., GDP_USD, INFLATION_RATE)")
    value: float = Field(..., description="The actual economic value")
    source: str = Field(..., description="Source of the data (e.g., WORLD_BANK)")
    
    @field_validator("year")
    def validate_year(cls, v):
        if v < 1900 or v > 2100:
            raise ValueError(f"Year {v} is out of realistic bounds.")
        return v

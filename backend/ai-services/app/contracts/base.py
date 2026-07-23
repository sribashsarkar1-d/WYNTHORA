from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BaseContract(BaseModel):
    """
    Base Pydantic Contract for all API data validation.
    Enforces that we track source metadata.
    """
    dataset_version: Optional[str] = Field(default=None, description="Version of the dataset")
    schema_version: str = Field(default="1.0", description="Version of the schema")
    checksum: Optional[str] = Field(default=None, description="Data integrity checksum")
    retrieved_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Time data was fetched")

    class Config:
        from_attributes = True
        populate_by_name = True

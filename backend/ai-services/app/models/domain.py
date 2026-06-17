from pydantic import BaseModel
class SimulationResult(BaseModel):
    id: str
    confidence: float

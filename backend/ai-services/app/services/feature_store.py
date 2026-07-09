import logging
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.schema import EconomicTimeSeriesModel
from app.core.database import AsyncSessionLocal

logger = logging.getLogger("FeatureStore")

class FeatureStore:
    """
    Enterprise Feature Store for Machine Learning Pipeline.
    Aggregates database rows into fixed-size tensors (sequences) for LSTM and Transformers.
    """
    def __init__(self):
        self.sequence_length = 10 # Predict based on last 10 ticks/years
    
    async def get_macro_sequence(self, country_code: str = "USA") -> np.ndarray:
        """
        Fetches the last N time steps to form a sequence for the LSTM predictor.
        Sequence Features: [GDP, Inflation, Unemployment, Interest (Mocked), CO2 (Mocked)]
        """
        async with AsyncSessionLocal() as session:
            query = select(EconomicTimeSeriesModel).where(
                EconomicTimeSeriesModel.country_code == country_code
            ).order_by(EconomicTimeSeriesModel.year.desc()).limit(self.sequence_length)
            
            result = await session.execute(query)
            rows = result.scalars().all()
            
            # If we don't have enough data, pad with zeros (or mean imputation in prod)
            sequence = []
            for row in reversed(rows): # Reverse to get chronological order
                gdp = float(row.gdp_usd) if row.gdp_usd else 0.0 # type: ignore
                inf = float(row.inflation_rate) if row.inflation_rate else 0.0 # type: ignore
                unemp = float(row.unemployment_rate) if row.unemployment_rate else 0.0 # type: ignore
                
                # We mock interest and co2 since they aren't in this specific table yet
                interest = 0.05
                co2 = 412.0
                
                sequence.append([gdp, inf, unemp, interest, co2])
                
            # Padding
            while len(sequence) < self.sequence_length:
                sequence.insert(0, [0.0, 0.0, 0.0, 0.0, 0.0])
                
            return np.array(sequence)

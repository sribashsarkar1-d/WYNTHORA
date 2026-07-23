import asyncio
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SimulationStateStore:
    """
    Centralized, thread-safe (and async-safe) key-value store for Simulation state.
    Allows independent domains (Economy, Politics) to share macro variables safely.
    Future upgrade: Can be backed by Redis for multi-node distribution.
    """
    def __init__(self):
        self._state: Dict[str, Any] = {
            "global_gdp": 100000.0,
            "average_temperature": 15.0,
            "global_population": 8000000000,
            "active_crises": []
        }
        self._lock = asyncio.Lock()
        
    async def get(self, key: str, default: Any = None) -> Any:
        async with self._lock:
            return self._state.get(key, default)
            
    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            self._state[key] = value
            
    async def update(self, updates: Dict[str, Any]) -> None:
        async with self._lock:
            self._state.update(updates)
            
    async def get_all(self) -> Dict[str, Any]:
        async with self._lock:
            # Return a shallow copy to prevent external unsynchronized mutations
            return self._state.copy()

from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseAutonomousAgent(ABC):
    """
    Abstract interface for AI Agents participating in the World Simulation.
    Agents can represent Nation-States, Corporations, or Central Banks.
    They follow a Perceive -> Reason -> Act loop.
    """
    
    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
        self.memory = []
        
    @abstractmethod
    def perceive(self, world_state: Dict[str, Any]) -> None:
        """
        Reads the current state of the simulation (e.g., economy, geopolitics).
        Updates the agent's internal memory.
        """
        pass
        
    @abstractmethod
    def reason(self, context: str) -> str:
        """
        Uses an LLM or predefined policy to analyze the state and decide on the next move.
        Returns a string representation of the chosen strategy or thought process.
        """
        pass
        
    @abstractmethod
    def act(self) -> Dict[str, Any]:
        """
        Executes the action on the simulation engine (e.g., raise interest rates, declare embargo).
        Returns a dictionary representing the action payload.
        """
        pass

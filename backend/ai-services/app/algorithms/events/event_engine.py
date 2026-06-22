from abc import ABC, abstractmethod
import logging
from typing import Dict, Any

class GlobalEvent(ABC):
    """
    Abstract base class for all global events in the simulation.
    Events trigger cascading impacts across Economy, Politics, Society, and Markets.
    """
    def __init__(self, name: str, severity: float):
        self.name = name
        self.severity = severity  # Scale 1.0 to 10.0
        self.active = True
        self.logger = logging.getLogger(f"Event_{self.name.replace(' ', '')}")

    @abstractmethod
    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates the delta (changes) to apply to the global state based on this event.
        """
        pass

class WarEvent(GlobalEvent):
    def __init__(self, name: str, severity: float, regions_involved: list, conflict_type: str = "Generic"):
        super().__init__(name, severity)
        self.regions_involved = regions_involved
        self.conflict_type = conflict_type # e.g., "Russia-Ukraine", "China-Taiwan", "India-Pakistan"

    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.warning(f"WAR EVENT TRIGGERED: {self.name} ({self.conflict_type}, Severity {self.severity})")
        
        # Base impacts
        impact = {
            "manufacturing_output_modifier": -0.05 * self.severity,
            "market_volatility_modifier": +0.10 * self.severity,
            "geopolitical_tension_modifier": +0.20 * self.severity,
            "inflation_spike": +0.02 * self.severity,
            "oil_price_spike": +0.05 * self.severity,
            "trade_disruption": +0.10 * self.severity
        }
        
        # Specific conflict impacts
        if self.conflict_type == "Russia-Ukraine":
            # Massive oil/gas and agriculture (wheat) disruption
            impact["oil_price_spike"] += 0.15 * self.severity
            impact["agriculture_output_modifier"] = -0.12 * self.severity
            impact["inflation_spike"] += 0.08 * self.severity
            
        elif self.conflict_type == "China-Taiwan":
            # Massive technology (semiconductor) and global trade disruption
            impact["technology_output_modifier"] = -0.25 * self.severity
            impact["manufacturing_output_modifier"] -= 0.10 * self.severity
            impact["market_crash_probability"] = +0.40 * self.severity
            
        elif self.conflict_type == "India-Pakistan":
            # Regional instability, potential nuclear threat spikes volatility
            impact["market_volatility_modifier"] += 0.20 * self.severity
            impact["geopolitical_tension_modifier"] += 0.30 * self.severity

        return impact

class PandemicEvent(GlobalEvent):
    def __init__(self, name: str, severity: float):
        super().__init__(name, severity)

    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.warning(f"PANDEMIC EVENT TRIGGERED: {self.name} (Severity {self.severity})")
        # Pandemic heavily hits services and agriculture (labor shortage), crashes market drift
        impact = {
            "services_output_modifier": -0.08 * self.severity,
            "agriculture_output_modifier": -0.03 * self.severity,
            "market_drift_modifier": -0.05 * self.severity
        }
        return impact

class ClimateDisasterEvent(GlobalEvent):
    def __init__(self, name: str, severity: float, disaster_type: str = "Generic"):
        super().__init__(name, severity)
        self.disaster_type = disaster_type # Flood, Drought, Heatwave, Hurricane, Wildfire

    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.warning(f"CLIMATE DISASTER TRIGGERED: {self.name} ({self.disaster_type}, Severity {self.severity})")
        
        impact = {
            "co2_emissions_modifier": +0.02 * self.severity
        }
        
        if self.disaster_type == "Flood":
            impact["agriculture_output_modifier"] = -0.15 * self.severity
            impact["infrastructure_damage"] = 0.10 * self.severity
        elif self.disaster_type == "Drought":
            impact["agriculture_output_modifier"] = -0.25 * self.severity
            impact["inflation_spike"] = 0.05 * self.severity # Food inflation
        elif self.disaster_type == "Heatwave":
            impact["services_output_modifier"] = -0.05 * self.severity
            impact["energy_demand_spike"] = 0.10 * self.severity
        elif self.disaster_type == "Hurricane":
            impact["infrastructure_damage"] = 0.20 * self.severity
            impact["manufacturing_output_modifier"] = -0.10 * self.severity
            impact["trade_disruption"] = 0.15 * self.severity
        elif self.disaster_type == "Wildfire":
            impact["agriculture_output_modifier"] = -0.10 * self.severity
            impact["co2_emissions_modifier"] += 0.05 * self.severity # Massive extra CO2
            
        return impact

class EnergyCrisisEvent(GlobalEvent):
    def __init__(self, name: str, severity: float):
        super().__init__(name, severity)

    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.warning(f"ENERGY CRISIS TRIGGERED: {self.name} (Severity {self.severity})")
        # Energy crisis destroys manufacturing and spikes inflation
        impact = {
            "manufacturing_output_modifier": -0.15 * self.severity,
            "inflation_spike": +0.05 * self.severity
        }
        return impact

class EventEngine:
    """
    Manages active events and aggregates their impacts on the world state.
    """
    def __init__(self):
        self.active_events = []
        self.logger = logging.getLogger("EventEngine")

    def trigger_event(self, event: GlobalEvent):
        self.active_events.append(event)
        self.logger.info(f"Triggered new event: {event.name}")

    def resolve_events(self, event_names_to_resolve: list):
        for event in self.active_events:
            if event.name in event_names_to_resolve:
                event.active = False
        self.active_events = [e for e in self.active_events if e.active]

    def get_aggregated_impacts(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        aggregated_impact = {}
        for event in self.active_events:
            impacts = event.calculate_impact(global_state)
            for key, value in impacts.items():
                aggregated_impact[key] = aggregated_impact.get(key, 0.0) + value
        return aggregated_impact

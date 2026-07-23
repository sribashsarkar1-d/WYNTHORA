from abc import ABC, abstractmethod
import logging
from typing import Dict, Any, List
import random
import uuid

class GlobalEvent(ABC):
    """
    Abstract base class for all global events in the simulation.
    Events trigger cascading impacts across Economy, Politics, Society, and Markets.
    """
    def __init__(self, name: str, severity: float, probability: float = 1.0):
        self.id = str(uuid.uuid4())
        self.name = name
        self.severity = max(1.0, min(10.0, severity))  # Scale 1.0 to 10.0
        self.probability = probability
        self.active = True
        self.logger = logging.getLogger(f"Event_{self.name.replace(' ', '')}")

    @abstractmethod
    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates the delta (changes) to apply to the global state based on this event.
        """
        pass

    @abstractmethod
    def get_rollback_impact(self) -> Dict[str, Any]:
        """
        Calculates the reverse impact when the event resolves.
        """
        pass

class WarEvent(GlobalEvent):
    def __init__(self, name: str, severity: float, regions_involved: list, conflict_type: str = "Generic", probability: float = 1.0):
        super().__init__(name, severity, probability)
        self.regions_involved = regions_involved
        self.conflict_type = conflict_type

    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.warning(f"WAR EVENT TRIGGERED: {self.name} ({self.conflict_type}, Severity {self.severity})")
        impact = {
            "manufacturing_output_modifier": -0.05 * self.severity,
            "market_volatility_modifier": +0.10 * self.severity,
            "geopolitical_tension_modifier": +0.20 * self.severity,
            "inflation_spike": +0.02 * self.severity,
            "oil_price_spike": +0.05 * self.severity,
            "trade_disruption": +0.10 * self.severity
        }
        if self.conflict_type == "Russia-Ukraine":
            impact["oil_price_spike"] += 0.15 * self.severity
            impact["agriculture_output_modifier"] = -0.12 * self.severity
            impact["inflation_spike"] += 0.08 * self.severity
        elif self.conflict_type == "China-Taiwan":
            impact["technology_output_modifier"] = -0.25 * self.severity
            impact["manufacturing_output_modifier"] -= 0.10 * self.severity
            impact["market_crash_probability"] = +0.40 * self.severity
        elif self.conflict_type == "India-Pakistan":
            impact["market_volatility_modifier"] += 0.20 * self.severity
            impact["geopolitical_tension_modifier"] += 0.30 * self.severity
        return impact

    def get_rollback_impact(self) -> Dict[str, Any]:
        self.logger.info(f"WAR EVENT RESOLVED: {self.name}")
        impact = self.calculate_impact({})
        return {k: -v for k, v in impact.items() if "probability" not in k}

class PandemicEvent(GlobalEvent):
    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.warning(f"PANDEMIC EVENT TRIGGERED: {self.name} (Severity {self.severity})")
        return {
            "services_output_modifier": -0.08 * self.severity,
            "agriculture_output_modifier": -0.03 * self.severity,
            "market_drift_modifier": -0.05 * self.severity,
            "infection_rate_spike": +0.10 * self.severity
        }
        
    def get_rollback_impact(self) -> Dict[str, Any]:
        self.logger.info(f"PANDEMIC EVENT RESOLVED: {self.name}")
        return {
            "services_output_modifier": +0.08 * self.severity,
            "agriculture_output_modifier": +0.03 * self.severity,
            "market_drift_modifier": +0.05 * self.severity,
            "infection_rate_spike": -0.10 * self.severity
        }

class ClimateDisasterEvent(GlobalEvent):
    def __init__(self, name: str, severity: float, disaster_type: str = "Generic", probability: float = 1.0):
        super().__init__(name, severity, probability)
        self.disaster_type = disaster_type

    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.warning(f"CLIMATE DISASTER TRIGGERED: {self.name} ({self.disaster_type}, Severity {self.severity})")
        impact = {"co2_emissions_modifier": +0.02 * self.severity}
        
        if self.disaster_type == "Flood":
            impact["agriculture_output_modifier"] = -0.15 * self.severity
            impact["infrastructure_damage"] = 0.10 * self.severity
        elif self.disaster_type == "Drought":
            impact["agriculture_output_modifier"] = -0.25 * self.severity
            impact["inflation_spike"] = 0.05 * self.severity
        elif self.disaster_type == "Heatwave":
            impact["services_output_modifier"] = -0.05 * self.severity
            impact["energy_demand_spike"] = 0.10 * self.severity
        elif self.disaster_type == "Hurricane":
            impact["infrastructure_damage"] = 0.20 * self.severity
            impact["manufacturing_output_modifier"] = -0.10 * self.severity
            impact["trade_disruption"] = 0.15 * self.severity
        elif self.disaster_type == "Wildfire":
            impact["agriculture_output_modifier"] = -0.10 * self.severity
            impact["co2_emissions_modifier"] += 0.05 * self.severity
        return impact

    def get_rollback_impact(self) -> Dict[str, Any]:
        self.logger.info(f"CLIMATE DISASTER RESOLVED: {self.name}")
        impact = self.calculate_impact({})
        # Rollback temporary modifiers, but leave permanent ones (like infrastructure damage)
        rollback = {k: -v for k, v in impact.items() if "damage" not in k and "co2" not in k}
        return rollback

class EnergyCrisisEvent(GlobalEvent):
    def calculate_impact(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.warning(f"ENERGY CRISIS TRIGGERED: {self.name} (Severity {self.severity})")
        return {
            "manufacturing_output_modifier": -0.15 * self.severity,
            "inflation_spike": +0.05 * self.severity
        }
        
    def get_rollback_impact(self) -> Dict[str, Any]:
        self.logger.info(f"ENERGY CRISIS RESOLVED: {self.name}")
        return {
            "manufacturing_output_modifier": +0.15 * self.severity,
            "inflation_spike": -0.05 * self.severity
        }

class EventEngine:
    """
    Manages active events and aggregates their impacts on the world state.
    Provides automated rollback for resolved events.
    """
    def __init__(self):
        self.active_events: List[GlobalEvent] = []
        self.resolved_events: List[GlobalEvent] = []
        self.logger = logging.getLogger("EventEngine")

    def trigger_event(self, event: GlobalEvent):
        # Determine if the event actually fires based on its probability
        if random.random() <= event.probability:
            self.active_events.append(event)
            self.logger.info(f"Triggered new event: {event.name} (Severity {event.severity})")
        else:
            self.logger.info(f"Event {event.name} failed probability check and was not triggered.")

    def resolve_events(self, event_names_to_resolve: list) -> Dict[str, Any]:
        """
        Resolves events and returns the aggregated rollback impacts.
        """
        rollback_impacts = {}
        for event in self.active_events:
            if event.name in event_names_to_resolve:
                event.active = False
                self.resolved_events.append(event)
                # Calculate rollback
                evt_rollback = event.get_rollback_impact()
                for key, value in evt_rollback.items():
                    rollback_impacts[key] = rollback_impacts.get(key, 0.0) + value
                    
        self.active_events = [e for e in self.active_events if e.active]
        return rollback_impacts

    def get_aggregated_impacts(self, global_state: Dict[str, Any]) -> Dict[str, Any]:
        aggregated_impact = {}
        for event in self.active_events:
            impacts = event.calculate_impact(global_state)
            for key, value in impacts.items():
                aggregated_impact[key] = aggregated_impact.get(key, 0.0) + value
        return aggregated_impact

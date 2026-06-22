import networkx as nx
from typing import Dict, Any
import logging

class SupplyChainEngine:
    """
    Simulates global supply chain logistics: Ports, Shipping Routes, Factories.
    Uses a graph representation to model bottlenecks and propagation of shocks.
    """
    def __init__(self):
        self.logger = logging.getLogger("SupplyChainEngine")
        self.network = nx.DiGraph()
        self._initialize_base_network()
        
    def _initialize_base_network(self):
        """
        Creates a simplified base network of major global supply chain nodes.
        """
        # Add major factory hubs
        factories = ["EastAsia_Mfg", "SouthAsia_Mfg", "Europe_Mfg", "NorthAmerica_Mfg"]
        for f in factories:
            self.network.add_node(f, type="factory", capacity=100.0, current_output=100.0, backlog=0.0)
            
        # Add major ports
        ports = ["Shanghai_Port", "Singapore_Port", "Rotterdam_Port", "LA_Port"]
        for p in ports:
            self.network.add_node(p, type="port", capacity=200.0, throughput=180.0, congestion=0.0)
            
        # Add edges (shipping routes)
        self.network.add_edge("EastAsia_Mfg", "Shanghai_Port", capacity=100.0)
        self.network.add_edge("SouthAsia_Mfg", "Singapore_Port", capacity=80.0)
        self.network.add_edge("Europe_Mfg", "Rotterdam_Port", capacity=90.0)
        self.network.add_edge("NorthAmerica_Mfg", "LA_Port", capacity=90.0)
        
        # Inter-port transcontinental routes
        self.network.add_edge("Shanghai_Port", "LA_Port", capacity=150.0, cost=1.0)
        self.network.add_edge("Shanghai_Port", "Rotterdam_Port", capacity=120.0, cost=1.2)
        self.network.add_edge("Singapore_Port", "Rotterdam_Port", capacity=100.0, cost=1.1)
        self.network.add_edge("Rotterdam_Port", "LA_Port", capacity=80.0, cost=0.8)
        
        # Add Air Cargo Hubs
        air_hubs = ["HongKong_Air", "Frankfurt_Air", "Memphis_Air"]
        for a in air_hubs:
            self.network.add_node(a, type="air_cargo", capacity=50.0, throughput=45.0, congestion=0.0)
            
        # Add Rail Networks
        rail_hubs = ["TransSiberian_Rail", "US_Freight_Rail", "Euro_Rail"]
        for r in rail_hubs:
            self.network.add_node(r, type="rail", capacity=80.0, throughput=75.0, congestion=0.0)

    def apply_shock(self, target_node: str, severity: float):
        """
        Applies a localized shock (e.g., strike, pandemic closure, war blockade)
        Severity is 0.0 to 1.0 (1.0 = total closure).
        """
        if target_node in self.network:
            node = self.network.nodes[target_node]
            if node["type"] == "port":
                node["throughput"] *= (1.0 - severity)
                node["congestion"] += severity
            elif node["type"] == "factory":
                node["current_output"] *= (1.0 - severity)
                node["backlog"] += (node["capacity"] - node["current_output"])

    def step(self, global_demand_factor: float) -> Dict[str, Any]:
        """
        Advance the supply chain simulation.
        """
        bottlenecks = []
        total_output = 0.0
        
        # 1. Update Factories
        for node, data in self.network.nodes(data=True):
            if data["type"] == "factory":
                # Try to clear backlog if output is recovering
                recovery_rate = 0.1
                data["current_output"] = min(data["capacity"], data["current_output"] + (data["capacity"] * recovery_rate))
                
                # Production depends on global demand
                actual_production = data["current_output"] * global_demand_factor
                total_output += actual_production
                
                # Check for factory bottlenecks
                if data["current_output"] < data["capacity"] * 0.5:
                    bottlenecks.append(node)
                    
            elif data["type"] in ["port", "air_cargo", "rail"]:
                # Logistics slowly recover from congestion
                if data["congestion"] > 0:
                    data["congestion"] = max(0.0, data["congestion"] - 0.05)
                    data["throughput"] = data["capacity"] * (1.0 - data["congestion"])
                
                # Check for bottlenecks
                if data["congestion"] > 0.5:
                    bottlenecks.append(node)
                    
        # 2. Network Flow logic (discrete layers)
        ports = [d["congestion"] for n, d in self.network.nodes(data=True) if d["type"]=="port"]
        airs = [d["congestion"] for n, d in self.network.nodes(data=True) if d["type"]=="air_cargo"]
        rails = [d["congestion"] for n, d in self.network.nodes(data=True) if d["type"]=="rail"]
        
        avg_port_congestion = sum(ports) / len(ports) if ports else 0.0
        avg_air_congestion = sum(airs) / len(airs) if airs else 0.0
        avg_rail_congestion = sum(rails) / len(rails) if rails else 0.0
        
        supply_health = 1.0 - ((avg_port_congestion + avg_air_congestion + avg_rail_congestion) / 3.0)
        
        return {
            "supply_chain_health": supply_health,
            "total_factory_output": total_output,
            "active_bottlenecks": bottlenecks,
            "port_health": 1.0 - avg_port_congestion,
            "air_health": 1.0 - avg_air_congestion,
            "rail_health": 1.0 - avg_rail_congestion
        }

if __name__ == "__main__":
    sc = SupplyChainEngine()
    print("Initial step:", sc.step(1.0))
    sc.apply_shock("Shanghai_Port", 0.8) # Massive closure
    print("After shock:", sc.step(1.0))

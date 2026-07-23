from .pathfinding import AStarPathfinder
from .cellular import CellularAutomata
from typing import Any

class WorldEnvironment:
    """
    The Grid World that holds agents and spatial algorithms.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents = []
        
        # 5. Cellular Automata for environment effects (e.g., pandemic, pollution)
        self.cellular = CellularAutomata(width, height)
        # Seed an infection
        self.cellular.set_state(width//2, height//2, 1.0)
        
        # 6. A* Pathfinding map
        obstacles = [(2, 2), (2, 3), (2, 4)]
        self.pathfinder = AStarPathfinder(width, height, obstacles)
        
        # 7. Global State (influenced by Politics module)
        self.global_tax_rate = 0.35

    def add_agent(self, agent):
        self.agents.append(agent)

    async def tick(self, state_store: Any = None) -> None:
        """
        Advances the simulation by one step asynchronously.
        """
        import asyncio
        
        # Read from state_store if provided
        if state_store:
            self.global_tax_rate = await state_store.get("global_tax_rate", 0.35)
            # If average temp is too high, increase infection spread
            avg_temp = await state_store.get("average_temperature", 15.0)
            spread_modifier = 0.2 + (max(0, avg_temp - 15.0) * 0.01)
        else:
            spread_modifier = 0.2
            
        def process_agents():
            # Step Cellular Automata
            self.cellular.step(spread_rate=spread_modifier, decay_rate=0.05)
            
            # Step Agents
            for agent in self.agents:
                agent.step()
                
                # Agents can check cellular state
                infection_risk = self.cellular.get_state(agent.x, agent.y)
                if infection_risk > 0.5:
                    # Agent uses A* to run away to origin
                    path = self.pathfinder.find_path((agent.x, agent.y), (0, 0))
                    if path and len(path) > 0:
                        agent.x, agent.y = path[0] # Move one step
                        
        # Run CPU-bound pathfinding and agent steps in a separate thread
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, process_agents)
        
        # Write back any relevant metrics to state store
        if state_store:
            await state_store.update({
                "abm_active_agents": len(self.agents)
            })

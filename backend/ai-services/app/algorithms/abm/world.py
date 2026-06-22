from pathfinding import AStarPathfinder
from cellular import CellularAutomata

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

    def tick(self):
        """
        Advances the simulation by one step.
        """
        # Step Cellular Automata
        self.cellular.step(spread_rate=0.2, decay_rate=0.05)
        
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

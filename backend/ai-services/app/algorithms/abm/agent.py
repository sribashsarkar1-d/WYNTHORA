from algorithms.abm.fsm import FiniteStateMachine, State
from algorithms.abm.bandit import UCBBandit
from algorithms.abm.utility import CobbDouglasUtility
from algorithms.abm.decision_tree import build_protest_tree

class IdleState(State):
    def __init__(self):
        super().__init__("IDLE")
    def update(self, agent):
        # Look for a job
        job_sector = agent.bandit.select_arm()
        agent.current_job = job_sector
        print(f"Agent {agent.id} chose sector {job_sector} using UCB.")

class WorkingState(State):
    def __init__(self):
        super().__init__("WORKING")
    def update(self, agent):
        # Earn money based on 9 sectors
        sector_rewards = {
            "Technology": 120,
            "Healthcare": 110,
            "Defense": 105,
            "Energy": 95,
            "Government": 90,
            "Manufacturing": 85,
            "Education": 80,
            "Services": 70,
            "Agriculture": 60
        }
        
        # Add some random variance to the reward
        import random
        base_reward = sector_rewards.get(agent.current_job, 50)
        variance = random.uniform(-0.1, 0.2)
        reward = base_reward * (1 + variance)
        
        agent.wealth += reward
        agent.bandit.update(agent.current_job, reward)
        print(f"Agent {agent.id} worked in {agent.current_job} and earned ${reward:.2f}. Total wealth: ${agent.wealth:.2f}")

class VirtualCitizen:
    """
    The core Agent that ties all 6 algorithms together.
    """
    def __init__(self, agent_id, x, y, world):
        self.id = agent_id
        self.x = x
        self.y = y
        self.world = world
        self.wealth = 100.0
        self.current_job = None
        
        # 1. Multi-Armed Bandit for Job Selection (9 Sectors)
        sectors = [
            "Agriculture", "Manufacturing", "Technology", "Energy", 
            "Healthcare", "Services", "Government", "Defense", "Education"
        ]
        self.bandit = UCBBandit(sectors)
        
        # Inject random noise into initial Q-values so agents distribute uniquely
        import random
        for sector in sectors:
            self.bandit.values[sector] = random.uniform(50.0, 150.0)
            self.bandit.counts[sector] = 1 # Force UCB to use values instead of exploring first sector
        self.bandit.total_pulls = len(sectors)
        
        # 2. Utility Maximization for Consumption
        self.utility_model = CobbDouglasUtility(A=1.0)
        self.utility_model.set_preference("Food", 0.6)
        self.utility_model.set_preference("Entertainment", 0.4)
        
        # 3. Decision Tree for complex logic (e.g., protesting)
        self.decision_tree = build_protest_tree()
        
        # 4. Finite State Machine for lifecycle
        self.fsm = FiniteStateMachine()
        self.fsm.add_state(IdleState())
        self.fsm.add_state(WorkingState())
        
        # Transitions
        self.fsm.add_transition("IDLE", "WORKING", lambda a: a.current_job is not None)
        self.fsm.add_transition("WORKING", "IDLE", lambda a: a.wealth > 500) # Stop working if rich
        
        self.fsm.set_initial_state("IDLE", self)

    def step(self):
        # Update FSM state (might work, might go idle)
        self.fsm.update(self)
        
        # Utility Maximization: Decide what to buy
        prices = {"Food": 10.0, "Entertainment": 20.0}
        optimal_basket = self.utility_model.optimal_basket(self.wealth * 0.5, prices) # Spend half wealth
        
        # Decision Tree: Should protest?
        world_tax_rate = getattr(self.world, 'global_tax_rate', 0.35)
        attributes = {"wealth": self.wealth, "tax_rate": world_tax_rate} # Use dynamic world tax rate
        action = self.decision_tree.predict(attributes)
        if action == "PROTEST":
            print(f"Agent {self.id} is PROTESTING due to high taxes and low wealth!")

        # Move randomly for now, or use A* if given a goal
        # (A* logic is handled by calling self.world.pathfinder.find_path)

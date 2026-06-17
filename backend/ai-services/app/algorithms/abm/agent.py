from fsm import FiniteStateMachine, State
from bandit import UCBBandit
from utility import CobbDouglasUtility
from decision_tree import build_protest_tree

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
        # Earn money
        reward = 100 if agent.current_job == "Tech" else 50
        agent.wealth += reward
        agent.bandit.update(agent.current_job, reward)
        print(f"Agent {agent.id} worked in {agent.current_job} and earned ${reward}. Total wealth: ${agent.wealth}")

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
        
        # 1. Multi-Armed Bandit for Job Selection
        self.bandit = UCBBandit(["Tech", "Agriculture", "Services"])
        
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
        attributes = {"wealth": self.wealth, "tax_rate": 0.35} # World tax rate
        action = self.decision_tree.predict(attributes)
        if action == "PROTEST":
            print(f"Agent {self.id} is PROTESTING due to high taxes and low wealth!")

        # Move randomly for now, or use A* if given a goal
        # (A* logic is handled by calling self.world.pathfinder.find_path)

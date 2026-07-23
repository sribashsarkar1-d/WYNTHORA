class State:
    def __init__(self, name):
        self.name = name

    def on_enter(self, agent):
        pass

    def on_exit(self, agent):
        pass

    def update(self, agent):
        # Override to define behavior during this state
        pass

class FiniteStateMachine:
    """
    Manages the lifecycle states of an agent.
    """
    def __init__(self):
        self.states = {}
        self.transitions = {} # Format: { from_state_name: [ (condition_func, to_state_name) ] }
        self.current_state = None

    def add_state(self, state: State):
        self.states[state.name] = state
        self.transitions[state.name] = []

    def add_transition(self, from_state_name, to_state_name, condition_func):
        if from_state_name in self.states and to_state_name in self.states:
            self.transitions[from_state_name].append((condition_func, to_state_name))

    def set_initial_state(self, state_name, agent):
        if state_name in self.states:
            self.current_state = self.states[state_name]
            self.current_state.on_enter(agent)

    def update(self, agent):
        if not self.current_state:
            return

        # Check for transitions
        state_name = self.current_state.name
        for condition_func, to_state_name in self.transitions[state_name]:
            if condition_func(agent):
                self.current_state.on_exit(agent)
                self.current_state = self.states[to_state_name]
                self.current_state.on_enter(agent)
                break # Only transition once per tick

        # Run current state behavior
        if self.current_state:
            self.current_state.update(agent)

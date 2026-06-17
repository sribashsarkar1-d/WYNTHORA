try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class ActorCritic(nn.Module if TORCH_AVAILABLE else object):
    """
    Architecture for Proximal Policy Optimization (PPO) and Soft Actor-Critic (SAC).
    """
    def __init__(self, state_dim=4, action_dim=2):
        if not TORCH_AVAILABLE:
            return
        super(ActorCritic, self).__init__()
        
        # Actor Network (Policy)
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim),
            nn.Softmax(dim=-1)
        )
        
        # Critic Network (Value)
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, state):
        if not TORCH_AVAILABLE:
            # Fallback for compilation if Torch is missing
            return [0.5, 0.5], 0.0
            
        action_probs = self.actor(state)
        state_value = self.critic(state)
        return action_probs, state_value

    def get_weights(self):
        if not TORCH_AVAILABLE: return {"mock_weight": 1.0}
        return self.state_dict()

    def set_weights(self, weights):
        if not TORCH_AVAILABLE: return
        self.load_state_dict(weights)

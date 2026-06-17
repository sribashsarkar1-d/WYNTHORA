import numpy as np
import torch
from graph_sage import SimpleGraphSAGE
from pagerank import calculate_pagerank
from bbn import setup_geopolitics_bbn
from mdp import MarkovDecisionProcess
from hmm import HiddenMarkovModel

class GeopoliticsModel:
    """
    Integrates GNN, PageRank, MDP, HMM, and BBN to manage global alliances and supply chains.
    """
    def __init__(self):
        self.countries = ["USA", "China", "EU", "Russia", "India"]
        self.num_countries = len(self.countries)
        
        # 1. PageRank (Trade Matrix: rows=from, cols=to)
        # Represents volume of trade exports
        self.trade_matrix = np.array([
            [0.0, 0.2, 0.4, 0.1, 0.3], # USA
            [0.4, 0.0, 0.3, 0.2, 0.1], # China
            [0.3, 0.3, 0.0, 0.2, 0.2], # EU
            [0.1, 0.4, 0.3, 0.0, 0.2], # Russia
            [0.2, 0.1, 0.2, 0.5, 0.0]  # India
        ])
        
        # 2. GNN / GraphSAGE (Alliance Network)
        # Node Features: [GDP, Military_Power]
        self.node_features = torch.tensor([
            [25.0, 10.0], # USA
            [18.0, 8.0],  # China
            [17.0, 5.0],  # EU
            [2.0,  7.0],  # Russia
            [3.5,  4.0]   # India
        ], dtype=torch.float32)
        
        # Adjacency Matrix (1 = Allied, 0 = Not)
        self.alliance_matrix = torch.tensor([
            [1.0, 0.0, 1.0, 0.0, 1.0],
            [0.0, 1.0, 0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 1.0, 1.0],
            [1.0, 0.0, 0.0, 1.0, 1.0]
        ], dtype=torch.float32)
        
        # In=2, Hidden=4, Out=2
        self.gnn = SimpleGraphSAGE(2, 4, 2)
        
        # 3. BBN
        self.bbn = setup_geopolitics_bbn()
        
        # 4. HMM (Guessing if a country is preparing for war)
        self.hmm = HiddenMarkovModel(
            states=['PEACE', 'WAR_PREP'],
            observations=['Trade_Normal', 'Sanctions_Imposed', 'Military_Drill'],
            start_prob={'PEACE': 0.8, 'WAR_PREP': 0.2},
            trans_prob={
                'PEACE': {'PEACE': 0.9, 'WAR_PREP': 0.1},
                'WAR_PREP': {'PEACE': 0.2, 'WAR_PREP': 0.8}
            },
            emit_prob={
                'PEACE': {'Trade_Normal': 0.8, 'Sanctions_Imposed': 0.1, 'Military_Drill': 0.1},
                'WAR_PREP': {'Trade_Normal': 0.1, 'Sanctions_Imposed': 0.4, 'Military_Drill': 0.5}
            }
        )
        
        # 5. MDP (AI Leader Strategy)
        states = ['PEACE', 'TENSION']
        actions = ['DIPLOMACY', 'BUILD_ARMS']
        trans = {
            'PEACE': {
                'DIPLOMACY': {'PEACE': 0.9, 'TENSION': 0.1},
                'BUILD_ARMS': {'PEACE': 0.5, 'TENSION': 0.5}
            },
            'TENSION': {
                'DIPLOMACY': {'PEACE': 0.4, 'TENSION': 0.6},
                'BUILD_ARMS': {'PEACE': 0.1, 'TENSION': 0.9}
            }
        }
        rewards = {
            'PEACE': {'DIPLOMACY': 10, 'BUILD_ARMS': -5},
            'TENSION': {'DIPLOMACY': 5, 'BUILD_ARMS': 2}
        }
        self.mdp = MarkovDecisionProcess(states, actions, trans, rewards)
        self.mdp.value_iteration()

    def run_analysis(self):
        print("=== GEOPOLITICS MODEL ANALYSIS ===")
        
        # PageRank (Trade Hubs)
        ranks = calculate_pagerank(self.trade_matrix)
        top_hub = self.countries[np.argmax(ranks)]
        print(f"\n1. Global Trade Hub (PageRank): {top_hub} (Score: {np.max(ranks):.3f})")
        
        # GNN Embeddings
        with torch.no_grad():
            embeddings = self.gnn(self.node_features, self.alliance_matrix)
            print(f"\n2. GNN Generated Alliance Embeddings:\n{embeddings.numpy()}")
            
        # BBN Probability
        prob_recession = self.bbn.query_probability("Global_Recession", (True, True))
        print(f"\n3. BBN: Prob. of Global Recession given Oil Crash AND Sanctions: {prob_recession*100}%")
        
        # MDP Optimal Strategy
        policy = self.mdp.get_optimal_policy()
        print(f"\n4. MDP Leader Strategy: If PEACE -> {policy['PEACE']}, If TENSION -> {policy['TENSION']}")
        
        # HMM Secret Inference
        obs_seq = ['Trade_Normal', 'Military_Drill', 'Military_Drill']
        _, hidden_states = self.hmm.viterbi(obs_seq)
        print(f"\n5. HMM Inference: Based on observations {obs_seq}, the country's hidden states were: {hidden_states}")

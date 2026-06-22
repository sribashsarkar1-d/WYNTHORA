import numpy as np
import torch
from algorithms.gnn.graph_sage import SimpleGraphSAGE
from algorithms.gnn.pagerank import calculate_pagerank
from algorithms.gnn.bbn import setup_geopolitics_bbn
from algorithms.gnn.mdp import MarkovDecisionProcess
from algorithms.gnn.hmm import HiddenMarkovModel

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from algorithms.data_loader import RealWorldDataLoader
class GeopoliticsModel:
    """
    Integrates GNN, PageRank, MDP, HMM, and BBN to manage global alliances and supply chains.
    """
    def __init__(self):
        self.countries = ["USA", "China", "EU", "Russia", "India"]
        self.num_countries = len(self.countries)
        
        # 1. PageRank (Trade Matrix: rows=from, cols=to)
        # Represents volume of trade exports
        self.data_loader = RealWorldDataLoader()
        self.trade_matrix = self.data_loader.get_global_trade_matrix()
        
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

    def run_analysis(self, active_events=None, global_gdp=None):
        if active_events is None:
            active_events = []
            
        print("=== GEOPOLITICS MODEL ANALYSIS ===")
        
        # 1. Determine dynamic states from the simulation's active events
        has_oil_crash = any(e.__class__.__name__ == 'EnergyCrisisEvent' for e in active_events)
        has_sanctions = any(e.__class__.__name__ == 'WarEvent' for e in active_events)
        has_war = any(e.__class__.__name__ == 'WarEvent' for e in active_events)
        
        # PageRank (Trade Hubs)
        ranks = calculate_pagerank(self.trade_matrix)
        top_hub = self.countries[np.argmax(ranks)]
        print(f"\n1. Global Trade Hub (PageRank): {top_hub} (Score: {np.max(ranks):.3f})")
        
        # Dynamically update alliance matrix (e.g. isolate Russia during war)
        if has_war:
            self.alliance_matrix[3, :] = 0.0 # Isolate Russia
            self.alliance_matrix[:, 3] = 0.0
            
        # GNN Embeddings (Dynamically scaled by global economic health)
        if global_gdp is not None:
            gdp_multiplier = max(0.5, min(1.5, global_gdp / 300000.0))
            current_features = self.node_features * gdp_multiplier
        else:
            current_features = self.node_features
            
        with torch.no_grad():
            embeddings = self.gnn(current_features, self.alliance_matrix)
            print(f"\n2. GNN Generated Alliance Embeddings:\n{embeddings.numpy()}")
            
        # BBN Probability using dynamic simulation state
        prob_recession = self.bbn.query_probability("Global_Recession", (has_oil_crash, has_sanctions))
        print(f"\n3. BBN: Prob. of Global Recession given Oil Crash={has_oil_crash} AND Sanctions={has_sanctions}: {prob_recession*100}%")
        
        # MDP Dynamic Policy Optimization
        for state in self.mdp.R:
            if has_war:
                self.mdp.R[state]['ATTACK'] = 10.0 # Reward aggression during war
                self.mdp.R[state]['DIPLOMACY'] = -5.0 # Penalize diplomacy
            else:
                self.mdp.R[state]['ATTACK'] = -10.0 # Penalize aggression in peace
                self.mdp.R[state]['DIPLOMACY'] = 10.0 # Reward peace
                
        self.mdp.value_iteration()
        policy = self.mdp.get_optimal_policy()
        print(f"\n4. MDP Leader Strategy: If PEACE -> {policy['PEACE']}, If TENSION -> {policy['TENSION']}")
        
        # HMM Secret Inference using dynamic observation sequence
        obs_seq = []
        for _ in range(3):
            if has_war:
                obs_seq.append(np.random.choice(['Military_Drill', 'Sanctions_Imposed']))
            else:
                obs_seq.append('Trade_Normal')
                
        _, hidden_states = self.hmm.viterbi(obs_seq)
        print(f"\n5. HMM Inference: Based on dynamic observations {obs_seq}, the country's hidden states were: {hidden_states}")

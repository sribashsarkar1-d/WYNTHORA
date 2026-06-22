import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv # type: ignore
import logging

class TemporalGNN(torch.nn.Module):
    """
    Temporal Graph Neural Network for predicting dynamic geopolitical alliances and conflict risks.
    Replaces the static matrix and placeholder GraphSAGE with real structural modeling.
    """
    def __init__(self, num_node_features: int, hidden_channels: int, num_classes: int):
        super(TemporalGNN, self).__init__()
        self.logger = logging.getLogger("Temporal_GNN")
        
        self.conv1 = GCNConv(num_node_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.out = torch.nn.Linear(hidden_channels, num_classes)
        
    def forward(self, x, edge_index, edge_weight=None):
        """
        x: Node features (e.g. GDP, Military Power, Population)
        edge_index: Graph connectivity (Trade routes, Alliances)
        edge_weight: Strength of connection (Trade volume, Diplomatic sentiment)
        """
        # First Graph Convolutional layer
        x = self.conv1(x, edge_index, edge_weight)
        x = F.relu(x)
        x = F.dropout(x, p=0.2, training=self.training)
        
        # Second Graph Convolutional layer
        x = self.conv2(x, edge_index, edge_weight)
        x = F.relu(x)
        
        # Output prediction for each node (e.g. Probability of entering conflict)
        out = self.out(x)
        return torch.sigmoid(out)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Dummy test to ensure architecture works with 195 nodes
    num_nodes = 195
    # 195 countries, 3 features each (GDP, Mil, Pop)
    x = torch.rand((num_nodes, 3)) 
    
    # Create a random graph (e.g., 500 trade edges between 195 countries)
    edge_index = torch.randint(0, num_nodes, (2, 500))
    edge_weight = torch.rand((500,))
    
    model = TemporalGNN(num_node_features=3, hidden_channels=8, num_classes=1)
    
    predictions = model(x, edge_index, edge_weight)
    print(f"Conflict Risk Predictions per Country shape: {predictions.shape}")
    print("Top 5 Riskiest Nations:")
    scores = predictions.detach().numpy().flatten()
    top_5 = scores.argsort()[-5:][::-1]
    for idx in top_5:
        print(f"Node {idx}: Risk {scores[idx]:.4f}")

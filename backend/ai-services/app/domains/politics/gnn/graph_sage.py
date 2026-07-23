import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleGraphSAGE(nn.Module):
    """
    A lightweight Graph Neural Network (similar to GraphSAGE/GCN).
    Used to generate 'embeddings' for countries based on their alliances.
    Countries that share similar allies will end up with similar embedding vectors.
    """
    def __init__(self, in_features, hidden_features, out_features):
        super(SimpleGraphSAGE, self).__init__()
        # Linear layer to transform node features
        self.W1 = nn.Linear(in_features, hidden_features)
        # Linear layer to transform aggregated neighbor features
        self.W2 = nn.Linear(hidden_features, out_features)

    def forward(self, node_features, adjacency_matrix):
        """
        :param node_features: Tensor of shape (num_nodes, in_features)
        :param adjacency_matrix: Tensor of shape (num_nodes, num_nodes)
        :return: Node embeddings of shape (num_nodes, out_features)
        """
        # Step 1: Transform features
        h = F.relu(self.W1(node_features))
        
        # Step 2: Message Passing (Aggregate neighbor features)
        # Multiply adjacency matrix by feature matrix to sum neighbor features
        # Adding Identity matrix (self-loops) so node keeps its own features too
        I = torch.eye(adjacency_matrix.size(0))
        A_hat = adjacency_matrix + I
        
        # Normalize adjacency (simple row normalization)
        row_sum = A_hat.sum(dim=1, keepdim=True)
        A_norm = A_hat / row_sum
        
        neighbor_aggr = torch.matmul(A_norm, h)
        
        # Step 3: Final transformation
        embeddings = self.W2(neighbor_aggr)
        return embeddings

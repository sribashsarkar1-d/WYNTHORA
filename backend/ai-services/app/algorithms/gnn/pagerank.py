import numpy as np

def calculate_pagerank(adjacency_matrix, d=0.85, max_iterations=100, tol=1.0e-6):
    """
    Calculates the PageRank of nodes in a graph.
    Used for finding the most critical hubs in the Global Trade Supply Chain.
    
    :param adjacency_matrix: 2D numpy array (num_nodes, num_nodes) representing directed links (trade flows).
    :param d: Damping factor (probability of continuing to follow links).
    :return: 1D numpy array of PageRank scores.
    """
    num_nodes = adjacency_matrix.shape[0]
    
    # Normalize outgoing links (columns sum to 1)
    # If a column sum is 0, we avoid division by zero
    col_sums = adjacency_matrix.sum(axis=0)
    col_sums[col_sums == 0] = 1.0 
    M = adjacency_matrix / col_sums
    
    # Initialize ranks equally
    v = np.ones(num_nodes) / num_nodes
    
    for i in range(max_iterations):
        # PageRank formula: v_new = (1-d)/N + d * M * v
        v_new = ((1 - d) / num_nodes) + d * np.dot(M, v)
        
        # Check convergence
        if np.linalg.norm(v_new - v, ord=1) < tol:
            break
        v = v_new
        
    return v

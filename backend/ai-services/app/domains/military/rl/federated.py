try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class FederatedAveraging:
    """
    Federated Averaging (FedAvg) Algorithm.
    Allows multiple decentralized AI agents to train locally and securely merge their
    "impact gradients" without sharing raw, sensitive data.
    """
    def aggregate_weights(self, global_weights, local_weights_list, learning_rate=1.0):
        """
        Averages the weights of local models to update the global model.
        """
        if not TORCH_AVAILABLE or not local_weights_list:
            return global_weights
            
        num_models = len(local_weights_list)
        aggregated_weights = {}

        # Initialize with zeros
        for key in global_weights.keys():
            aggregated_weights[key] = torch.zeros_like(global_weights[key])

        # Sum up local weights
        for local_weights in local_weights_list:
            for key in local_weights.keys():
                aggregated_weights[key] += local_weights[key]

        # Average and apply learning rate
        for key in aggregated_weights.keys():
            aggregated_weights[key] = aggregated_weights[key] / num_models
            # Apply update: W_global = W_global + lr * (W_avg - W_global)
            global_weights[key] = global_weights[key] + learning_rate * (aggregated_weights[key] - global_weights[key])

        return global_weights

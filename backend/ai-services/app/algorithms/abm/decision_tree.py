from typing import Optional, Dict, Any

class DecisionNode:
    """
    Lightweight Decision Tree Node for categorical/threshold choices.
    Allows agents to evaluate complex conditions rapidly.
    """
    def __init__(self, 
                 feature: Optional[str] = None, 
                 threshold: Optional[float] = None, 
                 left: Optional['DecisionNode'] = None, 
                 right: Optional['DecisionNode'] = None, 
                 *, 
                 value: Optional[str] = None):
        self.feature = feature       # String key of the attribute to check (e.g., "wealth")
        self.threshold = threshold   # Float or categorical value to split on
        self.left = left             # DecisionNode for True branch
        self.right = right           # DecisionNode for False branch
        self.value = value           # If leaf node, this is the final decision/action

    def is_leaf(self) -> bool:
        return self.value is not None

class DecisionTree:
    """
    Wrapper for a tree of DecisionNodes.
    """
    def __init__(self, root: DecisionNode):
        self.root = root

    def predict(self, agent_attributes: Dict[str, Any]) -> str:
        """
        Traverses the tree based on the agent's attributes dictionary.
        Returns the predicted action/value.
        """
        current_node: Optional[DecisionNode] = self.root
        
        while current_node is not None and not current_node.is_leaf():
            feature_key = current_node.feature
            if feature_key is None:
                # Safety fallback for malformed nodes
                current_node = current_node.right
                continue
                
            feature_val = agent_attributes.get(feature_key, 0)
            
            # Simple threshold split (can be extended for categorical)
            if current_node.threshold is not None and feature_val <= current_node.threshold:
                current_node = current_node.left
            else:
                current_node = current_node.right
                
        if current_node is not None and current_node.value is not None:
            return current_node.value
        return "UNKNOWN"

# Example Tree Construction Helper
def build_protest_tree():
    """
    Returns a predefined tree for deciding if an agent should protest.
    Logic: If tax_rate > 0.3 -> If wealth < 1000 -> Protest (True)
    """
    leaf_protest = DecisionNode(value="PROTEST")
    leaf_peace = DecisionNode(value="PEACEFUL")
    
    # Check Wealth
    wealth_node = DecisionNode(feature="wealth", threshold=50, left=leaf_protest, right=leaf_peace)
    
    # Check Tax Rate
    root = DecisionNode(feature="tax_rate", threshold=0.3, left=leaf_peace, right=wealth_node)
    
    return DecisionTree(root)

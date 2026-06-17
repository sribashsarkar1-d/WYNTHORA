import hashlib

class MerkleNode:
    def __init__(self, left, right, hash_val):
        self.left = left
        self.right = right
        self.hash_val = hash_val

class MerkleTree:
    """
    Creates a Merkle Tree from a list of simulation state transactions.
    Used for enterprise cryptographic proof of simulation integrity.
    """
    def __init__(self, data_blocks):
        self.leaves = [self._hash_data(block) for block in data_blocks]
        self.root = self._build_tree(self.leaves)

    def _hash_data(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _build_tree(self, nodes):
        if len(nodes) == 0:
            return None
        if len(nodes) == 1:
            return MerkleNode(None, None, nodes[0])

        new_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i+1] if i+1 < len(nodes) else left
            combined_hash = self._hash_data(left + right)
            new_level.append(combined_hash)

        return self._build_tree(new_level)

    def get_root_hash(self):
        return self.root.hash_val if self.root else None

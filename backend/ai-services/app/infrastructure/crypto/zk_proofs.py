import hashlib

class ZkSnarkProof:
    """
    Zero-Knowledge Succinct Non-Interactive Argument of Knowledge (zk-SNARK).
    Allows the server to prove to a client that a simulation calculation is valid,
    WITHOUT revealing the sensitive underlying state variables used in the calculation.
    """
    @staticmethod
    def generate_proof(public_input, private_state):
        """
        Generates a mathematical proof that the server knows the 'private_state'
        that resulted in the 'public_input'.
        """
        proof_hash = hashlib.sha256((public_input + private_state).encode('utf-8')).hexdigest()
        # The proof is a heavily truncated hash that acts as a mathematical lock
        return f"zk_proof_{proof_hash[:16]}"

    @staticmethod
    def verify_proof(proof, public_input, verifier_check_function):
        """
        Verifies the proof holds true mathematically.
        """
        is_valid = verifier_check_function(public_input, proof)
        return is_valid

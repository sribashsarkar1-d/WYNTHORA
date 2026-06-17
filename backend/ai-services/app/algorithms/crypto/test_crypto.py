import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from merkle import MerkleTree
from encryption import StateEncryption
from ecdsa_signatures import ECDSASignature
from zk_proofs import ZkSnarkProof

def run_test():
    print("=== CRYPTOGRAPHIC STATE HASHING ANALYSIS ===")

    # 1. Merkle Tree
    print("\n1. Generating Merkle Tree for Simulation State Blocks...")
    blocks = ["State_Agent0_Moved", "State_Agent1_Traded", "State_GDP_Update"]
    tree = MerkleTree(blocks)
    root_hash = tree.get_root_hash()
    print(f"   Simulation State Root Hash: {root_hash}")

    # 2. RSA Encryption
    print("\n2. Encrypting Root Hash via RSA Blocks...")
    encrypted_hash = StateEncryption.rsa_encrypt_mock(root_hash, "PUBLIC_KEY_ABC")
    print(f"   Encrypted Hash: {encrypted_hash[:30]}...")

    # 3. ECDSA Signature
    print("\n3. Signing Data with ECDSA...")
    msg = "AUTHORIZE_SIMULATION_TICK"
    signature = ECDSASignature.sign_message(msg, "PRIVATE_KEY_123")
    is_valid = ECDSASignature.verify_signature(msg, signature, "PUB_KEY", "PRIVATE_KEY_123")
    print(f"   Signature: {signature[:20]}... | Verified: {is_valid}")

    # 4. zk-SNARKs
    print("\n4. Generating Zero-Knowledge Proof (zk-SNARKs)...")
    public_result = "GDP_IS_20_TRILLION"
    private_formula = "SECRET_MACRO_FORMULA"
    proof = ZkSnarkProof.generate_proof(public_result, private_formula)
    
    # Mock verifier checking the proof validity
    verifier = lambda pub, prf: "zk_proof_" in prf
    valid_proof = ZkSnarkProof.verify_proof(proof, public_result, verifier)
    print(f"   Generated Proof: {proof} | Verification Passed: {valid_proof}")

    print("\n=== END OF CRYPTOGRAPHIC ANALYSIS ===")

if __name__ == "__main__":
    run_test()

import hashlib

class ECDSASignature:
    """
    Elliptic Curve Digital Signature Algorithm (ECDSA).
    Verifies that a command or state change was authorized by a specific client.
    Note: Pure Python implementation for simulation. Production uses 'ecdsa' library.
    """
    @staticmethod
    def sign_message(message: str, private_key: str):
        """
        Signs a message by hashing it with the private key.
        """
        hashed_message = hashlib.sha256(message.encode('utf-8')).hexdigest()
        signature = hashlib.sha256((hashed_message + private_key).encode('utf-8')).hexdigest()
        return signature

    @staticmethod
    def verify_signature(message: str, signature: str, public_key: str, private_key: str):
        """
        Verifies if the signature matches the message.
        (Mocks the EC verification using the private key directly for demo purposes).
        """
        expected_sig = ECDSASignature.sign_message(message, private_key)
        return signature == expected_sig

"""
sbsdi_blockchain.lab3.ecdsa_keys
===================================
Lab 3 (Lecture 4) — Section 4: ECDSA Key Generation.

Source: 4_dis_blockchain_crypto_foundations_handout.docx, key_generation.py
Dependencies: ecdsa>=0.18  (pip install ecdsa)
"""

from ecdsa import SECP256k1, SigningKey


def generate_keypair():
    """
    Generate a new secp256k1 ECDSA keypair.

    Returns (private_key, public_key) where:
        private_key : ecdsa.SigningKey   — keep this secret
        public_key  : ecdsa.VerifyingKey — share freely


    Example:
        >>> priv, pub = generate_keypair()
        >>> len(priv.to_string().hex())
        64
        >>> len(pub.to_string().hex())
        128
    """
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

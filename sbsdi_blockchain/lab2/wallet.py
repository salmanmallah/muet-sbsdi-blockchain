"""
sbsdi_blockchain.lab2.wallet
=============================
Lab 2 (Lecture 3) — Module 5: Wallet (ECDSA secp256k1 keypair).

Source: 3-dis_blockchain_lab_handout.docx, blockchain_lab.py — Module 5
Dependencies: ecdsa>=0.18  (pip install ecdsa)

NOTE ON LIBRARY CHOICE
The original handout for Lab 2 used the `cryptography` (PyCA) library:
    from cryptography.hazmat.primitives.asymmetric import ec
    ...
    self.private_key = ec.generate_private_key(ec.SECP256K1())

This package standardises on the `ecdsa` library instead, which:
  1. Is used in Lab 3 handout (consistent API across all labs)
  2. Has a simpler, more readable API (better for students)
  3. Has a stable API — `ecdsa>=0.18` is safe across Python 3.8–3.13

The public-facing API (Wallet.address(), Wallet.private_key,
Wallet.public_key) is identical in behaviour. Only the internal
implementation changed.
"""
from __future__ import annotations


import hashlib

from ecdsa import SECP256k1, SigningKey


class Wallet:
    """
    Generates a REAL secp256k1 keypair — the curve Bitcoin/Ethereum use.

    Attributes:
        name        : human-readable label (e.g. "Alice")
        private_key : ecdsa.SigningKey object (keep secret!)
        public_key  : ecdsa.VerifyingKey object (share freely)
    """

    def __init__(self, name: str):
        self.name = name
        self.private_key: SigningKey = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def address(self) -> str:
        """
        Derive a short wallet address from the public key.

        Takes the first 20 hex chars of SHA-256(compressed public key bytes).
        """
        # to_string() gives 64-byte uncompressed pubkey (x || y)
        pub_bytes = self.public_key.to_string()
        x = pub_bytes[:32]
        # Compressed form prefix: 0x02 if y is even, 0x03 if odd
        y_last_byte = pub_bytes[-1]
        prefix = b"\x02" if y_last_byte % 2 == 0 else b"\x03"
        compressed = prefix + x
        return hashlib.sha256(compressed).hexdigest()[:20]

    def __repr__(self) -> str:
        return f"Wallet(name={self.name!r}, address={self.address()})"

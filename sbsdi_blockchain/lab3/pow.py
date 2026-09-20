"""
sbsdi_blockchain.lab3.pow
===========================
Lab 3 (Lecture 4) — Section 3: Proof-of-Work.

Source: 4_dis_blockchain_crypto_foundations_handout.docx, proof_of_work.py
Dependencies: stdlib only (hashlib)
"""

import hashlib


def proof_of_work(data: bytes, difficulty: int = 5) -> tuple[int, str]:
    """
    Find a nonce such that SHA-256(data + str(nonce)) starts with
    *difficulty* leading zeros.

    Returns (nonce, hash_hex).


    Example:
        >>> nonce, h = proof_of_work(b"block-data", difficulty=5)
        >>> print(f"Found nonce={nonce} -> hash={h}")
    """
    target = "0" * difficulty
    nonce = 0
    while True:
        attempt = data + str(nonce).encode()
        h = hashlib.sha256(attempt).hexdigest()
        if h.startswith(target):
            return nonce, h
        nonce += 1

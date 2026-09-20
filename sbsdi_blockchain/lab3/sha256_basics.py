"""
sbsdi_blockchain.lab3.sha256_basics
=====================================
Lab 3 (Lecture 4) — Section 1: SHA-256 Basics + Avalanche Effect.

Source: 4_dis_blockchain_crypto_foundations_handout.docx, sha256_basics.py
Dependencies: stdlib only (hashlib)
"""

import hashlib


def sha256(data: bytes) -> str:
    """
    Single SHA-256 hash. Returns 64-character hex string.
    """
    return hashlib.sha256(data).hexdigest()


def avalanche_demo(original: bytes, modified: bytes) -> dict:
    """
    Demonstrate the avalanche effect: a 1-character change in input
    produces a completely different hash.


    Returns a dict with both hashes and the number of differing hex chars.
    """
    h1 = hashlib.sha256(original).hexdigest()
    h2 = hashlib.sha256(modified).hexdigest()
    diff_chars = sum(c1 != c2 for c1, c2 in zip(h1, h2))
    return {
        "original_hash": h1,
        "modified_hash": h2,
        "differing_hex_chars": diff_chars,
        "total_hex_chars": len(h1),
    }

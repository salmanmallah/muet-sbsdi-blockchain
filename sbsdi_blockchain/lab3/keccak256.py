"""
sbsdi_blockchain.lab3.keccak256
=================================
Lab 3 (Lecture 4) — Section 2: Keccak-256 (Ethereum hashing).

Source: 4_dis_blockchain_crypto_foundations_handout.docx, keccak256.py
Dependencies: pycryptodome>=3.15  (pip install pycryptodome)

IMPORTANT: Install pycryptodome, NOT the old pycrypto package.
Both expose `from Crypto.Hash import keccak` but only pycryptodome
implements Keccak-256 correctly. If you have pycrypto installed,
uninstall it first: pip uninstall pycrypto
"""
from __future__ import annotations



def keccak256(data: bytes) -> str:
    """
    Keccak-256 hash of *data*. Returns 64-character hex string.

    This is the hash function Ethereum uses internally (not SHA-3 — they
    diverge in padding; Ethereum standardised on the original Keccak
    submission before the NIST SHA-3 standard was finalised).


    Example:
        >>> keccak256(b"Hello, Blockchain!")
        '85969098df123880318fdb891f91d7170a681fcf21a09e9035c9e276b7d5c90f'
    """
    from Crypto.Hash import keccak  # pycryptodome
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.hexdigest()

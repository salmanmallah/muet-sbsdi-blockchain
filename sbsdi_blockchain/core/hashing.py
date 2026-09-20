"""
sbsdi_blockchain.core.hashing
==============================
Shared cryptographic hashing utilities used across all labs.
No external dependencies — pure Python stdlib.
"""

import hashlib


def sha256(data: bytes) -> str:
    """
    Single SHA-256 hash of *data*.

    Returns the hex digest string (64 hex chars).
    """
    return hashlib.sha256(data).hexdigest()


def sha256_bytes(data: bytes) -> bytes:
    """Single SHA-256, returns raw bytes (useful for chaining)."""
    return hashlib.sha256(data).digest()


def sha256d(data: bytes) -> bytes:
    """
    Double SHA-256 — the exact hashing Bitcoin uses for Merkle trees.
    sha256d(x) = SHA-256(SHA-256(x))

    Returns raw bytes so it can be concatenated for the next level.
    """
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def keccak256(data: bytes) -> str:
    """
    Keccak-256 hash — used by Ethereum for address derivation.

    Requires: pycryptodome  (pip install pycryptodome)
    NOTE: Use pycryptodome, NOT the old abandoned pycrypto package.
          Both expose `from Crypto.Hash import keccak` but only
          pycryptodome implements it correctly.

    Returns the hex digest string (64 hex chars).
    """
    from Crypto.Hash import keccak  # pycryptodome
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.hexdigest()

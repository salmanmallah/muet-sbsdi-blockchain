"""
sbsdi_blockchain.lab3.sign_verify
====================================
Lab 3 (Lecture 4) — Sections 6 & 7: ECDSA Sign, Verify, and Tamper Test.

Source: 4_dis_blockchain_crypto_foundations_handout.docx
        sign_and_verify.py  (Section 6)
        tamper_test.py      (Section 7)
Dependencies: ecdsa>=0.18, stdlib (hashlib)
"""
from __future__ import annotations


import hashlib

from ecdsa import BadSignatureError, SigningKey, VerifyingKey


def sign(private_key: SigningKey, message: bytes) -> bytes:
    """
    Sign *message* with *private_key* using deterministic ECDSA + SHA-256.

    The signature is deterministic (RFC 6979) — the same (key, message) pair
    always produces the same signature. Only the private key holder can produce it.


    Returns:
        Raw bytes of the DER-encoded signature.
    """
    return private_key.sign(message, hashfunc=hashlib.sha256)


def verify(public_key: VerifyingKey, signature: bytes, message: bytes) -> bool:
    """
    Verify *signature* on *message* using *public_key*.

    Returns True if valid, False if tampered or wrong key.


    Example:
        >>> from sbsdi_blockchain.lab3 import generate_keypair, sign, verify
        >>> priv, pub = generate_keypair()
        >>> msg = b"Alice pays Bob 5 BTC"
        >>> sig = sign(priv, msg)
        >>> verify(pub, sig, msg)
        True
        >>> verify(pub, sig, b"Alice pays Bob 500 BTC")   # tampered
        False
    """
    try:
        public_key.verify(signature, message, hashfunc=hashlib.sha256)
        return True
    except BadSignatureError:
        return False

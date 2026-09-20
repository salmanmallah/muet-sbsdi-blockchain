"""
sbsdi_blockchain.lab3
======================
Lab 3 — Lecture 4: Cryptographic Foundations.

Source: 4_dis_blockchain_crypto_foundations_handout.docx
Dependencies:
    ecdsa>=0.18       (pip install ecdsa)      — ECDSA key gen + signing
    pycryptodome>=3.15 (pip install pycryptodome) — Keccak-256

pip install sbsdi-blockchain    ← installs both automatically

Exports:
    Hashing:
        sha256          — single SHA-256 (returns hex string)
        avalanche_demo  — show how 1-char change changes the entire hash
        keccak256       — Keccak-256 (Ethereum's hash function)

    Proof-of-Work:
        proof_of_work   — find nonce so SHA-256(data+nonce) has N leading zeros

    ECDSA Cryptography:
        generate_keypair    — secp256k1 keypair (SigningKey, VerifyingKey)
        derive_eth_address  — Keccak-256 of pubkey → Ethereum address
        sign                — sign bytes with private key
        verify              — verify signature against public key

    Merkle Trees:
        sha256d         — double SHA-256 (Bitcoin Merkle standard)
        MerkleTree      — build tree, get root, get SPV proof
        verify_proof    — verify SPV proof for a leaf

    Capstone:
        capstone.Block          — full block: MerkleTree + PoW
        capstone.build_signed_block — sign a tx and build a mined block
"""
from __future__ import annotations


from .sha256_basics import sha256, avalanche_demo
from .keccak256 import keccak256
from .pow import proof_of_work
from .ecdsa_keys import generate_keypair
from .eth_address import derive_eth_address
from .sign_verify import sign, verify
from .merkle import sha256d, MerkleTree, verify_proof
from . import capstone

__all__ = [
    # Hashing
    "sha256",
    "avalanche_demo",
    "keccak256",
    # PoW
    "proof_of_work",
    # ECDSA
    "generate_keypair",
    "derive_eth_address",
    "sign",
    "verify",
    # Merkle
    "sha256d",
    "MerkleTree",
    "verify_proof",
    # Capstone
    "capstone",
]

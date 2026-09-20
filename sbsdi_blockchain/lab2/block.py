"""
sbsdi_blockchain.lab2.block
============================
Lab 2 (Lecture 3) — Module 4: Block with Merkle root + PoW.

Source: 3-dis_blockchain_lab_handout.docx, blockchain_lab.py — Module 4
Dependencies: stdlib only (hashlib, json, time)

This Block stores a *list of transactions* (not a raw string like Lab 1).
The Merkle root of all transactions is included in the hash, so tampering
with any transaction inside the block changes the block hash.
"""
from __future__ import annotations


import hashlib
import json
import time

from .merkle import merkle_root


class Block:
    """
    A block that holds a list of transaction dicts and includes their
    Merkle root in its hash.

    The Merkle root is recomputed from the CURRENT transactions on every
    call to compute_hash(), so tampering with a transaction after mining
    will always be detectable — the stored hash will no longer match.
    """

    def __init__(
        self,
        index: int,
        transactions: list,
        previous_hash: str,
        timestamp: float | None = None,
        nonce: int = 0,
    ):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_root = merkle_root(transactions)
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        SHA-256 over (index, timestamp, Merkle root of current txns,
        previous_hash, nonce).

        Merkle root is recomputed live — NOT cached — so post-mining
        transaction tampering is always detected.
        """
        header = {
            "index": self.index,
            "timestamp": self.timestamp,
            "merkle_root": merkle_root(self.transactions),
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        return hashlib.sha256(json.dumps(header, sort_keys=True).encode()).hexdigest()

    def mine(self, difficulty: int = 4) -> "Block":
        """
        Proof-of-Work: increment nonce until hash starts with *difficulty* zeros.
        Modifies self in-place and returns self for chaining.
        """
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()
        return self

    def is_hash_valid(self) -> bool:
        """
        Check that the stored hash still matches the current block content.
        """
        return self.hash == self.compute_hash()

    def __repr__(self) -> str:
        return (
            f"Block(index={self.index}, "
            f"txns={len(self.transactions)}, "
            f"hash={self.hash[:12]}...)"
        )

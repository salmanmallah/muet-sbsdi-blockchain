"""
sbsdi_blockchain.lab1.block
============================
Lab 1 (Lecture 2) — Step 1: Define the Block Class.

Source: 2_Dis_Blockchain_Intro_Lab.docx, Step 1.2
Dependencies: stdlib only (hashlib, json, time)
"""

import hashlib
import json
import time


class Block:
    """
    A single block in a blockchain.

    Each block contains:
    - index       : position in the chain (0 = genesis)
    - timestamp   : Unix timestamp when block was created
    - data        : arbitrary payload (string or dict)
    - previous_hash: hash of the previous block (links the chain)
    - nonce       : counter used for Proof-of-Work mining
    - hash        : SHA-256 hash of the above fields

    The nonce starts at 0 and is incremented by the miner until the
    hash meets the difficulty target (leading zeros).
    """

    def __init__(self, index: int, timestamp: float, data, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        Compute the SHA-256 hash of this block's contents.

        All fields (including nonce) are serialised to JSON with sorted keys
        so the hash is deterministic regardless of dict insertion order.

        """
        block_contents = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_contents, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self) -> str:
        return (
            f"Block(index={self.index}, "
            f"hash={self.hash[:12]}..., "
            f"prev={self.previous_hash[:12]}..., "
            f"nonce={self.nonce})"
        
        )

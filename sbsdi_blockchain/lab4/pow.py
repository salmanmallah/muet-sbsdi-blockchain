"""
sbsdi_blockchain.lab4.pow
===========================
Lab 4 (Lecture 5) — Lab 1: Proof-of-Work Blockchain.

Source: 5_Dis_Blockchain_Consensus_Mechanisms_Handou.docx, lab1_pow.py
Dependencies: stdlib only (hashlib, json, time)
"""

import hashlib
import json
import time


class Block:
    """
    A PoW block that stores a list of transactions.
    """

    def __init__(
        self,
        index: int,
        previous_hash: str,
        transactions: list,
        timestamp: float | None = None,
    ):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash: str | None = None

    def compute_hash(self) -> str:
        """
        SHA-256 over JSON-serialised block fields (sorted keys, encoded).
        """
        block_string = json.dumps(
            {
                "index": self.index,
                "previous_hash": self.previous_hash,
                "transactions": self.transactions,
                "timestamp": self.timestamp,
                "nonce": self.nonce,
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self) -> str:
        return (
            f"Block(index={self.index}, "
            f"nonce={self.nonce}, "
            f"hash={str(self.hash)[:12]}...)"
        )


def mine_block(block: Block, difficulty: int) -> str:
    """
    PoW: find a nonce so that block.compute_hash() starts with *difficulty* zeros.

    Sets block.hash and returns the hash.
    """
    target = "0" * difficulty
    while True:
        block.hash = block.compute_hash()
        if block.hash.startswith(target):
            return block.hash
        block.nonce += 1


class PoWBlockchain:
    """
    A proof-of-work blockchain (Lab 4 variant).
    """

    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        genesis = Block(0, "0", [])
        mine_block(genesis, self.difficulty)
        self.chain: list[Block] = [genesis]

    def add_block(self, transactions: list) -> Block:
        """Create, mine, and append a new block."""
        prev = self.chain[-1]
        block = Block(len(self.chain), prev.hash, transactions)
        mine_block(block, self.difficulty)
        self.chain.append(block)
        return block

    def is_valid(self) -> bool:
        """
        Verify hash integrity and chain linking for every block.
        """
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i - 1]
            if cur.hash != cur.compute_hash():
                return False
            if cur.previous_hash != prev.hash:
                return False
            if not cur.hash.startswith("0" * self.difficulty):
                return False
        return True

    def __repr__(self) -> str:
        return f"PoWBlockchain({len(self.chain)} blocks, difficulty={self.difficulty})"

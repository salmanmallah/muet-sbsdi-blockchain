"""
sbsdi_blockchain.lab1.blockchain
==================================
Lab 1 (Lecture 2) — Steps 2 & 4: Blockchain Class + Validation.

Source: 2_Dis_Blockchain_Intro_Lab.docx, Steps 2.1 and 4.1
Dependencies: stdlib only
"""

import time
from .block import Block


class Blockchain:
    """
    A simple linked list of Block objects.

    The chain always starts with a Genesis block (index=0, prev_hash="0").
    New blocks are appended via add_block(); each references the hash of
    the previous block, forming a tamper-evident chain.
    """

    def __init__(self):
        self.chain: list[Block] = [self._create_genesis_block()]

    # ------------------------------------------------------------------
    # Step 2.1 — Genesis block
    # ------------------------------------------------------------------

    def _create_genesis_block(self) -> Block:
        """
        Create the very first block (index=0).
        Its previous_hash is "0" by convention (there is no real predecessor).
        """
        return Block(0, time.time(), "Genesis Block", "0")

    # ------------------------------------------------------------------
    # Step 2.1 — Chain helpers
    # ------------------------------------------------------------------

    def get_latest_block(self) -> Block:
        """Return the most recently added block."""
        return self.chain[-1]

    def add_block(self, data, difficulty: int = 4) -> Block:
        """
        Create a new block containing *data*, mine it to *difficulty*
        leading zeros, and append it to the chain.
        """
        previous_block = self.get_latest_block()
        new_block = Block(
            previous_block.index + 1,
            time.time(),
            data,
            previous_block.hash,
        )
        self.mine_block(new_block, difficulty)
        self.chain.append(new_block)
        return new_block

    # ------------------------------------------------------------------
    # Step 3.1 — Proof-of-Work mining
    # ------------------------------------------------------------------

    def mine_block(self, block: Block, difficulty: int) -> None:
        """
        Brute-force a nonce so that block.hash starts with *difficulty* zeros.
        """
        target = "0" * difficulty
        while block.hash[:difficulty] != target:
            block.nonce += 1
            block.hash = block.compute_hash()

    # ------------------------------------------------------------------
    # Step 4.1 — Chain validation
    # ------------------------------------------------------------------

    def is_chain_valid(self) -> bool:
        """
        Walk the chain from block 1 onward and verify two invariants
        for each block:

        1. block.hash == block.compute_hash()   (data has not been altered)
        2. block.previous_hash == chain[i-1].hash  (links are intact)

        Returns True if every block passes; False at the first violation.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                print(f"Block {current.index} has been tampered with!")
                return False

            if current.previous_hash != previous.hash:
                print(
                    f"Block {current.index} is not properly linked "
                    f"to Block {previous.index}!"
                )
                return False

        return True

    def __repr__(self) -> str:
        return f"Blockchain({len(self.chain)} blocks)"

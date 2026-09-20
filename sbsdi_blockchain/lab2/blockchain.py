"""
sbsdi_blockchain.lab2.blockchain
==================================
Lab 2 (Lecture 3) — Module 5: Blockchain (mempool + mining + validation).

Source: 3-dis_blockchain_lab_handout.docx, blockchain_lab.py — Module 5
Dependencies: stdlib only (uses Block, Mempool, Transaction from same lab)
"""

from .block import Block
from .mempool import Mempool, get_balance
from .transaction import Transaction


class Blockchain:
    """
    A proof-of-work blockchain with a transaction mempool.

    Supports:
    - Genesis grants (initial coin distribution)
    - Transaction submission (with balance + signature checks via Mempool)
    - Mining pending transactions into blocks
    - Chain validity checking (hash integrity + PoW target)
    - Transaction confirmations (depth from tip)
    """

    def __init__(self, difficulty: int = 4, genesis_grants: dict | None = None):
        self.chain: list[Block] = [Block(0, [], "0")]
        self.difficulty = difficulty
        self.mempool = Mempool()
        self.genesis_grants: dict = genesis_grants or {}

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def submit_transaction(self, tx: Transaction) -> None:
        """
        Validate and add *tx* to the mempool.

        Raises ValueError if the transaction is invalid or balance is insufficient.
        """
        self.mempool.add(tx, self.chain, self.genesis_grants)

    def mine_pending_transactions(self) -> Block:
        """
        Pull all pending transactions from the mempool, pack them into a
        new block, mine it (PoW), append to the chain, and mark each
        transaction as CONFIRMED.
        """
        txs = self.mempool.pop_all_by_fee()
        tx_dicts = [t.to_dict() for t in txs]
        new_block = Block(len(self.chain), tx_dicts, self.last_block.hash)
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        for t in txs:
            t.status = Transaction.STATUS_CONFIRMED
        return new_block

    def is_chain_valid(self) -> bool:
        """
        Verify every block in the chain:
        1. Hash is still valid (data unchanged)
        2. previous_hash links are intact
        3. Hash meets the PoW difficulty target
        """
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i - 1]
            if not cur.is_hash_valid():
                return False
            if cur.previous_hash != prev.hash:
                return False
            if not cur.hash.startswith("0" * self.difficulty):
                return False
        return True

    def confirmations(self, txid: str) -> int:
        """
        Return how many blocks deep a transaction is (0 = not found).
        """
        for block in self.chain:
            if any(t["txid"] == txid for t in block.transactions):
                return len(self.chain) - 1 - block.index
        return 0

    def __repr__(self) -> str:
        return f"Blockchain({len(self.chain)} blocks, difficulty={self.difficulty})"

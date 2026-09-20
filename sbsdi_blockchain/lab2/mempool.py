"""
sbsdi_blockchain.lab2.mempool
==============================
Lab 2 (Lecture 3) — Module 5: Mempool (pending transaction pool) + balance.

Source: 3-dis_blockchain_lab_handout.docx, blockchain_lab.py — Module 5
Dependencies: stdlib only (uses Transaction from same lab)

The mempool validates incoming transactions (signature, balance, self-send)
and sorts them by fee (highest fee first) to model miner incentives.
"""

from .transaction import Transaction


def get_balance(address: str, chain: list, genesis_grants: dict | None = None) -> float:
    """
    Recompute an address's balance by scanning all confirmed transactions
    in *chain* (list of Block objects).

    Starts from *genesis_grants* (a dict of address → initial balance),
    then adds incoming and subtracts outgoing amounts + fees for every
    confirmed transaction in the chain.
    """
    balance = dict(genesis_grants or {}).get(address, 0)
    for block in chain:
        for tx in block.transactions:
            if tx["sender"] == address:
                balance -= tx["amount"] + tx.get("fee", 0)
            if tx["receiver"] == address:
                balance += tx["amount"]
    return balance


class Mempool:
    """
    A pool of validated, pending transactions waiting to be mined.

    Miners prioritise transactions with higher fees (fee market model).
    Incoming transactions are rejected if they are invalid (bad signature,
    insufficient balance, or self-send).
    """

    def __init__(self):
        self.pending: dict[str, Transaction] = {}

    def add(
        self,
        tx: Transaction,
        chain: list,
        genesis_grants: dict | None = None,
    ) -> None:
        """
        Validate *tx* and add it to the pending pool.

        Rejects with ValueError if:
          - signature is invalid, amount ≤ 0, or self-send (is_valid check)
          - sender balance < amount + fee
        """
        if not tx.is_valid():
            tx.status = Transaction.STATUS_REJECTED
            raise ValueError(
                "Invalid transaction (bad signature / amount / self-send)"
            )
        balance = get_balance(tx.sender, chain, genesis_grants)
        if balance < tx.amount + tx.fee:
            tx.status = Transaction.STATUS_REJECTED
            raise ValueError(
                f"Insufficient balance: has {balance}, "
                f"needs {tx.amount + tx.fee}"
            )
        tx.status = Transaction.STATUS_PENDING
        self.pending[tx.txid] = tx

    def pop_all_by_fee(self) -> list[Transaction]:
        """
        Remove and return all pending transactions, sorted by fee descending.

        Miners call this to select transactions for the next block.
        """
        txs = sorted(self.pending.values(), key=lambda t: t.fee, reverse=True)
        self.pending.clear()
        return txs

    def __len__(self) -> int:
        return len(self.pending)

    def __repr__(self) -> str:
        return f"Mempool({len(self.pending)} pending txns)"

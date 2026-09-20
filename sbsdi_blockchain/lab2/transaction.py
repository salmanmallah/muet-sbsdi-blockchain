"""
sbsdi_blockchain.lab2.transaction
===================================
Lab 2 (Lecture 3) — Module 5: Transaction (sign, verify, lifecycle states).

Source: 3-dis_blockchain_lab_handout.docx, blockchain_lab.py — Module 5
Dependencies: ecdsa>=0.18, stdlib (hashlib, time)

A Transaction moves coins from a Wallet (sender) to an address (receiver).
It must be signed with the sender's private key before being submitted to
the network. Miners verify the signature before including it in a block.
"""

import hashlib
import time

from ecdsa import BadSignatureError

from .wallet import Wallet


class Transaction:
    """
    A signed transfer of coins between two parties.

    Lifecycle states (class constants):
        STATUS_CREATED   → just instantiated, not yet signed
        STATUS_PENDING   → signed and submitted to the mempool
        STATUS_REJECTED  → invalid signature, bad balance, or self-send
        STATUS_CONFIRMED → included in a mined block
    """

    STATUS_CREATED = "CREATED"
    STATUS_PENDING = "PENDING"
    STATUS_REJECTED = "REJECTED"
    STATUS_CONFIRMED = "CONFIRMED"

    def __init__(
        self,
        sender_wallet: Wallet,
        receiver_address: str,
        amount: float,
        fee: float = 0.0,
    ):
        """
        """
        self.sender: str = sender_wallet.address()
        self.sender_wallet: Wallet = sender_wallet
        self.receiver: str = receiver_address
        self.amount: float = amount
        self.fee: float = fee
        self.timestamp: float = time.time()
        self.status: str = Transaction.STATUS_CREATED
        self.signature: bytes | None = None
        self.txid: str = self._compute_txid()

    def _compute_txid(self) -> str:
        """
        Deterministic transaction ID = SHA-256 of (sender, receiver, amount, fee, timestamp).
        """
        raw = f"{self.sender}{self.receiver}{self.amount}{self.fee}{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def sign(self) -> None:
        """
        Sign the transaction with the sender's private key.

        Uses deterministic RFC 6979 ECDSA (secp256k1) with SHA-256.
        The signature covers the txid (which is derived from all transaction fields).
        """
        self.signature = self.sender_wallet.private_key.sign(
            self.txid.encode(), hashfunc=hashlib.sha256
        )

    def verify_signature(self) -> bool:
        """
        Verify the signature against the sender's public key.

        Returns False if no signature or if verification fails.
        """
        if self.signature is None:
            return False
        try:
            self.sender_wallet.public_key.verify(
                self.signature, self.txid.encode(), hashfunc=hashlib.sha256
            )
            return True
        except BadSignatureError:
            return False

    def is_valid(self) -> bool:
        """
        Full validity check: positive amount, no self-send, valid signature.
        """
        return (
            self.amount > 0
            and self.sender != self.receiver
            and self.verify_signature()
        )

    def to_dict(self) -> dict:
        """
        Serialise the transaction to a plain dict (for block storage).
        """
        return {
            "txid": self.txid,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "fee": self.fee,
            "status": self.status,
        }

    def __repr__(self) -> str:
        return (
            f"Transaction(from={self.sender[:8]}..., "
            f"to={self.receiver[:8]}..., "
            f"amount={self.amount}, fee={self.fee}, "
            f"status={self.status})"
        )

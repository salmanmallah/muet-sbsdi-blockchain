"""
sbsdi_blockchain.lab3.capstone
================================
Lab 3 (Lecture 4) — Section 10: Capstone Mini Blockchain.

Source: 4_dis_blockchain_crypto_foundations_handout.docx, capstone_mini_blockchain.py
Dependencies: ecdsa>=0.18, stdlib (hashlib, time)

Combines all Lab 3 concepts into a minimal but complete blockchain:
- ECDSA-signed transactions (ecdsa library, secp256k1)
- Bitcoin-style double-SHA256 Merkle tree over transactions
- Proof-of-Work block mining
- Chain linking via previous_hash
"""

import hashlib
import time

from ecdsa import SECP256k1, SigningKey

from .merkle import MerkleTree, sha256d


class Block:
    """
    A capstone block that combines Merkle tree + PoW mining.
    """

    def __init__(
        self,
        index: int,
        prev_hash: str,
        transactions: list[bytes],
        difficulty: int = 4,
    ):
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.merkle_root = MerkleTree(transactions).merkle_root if transactions else sha256d(b"").hex()
        self.timestamp = int(time.time())
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self._mine()

    def _header(self) -> bytes:
        """
        Serialise block header fields into bytes for hashing.
        """
        return (
            f"{self.index}{self.prev_hash}{self.merkle_root}"
            f"{self.timestamp}{self.nonce}"
        ).encode()

    def _mine(self) -> str:
        """
        PoW: increment nonce until SHA-256(_header()) starts with *difficulty* zeros.
        """
        target = "0" * self.difficulty
        while True:
            h = hashlib.sha256(self._header()).hexdigest()
            if h.startswith(target):
                return h
            self.nonce += 1

    def __repr__(self) -> str:
        return (
            f"Block(index={self.index}, "
            f"txns={len(self.transactions)}, "
            f"nonce={self.nonce}, "
            f"hash={self.hash[:12]}...)"
        )


def build_signed_block(
    signing_key: SigningKey,
    tx_data: bytes,
    prev_hash: str,
    index: int = 1,
    difficulty: int = 4,
) -> Block:
    """
    Helper: sign *tx_data* with *signing_key*, embed in signed_tx bytes,
    and build a Block containing [genesis_tx, signed_tx].

    Returns the mined block containing the signed transaction.
    """
    signature = signing_key.sign(tx_data, hashfunc=hashlib.sha256)
    signed_tx = tx_data + b"|sig:" + signature.hex().encode()

    genesis = Block(index=0, prev_hash="0" * 64, transactions=[b"genesis"], difficulty=difficulty)
    block = Block(
        index=index,
        prev_hash=genesis.hash,
        transactions=[signed_tx],
        difficulty=difficulty,
    )
    return block

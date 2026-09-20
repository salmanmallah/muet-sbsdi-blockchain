"""
sbsdi_blockchain.lab3.merkle
==============================
Lab 3 (Lecture 4) — Sections 8 & 9: Bitcoin Merkle Tree + SPV Proof.

Source: 4_dis_blockchain_crypto_foundations_handout.docx
        merkle_tree_build.py  (Section 8)
        merkle_proof.py       (Section 9)
Dependencies: stdlib only (hashlib)

Uses Bitcoin's DOUBLE SHA-256 (sha256d) — not the single-SHA256 used in Lab 2.
sha256d(x) = SHA-256(SHA-256(x))
"""
from __future__ import annotations


import hashlib


def sha256d(data: bytes) -> bytes:
    """
    Double SHA-256 — Bitcoin's standard Merkle leaf and node hash.

    Returns raw bytes (not hex) so they can be concatenated for the next level.
    """
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


class MerkleTree:
    """
    A Bitcoin-style Merkle tree using double-SHA256.

    Supports:
    - root()      — compute the Merkle root (hex string)
    - get_proof() — generate an SPV proof for a leaf by index
    - verify_proof() (standalone function) — verify an SPV proof
    """

    def __init__(self, leaves: list[bytes]):
        """
        Initialise the tree from a list of *leaves* (raw bytes).
        Each leaf is hashed with sha256d immediately.
        """
        self.leaves = [sha256d(leaf) for leaf in leaves] if leaves else [sha256d(b"")]
        self.levels: list[list[bytes]] = []
        self._build()

    def _build(self) -> None:
        """
        Build all levels of the tree bottom-up until only the root remains.

        If a level has an odd number of hashes, duplicate the last one
        (Bitcoin standard padding rule).
        """
        current = self.leaves[:]
        self.levels.append(current)
        while len(current) > 1:
            if len(current) % 2 == 1:
                current.append(current[-1])  # duplicate lone leaf
            next_level = []
            for i in range(0, len(current), 2):
                combined = current[i] + current[i + 1]
                next_level.append(sha256d(combined))
            current = next_level
            self.levels.append(current)

    def root(self) -> str:
        """
        Return the Merkle root as a hex string.
        """
        return self.levels[-1][0].hex()

    def get_proof(self, index: int) -> list[tuple[bytes, bool]]:
        """
        Generate an SPV (Simplified Payment Verification) proof for the
        leaf at *index*.

        Returns a list of (sibling_hash_bytes, is_right) pairs — one per
        tree level. is_right is True if the sibling is to the right of the
        current node.
        """
        proof: list[tuple[bytes, bool]] = []
        idx = index
        for level in self.levels[:-1]:
            level = level[:]  # don't mutate original
            if len(level) % 2 == 1:
                level.append(level[-1])
            pair_idx = idx ^ 1          # sibling's index (XOR with 1)
            is_right = pair_idx > idx   # True if sibling is to the right
            proof.append((level[pair_idx], is_right))
            idx //= 2
        return proof


def verify_proof(leaf: bytes, proof: list[tuple[bytes, bool]], root_hex: str) -> bool:
    """
    Verify that *leaf* is included in the Merkle tree with root *root_hex*,
    using the SPV *proof* produced by MerkleTree.get_proof().


    Example:
        >>> from sbsdi_blockchain.lab3 import MerkleTree, verify_proof
        >>> txs = [b"Alice pays Bob 5 BTC", b"Bob pays Carol 2 BTC"]
        >>> tree = MerkleTree(txs)
        >>> proof = tree.get_proof(0)
        >>> verify_proof(txs[0], proof, tree.root())
        True
        >>> verify_proof(b"Fake transaction", proof, tree.root())
        False
    """
    current = sha256d(leaf)
    for sibling, is_right in proof:
        if is_right:
            current = sha256d(current + sibling)
        else:
            current = sha256d(sibling + current)
    return current.hex() == root_hex

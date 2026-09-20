"""
sbsdi_blockchain.lab2.merkle
=============================
Lab 2 (Lecture 3) — Module 4 (partial): Merkle Root computation.

Source: 3-dis_blockchain_lab_handout.docx, blockchain_lab.py — Module 4
Dependencies: stdlib only (hashlib, json)

The Merkle root summarises all transactions in a block into a single hash.
Tampering with any transaction changes the root, making the block's hash invalid.
"""

import hashlib
import json


def merkle_root(items: list) -> str:
    """
    Compute a Merkle root over a list of JSON-serialisable items.

    Each item is hashed with SHA-256 (single, not double-SHA256 — the simpler
    Bitcoin-style double-hash is in lab3.merkle). Pairs of hashes are combined
    by concatenation + SHA-256 until a single root remains.

    If the number of hashes at any level is odd, the last hash is duplicated
    before pairing — the standard Bitcoin padding rule.


    Args:
        items: list of dicts, strings, or any JSON-serialisable values.

    Returns:
        64-character hex string (SHA-256 Merkle root).
    """
    if not items:
        return hashlib.sha256(b"").hexdigest()

    # Leaf layer: hash each item
    layer = [
        hashlib.sha256(json.dumps(i, sort_keys=True).encode()).hexdigest()
        for i in items
    ]

    # Reduce layer-by-layer until only the root remains
    while len(layer) > 1:
        if len(layer) % 2 == 1:
            layer.append(layer[-1])  # duplicate last hash if odd count
        layer = [
            hashlib.sha256((layer[i] + layer[i + 1]).encode()).hexdigest()
            for i in range(0, len(layer), 2)
        ]

    return layer[0]

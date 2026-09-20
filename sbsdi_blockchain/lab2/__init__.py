"""
sbsdi_blockchain.lab2
======================
Lab 2 — Lecture 3: Distributed Blockchain Systems.

Source: 3-dis_blockchain_lab_handout.docx
Dependencies: ecdsa>=0.18  (stdlib for all other modules)

pip install sbsdi-blockchain    ← installs ecdsa automatically

Exports:
    DLT / Network:
        Ledger                  — one node's local ledger copy
        DistributedLedgerNetwork— naive DLT with online/offline state

    P2P Gossip:
        PeerNode                — gossip node with TTL-limited relay
        build_ring              — convenience: build an N-node ring topology

    Blockchain (Module 4 + 5):
        merkle_root             — compute Merkle root over a list of items
        Block                   — block with Merkle root and PoW mining
        Wallet                  — secp256k1 ECDSA keypair + address
        Transaction             — signed transfer with lifecycle states
        Mempool                 — fee-prioritised pending transaction pool
        get_balance             — scan chain to compute address balance
        Blockchain              — full PoW blockchain with mempool + mining

    Capstone:
        ConsensusNode           — PeerNode + Blockchain + longest-chain gossip
"""
from __future__ import annotations


from .dlt import DistributedLedgerNetwork, Ledger
from .p2p import PeerNode, build_ring
from .merkle import merkle_root
from .block import Block
from .wallet import Wallet
from .transaction import Transaction
from .mempool import Mempool, get_balance
from .blockchain import Blockchain
from .consensus import ConsensusNode

__all__ = [
    # DLT
    "Ledger",
    "DistributedLedgerNetwork",
    # P2P
    "PeerNode",
    "build_ring",
    # Blockchain
    "merkle_root",
    "Block",
    "Wallet",
    "Transaction",
    "Mempool",
    "get_balance",
    "Blockchain",
    # Capstone
    "ConsensusNode",
]

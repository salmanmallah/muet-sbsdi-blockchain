"""
sbsdi_blockchain.lab4
======================
Lab 4 — Lecture 5: Consensus Mechanisms.

Source: 5_Dis_Blockchain_Consensus_Mechanisms_Handou.docx
Dependencies: stdlib only (hashlib, json, time, random)
              "Nothing needs to be pip installed for these labs." — official handout

pip install sbsdi-blockchain    ← still works, no extra packages needed for lab4

Exports:
    Proof-of-Work:
        Block           — PoW block (json.dumps hash + nonce)
        mine_block      — find nonce for difficulty target
        PoWBlockchain   — full PoW chain with add_block + is_valid

    Proof-of-Stake:
        Validator           — node with stake + slashed flag
        select_validator    — stake-weighted random selection
        propose_block       — selected validator proposes a block
        slash               — penalise a misbehaving validator

    PBFT:
        Node            — honest or Byzantine node with vote()
        pbft_consensus  — run 3-phase PBFT, return consensus result
        build_network   — helper: build N-node network with M Byzantine

    Decentralisation:
        nakamoto_coefficient — min entities to control >50% of resource

    Scalability:
        calculate_tps           — TPS = (block_size / tx_size) / block_time
        propagation_estimate    — block propagation latency in ms
        sharded_tps             — effective TPS with sharding
        pbft_message_count      — PBFT O(n²) message count
"""

from .pow import Block, mine_block, PoWBlockchain
from .pos import Validator, select_validator, propose_block, slash
from .pbft import Node, pbft_consensus, build_network
from .decentralization import nakamoto_coefficient
from .scalability import (
    calculate_tps,
    propagation_estimate,
    sharded_tps,
    pbft_message_count,
)

__all__ = [
    # PoW
    "Block",
    "mine_block",
    "PoWBlockchain",
    # PoS
    "Validator",
    "select_validator",
    "propose_block",
    "slash",
    # PBFT
    "Node",
    "pbft_consensus",
    "build_network",
    # Decentralisation
    "nakamoto_coefficient",
    # Scalability
    "calculate_tps",
    "propagation_estimate",
    "sharded_tps",
    "pbft_message_count",
]

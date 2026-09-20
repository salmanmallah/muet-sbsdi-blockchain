"""
sbsdi_blockchain.lab4.pbft
============================
Lab 4 (Lecture 5) — Lab 3: Practical Byzantine Fault Tolerance (PBFT).

Source: 5_Dis_Blockchain_Consensus_Mechanisms_Handou.docx, lab3_pbft.py
Dependencies: stdlib only (random)

PBFT guarantees consensus as long as fewer than 1/3 of nodes are Byzantine.
With n total nodes, f = (n-1)//3 is the maximum tolerable faulty nodes.
A quorum requires 2f+1 matching votes.
"""
from __future__ import annotations


import random
from collections import Counter


class Node:
    """
    A node in a PBFT consensus round.

    Byzantine nodes randomly vote for a conflicting value to simulate
    a real-world adversary trying to disrupt consensus.
    """

    def __init__(self, node_id: int, is_byzantine: bool = False):
        self.node_id = node_id
        self.is_byzantine = is_byzantine
        self.log: list = []

    def vote(self, proposed_value) -> str:
        """
        Vote on *proposed_value*.
        Byzantine nodes randomly return 'CORRUPT_VALUE' or the real value.
        """
        if self.is_byzantine:
            return random.choice(["CORRUPT_VALUE", proposed_value])
        return str(proposed_value)

    def __repr__(self) -> str:
        kind = "Byzantine" if self.is_byzantine else "Honest"
        return f"Node({self.node_id}, {kind})"


def pbft_consensus(nodes: list[Node], proposed_value: str) -> dict:
    """
    Run a simplified 3-phase PBFT consensus round.

    Phase 1 — Pre-Prepare: primary broadcasts proposed_value to all nodes.
    Phase 2 — Prepare:     each node votes (Byzantine nodes may lie).
    Phase 3 — Commit:      tally votes; if 2f+1 agree, consensus is reached.


    Returns a dict with:
        n, f, quorum, votes, vote_counts, winner, consensus_reached
    """
    n = len(nodes)
    f = (n - 1) // 3
    quorum = 2 * f + 1

    # Phase 2: Prepare — each node votes
    votes = [node.vote(proposed_value) for node in nodes]

    # Phase 3: Commit — tally and check quorum
    vote_counts = dict(Counter(votes))
    winner, count = Counter(votes).most_common(1)[0]
    consensus_reached = count >= quorum

    return {
        "n": n,
        "f": f,
        "quorum": quorum,
        "votes": votes,
        "vote_counts": vote_counts,
        "winner": winner,
        "winner_votes": count,
        "consensus_reached": consensus_reached,
    }


def build_network(n: int, num_byzantine: int = 0) -> list[Node]:
    """
    Build a network of *n* nodes, with *num_byzantine* marked as Byzantine.

    The first *num_byzantine* nodes are Byzantine; the rest are honest.
    """
    nodes = []
    for i in range(n):
        is_byzantine = i < num_byzantine
        nodes.append(Node(i + 1, is_byzantine=is_byzantine))
    return nodes

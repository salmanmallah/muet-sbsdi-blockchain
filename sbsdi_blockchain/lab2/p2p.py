"""
sbsdi_blockchain.lab2.p2p
==========================
Lab 2 (Lecture 3) — Module 2: Peer-to-Peer Gossip Network.

Source: 3-dis_blockchain_lab_handout.docx, blockchain_lab.py — Module 2
Dependencies: stdlib only (random)

Demonstrates how a message propagates across a ring topology where each
node is only directly connected to two neighbours, yet every node receives
the message via gossip relaying.
"""

import random


class PeerNode:
    """
    A node in a P2P gossip network.

    Each node has:
    - node_id      : unique string identifier (e.g. "P1")
    - peers        : set of directly connected PeerNode objects
    - inbox        : list of all messages received (including relayed ones)
    - seen_messages: set of message_ids already processed (deduplication)
    """

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.peers: set["PeerNode"] = set()
        self.inbox: list = []
        self.seen_messages: set[str] = set()

    def connect(self, other: "PeerNode") -> None:
        """
        Create a symmetric (bidirectional) connection.
        A knows B, B knows A.
        """
        self.peers.add(other)
        other.peers.add(self)

    def broadcast(self, message, message_id: str | None = None, ttl: int = 10) -> str:
        """
        Originate a broadcast from this node.

        Assigns a random message_id if not provided, then starts gossip.
        Returns the message_id so the caller can track it.
        """
        message_id = message_id or f"{self.node_id}-{random.randint(0, 1_000_000)}"
        self._gossip(message, message_id, sender=None, ttl=ttl)
        return message_id

    def _gossip(
        self,
        message,
        message_id: str,
        sender: "PeerNode | None",
        ttl: int,
    ) -> None:
        """
        Internal gossip relay: accept the message (if new and TTL > 0),
        add to inbox, then forward to all peers except the sender.

        TTL (time-to-live) prevents infinite loops on cyclic graphs.
        """
        if message_id in self.seen_messages or ttl <= 0:
            return
        self.seen_messages.add(message_id)
        self.inbox.append(message)
        for peer in self.peers:
            if peer is not sender:
                peer._gossip(message, message_id, sender=self, ttl=ttl - 1)

    def __repr__(self) -> str:
        return f"PeerNode({self.node_id!r}, peers={[p.node_id for p in self.peers]})"


def build_ring(n: int) -> list[PeerNode]:
    """
    Build a ring topology of *n* PeerNodes (P1 … Pn).

    Each node connects to its two immediate neighbours only.
    A message still reaches every node via gossip relaying.


    Usage:
        from sbsdi_blockchain.lab2 import build_ring
        nodes = build_ring(8)
        nodes[0].broadcast({"tx": "Alice pays Bob 5 coins"})
        for n in nodes:
            print(f"  {n.node_id} received: {n.inbox}")
    """
    nodes = [PeerNode(f"P{i}") for i in range(1, n + 1)]
    for i in range(n):
        nodes[i].connect(nodes[(i + 1) % n])
    return nodes

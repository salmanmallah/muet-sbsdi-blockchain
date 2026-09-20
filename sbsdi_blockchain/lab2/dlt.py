"""
sbsdi_blockchain.lab2.dlt
==========================
Lab 2 (Lecture 3) — Module 1: Distributed Ledger Technology.

Source: 3-dis_blockchain_lab_handout.docx, blockchain_lab.py — Module 1
Dependencies: stdlib only

Simulates a naive network of nodes, each holding their own local copy
of a ledger, with broadcast, offline/online state, and eventual consistency.
"""


class Ledger:
    """
    One node's local copy of the ledger — an ordered list of entries.
    """

    def __init__(self, owner: str):
        self.owner = owner
        self.entries: list = []

    def add_entry(self, entry) -> None:
        """Append a new entry to this node's local ledger."""
        self.entries.append(entry)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ledger):
            return NotImplemented
        return self.entries == other.entries

    def __repr__(self) -> str:
        return f"Ledger(owner={self.owner!r}, entries={len(self.entries)})"


class DistributedLedgerNetwork:
    """
    A naive network of ledger-holding nodes with online/offline state.

    Demonstrates eventual consistency: nodes that go offline miss broadcasts
    and need to be synced before the network is consistent again.
    """

    def __init__(self, node_names: list[str]):
        self.nodes: dict[str, Ledger] = {
            name: Ledger(name) for name in node_names
        }
        self.offline: set[str] = set()

    def go_offline(self, name: str) -> None:
        """Mark node *name* as offline — it will miss future broadcasts."""
        self.offline.add(name)

    def go_online(self, name: str) -> None:
        """Bring node *name* back online (does NOT auto-sync)."""
        self.offline.discard(name)

    def broadcast_entry(self, entry, origin_node: str) -> None:
        """
        Broadcast *entry* to all currently ONLINE nodes.

        Nodes in self.offline receive nothing — they fall behind.
        """
        for name, ledger in self.nodes.items():
            if name not in self.offline:
                ledger.add_entry(entry)

    def sync_node(self, name: str) -> None:
        """
        Bring a previously-offline node up to date with the majority state.

        Uses the longest ledger among online nodes as the reference
        (simple majority heuristic — not full BFT).
        """
        reference = max(self.nodes.values(), key=lambda l: len(l.entries))
        self.nodes[name].entries = list(reference.entries)

    def is_consistent(self) -> bool:
        """
        Return True if all ONLINE nodes have identical ledger contents.
        """
        ledgers = [
            l for name, l in self.nodes.items() if name not in self.offline
        ]
        if not ledgers:
            return True
        return all(l == ledgers[0] for l in ledgers[1:])

    def __repr__(self) -> str:
        online = [n for n in self.nodes if n not in self.offline]
        return f"DistributedLedgerNetwork(nodes={list(self.nodes)}, offline={list(self.offline)}, online={online})"

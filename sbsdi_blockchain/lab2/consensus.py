"""
sbsdi_blockchain.lab2.consensus
=================================
Lab 2 (Lecture 3) — Capstone: ConsensusNode (longest-chain gossip).

Source: 3-dis_blockchain_lab_handout.docx, blockchain_lab.py — Capstone
Dependencies: stdlib only (builds on PeerNode + Blockchain)

ConsensusNode extends PeerNode with a local Blockchain. When a node
receives a block announcement, it adopts the longest valid chain (Nakamoto
consensus) and relays the announcement to further peers via gossip.
"""
from __future__ import annotations


from .blockchain import Blockchain
from .p2p import PeerNode


class ConsensusNode(PeerNode):
    """
    A P2P node that also maintains a local Blockchain and participates
    in Nakamoto-style longest-chain consensus.
    """

    def __init__(self, node_id: str, blockchain: Blockchain):
        super().__init__(node_id)
        self.blockchain = blockchain

    def receive_block_announcement(
        self,
        remote_len: int,
        remote_valid: bool,
        remote_chain: list,
        sender: "ConsensusNode | None" = None,
    ) -> None:
        """
        Handle an incoming chain announcement.

        If the remote chain is valid AND longer than ours, adopt it.
        Then relay (gossip) the announcement to all ConsensusNode peers
        except the sender.
        """
        if remote_valid and remote_len > len(self.blockchain.chain):
            self.blockchain.chain = remote_chain

        # Relay to further peers (gossip)
        for peer in self.peers:
            if peer is not sender and isinstance(peer, ConsensusNode):
                peer.receive_block_announcement(
                    remote_len, remote_valid, remote_chain, sender=self
                )

    def broadcast_new_block(self) -> None:
        """
        Announce this node's current chain to all connected ConsensusNode peers.
        """
        for peer in self.peers:
            if isinstance(peer, ConsensusNode):
                peer.receive_block_announcement(
                    len(self.blockchain.chain),
                    self.blockchain.is_chain_valid(),
                    self.blockchain.chain,
                    sender=self,
                )

    def __repr__(self) -> str:
        return (
            f"ConsensusNode({self.node_id!r}, "
            f"chain_len={len(self.blockchain.chain)})"
        )

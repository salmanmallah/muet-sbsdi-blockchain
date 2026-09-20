"""
Tests for Module 2 (Distributed Ledgers & P2P Networks).
"""
import pytest
from sbsdi_blockchain.lab2 import (
    DistributedLedgerNetwork,
    build_ring,
    merkle_root,
    Block,
    Wallet,
    Transaction,
    Blockchain,
    ConsensusNode,
)


def test_dlt_network_and_sync():
    network = DistributedLedgerNetwork(["Node_A", "Node_B", "Node_C"])
    network.broadcast_entry({"tx": "Alice pays Bob 10"}, origin_node="Node_A")
    assert network.is_consistent() is True

    # Offline simulation
    network.go_offline("Node_C")
    network.broadcast_entry({"tx": "Bob pays Carol 5"}, origin_node="Node_A")
    # When Node_C comes back online without syncing, the online network is inconsistent
    network.go_online("Node_C")
    assert network.is_consistent() is False

    # Sync offline node
    network.sync_node("Node_C")
    assert network.is_consistent() is True


def test_p2p_gossip_ring():
    nodes = build_ring(6)
    nodes[0].broadcast("Announcement: Block 10 Mined")
    # All nodes should have received the message via gossip relay
    assert all(len(n.inbox) == 1 for n in nodes)


def test_merkle_root_calculation():
    items = ["tx1", "tx2", "tx3", "tx4"]
    root = merkle_root(items)
    assert isinstance(root, str)
    assert len(root) == 64


def test_wallet_and_transaction_signature():
    alice = Wallet("Alice")
    bob = Wallet("Bob")

    assert alice.address() != bob.address()

    # Create & sign transaction
    tx = Transaction(alice, bob.address(), amount=15.0, fee=1.0)
    tx.sign()
    assert tx.is_valid() is True


def test_blockchain_mempool_and_mining():
    alice = Wallet("Alice")
    bob = Wallet("Bob")

    genesis_grants = {alice.address(): 100.0}
    bc = Blockchain(difficulty=2, genesis_grants=genesis_grants)

    tx = Transaction(alice, bob.address(), amount=20.0, fee=1.0)
    tx.sign()

    bc.submit_transaction(tx)
    assert len(bc.mempool) == 1

    mined_block = bc.mine_pending_transactions()
    assert mined_block is not None
    assert bc.is_chain_valid() is True

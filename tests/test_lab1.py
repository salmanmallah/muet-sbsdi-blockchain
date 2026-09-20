"""
Tests for Module 1 (Blockchain Fundamentals & Proof-of-Work).
"""
import pytest
from sbsdi_blockchain.lab1 import Block, Blockchain, time_mining


def test_block_creation_and_hash():
    block = Block(0, 1000.0, "Genesis Block", "0")
    assert block.index == 0
    assert block.data == "Genesis Block"
    assert block.previous_hash == "0"
    assert len(block.hash) == 64


def test_blockchain_mining_and_integrity():
    bc = Blockchain()
    assert len(bc.chain) == 1
    assert bc.is_chain_valid() is True

    # Add block with difficulty 3
    b1 = bc.add_block("Tx1: Alice -> Bob 10", difficulty=3)
    assert b1.index == 1
    assert b1.hash.startswith("000")
    assert bc.is_chain_valid() is True

    # Add second block
    b2 = bc.add_block("Tx2: Bob -> Carol 5", difficulty=3)
    assert b2.index == 2
    assert b2.previous_hash == b1.hash
    assert bc.is_chain_valid() is True


def test_blockchain_tamper_detection():
    bc = Blockchain()
    bc.add_block("Original Data", difficulty=2)
    assert bc.is_chain_valid() is True

    # Tamper with block data
    bc.chain[1].data = "Hacked Data"
    assert bc.is_chain_valid() is False


def test_time_mining_benchmark():
    bc = Blockchain()
    elapsed = time_mining(bc, "Benchmark Block", difficulty=2)
    assert isinstance(elapsed, float)
    assert elapsed >= 0.0

"""
Tests for Module 4 (Consensus Mechanisms & Network Metrics).
"""
import pytest
from sbsdi_blockchain.lab4 import (
    Block,
    mine_block,
    PoWBlockchain,
    Validator,
    select_validator,
    propose_block,
    slash,
    Node,
    pbft_consensus,
    build_network,
    nakamoto_coefficient,
    calculate_tps,
    propagation_estimate,
    sharded_tps,
    pbft_message_count,
)


def test_pow_blockchain_and_mining():
    chain = PoWBlockchain(difficulty=3)
    assert len(chain.chain) == 1
    assert chain.is_valid() is True

    b1 = chain.add_block(["Alice->Bob: 10", "Bob->Carol: 5"])
    assert b1.hash.startswith("000")
    assert chain.is_valid() is True


def test_pos_validator_selection_and_slashing():
    v1 = Validator("Validator_A", stake=300)
    v2 = Validator("Validator_B", stake=100)
    validators = [v1, v2]

    elected = select_validator(validators)
    assert elected in validators

    # Slashing
    slash(v1, penalty=0.5)
    assert v1.slashed is True
    assert v1.stake == 150


def test_pbft_consensus_with_byzantine_faults():
    # 7 nodes, 2 Byzantine, quorum 5
    nodes = build_network(7, num_byzantine=2)
    result = pbft_consensus(nodes, "COMMIT_BLOCK_42")
    assert result["consensus_reached"] is True
    assert result["winner"] == "COMMIT_BLOCK_42"
    assert result["winner_votes"] >= 5


def test_decentralization_nakamoto_coefficient():
    pools = [21, 18, 15, 12, 10, 9, 8, 7]
    nc = nakamoto_coefficient(pools)
    assert nc == 3


def test_scalability_metrics():
    tps = calculate_tps(block_size_bytes=1_000_000, avg_tx_size_bytes=250, block_time_seconds=600)
    assert pytest.approx(tps, 0.01) == 6.67

    msgs = pbft_message_count(7)
    assert msgs == 84

    stps = sharded_tps(base_tps=7.0, num_shards=64, cross_shard_overhead=0.1)
    assert pytest.approx(stps, 0.1) == 403.2

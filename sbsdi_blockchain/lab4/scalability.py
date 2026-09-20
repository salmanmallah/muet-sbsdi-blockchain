"""
sbsdi_blockchain.lab4.scalability
====================================
Lab 4 (Lecture 5) — Lab 5: Blockchain Scalability Analysis.

Source: 5_Dis_Blockchain_Consensus_Mechanisms_Handou.docx, lab5_scalability.py
Dependencies: stdlib only

Provides analytical models for:
- Transaction throughput (TPS)
- Block propagation latency estimate
- Sharding TPS improvement
- PBFT message complexity (O(n²))
"""
from __future__ import annotations



def calculate_tps(block_size_bytes: int, avg_tx_size_bytes: int, block_time_seconds: float) -> float:
    """
    Estimate transactions per second (TPS) for a blockchain.

    Formula: TPS = (block_size / avg_tx_size) / block_time


    Example — Bitcoin approximation:
        >>> calculate_tps(1_000_000, 250, 600)
        6.666...

    Args:
        block_size_bytes:   maximum block size in bytes (e.g. 1_000_000 for Bitcoin 1 MB)
        avg_tx_size_bytes:  average transaction size in bytes (e.g. 250)
        block_time_seconds: average time between blocks in seconds (e.g. 600 for Bitcoin)

    Returns:
        float — transactions per second
    """
    txs_per_block = block_size_bytes / avg_tx_size_bytes
    return txs_per_block / block_time_seconds


def propagation_estimate(
    block_size_bytes: int,
    bandwidth_bps: float,
    num_hops: int,
    processing_ms_per_hop: float = 50.0,
) -> float:
    """
    Estimate block propagation latency in milliseconds.

    Models total latency as: transmission time + processing time per hop.

    Formula: latency_ms = (block_size_bytes * 8 / bandwidth_bps) * 1000 * num_hops
                         + processing_ms_per_hop * num_hops

    Args:
        block_size_bytes:       size of the block (bytes)
        bandwidth_bps:          network bandwidth in bits per second
        num_hops:               number of network hops to reach most nodes
        processing_ms_per_hop:  validation + forwarding time per node (ms)

    Returns:
        float — estimated propagation latency in milliseconds
    """
    transmission_ms = (block_size_bytes * 8 / bandwidth_bps) * 1000
    total_latency_ms = (transmission_ms + processing_ms_per_hop) * num_hops
    return total_latency_ms


def sharded_tps(
    base_tps: float,
    num_shards: int,
    cross_shard_overhead: float = 0.1,
) -> float:
    """
    Estimate effective TPS with sharding.

    Sharding splits the network into *num_shards* parallel chains, each
    processing transactions independently. Cross-shard transactions incur
    overhead (default 10%).

    Formula: effective_tps = base_tps * num_shards * (1 - cross_shard_overhead)


    Args:
        base_tps:               TPS of a single shard
        num_shards:             number of shards
        cross_shard_overhead:   fraction of capacity lost to cross-shard coordination

    Returns:
        float — effective TPS across all shards
    """
    return base_tps * num_shards * (1 - cross_shard_overhead)


def pbft_message_count(n: int) -> int:
    """
    Count the total PBFT messages for one consensus round with *n* nodes.

    PBFT has O(n²) message complexity:
    - Pre-prepare:  1 message (primary → all)
    - Prepare:      n * (n-1) messages (each node → all others)
    - Commit:       n * (n-1) messages (each node → all others)
    Total ≈ 2n² messages


    Example:
        >>> pbft_message_count(7)
        84
        >>> pbft_message_count(100)
        19800

    This quadratic growth explains why PBFT is unsuitable for large
    permissionless networks but works well in small consortium chains.
    """
    return 2 * n * (n - 1)

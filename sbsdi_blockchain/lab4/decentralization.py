"""
sbsdi_blockchain.lab4.decentralization
=========================================
Lab 4 (Lecture 5) — Lab 4: Measuring Decentralisation.

Source: 5_Dis_Blockchain_Consensus_Mechanisms_Handou.docx, decentralization.py
Dependencies: stdlib only

The Nakamoto Coefficient measures how many entities need to collude to
control more than 50% of a network's resources (hash power, stake, etc.).
A lower coefficient = less decentralised.
"""


def nakamoto_coefficient(shares: list[float]) -> int:
    """
    Compute the Nakamoto Coefficient for a set of entity shares.

    *shares* is a list of each entity's percentage of control,
    e.g. [21, 18, 15, 12, 10, 9, 8, 7] for mining pool hash-power shares.

    Algorithm: sort descending, accumulate until >50% — the count at that
    point is the Nakamoto Coefficient.


    Example:
        >>> nakamoto_coefficient([21, 18, 15, 12, 10, 9, 8, 7])
        3
        # Pools with 21+18+15 = 54% > 50% — only 3 pools needed to collude.

    Args:
        shares: list of numeric values (% or absolute) representing each
                entity's control. Does NOT need to sum to 100.

    Returns:
        int — minimum number of entities needed to control >50%.
    """
    shares_sorted = sorted(shares, reverse=True)
    cumulative = 0.0
    count = 0
    for s in shares_sorted:
        cumulative += s
        count += 1
        if cumulative > 50:
            return count
    return count  # degenerate case: no single entity crosses 50%

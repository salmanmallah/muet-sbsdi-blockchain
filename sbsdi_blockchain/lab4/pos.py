"""
sbsdi_blockchain.lab4.pos
===========================
Lab 4 (Lecture 5) — Lab 2: Proof-of-Stake.

Source: 5_Dis_Blockchain_Consensus_Mechanisms_Handou.docx, lab2_pos.py
Dependencies: stdlib only (random)
"""
from __future__ import annotations


import random


class Validator:
    """
    A PoS validator node with a stake (amount of coins locked as collateral).

    Validators with higher stake have a proportionally higher probability
    of being selected to propose the next block.
    """

    def __init__(self, name: str, stake: float):
        self.name = name
        self.stake = stake
        self.slashed = False

    def __repr__(self) -> str:
        return f"{self.name}(stake={self.stake}, slashed={self.slashed})"


def select_validator(validators: list[Validator]) -> Validator:
    """
    Stake-weighted random selection — higher stake = higher probability.

    Only considers non-slashed validators.
    """
    active = [v for v in validators if not v.slashed]
    if not active:
        raise ValueError("No active (non-slashed) validators available.")
    total = sum(v.stake for v in active)
    pick = random.uniform(0, total)
    cumulative = 0.0
    for v in active:
        cumulative += v.stake
        if pick <= cumulative:
            return v
    return active[-1]  # fallback (floating-point safety)


def propose_block(validator: Validator, transactions: list) -> dict:
    """
    The selected validator proposes the next block.
    """
    return {
        "proposer": validator.name,
        "transactions": transactions,
        "stake_used": validator.stake,
    }


def slash(validator: Validator, penalty: float = 0.5) -> None:
    """
    Slash a misbehaving validator — reduce their stake by *penalty* fraction
    and mark them as slashed (they can no longer be selected).
    """
    validator.stake *= 1 - penalty
    validator.slashed = True

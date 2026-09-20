"""
sbsdi_blockchain.lab1.pow
===========================
Lab 1 (Lecture 2) — Step 3: Proof-of-Work mining utilities.

Source: 2_Dis_Blockchain_Intro_Lab.docx, Step 3.3
Dependencies: stdlib only (time)
"""

import time


def time_mining(blockchain, data: str, difficulty: int) -> float:
    """
    Add a block to *blockchain* at *difficulty* and return the elapsed
    time in seconds.

    Usage:
        from sbsdi_blockchain.lab1 import Blockchain, time_mining
        chain = Blockchain()
        elapsed = time_mining(chain, "Test block", difficulty=5)
        print(f"Difficulty 5 took {elapsed:.3f}s")
    """
    start = time.time()
    blockchain.add_block(data, difficulty=difficulty)
    return time.time() - start


def compare_difficulties(difficulties: list[int], data: str = "Timing test") -> dict:
    """
    Convenience helper: run time_mining for each value in *difficulties*
    and return a dict mapping difficulty → seconds.

    Usage:
        from sbsdi_blockchain.lab1 import Blockchain, compare_difficulties
        results = compare_difficulties([3, 4, 5, 6])
        for d, t in results.items():
            print(f"  difficulty={d}  {t:.3f}s")
    """
    from .blockchain import Blockchain

    results = {}
    for d in difficulties:
        chain = Blockchain()
        elapsed = time_mining(chain, data, difficulty=d)
        results[d] = elapsed
    return results

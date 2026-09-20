"""
sbsdi_blockchain.lab1
======================
Lab 1 — Lecture 2: Building Your First Blockchain in Python.

Source: 2_Dis_Blockchain_Intro_Lab.docx
Dependencies: stdlib only (hashlib, json, time) — no pip install needed.

Exports:
    Block          — single block with SHA-256 hash + nonce
    Blockchain     — linked chain with genesis block, mining, validation
    time_mining    — time how long mining takes at a given difficulty
    compare_difficulties — compare multiple difficulties
"""

from .block import Block
from .blockchain import Blockchain
from .pow import time_mining, compare_difficulties

__all__ = [
    "Block",
    "Blockchain",
    "time_mining",
    "compare_difficulties",
]

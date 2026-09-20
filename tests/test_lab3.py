"""
Tests for Module 3 (Cryptographic Foundations & Ethereum Primitives).
"""
from __future__ import annotations

import pytest
from sbsdi_blockchain.lab3 import (
    sha256,
    avalanche_demo,
    keccak256,
    proof_of_work,
    generate_keypair,
    derive_eth_address,
    sign,
    verify,
    sha256d,
    MerkleTree,
    verify_proof,
    capstone,
)


def test_sha256_and_avalanche():
    h1 = sha256(b"MUET Blockchain")
    h2 = sha256(b"MUET Blockchain.")
    assert len(h1) == 64
    assert len(h2) == 64
    assert h1 != h2

    demo = avalanche_demo(b"MUET Blockchain", b"MUET Blockchain.")
    assert demo["differing_hex_chars"] > 20


def test_keccak256():
    kh = keccak256(b"MUET Blockchain")
    assert len(kh) == 64
    assert isinstance(kh, str)


def test_proof_of_work_standalone():
    nonce, block_hash = proof_of_work(b"TestData", difficulty=3)
    assert block_hash.startswith("000")
    assert isinstance(nonce, int)


def test_ecdsa_keypair_and_signatures():
    priv, pub = generate_keypair()
    msg = b"Transfer 100 SBSDI-Coins"

    sig = sign(priv, msg)
    assert verify(pub, sig, msg) is True
    assert verify(pub, sig, b"Tampered Message") is False


def test_ethereum_address_derivation():
    _, pub = generate_keypair()
    eth_addr = derive_eth_address(pub)
    assert eth_addr.startswith("0x")
    assert len(eth_addr) == 42


def test_merkle_tree_and_spv_proof():
    txs = [b"tx0", b"tx1", b"tx2", b"tx3"]
    tree = MerkleTree(txs)
    root = tree.root()
    assert len(root) == 64

    # SPV Proof for tx index 2
    proof = tree.get_proof(index=2)
    assert verify_proof(txs[2], proof, root) is True
    assert verify_proof(b"fake_tx", proof, root) is False


def test_capstone_mini_blockchain():
    priv, pub = generate_keypair()
    mined_block = capstone.build_signed_block(
        signing_key=priv,
        tx_data=b"Alice->Bob: 25.0",
        prev_hash="0" * 64,
        difficulty=2
    )
    assert mined_block.hash.startswith("00")
    assert len(mined_block.merkle_root) == 64
